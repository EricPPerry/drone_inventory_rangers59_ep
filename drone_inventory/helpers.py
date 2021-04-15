from functools import wraps
import secrets

from flask import request, jsonify
#jsonify will allow us to pass a message if they're not authenticated

from drone_inventory.models import Drone, User

def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        token = None #start by assuming no one has access to our app

        if 'x-access-token' in request.headers:
            #every request to the API needs to have a 'Header'
            #referencing dictionary in Insomnia, 
            token = request.headers['x-access-token'].split(' ')[1]
        
        #sad path, if we don't receive a token
        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        #after verifying we have a token
        #further verification that we have a user matched with this token
        try:
            current_user_token = User.query.filter_by(token = token).first()
        
        except:
            owner = User.query.filter_by(token = token).first()
            if token != owner.token and secrets.compare_digest(token, owner.token):
                return jsonify({"message":"Token is invalid!"})
        return our_flask_function(current_user_token, *args, **kwargs)
    return decorated

import decimal
from flask import json

#need to change decimal values (price, cost of production, etc) to strings, for easier json
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            #Convert decimal value into a string
            return str(obj)
        return super(JSONEncoder, self).default(obj)