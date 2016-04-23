"""
    This contains the controllers for the main site
"""

from flask import (Blueprint, g, render_template, abort)
from . import main_routes
from app.db import db_session
from models.sheets import Sheetmusic



@main_routes.route('/')
def index():
    return render_template('main.html')




