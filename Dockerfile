# Dockerfile

# Use uma imagem oficial do Python como imagem base
FROM python:3.9-slim

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo de requisitos
COPY requirements.txt /app/

# Instale as dependências do projeto
RUN pip install flake8 black
RUN pip install --no-cache-dir -r requirements.txt

# Copie o conteúdo do projeto para dentro do contêiner
COPY . /app/

# Exponha a porta que o Django irá usar
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
