from pydantic import BaseModel, Field, EmailStr, validator
import re
from typing import List, Dict, Any
import random
import string

# POST /users
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str | None = None
    age: int | None = Field(None, ge=18, le=120)
    is_active: bool = True
    
    # Валидация username
    @validator('username')
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9]+$', v):
            raise ValueError('Только буквы и цифры')
        return v
    
    # Валидация пароля
    @validator('password')
    def validate_password(cls, v):
        if not any(c.isdigit() for c in v):
            raise ValueError('Нужна хотя бы 1 цифра')
        if not any(c.isalpha() for c in v):
            raise ValueError('Нужна хотя бы 1 буква')
        return v
    
# POST /items
class ItemCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: str | None = Field(None, max_length=1000)
    price: float = Field(..., gt=0, le=1_000_000)
    tax: float = Field(0, ge=0, le=100)
    tags: List[str] | None = Field(None, max_length=5)
    quantity: int | None = Field(None, ge=0, le=1000)
    in_stock: bool | None = None
    
    @validator('in_stock', always=True)
    def validate_in_stock(cls, v, values):
        quantity = values.get('quantity')
        
        # Если quantity указан и больше 0, то in_stock должен быть True
        if quantity is not None and quantity > 0:
            return True
        
        # Если quantity указан и равен 0, то in_stock должен быть False
        if quantity is not None and quantity == 0:
            return False
        
        # Если quantity не указан, оставляем in_stock как есть
        return v

# POST /filter-users

# Модель для отдельного пользователя во входных данных
class FilterUser(BaseModel):
    name: str
    age: int
    active: bool

# Модель для фильтров
class Filters(BaseModel):
    min_age: int | None = Field(0, ge=0, le=150)
    max_age: int | None = Field(150, ge=0, le=150)
    active_only: bool | None = None
    
    @validator('max_age')
    def validate_age_range(cls, v, values):
        if v is not None and values.get('min_age') is not None:
            if v < values['min_age']:
                raise ValueError('max_age не может быть меньше min_age')
        return v

# PUT /users/{user_id}

# Основная модель запроса
class FilterUsersRequest(BaseModel):
    users: List[FilterUser] = Field(..., max_length=100)
    filters: Filters
# Модель ответа
class FilterUsersResponse(BaseModel):
    total_input: int
    filtered_count: int
    filtered_users: List[Dict[str, Any]]
    applied_filters: Dict[str, Any]

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None
    age: int | None = Field(None, ge=18, le=120)
    is_active: bool | None = None

# Функция для генерации случайных значений
def generate_random_email() -> str:
    # Генерирует случайный email
    username = ''.join(random.choices(string.ascii_lowercase, k=8))
    domains = ['example.com', 'test.com', 'mail.com', 'gmail.com', 'yandex.ru']
    return f"{username}@{random.choice(domains)}"

def generate_random_full_name() -> str:
    # Генерирует случайное полное имя
    first_names = ['Иван', 'Петр', 'Кирилл', 'Алексей', 'Дмитрий', 'Анна', 
                   'Мария', 'Елена', 'Сергей', 'Василий', 'Игорь', 'Данил', 
                   'Александр', 'Константин', 'Вячеслав', 'Андрей', 'Дамир']
    last_names = ['Иванов(-а)', 'Петров(-а)', 'Сидоров(-а)', 'Алексеев(-а)', 
                  'Дмитриев(-а)', 'Смирнов(-а)', 'Кузнецов(-а)', 'Курпатов(-а)', 'Хадиулин(-а)']
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def generate_random_age() -> int:
    # Генерирует случайный возраст от 18 до 120
    return random.randint(18, 120)

def generate_random_bool() -> bool:
    # Генерирует случайное булево значение
    return random.choice([True, False])