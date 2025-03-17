import socket
import argparse
from cryptography.fernet import Fernet


def udp_proxy(listen_ip, listen_port, target_ip, target_port, encryption_key=None):
    """Запускает UDP-прокси сервер с шифрованием для передачи между локальной машиной и VDS"""
    # Инициализация Fernet с ключом шифрования
    cipher = None
    if encryption_key:
        cipher = Fernet(encryption_key)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((listen_ip, listen_port))
    sock.settimeout(5)  # Таймаут в 5 секунд

    print(f"🔥 Proxy server listening on {listen_ip}:{listen_port} → Forwarding to {target_ip}:{target_port}")
    if cipher:
        print(f"🔒 Шифрование включено")

    # Словарь для хранения адресов клиентов
    clients = {}

    try:
        while True:
            try:
                data, addr = sock.recvfrom(1024)
            except socket.timeout:
                continue

            # Игнорируем пустые пакеты
            if not data.strip():
                continue

            # Сохраняем адрес клиента для ответа
            clients[addr] = True

            print(f"📥 Получено '{data.decode('utf-8', errors='ignore')}' от {addr}")

            # Шифруем данные перед отправкой на VDS
            if cipher:
                try:
                    encrypted_data = cipher.encrypt(data)
                    print(f"🔒 Данные зашифрованы: {encrypted_data[:20]}...")
                except Exception as e:
                    print(f"⚠️ Ошибка шифрования: {e}")
                    continue
            else:
                encrypted_data = data

            try:
                sock.sendto(encrypted_data, (target_ip, target_port))
                print(f"📤 Отправлено на VDS {target_ip}:{target_port}")
            except OSError as e:
                print(f"❌ Ошибка при отправке данных: {e}")
                continue

            # Ждем ответа от VDS
            try:
                encrypted_response, target_addr = sock.recvfrom(1024)

                # Проверяем, что ответ пришел от целевого сервера
                if target_addr[0] != target_ip or target_addr[1] != target_port:
                    print(f"⚠️ Получен ответ от неизвестного источника: {target_addr}")
                    continue

                # Расшифровываем ответ от VDS
                if cipher:
                    try:
                        response = cipher.decrypt(encrypted_response)
                        print(f"🔓 Ответ расшифрован")
                    except Exception as e:
                        print(f"⚠️ Ошибка расшифровки: {e}")
                        continue
                else:
                    response = encrypted_response

                # Отправляем ответ обратно клиенту
                print(f"📤 Отправляем ответ '{response.decode('utf-8', errors='ignore')}' клиенту {addr}")
                sock.sendto(response, addr)

            except socket.timeout:
                print("⏳ VDS не ответил в течение 5 секунд")

    except KeyboardInterrupt:
        print("\n🚪 Прокси-сервер завершён (Ctrl + C)")

    finally:
        sock.close()
        print("✅ Порт освобождён. Выход.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UDP Proxy с шифрованием для передачи на VDS")
    parser.add_argument("--listen-ip", default="0.0.0.0", help="IP для прослушивания (по умолчанию: 0.0.0.0)")
    parser.add_argument("--listen-port", type=int, default=9999, help="Порт для прослушивания (по умолчанию: 9999)")
    parser.add_argument("--target-ip", required=True, help="IP VDS сервера")
    parser.add_argument("--target-port", type=int, required=True, help="Порт VDS сервера")
    parser.add_argument("--key", help="Ключ шифрования (если не указан, шифрование отключено)")
    parser.add_argument("--generate-key", action="store_true", help="Сгенерировать новый ключ шифрования")

    args = parser.parse_args()

    encryption_key = None
    if args.generate_key:
        encryption_key = Fernet.generate_key()
        print(f"🔑 Сгенерирован новый ключ: {encryption_key.decode()}")
    elif args.key:
        encryption_key = args.key.encode()

    udp_proxy(args.listen_ip, args.listen_port, args.target_ip, args.target_port, encryption_key)