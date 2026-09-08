"""
SQL Battle Backend - Seed script for initial data.
Run this to populate the database with sample tasks and an admin user.
"""
import asyncio
import sys
sys.path.insert(0, '.')

from database import init_db, async_session
from models import User, Task, Settings
from auth import get_password_hash
from datetime import datetime


async def seed():
    await init_db()
    
    async with async_session() as db:
        # Create admin user
        admin = User(
            username="admin",
            email="admin@sqlbattle.com",
            password_hash=get_password_hash("admin123"),
            role="admin",
            rating=0,
            total_points=0
        )
        db.add(admin)
        
        # Create sample tasks
        task1 = Task(
            title="Найди активных хакеров",
            description="Напишите запрос, который вернёт список имён всех активных хакеров (status = 'active').",
            difficulty="easy",
            points=100,
            schema="""CREATE TABLE hackers (
  id INT,
  name VARCHAR,
  status VARCHAR
);""",
            tables=[
                {
                    "name": "hackers",
                    "columns": [
                        {"name": "id", "type": "INT"},
                        {"name": "name", "type": "VARCHAR"},
                        {"name": "status", "type": "VARCHAR"}
                    ],
                    "sampleData": [
                        {"id": 1, "name": "Алексей", "status": "active"},
                        {"id": 2, "name": "Мария", "status": "inactive"},
                        {"id": 3, "name": "Дмитрий", "status": "active"},
                        {"id": 4, "name": "Елена", "status": "active"},
                        {"id": 5, "name": "Сергей", "status": "inactive"}
                    ]
                }
            ],
            expected_result=[
                {"name": "Алексей"},
                {"name": "Дмитрий"},
                {"name": "Елена"}
            ]
        )
        db.add(task1)
        
        task2 = Task(
            title="Топ-10 самых дорогих заказов",
            description="Напишите запрос, который вернёт 10 самых дорогих заказов с указанием ID клиента и суммы заказа. Отсортируйте по убыванию суммы.",
            difficulty="medium",
            points=250,
            schema="""CREATE TABLE orders (
  id INT,
  client_id INT,
  amount DECIMAL,
  created_at TIMESTAMP
);""",
            tables=[
                {
                    "name": "orders",
                    "columns": [
                        {"name": "id", "type": "INT"},
                        {"name": "client_id", "type": "INT"},
                        {"name": "amount", "type": "DECIMAL"},
                        {"name": "created_at", "type": "TIMESTAMP"}
                    ],
                    "sampleData": [
                        {"id": 1, "client_id": 101, "amount": 1500.50, "created_at": "2026-09-01 10:30:00"},
                        {"id": 2, "client_id": 102, "amount": 2300.00, "created_at": "2026-09-02 14:15:00"},
                        {"id": 3, "client_id": 103, "amount": 890.75, "created_at": "2026-09-03 09:45:00"},
                        {"id": 4, "client_id": 104, "amount": 3200.00, "created_at": "2026-09-04 11:00:00"},
                        {"id": 5, "client_id": 105, "amount": 750.25, "created_at": "2026-09-05 16:30:00"},
                        {"id": 6, "client_id": 101, "amount": 1800.00, "created_at": "2026-09-06 09:00:00"},
                        {"id": 7, "client_id": 106, "amount": 4500.00, "created_at": "2026-09-07 13:45:00"},
                        {"id": 8, "client_id": 107, "amount": 990.00, "created_at": "2026-09-08 10:20:00"},
                        {"id": 9, "client_id": 108, "amount": 2100.50, "created_at": "2026-09-09 15:10:00"},
                        {"id": 10, "client_id": 109, "amount": 1650.75, "created_at": "2026-09-10 08:30:00"},
                        {"id": 11, "client_id": 110, "amount": 3800.00, "created_at": "2026-09-11 12:00:00"},
                        {"id": 12, "client_id": 102, "amount": 520.00, "created_at": "2026-09-12 14:30:00"}
                    ]
                }
            ],
            expected_result=[
                {"client_id": 107, "amount": 4500.00},
                {"client_id": 110, "amount": 3800.00},
                {"client_id": 104, "amount": 3200.00},
                {"client_id": 102, "amount": 2300.00},
                {"client_id": 108, "amount": 2100.50},
                {"client_id": 106, "amount": 1800.00},
                {"client_id": 101, "amount": 1500.50},
                {"client_id": 109, "amount": 1650.75},
                {"client_id": 103, "amount": 890.75},
                {"client_id": 107, "amount": 990.00}
            ]
        )
        db.add(task2)
        
        task3 = Task(
            title="Анализ заказов клиентов",
            description="Напишите запрос, который вернёт имя клиента, общую сумму его заказов и количество заказов. Выведите только тех клиентов, у которых более 2 заказов. Отсортируйте по общей сумме по убыванию.",
            difficulty="hard",
            points=500,
            schema="""CREATE TABLE users (
  id INT,
  name VARCHAR,
  email VARCHAR
);

CREATE TABLE orders (
  id INT,
  user_id INT,
  total_amount DECIMAL,
  created_at TIMESTAMP
);""",
            tables=[
                {
                    "name": "users",
                    "columns": [
                        {"name": "id", "type": "INT"},
                        {"name": "name", "type": "VARCHAR"},
                        {"name": "email", "type": "VARCHAR"}
                    ],
                    "sampleData": [
                        {"id": 1, "name": "Иван Петров", "email": "ivan@mail.ru"},
                        {"id": 2, "name": "Мария Сидорова", "email": "maria@mail.ru"},
                        {"id": 3, "name": "Дмитрий Козлов", "email": "dmitry@mail.ru"},
                        {"id": 4, "name": "Елена Волкова", "email": "elena@mail.ru"}
                    ]
                },
                {
                    "name": "orders",
                    "columns": [
                        {"name": "id", "type": "INT"},
                        {"name": "user_id", "type": "INT"},
                        {"name": "total_amount", "type": "DECIMAL"},
                        {"name": "created_at", "type": "TIMESTAMP"}
                    ],
                    "sampleData": [
                        {"id": 101, "user_id": 1, "total_amount": 1500.50, "created_at": "2026-09-01 10:30:00"},
                        {"id": 102, "user_id": 1, "total_amount": 2300.00, "created_at": "2026-09-02 14:15:00"},
                        {"id": 103, "user_id": 2, "total_amount": 890.75, "created_at": "2026-09-03 09:45:00"},
                        {"id": 104, "user_id": 1, "total_amount": 450.00, "created_at": "2026-09-04 16:20:00"},
                        {"id": 105, "user_id": 3, "total_amount": 1200.00, "created_at": "2026-09-05 11:00:00"},
                        {"id": 106, "user_id": 2, "total_amount": 3400.00, "created_at": "2026-09-06 13:30:00"},
                        {"id": 107, "user_id": 2, "total_amount": 750.00, "created_at": "2026-09-07 09:15:00"},
                        {"id": 108, "user_id": 4, "total_amount": 2100.00, "created_at": "2026-09-08 15:45:00"}
                    ]
                }
            ],
            expected_result=[
                {"name": "Мария Сидорова", "total_sum": 5040.75, "order_count": 3},
                {"name": "Иван Петров", "total_sum": 4250.50, "order_count": 3}
            ]
        )
        db.add(task3)
        
        # Create settings
        settings_obj = Settings(
            battle_start=datetime(2026, 9, 15, 10, 0, 0),
            round_duration_minutes=120
        )
        db.add(settings_obj)
        
        await db.commit()
        print("✅ Database seeded successfully!")
        print("   Admin user: admin / admin123")
        print("   3 sample tasks created")


if __name__ == "__main__":
    asyncio.run(seed())
