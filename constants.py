'''
 # @ Author: Wilfried Grousson
 # @ Created: 2023-01-11
 # @ License: MIT
 # @ Description: """This module defines project-level constants."""
 '''
import os
import logging

APP_NAME = "CGMeter"
APP_VERSION = "0.1.0"
APP_AUTHOR = "Wilfried Grousson"
APP_CONFIG_DIR = "config"
APP_CG_CONFIG_NAME = "cgconfig.json"
LOG_LEVEL = logging.DEBUG
EMULATE_HX711 = True
APP_CG_FILENAME = os.path.join(os.getcwd(),APP_CONFIG_DIR,APP_CG_CONFIG_NAME)
