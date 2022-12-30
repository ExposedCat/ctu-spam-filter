from helpers.file_reader import FileReader


class EvaluationUtils:
    @staticmethod
    def read_classification_from_file(path: str):
        contents = FileReader.read_text(path, False)
        classification = {}
        for line in contents:
            result = line.split()
            if len(result) != 2:
                continue
            classification[result[0]] = result[1]
        return classification

    def read_classification_from_memory_file(file):
        contents = file
        file.seek(0)
        classification = {}
        for line in contents:
            result = line.split()
            if len(result) != 2:
                continue
            classification[result[0]] = result[1]
        return classification
