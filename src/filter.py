from os.path import abspath
from helpers.writer import Writer
from services.word_evaluator import Wordset, WeightedWordDict
from services.word_matcher import WordMatcher
from evaluation.quality import QualityComputor


class SpamFilter:
    def __init__(
        self,
        directory: str = abspath("../test/first"),
        ham_tag: str = "OK",
        spam_tag: str = "SPAM",
    ):
        self.ham_counter = Wordset(
            f'{directory}/!truth.txt', tag=ham_tag
        ).count()
        self.spam_counter = Wordset(
            f'{directory}/!truth.txt', tag=spam_tag
        ).count()
        self.weighted_words = WeightedWordDict(
            self.ham_counter, self.spam_counter, 100
        )

    def get_max_value(
        self,
        first_dir: str = abspath("../test/first"),
        second_dir: str = abspath("../test/second"),
        logs: bool = True,
    ) -> None:
        writer = Writer("Max Value", logs)
        maxval = (0, 0)
        for i in range(-100, 0):
            WordMatcher.debug_check_corpus(
                f'{first_dir}/!truth.txt', self.weighted_words, i / 100
            )
            quality = QualityComputor.compute(first_dir)
            if maxval[0] < quality:
                maxval = quality, i
            writer.print((round(quality, 2), i / 100))
        writer.print(f"Max value: {round(maxval[0],2)} {maxval[1]/100}")

        self.weighted_words = WeightedWordDict(
            self.ham_counter, self.spam_counter, 1
        )
        WordMatcher.debug_check_corpus(
            f'{second_dir}/!truth.txt', self.weighted_words, maxval[1] / 100
        )
        writer.print(QualityComputor.compute(second_dir))
