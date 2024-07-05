""""""

import re

snake_pattern = re.compile(r"(?<!^)(?=[A-Z])")


def to_snake(word: str) -> str:
    return snake_pattern.sub("_", word).lower()


def to_pascal(word: str) -> str:
    return "".join(w.title() for w in word.split("_"))
