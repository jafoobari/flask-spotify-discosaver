import os
basedir = os.path.abspath(os.path.dirname(__file__))


class DefaultConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    SESSION_REFRESH_EACH_REQUEST = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #Spotify client details
    CLIENT_ID = '8412e923acce48a8b99ada05b6ba1181'     
    CLIENT_SECRET = 'fbcadd353812442aaf9bd8c2bf6f0801'
    REDIRECT_URI = 'http://hyzypg.pythonanywhere.com/success'
    SCOPE = 'playlist-modify-private playlist-read-private'


class DevelopmentConfig(DefaultConfig):
    DEBUG = True
    REDIRECT_URI = 'http://localhost:5000/success'
    
class TestingConfig(DefaultConfig):
    TESTING = True

configs = {
    "dev": "config.DevelopmentConfig",
    "testing": "config.TestingConfig",
    "default": "config.DefaultConfig"
}

def configure_app(app):    
    config_name = os.getenv('FLASK_CONFIG', 'default')
    app.config.from_object(configs[config_name])

