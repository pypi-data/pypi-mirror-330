from sklearn.metrics import precision_recall_fscore_support


def calculate_metrics(y_true, y_pred):
    precision, recall, fbeta_score, support = precision_recall_fscore_support(y_true, y_pred)
    return precision, recall, fbeta_score, support
