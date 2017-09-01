from flask import flash, request, redirect, render_template, url_for

from client_app import app, db
from client_app.forms import registration_form
from client_app.models.restaurant import Restaurant
from client_app.models.user import User


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/restaurant')
def show_list_of_restaurants():
    list_of_restaurants = Restaurant\
        .query\
        .join(Restaurant.restaurant_type)\
        .filter(Restaurant.status == 0)\
        .order_by(Restaurant.name)\
        .all()
    return render_template(
        'list_of_restaurants.html', list_of_restaurants=list_of_restaurants)


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
