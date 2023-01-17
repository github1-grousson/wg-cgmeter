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
APP_VERSION = "0.2.0"
APP_AUTHOR = "Wilfried Grousson"
APP_CONFIG_DIR = "config"
APP_CG_CONFIG_NAME = "cgconfig.json"
LOG_LEVEL = logging.DEBUG
EMULATE_HX711 = False
APP_CG_FILENAME = os.path.join(os.getcwd(),APP_CONFIG_DIR,APP_CG_CONFIG_NAME)
