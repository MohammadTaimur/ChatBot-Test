FROM python:3.13-slim

WORKDIR /InterviewTest

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000 8501

CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port 8000 & streamlit run frontend/streamlit_app.py --server.port=8501 --server.address=0.0.0.0"]