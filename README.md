# hotel-booking-service
Сервис для бронирования отелей на основе Django REST Framework.
# Особенности
Django 5.2.6
Django REST Framework
PostgreSQL
Docker
Poetry
Pydantic Settings
Ruff
Pre-commit
Pytest

# Запуск с Docker
## Клонируйте репозиторий
git clone <repository-url>
cd hotel-booking-service

## Настройте переменные окружения
cp .env.example .env
Отредактируйте .env

## Запустите приложение
docker-compose up --build

## Приложение доступно по адресу
http://localhost:8000

hotel-booking-service/
├── src/                    # Исходный код приложения
│   ├── core/              # Основные настройки проекта
│   ├── rooms/             # Приложение для управления номерами
│   └── bookings/          # Приложение для бронирований
├── tests/                 # Тесты
├── docker-compose.yml     # Конфигурация Docker
├── Dockerfile            # Образ для production
├── DockerfileTest        # Образ для тестирования
├── pyproject.toml        # Зависимости и настройки Poetry
└── wait_for_db.py        # Скрипт ожидания БД



## API Endpoints
Управление номерами (/api/rooms/)
POST /api/rooms/create/ - создание номера

DELETE /api/rooms/delete/{id}/ - удаление номера

GET /api/rooms/list/ - список номеров (с сортировкой)

Управление бронированиями (/api/bookings/)
POST /api/bookings/create/ - создание брони

DELETE /api/bookings/delete/{id}/ - удаление брони

GET /api/bookings/list/{room_id}/ - бронирования номера


##  Тестирование
 docker-compose -f docker-compose.test.yml up --build
