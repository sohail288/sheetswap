""" Controllers for trade """
from datetime import datetime

from flask import (request,
                   session,
                   g,
                   url_for,
                    flash,
                   redirect,
                    render_template,
)

from models import Trade, Item, User

from . import trade_routes

@trade_routes.route('/<int:trade_id>')
def main(trade_id):
    """ this is the main controller for a trade.  It is the basis of a trade where two users can see what's going on
    :param trade_id: This is the id of the trade
    :return: returns a response object
    """
    trade = Trade.query.filter_by(id=trade_id).one_or_none()

    if not (g.user.id == trade.user_from_id or g.user.id == trade.user_to_id):
        flash('You are not a part of that trade')
        return redirect('main.dashboard')

    if not trade:
        flash("That trade doesn't exist or you are not a part of it")
        return redirect('main.dashboard')

    user_from = User.query.filter_by(id=trade.user_from_id).one()
    user_to   = User.query.filter_by(id=trade.user_to_id).one()

    return render_template('trades/main.html', trade=trade,
                           user_from=user_from,
                           user_to=user_to)


@trade_routes.route('/request/<int:requested_item_id>', methods=['POST'])
def request_trade(requested_item_id):
    requested_item = Item.query.filter_by(id=requested_item_id).one()
    to_user_id = requested_item.user.id
    from_user_id = g.user.id

    new_trade = Trade(user_from_id = from_user_id,
                      user_to_id = to_user_id,
                      item_to=requested_item)
    g.db.add(new_trade)
    g.db.commit()
    flash("Requested a trade for {} with {}".format(requested_item.sheetmusic.title,
                                                    requested_item.user.username),
          "success")
    return redirect(url_for('main.index'))

@trade_routes.route('/accept/<int:trade_id>', methods=['POST'])
def accept_trade(trade_id):
    trade = Trade.query.filter_by(id=trade_id).one()

    if trade.user_to_id != g.user.id:
        flash("Are you crazy!", 'error')
        return redirect("main.dashboard")

    else:
        session['TRADING'] = True
        session['trade_id'] = trade_id
        return redirect(url_for('.trading', from_user_id=trade.user_from_id))

@trade_routes.route('/reject/<int:trade_id>', methods=['POST'])
def reject_trade(trade_id):
    trade = Trade.query.filter_by(id=trade_id).one()
    from_user = User.query.filter_by(id=trade.user_from_id).one()

    if trade.user_to_id != g.user.id:
        return redirect("Are you crazy!", "error")
    else:
        trade.rejected = True
        trade.trade_fin_timestamp = datetime.now()
        trade.completed = True
        g.db.commit()

        flash("Rejected trade from {} for {}".format(from_user.username,
            trade.item_to.sheetmusic.title))
        return redirect(url_for('main.dashboard'))

@trade_routes.route('/trading', methods=['POST', 'GET'])
def trading():

    if request.method == 'POST':
        from_item_id, trade_id = [int(tok) for tok in request.form.get('trade_item').split()]
        trade = g.db.query(Trade).filter_by(id=trade_id).one()
        from_item = Item.query.filter_by(id=from_item_id).one()

        trade.item_from = from_item
        trade.completed = True
        trade.trade_fin_timestamp = datetime.now()
        trade.item_to.available =  False
        trade.item_from.available = False

        g.db.commit()

        flash("trade completed", "success")
        return redirect(url_for('.main', trade_id=trade.id))

    if not session.get('TRADING', False):
        flash("Your trading session expired.  Try it again.")
        return redirect(url_for('main.dashboard'))

    from_user_id = int(request.args.get('from_user_id'))
    from_user = User.query.filter_by(id=from_user_id).one()
    items_to_trade_with = Item.query.filter_by(user_id=from_user_id).filter(Item.available == True).all()
    trading = session.pop('TRADING', None)
    trade_id = session.pop('trade_id', None)

    return render_template('trades/trading.html',
                           from_user=from_user,
                           items=items_to_trade_with,
                           trade_id=trade_id,
                           trading=trading)

#@trade_routes.route('/complete/<int:item_id>/<int:trade_id>')
#def complete(item_id, trade_id):





