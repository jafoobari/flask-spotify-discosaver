from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import config


app = Flask(__name__)
#Takes place of app.config.from_object(Config)
config.configure_app(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from dw_saver import routes, models