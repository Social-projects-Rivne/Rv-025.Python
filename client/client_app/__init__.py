from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from jinja2 import environmentfilter
from itertools import groupby
from jinja2.filters import make_attrgetter, _GroupTuple


app = Flask(__name__)
Bootstrap(app)
db = SQLAlchemy()


# Custom Filter
# http://jinja.pocoo.org/docs/dev/api/#custom-filters
@environmentfilter
def do_not_sorted_groupby(environment, value, attribute):
    expr = make_attrgetter(environment, attribute)
    return [_GroupTuple(key, list(values)) for key, values
            in groupby(value, expr)]

app.jinja_env.filters['not_sorted_groupby'] = do_not_sorted_groupby


from client_app.views import index
