from os.path import dirname, basename
from helpers.file_reader import read_text_file
from helpers.text_parser import get_words
from evaluation.utils import EvaluationUtils


class WeightedWordDict:
    def __init__(self, first: dict, second: dict, threshold: int = 0):
        '''Create a dictionary of words in two wordsets. The dictionary
        entries will consist of key-value pairs, where key is the word,
        and value is the likelihood (-1 to 1) of it being in the first
        or second wordset. '''
        self.counter = {}
        for word in dict(first, **second):
            total = first.get(word, 0) + second.get(word, 0)
            if threshold == 0 or total > threshold:
                diff = first.get(word, 0) - second.get(word, 0)
                self.counter[word] = round(diff / total, 2)

    def as_dict(self) -> dict:
        return self.counter


class Wordset:
    def __init__(
        self,
        filepath: str,
        from_classification: bool = True,
        tag: str | None = None,
    ):
        '''Generate a wordset either from a classification (!truth.txt), or a
        single file'''
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
                self.words += get_words(
                    read_text_file(f'{directory}/{filename}')  # type: ignore
                )

    def get_from_file(self, filepath: str):
        return get_words(read_text_file(filepath))  # type: ignore

    def to_counter(self) -> dict:
        ''' Convert the Wordset to a counter, where the value of each word is the
            amount of times it is encountered in the set.'''
        counter = {}
        for word in self.words:
            counter[word] = counter.get(word, 0) + 1
        return counter

    def evaluate(self, weights: WeightedWordDict) -> float:
        ''' Evaluate a wordset based on a WeightedWordDict. 
            The evaluation result is the sum of all the weights of the words
            in a given wordset, normalized to the (-1,1) range.'''
        counter = weights.as_dict()
        amount_of_words = len([word for word in self.words if word in counter])

        '''
        We tried experimenting with fuzzy wordmatching, however this was way 
        slower and produced worse results. Spammers are usually not typing
        out emails on their own, so it's way more likely for spam words to be
        exact matches anyway.

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
        amount_of_words = amount_of_words if amount_of_words != 0 else 1
        value = 0
        for word in self.words:
            value += counter.get(word, 0) / amount_of_words
        return value
