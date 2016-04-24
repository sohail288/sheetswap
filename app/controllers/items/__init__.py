from flask import Blueprint

items_routes = Blueprint('items', __name__, url_prefix='/items')

from . import controllers