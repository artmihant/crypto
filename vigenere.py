import sys

ALPHABER =  'ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
            'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ' \
            '0123456789'


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


def encrypt(message, keyword):
    """ Зашифровать сообщение """
    code = encode(message)
    keycode = encode(keyword)
    encrypt_code = [
        (value + keycode[index%len(keycode)]) % len(ALPHABER) if type(value) == int else value
        for index, value in enumerate(code)
    ]

    encrypt_message = decode(encrypt_code)

    return encrypt_message


def decrypt(message, keyword):
    """ Расшифровать сообщение """
    code = encode(message)
    keycode = encode(keyword)

    encrypt_code = [
        (value - keycode[index%len(keycode)]) % len(ALPHABER) if type(value) == int else value
        for index, value in enumerate(code)
    ]

    encrypt_message = decode(encrypt_code)

    return encrypt_message


def main():
    """ Логика работы с программой """

    commands = 'encrypt', 'decrypt'

    help_message = """Доступные команды:
    encrypt <keyword> <message> \t Зашифровать сообщенние
    decrypt <keyword> <message> \t Расшифровать сообщенние
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

            keyword = sys.argv[2]         
            message = ' '.join(sys.argv[3:])

            if command == 'encrypt':
                sys.exit(encrypt(message, keyword))
            if command == 'decrypt':
                sys.exit(decrypt(message, keyword))

    else:
        print(f'Неизвестная команда {command}')
        sys.exit(help_message)


if __name__ == '__main__':

    main()
