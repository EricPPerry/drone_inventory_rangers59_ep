#With this file, we're telling python this entire folder (drone_inventory) 
#is considered one packet
from flask import Flask
from config import Config

from .site.routes import site
from .authentication.routes import auth
from .api.routes import api

from flask_migrate import Migrate
from .models import db as root_db, login_manager, ma

from flask_cors import CORS

from .helpers import JSONEncoder

app = Flask(__name__)

app.config.from_object(Config)

app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)

#connect SQLAlchemy and Flask together
root_db.init_app(app)
migrate = Migrate(app, root_db)

login_manager.init_app(app)
login_manager.login_view = 'auth.signin' #Specifies what page to load for NON-auth'd users

ma.init_app(app)

#import all models at the BOTTOM/BASE of everything, so when we call 'migrate' later, models is callable

CORS(app)

app.json_encoder = JSONEncoder

from drone_inventory import models