import os

basedir = os.path.abspath(os.path.dirname(__file__))
#Giving access to project in ANY OS we find ourselves in
#Allow outside files/folders to have the ability to add to the project from
#the base directory 

class Config():
    """
    We will set Config variables for the Flask App here.
    Using Environment variables where available, otherwise 
    we will create the config variable(s) if not already done
    """

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'You will never guess...'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEPLOY_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    #Allows us to see if something went wrong accessing DATABASE_URL, as sqlite will be made if it fails/goes wrong
    SQLALCHEMY_TRACK_MODIFICATIONS = False #Turn off update messages from the database
    