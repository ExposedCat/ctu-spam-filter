from helpers.file_reader import read_email_file
from helpers.words_parser import parse_words
from services.email_cleaner import clean_email
from services.word_evaluator import *
import os


def read_classification_from_file(filename):
    with open(filename, "rt", encoding="utf-8") as f:
        dictionary = dict()
        for line in f:
            dictionary[line.split()[0]] = line.split()[1]
        return dictionary
    return dict()


def generate_wordset_from_tagged_email_set(filename, tag):
    classification = read_classification_from_file(filename)
    wordset = []
    for x in classification:
        if classification.get(x) == tag:
            wordset += parse_words(clean_email(
                read_email_file(os.path.dirname(filename)+"/"+x)))
    return wordset


def wordset_to_countdict(wordset):
    counter = {}
    for word in wordset:
        counter[word] = counter.get(word, 0) + 1
    return counter


def weighted_word_dict(firstdict, seconddict, frequency_cutoff=0):
    counter = {}
    for word in dict(firstdict, **seconddict):
        if (frequency_cutoff == 0 or firstdict.get(word, 0) + seconddict.get(word, 0) > frequency_cutoff):
            counter[word] = round((firstdict.get(word, 0) - seconddict.get(word, 0)) /
                                  (firstdict.get(word, 0) + seconddict.get(word, 0)), 2), firstdict.get(word, 0) + seconddict.get(word, 0)
    return counter

def reweigh_weighted_word_dict(weidghtedict):
    for word in weidghtedict:
        temp_dict = {key: weidghtedict[key][1] for key in weidghtedict}
        max_freq_key = max(temp_dict, key=temp_dict.get)
        weidghtedict[word] = (weidghtedict[word][0], temp_dict[word]/temp_dict[max_freq_key])