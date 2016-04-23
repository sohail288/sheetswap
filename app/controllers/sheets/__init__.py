from flask import Blueprint

sheets_routes = Blueprint('sheets', __name__, url_prefix='/sheets')


from . import controllers
