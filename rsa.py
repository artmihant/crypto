import base64
from random import randint
import math
import sys

from prime_gen import generate_prime_number


# Размер единичного блока шифрования в байтах. Чем этот параметр больше, тем длиннее ключи и тем надежней шифр
# Увеличение этого параметра на 1 прибавляет примерно 2.4 десятичные цифры (или 8 бит) к длине ключа

## Прогрессия сложности взлома

# При BLOCK_SIZE = 4 возможен взлом ключа на листочке ручкой

# При BLOCK_SIZE = 8 возможен взлом ключа простыми алгоритмами за минуты

# При BLOCK_SIZE = 16 возможен взлом ключа простыми алгоритмами за дни или сложными алгоритмами за минуты

# При BLOCK_SIZE = 32 возможен взлом ключа очень сложными алгоритмами за часы вычислений

# При BLOCK_SIZE = 64 возможен взлом ключа очень сложными алгоритмами за годы вычислений

# При BLOCK_SIZE = 96 получится число примерно 240 знаков 
#   что соответствует RSA-240 - наибольшему на текущий момент взломанному числу

# При BLOCK_SIZE = 128 алгоритм можно считать аналогичным RSA-1024, 
#   т.е. невзламываемым в смысле вычислительных возможностей образца 2023 года.


BLOCK_SIZE = 96


def gcd(a, b):
    """ Наибольший общий делитель чисел a и b """
    if a == 0:
        return b
    return gcd(b % a, a)


