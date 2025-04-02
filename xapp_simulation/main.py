import socket
import time
import select

from ran_messages_pb2 import RAN_message, RAN_message_type, RAN_indication_request, RAN_parameter
from e2_message import send_indication_request, handle_received_message


def main():
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind(("0.0.0.0", 6600))

    target = ("127.0.0.1", 6655)
    interval = 5  # giây
    last_sent_time = 0

    print("[INFO] Bắt đầu lắng nghe và gửi định kỳ mỗi 30 giây...")

    while True:
        now = time.time()
        if now - last_sent_time >= interval:
            send_indication_request(udp_sock, target, [RAN_parameter.GNB_ID, RAN_parameter.SOMETHING, RAN_parameter.UE_LIST,
                                                    #    RAN_parameter.SCHED_INFO_, RAN_parameter.SCHED_CONTROL, RAN_parameter.MAX_PRB,
                                                    #    RAN_parameter.USE_TRUE_GBR, RAN_parameter.SLICING_CONTROL
                                                       ])
            last_sent_time = now

        # Dùng select để chờ dữ liệu tối đa 1 giây
        rlist, _, _ = select.select([udp_sock], [], [], 1.0)
        if udp_sock in rlist:
            data, addr = udp_sock.recvfrom(8192)
            handle_received_message(data, addr)

if __name__ == "__main__":
    main()