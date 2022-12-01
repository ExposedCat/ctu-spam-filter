import re


def parse_words(text: str) -> list[str]:
    return list(filter(lambda word: len(word), re.split('\.+|\s+|\n+', text)))
