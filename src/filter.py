from helpers.file_reader import read_email_file
from helpers.words_parser import parse_words
from services.email_cleaner import clean_email
from services.word_evaluator import *
from services.word_matcher import *
from eval.quality import compute_quality_for_corpus

dir= "../test/first/"

okset = generate_wordset_from_tagged_email_set(
    dir+"!truth.txt", "OK")
spamset = generate_wordset_from_tagged_email_set(
    dir+"!truth.txt", "SPAM")

okcount = wordset_to_countdict(okset)
spamcount = wordset_to_countdict(spamset)

wwd = weighted_word_dict(okcount, spamcount, 100)
reweigh_weighted_word_dict(wwd)

maxval = (0, 0)
for i in range(-40, 0):
    debug_check_corpus(dir+"!truth.txt", wwd, i/100)
    q = compute_quality_for_corpus(dir)
    if maxval[0] < q:
        maxval = q, i
    print(round(q, 2), i/100)
print(f"winner: {round(maxval[0],2)} {maxval[1]/100}")

wwd = weighted_word_dict(okcount, spamcount, 5)
reweigh_weighted_word_dict(wwd)
debug_check_corpus(dir+"!truth.txt", wwd, maxval[1]/100)
print(compute_quality_for_corpus(dir))