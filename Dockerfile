# Dockerfile server
FROM python:3.9-slim

WORKDIR /app

COPY . /app

# Создаём папку для базы данных
RUN mkdir -p /app/data

RUN pip install --no-cache-dir -r requirements.txt

RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. glossary.proto

EXPOSE 50051

CMD ["python", "server.py"]