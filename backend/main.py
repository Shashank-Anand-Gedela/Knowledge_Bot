from pathlib import Path
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from chatbot import (
    ask_question,
    reload_knowledge_base,
    add_document_to_knowledge_base,
    delete_document_from_knowledge_base
)

app = FastAPI(
    title="Knowledge Bot API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


DOCUMENTS_FOLDER = Path("documents")


@app.get("/")
def home():
    return {
        "message": "Knowledge Bot Running"
    }


@app.get("/ask")
def ask(question: str, selected_document: str | None = None):
    result = ask_question(
        query=question,
        selected_document=selected_document
    )

    return {
        "question": question,
        "selected_document": selected_document,
        "answer": result["answer"],
        "sources": result.get("sources", [])
    }


@app.get("/documents")
def get_documents():
    documents_folder = Path("documents")

    supported_extensions = {
        ".pdf",
        ".docx",
        ".pptx",
        ".xlsx",
        ".txt"
    }

    files = []

    if documents_folder.exists():
        for file in documents_folder.iterdir():
            if file.is_file() and file.suffix.lower() in supported_extensions:
                files.append({
                    "name": file.name,
                    "type": file.suffix.replace(".", "").upper(),
                    "url": f"http://localhost:8000/documents/open/{file.name}"
                })

    files.sort(
        key=lambda x: x["name"].lower()
    )

    return {
        "documents": files
    }


@app.get("/documents/open/{file_name}")
def open_document(file_name: str):
    documents_folder = Path("documents")

    if not documents_folder.exists():
        raise HTTPException(
            status_code=404,
            detail="Documents folder not found."
        )

    matched_file = None

    for file in documents_folder.iterdir():
        if file.is_file() and file.name.lower() == file_name.lower():
            matched_file = file
            break

    if matched_file is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    return FileResponse(
        path=matched_file,
        #filename=matched_file.name
    )


@app.delete("/documents/{file_name}")
def delete_document(file_name: str):
    documents_folder = Path("documents")

    if not documents_folder.exists():
        raise HTTPException(
            status_code=404,
            detail="Documents folder not found."
        )

    matched_file = None

    for file in documents_folder.iterdir():
        if file.is_file() and file.name.lower() == file_name.lower():
            matched_file = file
            break

    if matched_file is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    matched_file.unlink()

    delete_document_from_knowledge_base(matched_file.name)

    return {
        "message": "Document deleted successfully.",
        "filename": matched_file.name
    }


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    documents_folder = Path("documents")

    documents_folder.mkdir(exist_ok=True)

    destination = documents_folder / file.filename

    if destination.exists():
        raise HTTPException(
            status_code=400,
            detail="Document already exists."
        )

    with destination.open("wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    add_document_to_knowledge_base(str(destination))

    return {
        "message": "Document uploaded successfully.",
        "filename": file.filename
    }


@app.post("/reload")
def reload_documents():
    reload_knowledge_base()

    return {
        "message": "Knowledge base reloaded successfully."
    }