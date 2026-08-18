# ABP Conference Booking API

RESTful API сервіс для управління конференц-залами, додатковими послугами та бронюванням з урахуванням складних бізнес-правил та тарифних зон.

## Архітектура
Проект побудований за принципами
 **Чистої архітектури (Clean Architecture)**:
- **Domain (`app/core`, `app/domain`)**: Бізнес-логіка, доменні моделі, Pydantic-схеми та ізольований калькулятор вартості оренди.
- **Infrastructure (`app/infrastructure`)**: Робота з базою даних (PostgreSQL) через SQLAlchemy 2.0, репозиторії.
- **Services (`app/services`)**: Сценарії використання (Use Cases) та перевірка бізнес-правил.
- **API (`app/api`)**: FastAPI контролери та маршрутизація.

## Вимоги
- Python 3.10+
- Docker & Docker Compose

## Швидкий запуск

1. **Клонуйте репозиторій та перейдіть у папки проекту.**

2. **Запустіть базу даних через Docker Compose:**

bash

docker compose up -d

3. **Створіть та активуйте віртуальне середовище:**

bash

python3 -m venv venv

source venv/bin/activate

4. **Встановіть залежності:**

bash

pip install -r requirements.txt

5. **Заповніть базу початковими даними (зали та послуги):**

bash

python seed.py

6. **Запустіть сервер:**

bash

git add README.mduvicorn app.main:app --reload

Доступ до інтерактивної документації Swagger UI: **http://127.0.0.1:8000/docs**