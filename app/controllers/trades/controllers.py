""" Controllers for trade """
from datetime import datetime

from flask import (request,
                   session,
                   g,
                   url_for,
                   flash,
                   redirect,
                   render_template)

from models import Trade, Item, User

from . import trade_routes

from app.decorators import user_is_part_of_trade, user_is_logged_in, user_passes_test
from util.emailing import send_mail


@trade_routes.before_request
@user_is_logged_in
def before_request():
    pass


@trade_routes.route('/<int:trade_id>')
@user_is_part_of_trade()
def main(trade_id):
    """ this is the main controller for a trade.  It is the basis of a trade where two users can see what's going on
    :param trade_id: This is the id of the trade
    :return: returns a response object
    """
    trade = Trade.query.filter_by(id=trade_id).one_or_none()

    if not trade:
        flash("That trade doesn't exist", 'error')
        return redirect('main.dashboard')

    user_from = trade.user_from
    user_to = trade.user_to

    return render_template('trades/main.html', trade=trade,
                           user_from=user_from,
                           user_to=user_to)


def user_doesnt_already_have_an_active_trade_with_item():
    item_id = int(request.url.rsplit('/', 1)[-1])
    if item_id in [trade.item_to_id for trade in g.user.trades]:
        return False
    return True


@trade_routes.route('/request/<int:requested_item_id>', methods=['POST'])
@user_passes_test(test_func=user_doesnt_already_have_an_active_trade_with_item)
@user_passes_test(test_func=lambda: len(g.user.addresses) > 0,
                  flashed_message="add an address before trading",
                  view_path_to_redirect_to='auth.add_address')
def request_trade(requested_item_id):
    requested_item = Item.query.filter_by(id=requested_item_id).one()
    to_user_id = requested_item.user.id
    from_user_id = g.user.id

    new_trade = Trade(user_from_id=from_user_id,
                      user_to_id=to_user_id,
                      item_to=requested_item)
    g.db.add(new_trade)
    g.db.commit()

    send_mail.delay(requested_item.user.email, 'Got a new request!', 'emails/trade_requested',
                    user_from=g.user.username,
                    title=requested_item.sheetmusic.title)

    flash("Requested a trade for {} with {}".format(requested_item.sheetmusic.title,
                                                    requested_item.user.username),
          "success")
    return redirect(url_for('main.index'))


@trade_routes.route('/accept/<int:trade_id>', methods=['POST'])
@user_is_part_of_trade()
def accept_trade(trade_id):
    """
    :param trade_id: the id for the trade
    :return: redirect object.
    If trade is accepted, a trading session is initialized
    """
    trade = Trade.query.filter_by(id=trade_id).one()
    session['TRADING'] = True
    session['trade_id'] = trade_id
    return redirect(url_for('.trading', from_user_id=trade.user_from_id))


@trade_routes.route('/reject/<int:trade_id>', methods=['POST'])
@user_is_part_of_trade()
def reject_trade(trade_id):
    trade = Trade.query.filter_by(id=trade_id).one()
    from_user = User.query.filter_by(id=trade.user_from_id).one()

    trade.rejected = True
    trade.trade_fin_timestamp = datetime.now()
    trade.completed = True
    g.db.commit()

    flash("Rejected trade from {} for {}".format(from_user.username,
                                                 trade.item_to.sheetmusic.title), 'success')
    return redirect(url_for('main.dashboard'))


@trade_routes.route('/trading', methods=['POST', 'GET'])
def trading():

    if request.method == 'POST':
        # get the from item id and trade id from the form
        from_item_id, trade_id = [int(tok) for tok in request.form.get('trade_item').split()]
        trade = g.db.query(Trade).filter_by(id=trade_id).one()
        from_item = Item.query.filter_by(id=from_item_id).one()

        trade.item_from = from_item
        trade.completed = True
        trade.trade_fin_timestamp = datetime.now()
        trade.item_to.available = False
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
