"""
    Controllers for Items
"""

from uuid import uuid4
import os

from flask import (g,
                   request,
                   redirect,
                   url_for,
                   flash,
                   send_from_directory,
                   render_template)

from werkzeug.utils import secure_filename
from PIL import Image

from . import items_routes
from app.tasks import save_image
from models import Item, Sheetmusic, ItemImage
from models.items.forms import CreateItemForm, EditItemForm
from models.sheets.forms import SheetMusicForm
from app.decorators import user_is_logged_in


@items_routes.route('/')
def main():
    items = g.db.query(Item).filter(Item.available == True).all()
    return render_template('items/index.html', items=items)


@items_routes.route('/create', methods=['POST', 'GET'])
@user_is_logged_in
def create():
    form = CreateItemForm(request.form)
    if request.method == 'POST' and form.validate():
        sheetmusic_id = form.sheetmusic_id.data
        sheetmusic = Sheetmusic.query.filter_by(id=sheetmusic_id).one()
        new_item = Item()
        form.populate_obj(new_item)

        new_item.user_id = g.user.id

        g.db.add(new_item)
        g.db.commit()

        for file in request.files.getlist('images'):
            if file:
                ext = file.filename.rsplit('.', 1)[-1]
                filename = g.user.username + '_' + str(uuid4()) + '.' + ext
                image = ItemImage(filename)
                save_image(file, filename)
                new_item._images.append(image)
        g.db.commit()

        flash("You just made a new item!", "success")
        return redirect(url_for('items.index', item_id=new_item.id))

    sheetmusic_id = int(request.args.get('sheetmusic_id', 0))
    if sheetmusic_id:
        form.sheetmusic_id.data = sheetmusic_id
    return render_template('items/create_item.html', form=form)


@items_routes.route('/<int:item_id>')
def index(item_id):
    item = Item.query.filter_by(id=item_id).one_or_none()
    if item is None:
        flash('That item does not exist!')
        if g.user is None:
            return redirect(url_for('main.index'))
        else:
            return redirect(url_for('main.dashboard'))
    return render_template('items/view_item.html', item=item)


@items_routes.route('/<int:item_id>/update', methods=['POST', 'GET'])
@user_is_logged_in
def update(item_id):
    item = Item.query.filter_by(id=item_id).one_or_none()
    form = EditItemForm(request.form, item)
    if request.method == 'POST' and form.validate():
        form.populate_obj(item)
        g.db.commit()

        for file in request.files.getlist('images'):
            if file:
                ext = file.filename.rsplit('.', 1)[-1]
                filename = g.user.username + '_' + str(uuid4()) + '.' + ext
                image = ItemImage(filename)
                save_image(file, filename)
                item._images.append(image)
        g.db.commit()
        flash('item updated', 'success')
        return redirect(url_for('.index', item_id=item_id))
    return render_template('items/update_item.html', form=form, item_id=item_id)


@items_routes.route('/<int:item_id>/remove', methods=['POST'])
@user_is_logged_in
def remove(item_id):
    item = Item.query.filter_by(id=item_id).one_or_none()

    if g.user.id == item.user.id \
            and request.method == 'POST'\
            and not item.trades:
        g.db.delete(item)
        g.db.commit()
        flash('item removed', 'success')
        return redirect(url_for('main.dashboard'))
    flash('Cannot do that', 'error')
    return redirect(url_for('main.dashboard'))

