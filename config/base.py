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

# SCRAPY SETTINGS BELOW

BOT_NAME = 'scraper'

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:108.0) Gecko/20100101 Firefox/108.0'
USER_AGENT_LIST = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:108.0) Gecko/20100101 Firefox/108.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
]

ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 32
DOWNLOAD_DELAY = 1.5

SCRAPER_TOR_HTTP_PROXY = None

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
AUTOTHROTTLE_DEBUG = True

HTTPCACHE_ENABLED = False
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = []

REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
