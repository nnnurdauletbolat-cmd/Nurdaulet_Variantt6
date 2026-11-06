# 6-нұсқа. Хэмминг коды (7, 4)
# Ақпараттық комбинация: 0011
# 5-разряд беру кезінде бұрмаланады.
# Бақылау разрядтары: 1, 2, 4 (жұптық бақылау).

def encode_hamming(data):
    """4 биттік ақпаратты (7,4) Хэмминг кодына түрлендіреді."""
    if len(data) != 4 or any(bit not in "01" for bit in data):
        raise ValueError("Ақпараттық комбинация 4 биттен тұруы керек.")

    # 1, 2, 4 — бақылау позициялары.
    # 3, 5, 6, 7 — ақпараттық позициялар.
    code = [0] * 8  # 1-ден басталатын позициялар үшін 0-индекс қолданылмайды.
    data_positions = [3, 5, 6, 7]

    for position, bit in zip(data_positions, data):
        code[position] = int(bit)

    # Жұптық ережесі бойынша бақылау биттерін есептеу.
    code[1] = code[3] ^ code[5] ^ code[7]
    code[2] = code[3] ^ code[6] ^ code[7]
    code[4] = code[5] ^ code[6] ^ code[7]

    return "".join(str(code[i]) for i in range(1, 8))


def introduce_error(code, error_position):
    """Көрсетілген позициядағы битті инверсиялайды."""
    bits = list(code)
    index = error_position - 1
    bits[index] = "1" if bits[index] == "0" else "0"
    return "".join(bits)


def decode_and_correct(received):
    """Синдром арқылы қатені тауып, бір биттік қатені түзетеді."""
    bits = [0] + [int(bit) for bit in received]

    # Әр бақылау тобы бойынша тексеру нәтижелері.
    e1 = bits[1] ^ bits[3] ^ bits[5] ^ bits[7]
    e2 = bits[2] ^ bits[3] ^ bits[6] ^ bits[7]
    e4 = bits[4] ^ bits[5] ^ bits[6] ^ bits[7]

    # Синдром: E4 E2 E1.
    syndrome_bits = f"{e4}{e2}{e1}"
    error_position = int(syndrome_bits, 2)

    corrected = list(received)
    if 1 <= error_position <= 7:
        index = error_position - 1
        corrected[index] = "1" if corrected[index] == "0" else "0"

    return e1, e2, e4, syndrome_bits, error_position, "".join(corrected)


def main():
    data = "0011"
    error_position = 5

    print("6-нұсқа — Хэмминг коды")
    print("-" * 35)
    print(f"Бастапқы ақпараттық комбинация: {data}")

    correct_code = encode_hamming(data)
    print(f"Дұрыс кодтық комбинация C:      {correct_code}")

    received = introduce_error(correct_code, error_position)
    print(f"Бұрмаланған разряд:             {error_position}")
    print(f"Қабылданған комбинация C*:      {received}")

    e1, e2, e4, syndrome, error, corrected = decode_and_correct(received)
    print("\nҚателерді тексеру нәтижелері:")
    print(f"E1 = {e1}")
    print(f"E2 = {e2}")
    print(f"E4 = {e4}")
    print(f"Синдром S = E4E2E1 = {syndrome}")
    print(f"Синдромның ондық мәні: {error}")

    if error == 0:
        print("Қате анықталған жоқ.")
    elif 1 <= error <= 7:
        print(f"Қате {error}-разрядта анықталды.")
        print(f"Түзетілген комбинация:         {corrected}")
    else:
        print("Синдром 7-ден үлкен: бір разрядтық қатені түзету мүмкін емес.")


if __name__ == "__main__":
    main()
