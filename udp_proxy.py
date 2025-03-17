import socket

# Настройки прокси
PROXY_IP = "0.0.0.0"  # Слушаем все интерфейсы
PROXY_PORT = 9999     # Порт прокси

# Настройки ZYNQ (сейчас не используется)
ZYNQ_IP = "192.168.1.100"
ZYNQ_PORT = 8888

sock = None  # Создаём переменную заранее

try:
    print("Создание UDP-сокета...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((PROXY_IP, PROXY_PORT))
    print("UDP-прокси запущен! Ожидаем данные...\n")

    # Запуск основного цикла
    while True:
        try:
            data, addr = sock.recvfrom(4096)  # Получаем UDP-данные от клиента
            if not data:
                continue  # Если данных нет, пропускаем

            # Попытка декодирования сообщения (если текст)
            try:
                log_message = data.decode("utf-8", errors="replace")
                print("Получено от {}: {}".format(addr, log_message))
            except UnicodeDecodeError:
                log_message = data  # Если не текст, оставляем как байты
                print("Получены бинарные данные от {}: {}".format(addr, log_message))

            # Фиктивный ответ (эхо)
            response = b"ECHO: " + data
            sock.sendto(data, addr) # w/o ECHO
            # sock.sendto(response, addr)
            print("Ответ клиенту отправлен (байты): {}\n".format(response))

        except KeyboardInterrupt:
            print("\nОстановка прокси-сервера (Ctrl+C)")
            break  # Выход из цикла

        except Exception as e:
            print("Ошибка приема данных:", e)

finally:
    if sock:  # Закрываем сокет только если он был создан
        sock.close()
        print("Сокет закрыт.")
    input("Нажмите Enter для выхода...")
