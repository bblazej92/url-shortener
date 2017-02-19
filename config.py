
class Config:
    MONGODB_HOST = 'db'


class DevelopmentConfig(Config):
    URL_PREFIX = 'localhost:5000'
    DEBUG = True


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
