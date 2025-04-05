import socket
import time
import select

from ran_messages_pb2 import RAN_parameter
from e2_message import send_indication_request, handle_received_message


def main():
    server_addr = ("hpg1.0x2f0713.id.vn", 6600)
    interval = 5  # giây
    last_sent_time = 0

    # Tạo socket TCP và connect tới server
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.connect(server_addr)
    tcp_sock.setblocking(False)  # không block khi recv

    print(f"[INFO] Đã kết nối TCP tới {server_addr[0]}:{server_addr[1]}")

    print("[INFO] Gửi định kỳ mỗi 5 giây và lắng nghe phản hồi...")

    while True:
        now = time.time()

        # Gửi yêu cầu định kỳ
        if now - last_sent_time >= interval:
            send_indication_request(tcp_sock, [RAN_parameter.GNB_ID,
                                               RAN_parameter.SOMETHING,
                                               RAN_parameter.UE_LIST])
            last_sent_time = now

        # Dùng select để kiểm tra có dữ liệu về không
        rlist, _, _ = select.select([tcp_sock], [], [], 1.0)
        if tcp_sock in rlist:
            try:
                data = tcp_sock.recv(8192)
                if not data:
                    print("[INFO] Server đóng kết nối")
                    break
                handle_received_message(data, server_addr)
            except BlockingIOError:
                continue


if __name__ == "__main__":
    main()
