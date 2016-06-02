"""
    Controllers for Items
"""

from uuid import uuid4
import os
import re

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
from app.decorators import user_is_logged_in, user_passes_test


def item_is_in_a_completed_trade(item):
    return any(t.completed for t in item.trades)


def user_owns_item():
    user = g.user
    item_id = request.view_args['item_id']
    return item_id in [item.id for item in user.items]


def item_is_visible():
    """ If item has been traded already or is unavailable then you cannot view it unless you own it"""
    user = g.user
    item_id = request.view_args['item_id']
    item = Item.query.filter_by(id=item_id).one()

    is_in_a_completed_trade = [t for t in item.trades if t.completed]

    if is_in_a_completed_trade or not item.available:
        user_is_trade_user = False
        if is_in_a_completed_trade:
            item_trade = is_in_a_completed_trade[0]
            trade_user = item_trade.user_from if user != item_trade.user_to else item_trade.user_to
            user_is_trade_user = user == trade_user
        return user == item.user or user_is_trade_user
    else:
        return True


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
@user_passes_test(item_is_visible)
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
@user_passes_test(user_owns_item)
@user_is_logged_in
def update(item_id):
    item = Item.query.filter_by(id=item_id).one_or_none()
    form = EditItemForm(request.form, item)
    if request.method == 'POST' and form.validate():
        # user should not be allowed to change an item if its in a trade already
        if item_is_in_a_completed_trade(item):
            flash("You cannot change an item that has already been traded", "error")
            return redirect(url_for('.index', item_id=item_id))

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
