import os
import io
from os.path import dirname
from helpers.writer import Writer
from services.word_evaluator import Wordset, WeightedWordDict


def generate_static_training_data(filepath: str, weights: WeightedWordDict):
    '''Generates a list of tuples: (filename, evaluated value) for each
       email in a set.'''
    filenames = [
        filename
        for filename in os.listdir(dirname(filepath))
        if filename[0] != '!'
    ]
    directory = dirname(filepath)
    file = io.StringIO()
    words_per_file = [
        (filename, Wordset(f'{directory}/{filename}', False).evaluate(weights))
        for filename in filenames
    ]
    file.seek(0)
    return words_per_file


def try_cutoff_on_generated_data(
    generated_data: list,
    cutoff: float,
    logs: bool = False,
):
    '''Using the generated list of tuples, run a test filter operation on the
       training data generated. Grab every email's evaluated
       value and match it against the cutoff. 
       Return an in-memory !prediction.txt file.'''
    file = io.StringIO()
    for generated_tuple in generated_data:
        score = generated_tuple[1]
        tag = "OK" if score > cutoff else "SPAM"
        line = f"{generated_tuple[0]} {tag}\n"
        writer = Writer("Word Matcher", logs)
        writer.print(data=line, file=file, multiple=logs, force=True)
    file.seek(0)
    return file


def score_corpus(
    filepath: str,
    weights: WeightedWordDict,
    cutoff: float,
    logs: bool = False,
):
    '''Evaluate every email in a given set, match it against the "cutoff"
       and write to a !prediction.txt file on disk.'''
    filenames = [
        filename for filename in os.listdir(filepath) if filename[0] != '!'
    ]

    wordset = []
    with open(f'{filepath}/!prediction.txt', "w", encoding="utf-8") as file:
        for filename in filenames:
            wordset = Wordset(f'{filepath}/{filename}', False)
            score = wordset.evaluate(weights)
            tag = "OK" if score > cutoff else "SPAM"
            line = f"{filename} {tag}\n"
            writer = Writer("Test on corpus", logs)
            writer.print(data=line, file=file, multiple=logs, force=True)
        file.seek(0)
        return file