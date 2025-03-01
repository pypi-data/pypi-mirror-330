import numpy as np
from typing import List, Tuple, Optional, Callable, Union
from langchain_core.embeddings import Embeddings

def evaluate_topic_model(
    embedding_model: Embeddings,
    true_topics: List[Union[str, List[str]]],
    predicted_topics: List[Union[str, List[str]]],
    return_low_pairs: bool = False,
    enable_multi_label_matching: bool = True,
    similarity_threshold: float = 0.5,
    low_similarity_penalty: float = 1.0
) -> Tuple[float, Optional[List[Tuple[str, str, float, int]]]]:
    """
    Evaluates the alignment between true and predicted topics using embeddings.
    
    This function computes a score in the range [0, 1], where:
      - 1 indicates a perfect match.
      - 0 indicates a complete mismatch.
      
    The score is computed per position. For each paired position:
      - If the position contains a single topic, the score is the clamped cosine similarity
        between the true and predicted topic embeddings. However, if this similarity is below 
        the 'similarity_threshold', it is multiplied by 'low_similarity_penalty' (a value between 0 and 1)
        to penalize low-similarity pairs.
      - If the position contains multiple topics (i.e., multi-label, provided as a list of strings)
        and enable_multi_label_matching is True, a greedy matching strategy is used. For each matched
        pair, if its cosine similarity is below 'similarity_threshold', the similarity is reduced 
        (multiplied by 'low_similarity_penalty'); otherwise, it is used as is. Unpaired topics are assigned a score of 0.
      - If one side of the position is empty while the other is not, that position is scored as 0.
      
    If the number of positions differs between true_topics and predicted_topics, extra positions 
    are treated as complete mismatches (score = 0).
    
    Optionally, the function returns a list of low-similarity pairs (i.e. those with raw similarity 
    below the similarity_threshold) along with their position.
    
    Args:
        embedding_model: An embedding model with an `embed_query(topic: str) -> np.ndarray` method.
        true_topics: List of ground-truth topics; each element can be a string or a list of strings.
        predicted_topics: List of predicted topics; each element can be a string or a list of strings.
        return_low_pairs: If True, also return a list of pairs with raw similarity below similarity_threshold.
        enable_multi_label_matching: If True, use greedy matching for positions with multiple topics.
        similarity_threshold: Threshold below which a pair is considered low-similarity (for flagging and penalty).
        low_similarity_penalty: A factor (between 0 and 1) to penalize similarities below threshold 
                                (1 means no penalty; values closer to 0 reduce the effective similarity).
    
    Returns:
        A tuple:
          - Final score in [0, 1]. (1 means perfect matching; 0 means completely mismatched.)
          - Optionally, a list of low-similarity pairs in the form (true_topic, pred_topic, raw_similarity, position).
    """
    # --- Helper: Compute cosine similarity and clamp to [0,1] ---
    def cosine_similarity(t_embed: np.ndarray, p_embed: np.ndarray) -> float:
        sim = np.dot(t_embed, p_embed) / (np.linalg.norm(t_embed) * np.linalg.norm(p_embed) + 1e-8)
        return max(min(sim, 1.0), 0.0)
    
    # --- Input Normalization ---
    # Wrap any string element into a list so that every position is a list of topics.
    true_topics_norm = [[t] if isinstance(t, str) else t for t in true_topics]
    pred_topics_norm = [[p] if isinstance(p, str) else p for p in predicted_topics]
    
    n_true = len(true_topics_norm)
    n_pred = len(pred_topics_norm)
    min_positions = min(n_true, n_pred)
    extra_positions = abs(n_true - n_pred)
    
    total_score = 0.0
    low_sim_pairs = []  # To record pairs with raw similarity below similarity_threshold.
    embedding_cache = {}
    
    def get_embedding(topic: str) -> np.ndarray:
        if topic not in embedding_cache:
            embedding_cache[topic] = embedding_model.embed_query(topic)
        return embedding_cache[topic]
    
    # --- Greedy Matching for Multi-Label Positions ---
    def greedy_match(sim_matrix: np.ndarray, t_topics: List[str], p_topics: List[str], pos: int) -> float:
        sims = sim_matrix.copy()
        matched_indices = []  # list of (i, j) pairs for matched topics.
        t_used = set()
        p_used = set()
        score_sum = 0.0
        
        while True:
            if sims.size == 0:
                break
            i, j = np.unravel_index(sims.argmax(), sims.shape)
            if sims[i, j] <= 0:
                break
            matched_indices.append((i, j))
            t_used.add(i)
            p_used.add(j)
            raw_sim = sim_matrix[i, j]
            # Apply penalty if similarity is below the threshold.
            effective_sim = raw_sim * low_similarity_penalty if raw_sim < similarity_threshold else raw_sim
            score_sum += effective_sim
            # Mark the entire row and column as used.
            sims[i, :] = -1
            sims[:, j] = -1
        
        num_topics = max(len(t_topics), len(p_topics))
        for (i, j) in matched_indices:
            if sim_matrix[i, j] < similarity_threshold:
                low_sim_pairs.append((t_topics[i], p_topics[j], sim_matrix[i, j], pos))
        return score_sum / num_topics  # Normalize to [0,1].
    
    # --- Evaluate Each Paired Position ---
    for pos in range(min_positions):
        T_i = [t.strip() for t in true_topics_norm[pos] if isinstance(t, str) and t.strip()] \
              if all(isinstance(t, str) for t in true_topics_norm[pos]) else true_topics_norm[pos]
        P_i = [p.strip() for p in pred_topics_norm[pos] if isinstance(p, str) and p.strip()] \
              if all(isinstance(p, str) for p in pred_topics_norm[pos]) else pred_topics_norm[pos]
        
        if not T_i and not P_i:
            positional_score = 1.0
        elif not T_i or not P_i:
            positional_score = 0.0
        else:
            T_unique = list(set(T_i))
            P_unique = list(set(P_i))
            T_embeds = [get_embedding(t) for t in T_unique]
            P_embeds = [get_embedding(p) for p in P_unique]
            sim_matrix = np.array([[cosine_similarity(t_e, p_e) for p_e in P_embeds] for t_e in T_embeds])
            
            if enable_multi_label_matching and (len(T_unique) > 1 or len(P_unique) > 1):
                positional_score = greedy_match(sim_matrix, T_unique, P_unique, pos)
            else:
                raw_sim = sim_matrix[0, 0]
                effective_sim = raw_sim * low_similarity_penalty if raw_sim < similarity_threshold else raw_sim
                positional_score = effective_sim
                if raw_sim < similarity_threshold:
                    low_sim_pairs.append((T_unique[0], P_unique[0], raw_sim, pos))
        total_score += positional_score
    
    total_positions = max(n_true, n_pred)
    final_score = (total_score + 0 * extra_positions) / total_positions
    final_score = max(min(final_score, 1.0), 0.0)
    
    return (final_score, low_sim_pairs) if return_low_pairs else (final_score, None)
