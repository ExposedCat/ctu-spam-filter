import os
from helpers.file_reader import FileReader


class Corpus:
    def __init__(self, filename):
        self.path = filename

    def emails(self):
        filenames = [
            filename
            for filename in os.listdir(self.path)
            if filename[0] != '!'
        ]
        for filename in filenames:
            email = FileReader.read_text(f'{self.path}/{filename}')
            yield filename, email
