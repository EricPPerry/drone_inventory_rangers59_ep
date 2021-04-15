from flask import Blueprint, render_template, request, flash, redirect, url_for
from drone_inventory.forms import UserLoginForm
#auth gets imported to __init__, and then app.register_blueprint(auth) so these routes can be used
auth = Blueprint('auth', __name__, template_folder='auth_templates')

#after we set up database/db.session
from drone_inventory.models import  User, db, check_password_hash

#Imports for flask login
from flask_login import login_user, logout_user, login_required


@auth.route('/signup', methods=['GET','POST'])
def signup():
    form = UserLoginForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email,password)


            #do this after establishing database
            user = User(email, password = password)
            #create interface between database and user model
            #like an insert statement/session
            db.session.add(user)
            db.session.commit()

            flash(f'You have successfully created a user account {email}', 'user-created')

            return redirect(url_for('site.home'))
    except:
        raise Exception('Invalid Form Data: Please Check Your Form Inputs')
    return render_template('signup.html', form = form)

@auth.route('/signin', methods=['GET','POST'])
def signin():
    form = UserLoginForm()

    #try to get info and validate the form, if it isnt found - give error
    try:
        #checks if the request from form submission is set to 'POST' and form is validated
        if request.method == 'POST' and form.validate_on_submit():
            #set variables equal to values entered into signin form
            email = form.email.data
            password = form.password.data
            #print lets us know these things are getting pulled correctly, helps error checking/finding
            print(email,password)

            #we want to filter by the email provided by the form (defined above)
            #.first() asks for first value that comes back under this query
            logged_user = User.query.filter(User.email == email).first()

            #want to check password and currently logged user
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('You were successfully logged in: via email/password', 'auth-success')
                return redirect(url_for('site.home'))
            else:
                flash('Your email/password is incorrect', 'auth-failed')
                return redirect(url_for('auth.signin'))
    except:
        raise Exception('Invalid Form Data: Please Check Your Form!')
    
    #pass the form = UserLoginForm() to return statement
    return render_template('signin.html', form = form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))
