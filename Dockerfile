# Use uma imagem base do Python  
FROM python:3.9-slim  

# Defina o diretório de trabalho dentro do contêiner  
WORKDIR /app  

# Instale dependências do sistema necessárias para o OpenCV  
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0  

# Copie o código e os arquivos necessários para o diretório de trabalho  
COPY Face_Recognition.py /app/  

# Copie o arquivo de dependências e instale o Gunicorn e outras dependências
COPY requirements.txt /app/  
RUN pip install --no-cache-dir -r requirements.txt  

# Exponha a porta 5000 (onde o Flask vai rodar)  
EXPOSE 5000  

# Comando para iniciar o servidor Flask usando Gunicorn  
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "Face_Recognition:app"]
