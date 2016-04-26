from flask import Blueprint

trade_routes = Blueprint('trades', __name__, url_prefix='/trades')

from . import controllers