
from PIL import Image


# Маркери початку та кінця повідомлення
START_MARKER = b"<|START|>"
END_MARKER = b"<|END|>"


def hide_message(image_path, message, output_path):
    # Відкриваємо вихідне зображення
    image = Image.open(image_path).convert("RGB")
    pixels = list(image.get_flattened_data())

    # Перетворюємо текст у байти UTF-8 та додаємо маркери
    message_bytes = message.encode("utf-8")
    full_message = START_MARKER + message_bytes + END_MARKER

    # Перші 32 біти містять довжину даних у байтах
    binary_message = format(len(full_message), "032b")
    binary_message += "".join(
        format(byte, "08b") for byte in full_message
    )

    # Перевіряємо місткість зображення
    capacity_bits = len(pixels) * 3

    if len(binary_message) > capacity_bits:
        raise ValueError(
            "Повідомлення завелике для цього зображення!"
        )

    # Аналіз місткості
    used_bits = len(binary_message)
    usage_percent = used_bits / capacity_bits * 100

    # Вбудовуємо біти у молодші біти RGB-каналів
    new_pixels = []
    bit_index = 0

    for pixel in pixels:
        new_pixel = []

        for channel in pixel:
            if bit_index < len(binary_message):
                channel = (
                    (channel & 254)
                    | int(binary_message[bit_index])
                )
                bit_index += 1

            new_pixel.append(channel)

        new_pixels.append(tuple(new_pixel))

    # Зберігаємо результат у форматі PNG
    stego_image = Image.new("RGB", image.size)
    stego_image.putdata(new_pixels)
    stego_image.save(output_path, format="PNG")

    # Виводимо технічний звіт
    print("\n" + "=" * 42)
    print("       ЗВІТ ПРО ПРИХОВУВАННЯ")
    print("=" * 42)
    print("Статус: повідомлення успішно приховано")
    print(f"Розмір зображення: {image.width} x {image.height}")
    print("Метод приховування: LSB")
    print("Канали: RGB")
    print("Кодування тексту: UTF-8")
    print("Формат вихідного файлу: PNG")
    print("-" * 42)
    print(f"Розмір початкового тексту: {len(message_bytes)} байтів")
    print(
        f"Розмір маркерів: "
        f"{len(START_MARKER) + len(END_MARKER)} байтів"
    )
    print(f"Розмір даних із маркерами: {len(full_message)} байтів")
    print("Заголовок довжини: 32 біти")
    print(f"Доступна місткість: {capacity_bits} бітів")
    print(f"Використано: {used_bits} бітів")
    print(f"Використання місткості: {usage_percent:.4f}%")
    print("-" * 42)
    print(f"Маркер початку: {START_MARKER.decode('ascii')}")
    print(f"Маркер кінця: {END_MARKER.decode('ascii')}")
    print("Призначення маркерів: перевірка меж повідомлення")
    print(f"Файл збережено: {output_path}")
    print("=" * 42)


def extract_message(image_path):
    # Відкриваємо зображення з прихованими даними
    image = Image.open(image_path).convert("RGB")
    pixels = list(image.get_flattened_data())

    # Зчитуємо молодші біти RGB-каналів
    bits = "".join(
        str(channel & 1)
        for pixel in pixels
        for channel in pixel
    )

    if len(bits) < 32:
        raise ValueError(
            "Недостатньо даних для читання повідомлення!"
        )

    # Зчитуємо довжину повідомлення
    message_length = int(bits[:32], 2)
    available_bytes = (len(bits) - 32) // 8

    if message_length > available_bytes:
        raise ValueError(
            "Некоректна довжина даних. "
            "Можливо, зображення не містить повідомлення."
        )

    # Перетворюємо біти на байти
    message_bits = bits[32:32 + message_length * 8]
    message_bytes = bytes(
        int(message_bits[i:i + 8], 2)
        for i in range(0, len(message_bits), 8)
    )

    # Перевіряємо маркери
    if not message_bytes.startswith(START_MARKER):
        raise ValueError(
            "Маркер початку не знайдено. "
            "Файл може не містити повідомлення цієї програми."
        )

    if not message_bytes.endswith(END_MARKER):
        raise ValueError(
            "Маркер кінця не знайдено. Дані можуть бути пошкоджені."
        )

    # Видаляємо маркери
    text_bytes = message_bytes[
        len(START_MARKER):-len(END_MARKER)
    ]

    extracted_text = text_bytes.decode("utf-8")

    print("\n--- Результат перевірки ---")
    print("Маркер початку: знайдено")
    print("Маркер кінця: знайдено")
    print("Структура повідомлення: коректна")
    print(f"Довжина даних із маркерами: {message_length} байтів")

    return extracted_text


