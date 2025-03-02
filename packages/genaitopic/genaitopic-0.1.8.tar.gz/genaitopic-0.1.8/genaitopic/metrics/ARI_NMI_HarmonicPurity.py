import pandas as pd
import numpy as np
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score
from sklearn.metrics.cluster import contingency_matrix

def compute_harmonic_purity(y_true, y_pred):
    """
    Compute Harmonic Purity as the harmonic mean of per-class recalls.

    For each true class, recall is defined as the fraction of samples in the most
    frequent predicted cluster over the total samples in that class. If any recall
    is zero, the overall score is 0.

    Parameters:
        y_true (array-like): True topic labels.
        y_pred (array-like): Predicted topic labels.

    Returns:
        float: Harmonic Purity score.

    Example:
        >>> compute_harmonic_purity([0, 0, 1, 1], [1, 1, 1, 0])
        0.6666666666666666
    """
    cont = contingency_matrix(y_true, y_pred)
    recalls = []
    for row in cont:
        total = row.sum()
        if total == 0:
            continue
        recall = row.max() / total
        recalls.append(recall)
    if not recalls or min(recalls) == 0:
        return 0.0
    harmonic = len(recalls) / sum(1 / r for r in recalls)
    return harmonic

def evaluate_topic_model(df, y_true_col, y_pred_col):
    """
    Evaluate topic modeling performance using Adjusted Rand Index (ARI), Normalized 
    Mutual Information (NMI), and Harmonic Purity.

    Extracts true and predicted topic labels from a DataFrame and computes:
      - ARI: Similarity measure between true and predicted labels.
      - NMI: Mutual information normalized to [0, 1].
      - Harmonic Purity: Harmonic mean of per-class recalls.

    Parameters:
        df (pandas.DataFrame): DataFrame containing topic modeling results.
        y_true_col (str): Column name for ground truth topics.
        y_pred_col (str): Column name for predicted topics.

    Returns:
        dict: Dictionary with keys "ARI", "NMI", and "Harmonic Purity".

    Example:
        >>> a = {'true_label': [0, 0, 1, 1], 'pred_label': [1, 1, 1, 0]}
        >>> b = pd.DataFrame(a)
        >>> evaluate_topic_model(b, 'true_label', 'pred_label')
        {'ARI': 0.0, 'NMI': 0.343, 'Harmonic Purity': 0.6666666666666666}
    """
    y_true = df[y_true_col].values
    y_pred = df[y_pred_col].values

    ari = adjusted_rand_score(y_true, y_pred)
    nmi = normalized_mutual_info_score(y_true, y_pred)
    hp = compute_harmonic_purity(y_true, y_pred)
    
    return {
        "ARI": ari,
        "NMI": nmi,
        "Harmonic Purity": hp
    }
