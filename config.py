import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:@localhost/mbp_health'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SENDINBLUE_API_KEY = os.environ.get('SENDINBLUE_API_KEY')
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/profile_pics')
