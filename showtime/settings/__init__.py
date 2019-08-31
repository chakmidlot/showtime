import os

APP_NAME = "showtime"

TELEGRAM_HOST = "https://api.telegram.org"

TELEGRAM_POLLING_TIMEOUT = 20

MONGO_URI = "localhost:37017"

if os.getenv("ENV", '').lower() == 'test':
    from showtime.settings.test import *
