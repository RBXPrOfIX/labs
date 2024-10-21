import socket


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(1)
    print("Сервер запущен и ожидает подключения...")

    client_socket, addr = server_socket.accept()
    print(f"Подключен клиент: {addr}")

    while True:
        message = client_socket.recv(1024).decode('utf-8')
        if message.lower() == 'exit':
            print("Клиент отключился.")
            break
        print(f"Клиент: {message}")

        response = input("Сервер: ")
        client_socket.send(response.encode('utf-8'))
        if response.lower() == 'exit':
            print("Сервер завершает работу.")
            break

    client_socket.close()
    server_socket.close()


if __name__ == "__main__":
    start_server()