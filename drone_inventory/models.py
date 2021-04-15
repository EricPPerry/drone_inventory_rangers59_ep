from flask_sqlalchemy import SQLAlchemy
import uuid #allows us to generate UNIQUE ID when needed
from datetime import datetime

#Adding Flask security features
from werkzeug.security import generate_password_hash, check_password_hash

#Import for Secrets Module (Provided by Python)
import secrets

#Imports for Login Manager and the UserMixin
from flask_login import LoginManager, UserMixin

#Import for flask-Marshmallow
from flask_marshmallow import Marshmallow

#instantiate SQLAlchemy with alias of 'db'
db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

#allows us to make this particular to specific user
#checks to make sure we have a user in database matching the id/info provided
#'call back' function, calling back after something else happens i.e. user attempts to login, this check happens
#returns instance of current_user, that we call on in other place - profile/login checks
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

#create first model
class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '') #nullable allows this to be empty
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150),nullable = False)
    password = db.Column(db.String, nullable = False, default = '')
    token = db.Column(db.String, default = '', unique = True) #'unique' constraint, so no duplicate tokens
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    drone = db.relationship('Drone', backref = 'owner', lazy = True) #lazy means it only loads/is available when needed

    #set methods in class (User())

    def __init__(self, email, first_name = '', last_name = '', id = '', password = '', token = ''):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
    
    #set methods referenced withed __init__()
    #generates token with secrets.token_hex based on length (provided as 24 when called in __init__())
    def set_token(self, length):
        return secrets.token_hex(length)
    
    #gives us id
    def set_id(self):
        return str(uuid.uuid4())
    
    #accepts plain text password, hashes it and returns it in __init__()
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been created and added to database!'


class Drone(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(200), nullable = True)
    price = db.Column(db.Numeric(precision=10, scale = 2))#like using (10,2) in SQL
    camera_quality = db.Column(db.String(150), nullable = True)
    flight_time = db.Column(db.String(100), nullable = True)
    max_speed = db.Column(db.String(100))
    dimensions = db.Column(db.String(100))
    weight = db.Column(db.String(50))
    cost_of_prod = db.Column(db.Numeric(precision = 10, scale = 2))
    series = db.Column(db.String(150))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, description, price, camera_quality, flight_time, max_speed, dimensions, weight, cost_of_prod, series, user_token, id = ''):
        #id goes at end, since it is being used in a method/function
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.price = price
        self.camera_quality = camera_quality
        self.flight_time = flight_time
        self.max_speed = max_speed
        self.dimensions = dimensions
        self.weight = weight
        self.cost_of_prod = cost_of_prod
        self.series = series
        self.user_token = user_token
    
    def __repr__(self):
        return f'The following drone has been added:{self.name}'

    def set_id(self):
        return secrets.token_urlsafe()

#Creation of API Schema via the marshmallow package
class DroneSchema(ma.Schema):
    class Meta:
        #this starts the process of defining what comes back when asking for info via Insomnia
        fields = ['id', 'name', 'description', 'price', 'camera_quality', 'flight_time', 'max_speed', 'dimensions', 'weight', 'cost_of_prod', 'series']


#now we instantiate so we can use the DroneSchema stuff

drone_schema = DroneSchema()
drones_schema = DroneSchema(many = True) #allows multiple drones to come back as a list

    

