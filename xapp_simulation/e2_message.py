import socket
import datetime
from ran_messages_pb2 import (
    RAN_message,
    RAN_message_type,
    RAN_indication_request,
    RAN_control_request,
    RAN_parameter,
)
from google.protobuf.json_format import MessageToJson

def timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def send_indication_request(sock: socket.socket, target_params):
    req = RAN_indication_request()
    req.target_params.extend(target_params)

    msg = RAN_message()
    msg.msg_type = RAN_message_type.INDICATION_REQUEST
    msg.ran_indication_request.CopyFrom(req)

    serialized = msg.SerializeToString()
    sock.send(serialized)

    print(f"[{timestamp()}] [SEND] Gửi bản tin Indication Request qua TCP")
    print(MessageToJson(msg, indent=2))

def handle_received_message(data: bytes, addr=None):
    msg = RAN_message()
    msg.ParseFromString(data)

    print(f"[{timestamp()}] [RECV] Nhận bản tin từ server")
    print(f" - Loại bản tin: {RAN_message_type.Name(msg.msg_type)}")

    if msg.msg_type == RAN_message_type.INDICATION_RESPONSE:
        for param in msg.ran_indication_response.param_map:
            print(f"   + Param: {param.key}, type: {param.WhichOneof('value')}")
    else:
        print("   + Nội dung không phải bản tin Indication Response.")

    print("↪ Nội dung chi tiết:")
    print(MessageToJson(msg, indent=2))

def send_control(sock: socket.socket):
    ctrl_req = RAN_control_request()
    entry = ctrl_req.target_param_map.add()
    entry.key = RAN_parameter.SCHED_CONTROL
    entry.sche_ctrl.max_cell_allocable_prbs = 42

    msg = RAN_message()
    msg.msg_type = RAN_message_type.CONTROL
    msg.ran_control_request.CopyFrom(ctrl_req)

    serialized = msg.SerializeToString()
    sock.send(serialized)

    print(f"[{timestamp()}] [SEND] Gửi bản tin Control qua TCP")
    print(MessageToJson(msg, indent=2))
