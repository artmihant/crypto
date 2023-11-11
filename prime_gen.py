import math

from random import randint

PRIMES_LESS_256 = [ 
    2,   3,   5,   7,   11,  13,  17,  19,  23,  29, 
    31,  37,  41,  43,  47,  53,  59,  61,  67,  71, 
    73,  79,  83,  89,  97,  101, 103, 107, 109, 113, 
    127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 
    179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 
    233, 239, 241, 251
] # все простые меньше 256

COUNTER = {
    0: 664579, 
    2: 9334671, 
    3: 563, 
    5: 92, 
    7: 32, 
    11: 11, 
    13: 12, 
    17: 4, 
    19: 6, 
    23: 2, 
    29: 2, 
    31: 7, 
    37: 4, 
    41: 5, 
    43: 4, 
    53: 2, 
    61: 2, 
    101: 1, 
    109: 1
}

def fermat_prime_test(number):

    if number < 2:
        return False

    for prime in PRIMES_LESS_256:

        if prime > number**0.5:
            return True

        if pow(prime, number-1, number) != 1:
            COUNTER[prime] += 1
            return False

    return True

def pocklington_prime_test(number, seed):
    """ 
        проверят число (number) на простоту
        seed - простое число, такое, что number-1 делится на seed, и seed**2 > number

        если True, кандидат простой
        если False, кандидат составной (почти всегда)
    """
    for prime in PRIMES_LESS_256:

        # Если, для некого prime, number удолетворяет:
        
        # 1. тесту ферма
        if pow(prime, number-1, number) != 1:
            # если не удолелетворяет - составное (или равно prime)
            return prime == number

        # 2. условию взаимопростоты со особой хитрой степенью
        gcd = math.gcd(
            number,
            pow(prime, (number-1)//seed, number) - 1
        )
        
        if gcd == 1:
            # то number гарантированно простое
            return True

        if gcd == number:
            # непонятно, продолжаем
            continue

        # у number есть делитель - gcd - не равный ему и 1. Составное.
        return False

    # непонятно, отбрасываем
    return False


def generate_prime_number(bytes:int):
    """ Генерирует случайное простое число больше 256**bytes """
    assert bytes > -1

    if bytes == 0:
        return PRIMES_LESS_256[randint(1, len(PRIMES_LESS_256))]

    if bytes < 4:
        while True:
            number = 2*randint(265**bytes//2, 2*265**bytes) + 1
            if fermat_prime_test(number):
                return number

    # если запрос на не очень маленькое число, 
    #   нужно сперва создать число поменьше (чуть больше корня из запроса)

    seed = generate_prime_number((bytes-1)//2+1) # s
    # print(seed, seed/256**(bytes-1))

    # может, нам сразу дадут подходящее число?
    if seed > 256**bytes:
        return seed

    while True:

        # генерируем кандидата размера чуть меньше (не более чем в два раза меньше) seed**2.
        #   генерируем его сразу нечетным и нужного размера
        number = 2*randint(seed//4, seed//2)*seed + 1

        if number < 256**bytes:
            continue

        # проверяем кандидата на простоту
        if pocklington_prime_test(number, seed):
            return number




if __name__ == '__main__':

    k = 16
    # for k in range(0,24):
    for i in range(1000):
        prime = generate_prime_number(k)
        print(k, prime, prime/256**k)
