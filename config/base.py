import enum
import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENV = os.getenv('ENVIRONMENT', None)  # must be on of [local,stage,pre,prod]

HOST = '0.0.0.0'
PORT = 8080
CLIENT_MAX_SIZE = 30 * 1024 ** 2

API_ENABLED = True
ADMIN_ENABLED = True

# Уровень логирования
# Один из DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL = 'INFO'

# Уровень логирования для сторонних библиотек
# Один из DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL_LIBRARY = 'WARNING'

# Конфигурация БД
DB_NAME = 'postgres'
DB_HOST = 'postgres'
DB_PORT = 5432
DB_USER = 'postgres'
DB_PASS = 'postgres'
DB_ECHO = False
DB_MAX_CONNECTION = 5

LOG_SETTINGS = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'default': {'()': 'common.context.log_tools.CMDFormatter'},
    },
    'handlers': {
        'default': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        }
    },
    'loggers': {
        '': {
            'level': lambda conf: conf.get('LOG_LEVEL'),
            'handlers': ['default'],
        },
        'aiohttp.web': {'level': lambda conf: conf.get('LOG_LEVEL_LIBRARY'), 'handlers': ['default']},
    },
}


class HealthStatus(enum.Enum):
    ACTIVE = 200
    MAINTENANCE = 429
    SHUTDOWN = 503


CURRENT_HEALTH_STATUS = HealthStatus.SHUTDOWN.value
