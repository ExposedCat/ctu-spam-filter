from os.path import dirname, basename
from helpers.file_reader import FileReader
from helpers.text_parser import TextParser
from evaluation.utils import EvaluationUtils


class WeightedWordDict:
    def __init__(self, first: dict, second: dict, threshold: int = 0):
        self.counter = {}
        for word in dict(first, **second):
            total = first.get(word, 0) + second.get(word, 0)
            if threshold == 0 or total > threshold:
                diff = first.get(word, 0) - second.get(word, 0)
                self.counter[word] = round(diff / total, 2),
        #self.reweigh()

    def as_dict(self) -> dict:
        return self.counter

    def reweigh(self):
        for word in self.counter:
            temp_dict = {word: self.counter[word][1] for word in self.counter}
            max_freq_key = max(temp_dict, key=temp_dict.get)  # type: ignore
            self.counter[word] = (
                self.counter[word][0],
                temp_dict[word] / temp_dict[max_freq_key],
            )


class Wordset:
    def __init__(
        self,
        filepath: str,
        from_classification: bool = True,
        tag: str | None = None,
    ):
        self.words = []
        if from_classification:
            self.build_from_classification(filepath, tag)
        else:
            self.words = self.get_from_file(filepath)

    def build_from_classification(self, filepath: str, tag: str | None):
        classification = EvaluationUtils.read_classification_from_file(
            filepath
        )
        directory = dirname(filepath)
        for filename in classification:
            if tag is None or classification[filename] == tag:
                self.words += TextParser.get_words(
                    FileReader.read_text(f'{directory}/{filename}')  # type: ignore
                )

    def get_from_file(self, filepath: str):
        return TextParser.get_words(
            FileReader.read_text(filepath)  # type: ignore
        )

    def to_counter(self) -> dict:
        counter = {}
        for word in self.words:
            counter[word] = counter.get(word, 0) + 1
        return counter

    def evaluate(self, weights: WeightedWordDict) -> float:
        counter = weights.as_dict()
        amount_of_words = len([word for word in self.words if word in counter])

        '''
        # 
        # FUZZY MATCHING UNRELIABLE?
        # 
        close_matches = difflib.get_close_matches(word, weights.keys())
        if len(close_matches):
            close_match_dict = {
                word: weights[word][0] for word in close_matches
            }
            preferred_match = max(close_match_dict, key=close_match_dict.get)
            value += (weights.get(preferred_match)[0]) / amount_of_words
        '''

        # Do not divide by zero
        amount_of_words = amount_of_words if amount_of_words else 1
        #??????????????????????????????????????????????????????????
        #if not 0 then amount_of_words, else 0?????????????????????
        value = 0
        for word in self.words:
            value += counter.get(word, (0, 0))[0] / amount_of_words
        return value
