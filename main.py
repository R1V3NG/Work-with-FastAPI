from fastapi import FastAPI, HTTPException
from pyd import *
import random

app = FastAPI()

users_db = {}
items_db = {}

@app.post("/users")
def create_user(user: UserCreate):
    user_id = random.randint(1000, 9999)
    
    # Сохраняем полные данные (с паролем)
    users_db[user_id] = user.dict()
    
    # Возвращаем без пароля
    return {
        "id": user_id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "age": user.age,
        "is_active": user.is_active
    }

@app.post("/items")
def create_item(item: ItemCreate):
    # Генерируем ID
    item_id = random.randint(1000, 9999)
    
    # Вычисляем цену с налогом
    price_with_tax = item.price * (1 + item.tax / 100)
    
    # Определяем in_stock, если не указано
    in_stock = item.in_stock
    if in_stock is None:
        in_stock = item.quantity is not None and item.quantity > 0
    
    # Сохраняем в БД
    items_db[item_id] = {
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "tax": item.tax,
        "tags": item.tags,
        "quantity": item.quantity,
        "in_stock": in_stock
    }
    
    # Возвращаем ответ
    return {
        "id": item_id,
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "tax": item.tax,
        "price_with_tax": round(price_with_tax, 2),
        "tags": item.tags,
        "quantity": item.quantity,
        "in_stock": in_stock
    }

# # GET эндпоинты для проверки
# @app.get("/items")
# def get_all_items():
#     result = []
#     for item_id, item in items_db.items():
#         result.append({
#             "id": item_id,
#             **item
#         })
#     return result

# @app.get("/items/{item_id}")
# def get_item(item_id: int):
#     if item_id not in items_db:
#         return {"error": "Item not found"}
#     return {
#         "id": item_id,
#         **items_db[item_id]
#     }

@app.post("/filter-users", response_model=FilterUsersResponse)
def filter_users(request: FilterUsersRequest):
    # Получаем данные из запроса
    users = request.users
    filters = request.filters
    
    # Применяем фильтры
    filtered_users = []
    
    for user in users:
        include = True
        
        # Фильтр по минимальному возрасту
        if filters.min_age is not None and user.age < filters.min_age:
            include = False
            
        # Фильтр по максимальному возрасту
        if filters.max_age is not None and user.age > filters.max_age:
            include = False
            
        # Фильтр по активности
        if filters.active_only and not user.active:
            include = False
            
        if include:
            filtered_users.append(user.dict())
    
    # Формируем ответ
    applied_filters = {}
    if filters.min_age is not None:
        applied_filters["min_age"] = filters.min_age
    if filters.max_age is not None:
        applied_filters["max_age"] = filters.max_age
    if filters.active_only is not None:
        applied_filters["active_only"] = filters.active_only
    
    return FilterUsersResponse(
        total_input=len(users),
        filtered_count=len(filtered_users),
        filtered_users=filtered_users,
        applied_filters=applied_filters
    )

@app.put("/users/{user_id}")
def update_user(user_id: int, user_update: UserUpdate):
    # Проверяем, существует ли пользователь
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    # Получаем текущие данные пользователя
    current_user = users_db[user_id].copy()
    
    # Обновляем только переданные поля
    update_data = user_update.dict(exclude_unset=True)
    current_user.update(update_data)
    
    # Для полей, которых нет в запросе, заполняем рандомно
    if 'email' not in update_data:
        current_user['email'] = generate_random_email()
    
    if 'full_name' not in update_data:
        current_user['full_name'] = generate_random_full_name()
    
    if 'age' not in update_data:
        current_user['age'] = generate_random_age()
    
    if 'is_active' not in update_data:
        current_user['is_active'] = generate_random_bool()
    
    # Сохраняем обновлённые данные
    users_db[user_id] = current_user
    
    # Возвращаем обновлённого пользователя (без пароля)
    return {
        "id": user_id,
        "username": current_user['username'],
        "email": current_user['email'],
        "full_name": current_user.get('full_name'),
        "age": current_user.get('age'),
        "is_active": current_user.get('is_active', True)
    }

# # GET эндпоинты для проверки
# @app.get("/users/{user_id}")
# def get_user(user_id: int):
#     if user_id not in users_db:
#         raise HTTPException(status_code=404, detail="Пользователь не найден")
    
#     user = users_db[user_id]
#     return {
#         "id": user_id,
#         "username": user['username'],
#         "email": user['email'],
#         "full_name": user.get('full_name'),
#         "age": user.get('age'),
#         "is_active": user.get('is_active', True)
#     }

# @app.get("/users")
# def get_all_users():
#     result = []
#     for user_id, user in users_db.items():
#         result.append({
#             "id": user_id,
#             "username": user['username'],
#             "email": user['email'],
#             "full_name": user.get('full_name'),
#             "age": user.get('age'),
#             "is_active": user.get('is_active', True)
#         })
#     return result