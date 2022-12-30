from os.path import dirname
from helpers.writer import Writer
from evaluation.utils import EvaluationUtils
from services.word_evaluator import Wordset, WeightedWordDict


class WordMatcher:
    @staticmethod
    def debug_check_corpus(
        filepath: str,
        weights: WeightedWordDict,
        threshold: float,
        logs: bool = False,
    ):
        classification = EvaluationUtils.read_classification_from_file(
            filepath
        )
        wordset = []
        directory = dirname(filepath)
        with open(f'{directory}/!prediction.txt', "w") as file:
            for filename in classification:
                wordset = Wordset(f'{directory}/{filename}', False)
                score = wordset.evaluate(weights)
                tag = "OK" if score > threshold else "SPAM"
                line = f"{filename} {tag}\n"
                writer = Writer("Word Matcher", logs)
                writer.print(data=line, file=file, multiple=logs, force=True)