def euclid_extended(a, b):
    """ Для a,b находит x,y такие, что x*a + y*b = gcd(a, b) """
    if a == 0:
        return 0, 1
    y, z = euclid_extended(b % a, a)
    x = z - (b // a) * y

    return x, y


def generate_coprime_number(a):
    """ Генерирует случайное число, взаимопростое с a """
    b = randint(a//2, a)

    if gcd(a, b) != 1:
        return generate_coprime_number(a)

    return b


def generate_cripto_key():
    """ Генерирует открытую экспоненту, секретную экспоненту и модуль """
    A = generate_prime_number(BLOCK_SIZE//2)
    B = generate_prime_number(BLOCK_SIZE//2)

    if A == B:
        return generate_cripto_key()

    module = A*B 

    euler = (A-1)*(B-1)

    public_exp = generate_coprime_number(euler)
    secret_exp,_ = euclid_extended(public_exp, euler)

    if secret_exp < 0:
        secret_exp += euler

    return public_exp, secret_exp, module


def hack(public_exp, module):
    """ Пытается разложить module на множители и подобрать секретную экспоненту """

    for A in range(3, int(math.sqrt(module)), 2):
        if A%(10**7+1) == 0:
            print(f'Hack progress: {100*A/math.sqrt(module):.2f}%') 
        if module%A == 0:
            B = module//A
            break
    else:
        return None

    print(f'{module} = {A} * {B}')

    euler = (A-1)*(B-1)

    secret_exp,_ = euclid_extended(public_exp, euler)

    if secret_exp < 0:
        secret_exp += euler

    return public_exp, secret_exp, module


def crypt(blocks, exp, module):
    """ За- или рас- шифровывает цепочку блоков по переданному ключу """
    return [
        pow(block, exp, module)
        for block in blocks
    ]


def encode_from_bytes(bmessage):
    """ Разбивает байт-строку на фрагменты длиной BLOCK_LENGTH байт и переводит их в числа """

    if rem := len(bmessage) % BLOCK_SIZE: # Дополняем сообщение до целого числа блоков пробелами
        bmessage += b' '*(BLOCK_SIZE - rem)

    return [
        int.from_bytes(bytes=bmessage[i:i+BLOCK_SIZE], byteorder='big')
        for i in range(0, len(bmessage), BLOCK_SIZE)
    ]


def decode_to_bytes(blocks):
    """ Склеивает из цепочки блоков байт-строку """

    return b''.join([
        block.to_bytes(length=BLOCK_SIZE, byteorder='big')
        for block in blocks
    ])


def decode_from_base64(encrypt_message):
    """ Переводит сообщение из base64 в цепочку блоков """

    base64_block_size = 4*math.ceil((BLOCK_SIZE+1)/3)

    return [  
        int.from_bytes(bytes=base64.b64decode(encrypt_message[i:i+base64_block_size]), byteorder='big')
        for i in range(0, len(encrypt_message), base64_block_size)
    ]


def encode_to_base64(blocks):
    """ Конвертирует цепочку блоков в base64 """

    block_size = BLOCK_SIZE+1 # нужно взять с небольшим запасом

    return b''.join([
        base64.b64encode(block.to_bytes(length=block_size, byteorder='big'))
        for block in blocks
    ])


def encrypt(message, public_exp, module):
    """ Зашифрование сообщения с помощью открытого ключа """

    bmessage = message.strip().encode('utf-8') # Переводим сообщение из юникодной строки в байт-строку

    blocks = encode_from_bytes(bmessage) # Кодируем байт-строку в цепочку блоков

    encrypt_blocks = crypt(blocks, public_exp, module) # Зашифровываем цепочку блоков публичным ключом

    encrypt_message = encode_to_base64(encrypt_blocks) # Конвертируем цепочку блоков в байт-строку base64

    return encrypt_message.decode() # Превращаем байт-строку base64 в обычную строку base64 и возвращаем


def decrypt(encrypt_message, secret_exp, module):
    """ Расшифрование сообщения с помощью секретного ключа """

    try:

        encrypt_message = encrypt_message.strip().encode('utf-8') # Указываем зашифрованной строке base64 что она байт-строка
    
        encrypt_blocks = decode_from_base64(encrypt_message) # Переводим сообщение из base64 в цепочку блоков

        blocks = crypt(encrypt_blocks, secret_exp, module) # Расшифровываем цепочку блоков секретным ключом

        bmessage = decode_to_bytes(blocks) # Декодируем сообщение из цепочки в байт-строку

        return bmessage.decode() # Превращаем байт-строку в обычную строку и возвращаем

    except:

        sys.exit('Не могу расшифровать: сообщение повреждено или неправильный ключ!')



def main():
    """ Логика работы с программой """

    commands = 'encrypt', 'decrypt', 'hack', 'genkey'

    help_message = """Доступные команды:
    genkey \t сгенерирует тройку: <open_exp> <secret_exp> <module>
    encrypt <public_exp> <module> <message> \t Зашифровать сообщенние
    decrypt <secret_exp> <module> <message> \t Расшифровать сообщенние
    hack <open_exp> <module> \t Попытаться разложить module на простые и хакнуть ключ
    """
    
    if len(sys.argv) == 1:
        sys.exit(help_message)

    command = sys.argv[1]

    if command in commands:
        if command == 'genkey':
            (public_exp, secret_exp, module) = generate_cripto_key()
            print(f'Публичный ключ: {public_exp} {module}')
            print(f'Секретный ключ: {secret_exp} {module}')
            sys.exit()

        if command in ['encrypt', 'decrypt']:
            if len(sys.argv) < 4:
                sys.exit('Не указан ключ')
            if len(sys.argv) == 4:
                sys.exit('Не указано сообщение')

            exp = int(sys.argv[2])
            module = int(sys.argv[3])     
            message = ' '.join(sys.argv[4:])

            if command == 'encrypt':
                sys.exit(encrypt(message, exp, module))
            
            if command == 'decrypt':
                sys.exit(decrypt(message, exp, module))

        if command == 'hack':
            if len(sys.argv) < 4:
                sys.exit('Не указан ключ')
            
            exp = int(sys.argv[2])
            module = int(sys.argv[3])   

            (public_exp, secret_exp, module) = hack(exp, module)
            print(f'Секретный ключ: {secret_exp} {module}')
            sys.exit()
    else:
        print(f'Неизвестная команда {command}')
        sys.exit(help_message)


if __name__ == '__main__':

    # message = 'Привет, как дела, что делаешь?'

    # public_exp, module = 37232839779152700803, 44502594942665793551
    # secret_exp, module = 17906173911654058667, 44502594942665793551

    main()