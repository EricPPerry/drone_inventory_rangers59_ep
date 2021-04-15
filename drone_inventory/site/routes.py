from flask import Blueprint, render_template
from flask_login import login_required
#site gets imported to __init__, and then app.register_blueprint(site) so these routes can be used
site = Blueprint('site', __name__, template_folder='site_templates')
"""
Blueprint Configuration 
-The first argument ('site'), is the Blueprint's name, which is used by
Flask's routing system
-Second argument (__name__) is the Blueprint's import name, which Flask uses
to locate the Blueprint resources. 
-Last argument (template_folder) is the Blueprint's HTML template folder, which
tells the Blueprint which HTML files to use for specific routes
"""

#creating a route
@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile')
@login_required
def profile():
    return render_template('profile.html')