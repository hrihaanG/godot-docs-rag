FROM python:3.12-slim

WORKDIR /app

# CPU-only PyTorch: much smaller than the default Linux build
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download the embedding model into the image so it is not fetched on every start
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

COPY load_docs.py chunk_docs.py search.py answer.py agent.py api.py ./
COPY chroma_db ./chroma_db

EXPOSE 8000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]