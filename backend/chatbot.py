from document_loader import (
    load_documents,
    load_single_document
)
import numpy as np
from embeddings import create_embeddings
from vector_store import create_faiss_index
from gemini_service import generate_answer
from cache_manager import (
    initialize_cache,
    cache_exists,
    save_index,
    load_index,
    save_embeddings,
    load_embeddings,
    save_chunks,
    load_chunks,
    save_metadata,
    load_metadata
)

# =====================================================
# Load Documents
# =====================================================

initialize_cache()

if cache_exists():

    print("Loading Knowledge Base from Cache...")

    chunks = load_chunks()

    metadata = load_metadata()

    embeddings = load_embeddings()

    index = load_index()

    print(f"{len(chunks)} chunks loaded from cache.")

else:

    print("No cache found.")

    print("Loading documents...")

    chunks, metadata = load_documents()

    print(f"{len(chunks)} chunks loaded.")

    print("Creating embeddings...")

    embeddings = create_embeddings(chunks)

    print("Building FAISS index...")

    index = create_faiss_index(embeddings)

    print("Saving cache...")

    save_chunks(chunks)

    save_metadata(metadata)

    save_embeddings(embeddings)

    save_index(index)

    print("Knowledge Base Cached Successfully.")

def reload_knowledge_base():

    global chunks
    global metadata
    global embeddings
    global index

    print("Reloading Knowledge Base...")

    chunks, metadata = load_documents()

    embeddings = create_embeddings(chunks)

    index = create_faiss_index(embeddings)

    save_chunks(chunks)
    save_metadata(metadata)
    save_embeddings(embeddings)
    save_index(index)

    print("Knowledge Base Reloaded!")

def add_document_to_knowledge_base(file_path):

    global chunks
    global metadata
    global embeddings
    global index

    print("Processing uploaded document...")

    new_chunks, new_metadata = load_single_document(file_path)

    if not new_chunks:

        print("No chunks created.")
        return

    print("Creating embeddings...")

    new_embeddings = create_embeddings(new_chunks)

    print(f"Adding {len(new_chunks)} chunks to FAISS...")

    index.add(
        new_embeddings.astype("float32")
    )

    chunks.extend(
        new_chunks
    )

    metadata.extend(
        new_metadata
    )

    embeddings = np.vstack(
        (
            embeddings,
            new_embeddings
        )
    )

    print("Updating cache...")

    save_chunks(chunks)
    save_metadata(metadata)
    save_embeddings(embeddings)
    save_index(index)

    print("Knowledge Base Updated Successfully.")


TOP_K = 5


def ask_question(query):

    # Create embedding for user query
    query_embedding = create_embeddings([query])

    # Search FAISS
    distances, indices = index.search(
        query_embedding,
        k=TOP_K
    )

    context = ""
    retrieved_sources = []

    # Build context
    for idx, score in zip(indices[0], distances[0]):

        if idx == -1:
            continue

        context += chunks[idx]
        context += "\n\n"

        retrieved_sources.append({

            "document": metadata[idx]["document"],

            "file_type": metadata[idx]["file_type"],

            "reference": metadata[idx]["reference"],

            "heading": metadata[idx]["heading"],

            "score": round(float(score) * 100, 2)

        })

    # No retrieved chunks
    if len(retrieved_sources) == 0:

        return {

            "answer": "I couldn't find this information in the uploaded documents.",

        }

    # Generate answer
    answer = generate_answer(
        context,
        query
    ).strip()

    # If Gemini couldn't answer, don't return any source
    if answer.lower().startswith("i couldn't find this information"):

        return {

            "answer": answer,

        }

    # Remove duplicate sources
    unique_sources = []

    seen = set()

    for source in retrieved_sources:

        key = (

            source["document"],

            source["reference"],

            source["heading"]

        )

        if key not in seen:

            seen.add(key)

            unique_sources.append(source)

    # Only keep the best source
    top_source = unique_sources[0] if unique_sources else None

    return {

        "answer": answer,

    }