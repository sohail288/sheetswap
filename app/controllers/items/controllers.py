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
from models.items import Item


@items_routes.route('/')
def main():
    items = g.db.query(Item).filter(Item.available == True)
    return render_template('items/index.html', items=items)

@items_routes.route('/create', methods=['POST', 'GET'])
def create():
    posting = 'not posting'
    if request.method == 'POST':
        posting = 'posting'
        # redirect to item page

    return render_template('items/create_item.html', posting=posting)

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