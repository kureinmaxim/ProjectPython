import socket

SERVER_IP = "127.0.0.1"  # IP прокси-сервера
SERVER_PORT = 9999  # Порт прокси-сервера

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    try:
        message = input("Введите сообщение: ").strip()
        if not message:
            continue  # Пропускаем пустой ввод

        sock.sendto(message.encode("utf-8"), (SERVER_IP, SERVER_PORT))

        data, _ = sock.recvfrom(1024)
        print("Ответ от сервера:", data.decode("utf-8", errors="ignore"))

    except UnicodeDecodeError as e:
        print(f"Ошибка кодировки: {e}")
    except KeyboardInterrupt:
        print("\nВыход из клиента.")
        break
