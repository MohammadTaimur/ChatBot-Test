import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import numpy as np
from fastapi import HTTPException
from typing import List

# Load the embedding model
try:
    embedding_model = SentenceTransformer('all-MiniLM-L6-V2')
except Exception as e:
    raise HTTPException(status_code=404, detail={f"Embedding model could not be loaded: {e}"})

# Initialize ChromaDB client
chroma_client = chromadb.Client(Settings(
    persist_directory="chroma_store"
))

def embeddings(chunks: List[str]) -> None:
    """
    Generates embeddings for the provided text chunks and stores them in a ChromaDB collection.

    Args:
        chunks (List[str]): A list of text chunks to embed and store.

    Raises:
        HTTPException: If there is an error during embedding generation or ChromaDB storage.
    """
    try:
        embeddings = np.array([embedding_model.encode(chunk) for chunk in chunks], dtype=np.float32)
        collections = chroma_client.get_or_create_collection(name="pdf_chunks")
        collections.add(
            documents=chunks,
            embeddings=embeddings,
            ids=[f"chunk_{i}" for i in range(len(chunks))],
            metadatas=[{"source": "pdf"} for _ in chunks]
        )
    except Exception as e:
        raise HTTPException(status_code=402, detail={f"Error Creating Embeddings Or Storing in ChromaDB: {e}"})


def retrieve_relevent_text(query: str) -> str:
    """
    Retrieves the most relevant text chunk from ChromaDB based on the query.

    Args:
        query (str): The user's question or search query.

    Returns:
        str: The most relevant text chunk retrieved from ChromaDB.

    Raises:
        HTTPException: If there is an error during retrieval or embedding generation.
    """
    try:
        query_embedding = embedding_model.encode(query)
        collections = chroma_client.get_collection(name="pdf_chunks")

        results = collections.query(query_embeddings=query_embedding, n_results=3)

        for doc in results['documents'][0]:
            return doc
    except Exception as e:
        raise HTTPException(status_code=403, detail={f"Error Retrieving Context: {e}"})