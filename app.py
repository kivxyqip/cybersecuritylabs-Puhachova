import re
from datetime import datetime


def analyze_password(password, first_name, last_name, birth_date_str):
    score = 0
    feedback = []
    personal_matches = []

    if not password:
        return 0, ["Пароль порожній!"], []

    pwd_lower = password.lower()

    # 1. Перевірка на наявність персональних даних
    if first_name and len(first_name) > 2 and first_name.lower() in pwd_lower:
        personal_matches.append(f"Ім'я ({first_name})")

    if last_name and len(last_name) > 2 and last_name.lower() in pwd_lower:
        personal_matches.append(f"Прізвище ({last_name})")

    # Аналіз дати народження
    try:
        bdate = datetime.strptime(birth_date_str, "%d.%m.%Y")
        year_str = str(bdate.year)
        short_year = year_str[2:]
        day_str = f"{bdate.day:02d}"
        month_str = f"{bdate.month:02d}"

        if year_str in password:
            personal_matches.append(f"Рік народження ({year_str})")
        elif short_year in password and len(password) < 12:
            personal_matches.append(f"Скорочений рік народження ({short_year})")

        if (day_str + month_str) in password or (month_str + day_str) in password:
            personal_matches.append("День та місяць народження")
    except ValueError:
        pass

    # 2. Оцінка за довжину (макс. 5 балів)
    if len(password) >= 14:
        score += 5
    elif len(password) >= 10:
        score += 4
    elif len(password) >= 8:
        score += 2
    else:
        feedback.append("Пароль занадто короткий (рекомендовано від 10-12 символів).")

    # 3. Перевірка різноманіття символів (макс. 5 балів)
    has_upper = bool(re.search(r'[A-ZА-ЯІЇЄҐ]', password))
    has_lower = bool(re.search(r'[a-zа-яіїєґ]', password))
    has_digits = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password))

    types_count = sum([has_upper, has_lower, has_digits, has_special])

    if types_count == 4:
        score += 5
    elif types_count == 3:
        score += 3
    elif types_count == 2:
        score += 2
    else:
        score += 1

    if not has_upper:
        feedback.append("Додайте великі літери (A-Z, А-Я).")
    if not has_lower:
        feedback.append("Додайте малі літери (a-z, а-я).")
    if not has_digits:
        feedback.append("Додайте цифри (0-9).")
    if not has_special:
        feedback.append("Додайте спеціальні символи (!@#$%^&*).")

    # 4. Штраф за персональні дані
    if personal_matches:
        score = max(1, score - 3)
        feedback.append("УВАГА: Виявлено персональні дані! Це робить пароль вразливим до атак соціальної інженерії.")

    score = min(10, max(1, score))
    return score, personal_matches, feedback


def main():
    print("=" * 60)
    print("      ПРОГРАМА АНАЛІЗУ БЕЗПЕКИ ПАРОЛІВ (ЛР №1)")
    print("=" * 60)

    # Запит персональних даних користувача з можливістю заповнення за замовчуванням
    print("Введіть персональні дані для аналізу (або натисніть Enter для значень за замовчуванням):")

    input_fname = input("Ім'я: ").strip()
    first_name = input_fname if input_fname else "Марія"

    input_lname = input("Прізвище: ").strip()
    last_name = input_lname if input_lname else "Пугачова"

    input_bdate = input("Дата народження ДД.ММ.РРРР: ").strip()
    birth_date_str = input_bdate if input_bdate else "31.01.2004"

    print("\n" + "-" * 60)
    print(f"Дані для перевірки: {last_name} {first_name}, {birth_date_str}")
    print("-" * 60)

    while True:
        pwd = input("\nВведіть пароль для перевірки (або 'exit' для виходу): ").strip()

        if pwd.lower() == 'exit':
            print("\nРоботу завершено.")
            break

        score, matches, feedback = analyze_password(pwd, first_name, last_name, birth_date_str)

        print("\n" + "." * 40)
        print(f"РЕЗУЛЬТАТ ОЦІНКИ: {score} / 10 балів")

        if score >= 8:
            print("Статус: ВИСОКИЙ РІВЕНЬ БЕЗПЕКИ")
        elif score >= 5:
            print("Статус: СЕРЕДНІЙ РІВЕНЬ БЕЗПЕКИ")
        else:
            print("Статус: НИЗЬКИЙ РІВЕНЬ БЕЗПЕКИ")

        if matches:
            print("\n[!] Знайдені персональні дані у паролі:")
            for m in matches:
                print(f"  - {m}")
        else:
            print("\n[+] Персональних даних у паролі не виявлено.")

        if feedback:
            print("\n[*] Рекомендації щодо покращення:")
            for f in feedback:
                print(f"  - {f}")
        print("." * 40)


if __name__ == "__main__":
    main()
