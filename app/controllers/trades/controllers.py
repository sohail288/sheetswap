""" Controllers for trade """
from flask import (request,
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

    return render_template('trades/main.html', trade=trade)


