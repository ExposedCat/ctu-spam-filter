import difflib
from helpers.file_reader import read_email_file
from helpers.words_parser import parse_words
from services.email_cleaner import clean_email
from services.word_evaluator import *
import os
import time


def evaluate_wordset(weighted_dict, wordset):
    value = 0
    amount_of_words = len([x for x in wordset if x in weighted_dict])
    for word in wordset:
        '''
        close_matches = difflib.get_close_matches(word, weidghtedict.keys())
        if (len(close_matches)):
            close_match_dict = {
                key: weidghtedict[key][0] for key in close_matches}
            preferred_match = max(close_match_dict, key=close_match_dict.get)
            value += (weidghtedict.get(preferred_match)[0])/amount_of_words 
            
            
        FUZZY MATCHING UNRELIABLE?
        '''
        value += (weighted_dict.get(word, (0,0))[0])/amount_of_words 
    return value


def debug_check_corpus(filename, weighted_dict, cutoff):
    classification = read_classification_from_file(filename)
    wordset = []
    with open(os.path.dirname(filename)+"/"+"!prediction.txt", "w") as file:
        for x in classification:
            wordset = parse_words(clean_email(
                read_email_file(os.path.dirname(filename)+"/"+x)))
            val = evaluate_wordset(weighted_dict, wordset)
            if val > cutoff:
                tag = "OK"
            else:
                tag = "SPAM"
            #print(
            #    f'File {x}\nValue :{evaluate_wordset(weidghtedict, wordset)}\nTRUTH : {classification.get(x)} PREDICT: {tag}\n')
            file.write(f"{x} {tag}\n")
