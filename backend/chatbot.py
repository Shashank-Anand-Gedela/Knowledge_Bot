from document_loader import load_documents
from embeddings import create_embeddings
from vector_store import create_faiss_index
from gemini_service import generate_answer

# =====================================================
# Load Documents
# =====================================================

print("Loading documents...")

chunks, metadata = load_documents()

print(f"{len(chunks)} chunks loaded.")

print("Creating embeddings...")

embeddings = create_embeddings(chunks)

print("Building FAISS index...")

index = create_faiss_index(embeddings)

print("Knowledge Base Ready!")

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