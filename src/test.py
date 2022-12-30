from filter import MyFilter
from evaluation.quality import QualityComputor


spam_filter = MyFilter()
#spam_filter.train("../test/first", (-60, -30), 1, 150, logs = True)
spam_filter.test("../test/second", logs=True)
print(f"{QualityComputor.compute('../test/second')}")
