import re


def _clean_text(text: str) -> str:
    '''Clean up a text string - remove html tags, etc.'''
    return re.sub('</?.+?>|<!--.+?-->', '', re.sub('=?\n', '', text))


def get_words(text: str) -> list[str]:
    '''Get a list of words in a given text string.'''
    return list(
        filter(
            lambda word: len(word),
            re.split('\.+|\s+|\n+', _clean_text(text)),
        )
    )
