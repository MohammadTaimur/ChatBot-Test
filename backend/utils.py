from fastapi import UploadFile, HTTPException
import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List

def readPDF(file: UploadFile) -> str:
    """
    Reads the content of a PDF file and returns the extracted text.

    Parameters:
    - file (UploadFile): The uploaded PDF file to read.

    Returns:
    - str: The extracted text from the PDF.
    - HTTPException: If an error occurs while reading the PDF.
    """
    try:
        pdf_text = ""
        with pdfplumber.open(file.file) as pdf:
            for page in pdf.pages:
                pdf_text += page.extract_text()
        return pdf_text.strip()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error Reading PDF: {e}")


def chunking_text(text: str) -> List[str]:
    """
    Splits the given text into chunks for processing.

    Parameters:
    - text (str): The input text to split into chunks.

    Returns:
    - List[str]: A list of text chunks.
    - HTTPException: If an error occurs during text chunking.
    """
    try:
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        return splitter.split_text(text)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Error Chunking Text/PDF: {e}")