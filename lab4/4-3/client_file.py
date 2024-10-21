import socket
import easygui as eg


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    eg.msgbox("Подключено к серверу.", title="Клиент")

    while True:
        filename = eg.enterbox("Введите название файла: ", title="Клиент")
        client_socket.send(filename.encode('utf-8'))
        if filename.lower() == 'exit':
            eg.msgbox("Отключение от сервера.", title="Клиент")
            break

        response = client_socket.recv(1024).decode('utf-8')
        eg.msgbox(response, title="Клиент")

    client_socket.close()


if __name__ == "__main__":
    start_client()