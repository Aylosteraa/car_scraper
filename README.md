Застосунок для періодичного збору даних про б/у автомобілі з платформи AutoRia.  
Проєкт реалізований з використанням асинхронного скрапінгу, PostgreSQL та Docker.

Основний функціонал

- Асинхронний скрапінг сторінок зі списком авто
- Збір посилань на карточки автомобілів
- Парсинг даних з кожної карточки авто
- Збереження даних у PostgreSQL
- Відсутність дублів
- Щоденний дамп бази даних у папку `dumps/`
- Повна docker-compose інфраструктура

---

Стек технологій

- Python 3.11
- aiohttp
- BeautifulSoup4
- SQLAlchemy (async)
- PostgreSQL
- Docker / Docker Compose

---

Структура проєкту


- main.py - Точка входу застосунку
- main_page_scrapping.py - Збір URL карточок авто
- card_scrapping.py - Парсинг даних з карточок авто
- repo.py - Робота з БД 
- models.py - Моделі SQLAlchemy
- db.py - Підключення до БД
- init_db.py - Ініціалізація таблиць
- requirements.txt - Python-залежності

- Dockerfile - Контейнер scraper
- Dockerfile.backup - Контейнер backup
- docker-compose.yml - Оркестрація сервісів
- entrypoint.sh - Стартовий скрипт scraper

- backup.sh - Скрипт дампу БД
- crontab - Cron-розклад бекапів
- dumps/ - Дампи бази даних

- .env - Приклад змінних середовища
- README.md

---

Запуск програми

1. Створи файл `.env` у корені проєкту на основі прикладу:

```
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/auto_db
```

2. Перевірити, що Docker встановлено на ПК 

```
docker --version
docker compose version
```

3. Запустити проєкт 

```
docker compose up --build
```

