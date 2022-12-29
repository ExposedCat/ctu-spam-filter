def read_classification_from_file(filename):
    with open(filename, "rt", encoding="utf-8") as f:
        dictionary = dict()
        for line in f:
            dictionary[line.split()[0]] = line.split()[1]
        return dictionary
    return dict()
