"""
    Controllers for Items
"""

from flask import (g,
                   request,
                   redirect,
                   url_for,
                   flash,
                   render_template)

from . import items_routes
from models import Item, Sheetmusic
from models.items.forms import CreateItemForm, EditItemForm
from models.sheets.forms import SheetMusicForm

from app.decorators import user_is_logged_in


@items_routes.route('/')
def main():
    items = g.db.query(Item).filter(Item.available == True)
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
        flash('item updated', 'success')
        return redirect(url_for('.index', item_id=item_id))
    return render_template('items/update_item.html', form=form, item_id=item_id)

@items_routes.route('/<int:item_id>/remove', methods=['POST', 'GET'])
@user_is_logged_in
def remove(item_id):
    return render_template('items/remove_item.html')