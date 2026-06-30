import faiss
import numpy as np


def create_faiss_index(embeddings):

    embeddings = np.asarray(

        embeddings,

        dtype="float32"

    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(

        dimension

    )

    index.add(

        embeddings

    )

    return index