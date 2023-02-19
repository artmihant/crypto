import sys

ALPHABER = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'


def encode(message):
    """ Кодируем сообщение, т.е. превращаем его в список чисел """

    message = message.upper()
    
    # Таблица кодировки сопоставляет буквы с числами
    encode_table = {
        letter: value
        for value, letter in enumerate(ALPHABER)
    }

    code = [
        encode_table.get(letter, letter)
        for letter in message
    ]

    return code


def decode(code):
    """ Декодируем сообщение из списка чисел """

    # Таблица декодировки сопоставляет числа с буквами
    decode_table = {
        value: letter
        for value, letter in enumerate(ALPHABER)
    }

    message = ''.join([
        decode_table.get(value, value)
        for value in code
    ])

    return message


def encrypt(message, key):
    """ Зашифровать сообщение """
    code = encode(message)

    encrypt_code = [
        (value + key) % len(ALPHABER) if type(value) == int else value
        for value in code
    ]

    encrypt_message = decode(encrypt_code)

    return encrypt_message


def decrypt(message, key):
    """ Расшифровать сообщение """
    code = encode(message)

    encrypt_code = [
        (value - key) % len(ALPHABER) if type(value) == int else value
        for value in code
    ]

    encrypt_message = decode(encrypt_code)

    return encrypt_message


def analisys(message):
    """ Попробовать расшифровать сообщение всеми ключами """

    for key in range(len(ALPHABER)):
        print(decrypt(message))


def main():
    """ Логика работы с программой """

    commands = 'encrypt', 'decrypt', 'hack'

    help_message = """Доступные команды:
    encrypt <key> <message> \t Зашифровать сообщенние
    decrypt <key> <message> \t Расшифровать сообщенние
    hack <message> \t Показать все варианты расшифровки
    """

    if len(sys.argv) == 1:
        sys.exit(help_message)

    command = sys.argv[1]

    if command in commands:
        if command in ['encrypt', 'decrypt']:
            if len(sys.argv) == 2:
                sys.exit('Не указан ключ')
            if len(sys.argv) == 3:
                sys.exit('Не указано сообщение')

            key = int(sys.argv[2])         
            message = ' '.join(sys.argv[3:])

            if command == 'encrypt':
                sys.exit(encrypt(message, key))
            if command == 'decrypt':
                sys.exit(decrypt(message, key))

        if command == 'hack':
            if len(sys.argv) == 2:
                sys.exit('Не указано сообщение')
        
            message = ' '.join(sys.argv[2:])
            for key in range(len(ALPHABER)):
                print(key, '\t'+ decrypt(message, key))

    else:
        print(f'Неизвестная команда {command}')
        sys.exit(help_message)


if __name__ == '__main__':

    main()