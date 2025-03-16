import socket
import argparse


def udp_proxy(listen_ip, listen_port, target_ip, target_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((listen_ip, listen_port))

    print(f"🔥 Proxy server listening on {listen_ip}:{listen_port} → Forwarding to {target_ip}:{target_port}")

    while True:
        data, addr = sock.recvfrom(1024)

        # Фильтруем пакеты: принимаем только от 127.0.0.1
        if not addr[0].startswith("127."):
            print(f"🚨 Ignoring packet from unauthorized address {addr}")
            continue

        # Игнорируем пустые пакеты
        if not data.strip():
            print(f"🚨 Ignoring empty packet from {addr}")
            continue

        print(
            f"📥 Received '{data.decode('utf-8', errors='ignore')}' from {addr} — Forwarding to {target_ip}:{target_port}")
        sock.sendto(data, (target_ip, target_port))

        response, target_addr = sock.recvfrom(1024)
        print(f"📤 Response '{response.decode('utf-8', errors='ignore')}' from {target_addr} — Sending back to {addr}")
        sock.sendto(response, addr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple UDP Proxy")
    parser.add_argument("--listen-ip", default="127.0.0.1", help="IP to listen on (default: 127.0.0.1)")
    parser.add_argument("--listen-port", type=int, required=True, help="Port to listen on")
    parser.add_argument("--target-ip", required=True, help="Target IP to forward packets to")
    parser.add_argument("--target-port", type=int, required=True, help="Target port to forward packets to")

    args = parser.parse_args()

    udp_proxy(args.listen_ip, args.listen_port, args.target_ip, args.target_port)
