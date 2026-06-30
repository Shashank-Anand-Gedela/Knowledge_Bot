import os
import fitz
from docx import Document
from pptx import Presentation
from openpyxl import load_workbook
from langchain_text_splitters import RecursiveCharacterTextSplitter

DOCUMENTS_FOLDER = "documents"

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)


def clean_text(text):
    return " ".join(text.split())


def load_documents():

    chunks = []
    metadata = []

    for file in os.listdir(DOCUMENTS_FOLDER):

        file_path = os.path.join(DOCUMENTS_FOLDER, file)

        # =====================================================
        # PDF
        # =====================================================

        if file.lower().endswith(".pdf"):

            pdf = fitz.open(file_path)

            total_pages = len(pdf)

            for page_number, page in enumerate(pdf):

                text = clean_text(page.get_text())

                if not text:
                    continue

                page_chunks = splitter.split_text(text)

                for chunk in page_chunks:

                    chunks.append(chunk)

                    metadata.append({

                        "document": file,

                        "file_type": "PDF",

                        "reference": f"Page {page_number+1} of {total_pages}",

                        "heading": "PDF Content",

                        "chunk": chunk

                    })

        # =====================================================
        # WORD
        # =====================================================

        elif file.lower().endswith(".docx"):

            document = Document(file_path)

            current_heading = "Document"

            for para in document.paragraphs:

                text = clean_text(para.text)

                if not text:
                    continue

                if para.style.name.startswith("Heading"):

                    current_heading = text

                page_chunks = splitter.split_text(text)

                for chunk in page_chunks:

                    chunks.append(chunk)

                    metadata.append({

                        "document": file,

                        "file_type": "Word",

                        "reference": "Section",

                        "heading": current_heading,

                        "chunk": chunk

                    })

        # =====================================================
        # POWERPOINT
        # =====================================================

        elif file.lower().endswith(".pptx"):

            presentation = Presentation(file_path)

            total_slides = len(presentation.slides)

            for slide_number, slide in enumerate(presentation.slides):

                slide_title = "Untitled Slide"

                slide_text = ""

                if slide.shapes.title:

                    title = clean_text(slide.shapes.title.text)

                    if title:

                        slide_title = title

                for shape in slide.shapes:

                    if hasattr(shape, "text"):

                        slide_text += shape.text + "\n"

                slide_text = clean_text(slide_text)

                if not slide_text:
                    continue

                page_chunks = splitter.split_text(slide_text)

                for chunk in page_chunks:

                    chunks.append(chunk)

                    metadata.append({

                        "document": file,

                        "file_type": "PowerPoint",

                        "reference": f"Slide {slide_number+1} of {total_slides}",

                        "heading": slide_title,

                        "chunk": chunk

                    })

        # =====================================================
        # EXCEL
        # =====================================================

        elif file.lower().endswith(".xlsx"):

            workbook = load_workbook(file_path)

            total_sheets = len(workbook.sheetnames)

            for sheet_number, worksheet in enumerate(workbook.worksheets):

                sheet_name = worksheet.title

                rows = []

                for row in worksheet.iter_rows(values_only=True):

                    values = [

                        str(cell)

                        for cell in row

                        if cell is not None

                    ]

                    if values:

                        rows.append(" ".join(values))

                sheet_text = clean_text("\n".join(rows))

                if not sheet_text:
                    continue

                page_chunks = splitter.split_text(sheet_text)

                for chunk in page_chunks:

                    chunks.append(chunk)

                    metadata.append({

                        "document": file,

                        "file_type": "Excel",

                        "reference": f"Sheet {sheet_number+1} of {total_sheets}",

                        "heading": sheet_name,

                        "chunk": chunk

                    })

        # =====================================================
        # TEXT
        # =====================================================

        elif file.lower().endswith(".txt"):

            with open(

                file_path,

                "r",

                encoding="utf-8"

            ) as f:

                text = clean_text(f.read())

            if not text:
                continue

            page_chunks = splitter.split_text(text)

            for chunk in page_chunks:

                chunks.append(chunk)

                metadata.append({

                    "document": file,

                    "file_type": "Text",

                    "reference": "Text File",

                    "heading": "General",

                    "chunk": chunk

                })

    return chunks, metadata