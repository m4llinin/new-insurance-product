# New Insurance Product  
Проект предназначен для быстрого создания и вывода в продажу новых страховых продуктов, а также удобную работу агента для оформления этих продуктов.

## Технологии  
FastAPI, PostgreSQL, AsyncPG, SQLAlchemy 2.0, Alembic, RabbitMQ, Redis, Uvicorn, HttpX, Loguru, MyPy, Pydantic, PyTest

## Функции  
- Создает и сохранает новый продукт в БД  
- Считает стоимость полиса и страховую премию агента при оформлении  
- Оформляет страховой полис с возможностью указания всех рисков  

## Запуск  
1. Клонировать проект  
```bash
git clone https://github.com/m4llinin/new-insurance-product.git
cd new-insurance-product  
```
2. Заполнить файл env/prod.env
3. Запустить при помощи docker-compose.yml
```bash
docker compose up --build -d
```
