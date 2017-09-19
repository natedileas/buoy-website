# ME-DEFINED
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

APP_HOST = 'localhost'
APP_PORT = 5000

# Celery configuration
# redis is the async arch behind celery
CELERY_BROKER_URL = 'redis://{0}:{1}/{2}'.format(REDIS_HOST, REDIS_PORT, REDIS_DB)
CELERY_RESULT_BACKEND = 'redis://{0}:{1}/{2}'.format(REDIS_HOST, REDIS_PORT, REDIS_DB)

# FLASK OPTIONS
# flask WTF config, stands for cross-site request forgery prevention
CSRF_ENABLED = True
SECRET_KEY = 'password'
# \x81\xf6F\xad\xc0\xe2N\xf2\xdb\x89\x0b\xee\xd0x\x9c\x18\x1a\x91\xbf\x88\xa1/\xab\x14U
