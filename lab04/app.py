import hashlib
import math
import os


# Параметри спрощеної RSA-моделі
P = 1009
Q = 1013

N = P * Q
PHI = (P - 1) * (Q - 1)


def read_document(document_path):
    """Зчитування документа та обчислення його SHA-256 хешу."""

    if not os.path.isfile(document_path):
        print("Файл документа не знайдено!")
        return None, None

    try:
        with open(document_path, "rb") as file:
            document_data = file.read()

        document_hash = hashlib.sha256(document_data).hexdigest()
        return document_hash, document_data

    except OSError:
        print("Помилка під час читання документа!")
        return None, None


def generate_keys():
    print("\n--- Генерація ключів ---")

    name = input("Введіть ПІБ: ").strip()
    birth_date = input("Введіть дату народження (ДДММРРРР): ").strip()
    secret_word = input("Введіть секретне слово: ").strip()

    if not name or not birth_date or not secret_word:
        print("Усі поля повинні бути заповнені!")
        return

    personal_data = name + birth_date + secret_word

    # Формування основи приватного ключа
    private_hash = hashlib.sha256(
        personal_data.encode("utf-8")
    ).hexdigest()

    private_seed = int(private_hash, 16)

    # Формування приватного показника
    d = private_seed % (PHI - 2) + 2

    while math.gcd(d, PHI) != 1:
        d += 1
        if d >= PHI:
            d = 2

    # Формування відкритого показника
    e = pow(d, -1, PHI)

    try:
        # Збереження приватного ключа
        with open("private_key.txt", "w", encoding="utf-8") as file:
            file.write(private_hash + "\n")
            file.write(str(d) + "\n")
            file.write(str(N))

        # Збереження відкритого ключа
        with open("public_key.txt", "w", encoding="utf-8") as file:
            file.write(str(e) + "\n")
            file.write(str(N))

        print("\nПару ключів успішно сформовано!")
        print("Приватний ключ збережено у private_key.txt")
        print("Відкритий ключ збережено у public_key.txt")

    except OSError:
        print("Помилка під час збереження ключів!")


def create_signature():
    print("\n--- Створення цифрового підпису ---")

    if not os.path.isfile("private_key.txt"):
        print("Спочатку потрібно згенерувати ключі!")
        return

    document_path = input("Введіть назву файлу документа: ").strip()

    document_hash, _ = read_document(document_path)

    if document_hash is None:
        return

    try:
        # Зчитування приватного ключа
        with open("private_key.txt", "r", encoding="utf-8") as file:
            private_hash = file.readline().strip()
            d = int(file.readline().strip())
            n = int(file.readline().strip())

        if len(private_hash) != 64 or n != N:
            raise ValueError

        if not (1 < d < PHI) or math.gcd(d, PHI) != 1:
            raise ValueError

        # Перетворення хешу документа на число
        hash_number = int(document_hash, 16) % n

        # Створення цифрового підпису
        signature = pow(hash_number, d, n)

        with open("signature.txt", "w", encoding="utf-8") as file:
            file.write(str(signature))

        print("\nSHA-256 хеш документа:", document_hash)
        print("Цифровий підпис:", signature)
        print("Підпис збережено у файлі signature.txt")

    except (OSError, ValueError, IndexError):
        print("Помилка! Приватний ключ пошкоджений або має неправильний формат.")


def verify_signature():
    print("\n--- Перевірка цифрового підпису ---")

    if not os.path.isfile("public_key.txt") or not os.path.isfile("signature.txt"):
        print("Необхідно спочатку згенерувати ключі та створити підпис!")
        return

    document_path = input("Введіть назву файлу документа: ").strip()

    document_hash, _ = read_document(document_path)

    if document_hash is None:
        return

    try:
        # Зчитування відкритого ключа
        with open("public_key.txt", "r", encoding="utf-8") as file:
            e = int(file.readline().strip())
            n = int(file.readline().strip())

        # Зчитування цифрового підпису
        with open("signature.txt", "r", encoding="utf-8") as file:
            signature = int(file.read().strip())

        if n != N or not (1 < e < PHI):
            raise ValueError

        if not (0 <= signature < n):
            raise ValueError

        # Обчислення числового значення хешу
        hash_number = int(document_hash, 16) % n

        # Перевірка підпису відкритим ключем
        decrypted_signature = pow(signature, e, n)

        print("\nХеш документа:", hash_number)
        print("Результат перевірки підпису:", decrypted_signature)

        if hash_number == decrypted_signature:
            print("\nПідпис ДІЙСНИЙ!")
        else:
            print("\nПідпис ПІДРОБЛЕНИЙ! Документ або підпис було змінено.")

    except (OSError, ValueError):
        print("Помилка! Відкритий ключ або підпис пошкоджений.")


