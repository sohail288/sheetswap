"""
    This contains the controllers for the main site
"""

from sqlalchemy import and_

from flask import (Blueprint,
                   g,
                   request,
                   render_template,
                   redirect,
                   flash,
                   url_for,
                   session,
                   abort)

from . import main_routes
from models.sheets import Sheetmusic
from models import Trade, Item

from app.decorators import user_is_logged_in


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

@main_routes.route('/dashboard')
@user_is_logged_in
def dashboard():
    trades_for_user = g.db.query(Trade)\
        .filter(Trade.user_to_id == g.user.id)\
        .filter(Trade.completed == False)\
        .filter(Trade.rejected == False)\
        .all()
    completed_trades = g.db.query(Trade)\
        .filter(Trade.user_to_id == g.user.id)\
        .filter(Trade.completed == True)\
        .filter(Trade.rejected == False)\
        .all()
    rejected_trades  = g.db.query(Trade)\
        .filter(Trade.user_to_id == g.user.id)\
        .filter(Trade.rejected == True)\
        .all()

    return render_template('dashboard/index.html',
                           trades=trades_for_user,
                           completed_trades=completed_trades,
                           rejected_trades=rejected_trades)
