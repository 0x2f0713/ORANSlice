#!/bin/bash

# Tên session tmux
SESSION_NAME="iperf_test"

# Lấy địa chỉ IP của các interface
IP1=$(ip -4 addr show oaitun_ue1 | grep -oP '(?<=inet\s)\d+(\.\d+){3}')
IP2=$(ip -4 addr show oaitun_ue2 | grep -oP '(?<=inet\s)\d+(\.\d+){3}')

if [ -z "$IP1" ] || [ -z "$IP2" ]; then
  echo "Không tìm thấy địa chỉ IP cho oaitun_ue1 hoặc oaitun_ue2."
  exit 1
fi

# Khởi động tmux session mới
tmux new-session -d -s $SESSION_NAME

# Chạy iperf3 ở pane đầu tiên với IP1
tmux send-keys -t $SESSION_NAME "iperf3 -c 192.168.70.139 -R -B $IP1" C-m

# Chia dọc màn hình thành 2 cửa sổ
tmux split-window -h -t $SESSION_NAME

# Chạy iperf3 ở pane thứ hai với IP2
tmux send-keys -t $SESSION_NAME:0.1 "iperf3 -c 192.168.70.140 -R -B $IP2" C-m

# Gắn vào session tmux
tmux attach -t $SESSION_NAME

