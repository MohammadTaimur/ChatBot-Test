PDF ChatBot (FastAPI + Streamlit + Groq)<br>
This project allows users to upload a PDF, and then ask context-based questions about the content. It uses:
- 🧠 Groq LLM (llama3-8b-8192)
- ⚡ FastAPI (for backend/API)
- 🖼️ Streamlit (for frontend)
- 🔍 ChromaDB (for vector search)
- 📄 PDFPlumber (to extract text from PDFs)

Features:
- Upload a PDF file
- Extract and chunk content
- Store vector embeddings
- Chat with the document using Groq's LLM

Running via Docker:
Docker installed on your system
A .env file with your Groq API key

Folder Structure:
<br>
├── backend/<br>
│   ├── main.py<br>
│   ├── utils.py<br>
│   ├── chromaDatabaseFunctions.py<br>
├── frontend/<br>
│   └── streamlit_app.py<br>
├── requirements.txt<br>
├── Dockerfile<br>
└── .env        👈 NOT included in repo (you must create this)

Step by Step Setup:
1. Clone the repository:
   git clone https://github.com/MohammadTaimur/ChatBot-Test.git
   cd Chatbot-Test
2. Create .env
   Create a file named .env in the project root and add the following line with your own api key:
   GROQ_API_KEY=your_groq_api_key_here
3. Build the Docker image
   docker build -t yourdockername .
4. Run the container
   docker run -p 8000:8000 -p 8501:8501 --env-file .env yourdockername

Access the App
- Streamlit Frontend: http://localhost:8501
- FastAPI Docs: http://localhost:8000/docs
