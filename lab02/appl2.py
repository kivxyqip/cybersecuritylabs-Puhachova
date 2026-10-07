from math import gcd


# Алфавіти, які підтримує програма
ENGLISH_ALPHABET = "abcdefghijklmnopqrstuvwxyz"
UKRAINIAN_ALPHABET = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"


# Визначаємо алфавіт за текстом
def get_alphabet(text):
    if any(char.lower() in UKRAINIAN_ALPHABET for char in text):
        return UKRAINIAN_ALPHABET

    return ENGLISH_ALPHABET


# Генеруємо ключ для шифру Цезаря
def generate_caesar_key(birth_date, alphabet_length):
    digits = [int(char) for char in birth_date if char.isdigit()]
    return sum(digits) % alphabet_length


# Генеруємо параметри афінного шифру
def generate_affine_key(surname, birth_date, alphabet):
    digits = [int(char) for char in birth_date if char.isdigit()]

    a = sum(digits) % len(alphabet)

    # Для афінного шифру a має бути взаємно простим з довжиною алфавіту
    if a == 0:
        a = 1

    while gcd(a, len(alphabet)) != 1:
        a += 1

        if a == len(alphabet):
            a = 1

    # Створюємо параметр b на основі прізвища
    b = 0

    for char in surname.lower():
        if char in alphabet:
            b += alphabet.index(char)

    b %= len(alphabet)

    return a, b


# Перевіряємо, чи є символ літерою вибраного алфавіту
def is_letter(char, alphabet):
    return char.lower() in alphabet


# Шифрування шифром Цезаря
def caesar_encrypt(text, shift, alphabet):
    result = ""

    for char in text:
        if is_letter(char, alphabet):
            index = alphabet.index(char.lower())
            new_index = (index + shift) % len(alphabet)

            new_char = alphabet[new_index]

            if char.isupper():
                new_char = new_char.upper()

            result += new_char
        else:
            result += char

    return result


# Розшифрування шифру Цезаря
def caesar_decrypt(text, shift, alphabet):
    return caesar_encrypt(text, -shift, alphabet)


# Шифрування афінним шифром
def affine_encrypt(text, a, b, alphabet):
    result = ""

    for char in text:
        if is_letter(char, alphabet):
            index = alphabet.index(char.lower())
            new_index = (a * index + b) % len(alphabet)

            new_char = alphabet[new_index]

            if char.isupper():
                new_char = new_char.upper()

            result += new_char
        else:
            result += char

    return result


# Знаходимо обернений елемент для розшифрування
def modular_inverse(a, modulus):
    for x in range(1, modulus):
        if (a * x) % modulus == 1:
            return x

    return None


# Розшифрування афінного шифру
def affine_decrypt(text, a, b, alphabet):
    a_inverse = modular_inverse(a, len(alphabet))
    result = ""

    for char in text:
        if is_letter(char, alphabet):
            index = alphabet.index(char.lower())

            new_index = (
                a_inverse * (index - b)
            ) % len(alphabet)

            new_char = alphabet[new_index]

            if char.isupper():
                new_char = new_char.upper()

            result += new_char
        else:
            result += char

    return result


# Brute force для шифру Цезаря
def caesar_brute_force(text, alphabet):
    print("\n--- Brute force для Цезаря ---")

    for shift in range(1, len(alphabet)):
        result = caesar_decrypt(
            text,
            shift,
            alphabet
        )

        print(f"Зсув {shift:2}: {result}")


# Порівняльний аналіз двох шифрів
def show_comparison(
    text,
    caesar_result,
    affine_result,
    caesar_key,
    affine_a,
    affine_b,
    alphabet
):
    print("\n" + "=" * 70)
    print("ПОРІВНЯЛЬНИЙ АНАЛІЗ")
    print("=" * 70)

    print(
        f"{'Показник':<30}"
        f"{'Caesar':<18}"
        f"{'Affine':<18}"
    )

    print("-" * 70)

    print(
        f"{'Розмір алфавіту':<30}"
        f"{len(alphabet):<18}"
        f"{len(alphabet):<18}"
    )

    print(
        f"{'Ключ / параметри':<30}"
        f"{'shift = ' + str(caesar_key):<18}"
        f"{'a = ' + str(affine_a) + ', b = ' + str(affine_b):<18}"
    )

    print(
        f"{'Довжина тексту':<30}"
        f"{len(caesar_result):<18}"
        f"{len(affine_result):<18}"
    )

    print(
        f"{'Різних символів':<30}"
        f"{len(set(caesar_result.lower())):<18}"
        f"{len(set(affine_result.lower())):<18}"
    )

    print(
        f"{'Розшифрування':<30}"
        f"{'так':<18}"
        f"{'так':<18}"
    )

    print("=" * 70)

    print("\nВисновок:")
    print(
        "Шифр Цезаря простіший, оскільки використовує "
        "один параметр — зсув."
    )

    print(
        "Афінний шифр використовує два параметри — "
        "a та b, тому ключ має складнішу структуру."
    )


