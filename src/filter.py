from helpers.file_reader import read_email_file
from helpers.words_parser import parse_words
from services.email_cleaner import clean_email
from services.word_evaluator import *


okset = generate_wordset_from_tagged_email_set(
    "../test/first/!truth.txt", "OK")
spamset = generate_wordset_from_tagged_email_set(
    "../test/first/!truth.txt", "SPAM")

okcount = wordset_to_countdict(okset)
spamcount = wordset_to_countdict(spamset)

print(weighted_word_dict(okcount, spamcount, 50))