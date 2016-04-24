from flask import (request,
                   redirect,
                   flash,
                   g,
                   session,
                   render_template,
                   url_for)

from sqlalchemy.orm.exc import NoResultFound

from models.auth.forms import RegistrationForm, LoginForm
from models.auth import User, Address

from . import auth_routes

TEST_USER = 'johnnytest@email.com'
TEST_PASSWORD = 'johnnytest'


@auth_routes.route('/')
def index():
    return redirect(url_for('main.index'))

@auth_routes.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('logged out')
    return redirect(url_for('main.index'))

@auth_routes.route('/login', methods=['POST', 'GET'])
def login():
    if session.get('logged_in'):
        flash("Already Logged In")
        return redirect(url_for('main.index'))


    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        user = g.db.query(User).filter_by(email=form.email.data).one_or_none()
        if user and user.verify_password(form.password.data):
            session['logged_in'] = True
            session['current_user_id'] = user.id
            return redirect(url_for('main.index'))
        else:
            flash('That password and user combination may be wrong')

    return render_template('auth/login.html', form=form)

@auth_routes.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm(request.form)

    if request.method == 'POST' and form.validate():
        user = User()
        form.populate_obj(user)
        g.db.add(user)
        g.db.commit()

        session['current_user_id'] = user.id
        session['logged_in'] = True
        flash("Thanks for registering")
        return redirect(url_for('main.index'))

    return render_template('auth/registration.html', form=form)




