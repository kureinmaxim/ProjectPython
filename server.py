import socket

HOST = "127.0.0.1"  # Локальный адрес
PORT = 8888  # Порт сервера

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print(f"UDP Server запущен на {HOST}:{PORT}")

while True:
    data, addr = server_socket.recvfrom(4096)  # Получаем данные
    print(f"Получено от {addr}: {data.decode()}")

    response = f"Ответ от сервера: {data.decode()}".encode()
    server_socket.sendto(response, addr)  # Отправляем ответ
