from io import TextIOWrapper


def read_text_file(path: str, extract: bool = True) -> str | TextIOWrapper:
    file = open(path, 'r', encoding='utf-8')
    return file.read() if extract else file