def test_modified_document():
    print("\n--- Перевірка зміненого документа ---")

    if not os.path.isfile("public_key.txt") or not os.path.isfile("signature.txt"):
        print("Спочатку потрібно згенерувати ключі та створити підпис!")
        return

    document_path = input("Введіть назву зміненого документа: ").strip()

    document_hash, _ = read_document(document_path)

    if document_hash is None:
        return

    try:
        # Зчитування відкритого ключа
        with open("public_key.txt", "r", encoding="utf-8") as file:
            e = int(file.readline().strip())
            n = int(file.readline().strip())

        # Зчитування підпису оригінального документа
        with open("signature.txt", "r", encoding="utf-8") as file:
            signature = int(file.read().strip())

        if n != N or not (1 < e < PHI):
            raise ValueError

        if not (0 <= signature < n):
            raise ValueError

        # Обчислення хешу зміненого документа
        hash_number = int(document_hash, 16) % n

        # Перевірка старого підпису для нового документа
        decrypted_signature = pow(signature, e, n)

        print("\nХеш зміненого документа:", hash_number)
        print("Результат перевірки підпису:", decrypted_signature)

        if hash_number == decrypted_signature:
            print("\nПідпис ДІЙСНИЙ!")
        else:
            print("\nПідпис ПІДРОБЛЕНИЙ! Документ було змінено.")

    except (OSError, ValueError):
        print("Помилка! Відкритий ключ або підпис пошкоджений.")


def test_forgery():
    print("\n--- Перевірка підробленого підпису ---")

    if not os.path.isfile("public_key.txt") or not os.path.isfile("signature.txt"):
        print("Спочатку потрібно згенерувати ключі та створити підпис!")
        return

    document_path = input("Введіть назву початкового документа: ").strip()

    document_hash, _ = read_document(document_path)

    if document_hash is None:
        return

    try:
        # Зчитування відкритого ключа
        with open("public_key.txt", "r", encoding="utf-8") as file:
            e = int(file.readline().strip())
            n = int(file.readline().strip())

        # Зчитування оригінального підпису
        with open("signature.txt", "r", encoding="utf-8") as file:
            signature = int(file.read().strip())

        if n != N or not (1 < e < PHI):
            raise ValueError

        if not (0 <= signature < n):
            raise ValueError

        # Зміна цифрового підпису
        forged_signature = (signature + 1) % n

        # Обчислення хешу документа
        hash_number = int(document_hash, 16) % n

        # Перевірка зміненого підпису
        decrypted_signature = pow(forged_signature, e, n)

        print("\nОригінальний підпис:", signature)
        print("Змінений підпис:", forged_signature)
        print("Хеш документа:", hash_number)
        print("Результат перевірки:", decrypted_signature)

        if hash_number == decrypted_signature:
            print("\nПідпис ДІЙСНИЙ!")
        else:
            print("\nПідпис ПІДРОБЛЕНИЙ! Зміну підпису виявлено.")

    except (OSError, ValueError):
        print("Помилка! Відкритий ключ або підпис пошкоджений.")


def main():
    while True:
        print("\n========== СИСТЕМА ЦИФРОВОГО ПІДПИСУ ==========")
        print("1. Генерація пари ключів")
        print("2. Створення цифрового підпису")
        print("3. Перевірка цифрового підпису")
        print("4. Перевірка зміненого документа")
        print("5. Перевірка підробленого підпису")
        print("0. Вихід")

        choice = input("\nОберіть дію: ").strip()

        if choice == "1":
            generate_keys()
        elif choice == "2":
            create_signature()
        elif choice == "3":
            verify_signature()
        elif choice == "4":
            test_modified_document()
        elif choice == "5":
            test_forgery()
        elif choice == "0":
            print("\nЗавершення роботи програми.")
            break
        else:
            print("\nНевірний вибір. Спробуйте ще раз.")


if __name__ == "__main__":
    main()

