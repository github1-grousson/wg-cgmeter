#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
## a collection of cg gauge modules

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

import json
import logging
import constants
import threading
import time
from . import cg_gauge

class Singleton:
    _instance = None

    def  __new__(cls):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance

class CGMeter(Singleton) :
    _initialize = False

    def __load_from_file(self):
        self.__logger.debug("Loading CGMeter config from file: %s", self.__configfile)

        try:
            with open(self.__configfile, "r") as f:
                data = json.load(f)
                self.__load_from_dict(data["Modules"])
                self.__calibration_weight = data["CalibrationWeight"]
        except Exception as e:
            self.__logger.error("Error loading CGMeter config: " + str(e))
            raise e

    def __load_from_dict(self, data : dict):
        self.__modules = []
        try:
            for module in data:
                cgmod = cg_gauge.CGModule()
                cgmod.loadConfig(module, data[module])
                self.__modules.append(cgmod)

        except Exception as e:
            self.__logger.error("Error loading CGMeter config: " + str(e))

    def __read_modules(self, callback : callable):
        self.__logger.debug("CGMeter reading thread started")
        while self.__running:

            values = {}
            for module in self.__modules:
                if module.initialized:
                    values[module.name] = module.getWeight(6)
                    if values[module.name] is False:
                        print("Error reading module: " + module.name)
            
            callback(values)
            time.sleep(0.1)
        
        callback(None)
        self.__logger.debug("CGMeter reading thread stopped")
        
    def initialize(self,configfile : str, whichone : str = 'all'):
        if self._initialize:
            raise Exception("CGMeter already initialized")

        self.__logger = logging.getLogger(constants.APP_NAME)
        self.__running = False
        self._initialize = True

        try:
            self.__configfile = configfile
            self.__load_from_file()

            if whichone == 'all':
                for module in self.__modules:
                    module.initialize()
            else:
                for module in self.__modules:
                    if module.name == whichone:
                        module.initialize()
                        break
        except Exception as e:
            self.__logger.error("Error initializing CGMeter: " + str(e))

    def calibrate_module(self, module_name : str, known_weight_grams : float):
        try:
            for module in self.__modules:
                if module.name == module_name:
                    module.calibrate(known_weight_grams)
                    with open(self.__configfile, "r") as json_file:
                        data = json.load(json_file)
                    module.saveConfig(data["Modules"][module.name])
                    with open(self.__configfile, "w") as json_file:
                        json.dump(data, json_file, indent=4)
                    break
        except Exception as e:
            self.__logger.error("Error calibrating CGMeter module(%s):%s",module_name, str(e))
            raise e
        
    def tare(self, whichone : str = 'all'):
        try:
            if whichone == 'all':
                for module in self.__modules:
                    module.tare()
            else:
                for module in self.__modules:
                    if module.name == whichone:
                        module.tare()
                        break
        except Exception as e:
            self.__logger.error("Error taring CGMeter: " + str(e))

    def start_reading(self, callback : callable):
        #check at least if one module is initialized, otherwise raise exception
        initok = False
        for module in self.__modules:
            if module.initialized:
                initok = True
                break
        
        if not initok:
            raise Exception("No module initialized")

        try:
            self.__running = True
            self.__thread = threading.Thread(name='CGMeterThread',target=self.__read_modules, args=(callback,))
            self.__thread.start()
        except Exception as e:
            self.__logger.error("Error starting thread CGMeter: " + str(e))

    def stop_reading(self):
        if self.__running:
            self.__running = False
            #self.__thread.join()

    
    def calibration_weight(self):
        return self.__calibration_weight

    
    
    """Perhaps below this line should be deprecated in future ? Is there a need to thread 1 module reading ?"""
    def read_by_module(self, callback : callable, whichone : str = 'all') :
        try:
            if whichone == 'all':
                for module in self.__modules:
                    module.start(callback)
            else:
                for module in self.__modules:
                    if module.name == whichone:
                        module.start(callback)
                        break
        except Exception as e:
            self.__logger.error("Error reading CGMeter: " + str(e))

    def stop_by_module(self, whichone : str = 'all'):
        try:
            if whichone == 'all':
                for module in self.__modules:
                    module.stop()
            else:
                for module in self.__modules:
                    if module.name == whichone:
                        module.stop()
                        break
        except Exception as e:
            self.__logger.error("Error stopping CGMeter: " + str(e))

    
if __name__ == "__main__":
    raise Exception("This is a module, not a program. It should not be run directly.")