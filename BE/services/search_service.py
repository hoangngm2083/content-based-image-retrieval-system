import numpy as np
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity, chi2_kernel
from typing import List, Tuple, Dict, Any

from services.feature_extractor_service import extract_color_layout, extract_vgg_feature
from services.database_service import get_all_features


def hybrid_similarity(
    query_color: np.ndarray,
    query_vgg: np.ndarray,
    db_features: Dict[str, np.ndarray],
    weights: Tuple[float, float] = (0.4, 0.6)
) -> np.ndarray:
    """
    Compute weighted similarity scores combining MPEG-7 color layout and VGG16 features.

    Args:
        query_color (np.ndarray): Query image color layout feature vector.
        query_vgg (np.ndarray): Query image VGG16 feature vector.
        db_features (Dict[str, np.ndarray]): Database features with keys "color" and "vgg".
        weights (Tuple[float, float]): Weights for color and VGG similarities (default (0.4, 0.6)).

    Returns:
        np.ndarray: Combined similarity scores for each DB record.
    """

    # Normalize features
    query_vgg_norm = normalize(query_vgg.reshape(1, -1))
    db_vgg_norm = normalize(db_features["vgg"])

    # Compute similarities
    color_sim = chi2_kernel(query_color.reshape(1, -1), db_features["color"]).flatten()
    vgg_sim = cosine_similarity(query_vgg_norm, db_vgg_norm).flatten()

    # Weighted combination
    combined_scores = weights[0] * color_sim + weights[1] * vgg_sim
    return combined_scores


def search_hybrid(query_path: str, top_k: int = 10) -> List[Any]:
    """
    Search top-k similar images from database using hybrid similarity.

    Args:
        query_path (str): Path to query image.
        top_k (int): Number of top results to return.

    Returns:
        List[Any]: List of record IDs for top-k similar images.
    """
    # Extract features for query image
    query_color = extract_color_layout(query_path)
    query_vgg = extract_vgg_feature(query_path)

    # Load all features from DB
    records = get_all_features()
    if not records:
        return []



    # Prepare DB features as numpy arrays
    db_ids = [r[0] for r in records]
    db_paths = [r[1] for r in records]
    db_colors = np.array([r[2] for r in records])
    db_vggs = np.array([r[3] for r in records])

    db_features = {
        "color": db_colors,
        "vgg": db_vggs
    }
    # Calculate similarity scores
    scores = hybrid_similarity(query_color, query_vgg, db_features)
    
    # Get indices of top-k scores (descending)
    top_indices = np.argsort(scores)[-top_k:][::-1]

  

    # Return IDs corresponding to top indices
    return [{"id": db_ids[i], "img": db_paths[i]} for i in top_indices]

