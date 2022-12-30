class BinaryConfusionMatrix:
    def __init__(self, pos_tag, neg_tag):
        self.pos_tag = pos_tag
        self.neg_tag = neg_tag
        self.stats = {'tp': 0, 'tn': 0, 'fp': 0, 'fn': 0}

    def as_dict(self) -> dict:
        return self.stats

    def update(self, truth, prediction) -> None:
        tags = [self.pos_tag, self.neg_tag]
        if not (truth in tags or prediction in tags):
            raise ValueError(
                '`truth` or `prediction` argument differs from both specified tags'
            )
        result = 't' if truth == prediction else 'f'
        field = 'p' if truth == self.pos_tag else 'n'
        self.stats[result + field] += 1

    def compute_from_dicts(self, truth_dict: dict, pred_dict: dict):
        for keyname in pred_dict:
            self.update(truth_dict[keyname], pred_dict[keyname])