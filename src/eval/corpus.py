import os

class Corpus:
     def __init__(self,filename):
        self.path = filename
        self.filenames = [x for x in os.listdir(self.path) if x[0] != '!']

     def emails(self):
        for x in self.filenames:
            with open(self.path+'/'+x, "r", encoding='utf-8') as f:
                yield x, f.read()
