import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import random
from collections import deque

# ============================ 1. Hyperparams ===========================
GAMMA = 0.99
LR = 1e-3
BATCH_SIZE = 32
EPS_START = 1.0
EPS_END = 0.01
EPS_DECAY = 2000
MEMORY_SIZE = 10000
TARGET_UPDATE_FREQ = 100
NUM_EPISODES = 5000

MAX_RB_GROUP = 10
NUM_SLICES = 2

# Trọng số reward cho eMBB & Reliability
W_EMBB = 1.0
W_REL  = 2.0

# ============================ 2. Env for eMBB & Reliability =====================
class ResourceAllocationEnvReliability:
    """
    Môi trường toy-model:
      - slice_0: eMBB, có queue & throughput
      - slice_1: Reliability, có queue & reliability_metric

    state = [queue_0, throughput_0, queue_1, reliability_1]
    action = integer a => slice_0 nhận a nhóm RB, slice_1 nhận (MAX_RB_GROUP - a)
    reward = w0 * r_eMBB + w1 * r_Reliability
    """
    def __init__(self):
        self.queue = [10.0, 5.0]   # queue_0, queue_1
        self.thpt_0 = 0.0         # eMBB throughput tạm thời (slice_0)
        self.rel_metric_1 = 1.0   # Reliability metric (slice_1)
        
        # Ví dụ, queue_max để normalize, ...
        self.queue_max = 100.0
        
        # reset
        self.reset()

    def reset(self):
        self.queue = [random.uniform(5,15), random.uniform(3,10)]
        self.thpt_0 = random.uniform(0.0, 2.0)
        self.rel_metric_1 = random.uniform(0.8, 1.0)  # reliability ban đầu

        return self._get_state()

    def step(self, action):
        # Tính RB cho từng slice
        rb_0 = action
        rb_1 = MAX_RB_GROUP - action

        # (1) eMBB slice_0 => throughput
        # Giả sử throughput tỉ lệ thuận với rb_0 và bị giới hạn bởi queue
        # (chỉ là ví dụ)
        new_thpt_0 = rb_0 * 0.1
        # gói tin được truyền => queue giảm
        new_queue_0 = max(0, self.queue[0] - new_thpt_0)

        # (2) Reliability slice_1 => update reliability
        # Giả sử reliability = 1 - error_rate
        # error_rate giảm khi có nhiều rb_1 => reliability tăng dần tới 1.0
        # (chỉ là ví dụ toy)
        new_rel_1 = min(1.0, self.rel_metric_1 + 0.02 * rb_1)
        # queue_1 giảm 1 phần dựa vào "hiệu quả" (liên quan tới reliability)
        new_queue_1 = max(0, self.queue[1] - (0.2 * rb_1 * new_rel_1))

        # Tính reward:
        # r_eMBB = throughput_0 (hoặc log(throughput+1)), ...
        r_eMBB = new_thpt_0

        # r_Reliability = new_rel_1 (hoặc 1 - PER, etc.)
        r_REL = new_rel_1

        reward = W_EMBB * r_eMBB + W_REL * r_REL

        # Cập nhật env
        self.queue = [new_queue_0, new_queue_1]
        self.thpt_0 = new_thpt_0
        self.rel_metric_1 = new_rel_1
        
        # next_state
        next_state = self._get_state()

        done = False  # có thể đặt điều kiện done tuỳ mục đích

        return next_state, reward, done, {}

    def _get_state(self):
        return np.array([self.queue[0], 
                         self.thpt_0, 
                         self.queue[1],
                         self.rel_metric_1], dtype=np.float32)

# ============================ 3. DQN Network + Agent =====================
class DQNNetwork(nn.Module):
    def __init__(self, state_dim=4, action_dim=MAX_RB_GROUP+1):
        super(DQNNetwork, self).__init__()
        self.fc1 = nn.Linear(state_dim, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, action_dim)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

class DQNAgent:
    def __init__(self, state_dim=4, action_dim=MAX_RB_GROUP+1):
        self.state_dim = state_dim
        self.action_dim = action_dim

        self.eval_net = DQNNetwork(state_dim, action_dim)
        self.target_net = DQNNetwork(state_dim, action_dim)
        self.target_net.load_state_dict(self.eval_net.state_dict())

        self.memory = deque(maxlen=MEMORY_SIZE)
        self.optimizer = optim.Adam(self.eval_net.parameters(), lr=LR)
        self.learn_step_counter = 0

        self.epsilon = EPS_START

    def select_action(self, state):
        if random.random() < self.epsilon:
            action = random.randint(0, self.action_dim - 1)
        else:
            with torch.no_grad():
                s = torch.FloatTensor(state).unsqueeze(0)
                q_values = self.eval_net(s)
                action = torch.argmax(q_values, dim=1).item()
        return action

    def store_transition(self, s, a, r, s_, done):
        self.memory.append((s, a, r, s_, done))

    def update(self):
        if len(self.memory) < BATCH_SIZE:
            return

        batch = random.sample(self.memory, BATCH_SIZE)
        s, a, r, s_, d = zip(*batch)

        s  = torch.FloatTensor(s)
        a  = torch.LongTensor(a).unsqueeze(1)
        r  = torch.FloatTensor(r).unsqueeze(1)
        s_ = torch.FloatTensor(s_)
        d  = torch.FloatTensor(d).unsqueeze(1)

        q_eval = self.eval_net(s).gather(1, a)
        with torch.no_grad():
            q_next = self.target_net(s_).max(1, keepdim=True)[0]
        q_target = r + GAMMA * q_next * (1 - d)

        loss = nn.MSELoss()(q_eval, q_target)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        self.learn_step_counter += 1
        self.epsilon = max(EPS_END, 
                           EPS_START - (EPS_START - EPS_END) 
                           * self.learn_step_counter / EPS_DECAY)
        
        if self.learn_step_counter % TARGET_UPDATE_FREQ == 0:
            self.target_net.load_state_dict(self.eval_net.state_dict())

# ============================ 4. Training Loop ===========================
def train_dqn():
    env = ResourceAllocationEnvReliability()
    agent = DQNAgent()

    rewards_history = []
    for episode in range(NUM_EPISODES):
        state = env.reset()
        done = False
        ep_reward = 0
        step = 0
        while not done:
            action = agent.select_action(state)
            next_state, reward, done, _ = env.step(action)
            agent.store_transition(state, action, reward, next_state, done)
            agent.update()

            state = next_state
            ep_reward += reward
            step += 1

            if step > 100:  # giới hạn mỗi episode ~100 bước
                done = True

        rewards_history.append(ep_reward)
        if (episode+1) % 100 == 0:
            avg_r = np.mean(rewards_history[-100:])
            print(f"Episode {episode+1}, AvgReward={avg_r:.2f}, Eps={agent.epsilon:.3f}")

    return rewards_history

if __name__ == "__main__":
    final_r = train_dqn()
