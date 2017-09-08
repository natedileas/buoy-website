SECRET_KEY = 'password'
# \x81\xf6F\xad\xc0\xe2N\xf2\xdb\x89\x0b\xee\xd0x\x9c\x18\x1a\x91\xbf\x88\xa1/\xab\x14U

# Celery configuration
# redis is the async arch behind celery
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# flask WTF config, stands for cross-site request forgery prevention
CSRF_ENABLED = True

# database stuff
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