# Головна функція програми
def main():

    print("=" * 50)
    print("     ПОРІВНЯННЯ КЛАСИЧНИХ ШИФРІВ")
    print("=" * 50)

    # Введення персональних даних
    name = input("Введіть ім'я: ")
    surname = input("Введіть прізвище: ")
    birth_date = input(
        "Введіть дату народження (ДД.ММ.РРРР): "
    )

    # Введення тексту
    text = input(
        "Введіть текст для шифрування: "
    )

    # Визначаємо алфавіт
    alphabet = get_alphabet(text)

    if alphabet == UKRAINIAN_ALPHABET:
        alphabet_name = "Український"
    else:
        alphabet_name = "Англійський"

    # Генеруємо персональні ключі
    caesar_key = generate_caesar_key(
        birth_date,
        len(alphabet)
    )

    affine_a, affine_b = generate_affine_key(
        surname,
        birth_date,
        alphabet
    )

    print("\n--- Персональні ключі ---")
    print(f"Ім'я: {name}")
    print(f"Прізвище: {surname}")
    print(f"Дата народження: {birth_date}")
    print(f"Використаний алфавіт: {alphabet_name}")
    print(f"Кількість символів алфавіту: {len(alphabet)}")
    print(f"Caesar shift = {caesar_key}")
    print(f"Affine: a = {affine_a}, b = {affine_b}")

    # Головне меню
    while True:

        print("\n" + "=" * 40)
        print("МЕНЮ")
        print("=" * 40)
        print("1 — Шифр Цезаря")
        print("2 — Афінний шифр")
        print("3 — Використати обидва шифри")
        print("4 — Brute force для Цезаря")
        print("0 — Вихід")

        choice = input("\nОберіть дію: ")

        if choice == "1":

            encrypted = caesar_encrypt(
                text,
                caesar_key,
                alphabet
            )

            print("\n--- Шифр Цезаря ---")
            print(f"Ключ: shift = {caesar_key}")
            print(f"Алфавіт: {alphabet_name}")

            print(
                f"\nЗашифрований текст:\n{encrypted}"
            )

            print(
                f"\nРозшифрований текст:\n"
                f"{caesar_decrypt(encrypted, caesar_key, alphabet)}"
            )

        elif choice == "2":

            encrypted = affine_encrypt(
                text,
                affine_a,
                affine_b,
                alphabet
            )

            print("\n--- Афінний шифр ---")
            print(
                f"Ключ: a = {affine_a}, b = {affine_b}"
            )

            print(f"Алфавіт: {alphabet_name}")

            print(
                f"\nЗашифрований текст:\n{encrypted}"
            )

            print(
                f"\nРозшифрований текст:\n"
                f"{affine_decrypt(encrypted, affine_a, affine_b, alphabet)}"
            )

        elif choice == "3":

            caesar_result = caesar_encrypt(
                text,
                caesar_key,
                alphabet
            )

            affine_result = affine_encrypt(
                text,
                affine_a,
                affine_b,
                alphabet
            )

            print("\n--- РЕЗУЛЬТАТИ ---")

            print(
                f"\nCaesar:\n{caesar_result}"
            )

            print(
                f"\nAffine:\n{affine_result}"
            )

            print("\n--- Перевірка розшифрування ---")

            print(
                f"\nCaesar:\n"
                f"{caesar_decrypt(caesar_result, caesar_key, alphabet)}"
            )

            print(
                f"\nAffine:\n"
                f"{affine_decrypt(affine_result, affine_a, affine_b, alphabet)}"
            )

            show_comparison(
                text,
                caesar_result,
                affine_result,
                caesar_key,
                affine_a,
                affine_b,
                alphabet
            )

        elif choice == "4":

            encrypted = caesar_encrypt(
                text,
                caesar_key,
                alphabet
            )

            caesar_brute_force(
                encrypted,
                alphabet
            )

        elif choice == "0":

            print("\nПрограму завершено.")
            break

        else:
            print("\nНевірний вибір. Спробуйте ще раз.")


# Запуск програми
if __name__ == "__main__":
    main()
