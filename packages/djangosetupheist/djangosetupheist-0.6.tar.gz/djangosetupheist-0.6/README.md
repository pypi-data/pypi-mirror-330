# Django Setup (django_setup)

A command-line utility that simplifies Django project initialization and application management.

## Features

- **Streamlined Project Initialization**: Create a new Django project with environment variables support, sensible defaults, and a centralized app configuration system.
- **Simplified App Creation**: Add new apps to your project with automatic registration in URLs and settings.
- **Centralized App Management**: Manage all your project apps from a single configuration file.

## Installation

```bash
pip install djangosetupheist
```

## Usage

### Initialize a New Django Project

```bash
djs init [app_name]
```

If `app_name` is not provided, you will be prompted to enter one.

This command will:
- Create a new Django project with the specified name
- Set up a `.env` file for environment variables
- Configure settings.py to use environment variables for:
  - SECRET_KEY
  - ALLOWED_HOSTS
  - Other configurable settings
- Create an `appsConfig.py` file to centralize app registration

### Create a New App

```bash
djs startapp [app_name]
```

This command will:
- Create a new Django app with the specified name
- Add the app to `appsConfig.py` with default values:
  ```python
  {
      'app_name': 'app_name',
      'url': 'app_name/',
      'namespace': 'app_name'
  }
  ```
- The app will be automatically registered in `INSTALLED_APPS` and URL patterns

## appsConfig.py Structure

The `appsConfig.py` file is the central configuration point for all your apps. It contains a list of dictionaries with the following structure:

```python
app_configs = [
    {
        'app_name': 'items',      # The name of the app
        'url': 'items/',          # The URL prefix for this app
        'namespace': 'items'      # The namespace for this app's URLs
    },
    # More apps...
]
```

### Customizing App Configuration

You can modify the values in `appsConfig.py` to change how your apps are configured:

- **app_name**: The name of your app (should match the directory name)
- **url**: The URL prefix for this app in your project's URL configuration
- **namespace**: The namespace used for URL names

**Important**: If you change the `namespace`, make sure to update the app's `urls.py` file to match the new namespace.

## Benefits

- **Single Source of Truth**: Manage all your apps from a single configuration file
- **Reduced Boilerplate**: No need to manually update settings.py and urls.py when adding new apps
- **Environment Variable Support**: Built-in support for environment variables through .env file
- **Consistent Structure**: Maintain a consistent project structure across all your Django projects

## Example

After initializing a project with `djs init myproject`, your project structure will include:

```
myproject/
├── manage.py
├── myproject/
│   ├── assets/
│   │   ├── media/
│   │   ├── static/
│   ├── templates/
│   ├── .env
│   ├── .envtemp
│   ├── __init__.py
│   ├── appsConfig.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
```

The `appsConfig.py` file will contain:

```python
from django.urls import path, include

app_configs = [
    # { "app_name": "finances.payments", "url": "finances/payments", "namespace": "payments" },
]

def getAppUrls():
    urlpatterns = []
    for config in app_configs:
        urlpatterns.append(
            path(f"{config['url']}", include(f"{config['app_name']}.urls", namespace=config['namespace']))
        )
    return urlpatterns

def getAppNames():
    return [config['app_name'] for config in app_configs]
```


After running `djs startapp items`, the structure will be updated:

```
myproject/
├── .env
├── items/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── templates/
│   │   ├── items/
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── myproject/
│   ├── assets/
│   │   ├── media/
│   │   ├── static/
│   ├── templates/
│   ├── .env
│   ├── .envtemp
│   ├── __init__.py
│   ├── appsConfig.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
```

And `appsConfig.py` will be updated to include:

```python
app_configs = [
    {
        'app_name': 'items',
        'url': 'items/',
        'namespace': 'items'
    }
]
```

## Other Files
settings.py
```python
# Settings for store using django_setup
from pathlib import Path
import os, environ
from .appsConfig import getAppNames

# Uses environ to interface with environment variables
env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env() 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
INTERNAL_IPS = env.list('INTERNAL_IPS')

# CORS: Requires django-cors-headers
# CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS')
# CORS_ALLOW_ALL_ORIGINS = True


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
INSTALLED_APPS += getAppNames()

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "store.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'store/templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "store.wsgi.application"


# Database: using environment variables for both production and development
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.getenv("DB_ENGINE"),
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST"),
        # 'PORT': os.getenv("DB_PORT"),
        "OPTIONS": {}
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Secure Cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'store/assets/static/'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'store/assets/staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'store/assets/media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Email settings
EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_USE_TLS = env('EMAIL_USE_TLS')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')
TO_EMAILS = env.list('TO_EMAILS')
```

main urls.py
```python
from django.contrib import admin
from django.urls import path, include

from .appsConfig import getAppUrls

urlpatterns = [
    path("admin/", admin.site.urls),
]

urlpatterns += getAppUrls()
```

.env with an autogenerated secret key
```python
DEBUG=True
SECRET_KEY=x%kneIyp2Hk^l*[iaM1^SG<SB#V{owr@
ALLOWED_HOSTS=127.0.0.1,localhost

CORS_ALLOWED_ORIGINS=http://127.0.0.1,http://localhost
INTERNAL_IPS=127.0.0.1,localhost

APP_ROOT=.

DB_ENGINE='django.db.backends.sqlite3'
DB_NAME='db.sqlite3'
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
DB_STRICT_MYSQL=


EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'
EMAIL_HOST=''
EMAIL_PORT=
EMAIL_HOST_USER=''
EMAIL_HOST_PASSWORD=
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=''
TO_EMAILS=

# azure blob config
AZURE_ACCOUNT_NAME=''
AZURE_CONNECTION_STRING=''
AZURE_ACCOUNT_KEY=''
AZURE_URL_EXPIRATION_SECS=
AZURE_MEDIA_CONTAINER=''
AZURE_STATIC_CONTAINER=''
```


## License

GNU General Public License v3 or later (GPL-3.0+)