"""
Django settings for Single Sign On Portal (ssop) project.

Generated by 'django-admin startproject' using Django 3.2.15.

For more information on this file, see

https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import base64
import os
import sys
import datetime
import json
import pydot
import pyparsing

from pathlib import Path
from django.utils.safestring import mark_safe
from django.core.exceptions import ImproperlyConfigured
from django.contrib.admin.sites import AdminSite

#
# Either add this into settings.py
DEFAULT_AUTO_FIELD='django.db.models.AutoField'
# ... or
#
# class Topic(models.Model):
#     id = models.AutoField(primary_key=True)
#     ...





# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SSOPSB_VERSION = 'v1.1.2 -- ' + datetime.datetime.utcnow().strftime('%Y.%m.%d') 

# Enables a 'shutdown' banner For those times when Congress cannot get its act together
LAPSE_IN_APPROPRIATIONS = False
LAPSE_IN_APPROPRIATIONS_LINK = "https://www.commerce.gov/news/blog/2023/10/us-department-commerce-plan-orderly-shutdown-due-lapse-congressional"
LAPSE_IN_APPROPRIATIONS_MESSAGE_TOP = ""
LAPSE_IN_APPROPRIATIONS_MESSAGE_TOP = "TESTING, TESTING, TESTING ---- PLEASE IGNORE ----- "
LAPSE_IN_APPROPRIATIONS_MESSAGE_TOP = LAPSE_IN_APPROPRIATIONS_MESSAGE_TOP + "Parts of the U.S. government are closed. This site will not be updated; however, NOAA websites and social media channels necessary to protect lives and property will be maintained.  To learn more, visit commerce.gov."
LAPSE_IN_APPROPRIATIONS_MESSAGE_BOTTOM = "For the latest forecasts and critical weather information, visit weather.gov.  *Please note: Some Funding Opportunities offered under the Bipartisan Infrastructure Law and Inflation Reduction Act are open and can be applied for during the partial government shutdown."
LAPSE_IN_APPROPRIATIONS_MESSAGE_BOTTOM = LAPSE_IN_APPROPRIATIONS_MESSAGE_BOTTOM + " ---- END TESTING -----"

# https://stackoverflow.com/questions/42077532/django-security-and-settings
with open(os.path.join(BASE_DIR, 'secrets.json')) as secrets_file:
    jsonsecrets = json.load(secrets_file)

def get_secret(key):
    """Get secret setting or fail with ImproperlyConfigured"""
    try:
        return jsonsecrets[key]
    except KeyError:
        print("ImproperlyConfigured -- Missing value for key {}".format(key))
        raise ImproperlyConfigured("Missing value for key {}".format(key))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret('SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
#DEBUG = False 
DEBUG_SAML_DEBUG = False 
VERBOSE = False
DEBUG_VERBOSE = False 

# Organization structure 
DOMAIN = "noaa.gov"
ALL_ORGS_BY_ID = {
    "1": {"name": "NOAA", "parent": "#none", "contact": "Kirk Holub", "email": "kirk.l.holub@noaa.gov"},
    "2": {"name": "OAR", "parent": "NOAA", "contact": "Kirk Holub", "email": "kirk.l.holub@noaa.gov"},
    "3": {"name": "GSL", "parent": "OAR", "contact": "Kirk Holub", "email": "kirk.l.holub@noaa.gov"},
    "4": {"name": "GSL-ITS", "parent": "GSL", "contact": "Scott Nahman", "email": "scott.nahman@noaa.gov"},
    "5": {"name": "GSL-WIDS", "parent": "GSL", "contact": "Dan Nietfeld", "email": "dan.nietfeld@noaa.gov"},
    "6": {"name": "GSL-WIDS-WIZARD", "parent": "GSL-WIDS", "contact": "Jebb Stewart", "email": "jebb.q.stewart@@noaa.gov"},
    }



# SSO
#CSRF_TRUSTED_ORIGINS = ['https://sso-dev.noaa.gov', 'https://sso.noaa.gov']
#SAML_FOLDER = os.path.join(BASE_DIR, 'sites/saml')
#SSO_ERROR_REDIRECT = 'https://gsl.noaa.gov/ssopsb/oops'
#SSO_ERROR_REDIRECT = EXTERNAL_URL + 'oops'
#SSOPADMIN_AUTH_RETURN_TO = "/ssopsb/adminssopsb/sites/"
#ICAM_AUTH_RETURN_TO = EXTERNAL_URL + "icam_authenticated"

# NOTE: --- The group names ARE repeated in AUTH_SAML_USER_FLAGS_BY_GROUP -- so if you change one here, be sure to change it in FLAGS_BY_GROUP also
# LDAP_GROUPS and USER_FLAGS_BY_GROUP much match groupnames in add_groups_and_permissions.py
AUTH_SAML_GROUPS = {
    "cn=_OAR ALL,cn=groups,cn=nems,ou=apps,dc=noaa,dc=gov": {
        "modelslist": [],
        "viewmodels": ["About", "Attributes", "AttributeGroup", "AuthToken", "Connection", "Contact", "Organization", "Project", "Sysadmin", "Uniqueuser"]
    },
    "cn=_OAR GSL Sysadm,cn=groups,cn=nems,ou=apps,dc=noaa,dc=gov": {
        "modelslist": ["Contact", "Key", "Organization", "Project", "Room"],
        "viewmodels": ["About", "Attributes", "AttributeGroup", "AuthToken", "Connection", "Sysadmin", "Uniqueuser"]
    },
    'cn=_OAR ESRL GSL SSOPAdmin,cn=groups,cn=nems,ou=apps,dc=noaa,dc=gov': {
        "modelslist": ["About", "Attributes", "AttributeGroup", "AuthToken", "Connection", "Contact", "GraphNode", "Key", "Organization", "NodeType", "Project", "Sysadmin", "Uniqueuser", "User", "Room"],
        "viewmodels": []
    }
}

# The critical keyword is 'is_staff'.  If missing the user will not be able to login.
# is_staff could edited to allow use beyond GSL
# The others are needed in backend.py within this loop:
#             for (tag, group) in self.settings.USER_FLAGS_BY_GROUP.items():
AUTH_SAML_USER_FLAGS_BY_GROUP = {
    "is_active": "cn=_OAR ALL,cn=groups,cn=nems,ou=apps,dc=noaa,dc=gov",
    "is_staff": "cn=_OAR ALL,cn=groups,cn=nems,ou=apps,dc=noaa,dc=gov",
    "is_sysadmin": "_OAR GSL Sysadm,cn=groups,cn=nems,ou=apps,dc=noaa,dc=gov",
    "is_ssopadmin": "cn=_OAR ESRL GSL SSOPAdmin,cn=groups,cn=nems,ou=apps,dc=noaa,dc=gov"
}
#    "is_sysadmin": "_OAR GSL ITS SSG-GSL,cn=groups,cn=nems,ou=apps,dc=noaa,dc=gov",

# NOTE: mapping is case sensitive
AUTH_SAML_USER_ATTR_MAP = {
     "email": "mail",
     "member": "isMemberOf"
 }


SSOP_SYSADS = {}
#SSOP_SYSADS = {
#        'holubdev': {'type': 'localdev', 'email': 'kirk.l.holub@gmail.com', 'homeorg': 'noaa', 'divisions': ['oar', 'gsl', 'gsl-its']},
#}


LOCAL_PASSWORD_MINIMUM_LENGTH = 40
NONE_NAME = "#none"
NONE_NEVER_EXPIRES = '9999-12-31T23:59:59+00:00'
ANYONE_EMAIL = "#anynone.anywhere@anydomain.tld"
NONE_EMAIL = "#none.none@none.tld"

# Expire the session after an hour
SESSION_COOKIE_AGE = 3600
LOGOUT_EXPIRY = 2
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# email configuration
# use 25 instead of 587
# internal routing expects traffic from noreply.gsd@noaa.gov to originate on port 25; which is running TLS
# DMZ is pwx.noaa.gov domain
EMAIL_HOST = 'mail.pwx.noaa.gov'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'noreply.gsl@noaa.gov'
EMAIL_USE_TLS = True
SSOP_ADMIN_EMAIL = "ssopadmin.gsl@noaa.gov"

# Prevents bombarding most users with test emails while development is happening
#EMAIL_TEST_USERS = ['kirk.l.holub@gmail.com', 'kirk.l.holub@noaa.gov']
# An empty set means send notices to all users
EMAIL_TEST_USERS = []


USER_HAS_AUTHENTICATED_SUBJECT = 'SSOPSB Login'
body = 'Hello firstname,\nWe noticed you logged into SSOP sandbox admin at ymdhms.\n'
body = body + 'If you did not login at this time, please contact ' + SSOP_ADMIN_EMAIL
body = body + '\n\nYou can also direct message @Kirk Holub on https://oar-gsl.slack.com'
USER_HAS_AUTHENTICATED_BODY = body

# to help manage Contacts
#                         D    H    M      S
#CONTACT_RENEWAL_PERIOD = 60 * 24 * 60 * 60
#CONTACT_RENEWAL_PERIOD = 60 * 1440 * 60

# Policy per Security Officer
CONTACT_RENEWAL_PERIOD_DAYS = 60 
# days to minutes for debugging
#CONTACT_RENEWAL_PERIOD_DAYS = 4 

# days to minutes for debugging
CONTACT_RENEWAL_PERIOD_SECONDS = CONTACT_RENEWAL_PERIOD_DAYS * 24 * 60 * 60 
# days to minutes for debugging
#CONTACT_RENEWAL_PERIOD_SECONDS = CONTACT_RENEWAL_PERIOD_DAYS * 1 * 1 * 60 
CONTACT_RENEWAL_PERIOD_TIMEDELTA = datetime.timedelta(seconds=CONTACT_RENEWAL_PERIOD_SECONDS)

# time delay before initial warning and it results in having one token with a longer expiration time; this is exploited for account removal
EXPIRES_DT_DELTASECONDS = 600
# days to minutes for debugging
#EXPIRES_DT_DELTASECONDS = 30

CONTACT_RENEWAL_PERIOD_WARNINGS = [] 
# Send an warning email on this many days before an account is deleted
CONTACT_RENEWAL_PERIOD_WARNING_DAYS = [1, 15]
for d in CONTACT_RENEWAL_PERIOD_WARNING_DAYS:
    CONTACT_RENEWAL_PERIOD_WARNINGS.append(datetime.timedelta(days=d))
    # days to minutes for debugging
    #s = d * 60
    #CONTACT_RENEWAL_PERIOD_WARNINGS.append(datetime.timedelta(seconds=s))

if len(CONTACT_RENEWAL_PERIOD_WARNINGS) > int(1):
    CONTACT_RENEWAL_PERIOD_WARNINGS.sort() 


# in seconds
ACCOUNT_REVIEW_NAPTIME = 35

USER_REMOVAL_NOTICE_SUBJECT = 'Single Sign-On Portal Sandbox access expiration notice'
body = 'Hello firstname,\n'
body = body + '\nThe Single Sign-on Portal Sandbox (SSOPSB) is now automatically enforcing NOAA policy which requires the review of user access every ' + str(CONTACT_RENEWAL_PERIOD_DAYS) + ' days.\n'
body = body + '\nYour authorized SSOPSB projects are: project_list\n'
body = body + 'If you require continued access to any of these projects, then you must login to a project before expires_datetime UTC.\n'
body = body + 'Or, you may use this link to acknowledge your need for continued access: renewal_link.\n'
body = body + '\nYour SSOPSB access will be removed in removed_in_dtdelta days at expires_datetime UTC if you take no action.\n'
#body = body + '    Last connected at: last_connected_datetime\n'
#body = body + '    Previous warning sent at: warned_datetime\n'
body = body + '\nYour access can be removed immediately by visiting: remove_account_link\n'
body = body + '\nPlease contact the project owner if you have any questions.\n'
body = body + '\nDo not reply directly to this email; the sending address is not monitored.\n'
#body = body + 'body_comment'
USER_REMOVAL_NOTICE_BODY = body

# https://stackoverflow.com/questions/8023126/how-can-i-test-https-connections-with-django-as-easily-as-i-can-non-https-conne1826
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

#if DEBUG:
#    SESSION_COOKIE_AGE = 10 * SESSION_COOKIE_AGE
#else:
#    CSRF_COOKIE_SECURE = True
#    SESSION_COOKIE_SECURE = True

# tailored from https://www.webforefront.com/django/setupdjangologging.html
# unfortunately, cannot use a variable to enforce DRY for basepath
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'development_logfile': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.FileHandler',
            'filename': '/home/gslauth/logs/ssop_dev.log',
            'formatter': 'verbose'
        },
        'info_logfile': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/home/gslauth/logs/ssop_info.log',
            'formatter': 'verbose'
        },
        'production_logfile': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/home/gslauth/logs/ssop_production.log',
            'maxBytes': 1024 * 1024 * 1024 * 100,  # 100GB
            'backupCount': 5,
            'formatter': 'simple'
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
    },
    'loggers': {
        'django': {
            'handlers': ['development_logfile', 'production_logfile'],
        },
        'django.request': {
            'handlers': ['development_logfile', 'production_logfile'],
        },
        'django.server': {
            'handlers': ['development_logfile', 'production_logfile'],
        },
        'ssop': {
            'handlers': ['development_logfile', 'info_logfile', 'production_logfile'],
        },
        'py.warnings': {
            'handlers': ['development_logfile'],
        },
    }
}


HTTP_PROXY = "http://rhsm-proxy.gsd.esrl.noaa.gov:3128"


# https://pypi.org/project/django-auth-oidc/
AUTH_SERVER = get_secret('AUTH_SERVER')
AUTH_CLIENT_ID = get_secret('AUTH_CLIENT_ID')
AUTH_CLIENT_SECRET = get_secret('AUTH_CLIENT_SECRET')

# https://developers.login.gov/attributes/
AUTH_SCOPE = ["uuid", "profile:name", "given_name", "family_name"]

# Application definition

# for creating object mapping using django-extensions
GRAPH_MODELS = {
  'all_applications': True,
  'group_models': True,
}

GRAPH_MODELS = {
  'app_labels': ["sites"],
}

INSTALLED_APPS = [
    'sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django_extensions',
]

# https://docs.djangoproject.com/en/4.2/ref/contrib/sites/#module-django.contrib.sites
#SITE_ID = 1

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
#    'django.middleware.csrf.CsrfViewMiddleware',

# keeping model backend to support local, non-LDAP login as root as a backup (only known by KLH)
AUTHENTICATION_BACKENDS = [
                        "django_auth_saml.backend.SAMLBackend",
                        "django_contrib_auth.backends.ModelBackend"
]

EMAIL_BACKEND = 'backends.email.EmailBackend'

SESSION_ENGINE = 'django.contrib.sessions.backends.file'

ROOT_URLCONF = 'ssop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'ssop.context_processors.deploy_env',
                'ssop.context_processors.server_url',
                'ssop.context_processors.cwd_refresh_rate',
                'ssop.context_processors.lapse_in_appropriations',
            ],
        },
    },
]

WSGI_APPLICATION = 'ssop.wsgi.application'
SSOP_DEPLOY_ENV = 'Development'
DEFAULT_PROJECT_NAME = 'showattrs'

if SSOP_DEPLOY_ENV == "Development":
    DEPLOY_ENV_COLOR = '#ff6666'  # light red
    DEPLOY_ENV_TEXT_COLOR = 'gold'
    SERVER_FQDN = 'gsl-webstage8.gsd.esrl.noaa.gov'
    EXTERNAL_URL = 'https://gsl.noaa.gov/ssopsb/'
    SERVER_IP = '137.75.133.86'

elif SSOP_DEPLOY_ENV == "Integration":
    DEPLOY_ENV_COLOR = '#99ff99'  # light green
    DEPLOY_ENV_TEXT_COLOR = 'black'
    SERVER_FQDN = 'gsl-webssop.gsd.esrl.noaa.gov'
    EXTERNAL_URL = 'https://gsl.noaa.gov/ssop/'
    SERVER_IP = '137.75.133.109'

elif SSOP_DEPLOY_ENV == "Production":
    DEPLOY_ENV_COLOR = "#3399ff"  # blue
    DEPLOY_ENV_TEXT_COLOR = 'gold'
    SERVER_FQDN = '?.gsd.esrl.noaa.gov'
    SERVER_IP = '137.75.164.x'

else:
    msg = "environment variable SSOP_DEPLOY_ENVIRONMENT not set.  " \
          "Supported values: Development, Integration, Production"
    print(msg)
    sys.exit(-1)

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'gsl.noaa.gov', '140.172.12.92', SERVER_FQDN, SERVER_IP]

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
#DATABASENAME = BASE_DIR + '/ssop/db.sqlite3'
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': DATABASENAME,
#    }
#}

DATABASENAME = 'ssop_dev2'
DATABASEUSERNAME = 'ucanreadwrite'
DATABASEMIGRATIONUSERNAME = 'kirkholub'

DBPWD = get_secret('DATABASE_SECRET')
MIGRATIONPWD = get_secret('MIGRATION_SECRET')

# For initial setup or DB schema updates
#DATABASEUSERNAME = DATABASEMIGRATIONUSERNAME
#DBPWD = MIGRATIONPWD


# https://www.laurencegellert.com/2019/03/making-djangos-database-connection-more-secure-for-migrations/
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DATABASENAME,
        'HOST': 'localhost',
        'USER': DATABASEUSERNAME,
        'PASSWORD': DBPWD,
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_ALL_TABLES'",
            'auth_plugin': 'mysql_native_password',
            'isolation_level': 'repeatable read'
        },
    },
    'default_with_migration_rights': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DATABASENAME,
        'HOST': 'localhost',
        'USER': DATABASEMIGRATIONUSERNAME,
        'PASSWORD': MIGRATIONPWD,
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_ALL_TABLES'",
            'auth_plugin': 'mysql_native_password',
            'isolation_level': 'repeatable read'
        },
    }
}
DBDUMP_ROOT = '/home/gslauth/ssopdump/'

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

#https://docs.djangoproject.com/en/4.2/ref/contrib/admin/#adminsite-attributes
#from django.contrib import admin
#admin.site.site_header = 'My project'                    # default: "Django Administration"
#admin.site.index_title = 'Features area'                 # default: "Site administration"
#admin.site.site_title = 'HTML title from adminsitration' # default: "Django site admin"

AdminSite.site_header = 'SSOP Sandbox Administration'
AdminSite.site_title = 'SSOP sandbox sites admininistration'
AdminSite.index_title = 'SSOP sandbox administration'


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
DEFAULT_DATETIME_STR = '0001-01-01T00:00:00+00:00'
DEFAULT_DATETIME = datetime.datetime.fromisoformat(DEFAULT_DATETIME_STR)

# SSO
CSRF_TRUSTED_ORIGINS = ['https://sso-dev.noaa.gov', 'https://sso.noaa.gov']
SAML_FOLDER = os.path.join(BASE_DIR, 'sites/saml')
#SSO_ERROR_REDIRECT = 'https://gsl.noaa.gov/ssopsb/oops'
SSO_ERROR_REDIRECT = EXTERNAL_URL + 'oops'
ICAM_AUTH_RETURN_TO = EXTERNAL_URL + "icam_authenticated"

# for admin backend, we must return to the server
SSOPADMIN_AUTH_RETURN_TO = "/ssopsb/adminssopsb/sites/"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/usr/share/nginx/html/static/'


MEDIA_ROOT = 'uploads/'
MEDIA_URL = '/uploads/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# https://developers.login.gov/oidc/
LOGINDOTGOV_IDP_SERVER = 'https://idp.int.identitysandbox.gov'
LOGINDOTGOV_CLIENT_ID = 'urn:gov:gsa:openidconnect.profiles:sp:sso:noaa_oar:ssop'

# Basic identity assurance, does not require identity verification (this is the most common value).
LOGINDOTGOV_ACR = 'http://idmanagement.gov/ns/assurance/ial/2'
LOGINDOTGOV_ACR_PFISHING_RESISTANT = 'http://idmanagement.gov/ns/assurance/ial/2&phishing_resistant=true'
LOGINDOTGOV_CLIENT_ASSERTION_TYPE = 'urn%3Aietf%3Aparams%3Aoauth%3Aclient-assertion-type%3Ajwt-bearer'
LOGINDOTGOV_SCOPE = 'openid+email+profile+first_name+last_name'
#LOGINDOTGOV_RETURN_TO = 'https://gsl.noaa.gov/ssopsb/ldg_authenticated'
#LOGINDOTGOV_ERROR_REDIRECT = 'https://gsl.noaa.gov/ssopsb/oops'
#LOGINDOTGOV_LOGOUT_URI = 'https://gsl.noaa.gov/ssopsb/sites'
#LDG_BASE  = 'https://gsl.noaa.gov/ssopsb/'
LOGINDOTGOV_RETURN_TO = EXTERNAL_URL + 'ldg_authenticated'
LOGINDOTGOV_ERROR_REDIRECT = EXTERNAL_URL + 'oops'
LOGINDOTGOV_LOGOUT_URI = EXTERNAL_URL + 'sites'
LDG_BASE  = EXTERNAL_URL
LDG_POSTFIX  = '/'



# A known parameter return on auth sucess .... can be whatever we want as long as its > 22 chars
LOGINDOTGOV_LOGIN_STATE = '2.7182818284590452353602874'
LOGINDOTGOV_LOGOUT_STATE = '1.618033988749894848204586'
with open(os.path.join(BASE_DIR, 'logindotgov/certs/private.pem')) as privcert:
    LOGINDOTGOV_PRIVATE_CERT = privcert.read()

PROJECTS_PREFIX = '/ssopsb/static/projects/'
PROJECTS_POSTFIX = '/logo'
CONTACTS_URL = LDG_BASE + 'project_userlist/'

# JWT verification -- using GSL's LetsEncrypt certs
JWT_BASE_DIR = '/etc/pki/tls/private/gsl-webstage8.gsd.esrl.noaa.gov.'
certfile = JWT_BASE_DIR + 'pem'
keyfile = JWT_BASE_DIR + 'privkey'
with open(certfile) as pubcert:
    JWT_PUBLIC_CERT = pubcert.read()
    JWT_PUBLIC_CERT_B64 = str(base64.b64encode(JWT_PUBLIC_CERT.encode()))
with open(keyfile) as privkey:
    JWT_PRIVATE_KEY = privkey.read()
    JWT_PRIVATE_KEY_B64 = str(base64.b64encode(JWT_PRIVATE_KEY.encode()))

# safe token length
JWTSAFELEN = 30

# JWT expiration time in seconds -- will be added to current UTC
JWTEXP = 300

# Length of a production key -- to aid in deployments
PRODKEYLEN = 60

# Attributes one-time access token lifetime in seconds
ATTRS_ACCESS_TOKEN_LIFETIME = JWTEXP
DATA_AT_REST_KEY_ATTRS = get_secret('DATA_AT_REST_KEY_ATTRS')

# for graphing
NODE_TYPE_CHOICES = ['AllConnections', 'Attribute', 'AttributeGroup', 'Browser', 'Organization', 'Project', 'Uniqueuser', 'Conngroup', 'Namegroup']
# If true, [nodenumber] will we prepended to each node label
LABELNODES = False

# helps to reduce clutter in the Projects list
MAXUSERLIST = 3

# supported logo image types
LOGO_FILETYPES = ['png', 'jpg', 'jpeg']
LOGO_FILETYPESTR = ''
for it in LOGO_FILETYPES:
   LOGO_FILETYPESTR += str(it) + ', '
LOGO_FILETYPESTR = LOGO_FILETYPESTR[:-2]

HELP_NAME = "A simple, urlsafe (no spaces or special characters) name for this project.  It will be used to create a login url."
HELP_VERBOSE_NAME = "A longer name which does not have to be urlsafe (no spaces or special characters) for this project.  It will be set to the project's name if 'newproject' remains in the field."
HELP_RETURN_TO = "The URL to which authenticated users will be sent.  An authentication token string may be appended to the url using a ?"
HELP_ERROR_REDIRECT = "Users are directed to this url upon a login error.  Override the default value for custom error handling."
HELP_STATE = "A unique, immutable key used to differentiate projects.  This will be automatically set by the first Save operation."
HELP_CONNECTION_STATE = "A unique, immutable key used to differentiate connection requests.  This will be automatically set during each connections to an identity provider"
HELP_PUBCERT = "To generate a 2048-bit PEM-encoded public certificate for your project (with a 1-year validity period) run this command:<br>     openssl req -nodes -x509 -days 365 -newkey rsa:2048 -keyout private.pem -out public.crt<br>   This certificate is used to sign json web tokens."
HELP_DECRYPT_KEY_NAME = "Name of the 32 byte urlsave_64bencoded string generated using fernet.generate_key.<br>   This symetric key is used to encrypt data in transit.<br>  To rekey, delete the key and add a new one manually."
HELP_DECRYPT_KEY = "A 32 byte urlsave_64bencoded string generated using fernet.generate_key.<br>   This symetric key is used to encrypt data in transit."
HELP_DECRYPT_KEY_NAME = "A meaningful name used for display purposes.  If left as 'setme' a unique name will be created."
HELP_QUERYPARAM = "If True, the html query parameter specified in the URL query delimiter field and the access token value will be appended onto the RETURN_TO url."
HELP_DISPLAY_ORDER = "Used to order the projects on the main screen.  Item 1 is top, left.  If order is identical to another project(s), alphabetic sub-sorting will be used."
HELP_ENABLED = "If True the project's tile will be available on the main screen."
HELP_EXPIRETOKENS = "If True this project's authorization tokens will be fetched (and expired) upon use, as it will be in production.  If False (the default state), tokens will never expire which is convenitent for development work."
HELP_ORGANIZATION = "Organization responsible for this project."
HELP_GRAPHNODE = "Used for connection graphing.  Automatically generated when needed."
HELP_LOGOIMG = "An image used for the Project's tile on the main page.  Types are limited to: " + LOGO_FILETYPESTR + ".  The image will be resized using a square aspect ratio."
HELP_APP_PARAMS = "Optional field for application use.  Defaults is an empty dictionary."
HELP_PROJECT_OWNER = "The Federal sponsor for this Project."
HELP_CONTACT_EMAIL = "If email is the only field set, then the system will attempt to set firstname and lastname by splitting email address on the '@' and '.' characters when the SAVE button is clicked."
HELP_PFISHING_RESISTANT = "When true, users must use a crytographically secure method authentication method, such as WebAuthn or a PIV/CAC.  This setting only applied to login.gov since ICAM authentication always requires a CAC."
HELP_IDP = "The Identity Provider to be used -- select ICAM for CAC or PIV card based authenticaion."
HELP_SSOSTR = "SSO string sent in the HTML header cookie.  This sent is in addition to the HTTP Authentication header to support applications which may not be able to read the HTTP header."
HELP_ICAM_ATTRIBUTES = "User's ICAM attributes"
HELP_ICAM_GROUPS = "ICAM groups authorized for this project.  Users who are members of these groups will be authorized for this project.  Use command-click to select multiple groups."
HELP_USERLIST = "Users authorized for this project.  This list is IGNORED for ICAM authenticated Projects!  Use command-click to select multiple users.  Click + to add a new Contact."

# Critical Weather Day Status page
CWD_PREV = "uploads/ncocwd.txt"
CWD_URL = "https://www.nco.ncep.noaa.gov/status/cwd/"
CWD_PAGE_REFRESH_RATE = 60

# NCO likely only refreshes on synoptic times 0, 6, 12, 18 UTC.  However, just in case, pull every 15 minutes 
CWD_FETCH_INTERVAL = 900
DATA_CENTER_ROOMS = {
        "GA405": {"name": "(High Performance Computing Facility)", "state": "Normal"},
        "2B518": {"name": "(Central Facility Annex)", "state": "Normal"},
        "2B201": {"name": "(Central Computing Facility)", "state": "Normal"}
}

#  1248

