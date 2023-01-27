#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
## This module defines project-level constants.

Author: Wilfried Grousson
Created Date: 2023/01/13
------------------------------------
MIT License

Copyright (c) 2023 WG

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

APP_NAME = "CGMeter"
APP_VERSION = "0.3.0"
APP_AUTHOR = "Wilfried Grousson"
APP_CONFIG_DIR = "config"
LOG_LEVEL = logging.DEBUG
EMULATE_HX711 = False
APP_ROOT_FOLDER = os.path.dirname(os.path.abspath(__file__))
APP_CG_FILENAME = os.path.join(APP_ROOT_FOLDER,APP_CONFIG_DIR,"cgconfig.json")
APP_PLANES_FILENAME = os.path.join(APP_ROOT_FOLDER,APP_CONFIG_DIR,"planes.json")

ORIGIN = (244, 204) #this is the wing leading edge screen coordinates
RWHEEL = (225, 100)  #this is right wheel screen coordinates
LWHEEL = (225, 300) #this is left wheel screen coordinates
TWHEEL = (660, 204) #this is tail wheel screen coordinates
NOSE = (80, 204)    #this is nose screen coordinates

SCREEN_COORDINATES = {'ORIGIN': ORIGIN, 'RWHEEL': RWHEEL, 'LWHEEL': LWHEEL, 'TWHEEL': TWHEEL, 'NOSE': NOSE}

if __name__ == "__main__":
    raise Exception("This is a module, not a program. It should not be run directly.")