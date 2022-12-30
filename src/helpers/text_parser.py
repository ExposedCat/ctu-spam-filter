import re


class TextParser:
    @staticmethod
    def clean(text: str) -> str:
        return re.sub('</?.+?>|<!--.+?-->', '', re.sub('=?\n', '', text))

    @staticmethod
    def get_words(text: str) -> list[str]:
        return list(
            filter(
                lambda word: len(word),
                re.split('\.+|\s+|\n+', TextParser.clean(text)),
            )
        )
