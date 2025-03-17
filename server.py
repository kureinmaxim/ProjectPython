import socket

HOST = "0.0.0.0"  # Принимаем соединения со всех интерфейсов
PORT = 8888

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print(f"✅ UDP Server запущен на {HOST}:{PORT}")

while True:
    try:
        data, addr = server_socket.recvfrom(4096)  # Получаем данные
        print(f"📥 Получено от {addr}: {data!r}")  # Выводим сырой формат

        # Безопасно декодируем строку
        decoded_data = data.decode("utf-8", errors="replace")
        print(f"📝 Декодированные данные: {decoded_data}")

        # Формируем ответ
        response = f"Ответ от сервера: {decoded_data}".encode("utf-8")
        server_socket.sendto(response, addr)  # Отправляем ответ

    except Exception as e:
        print(f"❌ Ошибка обработки данных: {e}")
