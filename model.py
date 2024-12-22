from faker import Faker
from app import db, Product, app  # Import your app and models
from flask_sqlalchemy import SQLAlchemy

# Faker generates random data
faker = Faker()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "your-secret-key"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


# Categories of products
categories = ["Electronics", "Clothing", "Books", "Home Appliances", "Toys"]

def add_products():
    with app.app_context():  # This is needed to interact with the database
        for _ in range(100):  # Add 100 products
            product = Product(
                name=f"{faker.word().capitalize()} {faker.word().capitalize()}",
                price=round(faker.random_number(digits=4) / 100, 2),
                stock=faker.random_int(min=1, max=100),
                category=faker.random_choices(elements=categories, length=1)[0],  # Ensure single category
            )
            db.session.add(product)  # Add to database
        db.session.commit()  # Save to the database
        print("Added 100 products!")

if __name__ == "__main__":
    add_products()
