import re


def clean_email(text: str) -> str:
    return re.sub('</?.+?>|<!--.+?-->', '', re.sub('=?\n', '', text))
