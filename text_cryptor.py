from emoji import emoji_list
import random

ALPHABET = ["а","б","в","г","д","е","ё","ж","з","и","й","к","л","м","н","о",
            "п","р","с","т","у","ф","х","ц","ч","ш","щ","ъ","ы","ь","э","ю","я"]

def encrypt(message):

    message = message.lower()

    symbols = list(filter(lambda s: s in ALPHABET, set(list(message))))

    replace_map = {symbols[i]:e for i, e in enumerate(random.sample(emoji_list, len(symbols)))}

    encrypt_message = ''

    for s in message:
        if s in replace_map:
            encrypt_message += replace_map[s]
        else:
            encrypt_message += s

    return encrypt_message, replace_map

if __name__ == '__main__':

    text = """
Пётр Петрович, по прозванью Петров, поймал птицу пигалицу. 
Понёс по рынку, просил полтинку, выдали пятак, он и продал так.
    """

    encrypt_text, replace_map = encrypt(text)

    print(text)

    for s in replace_map:
        print(f'{s} -> {replace_map[s]}')

    print(encrypt_text)
