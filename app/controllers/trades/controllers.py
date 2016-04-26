""" Controllers for trade """
from flask import (request,
                   g,
                   url_for,
                   redirect,
                    render_template,
)

from . import trade_routes

@trade_routes.route('/<string:token>')
def main(token):
    """ this is the main controller for a trade.  It is the basis of a trade where two users can see what's going on
    :param token: This token is a unique trade identifier
    :return: returns a response object
    """

    from_user = dict(sheet_music='this one')
    to_user = dict(sheet_music='that one')

    return render_template('trades/main.html', from_user = from_user, to_user = to_user)


