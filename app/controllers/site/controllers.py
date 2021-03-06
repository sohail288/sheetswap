"""
    This contains the controllers for the main site
"""

from sqlalchemy import and_, desc

from flask import (Blueprint,
                   g,
                   request,
                   render_template,
                   redirect,
                   flash,
                   url_for,
                   session,
                   send_from_directory,
                   abort)

from . import main_routes
from models.sheets import Sheetmusic
from models import Trade, Item

from app.decorators import user_is_logged_in
from app.tasks import get_thumbnail_filename
from config import get_env_config


app_settings = get_env_config()


@main_routes.route('/')
def index():
    suggested_sheetmusic = set([i.sheetmusic for i in Item.query.all() if i.available])
    suggested_sheetmusic = sorted(suggested_sheetmusic, key=lambda i: -1*i.id)[:4]
    return render_template('main.html', suggested_sheetmusic=suggested_sheetmusic)


@main_routes.route('/results')
def search_results():
    q = request.args.get('q', None)
    if q:
        q_cleaned = q.strip().lower()
        results = g.db.query(Sheetmusic).filter(Sheetmusic.title.ilike('%{}%'.format(q_cleaned))).all()
        return render_template('search_results.html', results=results, q=q)
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
    rejected_trades = g.db.query(Trade)\
        .filter(Trade.user_to_id == g.user.id)\
        .filter(Trade.rejected == True)\
        .all()
    trades_requested = g.db.query(Trade)\
        .filter(Trade.user_from_id == g.user.id)\
        .all()

    return render_template('dashboard/index.html',
                           trades=trades_for_user,
                           completed_trades=completed_trades,
                           trades_requested =trades_requested,
                           rejected_trades=rejected_trades)


@main_routes.route('/images/<string:filename>')
def get_image(filename):
    return send_from_directory(app_settings.UPLOAD_FOLDER, filename)


@main_routes.route('/images/thumbnail/<string:filename>')
def get_thumbnail(filename):
    thumbnail = get_thumbnail_filename(filename)
    return send_from_directory(app_settings.UPLOAD_FOLDER, thumbnail)
