from .defaults import *

ALLOWED_HOSTS = ['*']

# Debug enabled to make django serve static files
DEBUG = True
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True

PRODUCTION_APPS = (
)
INSTALLED_APPS += PRODUCTION_APPS

