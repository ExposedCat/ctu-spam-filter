from filter import MyFilter
from evaluation.quality import QualityComputor
from helpers.writer import Writer


writer = Writer("Test")
writer.print("Creating filter")
spam_filter = MyFilter()
writer.print("Training filter")
spam_filter.train("../test/first", (-60, -30), 1, 150, logs=True)
writer.print("Testing filter")
spam_filter.test("../test/second")
writer.print("Computing filter quality")
quality = QualityComputor.compute("../test/second")
writer.print(f'Filter predicted {round(quality, 4) * 100}% emails correctly')
