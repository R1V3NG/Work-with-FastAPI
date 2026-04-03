from fastapi import FastAPI
from typing import Annotated
from models import *
from db import SessionDep

from fastapi import FastAPI, HTTPException, Query
from sqlmodel import select

app = FastAPI()

@app.get("/product", response_model=list[Product])
def GetProducts(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Product]:
    products = session.exec(select(Product).offset(offset).limit(limit)).all()
    return products

@app.get("/product/{product_id}", response_model=Product)
def GetProduct(product_id: int, session: SessionDep) -> Product:
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="product not found")
    return product

@app.post("/product", response_model=CreateProduct)
def PostProduct(product: CreateProduct, session: SessionDep):
    new_product = Product(name= product.name, 
                          description=product.description, 
                          price=product.price, 
                          category_id=product.category_id)
    session.add(new_product)
    session.commit()
    return product

@app.delete("/product")
def DeleteProduct(product_id: int, session: SessionDep):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    session.delete(product)
    session.commit()
    return {"status": True}

@app.patch("/product", response_model=CreateProduct)
def PatchProduct(product: UpdateProduct, session: SessionDep):
    old_product = session.get(Product, product.id)
    if not old_product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.name != None:
        old_product.name = product.name

    if product.description != None:
        old_product.description = product.description

    if product.price != None:
        old_product.price = product.price

    if product.category_id != None:
        old_product.category_id = product.category_id
    
    session.add(old_product)
    session.commit()
    session.refresh(old_product)
    return old_product

@app.get("/category", response_model=list[Category])
def GetCategories(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Category]:
    categories = session.exec(select(Category).offset(offset).limit(limit)).all()
    return categories

@app.get("/category/{category_id}", response_model=Category)
def GetCategory(category_id: int, session: SessionDep) -> Category:
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="category not found")
    return category

@app.post("/category", response_model=CreateCategory)
def PostCategory(category: CreateCategory, session: SessionDep):
    new_category = Category(name=category.name)
    session.add(new_category)
    session.commit()
    return category

@app.delete("/category")
def DeleteCategory(category_id: int, session: SessionDep):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    session.delete(category)
    session.commit()
    return {"status": True}

@app.patch("/category", response_model=CreateCategory)
def PatchCategory(category: UpdateCategory, session: SessionDep):  
    old_category = session.get(Category, category.id)
    if not old_category:
        raise HTTPException(status_code=404, detail="Category not found")

    if category.name != None:
        old_category.name = category.name
    
    session.add(old_category)
    session.commit()
    session.refresh(old_category)
    return old_category