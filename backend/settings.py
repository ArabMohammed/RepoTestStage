import os
from datetime import timedelta
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_e^ls4+xrxyy(32k$xnzxpm93i5v3u!_bl_$^^ze4gydkw!0k$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    ####### THird party apps ######
    'rest_framework',
    'djoser',
    'corsheaders',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    ######################################
    'accounts',
    'api.annonces',
    'api.localisation',
    'api.contacts',
    'django.contrib.sites',
    'api.messageoffre',
    ###### test django-all-auth ##########################
]
SITE_ID=1
MIDDLEWARE = [
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':[os.path.join(BASE_DIR, 'build')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        ##for postregsql
        #'NAME': 'auth_system',
        #'USER':'moh',
        #'PASSWORD':'password123',
        #'HOST':'localhost'
    }
}
#################SENDING EMAILS TO USERS#####################################
##################################################################
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT=587
EMAIL_HOST_USER = 'dzestatesd@gmail.com'
EMAIL_HOST_PASSWORD= 'oiwxbtptwlucfjat'
EMAIL_USE_TLS=True
# Password validation

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        #'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        #'rest_framework.authentication.BasicAuthentication',
        ###the last one for http sites###
        #'rest_framework.authentication.BasicAuthentication',
        #'rest_framework.authentication.SessionAuthentication',
    ),
    ## you must return it for production
    ##it insure that only authentified users can use certaisn apis
    #'DEFAULT_PERMISSION_CLASSES':(
    #    'rest_framework.permissions.IsAuthenticated',
    #),
    'DEFAULT_PAGINATION_CLASS':"rest_framework.pagination.LimitOffsetPagination",
    'PAGE_SIZE':10
    #'DEFAULT_RENDERER_CLASSES': (
     # 'rest_framework.renderers.JSONRenderer',
    #)
    
}

AUTHENTICATION_BACKENDS = (
    #'social_core.backends.google.GoogleOAuth2',
    #'social_core.backends.google.GoogleOpenId',
    #'social_core.backends.facebook.FacebookOAuth2',
    #'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)
SIMPLE_JWT = {
    'AUTH_HEADER_TYPES':('JWT',),
    'ACCESS_TOKEN_LIFETIME':timedelta(minutes=2000),
    'REFRESH_TOKEN_LIFETIME':timedelta(minutes=2000),
    'AUTH_TOKEN_CLASSES': (
        'rest_framework_simplejwt.tokens.AccessToken',
    )
}

DJOSER ={
    'LOGIN_FIELD':'email',
    'USER_CREATE_PASSWORD_RETYPE':True,
    'USERNAME_CHANGED_EMAIL_CONFIRMATION':True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION':True,
    'SEND_CONFIRMATION_EMAIL':True,
    'SET_USENAME_RETYPE':True,
    'SET_PASSWORD_RETYPE':True,
    'PASSWORD_RESET_CONFIRM_URL':'password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL':'email/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL':'activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL':True,
    'PASSWORD_RESET_CONFIRM_RETYPE':True,
    #'SOCIAL_AUTH_TOKEN_STRATEGY':'djoser.social.token.jwt.TokenStrategy',
    #'SOCIAL_AUTH_ALLOWED_REDIRECT_URIS':['http://localhost:3000/google'],
    'SERIALIZERS':{
        'user_create':'accounts.serializers.UserCreateSerializer',
        'user':'djoser.serializers.UserSerializer',
        "current_user": "djoser.serializers.UserSerializer",
        'user_delete':'djoser.serializers.UserSerializer',
    }
}
##############################################
##############################################

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CORS_ORIGIN_WHITELIST = [
     "http://localhost:3000",
     "http://127.0.0.1:3000", 
]

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATICFILES_DIRS=[
    os.path.join(BASE_DIR, 'build/static'),
    os.path.join(BASE_DIR, 'media'),
]
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# URL used to access the media
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'accounts.UserAccount'

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
#################################################"
##client web 3 ######################
########################################
GOOGLE_SSO_CLIENT_ID = '25353584449-vn4af7l1mrntv8g0si2grckm3nkb4eie.apps.googleusercontent.com'
GOOGLE_SSO_CLIENT_SECRT = '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'
GOOGLE_SSO_PROJECT_ID = 'MyProject123456789'
GOOGLE_SSO_ALLOWABLE_DOMAINS = ["esi.dz","gmail.com"]
#SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile', 'openid']
####################################################
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

