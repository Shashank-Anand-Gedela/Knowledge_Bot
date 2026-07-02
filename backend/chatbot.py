from document_loader import (
    load_documents,
    load_single_document
)
import numpy as np
import re
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


TOP_K = 5


GREETING_WORDS = {
    "hi",
    "hello",
    "hey",
    "good morning",
    "good afternoon",
    "good evening",
    "greetings",
    "how are you",
    "how are you?",
    "who are you",
    "who are you?",
    "what can you do",
    "what can you do?"
}


def is_greeting(query):
    cleaned_query = query.strip().lower()

    for word in GREETING_WORDS:
        if cleaned_query == word:
            return True

    return False

def is_gibberish(query):

    cleaned = query.strip().lower()

    if len(cleaned) <= 2:
        return True

    if cleaned.isdigit():
        return True

    # random keyboard patterns
    gibberish_patterns = [
        "asdf",
        "qwert",
        "zxcv",
        "hjkl",
        "poiuy",
        "lkjhg",
        "mnbvc",
        "qazwsx",
        "plmokn",
        "qwertyuiop",
        "asdfghjkl",
        "zxcvbnm",
        "qwerty",
        "asdfgh",
        "zxcvbn",
        "qazwsxedc",
        "qazxswedcvfrtgbnhyujmkiolp"

    ]

    for pattern in gibberish_patterns:
        if pattern in cleaned:
            return True

    words = cleaned.split()

    # Single weird word
    if len(words) == 1:

        word = words[0]

        vowels = sum(
            1 for c in word
            if c in "aeiou"
        )

        if len(word) >= 4 and vowels == 0:
            return True

        if len(word) >= 6 and vowels / len(word) < 0.2:
            return True

    return False


def reload_knowledge_base():

    global chunks
    global metadata
    global embeddings
    global index

    print("Reloading Knowledge Base...")

    chunks, metadata = load_documents()

    if not chunks:
        embeddings = np.array([], dtype="float32")
        index = None

        save_chunks(chunks)
        save_metadata(metadata)
        save_embeddings(embeddings)
        save_index(index)

        print("No documents found. Knowledge Base cleared.")
        return

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

    if index is None or len(chunks) == 0:

        index = create_faiss_index(new_embeddings)

        embeddings = new_embeddings

        chunks.extend(new_chunks)

        metadata.extend(new_metadata)

    else:

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


def delete_document_from_knowledge_base(file_name):
    """
    Existing behavior is preserved.
    After deleting a document from the folder, the safest way is to rebuild
    the knowledge base from remaining documents.
    """

    print(f"Removing document from knowledge base: {file_name}")

    reload_knowledge_base()

    print("Knowledge Base updated after deletion.")


def build_source_url(source):
    document_name = source.get("document", "")
    file_type = source.get("file_type", "")
    page_number = source.get("page_number")

    if file_type.upper() == "PDF" and page_number:
        return f"http://localhost:8000/documents/open/{document_name}#page={page_number}"

    return f"http://localhost:8000/documents/open/{document_name}"


def ask_question(query, selected_document=None):

    query = query.strip()

    if not query:
        return {
            "answer": "Please enter a proper question.",
            "sources": []
        }

    if is_greeting(query):
        return {
            "answer": "Hello! I can answer questions based on your uploaded documents. Please ask a question related to the documents.",
            "sources": []
        }

    if is_gibberish(query):
        return {
            "answer": "I could not understand your question. Please ask a clear question related to the uploaded documents.",
            "sources": []
        }

    if not chunks or index is None:
        return {
            "answer": "No uploaded documents are available. Please upload documents first.",
            "sources": []
        }

    query_embedding = create_embeddings([query])

    if selected_document:
        search_k = len(chunks)
    else:
        search_k = min(TOP_K, len(chunks))

    distances, indices = index.search(
        query_embedding,
        k=search_k
    )

    context = ""

    retrieved_sources = []

    for idx, score in zip(indices[0], distances[0]):

        if idx == -1:
            continue

        source_metadata = metadata[idx]

        if selected_document:
            if source_metadata["document"].lower() != selected_document.lower():
                continue

        context += chunks[idx]
        context += "\n\n"

        retrieved_sources.append({

            "document": source_metadata["document"],

            "file_type": source_metadata["file_type"],

            "reference": source_metadata["reference"],

            "heading": source_metadata["heading"],

            "page_number": source_metadata.get("page_number"),

            #"score": round(float(score) * 100, 2),

            "preview": chunks[idx][:300]

        })

        if len(retrieved_sources) >= TOP_K:
            break

    if len(retrieved_sources) == 0:

        if selected_document:
            return {
                "answer": f"I couldn't find this information in the selected document: {selected_document}.",
                "sources": []
            }

        return {
            "answer": "I couldn't find this information in the uploaded documents.",
            "sources": []
        }

    answer = generate_answer(
        context,
        query
    ).strip()

    if answer.lower().startswith("i couldn't find this information"):

        return {
            "answer": answer,
            "sources": []
        }

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

            source["source_url"] = build_source_url(source)

            unique_sources.append(source)

    return {
        "answer": answer,
        "sources": unique_sources
    }