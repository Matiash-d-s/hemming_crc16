from typing import List
from math import log2, ceil
from random import randrange


def crc16(x):
    a = 0xFFFF
    b = 0xA001
    for byte in x:
        a ^= ord(byte)
        for i in range(8):
            last = a % 2
            a >>= 1
            if last == 1:
                a ^= b
    s = hex(a).upper()
    return s


def __hamming_common(src: List[List[int]], s_num: int, encode=True) -> int:
    s_range = range(s_num)
    errors = 0

    for i in src:
        sindrome = 0
        for s in s_range:
            sind = 0
            for p in range(2 ** s, len(i) + 1, 2 ** (s + 1)):
                for j in range(2 ** s):
                    if (p + j) > len(i):
                        break
                    sind ^= i[p + j - 1]

            if encode:
                i[2 ** s - 1] = sind
            else:
                sindrome += (2 ** s * sind)

        if (not encode) and sindrome:
            try:
                i[sindrome - 1] = int(not i[sindrome - 1])
            except IndexError:
                errors += 1

    return errors


def hamming_encode(msg: str, mode: int = 8) -> str:
    """
    Encoding the message with Hamming code.
    :param msg: Message string to encode
    :param mode: number of significant bits
    :return:
    """

    result = ""
    msg_b = msg.encode("utf8")
    s_num = ceil(log2(log2(mode + 1) + mode + 1))  # number of control bits
    bit_seq = []
    for byte in msg_b:  # get bytes to binary values; every bits store to sublist
        bit_seq += list(map(int, f"{byte:08b}"))

    res_len = ceil((len(msg_b) * 8) / mode)  # length of result (bytes)
    bit_seq += [0] * (res_len * mode - len(bit_seq))  # filling zeros

    to_hamming = []

    for i in range(res_len):  # insert control bits into specified positions
        code = bit_seq[i * mode:i * mode + mode]
        for j in range(s_num):
            code.insert(2 ** j - 1, 0)
        to_hamming.append(code)

    errors = __hamming_common(to_hamming, s_num, True)  # process

    for i in to_hamming:
        result += "".join(map(str, i))

    return result


