from evaluation.utils import EvaluationUtils
from evaluation.confmat import BinaryConfusionMatrix


class QualityComputor:
    @staticmethod
    def quality_score(tp, tn, fp, fn):
        return (tp + tn) / (tp + tn + fp * 10 + fn)

    @staticmethod
    def compute(corpus_dir: str):
        truth = EvaluationUtils.read_classification_from_file(
            f'{corpus_dir}/!truth.txt'
        )
        prediction = EvaluationUtils.read_classification_from_file(
            f'{corpus_dir}/!prediction.txt'
        )
        confmat = BinaryConfusionMatrix(pos_tag='OK', neg_tag='SPAM')
        confmat.compute_from_dicts(truth, prediction)
        return QualityComputor.quality_score(**confmat.as_dict())
