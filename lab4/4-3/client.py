import socket


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    print("Подключено к серверу.")

    while True:
        message = input("Клиент: ")
        client_socket.send(message.encode('utf-8'))
        if message.lower() == 'exit':
            print("Отключение от сервера.")
            break

        response = client_socket.recv(1024).decode('utf-8')
        print(f"Сервер: {response}")
        if response.lower() == 'exit':
            print("Сервер завершил работу.")
            break

    client_socket.close()


if __name__ == "__main__":
    start_client()