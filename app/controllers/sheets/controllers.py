"""
The controllers for sheets
"""

from flask import (g,
                   flash,
                   request,
                   render_template,
                    url_for,
                   redirect)

from . import sheets_routes

from models.sheets import (Sheetmusic, Genre, Instrument)
from models.sheets.forms import SheetMusicForm


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

    return render_template('sheets/index.html', sheets = sheets)


@sheets_routes.route('/create', methods=['POST', 'GET'])
def create():
    form = SheetMusicForm(request.form)
    if request.method == 'POST' and form.validate():
        sheetmusic = Sheetmusic()
        populate_sheet_music(form, sheetmusic)
        g.db.add(sheetmusic)
        g.db.commit()

        if form.creating_item.data:
            flash("{} has been added to the database. Enter your copy's details below".format(sheetmusic.title),
                  "success")
            return redirect(url_for('items.create', sheetmusic_id = sheetmusic.id))

        else:
            flash("Added {}".format(form.title))
            return redirect(url_for('.main'))


    form.creating_item.data = int(request.args.get("creating_item", 0))

    return render_template('sheets/create_sheet_music.html', form=form)


@sheets_routes.route('/<int:sheet_music_id>', methods=['GET'])
def index(sheet_music_id):
    sheet_music = g.db.query(Sheetmusic).filter_by(id = sheet_music_id).first()
    items_available = [item for item in sheet_music.items
                       if not g.user or item.user_id != g.user.id]

    return render_template('sheets/sheet_music_page.html',
                           sheet_music=sheet_music,
                           items = items_available)


