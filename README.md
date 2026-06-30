# AI-Powered Knowledge Bot

## Overview

AI-Powered Knowledge Bot is a Retrieval-Augmented Generation (RAG) application that allows users to upload documents and ask questions in natural language. The system retrieves relevant information from the uploaded documents using semantic search and generates accurate answers using Google's Gemini model.

---

## Features

- AI-powered question answering
- Semantic document search using FAISS
- Supports PDF, DOCX, PPTX, XLSX, and TXT files
- React-based chat interface
- FastAPI backend
- Browse uploaded documents
- New Chat functionality
- Responsive user interface

---

## Technology Stack

### Frontend
- React.js
- CSS
- Axios

### Backend
- FastAPI
- Python

### AI
- Google Gemini API
- Sentence Transformers (all-MiniLM-L6-v2)
- FAISS

---

## Project Structure

```
Knowledge_Bot
│
├── backend
│
├── Knowledge_Bot_UI
│
└── README.md
```

---

## Installation

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd Knowledge_Bot_UI
npm install
npm run dev
```

---

## Future Enhancements

- Document upload from UI
- Chat history
- Authentication
- OCR support
- Cloud deployment

---

## Author

**Shashank Anand**