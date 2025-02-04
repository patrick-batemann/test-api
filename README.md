# FastAPI PostgreSQL API example

## Структура проекта
- `main.py` — точка входа в приложение
- `models.py` — описание моделей базы данных
- `schemas.py` — схемы Pydantic для валидации данных
- `database.py` — подключение к базе данных
- `services.py` — логика выполнения запросов
- `requirements.txt` — зависимости проекта
- `Dockerfile` — инструкция для сборки Docker-образа
- `docker-compose.yml` — конфигурация контейнеров
- `docs/postman_collection.json` — коллекция Postman с примерами запросов

## Требования
Перед запуском убедитесь, что у вас установлены:
- Python 3.9+
- PostgreSQL
- Docker и Docker Compose (для запуска в контейнере)
- Postman (для тестирования API)

## Установка и запуск
### Локальный запуск
1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
2. Настройте переменные окружения для подключения к базе данных.
3. Запустите сервер:
   ```bash
   uvicorn main:app --reload
   ```
4. API будет доступен по адресу `http://localhost:8000`

### Запуск в Docker
1. Соберите и запустите контейнеры:
   ```bash
   docker-compose up --build
   ```
2. API будет доступен по адресу `http://localhost:8000`

- По умолчанию таблица `Marketplace` создается автоматически при запуске контейнера, однако при необходимости ее структуру можно уточнить с помощью функции `_update_db()` в `services.py`:
    ```bash
    import services
    services._update_db()
    ```

## Тестирование API в Postman
В проект также добавлена **Postman коллекция**.
1. Откройте **Postman**.
2. Импортируйте файл `docs/postman_collection.json`.
3. Используйте готовые запросы для работы с API.
