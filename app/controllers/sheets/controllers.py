"""
The controllers for sheets
"""

from flask import (Blueprint,
                   g,
                   flash,
                   request,
                   render_template,
                   abort,
                    url_for,
                   redirect)

from app import TEMPLATE_DIR
from . import sheets_routes

from models.sheets import (Sheetmusic, Genre, Instrument)
from models.sheets.forms import SheetMusicForm





@sheets_routes.route('/')
def main():
    sheets = g.db.query(Sheetmusic).all()

    return render_template('sheets/index.html', sheets = sheets)


@sheets_routes.route('/create', methods=['POST', 'GET'])
def create():
    form = SheetMusicForm(request.form)

    if request.method == 'POST' and form.validate():
        sheet_music = Sheetmusic()

        for field in ['title', 'composer', 'time_signature', 'cover', 'arranged_by']:
            setattr(sheet_music, field, form[field].data if form[field].data else None)

        # add the genres
        sheet_music.parse_tags(form.genre.data, Genre, 'genre_tags')

        # add the instruments
        sheet_music.parse_tags(form.instrumentation.data, Instrument, 'instrumentation')

        g.db.add(sheet_music)
        g.db.commit()

        flash("Added {}".format(form.title))
        return redirect(url_for('.main'))

    return render_template('sheets/create_sheet_music.html', form=form)


@sheets_routes.route('/<int:sheet_music_id>', methods=['GET'])
def index(sheet_music_id):
    sheet_music = g.db.query(Sheetmusic).filter_by(id = sheet_music_id).first()

    return render_template('sheets/sheet_music_page.html', sheet_music=sheet_music)


