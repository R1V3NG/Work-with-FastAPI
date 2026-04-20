import models
from datetime import datetime, timedelta

models.db.create_db_and_tables()

with models.db.Session(models.db.engine) as session:
    user1 = models.Users(name="user", password="password-user")
    user2 = models.Users(name="admin", password="password-admin")
    session.add(user1)
    session.add(user2)
    session.commit()
    session.refresh(user1)
    session.refresh(user2)

    task1 = models.Tasks(
        title="Купить продукты",
        priority=models.Priority.MEDIUM,
        deadline=datetime.now() + timedelta(days=2),
        description="Молоко, хлеб, яйца",
        user_id=user1.id
    )
    task2 = models.Tasks(
        title="Сдать отчёт",
        priority=models.Priority.HIGH,
        deadline=datetime.now() + timedelta(days=1),
        description="Подготовить презентацию",
        user_id=user1.id
    )
    task3 = models.Tasks(
        title="Почитать книгу",
        priority=models.Priority.LOW,
        deadline=datetime.now() + timedelta(days=5),
        description="Закончить главу 3",
        user_id=user2.id
    )
    session.add_all([task1, task2, task3])
    session.commit()