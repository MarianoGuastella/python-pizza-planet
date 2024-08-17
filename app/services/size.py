from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, request

from ..controllers import SizeController
from ..services.base import BaseService

size = Blueprint('size', __name__)
size_service = BaseService(SizeController)

@size.route('/', methods=POST)
def create_size():
    return size_service.create(request.json)

@size.route("/<int:_id>", methods=PUT)
def update_size(_id: int):
    return size_service.update(_id, request.json)

@size.route("/<int:_id>", methods=GET)
def get_size_by_id(_id: int):
    return size_service.get_by_id(_id)

@size.route('/', methods=GET)
def get_sizes():
    return size_service.get_all()
