class BinaryConfusionMatrix:
    def __init__(self, pos_tag, neg_tag):
        self.pos_tag = pos_tag
        self.neg_tag = neg_tag
        self.TP = 0
        self.TN = 0
        self.FP = 0
        self.FN = 0

    def as_dict(self):
        return {'tp': self.TP, 'tn': self.TN, 'fp': self.FP, 'fn': self.FN}

    def update(self, truth, prediction):
        if truth not in (self.pos_tag, self.neg_tag):
            raise ValueError
        if prediction not in (self.pos_tag, self.neg_tag):
            raise ValueError
        self.TP += truth == prediction == self.pos_tag
        self.TN += truth == prediction == self.neg_tag
        self.FN += truth != prediction and truth == self.pos_tag
        self.FP += truth != prediction and truth == self.neg_tag
    
    def compute_from_dicts(self, truth_dict, pred_dict):
        for email in pred_dict:
            self.update(truth_dict[email], pred_dict[email])