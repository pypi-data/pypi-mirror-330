import os
import json
import h5py
import pandas as pd
import numpy as np
from flask import Blueprint, jsonify, request
from sklearn.neighbors import NearestNeighbors

from latentscope.models import get_embedding_model
from latentsae.sae import Sae

# Create a Blueprint
search_bp = Blueprint('search_bp', __name__)
DATA_DIR = os.getenv('LATENT_SCOPE_DATA')

# in memory cache of dataset metadata, embeddings, models and tokenizers
DATASETS = {}
DBS = {}
EMBEDDINGS = {}
FEATURES = {}
DATAFRAMES = {}

"""
Returns nearest neighbors for a given query string
Hard coded to 150 results currently
"""
@search_bp.route('/nn', methods=['GET'])
def nn():
    dataset = request.args.get('dataset')
    scope_id = request.args.get('scope_id')
    embedding_id = request.args.get('embedding_id')
    dimensions = request.args.get('dimensions')
    dimensions = int(dimensions) if dimensions else None
    # return_embeddings = True if request.args.get('return_embeddings') else False
    print("dimensions", dimensions)
    # Check if this scope has a LanceDB index
    query = request.args.get('query')
    print("query", query)      

    if embedding_id not in EMBEDDINGS:
        print("loading model", embedding_id)
        with open(os.path.join(DATA_DIR, dataset, "embeddings", embedding_id + ".json"), 'r') as f:
            metadata = json.load(f)
        model_id = metadata.get('model_id')
        print("Model ID:", model_id)
        model = get_embedding_model(model_id)
        model.load_model()
        EMBEDDINGS[dataset + "-" + embedding_id] = model
    else:
        model = EMBEDDINGS[dataset + "-" + embedding_id]

    # If lancedb is available, we use it to search
    if scope_id is not None:
        lance_path = os.path.join(DATA_DIR, dataset, "lancedb", scope_id + ".lance")
        if os.path.exists(lance_path):
            print(f"Found LanceDB index at {lance_path}, using vector search")
            return nn_lance(dataset, scope_id, model, query, dimensions)

    # Otherwise we use the nearest neighbors search from sklearn
    num = 150
    if dataset not in DATASETS or embedding_id not in DATASETS[dataset]:
        # load the dataset embeddings
        # embeddings = np.load(os.path.join(DATA_DIR, dataset, "embeddings", embedding_id + ".npy"))
        embedding_path = os.path.join(DATA_DIR, dataset, "embeddings", f"{embedding_id}.h5")
        with h5py.File(embedding_path, 'r') as f:
            embeddings = np.array(f["embeddings"])
        print("fitting embeddings")
        nne = NearestNeighbors(n_neighbors=num, metric="cosine")
        nne.fit(embeddings)
        if dataset not in DATASETS:
          DATASETS[dataset] = {}
        DATASETS[dataset][embedding_id] = nne
    else:
        nne = DATASETS[dataset][embedding_id]
    
    # embed the query string and find the nearest neighbor

    embedding = np.array(model.embed([query], dimensions=dimensions))
    distances, indices = nne.kneighbors(embedding)
    filtered_indices = indices[0]
    filtered_distances = distances[0]
    indices = filtered_indices
    distances = filtered_distances
    return jsonify(indices=indices.tolist(), distances=distances.tolist(), search_embedding=embedding.tolist())


def nn_lance(dataset, scope_id, model, query, dimensions):
    import lancedb
    db = lancedb.connect(os.path.join(DATA_DIR, dataset, "lancedb"))
    table = db.open_table(scope_id)
    embedding = model.embed([query], dimensions=dimensions)
    results = table.search(embedding).metric("cosine").select(["index"]).limit(100).to_list()
    indices = [result["index"] for result in results]
    distances = [result["_distance"] for result in results]
    return jsonify(indices=indices, distances=distances, search_embedding=embedding)

