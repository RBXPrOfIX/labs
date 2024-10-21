import socket
import easygui as eg


def caesar_cipher(text, key, decrypt=False):
    if decrypt:
        key = -key
    result = ''
    for char in text:
        if char.isalpha():
            shift = 65 if char.isupper() else 97
            result += chr((ord(char) - shift + key) % 26 + shift)
        else:
            result += char
    return result


def pair_cipher(text, d_1, d_2, decrypt=False):
    if decrypt:
        d_1, d_2 = d_2, d_1
    result = ''
    for char in text:
        if char.isalpha():
            shift = 65 if char.isupper() else 97
            index = ord(char) - shift
            if index in d_1:
                result += chr(d_2[d_1.index(index)] + shift)
            elif index in d_2:
                result += chr(d_1[d_2.index(index)] + shift)
            else:
                result += char
        else:
            result += char
    return result


def vigenere_cipher(text, key, decrypt=False):
    key = key.upper()
    result = ''
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = 65 if char.isupper() else 97
            key_char = key[key_index % len(key)]
            key_shift = ord(key_char) - 65
            if decrypt:
                key_shift = -key_shift
            result += chr((ord(char) - shift + key_shift) % 26 + shift)
            key_index += 1
        else:
            result += char
    return result


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(1)
    eg.msgbox("Сервер запущен и ожидает подключения...", title="Сервер")

    client_socket, addr = server_socket.accept()
    eg.msgbox(f"Подключен клиент: {addr}", title="Сервер")

    while True:
        message = client_socket.recv(1024).decode('utf-8')
        if message.lower() == 'exit':
            eg.msgbox("Клиент отключился.", title="Сервер")
            break
        eg.msgbox(f"Клиент: {message}", title="Сервер")

        response = eg.enterbox("Сервер: ", title="Сервер")
        client_socket.send(response.encode('utf-8'))
        if response.lower() == 'exit':
            eg.msgbox("Сервер завершает работу.", title="Сервер")
            break

    client_socket.close()
    server_socket.close()


if __name__ == "__main__":
    start_server()