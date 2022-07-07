from datetime import timedelta
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    SECRET_KEY = 'tokoSembakocUyy'

    UPLOAD_FOLDER = 'app/static/images/'

    POSTS_PER_PAGE = 10

    ALLOWED_EXTENSION = set(['txt', 'pdf', 'jpg', 'png', 'jpeg', 'gif'])

    # PERMANENT_SESSION_LIFETIME = timedelta(minutes=15)
    
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     "mysql+pymysql://root:rootpass@localhost/db_pos_example" 
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        "sqlite:///" + os.path.join(basedir, 'app',"sembako.db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False