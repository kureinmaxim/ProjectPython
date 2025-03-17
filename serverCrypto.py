import socket
import argparse
from cryptography.fernet import Fernet


def run_server(host, port, encryption_key=None):
    """Запускает UDP сервер на VDS с поддержкой шифрования"""
    # Инициализация Fernet с ключом шифрования
    cipher = None
    if encryption_key:
        cipher = Fernet(encryption_key)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))

    print(f"✅ VDS UDP Server запущен на {host}:{port}")
    if cipher:
        print(f"🔒 Шифрование включено")

    while True:
        try:
            encrypted_data, addr = server_socket.recvfrom(4096)
            print(f"📥 Получено от прокси {addr}")

            # Расшифровываем данные
            if cipher:
                try:
                    data = cipher.decrypt(encrypted_data)
                    print(f"🔓 Данные расшифрованы")
                except Exception as e:
                    print(f"⚠️ Ошибка расшифровки: {e}")
                    continue
            else:
                data = encrypted_data

            # Декодируем и обрабатываем данные
            decoded_data = data.decode("utf-8", errors="replace")
            print(f"📝 Декодированные данные: {decoded_data}")

            # Формируем ответ
            response = f"Ответ от VDS сервера: {decoded_data}".encode("utf-8")

            # Шифруем ответ перед отправкой обратно на прокси
            if cipher:
                try:
                    encrypted_response = cipher.encrypt(response)
                    print(f"🔒 Ответ зашифрован")
                except Exception as e:
                    print(f"⚠️ Ошибка шифрования ответа: {e}")
                    continue
            else:
                encrypted_response = response

            # Отправляем зашифрованный ответ обратно на прокси
            server_socket.sendto(encrypted_response, addr)
            print(f"📤 Отправлен ответ на прокси {addr}")

        except Exception as e:
            print(f"❌ Ошибка обработки данных: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VDS UDP Server с шифрованием")
    parser.add_argument("--host", default="0.0.0.0", help="IP адрес для прослушивания (по умолчанию: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8888, help="Порт для прослушивания (по умолчанию: 8888)")
    parser.add_argument("--key", help="Ключ шифрования (если не указан, шифрование отключено)")

    args = parser.parse_args()

    encryption_key = None
    if args.key:
        encryption_key = args.key.encode()

    run_server(args.host, args.port, encryption_key)