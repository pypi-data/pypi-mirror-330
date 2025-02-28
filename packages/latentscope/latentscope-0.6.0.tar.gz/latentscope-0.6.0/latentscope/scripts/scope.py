import os
import re
import json
import argparse
from datetime import datetime
from latentscope.util import get_data_dir
from latentscope import __version__


def main():
    parser = argparse.ArgumentParser(description='Setup a scope')
    parser.add_argument('dataset_id', type=str, help='Dataset id (directory name in data folder)')
    parser.add_argument('embedding_id', type=str, help='Embedding id')
    parser.add_argument('umap_id', type=str, help='UMAP id')
    parser.add_argument('cluster_id', type=str, help='Cluster id')
    parser.add_argument('cluster_labels_id', type=str, help='Cluster labels id')
    parser.add_argument('label', type=str, help='Label for the scope')
    parser.add_argument('description', type=str, help='Description of the scope')
    parser.add_argument('--scope_id', type=str, help='Scope id to overwrite existing scope', default=None)
    parser.add_argument('--sae_id', type=str, help='SAE id', default=None)

    args = parser.parse_args()
    scope(**vars(args))



def export_lance(directory, dataset, scope_id, metric="cosine", partitions=256):
    import lancedb
    import pandas as pd
    import h5py
    import numpy as np

    dataset_path = os.path.join(directory, dataset)
    print(f"Exporting scope {scope_id} to LanceDB database in {dataset_path}")
    
    # Validate directory
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory")
        return
    
    # Load the scope
    scope_path = os.path.join(dataset_path, "scopes")

    print(f"Loading scope from {scope_path}")
    scope_df = pd.read_parquet(os.path.join(scope_path, f"{scope_id}-input.parquet"))
    scope_meta = json.load(open(os.path.join(scope_path, f"{scope_id}.json")))

    print(f"Loading embeddings from {dataset_path}/embeddings/{scope_meta['embedding_id']}.h5")
    embeddings = h5py.File(os.path.join(dataset_path, "embeddings", f"{scope_meta['embedding_id']}.h5"), "r")

    db_uri = os.path.join(dataset_path, "lancedb")
    db = lancedb.connect(db_uri)

    print(f"Converting embeddings to numpy arrays", embeddings['embeddings'].shape)
    scope_df["vector"] = [np.array(row) for row in embeddings['embeddings']]

    if "sae_id" in scope_meta and scope_meta["sae_id"]:
        print(f"SAE scope detected, adding metadata")
        # read in the sae indices
        sae_path = os.path.join(dataset_path, "saes", f"{scope_meta['sae_id']}.h5")
        with h5py.File(sae_path, 'r') as f:
            all_top_indices = np.array(f["top_indices"])
            all_top_acts = np.array(f["top_acts"])

        # scope_df["sae_indices"] = all_top_indices
        # scope_df["sae_acts"] = all_top_acts
        scope_df["sae_indices"] = [row.tolist() for row in all_top_indices]
        scope_df["sae_acts"] = [row.tolist() for row in all_top_acts]

    table_name = scope_id

    # Check if the table already exists
    if scope_id in db.table_names():
        # Remove the existing table and its index
        db.drop_table(table_name)
        print(f"Existing table '{table_name}' has been removed.")

    print(f"Creating table '{table_name}'")
    tbl = db.create_table(table_name, scope_df)

    print(f"Creating ANN index for embeddings on table '{table_name}'")
    dim = embeddings['embeddings'].shape[1]
    sub_vectors = dim // 16
    print(f"Partitioning into {partitions} partitions, {sub_vectors} sub-vectors")
    tbl.create_index(num_partitions=partitions, num_sub_vectors=sub_vectors, metric=metric)

    print(f"Creating index for cluster on table '{table_name}'")
    tbl.create_scalar_index("cluster", index_type="BTREE")

    if "sae_id" in scope_meta and scope_meta["sae_id"]:
        print(f"Creating index for sae_indices on table '{table_name}'")
        tbl.create_scalar_index("sae_indices", index_type="LABEL_LIST")


    print(f"Table '{table_name}' created successfully")  