"""
Summarize features for a given set of dataset indices.
Summary includes
- top mean: average the features for all the indices and return the top N
- get the top feature for each index, count the number of times each feature is the top feature
input: [index1, index2, ...]

output: {

}
"""
@search_bp.route('/feature_summary', methods=['POST'])
def feature_summary():
    dataset = request.args.get('dataset')
    feature_id = request.args.get('feature_id')

"""
Get top row indices for a given feature
"""
@search_bp.route('/feature', methods=['GET'])
def feature():
    dataset = request.args.get('dataset')
    sae_id = request.args.get('sae_id')
    feature_id = request.args.get('feature_id')
    threshold = request.args.get('threshold')
    # Convert threshold to float if it exists
    threshold = float(threshold) if threshold is not None else 0.1

    top_n = request.args.get('top_n')
    if top_n is not None:
        top_n = int(top_n)
    if top_n is None:
        top_n = 100

    # load the saved features
    sae_path = os.path.join(DATA_DIR, dataset, "saes", f"{sae_id}.h5")
    with h5py.File(sae_path, 'r') as f:
        all_top_indices = np.array(f["top_indices"])
        all_top_acts = np.array(f["top_acts"])

    # Get max activation per row for the specific feature
    feature_activations = np.zeros(len(all_top_indices))
    for row_idx, (indices, acts) in enumerate(zip(all_top_indices, all_top_acts)):
        feature_mask = indices == int(feature_id)
        if np.any(feature_mask):
            feature_activations[row_idx] = np.max(acts[feature_mask])
        else:
            feature_activations[row_idx] = 0

    # Only get indices where there are non-zero activations
    non_zero_mask = feature_activations > 0
    if not np.any(non_zero_mask):
        return jsonify(top_row_indices=[])  # Return empty list if no activations

    # Filter by threshold and non-zero activations
    above_threshold_mask = feature_activations > threshold
    if not np.any(above_threshold_mask):
        return jsonify(top_row_indices=[])  # Return empty list if no activations above threshold

    # Get the indices of top_n highest activations from filtered activations
    top_row_indices = np.argsort(feature_activations[above_threshold_mask])[::-1]
    # if top_n:
    #     top_row_indices = top_row_indices[:top_n]
    actual_indices = np.where(above_threshold_mask)[0][top_row_indices]
    
    
    return jsonify(top_row_indices=actual_indices.tolist())

"""
Returns features for a given query string.
This will first embed the string and then use the SAE to get the topk features of the embedding.
"""
@search_bp.route('/features', methods=['GET'])
def features():
    dataset = request.args.get('dataset')
    embedding_id = request.args.get('embedding_id')
    dimensions = request.args.get('dimensions')
    dimensions = int(dimensions) if dimensions else None
    # return_embeddings = True if request.args.get('return_embeddings') else False
    print("dimensions", dimensions)

    num = 150
    if embedding_id not in EMBEDDINGS:
        print("loading model", embedding_id)
        with open(os.path.join(DATA_DIR, dataset, "embeddings", embedding_id + ".json"), 'r') as f:
            metadata = json.load(f)
        model_id = metadata.get('model_id')
        print("Model ID:", model_id)
        model = get_embedding_model(model_id)
        model.load_model()
        EMBEDDINGS[embedding_id] = model
    else:
        model = EMBEDDINGS[embedding_id]

    if dataset not in DATASETS or embedding_id not in DATASETS[dataset]:
        # load the dataset embeddings
        # embeddings = np.load(os.path.join(DATA_DIR, dataset, "embeddings", embedding_id + ".npy"))
        embedding_path = os.path.join(DATA_DIR, dataset, "embeddings", f"{embedding_id}.h5")
        with h5py.File(embedding_path, 'r') as f:
            embeddings = np.array(f["embeddings"])
        print("fitting embeddings")
        nne = NearestNeighbors(n_neighbors=num, metric="cosine")
        nne.fit(embeddings)
        if dataset not in DATASETS:
          DATASETS[dataset] = {}
        DATASETS[dataset][embedding_id] = nne
    else:
        nne = DATASETS[dataset][embedding_id]
    
    # embed the query string and find the nearest neighbor
    query = request.args.get('query')
    print("query", query)
    embedding = np.array(model.embed([query], dimensions=dimensions))
    distances, indices = nne.kneighbors(embedding)
    filtered_indices = indices[0]
    filtered_distances = distances[0]
    indices = filtered_indices
    distances = filtered_distances
    return jsonify(indices=indices.tolist(), distances=distances.tolist(), search_embedding=embedding.tolist())


