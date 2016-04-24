"""
    This contains the controllers for the main site
"""

from flask import (Blueprint,
                   g,
                   request,
                   render_template,
                   redirect,
                   flash,
                   url_for,
                   abort)

from . import main_routes
from app.db import db_session
from models.sheets import Sheetmusic




@main_routes.route('/')
def index():
    return render_template('main.html')


@main_routes.route('/results')
def search_results():
    q = request.args.get('q', None)
    if q:
        results = g.db.query(Sheetmusic).filter(Sheetmusic.title.like('%{}%'.format(q))).all()
        return render_template('search_results.html', results=results, q = q)
    flash('Need to search for something', 'error')
    return redirect(url_for('.index'))

