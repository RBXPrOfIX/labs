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


def decrypt_file(filename, cipher_type, key):
    with open(filename, 'r') as file:
        content = file.read()
        if cipher_type == "Цезарь":
            decrypted_content = caesar_cipher(content, key, decrypt=True)
        elif cipher_type == "Пары":
            d_1 = [109, 122, 106, 115, 100, 99, 105, 120, 110, 98, 121, 118, 107]
            d_2 = [112, 103, 108, 104, 111, 102, 119, 117, 97, 101, 116, 113, 114]
            decrypted_content = pair_cipher(content, d_1, d_2, decrypt=True)
        elif cipher_type == "Виженер":
            decrypted_content = vigenere_cipher(content, key, decrypt=True)
        else:
            decrypted_content = content
    return decrypted_content


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

        cipher_type = client_socket.recv(1024).decode('utf-8')
        key = client_socket.recv(1024).decode('utf-8')

        decrypted_content = decrypt_file(filename, cipher_type, key)
        client_socket.send(decrypted_content.encode('utf-8'))

    client_socket.close()
    server_socket.close()


if __name__ == "__main__":
    start_server()