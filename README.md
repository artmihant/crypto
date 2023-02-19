# Простая реализация алгоритма RSA

Данная программа может зашифровывать и расшифровывать сообщения посредством алгоритма [RSA](https://ru.wikipedia.org/wiki/RSA)


## Как использовать

Запуск:

    python -m rsa <command> <*args> 

Доступные команды:

    genkey \t сгенерирует тройку: <open_exp> <secret_exp> <module>

    encrypt <public_exp> <module> <message>     Зашифровать сообщенние

    decrypt <secret_exp> <module> <message>     Расшифровать сообщенние

    hack <open_exp> <module>     Попытаться разложить module на простые и хакнуть ключ


Пара целых чисел <public_exp> <module> называется открытым ключом.

Пара целых чисел <secret_exp> <module> называется секретным ключом.

Располагая открытым ключом вы можете шифровать сообщение. Сообщением является всё, что вы напишите в команде encrypt после открытого ключа. В качестве зашифрованного сообщения вам будет напечатана строка base64.

Расшифровка сообщений происходит аналогичным образом, командой decrypt.

Пример использования:

    > python -m rsa genkey

    Публичный ключ: 37510011688909726777 49081620712677117581
    Секретный ключ: 31456842056942067709 49081620712677117581

    > python -m rsa encrypt 37510011688909726777 49081620712677117581 Слоны идут на север

    AC4p6LOevMdbAMHVCmMhf/cKAEcI4D/FvqCQAdNunHSoU6gGAYwTj8UebR73

    > python -m rsa decrypt 31456842056942067709 49081620712677117581 AC4p6LOevMdbAMHVCmMhf/cKAEcI4D/FvqCQAdNunHSoU6gGAYwTj8UebR73

    Слоны идут на север

    > python -m rsa hack 37510011688909726777 49081620712677117581

    Hack progress: 0.14%
    Hack progress: 0.43%
    Hack progress: 0.71%
    ... (спустя примерно семь минут) ...
    Hack progress: 97.20%
    Hack progress: 97.49%
    49081620712677117581 = 6837222967 * 7178590043
    Секретный ключ: 31456842056942067709 49081620712677117581

## Особенности

Данная реализация подготовлена специально в качестве демонстрации алгоритма RSA для семинара по математике для школьников и не является эффективной или криптостойкой. **Не используете её в ситуации, когда вам действительно важно сохранить данные в тайне**.

В данной реализации вы не можете установить размер блока больше ~12 байт из-за неэффективного алгоритма генерации простых чисел. Модифицируя алгоритм, к примеру, добавив тест на [критерий Поклингтона](https://habr.com/ru/post/594135/), вы можете существенно увеличить размер вашего простого числа и соответственно повысить надежность шифрования.

Взлом ключа так же может быть оптимизирован, если вы замените в его реалзиации алгоритм простого перебора делителей на что-то более эффективное, например, [Метод квадратичных форм Шенкса](https://ru.wikipedia.org/wiki/%D0%9C%D0%B5%D1%82%D0%BE%D0%B4_%D0%BA%D0%B2%D0%B0%D0%B4%D1%80%D0%B0%D1%82%D0%B8%D1%87%D0%BD%D1%8B%D1%85_%D1%84%D0%BE%D1%80%D0%BC_%D0%A8%D0%B5%D0%BD%D0%BA%D1%81%D0%B0)

В целом в программе наличествует *гигантский* потенциал алгоритмической оптимизации. Почти каждый её фрагмент может быть качественно улучшен ценой серьезного усложнения как программного кода так и уровня задействованной математики.

## Настройка битности шифрования

Размер блока в данной реализации определяется константой `BLOCK_SIZE` в коде программы. По умолчанию `BLOCK_SIZE = 8` что соответствует 32-битному RSA-шифрованию.

Меняя параметр BLOCK_SIZE вы можете управлять качеством шифрования и длиной ключа. Каждая единица в этом параметре увеличивает надежность шифрования (т.е. среднее время взлома ключа эффективными средствами) примерно в 4 раза, а величину каждого из двух чисел ключа - примерно в 256 раз (т.е. где-то на 2.4 десятичные цифры)

Следует отметить, что в текущей реализации генерация ключа при BLOCK_SIZE > 12 будет занимать продолжительное время. Вы можете существенно улучшить это время, реализовав в функции генерации простого более эффективный алгоритм.

## Применение

Программа предназначена для живой демонстрации алгоритма RSA, написана с минимумом технических оптимизаций и максимально аккуратно в плане читаемости кода.

Вы можете попробовать улучшить её в рамках тренировки собственных навыков алгоритмического программирования или предложить другому человеку модифицировать её фрагмент в качестве тренировки или испытания (к примеру, в качестве технического задания на собеседовании).

Так же вы можете использовать её в случае, если вы *хотите* допустить возможность взлома вашего публичного ключа. К примеру, она может использоваться как часть организуемого вами квеста.

# Простейшие шифры добавления по кольцу остатков: Шифр Цезаря и шифр Вернама

В качестве бонуса в комплекте данной библиотеки шифрования предоставляеются простейшие реализации [шифра Цезаря](https://ru.wikipedia.org/wiki/%D0%A8%D0%B8%D1%84%D1%80_%D0%A6%D0%B5%D0%B7%D0%B0%D1%80%D1%8F) и [шифра Вернама](https://ru.wikipedia.org/wiki/%D0%A8%D0%B8%D1%84%D1%80_%D0%92%D0%B5%D1%80%D0%BD%D0%B0%D0%BC%D0%B0).

## Как использовать шифр Цезаря

Запуск:

    python -m caesar <command> <*args> 

Доступные команды:

    encrypt <key> <message>      Зашифровать сообщенние

    decrypt <key> <message>      Расшифровать сообщенние

    hack <message>       Показать все варианты расшифровки сообщения

В качестве ключа используется целое число. 
Шифр принимает данные на русском языке, причем автоматически переведет их в верхний регистр. Символы, не являющиеся буквами русского алфавита (например, пробелы или числа) зашифрованы не будут

С помощью hack можно автоматически перебрать и вывести все варианты подстановки возможных ключей для последующего криптоанализа.

Пример использования:

    > python -m caesar encrypt 3 слоны идут на север

    ФОСРЮ ЛЗЦХ РГ ФИЕИУ

    > python -m caesar decrypt 3 ФОСРЮ ЛЗЦХ РГ ФИЕИУ

    СЛОНЫ ИДУТ НА СЕВЕР

    > python -m caesar hack ФОСРЮ ЛЗЦХ РГ ФИЕИУ

    0       ФОСРЮ ЛЗЦХ РГ ФИЕИУ
    1       УНРПЭ КЖХФ ПВ УЗДЗТ
    2       ТМПОЬ ЙЕФУ ОБ ТЖГЖС
    3       СЛОНЫ ИДУТ НА СЕВЕР
    4       РКНМЪ ЗГТС МЯ РДБДП
    ...
    30      ЦРУТА НЙШЧ ТЕ ЦКЗКХ
    31      ХПТСЯ МИЧЦ СД ХЙЖЙФ


## Как использовать шифр Вернама

Запуск:

    python -m vernam <command> <*args> 

Доступные команды:

    encrypt <keyword> <message>      Зашифровать сообщенние

    decrypt <keyword> <message>      Расшифровать сообщенние

В качестве ключа используется любое слово, написанное в том же алфавите, что и исходное сообщение.

Пример использования:

    > python -m vernam encrypt ПАРОЛЬ слоны идут на север

    Q5OLW HЮTQ Z9 RD7RP

    > python -m vernam decrypt ПАРОЛЬ Q5OLW HЮTQ Z9 RD7RP

    СЛОНЫ ИДУТ НА СЕВЕР

Опция *hack* для данного алгоритма отсутствует, так как при достаточной длине ключа шифр Вейрама становится невзламываемым. 

## Настройка алфавита

Глобальная переменная ALPHABER отвечает за список символов, которые будут зашифрованы. Для примера, в шифре Цезаря задействованы только прописные буквы русского алфавита, а в шифре Вернама - прописные буквы русского и латинского алфавитов и десятичные цифры. Все эти символы будут встречаться в шифровке.

Вы можете настраивать данную переменную в соответствии со своими потребностями.

## Применение

Данные алгоритмы не представляют какой-либо математической сложности по своей сути. Вы можете применять их в любых ситуациях, когда хотите зашифровать что-то простым способом, не требующим особых вычислений.