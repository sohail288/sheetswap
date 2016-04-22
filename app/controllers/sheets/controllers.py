"""
The controllers for sheets
"""

from flask import (Blueprint)



sheets_controller = Blueprint('sheets', url_prefix='sheets')


@app.route('/sheet-test')
def sheet_test():
    return render_template('items/index.html')
