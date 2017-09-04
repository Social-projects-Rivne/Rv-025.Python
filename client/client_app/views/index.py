from client_app import app, db
from client_app.forms import registration_form

from flask import flash, render_template, redirect, url_for, session, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length

from client_app.models.restaurant import Restaurant
from client_app.models.user import User


class LoginForm(FlaskForm):
    email = StringField(
        'email',
        validators=[InputRequired(), Email('Invalid Email')]
    )
    password = PasswordField(
        'password',
        validators=[InputRequired(), Length(min=8)]
    )


@app.route('/')
def index():
    form = LoginForm()
    return render_template('index.html', form=form)


@app.route('/restaurant')
def show_list_of_restaurants():
    """ Generates list of restaurants
    """

    list_of_restaurants = Restaurant\
        .query\
        .join(Restaurant.restaurant_type)\
        .filter(Restaurant.status == 0)\
        .order_by(Restaurant.name)\
        .all()
    return render_template(
        'list_of_restaurants.html', list_of_restaurants=list_of_restaurants)


@app.route('/profile')
def profile():
    """ Get logged user from DB query
    """

    user_id = session['logged_in']
    current_user = User.query.get(user_id)
    return render_template('profile.html', current_user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def do_admin_login():
    """Get login credentials.
    STATUS_BANNED = 2: banned user
    ROLE_USER = 3: user role
    """

    STATUS_BANNED = 2
    ROLE_USER = 3

    if request.method == 'POST':
        login_email = str(request.form['email'])
        logged_user = User.query.filter_by(email=login_email).first()

        if (logged_user
                and logged_user.role == ROLE_USER
                and logged_user.status != STATUS_BANNED):
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
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))

  
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = registration_form.RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        new_user = User(form.name.data, form.email.data,
                        form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Thanks for registering', 'succes')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

