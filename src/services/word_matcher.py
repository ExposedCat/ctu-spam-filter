import os
import io
from os.path import dirname
from helpers.writer import Writer
from services.word_evaluator import Wordset, WeightedWordDict


class WordMatcher:
    @staticmethod
    def try_on_corpus(
        filepath: str,
        weights: WeightedWordDict,
        threshold: float,
        logs: bool = False,
    ):
        filenames = [
            filename
            for filename in os.listdir(dirname(filepath))
            if filename[0] != '!'
        ]
        wordset = []
        directory = dirname(filepath)
        file = io.StringIO()
        for filename in filenames:
            wordset = Wordset(f'{directory}/{filename}', False)
            score = wordset.evaluate(weights)
            tag = "OK" if score > threshold else "SPAM"
            line = f"{filename} {tag}\n"
            writer = Writer("Word Matcher", logs)
            writer.print(data=line, file=file, multiple=logs, force=True)
        file.seek(0)
        return file

    @staticmethod
    def test_on_corpus(
        filepath: str,
        weights: WeightedWordDict,
        threshold: float,
        logs: bool = False,
    ):
        filenames = [
            filename for filename in os.listdir(filepath) if filename[0] != '!'
        ]

        wordset = []
        with open(
            f'{filepath}/!prediction.txt', "w", encoding="utf-8"
        ) as file:
            for filename in filenames:
                wordset = Wordset(f'{filepath}/{filename}', False)
                score = wordset.evaluate(weights)
                tag = "OK" if score > threshold else "SPAM"
                line = f"{filename} {tag}\n"
                writer = Writer("Test on corpus", logs)
                writer.print(data=line, file=file, multiple=logs, force=True)
