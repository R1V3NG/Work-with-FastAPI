import models
from datetime import datetime, timedelta
from auth import AuthHandler

auth = AuthHandler()


models.db.create_db_and_tables()

with models.db.Session(models.db.engine) as session:
    admin = models.Users(
        name="admin",
        password=auth.get_password_hash("admin1234"),
        is_admin=True,
    )
    user = models.Users(
        name="user",
        password=auth.get_password_hash("password-user"),
        is_admin=False,
    )
    session.add_all([admin, user])
    session.commit()
    session.refresh(admin)
    session.refresh(user)

    from datetime import datetime, timedelta, timezone

    task1 = models.Tasks(
        title="Купить продукты",
        priority=models.Priority.MEDIUM,
        deadline=datetime.now(timezone.utc) + timedelta(days=2),
        description="Молоко, хлеб, яйца",
        user_id=user.id,
    )
    task2 = models.Tasks(
        title="Сдать отчёт",
        priority=models.Priority.HIGH,
        deadline=datetime.now(timezone.utc) + timedelta(days=1),
        description="Подготовить презентацию",
        user_id=user.id,
    )
    task3 = models.Tasks(
        title="Почитать книгу",
        priority=models.Priority.LOW,
        deadline=datetime.now(timezone.utc) + timedelta(days=5),
        description="Закончить главу 3",
        user_id=admin.id,
    )
    session.add_all([task1, task2, task3])
    session.commit()