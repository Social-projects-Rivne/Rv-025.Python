from client_app import app

from flask import Flask
from flask import flash, render_template, redirect, url_for, session, request

from client_app.models.restaurant import Restaurant
from client_app.models.user import User


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


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
    return render_template('profile.html', current_user=current_user )


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
        login_password = str(request.form['password'])
        logged_user = User.query.filter_by(email = login_email).first()

        if logged_user\
            and logged_user.role == ROLE_USER\
            and logged_user.status != STATUS_BANNED :
                session['logged_in'] = logged_user.id
                session['name'] = logged_user.name
                redirect('/profile')

        elif logged_user and logged_user.status == STATUS_BANNED:
            flash('your account has been banned', 'danger')
            return logout()
        else:
            flash('wrong login/password!','danger')
    else:
        return redirect('/')
    return redirect('/')


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect('/')
