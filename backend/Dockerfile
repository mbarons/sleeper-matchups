FROM python:3.13-slim

# Define o diretório de trabalho - daqui pra frente tudo é relativo a /app
WORKDIR /app

# Copia só o requirements.txt para usar o cache do Docker nas dependências
COPY requirements.txt requirements.txt

# Instala as dependências usando pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copia todo o código da aplicação para dentro do container
COPY . .

# Comando para rodar o servidor FastAPI com uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
