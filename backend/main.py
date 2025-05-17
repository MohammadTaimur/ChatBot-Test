#pip install groq fastapi uvicorn python-multipart pdfplumber langchain sentence-transformers chromadb python-dotenv
from groq import Groq
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from .utils import readPDF, chunking_text
from .chromaDatabaseFunctions import embeddings, retrieve_relevent_text
import os

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

app = FastAPI()

@app.post('/UploadingPDF/')
async def UploadingPDF(
    file : UploadFile = File(...) 
):
    """
    Endpoint to upload a PDF, extract its text, chunk it, and store embeddings in ChromaDB.

    Args:
        file (UploadFile): The uploaded PDF file.

    Returns:
        No returns
    """
    print("working")
    pdf_text = readPDF(file)
    chunks = chunking_text(pdf_text)
    embeddings(chunks)
    print("done")

chat_history = []

@app.post('/ChatBot/')
async def ChatBot(
     query : str = Form(...), #Form data needs python-multipart library
):
    """
    Endpoint to handle chatbot queries using a retrieved context from ChromaDB and Groq LLM.

    Args:
        query (str): The user's question.

    Returns:
        str: The chatbot's response.

    Raises:
        HTTPException: If LLM completion fails.
    """
    chat_history.append({"role": "user", "content": query})

    retrieved_context = retrieve_relevent_text(query)
    
    try:
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"""###Chat Role
You are a helpful and concise assistant. Use the ###context provided to answer the question.

###History
{chat_history}

###context
{retrieved_context}

###chat_instructions>
1. Stick to **factual, relevant** responses based on that context.
2. Do NOT make up information or go beyond the context.
3. If the answer cannot be found in the context, respond with: "I am sorry, I could not find the answer in the document provided."
4. If the user brings up inappropriate topics (e.g., adult content or personal questions): **Redirect** and say: "Let's keep things friendly and respectful!"
"""
                },
                {
                    "role": "user",
                    "content": query
                },
            ],
            model="llama3-8b-8192",
        )
        output = chat_completion.choices[0].message.content.strip()
        chat_history.append({"role": "assistant", "content": output})
        return output
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error Generating LLM Response: {e}")