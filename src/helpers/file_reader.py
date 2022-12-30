from io import TextIOWrapper


class FileReader:
    @staticmethod
    def read_text(path: str, extract: bool = True) -> str | TextIOWrapper:
        file = open(path, 'r', encoding='utf-8')
        return file.read() if extract else file
