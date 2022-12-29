import eval.utils
import eval.confmat
import eval.corpus

def quality_score(tp, tn, fp, fn):
    return (tp+tn)/(tp+tn+fp*10+fn)

def compute_quality_for_corpus(corpus_dir):
    truth = eval.utils.read_classification_from_file(corpus_dir+'/!truth.txt')
    predc = eval.utils.read_classification_from_file(corpus_dir+'/!prediction.txt')
    matrix = eval.confmat.BinaryConfusionMatrix("SPAM", "OK")
    matrix.compute_from_dicts(truth, predc)
    return quality_score(matrix.TP, matrix.TN, matrix.FP, matrix.FN) 