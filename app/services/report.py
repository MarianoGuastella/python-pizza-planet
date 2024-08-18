from flask import Blueprint, jsonify
from app.common.http_methods import GET
from app.controllers.report import ReportController
from app.repositories.reports.report import (
    MostRequestedIngredientStrategy,
    MonthWithMostRevenueStrategy,
    TopCustomersStrategy,
)

report = Blueprint("report", __name__)


@report.route("/", methods=GET)
def get_report():
    report_controller = ReportController(MostRequestedIngredientStrategy())
    most_requested_ingredient = report_controller.generate_report()

    report_controller.set_strategy(MonthWithMostRevenueStrategy())
    month_with_most_revenue = report_controller.generate_report()

    report_controller.set_strategy(TopCustomersStrategy())
    top_customers = report_controller.generate_report()

    return jsonify(
        most_requested_ingredient=most_requested_ingredient,
        month_with_most_revenue=month_with_most_revenue,
        top_customers=top_customers,
    )
