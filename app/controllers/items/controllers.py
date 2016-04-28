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
from models.items.forms import CreateItemForm
from models.sheets.forms import SheetMusicForm


@items_routes.route('/')
def main():
    items = g.db.query(Item).filter(Item.available == True)
    return render_template('items/index.html', items=items)

@items_routes.route('/create', methods=['POST', 'GET'])
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

        flash("Your item is new item!", "success")
        return redirect(url_for('main.dashboard'))

    sheetmusic_id = int(request.args.get('sheetmusic_id', 0))
    if sheetmusic_id:
        form.sheetmusic_id.data = sheetmusic_id
    return render_template('items/create_item.html', form=form)

@items_routes.route('/<int:item_id>')
def index(item_id):
    return render_template('items/view_item.html', item_id=item_id)


@items_routes.route('/<int:item_id>/update', methods=['POST', 'GET'])
def update(item_id):
    posting = 'not posting'
    if request.method == 'POST':
        posting = 'posting'
        flash('item updated', 'success')
        redirect(url_for('.index', item_id=item_id))

    return render_template('items/update_item.html', posting=posting, item_id=item_id)

@items_routes.route('/<int:item_id>/remove', methods=['POST', 'GET'])
def remove(item_id):
    return render_template('items/remove_item.html')