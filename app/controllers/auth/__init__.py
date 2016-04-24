from flask import Blueprint

auth_routes = Blueprint('auth', __name__, url_prefix='/auth')

from .controllers import *