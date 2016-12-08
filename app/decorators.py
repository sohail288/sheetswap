"""
    This module defines decorators that will be used in the controllers
"""

from flask import abort
from werkzeug.exceptions import abort, BadRequest
from functools import wraps
from flask import g, request, redirect, url_for, flash


# def owns_item()
""" This decorator makes sure that the item belongs to the user """


def user_is_part_of_trade(on_error=404):
    """ Checks to see if user is part of trade
    :param on_error: What to do on error
    :return: returns the decorator for decorative purposes
    """
    def decorator(func):
        @wraps(func)
        def wrapper(trade_id, *args, **kwargs):
            if trade_id not in g.user.trade_ids:
                flash('You are not a part of that trade', 'error')
                return redirect(url_for('main.dashboard'))
            return func(trade_id, *args, **kwargs)
        return wrapper
    return decorator


def user_is_logged_in(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        if g.user is None:
            flash('Must be logged in to access that', category='warning')
            return redirect(url_for('auth.login', next=request.path))
        return func(*args, **kwargs)

    return wrapper


def user_passes_test(test_func=lambda: False, view_path_to_redirect_to="", flashed_message="", **opts):
    def decorator(func):
        @user_is_logged_in
        @wraps(func)
        def wrapper(*args, **kwargs):
            if test_func():
                return func(*args, **kwargs)
            else:
                if view_path_to_redirect_to:
                    if flashed_message:
                        flash(flashed_message, category='error')
                    return redirect(url_for(view_path_to_redirect_to, next=request.path, **opts))
                abort(403)
        return wrapper
    return decorator
