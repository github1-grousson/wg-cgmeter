#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
## This is the main application entry point

Author: Wilfried Grousson
Created Date: 2023/01/13
Copyright (c) 2023 WG
------------------------------------
MIT License

Copyright (c) 2023 Your Company

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import os
import logging
import logging.handlers

''' Personal imports '''
from constants import APP_NAME, LOG_LEVEL, APP_VERSION, EMULATE_HX711
from gui.cgmainapp import CGMainApp

'''GPIO import'''
if not EMULATE_HX711:
    import RPi.GPIO as GPIO

'''For remote debugging
export DISPLAY=:0;
'''

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
    try:
        # start by initializing the RPi GPIO
        if not EMULATE_HX711:
            GPIO.setmode(GPIO.BCM)

        logger = __init_logging()
        logger.info("========== Starting " + APP_NAME + " v" + APP_VERSION + " ==========")
        # Create the main window
        app = CGMainApp()
        app.run()
        logger.info("========== Ending " + APP_NAME + " v" + APP_VERSION + " ==========")
        
    except Exception as e:
        raise e
    finally:
        if not EMULATE_HX711:
            GPIO.cleanup()