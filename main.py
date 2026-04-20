from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlmodel import select
from typing import Optional, List
import models
import db

app = FastAPI()
security = HTTPBasic(auto_error=False)

def get_current_user(
    session: db.SessionDep,
    credentials: Optional[HTTPBasicCredentials] = Depends(security),
) -> models.Users:
    if not credentials:
        raise HTTPException(status_code=401, detail="Необходима авторизоваться")
    user = session.exec(
        select(models.Users).where(models.Users.name == credentials.username)
    ).first()
    if not user or user.password != credentials.password:
        raise HTTPException(status_code=403, detail="Неверный логин или пароль")
    return user

def validate_password(password: str):
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Пароль должен быть длинной более 8 символов")
    if not any(c.isalpha() for c in password):
        raise HTTPException(status_code=400, detail="Пароль должен содержать хотя бы одну букву")
    if not any(c.isdigit() for c in password):
        raise HTTPException(status_code=400, detail="Пароль должен содержать хотя бы одну цифру")

@app.post("/user/register", response_model=models.UsersRead, tags=["Users"])
def register_user(user: models.UsersCreate, session: db.SessionDep):
    existing = session.exec(select(models.Users).where(models.Users.name == user.name)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    validate_password(user.password)
    db_user = models.Users(name=user.name, password=user.password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@app.get("/user/me", response_model=models.UsersRead, tags=["Users"])
def read_current_user(current_user: models.Users = Depends(get_current_user)):
    return current_user

@app.post("/tasks/", response_model=models.TasksRead, tags=["Tasks"])
def create_task(
    task: models.TasksCreate,
    session: db.SessionDep,
    current_user: models.Users = Depends(get_current_user),
):
    db_task = models.Tasks(
        title=task.title,
        priority=task.priority,
        deadline=task.deadline,
        description=task.description,
        user_id=current_user.id,
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@app.put("/tasks/{task_id}", response_model=models.TasksRead, tags=["Tasks"])
def update_task(
    task_id: int,
    task_update: models.TasksUpdate,
    session: db.SessionDep,
    current_user: models.Users = Depends(get_current_user),
):
    db_task = session.get(models.Tasks, task_id)
    if not db_task or db_task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@app.delete("/tasks/{task_id}", tags=["Tasks"])
def delete_task(
    task_id: int,
    session: db.SessionDep,
    current_user: models.Users = Depends(get_current_user),
):
    db_task = session.get(models.Tasks, task_id)
    if not db_task or db_task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    session.delete(db_task)
    session.commit()
    return {"ok": True}

@app.get("/tasks/", response_model=List[models.TasksRead], tags=["Tasks"])
def list_tasks(
    session: db.SessionDep,
    current_user: models.Users = Depends(get_current_user),
    sort_by_deadline: bool = Query(False, description="Сортировка дедлайна по возрастанию"),
    priority: Optional[models.Priority] = Query(None, description="Фильтрация по приоритету"),
    start: int = Query(0, ge=0, description="Начало пагинации"),
    end: int = Query(10, ge=1, le=100, description="Конец пагинации"),
):
    query = select(models.Tasks).where(models.Tasks.user_id == current_user.id)
    if priority:
        query = query.where(models.Tasks.priority == priority)
    if sort_by_deadline:
        query = query.order_by(models.Tasks.deadline.asc())
    tasks = session.exec(query.offset(start).limit(end)).all()
    return tasks

@app.get("/tasks/{task_id}", response_model=models.TasksRead, tags=["Tasks"])
def get_task(
    task_id: int,
    session: db.SessionDep,
    current_user: models.Users = Depends(get_current_user),
):
    task = session.get(models.Tasks, task_id)
    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task