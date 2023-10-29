# Сбор пожертвований для котиков «QR Кот»

Веб-приложение для сбора пожертвований.
Автоматически размещает все поступившие пожертвования по открытым проектам.

---
#### Установка:
```
git clone git@github.com:tWoAlex/cat_charity_fund.git
```

---
#### Запуск:

1. Создай и включи виртуальное окружение:

Windows:
```
python -m venv venv
```
```
source venv/Scripts/activate
```
Linux:
```
python -m venv env
```
```
source venv/bin/activate
```

2. Установи библиотеки:
```
pip install -r requirements.txt
```

3. Создай файл `.env` в корне проекта для секретных параметров:
```
APP_TITLE=QR Кот, сбор пожертвований для котиков # Название приложения
DESCRIPTION=Помогите котикам жить тепло, вкусно и счастливо! # Описание приложения

DATABASE_URL={{ драйвер + адрес БД }}
# Драйвер + адрес БД должен быть составлен в соответствии со спецификацией SQLAlchemy (docs.sqlalchemy.org/en/14/core/engines.html)
#   и поддерживать асинхронные запросы.
# Для локального тестирования можно использовать "sqlite+aiosqlite:///./fastapi.db"

SECRET={{ секретный ключ шифрования для проекта }}

# Автоматическое создание первого суперпользователя:
FIRST_SUPERUSER_EMAIL={{ E-mail суперпользователя }}
FIRST_SUPERUSER_PASSWORD={{ Пароль суперпользователя }}
```

4. Инициируй базу данных:
```
alembic upgrade head
```
Если в `.env`-файле указаны параметры **первого суперпользователя**, он будет создан при первом запуске приложения.

5. Запусти приложение:
```
uvicorn app.main:app
```

---

### API:

Подробная документация доступна по адресам `{{ Хост }}/docs` (OpenAPI) и `{{ Хост }}/redoc` (Redoc).

Примеры:

1. **GET** `{{ Хост }}/charity_project` отдаёт список всех проектов по сбору средств.

Формат ответа:
```
{
    "name": "string",
    "description": "string",
    "full_amount": 0,
    "id": 0,
    "invested_amount": 0,
    "fully_invested": true,
    "create_date": "2023-08-24T14:15:22Z",
    "close_date": "2023-11-24T10:10:00Z"
}
```
2. **POST** `{{ Хост  }}/donation` позволяет отправить пожертвование.

Формат запроса:
```
{
  "full_amount": 1000,
  "comment": "string"
}
```
3. **POST** `{{ Хост }}/auth/register` пройти регистрацию.

Формат запроса:
```
{
  "email": "user@example.com",
  "password": "string"
}
```

4. **POST** `{{ Хост }}/auth/jwt/login` получить токен авторизации.

Формат запроса:
```
{
  "email": "user@example.com",
  "password": "string"
}
```
Формат ответа:
```
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiOTIyMWZmYzktNjQwZi00MzcyLTg2ZDMtY2U2NDJjYmE1NjAzIiwiYXVkIjoiZmFzdGFwaS11c2VyczphdXRoIiwiZXhwIjoxNTcxNTA0MTkzfQ.M10bjOe45I5Ncu_uXvOmVV8QxnL-nZfcH96U90JaocI",
  "token_type": "bearer"
}
```

---
### О проекте:

#### Построен на: [**FastAPI 0.78**](https://fastapi.tiangolo.com/) с использованием ORM [**SQLAlchemy 1.4**](https://docs.sqlalchemy.org/en/14/).
#### Для управления пользователями использована библиотека [**Fastapi-Users 10.0**](https://fastapi-users.github.io/fastapi-users/10.0/).
#### Автор: Александр Муравякин, **[t.me/tWoAlex](https://t.me/tWoAlex)**