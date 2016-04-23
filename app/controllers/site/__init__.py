from flask import Blueprint

main_routes = Blueprint('main', __name__)

from . import controllers