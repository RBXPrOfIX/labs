import socket
import easygui as eg


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    eg.msgbox("Подключено к серверу.", title="Клиент")

    while True:
        filename = eg.enterbox("Введите название файла: ", title="Клиент")
        if filename.lower() == 'exit':
            client_socket.send(filename.encode('utf-8'))
            eg.msgbox("Отключение от сервера.", title="Клиент")
            break

        cipher_type = eg.buttonbox("Выберите тип шифра:", title="Шифрование", choices=["Цезарь", "Пары", "Виженер"])
        key = eg.enterbox("Введите ключ для шифра:", title="Шифрование")

        client_socket.send(filename.encode('utf-8'))
        client_socket.send(cipher_type.encode('utf-8'))
        client_socket.send(key.encode('utf-8'))

        decrypted_content = client_socket.recv(1024).decode('utf-8')
        eg.msgbox(f"Дешифрованное содержимое файла:\n{decrypted_content}", title="Клиент")

    client_socket.close()


if __name__ == "__main__":
    start_client()