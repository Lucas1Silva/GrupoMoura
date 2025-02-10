# Dockerfile
FROM python:3.10-slim

WORKDIR /app
ENV PYTHONPATH=/app

# Copia e instala as dependências
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia todo o código da aplicação
COPY . .

# Comando para iniciar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
