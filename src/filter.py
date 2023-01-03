import os
from helpers.writer import Writer
from services.word_matcher import WordMatcher
from evaluation.quality import QualityComputor
from services.word_evaluator import Wordset, WeightedWordDict


class MyFilter:
    def __init__(self, spam_tag="SPAM", ok_tag="OK"):
        self.spam_tag = spam_tag
        self.ok_tag = ok_tag
        self.trained = 0
        pass

    def train(
        self,
        set_dir,
        train_range=(-100, 20),
        desired_freq_cutoff=1,
        training_freq_cutoff=100,
        logs=False,
    ):

        self.trained = 1

        self.ok_counter = Wordset(
            f'{set_dir}/!truth.txt', tag=self.ok_tag
        ).to_counter()
        self.spam_counter = Wordset(
            f'{set_dir}/!truth.txt', tag=self.spam_tag
        ).to_counter()

        self.weighted_words = WeightedWordDict(
            self.ok_counter, self.spam_counter, training_freq_cutoff
        )

        writer = Writer("Training", logs)

        maxval = (0, 0)
        t1, t2 = train_range
        for i in range(t1, t2):
            prediction_file = WordMatcher.try_on_corpus(
                f'{set_dir}/!truth.txt', self.weighted_words, i / 100
            )
            prediction_file.seek(0)
            quality = QualityComputor.compute_on_memory_file(
                set_dir, prediction_file
            )
            if maxval[0] < quality:
                maxval = quality, i
            writer.print((round(quality, 2), i / 100))
            prediction_file.close()
        writer.print(f"Max value: {round(maxval[0],2)} {maxval[1]/100}")

        self.max_val = maxval[1] / 100

        self.weighted_words = WeightedWordDict(
            self.ok_counter, self.spam_counter, desired_freq_cutoff
        )

    def set_max_val(self, val):
        self.max_val = val

    def test(self, set_dir: str):
        file = open(f'{set_dir}/!prediction.txt', "w", encoding="utf-8")
        if not self.trained:
            for filen in [
                filename
                for filename in os.listdir(set_dir)
                if filename[0] != '!'
            ]:
                file.write(f"{filen} OK\n")
            file.close()
            return
        WordMatcher.test_on_corpus(
            f'{set_dir}',
            self.weighted_words,
            self.max_val,
        )
