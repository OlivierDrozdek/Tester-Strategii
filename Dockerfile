FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --default-timeout=1000 -e .

COPY src/ ./src/

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]