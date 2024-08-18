import logging
import sys
import os

# Add the root directory of the project to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from app import flask_app
from app.plugins import db
from app.repositories.models import (
    Beverage,
    Ingredient,
    Order,
    IngredientOrderDetail,
    BeverageOrderDetail,
    Size,
)

logging.basicConfig(level=logging.INFO)


def clean_database():
    """Deletes all records from specific tables in the database."""
    try:
        IngredientOrderDetail.query.delete()
        BeverageOrderDetail.query.delete()
        Order.query.delete()
        Ingredient.query.delete()
        Beverage.query.delete()
        Size.query.delete()

        db.session.commit()
        logging.info("Database cleaned successfully.")
    except Exception as e:
        logging.error(f"An error occurred while cleaning the database: {e}")
        db.session.rollback()


if __name__ == "__main__":
    with flask_app.app_context():
        confirm = input(
            "Are you sure you want to clean the database? This action cannot be undone. Type 'yes' to confirm: "
        )
        if confirm.lower() == "yes":
            clean_database()
        else:
            logging.info("Database cleaning canceled.")