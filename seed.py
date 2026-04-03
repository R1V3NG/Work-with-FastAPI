import db, models

db.create_db_and_tables()

with db.Session(db.engine) as s:
    s.add(models.Hero(name="My hero", secret_name="hero"))
    s.commit()