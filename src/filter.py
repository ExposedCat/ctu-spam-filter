from helpers.file_reader import read_email_file
from helpers.words_parser import parse_words
from services.email_cleaner import clean_email

email = read_email_file('test/first/0001.bfc8d64d12b325ff385cca8d07b84288')

cleared = clean_email(email['body'])
words = parse_words(cleared)
print(words)
