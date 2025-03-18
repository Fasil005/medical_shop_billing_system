import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOG_DIR = os.path.join(BASE_DIR, "logs")

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Log file name as the current date
LOG_FILE = os.path.join(LOG_DIR, f"logger_{datetime.now().strftime('%Y-%m-%d')}.log")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        # 'verbose': {
        #     'format': '{levelname} {asctime} [{module}.{funcName}] ({filename}:{lineno}) {message}',
        #     'style': '{',
        # },
        'detailed': {
            'format':'{levelname} {asctime} - {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING', 
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILE,
            'maxBytes': 1024 * 1024 * 5,  # 5MB
            'backupCount': 1, 
            'formatter': 'detailed',
        },
        'console': {
            'level': 'DEBUG',  
            'class': 'logging.StreamHandler',
            'formatter': 'detailed',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'DEBUG',

    },
}
