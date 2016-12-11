import os, json

#SETTINGS_PROFILE = 'production'
SETTINGS_PROFILE = 'development'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'w6r2649*rg5^n*&=79o%@-%m*t#87!jg-8(nn-k)ykj_u1tyu3'
# secrets_path = os.environ.get('OPENSHIFT_DATA_DIR')
# SECRET_KEY = json.loads(open(secrets_path+'/secrets.json').read())
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


if SETTINGS_PROFILE == 'production':
    OPENSHIFT_REDIS_HOST = os.environ.get('OPENSHIFT_REDIS_HOST')
    OPENSHIFT_REDIS_PORT = int(os.environ.get('OPENSHIFT_REDIS_PORT'))
    OPENSHIFT_REDIS_PASSWORD = os.environ.get('REDIS_CLI').split(' ')[-1]
    REDIS_PATH = ("redis://:{}@{}:{}/0").format(OPENSHIFT_REDIS_PASSWORD,
                                                OPENSHIFT_REDIS_HOST,
                                                OPENSHIFT_REDIS_PORT)
elif SETTINGS_PROFILE == 'development':
    #REDIS_PATH = ("localhost", 6379)
    REDIS_PATH = "redis://localhost:6379/0"
