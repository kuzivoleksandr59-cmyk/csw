def input() -> int:
    while True:
        try:
            frg_temp = int(input("Enter temperature in F: "))
            return frg_temp
        except ValueError:
            print("Please enter a valid integer.")


def convert(temp_f: float) -> float:
    cels_temp = (temp_f - 32) * 5 / 9
    return round(cels_temp, 1)


def main():
    while True:
        frg_user_temp = input()
        cels_temp = convert(frg_user_temp)

        print(f"Temperature in C: {cels_temp}")

        proceed = input("Want to proceed? y/n: ").strip().lower()
        if proceed != 'y':
            break


if __name__ == '__main__':
    main()