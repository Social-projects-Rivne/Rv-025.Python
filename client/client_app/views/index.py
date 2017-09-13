from flask import flash, render_template, redirect, url_for, session, request

from functools import wraps

from passlib.hash import pbkdf2_sha256

from client_app import app, db
from client_app.forms import registration_form
from client_app.forms import edit_form

from client_app.models.dish import Dish, DishCategory
from client_app.models.login import LoginForm
from client_app.models.restaurant import Restaurant
from client_app.models.user import User


def is_logged(f):
    """
    Is_Logged decorator.
    Put it in route you need to use only for logged user.
    Example:
        @app.route('/home')
        @is_logged
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


@app.errorhandler(404)
def page_not_found(e):
    """
    Catch all 404 erorrs
    """

    return render_template('404.html'), 404


@app.route('/')
def index():
    login_form = LoginForm()
    return render_template('index.html', login_form=login_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Get login credentials.
    STATUS_BANNED = 2: banned user
    ROLE_USER = 3: user role
    """

    STATUS_DELETED = 1
    STATUS_BANNED = 2
    ROLE_USER = 3

    if request.method == 'POST':
        login_email = str(request.form['email'])
        logged_user = User.query.filter_by(email=login_email).first()

        if (logged_user
                and logged_user.role == ROLE_USER
                and logged_user.status != STATUS_BANNED
                and logged_user.status != STATUS_DELETED):
            session['logged_in'] = logged_user.id
            session['name'] = logged_user.name
            redirect(url_for('profile'))
        elif logged_user and logged_user.status == STATUS_BANNED:
            flash('your account has been banned', 'danger')
            return logout()
        else:
            flash('wrong login/password!', 'danger')
    else:
        return redirect(url_for('index'))
    return redirect(url_for('index'))


@app.route("/logout")
@is_logged
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))


@app.route('/profile')
def profile():
    """ Get logged user from DB query
    """

    user_id = session['logged_in']
    current_user = User.query.get(user_id)
    return render_template('profile.html', current_user=current_user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if not session.get('logged_in'):
        form = registration_form.RegistrationForm(request.form)
        if request.method == 'POST' and form.validate():
            new_user = User(form.name.data, form.email.data,
                            form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Thanks for registering', 'success')
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/edit', methods=['GET', 'POST'])
@is_logged
def edit():
    user_id = session['logged_in']
    current_user = User.query.get(user_id)
    edit_user = edit_form.EditForm(request.form, obj=current_user)

    if request.method == 'POST' and edit_user.validate():
        if edit_user.password.data:
            current_user.password = pbkdf2_sha256.hash(edit_user.password.data)
        current_user.name = edit_user.name.data
        current_user.phone = edit_user.phone.data
        db.session.add(current_user)
        db.session.commit()
        session['name'] = current_user.name
        flash('Your changes have been saved.', 'success')
        return redirect(url_for('profile'))
    return render_template('edit_user.html', edit_user=edit_user)


@app.route('/restaurant')
def show_list_of_restaurants():
    """ Generates list of restaurants
    """

    form = registration_form.RegistrationForm(request.form)
    list_of_restaurants = Restaurant\
        .query\
        .filter(Restaurant.status == 0)\
        .order_by(Restaurant.name)\
        .all()
    return render_template('list_of_restaurants.html',
                           list_of_restaurants=list_of_restaurants,
                           form=form)


@app.route('/restaurant/<int:restaurant_id>')
def show_restaurant(restaurant_id):
    """ Show restaurant info page
    """

    form = registration_form.RegistrationForm(request.form)
    restaurant_info = Restaurant\
        .query\
        .filter(Restaurant.id == restaurant_id)\
        .first()
    menu = Dish\
        .query\
        .join(Dish.category_id__join)\
        .filter(
                Dish.available.is_(True),
                Dish.restaurant_id == restaurant_info.id) \
        .order_by(DishCategory.order)\
        .all()
    return render_template('restaurant.html',
                           restaurant_info=restaurant_info,
                           menu=menu,
                           form=form)
