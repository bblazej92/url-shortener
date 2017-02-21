
class Config:
    MONGODB_HOST = 'db'


class DevelopmentConfig(Config):
    URL_PREFIX = 'localhost:5000'
    DEBUG = True
    SECRET_KEY = 'development_is_secret!'
    OAUTH_CREDENTIALS = {
        'facebook': {
            'id': '1758312601153697',
            'secret': '97178dc5fdb2425a11f93118bdf88227'
        }
    }


class TestingConfig(Config):
    URL_PREFIX = 'http://test.pl'
    MONGODB_HOST = 'localhost'
    MONGODB_DB = 'test'
    testing = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
