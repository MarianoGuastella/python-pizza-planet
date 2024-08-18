from abc import ABC, abstractmethod
from sqlalchemy import func

from app.plugins import db
from app.repositories.models import Ingredient, IngredientOrderDetail, Order

MONTH_NAMES = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}


class ReportStrategy(ABC):
    @abstractmethod
    def generate(self):
        pass


class MostRequestedIngredientStrategy(ReportStrategy):
    def generate(self):
        most_requested_ingredient = (
            db.session.query(
                Ingredient.name,
                func.count(IngredientOrderDetail.ingredient_id).label("count"),
            )
            .join(Ingredient, Ingredient._id == IngredientOrderDetail.ingredient_id)
            .group_by(Ingredient.name)
            .order_by(func.count(IngredientOrderDetail.ingredient_id).desc())
            .first()
        )
        return {
            "name": most_requested_ingredient[0],
            "count": most_requested_ingredient[1],
        }


class MonthWithMostRevenueStrategy(ReportStrategy):
    def generate(self):
        month_revenue = (
            db.session.query(
                func.strftime("%Y-%m", Order.date).label("month"),
                func.sum(Order.total_price).label("revenue"),
            )
            .group_by("month")
            .order_by(func.sum(Order.total_price).desc())
            .first()
        )
        if month_revenue:
            year_month = month_revenue.month
            year, month = year_month.split("-")
            month_name = MONTH_NAMES[int(month)]
            return {"month": f"{month_name} {year}", "revenue": month_revenue.revenue}
        return {"month": None, "revenue": None}


class TopCustomersStrategy(ReportStrategy):
    def generate(self):
        top_customers = (
            db.session.query(
                Order.client_name, func.count(Order._id).label("orders_count")
            )
            .group_by(Order.client_name)
            .order_by(func.count(Order._id).desc())
            .limit(3)
            .all()
        )
        return [
            {"client_name": customer[0], "orders_count": customer[1]}
            for customer in top_customers
        ]
