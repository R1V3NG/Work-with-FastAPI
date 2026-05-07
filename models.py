from typing import Optional, List
from datetime import datetime
from enum import Enum
from sqlmodel import Field, SQLModel, Relationship
import db  # не убирать, нужна в seed.py для создания базы данных


class Priority(str, Enum):
    HIGH = "Высокий"
    MEDIUM = "Средний"
    LOW = "Низкий"


class Users(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    password: str
    is_admin: bool = Field(default=False)
    tasks: List["Tasks"] = Relationship(back_populates="user")


class UsersCreate(SQLModel):
    name: str
    password: str


class UsersRead(SQLModel):
    id: int
    name: str
    is_admin: bool


class Tasks(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    priority: Priority
    deadline: datetime
    description: Optional[str] = None
    user_id: int = Field(foreign_key="users.id")
    user: Users = Relationship(back_populates="tasks")


class TasksCreate(SQLModel):
    title: str
    priority: Priority
    deadline: datetime
    description: Optional[str] = None


class TasksUpdate(SQLModel):
    title: Optional[str] = None
    priority: Optional[Priority] = None
    deadline: Optional[datetime] = None
    description: Optional[str] = None


class TasksRead(SQLModel):
    id: int
    title: str
    priority: Priority
    deadline: datetime
    description: Optional[str] = None
    user_id: int
