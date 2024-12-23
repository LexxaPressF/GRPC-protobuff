# Глоссарий на gRPC

Проект реализует функционал управления глоссарием (добавление, изменение, удаление и получение терминов) с использованием gRPC и SQLite.

## Описание работы приложения

### 1. Добавление термина
Для добавления нового термина используется клиентское приложение. Пример кода:

```python
stub.AddTerm(glossary_pb2.Term(key="Python", description="A programming language."))
```

### 2. Получение всех терминов
Получение всех терминов из глоссария осуществляется следующим образом:

```python
response = stub.GetAllTerms(glossary_pb2.Empty())
for term in response.terms:
    print(f"{term.key}: {term.description}")
```

### 3. Получение термина по ключу
Получение конкретного термина производится через метод `GetTerm`:

```python
response = stub.GetTerm(glossary_pb2.Key(key="Python"))
print(f"{response.key}: {response.description}")
```

### 4. Обновление термина
Для изменения описания существующего термина используется следующий код:

```python
response = stub.UpdateTerm(glossary_pb2.Term(key="Python", description="An interpreted programming language."))
```

### 5. Удаление термина
Удаление термина по ключу производится следующим образом:

```python
response = stub.DeleteTerm(glossary_pb2.Key(key="Python"))
```

---

## Инструкция по запуску через Docker

### 1. Сборка Docker-образов
Создание Docker-образов осуществляется командой:

```bash
docker compose build
```

Эта команда создаёт образы для серверного и клиентского приложений на основе файлов `Dockerfile` и `docker-compose.yml`.

### 2. Запуск контейнеров
Запуск всех сервисов выполняется через команду:

```bash
docker compose up -d
```

- Флаг `-d` запускает контейнеры в фоновом режиме.
- Сервер становится доступен на порту `50051`.

Для проверки запущенных контейнеров используется команда:

```bash
docker compose ps
```

### 3. Запуск только сервера
Запуск только серверного контейнера осуществляется через:

```bash
docker compose up -d grpc-server
```

### 4. Просмотр логов
Просмотр логов контейнеров выполняется следующими командами:

- Логи сервера:

```bash
docker compose logs grpc-server
```

- Логи клиента:

```bash
docker compose logs grpc-client
```

### 5. Запуск клиента через Docker
Для запуска клиентского скрипта используется команда:

```bash
docker compose exec grpc-client python /app/client.py
```

Расшифровка команды:
- `docker compose exec` — выполнение команды внутри контейнера.
- `grpc-client` — имя клиентского сервиса из файла `docker-compose.yml`.
- `python /app/client.py` — команда для запуска клиентского приложения.

---

## Пример работы

### 1. Добавление термина
После добавления термина `Python` результат выглядит следующим образом:

```plaintext
Python: A programming language.
```

### 2. Получение всех терминов
Вывод списка терминов:

```plaintext
Python: A programming language.
```

### 3. Обновление термина
После обновления термина `Python` результат будет следующим:

```plaintext
Python: An interpreted programming language.
```

### 4. Удаление термина
После удаления термина он больше не будет доступен в глоссарии.

