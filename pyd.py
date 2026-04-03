from pydantic import BaseModel, Field
from typing import Optional

class UserChoice(BaseModel):
    choice:str = Field("Камень")

class UserCreate(BaseModel):
    id:int|None
    username:str = Field(example="Ivanov123", min_length=3, max_length=50)
    email:str = Field(example="ivanov@mail.ru")
    password:str = Field(example="password123", min_length=8)
    full_name:str | None = Field(default=None)
    age:int | None = Field(None, ge=18, le=120)
    is_active:bool = Field(True)

class ItemCreate(BaseModel):
    name:str = Field(min_length=3, max_length=100)
    description:str | None = Field(max_length=1000)
    price:float = Field(ge=0.01, le=1000000)
    tax:float = Field(0, ge=0, le=100)
    tags:list[str] | None
    in_stock:bool = Field(True)
    quantity:int | None = Field(example=1, ge=0, le=1000)

class User(BaseModel):
    name:str = Field(example="Анна")
    age:int = Field(example=25, ge=0, le=150)
    active:bool = Field(example=True)

class Filters(BaseModel):
    min_age:int | None = Field(0,example=None, ge=0, le=150)
    max_age:int | None = Field(150, ge=0, le=150)
    is_active:bool | None = Field(None, example=True)

class FilterUsers(BaseModel):
    users:list[User]
    filters:Filters

class ResponseFilters(BaseModel):
    total_input:int
    filtered_count:int
    filtered_users:list[User] = Field([])
    applied_filters:Filters

class UserUpdate(BaseModel):
    email:str | None = Field("")
    full_name:str | None = Field("")
    age:int | None = Field(17, ge=17, le=120)
    is_active:bool | None = Field(None)