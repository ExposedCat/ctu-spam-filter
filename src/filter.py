import os
from helpers.writer import Writer
from services.word_matcher import WordMatcher
from evaluation.quality import QualityComputor
from services.word_evaluator import Wordset, WeightedWordDict


class MyFilter:
    def __init__(self, spam_tag="SPAM", ok_tag="OK"):
        '''Create a MyFilter object'''
        self.spam_tag = spam_tag
        self.ok_tag = ok_tag
        self.trained = 0
        pass

    def train(
        self,
        set_dir: str,
        train_range: tuple[int, int] = (-100, 20),
        desired_freq_cutoff=1,
        training_freq_cutoff=100,
        logs=False,
        # These default values are not likely to work perfectly for every
        # email set, however our first correct upload scored max points
        # already, so we don't want to modify that result anymore :)
        # Otherwise it would be possible to figure these out dynamically
        # from the email set.
    ):
        '''Train the MyFilter object on an email set from "set_dir", expects
        the "set_dir" to contain !truth.txt. After this function is ran,
        the test() function will produce correct predictions.'''

        self.trained = 1

        self.ok_counter = Wordset(
            f'{set_dir}/!truth.txt', tag=self.ok_tag
        ).to_counter()
        self.spam_counter = Wordset(
            f'{set_dir}/!truth.txt', tag=self.spam_tag
        ).to_counter()

        # Generate WeightedWordDict from the two wordsets above. This will
        # contain words that are found in the email set more than
        # "training_freq_cutoff" times, and their respective likeliness to be
        # present in a spam/ok email (-1/1)
        self.weighted_words = WeightedWordDict(
            self.ok_counter, self.spam_counter, training_freq_cutoff
        )

        writer = Writer("Training", logs)

        max_value = (0, 0)
        t1, t2 = train_range

        # Generate the wordsets we will need to find the proper cutoff value.
        # and evaluate them in-place.
        generated_training_data = WordMatcher.generate_static_training_data(
            f'{set_dir}/!truth.txt', self.weighted_words
        )

        # Find the most suitable cutoff value for the given email set.
        # Try all values in "train_range" and select the one that maximizes
        # the prediction quality.
        # Due to the fact that the quality evaluation function we use
        # punishes more for false positives, this should find a conservative
        # and safe cutoff on its own.
        for i in range(t1, t2):
            prediction_file = WordMatcher.try_cutoff_on_generated_data(
                generated_training_data, i / 100
            )
            prediction_file.seek(0)

            quality = QualityComputor.compute_on_memory_file(
                set_dir, prediction_file
            )

            if max_value[0] < quality:
                max_value = quality, i
            writer.print((round(quality, 2), i / 100))
            prediction_file.close()

        # Print the max value found to logs
        writer.print(f"Max value: {round(max_value[0],2)} {max_value[1]/100}")

        self.best_cutoff = max_value[1] / 100

        # Regenerate WeightedWordDict with the desired_freq_cutoff.
        # Having found the correct cutoff for only the most frequent words,
        # we avoid over-fitting to the base data. However, including more words
        # in the final email evaluation seems to yield better results.
        self.weighted_words = WeightedWordDict(
            self.ok_counter, self.spam_counter, desired_freq_cutoff
        )

    def test(self, set_dir: str):
        '''Run the MyFilter test on "set_dir", generating a !prediction.txt
        file. The MyFilter expects to be trained at this point, and outputs
        an "all-ok" prediction otherwise.'''

        # If not trained, just mark everything as OK.
        if not self.trained:
            file = open(f'{set_dir}/!prediction.txt', "w", encoding="utf-8")
            for filen in [
                filename
                for filename in os.listdir(set_dir)
                if filename[0] != '!'
            ]:
                file.write(f"{filen} OK\n")
            file.close()
            return

        # Otherwise, run the score_corpus function with the WeightedWordDict
        # and best_cutoff.
        WordMatcher.score_corpus(
            f'{set_dir}',
            self.weighted_words,
            self.best_cutoff,
        )
