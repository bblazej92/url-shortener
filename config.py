
class Config:
    MONGODB_HOST = 'db'


class DevelopmentConfig(Config):
    SERVER_NAME = 'localhost:5000'
    DEBUG = True
    SECRET_KEY = 'development_is_secret!'
    OAUTH_CREDENTIALS = {
        'facebook': {
            'id': '1758312601153697',
            'secret': '97178dc5fdb2425a11f93118bdf88227'
        }
    }


class TestingConfig(Config):
    SERVER_NAME = 'localhost:5001'
    MONGODB_HOST = 'localhost'
    MONGODB_DB = 'test'
    SECRET_KEY = 'testing_is_secret!'
    LOGIN_DISABLED = True
    testing = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
