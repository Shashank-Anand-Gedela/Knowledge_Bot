from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def create_embeddings(text_chunks):

    embeddings = model.encode(

        text_chunks,

        convert_to_numpy=True,

        normalize_embeddings=True,

        show_progress_bar=False

    )

    return np.asarray(

        embeddings,

        dtype="float32"

    )