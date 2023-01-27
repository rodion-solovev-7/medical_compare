ENV = 'local'

# backend
HOST = '0.0.0.0'
PORT = 8080

# database
DB_HOST = 'postgres'
DB_NAME = 'postgres'
DB_PORT = 5432
DB_USER = 'postgres'
DB_PASS = 'postgres'
DB_MAX_CONNECTION = 5

# scraper
SCRAPER_TOR_HTTP_PROXY = None
SCRAPER_SAVE_SCRAPED_TO_DB = False

AUTO_SCRAPING_DELAY = 60 * 60 * 24 * 7

# logging
LOG_LEVEL = 'DEBUG'
LOG_LEVEL_LIBRARY = 'DEBUG'