def scope(dataset_id, embedding_id, umap_id, cluster_id, cluster_labels_id, label, description, scope_id=None, sae_id=None):
    DATA_DIR = get_data_dir()
    print("DATA DIR", DATA_DIR)
    directory = os.path.join(DATA_DIR, dataset_id, "scopes")

    def get_next_scopes_number(dataset):
        # figure out the latest scope number
        scopes_files = [f for f in os.listdir(directory) if re.match(r"scopes-\d+\.json", f)]
        if len(scopes_files) > 0:
            last_scopes = sorted(scopes_files)[-1]
            last_scopes_number = int(last_scopes.split("-")[1].split(".")[0])
            next_scopes_number = last_scopes_number + 1
        else:
            next_scopes_number = 1
        return next_scopes_number

    next_scopes_number = get_next_scopes_number(dataset_id)
    # make the umap name from the number, zero padded to 3 digits
    if not scope_id:
        id = f"scopes-{next_scopes_number:03d}"
    else:
        id = scope_id

    print("RUNNING:", id)

    import pandas as pd

    scope = {
        "ls_version": __version__,
        "id": id,
        "embedding_id": embedding_id,
        "umap_id": umap_id,
        "cluster_id": cluster_id,
        "cluster_labels_id": cluster_labels_id,
        "label": label,
        "description": description
    }
    if(sae_id):
        scope["sae_id"] = sae_id

    # read each json file and add its contents to the scope file
    dataset_file = os.path.join(DATA_DIR, dataset_id, "meta.json")
    with open(dataset_file) as f:
        dataset = json.load(f)
        scope["dataset"] = dataset

    embedding_file = os.path.join(DATA_DIR, dataset_id, "embeddings", embedding_id + ".json")
    with open(embedding_file) as f:
        embedding = json.load(f)
        # Remove min_values and max_values from embedding data
        embedding.pop('min_values', None)
        embedding.pop('max_values', None)
        scope["embedding"] = embedding

    if sae_id:
        sae_file = os.path.join(DATA_DIR, dataset_id, "saes", sae_id + ".json")
        with open(sae_file) as f:
            sae = json.load(f)
            scope["sae"] = sae

    umap_file = os.path.join(DATA_DIR, dataset_id, "umaps", umap_id + ".json")
    with open(umap_file) as f:
        umap = json.load(f)
        scope["umap"] = umap
    
    cluster_file = os.path.join(DATA_DIR, dataset_id, "clusters", cluster_id + ".json")
    with open(cluster_file) as f:
        cluster = json.load(f)
        scope["cluster"] = cluster
    
    if cluster_labels_id == "default":
        cluster_labels_id = cluster_id + "-labels-default"
        scope["cluster_labels"] = {"id": cluster_labels_id, "cluster_id": cluster_id}
    else:
        cluster_labels_file = os.path.join(DATA_DIR, dataset_id, "clusters", cluster_labels_id + ".json")
        with open(cluster_labels_file) as f:
            cluster_labels = json.load(f)
            scope["cluster_labels"] = cluster_labels

    # load the actual labels and save everything but the indices in a dict
    cluster_labels_df = pd.read_parquet(os.path.join(DATA_DIR, dataset_id, "clusters", cluster_labels_id + ".parquet"))
    # remove the indices column

    cluster_labels_df = cluster_labels_df.drop(columns=[col for col in ["indices", "labeled", "label_raw"] if col in cluster_labels_df.columns])
    # cluster_labels_df = cluster_labels_df.drop(columns=["indices", "labeled", "label_raw"])
    # change hulls to a list of lists
    cluster_labels_df["hull"] = cluster_labels_df["hull"].apply(lambda x: x.tolist())
    cluster_labels_df["cluster"] = cluster_labels_df.index
    scope["cluster_labels_lookup"] = cluster_labels_df.to_dict(orient="records")
    
    # create a scope parquet by combining the parquets from umap and cluster, as well as getting the labels from cluster_labels
    # then write the parquet to the scopes directory
    umap_df = pd.read_parquet(os.path.join(DATA_DIR, dataset_id, "umaps", umap_id + ".parquet"))
    print("umap columns", umap_df.columns)

    # TODO: make this a shared function with umapper.py
    # or maybe we don't need it in UMAP.py at all?
    def make_tiles(x, y, num_tiles=64):
        import numpy as np
        tile_size = 2.0 / num_tiles  # Size of each tile (-1 to 1 = range of 2)
        
        # Calculate row and column indices (0-63) for each point
        col_indices = np.floor((x + 1) / tile_size).astype(int)
        row_indices = np.floor((y + 1) / tile_size).astype(int)
        
        # Clip indices to valid range in case of numerical edge cases
        col_indices = np.clip(col_indices, 0, num_tiles - 1)
        row_indices = np.clip(row_indices, 0, num_tiles - 1)
        
        # Convert 2D grid indices to 1D tile index (row * num_cols + col)
        tile_indices = row_indices * num_tiles + col_indices
        return tile_indices

    # umap_df['tile_index_32'] = make_tiles(umap_df['x'], umap_df['y'], 32)
    umap_df['tile_index_64'] = make_tiles(umap_df['x'], umap_df['y'], 64)
    umap_df['tile_index_128'] = make_tiles(umap_df['x'], umap_df['y'], 128)

    cluster_df = pd.read_parquet(os.path.join(DATA_DIR, dataset_id, "clusters", cluster_id + ".parquet"))
    cluster_labels_df = pd.read_parquet(os.path.join(DATA_DIR, dataset_id, "clusters", cluster_labels_id + ".parquet"))
    # create a column where we lookup the label from cluster_labels_df for the index found in the cluster_df
    cluster_df["label"] = cluster_df["cluster"].apply(lambda x: cluster_labels_df.loc[x]["label"])
    print("cluster columns", cluster_df.columns)
    scope_parquet = pd.concat([umap_df, cluster_df], axis=1)
    # TODO: add the max activated feature to the scope_parquet
    # or all the sparse features? top 10?

    print("scope_id", scope_id)
    # create a column to indicate if the row has been deleted in the scope
    scope_parquet["deleted"] = False
    if scope_id is not None:
        # read the transactions file
        transactions_file_path = os.path.join(DATA_DIR, dataset_id, "scopes", scope_id + "-transactions.json")
        with open(transactions_file_path) as f:
            transactions = json.load(f)
            for transaction in transactions:
                if transaction["action"] == "delete_rows":
                    scope_parquet.loc[transaction["payload"]["row_ids"], "deleted"] = True

    # Add an ls_index column that is the index of each row in the dataframe
    scope_parquet['ls_index'] = scope_parquet.index
    print("scope columns", scope_parquet.columns)
    scope_parquet.to_parquet(os.path.join(directory, id + ".parquet"))

    scope["rows"] = len(scope_parquet)
    scope["columns"] = scope_parquet.columns.tolist()
    scope["size"] = os.path.getsize(os.path.join(directory, id + ".parquet"))
    scope["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    file_path = os.path.join(directory, id + ".json")
    with open(file_path, 'w') as f:
        json.dump(scope, f, indent=2)
    
    transactions_file_path = os.path.join(directory, id + "-transactions.json")
    if not os.path.exists(transactions_file_path):
        with open(transactions_file_path, 'w') as f:
            json.dump([], f)
    
    print("creating combined scope-input parquet")
    input_df = pd.read_parquet(os.path.join(DATA_DIR, dataset_id, "input.parquet"))
    input_df.reset_index(inplace=True)
    input_df = input_df[input_df['index'].isin(scope_parquet['ls_index'])]
    combined_df = input_df.join(scope_parquet.set_index('ls_index'), on='index', rsuffix='_ls')
    combined_df.to_parquet(os.path.join(directory, id + "-input.parquet"))

    print("exporting to lancedb")
    export_lance(DATA_DIR, dataset_id, id)

    print("wrote scope", id)

