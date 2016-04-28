from flask import Blueprint

tests = Blueprint("testing", __name__, url_prefix='/testing')

from . import controllers