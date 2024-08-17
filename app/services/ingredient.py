from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, request

from ..controllers import IngredientController
from ..services.base import BaseService

ingredient = Blueprint('ingredient', __name__)
ingredient_service = BaseService(IngredientController)


@ingredient.route('/', methods=POST)
def create_ingredient():
    return ingredient_service.create(request.json)


@ingredient.route("/<int:_id>", methods=PUT)
def update_ingredient(_id: int):
    return ingredient_service.update(_id, request.json)


@ingredient.route("/<int:_id>", methods=GET)
def get_ingredient_by_id(_id: int):
    return ingredient_service.get_by_id(_id)


@ingredient.route('/', methods=GET)
def get_ingredients():
    return ingredient_service.get_all()
