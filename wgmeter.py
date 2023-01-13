'''
 # @ Author: Wilfried Grousson
 # @ Created: 2023-01-12
 # @ License: MIT
 # @ Description: This is the main application entry point
 '''
import os
import logging
import logging.handlers

''' Personal imports '''
from constants import APP_NAME, LOG_LEVEL, APP_VERSION
from gui.cgmainapp import CGMainApp

def __init_logging():
        logger = logging.getLogger(APP_NAME)
        logger.setLevel(LOG_LEVEL)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s|%(module)s - %(levelname)s - %(message)s'))
        stream_handler.setLevel(LOG_LEVEL)
        logger.addHandler(stream_handler)

        log_file = os.path.join(os.path.realpath(os.path.dirname(__file__)), "log")
        if not os.path.exists(log_file):
            os.makedirs(log_file)

        needRoll = os.path.exists(log_file + "/cgmeter.log")
        file_handler = logging.handlers.RotatingFileHandler(log_file + "/cgmeter.log", backupCount=5)
        
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        file_handler.setLevel(LOG_LEVEL)
        file_handler.doRollover() if needRoll else None
        logger.addHandler(file_handler)
 
        return logger


if __name__ == "__main__":
    logger = __init_logging()
    logger.info("========== Starting " + APP_NAME + " v" + APP_VERSION + " ==========")
    # Create the main window
    app = CGMainApp()
    app.run()
    logger.info("========== Ending " + APP_NAME + " v" + APP_VERSION + " ==========")