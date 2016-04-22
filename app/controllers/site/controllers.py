"""
    This contains the controllers for the main site
"""

from flask import (Blueprint)

main_controller = Blueprint('main')

@app.route('/')
def index():
    return render_template('main.html')
