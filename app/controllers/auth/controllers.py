from flask import (request,
                   redirect,
                   flash,
                   g,
                   session,
                   render_template,
                   url_for)

from sqlalchemy.orm.exc import NoResultFound

from models.auth.forms import RegistrationForm, LoginForm, AddressForm
from models.auth import User, Address
from app.decorators import user_is_logged_in

from . import auth_routes

TEST_USER = 'johnnytest@email.com'
TEST_PASSWORD = 'johnnytest'


@auth_routes.route('/')
def index():
    return redirect(url_for('main.index'))


@auth_routes.route('/logout')
def logout():
    if session.get('logged_in'):
        session.pop('logged_in', None)
        session.pop('current_user_id', None)
        flash('logged out', 'success')
    return redirect(url_for('main.index'))


@auth_routes.route('/login', methods=['POST', 'GET'])
def login():
    if session.get('logged_in'):
        flash("Already Logged In", 'error')
        return redirect(url_for('main.index'))

    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        email = form.email.data
        user = g.db.query(User).filter_by(email=email.lower()).one_or_none()
        if user and user.verify_password(form.password.data):
            session['logged_in'] = True
            session['current_user_id'] = user.id
            flash('Welcome back {}!'.format(user.username), 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('That password and user combination may be wrong', 'error')

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
        flash("Thanks for registering", 'success')
        return redirect(url_for('main.index'))

    return render_template('auth/registration.html', form=form)


@auth_routes.route('/addresses')
@user_is_logged_in
def list_addresses():
    addresses = g.user.addresses
    return render_template('auth/address_list.html', addresses=addresses)


@auth_routes.route('/addresses/<int:address_id>/edit', methods=['POST', 'GET'])
@user_is_logged_in
def edit_address(address_id):
    address = Address.query.filter_by(id=address_id).one_or_none()
    form = AddressForm(request.form, address)

    if request.method == 'POST' and form.validate():
        form.populate_obj(address)
        g.db.commit()
        flash('Success!', 'success')
        return redirect(url_for('auth.list_addresses'))

    return render_template('auth/edit_address.html', form=form, address_id=address_id)


@auth_routes.route('/addresses/create', methods=['POST', 'GET'])
@user_is_logged_in
def add_address():
    form = AddressForm(request.form)

    if request.method == 'POST' and form.validate():
        address = Address()
        form.populate_obj(address)
        address.user = g.user
        g.db.add(address)
        g.db.commit()
        flash('Added new address')
        return redirect(url_for('auth.list_addresses'))

    return render_template('auth/add_address.html', form=form)
