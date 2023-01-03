import re


def _clean_text(text: str) -> str:
    return re.sub('</?.+?>|<!--.+?-->', '', re.sub('=?\n', '', text))


def get_words(text: str) -> list[str]:
    return list(
        filter(
            lambda word: len(word),
            re.split('\.+|\s+|\n+', _clean_text(text)),
        )
    )
