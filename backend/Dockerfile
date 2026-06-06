# base image
FROM python:3.11-slim

# set workdir
WORKDIR /app

# copia requirements
COPY requirements.txt .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copia codice
COPY . .

# esponi porta
EXPOSE 8000

# avvio
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

