import os

# default_config = {
#     'APPLICATION_ROOT': '/', 
#     'DEBUG': None, 
#     'ENV': None, 
#     'EXPLAIN_TEMPLATE_LOADING': False, 
#     'JSONIFY_MIMETYPE': 'application/json', 
#     'JSONIFY_PRETTYPRINT_REGULAR': False, 
#     'JSON_AS_ASCII': True, 
#     'JSON_SORT_KEYS': True, 
#     'MAX_CONTENT_LENGTH': None, 
#     'MAX_COOKIE_SIZE': 4093, 
#     'PERMANENT_SESSION_LIFETIME': datetime.timedelta(days=31), 
#     'PREFERRED_URL_SCHEME': 'http', 
#     'PRESERVE_CONTEXT_ON_EXCEPTION': None, 
#     'PROPAGATE_EXCEPTIONS': None, 
#     'SECRET_KEY': None, 
#     'SEND_FILE_MAX_AGE_DEFAULT': datetime.timedelta(seconds=43200), 
#     'SERVER_NAME': None, 
#     'SESSION_COOKIE_DOMAIN': None, 
#     'SESSION_COOKIE_HTTPONLY': True, 
#     'SESSION_COOKIE_NAME': 'session', 
#     'SESSION_COOKIE_PATH': None, 
#     'SESSION_COOKIE_SAMESITE': None, 
#     'SESSION_COOKIE_SECURE': False, 
#     'SESSION_REFRESH_EACH_REQUEST': True, 
#     'TEMPLATES_AUTO_RELOAD': None, 
#     'TESTING': False, 
#     'TRAP_BAD_REQUEST_ERRORS': None, 
#     'TRAP_HTTP_EXCEPTIONS': False, 
#     'USE_X_SENDFILE': False
# }


ROOT           = os.path.dirname(os.path.realpath(__file__))
STATIC_ROOT    = os.path.join(ROOT, 'static')
TEMPLATE_ROOT  = os.path.join(ROOT, 'templates')

FRONTEND_CONFIG_FILE = {
    "filename" : "site_config.json"
}

DATABASE_FILES = [
    'blog_data.json',
    'partners.json',
    'members.json'
]

class config(object):

    SECRET_KEY = '7afbbd085cd10de82a67572c1ebf7827'
    APPLICATION_ROOT = ROOT

    DATABASE_LOCATION = ''
    DATABASE_HOST = 'localhost'
    DATABASE_PASSWORD = False

    DEBUG = False
    TESTING = True


class test_config(config):

    ENV = 'test'
    TESTING = True

class development_config(config):

    ENV = 'development'
    TESTING = False


class production_config(config):

    ENV = 'production'
    TESTING = False
    DEBUG = True