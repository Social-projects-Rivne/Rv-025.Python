from client_app import app, db
from conf_parser import config as db_config

PSQL_PARAMS = db_config()
app.config.from_object('config.DevelopmentConfig')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = ('postgresql://%(user)s:'
                                         '%(password)s@%(host)s:'
                                         '%(port)s/%(name)s'
                                         % PSQL_PARAMS)

# fix for reload jinja templates, no need to restart server
app.jinja_env.auto_reload = True

db.init_app(app)

app.run()
