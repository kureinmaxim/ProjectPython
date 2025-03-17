import socket

SERVER_IP = "127.0.0.1"  # IP прокси-сервера
SERVER_PORT = 9999  # Порт прокси-сервера

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(5)  # Ждать ответ максимум 5 секунд

try:
    while True:
        try:
            message = input("Введите сообщение: ").strip()
            if message.lower() == "exit":
                print("Выход...")
                break  # Выход из цикла
            if not message:
                continue  # Пропускаем пустой ввод

            # Отправка сообщения с обработкой ошибок
            try:
                sock.sendto(message.encode("utf-8"), (SERVER_IP, SERVER_PORT))
            except OSError as e:
                print(f"❌ Ошибка при отправке: {e}")
                continue

            # Ожидание ответа
            try:
                data, _ = sock.recvfrom(1024)
                print("Ответ от сервера:", data.decode("utf-8", errors="ignore"))
            except socket.timeout:
                print("⏳ Сервер не ответил в течение 5 секунд. Продолжаем...")
            except ConnectionResetError:
                print("🚨 Сервер разорвал соединение (WinError 10054).")

        except KeyboardInterrupt:
            print("\n🚪 Завершение клиента (Ctrl + C)")
            break

except Exception as e:
    print(f"❌ Ошибка: {e}")

finally:
    sock.close()  # Закрываем сокет при выходе
    print("✅ Клиент завершил работу.")