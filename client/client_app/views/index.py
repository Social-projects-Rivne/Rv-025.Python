from flask import render_template

from client_app import app
from client_app.models.restaurant import Restaurant


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


@app.route('/restaurant/<int:restaurant_id>')
def show_restaurant(restaurant_id):
    restaurant_info = Restaurant\
        .query.filter(Restaurant.id == restaurant_id).first()
    return render_template('restaurant.html', restaurant_info=restaurant_info)
