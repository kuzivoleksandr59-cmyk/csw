import sys
from typing import List, Tuple

MATCHING_PAIRS = {
    ')': '(',
    '}': '{',
    ']': '[',
    '>': '<'
}
OPENING_BRACKETS = set(MATCHING_PAIRS.values())
CLOSING_BRACKETS = set(MATCHING_PAIRS.keys())


def check_brackets(text: str) -> Tuple[bool, List[int]]:
    stack: List[Tuple[str, int]] = []
    invalid_indices: List[int] = []

    for index, char in enumerate(text):
        if char in OPENING_BRACKETS:
            stack.append((char, index))
        elif char in CLOSING_BRACKETS:
            if stack and stack[-1][0] == MATCHING_PAIRS[char]:
                stack.pop()
            else:
                invalid_indices.append(index)

    for _, index in stack:
        invalid_indices.append(index)

    invalid_indices.sort()
    return len(invalid_indices) == 0, invalid_indices


def format_visual_error(text: str, invalid_indices: List[int]) -> str:
    pointers = [" "] * len(text)
    for idx in invalid_indices:
        if 0 <= idx < len(pointers):
            pointers[idx] = "^"
    return "".join(pointers)


def validate_brackets(text: str) -> bool:
    is_valid, invalid_indices = check_brackets(text)
    if not is_valid:
        pos_str = ", ".join(map(str, invalid_indices))
        visual = format_visual_error(text, invalid_indices)
        raise ValueError(
            f"Дужки незбалансовані на позиціях: {pos_str}\n"
            f"{text}\n"
            f"{visual}"
        )
    return True


def main():
    try:
        user_input = input("Введіть строку: ")
        if validate_brackets(user_input):
            print("Строка валідна")
    except ValueError as e:
        print(f"\nПомилка валідації (ValueError):\n{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()