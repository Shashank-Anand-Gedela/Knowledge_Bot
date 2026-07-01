import os
import pickle
import numpy as np
import faiss

CACHE_DIR = "cache"

INDEX_FILE = os.path.join(CACHE_DIR, "index.faiss")
EMBEDDINGS_FILE = os.path.join(CACHE_DIR, "embeddings.npy")
CHUNKS_FILE = os.path.join(CACHE_DIR, "chunks.pkl")
METADATA_FILE = os.path.join(CACHE_DIR, "metadata.pkl")


def initialize_cache():
    os.makedirs(CACHE_DIR, exist_ok=True)


def cache_exists():
    return (
        os.path.exists(INDEX_FILE)
        and os.path.exists(EMBEDDINGS_FILE)
        and os.path.exists(CHUNKS_FILE)
        and os.path.exists(METADATA_FILE)
    )


def save_index(index):
    faiss.write_index(index, INDEX_FILE)


def load_index():
    return faiss.read_index(INDEX_FILE)


def save_embeddings(embeddings):
    np.save(EMBEDDINGS_FILE, embeddings)


def load_embeddings():
    return np.load(EMBEDDINGS_FILE)


def save_chunks(chunks):
    with open(CHUNKS_FILE, "wb") as f:
        pickle.dump(chunks, f)


def load_chunks():
    with open(CHUNKS_FILE, "rb") as f:
        return pickle.load(f)


def save_metadata(metadata):
    with open(METADATA_FILE, "wb") as f:
        pickle.dump(metadata, f)


def load_metadata():
    with open(METADATA_FILE, "rb") as f:
        return pickle.load(f)