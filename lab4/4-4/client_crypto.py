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


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    eg.msgbox("Подключено к серверу.", title="Клиент")

    while True:
        message = eg.enterbox("Клиент: ", title="Клиент")
        if message.lower() == 'exit':
            client_socket.send(message.encode('utf-8'))
            eg.msgbox("Отключение от сервера.", title="Клиент")
            break

        # Шифрование сообщения
        cipher_type = eg.buttonbox("Выберите тип шифра:", title="Шифрование", choices=["Цезарь", "Пары", "Виженер"])
        if cipher_type == "Цезарь":
            key = int(eg.enterbox("Введите ключ для шифра Цезаря:", title="Шифрование"))
            message = caesar_cipher(message, key)
        elif cipher_type == "Пары":
            d_1 = [109, 122, 106, 115, 100, 99, 105, 120, 110, 98, 121, 118, 107]
            d_2 = [112, 103, 108, 104, 111, 102, 119, 117, 97, 101, 116, 113, 114]
            message = pair_cipher(message, d_1, d_2)
        elif cipher_type == "Виженер":
            key = eg.enterbox("Введите ключ для шифра Виженера:", title="Шифрование")
            message = vigenere_cipher(message, key)

        client_socket.send(message.encode('utf-8'))

        response = client_socket.recv(1024).decode('utf-8')
        eg.msgbox(f"Сервер: {response}", title="Клиент")
        if response.lower() == 'exit':
            eg.msgbox("Сервер завершил работу.", title="Клиент")
            break

    client_socket.close()


if __name__ == "__main__":
    start_client()