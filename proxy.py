import socket
import argparse

def udp_proxy(listen_ip, listen_port, target_ip, target_port):
    """Запускает UDP-прокси сервер"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((listen_ip, listen_port))
    sock.settimeout(5)  # Таймаут в 5 секунд, чтобы не зависать на recvfrom()

    print(f"🔥 Proxy server listening on {listen_ip}:{listen_port} → Forwarding to {target_ip}:{target_port}")

    try:
        while True:
            try:
                data, addr = sock.recvfrom(1024)
            except socket.timeout:
                continue  # Нет данных - ждем дальше

            # Игнорируем пустые пакеты
            if not data.strip():
                continue

            print(f"📥 Received '{data.decode('utf-8', errors='ignore')}' from {addr} → Forwarding to {target_ip}:{target_port}")

            # Отправка на целевой сервер
            try:
                sock.sendto(data, (target_ip, target_port))
                print(f"📤 Sent '{data.decode('utf-8', errors='ignore')}' to {target_ip}:{target_port}")
            except OSError as e:
                print(f"❌ Ошибка при отправке данных: {e}")
                # For macOS и Linux
                #if e.errno == 10051:
                # For Windows
                if e.winerror == 10051:
                    print("🚨 Проверь подключение к сети, маршруты и настройки файрвола!")
                continue

            # Получение ответа
            try:
                response, target_addr = sock.recvfrom(1024)
                print(f"📤 Response '{response.decode('utf-8', errors='ignore')}' from {target_addr} → Sending back to {addr}")
                sock.sendto(response, addr)
            except socket.timeout:
                print("⏳ Сервер не ответил в течение 5 секунд. Продолжаем...")

    except KeyboardInterrupt:
        print("\n🚪 Прокси-сервер завершён (Ctrl + C). Освобождаем порт...")

    finally:
        sock.close()
        print("✅ Порт освобождён. Выход.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple UDP Proxy")
    parser.add_argument("--listen-ip", default="127.0.0.1", help="IP для прослушивания (по умолчанию: 127.0.0.1)")
    parser.add_argument("--listen-port", type=int, default=9999, help="Порт для прослушивания (по умолчанию: 9999)")
    parser.add_argument("--target-ip", required=True, help="Целевой IP для пересылки пакетов")
    parser.add_argument("--target-port", type=int, required=True, help="Целевой порт")

    args = parser.parse_args()
    udp_proxy(args.listen_ip, args.listen_port, args.target_ip, args.target_port)
