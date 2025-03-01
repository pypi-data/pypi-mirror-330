import re


def to_kebab(input_str: str) -> str:
    return re.sub(r"\s+", "-", input_str).lower()


def to_snake(input_str: str) -> str:
    return re.sub(r"\s+", "_", input_str).lower()


def to_lower(input_str: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "", input_str).lower()


def to_sentence(input_str: str) -> str:
    sentence = re.sub(r"(?<!^)(?=[A-Z])", "", input_str).lower()
    return sentence.capitalize()
