import socket
from ran_messages_pb2 import RAN_message, RAN_message_type, RAN_indication_request, RAN_control_request, RAN_parameter

def send_indication_request(sock: socket.socket, target_addr, target_params):
    req = RAN_indication_request()
    req.target_params.extend(target_params)

    msg = RAN_message()
    msg.msg_type = RAN_message_type.INDICATION_REQUEST
    msg.ran_indication_request.CopyFrom(req)

    serialized = msg.SerializeToString()
    sock.sendto(serialized, target_addr)
    print(f"[SEND] Gửi bản tin Indication Request tới {target_addr}")

def handle_received_message(data: bytes, addr):
    msg = RAN_message()
    msg.ParseFromString(data)

    if msg.msg_type == RAN_message_type.INDICATION_RESPONSE:
        print(f"[RECV] Nhận bản tin Indication Response từ {addr}")
        for param in msg.ran_indication_response.param_map:
            print(f" - Param: {param.key}, type: {param.WhichOneof('value')}")
    else:
        print(f"[RECV] Nhận bản tin khác loại: msg_type={msg.msg_type}")

def send_control(sock: socket.socket, target_addr):
    # Tạo một bản tin control mẫu
    ctrl_req = RAN_control_request()
    entry = ctrl_req.target_param_map.add()
    entry.key = RAN_parameter.SCHED_CONTROL
    entry.sche_ctrl.max_cell_allocable_prbs = 42  # Ví dụ: thiết lập PRB tối đa

    # Gói vào RAN_message
    msg = RAN_message()
    msg.msg_type = RAN_message_type.CONTROL
    msg.ran_control_request.CopyFrom(ctrl_req)

    # Serialize và gửi
    serialized = msg.SerializeToString()
    sock.sendto(serialized, target_addr)
    print(f"Đã gửi bản tin Control tới {target_addr}")