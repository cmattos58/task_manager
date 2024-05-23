from .settings import *

# Use um banco de dados SQLite em memória para os testes
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': ':memory:',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'HOST': config('DATABASE_HOST'),
        'PORT': config('DATABASE_PORT'),
        'OPTIONS': {
            'options': "-c search_path=test_task_manager",
        }
    }
}

# Desative as notificações de senha para evitar erros durante os testes
AUTH_PASSWORD_VALIDATORS = []

# Use tokens JWT com tempo de vida curto para os testes
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(minutes=10),
}

# Defina o tamanho de paginação menor para os testes
REST_FRAMEWORK["PAGE_SIZE"] = 2

# Defina um diretório estático temporário para os testes
STATIC_URL = '/static/'