def main():
    # Оригінальний текст зберігається до завершення програми
    last_original_message = None

    while True:
        print("\n" + "=" * 42)
        print("       СТЕГАНОГРАФІЯ ЗОБРАЖЕНЬ")
        print("=" * 42)
        print("1. Приховати повідомлення в зображенні")
        print("2. Вилучити повідомлення із зображення")
        print("3. Вихід")
        print("=" * 42)

        choice = input("Оберіть дію (1-3): ").strip()

        if choice == "1":
            print("\n--- Приховування повідомлення ---")

            image_path = input(
                "Введіть шлях до вихідного зображення: "
            ).strip().strip('"')

            message = input(
                "Введіть текст, який потрібно приховати: "
            )

            output_path = input(
                "Назва вихідного PNG-файлу "
                "(Enter — stego_image.png): "
            ).strip().strip('"')

            if not output_path:
                output_path = "stego_image.png"

            if not output_path.lower().endswith(".png"):
                output_path += ".png"

            try:
                hide_message(image_path, message, output_path)
                last_original_message = message

                print(
                    "\nДля вилучення повідомлення "
                    "оберіть пункт 2."
                )

            except (OSError, ValueError, OverflowError) as error:
                last_original_message = None
                print(f"\nПомилка: {error}")

        elif choice == "2":
            print("\n--- Вилучення повідомлення ---")

            image_path = input(
                "Введіть шлях до зображення "
                "з прихованим повідомленням: "
            ).strip().strip('"')

            try:
                extracted_message = extract_message(image_path)

                print("\nВилучене повідомлення:")
                print("-" * 30)
                print(extracted_message)
                print("-" * 30)

                # Порівнюємо з оригінальним текстом
                if last_original_message is not None:
                    check_choice = input(
                        "\nПорівняти вилучений текст "
                        "з оригіналом? (т/н): "
                    ).strip().lower()

                    if check_choice in ("т", "так", "y", "yes"):
                        if extracted_message == last_original_message:
                            print(
                                "УСПІХ: початковий і вилучений "
                                "тексти повністю збігаються!"
                            )
                        else:
                            print(
                                "ПОМИЛКА: початковий і вилучений "
                                "тексти відрізняються!"
                            )
                else:
                    print(
                        "Оригінальний текст недоступний для "
                        "автоматичного порівняння в цьому запуску."
                    )

                # За бажанням зберігаємо текст у файл
                save_choice = input(
                    "\nЗберегти текст у TXT-файл? (т/н): "
                ).strip().lower()

                if save_choice in ("т", "так", "y", "yes"):
                    text_path = input(
                        "Назва TXT-файлу "
                        "(Enter — extracted_message.txt): "
                    ).strip().strip('"')

                    if not text_path:
                        text_path = "extracted_message.txt"

                    if not text_path.lower().endswith(".txt"):
                        text_path += ".txt"

                    with open(
                        text_path, "w", encoding="utf-8"
                    ) as file:
                        file.write(extracted_message)

                    print(f"Текст збережено у файл: {text_path}")

            except (OSError, ValueError, UnicodeError, OverflowError) as error:
                print(
                    f"\nНе вдалося вилучити повідомлення: {error}"
                )

        elif choice == "3":
            print("\nПрограму завершено.")
            break

        else:
            print("\nНевірний вибір. Введіть число від 1 до 3.")


if __name__ == "__main__":
    main()



