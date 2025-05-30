# Тестовое задание
Данный проект нацелен на мое изучение различных технологий бекенда на языке Python

Возможно будет полезно для других начинающих

## Стек
- FastAPI
- SQLAlchemy
- Pydantic
- Passlib
- Python-jose
- AioSqlite

## Архитектура
### Основная информация
Архитектура основана на модели **controller-model-view**

**Controller** - Основная часть логики работы приложения, там происходит обращение к базе данных, вычисление значений и прочее

**Model** - Различные классы и структуры для хранения и представления объектов приложения

**View** - Часть, взаимодействующая с пользователем (получает от него данные и приводит их к нужному формату и наоборот)

### Файловая структура
- `src` - Основная папка, хранящая в себе весь код
- `src/base` - Папка, хранящая в себе базовые системы (конфиг, база данных)
- `src/controllers` - Папка, хранящая в себе контроллеры приложения
- `src/models` - Папка, хранящая в себе модели приложения
- `src/routers` - Папка, хранящая в себе роутеры (routers, в данном случае это view-часть)
- `main.py` - Основной файл приложения, с которого идет запуск и lifespan

## Информация о проекте
Это бекенд для виртуальной библиотеки, который обладает следующим функционалом:

- Регистрация и логин пользователей
- Получение информации о книгах в каталоге
- Механизм забирания книг и их возвращения
- Получение информации о пользователях

### Основные роутеры
- POST `/auth/register`
- POST `/auth/login`
- GET `/books/list`
- POST `/books/borrow`
- GET `/users/borrowed_books_list`
