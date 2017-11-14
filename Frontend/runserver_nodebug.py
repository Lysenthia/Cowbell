from public import website
import logging
from logging.handlers import RotatingFileHandler
logHandler = RotatingFileHandler('logs/info.log', maxBytes=1024, backupCount=1)
logHandler.setLevel(logging.ERROR)
website.logger.setLevel(logging.ERROR)
website.logger.addHandler(logHandler)
website.run(debug=False, host='0.0.0.0', port=80)
