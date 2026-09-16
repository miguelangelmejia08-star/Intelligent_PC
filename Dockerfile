FROM python:3.14.7-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Crear el directorio de salidas
RUN mkdir -p outputs

CMD ["python", "main.py"]