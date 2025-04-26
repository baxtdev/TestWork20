# Transaction Service

## 📥 Установка и запуск проекта

### 1. Клонировать репозиторий
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```
## С помошью Docker,Docker-Compose
### 1. Создать .env файл
```bash
cp .env.example .env
```
#### или создаем .env файл и вставим эти значении
```bash POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=transaction_db
POSTGRES_HOST=db
POSTGRES_PORT=5432

SYNC_DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}
DATABASE_URL=postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}

REDIS_HOST=redis
REDIS_PORT=6379
```
### 2.Запуск Docker Compose
```bash
docker-compose up --build
```

## Запуск проекта локально (без Docker)
### 1.Создаем .env файл и вставвим
```bash
SYNC_DATABASE_URL = "sqlite:///./transaction_db.sqlite3"  
DATABASE_URL = "sqlite+aiosqlite:///./transaction_db.sqlite3"
REDIS_HOST = "localhost"
REDIS_PORT = "6379" 
```
### 2.Запуск проекта
```bash 
uvicorn transaction.main:app --reload
```
