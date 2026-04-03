import json
import db
import models

db.create_db_and_tables()

with open('products.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

with db.Session(db.engine) as s:
    categories_dict = {}
    
    for category_name in data['categories']:
        category = models.Category(name=category_name)
        s.add(category)
        categories_dict[category_name] = category
    
    s.commit()
    
    for product_data in data['products']:
        category = categories_dict.get(product_data['category'])
        
        if category:
            product = models.Product(
                name=product_data['name'],
                description=product_data.get('description', ''),
                price=product_data['price'],
                category=category
            )
            s.add(product)
    s.commit()