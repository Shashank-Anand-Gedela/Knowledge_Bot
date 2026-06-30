from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from chatbot import ask_question

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