def hamming_decode(msg: str, mode: int = 8):
    """
    Decoding the message with Hamming code.
    :param msg: Message string to decode
    :param mode: number of significant bits
    :return:
    """

    result = ""

    s_num = ceil(log2(log2(mode + 1) + mode + 1))  # number of control bits
    res_len = len(msg) // (mode + s_num)  # length of result (bytes)
    code_len = mode + s_num  # length of one code sequence

    to_hamming = []

    for i in range(res_len):  # convert binary-like string to int-list
        code = list(map(int, msg[i * code_len:i * code_len + code_len]))
        to_hamming.append(code)

    errors = __hamming_common(to_hamming, s_num, False)  # process

    for i in to_hamming:  # delete control bits
        for j in range(s_num):
            i.pop(2 ** j - 1 - j)
        result += "".join(map(str, i))

    msg_l = []

    for i in range(len(result) // 8):  # convert from binary-sring value to integer
        val = "".join(result[i * 8:i * 8 + 8])
        msg_l.append(int(val, 2))

    try:
        result = bytes(msg_l).decode("utf8")
    except UnicodeDecodeError:
        pass

    return result, errors


def noizer(msg: str, mode: int) -> str:
    """
    Generates an error in each element of a Hamming encoded message
    """
    seq = list(map(int, msg))
    s_num = ceil(log2(log2(mode + 1) + mode + 1))  # количество служебных битов
    code_len = mode + s_num  # длина кодового слова
    cnt = len(msg) // code_len
    result = ""

    for i in range(cnt):
        to_noize = seq[i * code_len:i * code_len + code_len]
        noize = randrange(code_len)
        to_noize[noize] = int(not to_noize[noize])
        result += "".join(map(str, to_noize))

    return result


def noizer2(msg: str, mode: int) -> str:
    """
    Generates up to 2 errors in each fourth element of a Hamming encoded message
    """
    seq = list(map(int, msg))
    s_num = ceil(log2(log2(mode + 1) + mode + 1))  # количество служебных битов
    code_len = mode + s_num  # длина кодового слова
    cnt = len(msg) // code_len
    result = ""

    for i in range(0, cnt, 4):
        to_noize = seq[i * code_len:i * code_len + code_len]
        noize1 = randrange(code_len)
        noize2 = randrange(code_len)
        to_noize[noize1] = int(not to_noize[noize1])
        to_noize[noize2] = int(not to_noize[noize2])
        result += "".join(map(str, to_noize))

    return result


if __name__ == '__main__':
    MODE = 74  # Всего 81. Исключаем 1,2,4,8,16,32,64. Остается 74
    msg = 'Из файла берётся первое слово — это может быть битовый (CRC-1), байтовый (CRC-8) или любой другой элемент. ' \
          'Если старший бит в слове «1», то слово сдвигается влево на один разряд с последующим выполнением операции ' \
          'XOR с порождающим полиномом. Соответственно, если старший бит в слове «0», то после сдвига операция XOR не ' \
          'выполняется. После сдвига теряется старший бит, а на место младшего бита загружается очередной бит из ' \
          'файла, и операция повторяется до тех пор, пока не загрузится последний бит файла. После прохождения всего ' \
          'файла в слове остаётся остаток, который и является контрольной суммой. В то время как циклические ' \
          'избыточные коды являются частью стандартов, у этого термина не существует общепринятого определения — ' \
          'трактовки различных авторов нередко противоречат друг другу. Этот парадокс касается и выбора ' \
          'многочлена-генератора: зачастую стандартизованные полиномы не являются самыми эффективными в плане ' \
          'статистических свойств соответствующего им check redundancy code. При этом многие широко используемые ' \
          'полиномы не являются наиболее эффективными из всех возможных. В 1993—2004 годах группа учёных занималась ' \
          'исследованием порождающих многочленов разрядности до 16 24 и 32 бит и нашла полиномы, дающие лучшую, ' \
          'нежели стандартизированные многочлены, производительность в смысле кодового расстояния. Один из ' \
          'результатов этого исследования уже нашёл своё применение в протоколе iSCSI. Самый популярный и ' \
          'рекомендуемый IEEE полином для CRC-32 используется в Ethernet, FDDI; также этот многочлен является ' \
          'генератором кода Хемминга. Использование другого полинома — CRC-32C — позволяет достичь такой же ' \
          'производительности при длине исходного сообщения от 58 бит до 131 кбит, а в некоторых диапазонах длины ' \
          'входного сообщения может быть даже выше, поэтому в наши дни он тоже пользуется популярностью. К примеру, ' \
          'стандарт ITU-T G.hn использует CRC-32C с целью обнаружения ошибок в полезной нагрузке. Ниже в таблице ' \
          'перечислены наиболее распространённые многочлены — генераторы CRC. На практике вычисление CRC может ' \
          'включать пре- и постинверсию, а также обратный порядок обработки битов. В проприетарных реализациях CRC ' \
          'для усложнения анализа кода применяют ненулевые начальные значения регистров.'
    print(f'Начальное сообщение:\n{msg}')
    checksum = crc16(msg)
    print(f'Контрольная сумма: {checksum}')
    print()
    print('Отправка без ошибок')
    enc_msg = hamming_encode(msg, MODE)
    print(f'Кодированное сообщение:\n{enc_msg}')
    dec_msg, err = hamming_decode(enc_msg, MODE)
    print(f'Декодированное сообщение:\n{dec_msg}')
    print(f'Контрольная сумма: {crc16(dec_msg)} ')
    print(f'Значения сумм совпадают:{crc16(dec_msg) == checksum}')
    print(f'Совпадение текстов: {msg == dec_msg}')
    print()
    print('Отправка не более 1 ошибки на слово')
    noize_msg = noizer(enc_msg, MODE)
    print(f'Кодированное сообщение с ошибками:\n{noize_msg}')
    dec_msg, err = hamming_decode(noize_msg, MODE)
    print(f'Декодированное сообщение:\n{dec_msg}')
    print(f'Контрольная сумма: {crc16(dec_msg)} ')
    print(f'Значения сумм совпадают:{crc16(dec_msg) == checksum}')
    print(f'Совпадение текстов: {msg == dec_msg}')
    print()
    print('Отправка до двух ошибок на каждое 4-ое слово')
    noize_msg = noizer2(enc_msg, MODE)
    print(f'Кодированное сообщение с ошибками:\n{noize_msg}')
    dec_msg, err = hamming_decode(noize_msg, MODE)
    print(f'Декодированное сообщение:\n{dec_msg}')
    print(f'Контрольная сумма: {crc16(dec_msg)} ')
    print(f'Значения сумм совпадают:{crc16(dec_msg) == checksum}')
    print(f'Количество обнаруженных ошибок: {err}')
