import socket
import easygui as eg


def count_words(text):
    return len(text.split())


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(1)
    eg.msgbox("Сервер запущен и ожидает подключения...", title="Сервер")

    client_socket, addr = server_socket.accept()
    eg.msgbox(f"Подключен клиент: {addr}", title="Сервер")

    while True:
        filename = client_socket.recv(1024).decode('utf-8')
        if filename.lower() == 'exit':
            eg.msgbox("Клиент отключился.", title="Сервер")
            break

        with open(filename, 'r') as file:
            content = file.read()
            word_count = count_words(content)
            response = f"Количество слов в файле: {word_count}"
            client_socket.send(response.encode('utf-8'))

    client_socket.close()
    server_socket.close()


if __name__ == "__main__":
    start_server()