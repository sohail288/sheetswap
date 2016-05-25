"""
The controllers for sheets
"""
from os.path import splitext

from flask import (g,
                   flash,
                   request,
                   render_template,
                   url_for,
                   send_from_directory,
                   redirect)
from sqlalchemy.sql import text

from . import sheets_routes
from models.sheets import Sheetmusic, Genre, Instrument
from models.sheets.forms import SheetMusicForm
from app.decorators import user_is_logged_in
from app.tasks import save_image


def populate_sheet_music(form, sheet_music):
    for field in ['title', 'composer', 'time_signature', 'cover', 'arranged_by']:
        setattr(sheet_music, field, form[field].data if form[field].data else None)

    # add the genres
    sheet_music.parse_tags(form.genre.data, Genre, 'genre_tags')

    # add the instruments
    sheet_music.parse_tags(form.instrumentation.data, Instrument, 'instrumentation')


@sheets_routes.route('/')
def main():
    sheets = g.db.query(Sheetmusic).all()

    return render_template('sheets/index.html', sheets=sheets)


@sheets_routes.route('/create', methods=['POST', 'GET'])
@user_is_logged_in
def create():
    form = SheetMusicForm(request.form)
    if request.method == 'POST' and form.validate():
        sheetmusic = Sheetmusic()
        populate_sheet_music(form, sheetmusic)
        g.db.add(sheetmusic)
        g.db.commit()

        if request.files.get('cover'):
            ext = splitext(request.files['cover'].filename)[-1]
            filename = "".join(sheetmusic.title.split(" ")) + '_' + str(sheetmusic.id) + '_cover' + ext
            save_image(request.files['cover'], filename)
            sheetmusic.cover = filename
            g.db.commit()

        if form.creating_item.data:
            flash("{} has been added to the database. Enter your copy's details below".format(sheetmusic.title),
                  "success")
            return redirect(url_for('items.create', sheetmusic_id=sheetmusic.id))
        else:
            flash("Added {}".format(form.title))
            return redirect(url_for('.main'))

    form.creating_item.data = int(request.args.get("creating_item", 0))
    return render_template('sheets/create_sheet_music.html', form=form)


@sheets_routes.route('/<int:sheet_music_id>', methods=['GET'])
def index(sheet_music_id):
    sheet_music = g.db.query(Sheetmusic).filter_by(id=sheet_music_id).first()
    if g.user:
        requested_items = [trade[0] for trade in
                           g.db.execute(text("SELECT item_to_id FROM trades WHERE trades.user_from_id=:x")
                                        .params(x=g.user.id)).fetchall()]
    else:
        requested_items = []
    items_available = [item for item in sheet_music.items
                       if not g.user or item.user_id != g.user.id and
                       item.id not in requested_items and item.available]

    return render_template('sheets/sheet_music_page.html',
                           sheet_music=sheet_music,
                           items=items_available)
