import doctest
import sys


def reverse_words(text: str) -> str:
    """
    >>> reverse_words("hello")
    'olleh'
    >>> reverse_words("qwer tyui")
    'rewq iuyt'
    >>> reverse_words("")
    ''
    >>> reverse_words("a1bcd efg!h")
    'd1cba hgf!e'
    >>> reverse_words(12345)
    Traceback (most recent call last):
    ...
    TypeError: Вхідний аргумент повинен бути строкою (str).
    """
    if not isinstance(text, str):
        raise TypeError("Вхідний аргумент повинен бути строкою (str).")

    if not text.isascii():
        raise ValueError("Текст повинен містити тільки ASCII символи")

    def reverse_single_word(word: str) -> str:
        letters = [char for char in word if char.isalpha()]
        result = []

        for char in word:
            if char.isalpha():
                result.append(letters.pop())
            else:
                result.append(char)

        return "".join(result)

    words = text.split(" ")
    reversed_words = [reverse_single_word(w) for w in words]
    return " ".join(reversed_words)

def start_interactive_session():
    print("Введіть 'exit' для виходу.\n")

    while True:
        try:
            user_input = input("Введіть текст: ")
            if user_input == "exit":
                print("Завершення роботи")
                break

            result = reverse_words(user_input)
            print(f"Результат: {result}\n")

        except ValueError as val_err:
            print(f"Помилка введення: {val_err}\n")
        except KeyboardInterrupt:
            print("\nПрограму примусово завершено")
            break
        except Exception as err:
            print(f"Виникла помилка: {err}\n")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("Запуск doctest.....")
        failures, tests = doctest.testmod()
        print(f"Тестування завершено: {tests - failures}/{tests} тестів успішно пройдено")
    else:
        failures, __ = doctest.testmod()
        if not failures:
            start_interactive_session()
        else:
            print("Виявлено помилку")




