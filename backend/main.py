from pathlib import Path
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from chatbot import (
    ask_question,
    reload_knowledge_base,
    add_document_to_knowledge_base
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


@app.get("/")
def home():

    return {

        "message": "Knowledge Bot Running"

    }


@app.get("/ask")
def ask(question: str):

    result = ask_question(question)

    return {

        "question": question,

        "answer": result["answer"],

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

                    "type": file.suffix.replace(".", "").upper()

                })

    files.sort(

        key=lambda x: x["name"].lower()

    )

    return {

        "documents": files

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

