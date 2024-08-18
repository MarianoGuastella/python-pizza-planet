import sys
import os

# Add the root directory of the project to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
import random
from faker import Faker
from app.plugins import db
from app import flask_app
from app.repositories.models import (
    Ingredient,
    Order,
    IngredientOrderDetail,
    BeverageOrderDetail,
    Size,
    Beverage,
)

fake = Faker()

ingredient_names = [
    "Tomato",
    "Cheese",
    "Pepperoni",
    "Mushroom",
    "Onion",
    "Olive",
    "Bacon",
    "Ham",
    "Pineapple",
    "Sausage",
]
beverage_names = [
    "Coke",
    "Pepsi",
    "Sprite",
    "Fanta",
    "Water",
    "Juice",
    "Tea",
    "Coffee",
    "Milkshake",
    "Lemonade",
]
size_names = ["Small", "Medium", "Large", "Extra Large", "Family"]


def create_fake_data():
    ingredients = []
    for _ in range(10):
        ingredient = Ingredient(
            name=random.choice(ingredient_names),
            price=round(random.uniform(0.5, 5.0), 2),
        )
        ingredients.append(ingredient)
        db.session.add(ingredient)

    beverages = []
    for _ in range(10):
        beverage = Beverage(
            name=random.choice(beverage_names), price=round(random.uniform(0.5, 5.0), 2)
        )
        beverages.append(beverage)
        db.session.add(beverage)

    sizes = []
    for _ in range(5):
        size = Size(
            name=random.choice(size_names), price=round(random.uniform(5.0, 20.0), 2)
        )
        sizes.append(size)
        db.session.add(size)
    db.session.commit()

    for _ in range(100):
        order = Order(
            client_name=fake.name(),
            client_dni=fake.ssn(),
            client_address=fake.address(),
            client_phone=fake.phone_number(),
            date=fake.date_this_year(),
            total_price=0.0,
            size_id=random.choice(sizes)._id,
        )
        db.session.add(order)
        db.session.flush()

        order_ingredients = random.sample(ingredients, random.randint(1, 5))
        for ingredient in order_ingredients:
            detail = IngredientOrderDetail(
                order_id=order._id,
                ingredient_id=ingredient._id,
                ingredient_price=ingredient.price,
            )
            db.session.add(detail)
            order.total_price += ingredient.price

        order_beverages = random.sample(beverages, random.randint(1, 3))
        for beverage in order_beverages:
            detail = BeverageOrderDetail(
                order_id=order._id,
                beverage_id=beverage._id,
                beverage_price=beverage.price,
            )
            db.session.add(detail)
            order.total_price += beverage.price

        db.session.commit()


if __name__ == "__main__":
    with flask_app.app_context():
        db.create_all()
        create_fake_data()
