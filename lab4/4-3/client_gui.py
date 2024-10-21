import socket
import easygui as eg


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    eg.msgbox("Подключено к серверу.", title="Клиент")

    while True:
        message = eg.enterbox("Клиент: ", title="Клиент")
        client_socket.send(message.encode('utf-8'))
        if message.lower() == 'exit':
            eg.msgbox("Отключение от сервера.", title="Клиент")
            break

        response = client_socket.recv(1024).decode('utf-8')
        eg.msgbox(f"Сервер: {response}", title="Клиент")
        if response.lower() == 'exit':
            eg.msgbox("Сервер завершил работу.", title="Клиент")
            break

    client_socket.close()


if __name__ == "__main__":
    start_client()