import os
basedir = os.path.abspath(os.path.dirname(__file__))


class DefaultConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    SESSION_REFRESH_EACH_REQUEST = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #Spotify client details
    CLIENT_ID = ''     
    CLIENT_SECRET = ''
    REDIRECT_URI = 'http://localhost:5000/success'
    SCOPE = 'playlist-modify-private playlist-modify-public'


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

