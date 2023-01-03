from io import TextIOWrapper
from helpers.file_reader import read_text_file


class EvaluationUtils:
    @staticmethod
    def read_classification_from_file(path: str):
        contents = read_text_file(path, False)
        classification = {}
        for line in contents:
            result = line.split()
            if len(result) != 2:
                continue
            classification[result[0]] = result[1]
        return classification

    @staticmethod
    def read_classification_from_memory_file(file: TextIOWrapper):
        contents = file
        file.seek(0)
        classification = {}
        for line in contents:
            result = line.split()
            if len(result) != 2:
                continue
            classification[result[0]] = result[1]
        return classification