@search_bp.route('/compare', methods=['GET'])
def compare():
    dataset = request.args.get('dataset')
    umap_left = request.args.get('umap_left')
    umap_right = request.args.get('umap_right')
    k = request.args.get('k')
    k = int(k) if k else 5

    umap_dir = os.path.join(DATA_DIR, dataset, "umaps")
    left_df = pd.read_parquet(os.path.join(umap_dir, f"{umap_left}.parquet"))
    left = left_df.to_numpy()
    right_df = pd.read_parquet(os.path.join(umap_dir, f"{umap_right}.parquet"))
    right = right_df.to_numpy()

    # Calculate the absolute displacement
    absolute_displacement = np.linalg.norm(right - left, axis=1)
    min_abs_displacement = np.min(absolute_displacement)
    max_abs_displacement = np.max(absolute_displacement)
    if max_abs_displacement - min_abs_displacement > 0:
        absolute_displacement = (absolute_displacement - min_abs_displacement) / (max_abs_displacement - min_abs_displacement)
    else:
        absolute_displacement = np.zeros_like(absolute_displacement)


    # Compute nearest neighbors in both projections
    # knn = NearestNeighbors(n_neighbors=k+1, metric="euclidean")  # +1 because the point itself is included
    # knn.fit(left)
    # distances1, indices1 = knn.kneighbors(left)

    # knn.fit(right)
    # distances2, indices2 = knn.kneighbors(right)

    # relative_displacement = np.abs(distances1 - distances2).mean(axis=1)
    # # Normalize relative_displacement
    # min_relative_displacement = np.min(relative_displacement)
    # max_relative_displacement = np.max(relative_displacement)
    # if max_relative_displacement - min_relative_displacement > 0:
    #     relative_displacement = (relative_displacement - min_relative_displacement) / (max_relative_displacement - min_relative_displacement)
    # else:
    #     relative_displacement = np.zeros_like(relative_displacement)

    
    # size = left.shape[0]
    # # Calculate displacement scores
    # displacement_scores = np.zeros(size)
    # for i in range(size):
    #     # Find the actual positions (0 to k-1) of common neighbors in each list
    #     neighbor_positions_1 = {index: pos for pos, index in enumerate(indices1[i]) if index in indices2[i]}
    #     neighbor_positions_2 = {index: pos for pos, index in enumerate(indices2[i]) if index in indices1[i]}
        
    #     # Calculate displacement for common neighbors
    #     displacements = []
    #     for index, pos1 in neighbor_positions_1.items():
    #         pos2 = neighbor_positions_2[index]
    #         displacement = abs(distances1[i, pos1] - distances2[i, pos2])
    #         displacements.append(displacement)
        
    #     # Compute the mean displacement for the point, if there are common neighbors
    #     if displacements:
    #         displacement_scores[i] = np.mean(displacements)

    # # normalize displacement_scores from 0 to 1
    # min_score = np.min(displacement_scores)
    # max_score = np.max(displacement_scores)
    # if max_score - min_score > 0:
    #     displacement_scores = (displacement_scores - min_score) / (max_score - min_score)
    # else:
    #     displacement_scores = np.zeros_like(displacement_scores)

    # TODO: why don't these actually add up to 1 even when i normalize each
    # combined_scores = 0.6 * absolute_displacement + 0.6 * relative_displacement + 0.6 * displacement_scores
    # combined_scores = (absolute_displacement + relative_displacement + displacement_scores) / 3
    combined_scores = absolute_displacement #(absolute_displacement + relative_displacement + displacement_scores) / 3
    return jsonify(combined_scores.tolist())
    # return jsonify(displacement_scores.tolist())


