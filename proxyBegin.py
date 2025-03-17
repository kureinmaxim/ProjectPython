import socket

# Настройки прокси
PROXY_HOST = "0.0.0.0"  # Слушаем все интерфейсы
PROXY_PORT = 9999  # Порт прокси
SERVER_HOST = "127.0.0.1"  # Куда перенаправлять трафик
SERVER_PORT = 8888  # Порт целевого сервера

# Создаём UDP-сокет
proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
proxy_socket.bind((PROXY_HOST, PROXY_PORT))

print(f"UDP Proxy запущен на {PROXY_HOST}:{PROXY_PORT}, перенаправляет на {SERVER_HOST}:{SERVER_PORT}")

while True:
    data, client_addr = proxy_socket.recvfrom(4096)  # Получаем данные от клиента
    print(f"[{client_addr}] -> {data.decode()}")

    # Отправляем данные на целевой сервер
    proxy_socket.sendto(data, (SERVER_HOST, SERVER_PORT))

    # Получаем ответ от сервера и отправляем обратно клиенту
    response, server_addr = proxy_socket.recvfrom(4096)
    print(f"[{server_addr}] <- {response.decode()}")
    proxy_socket.sendto(response, client_addr)
