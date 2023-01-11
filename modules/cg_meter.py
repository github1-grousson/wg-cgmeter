'''
 # @ Author: Wilfried Grousson
 # @ Created: 2023-01-11
 # @ License: MIT
 # @ Description: a collection of cg gauge modules
 '''
 
import json
import logging
import constants
import threading
import time
from . import cg_gauge

class CGMeter :
    def __init__(self, configfile : str):
        self.__logger = logging.getLogger(constants.APP_NAME)

        self.__configfile = configfile
        self.__load_from_file()

        self.__running = False

    def __load_from_file(self):
        self.__logger.debug("Loading CGMeter config from file: %s", self.__configfile)

        try:
            with open(self.__configfile, "r") as f:
                data = json.load(f)
                self.__load_from_dict(data["Modules"])
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
                    values[module.name] = module.getWeight(10)
            
            callback(values)
            time.sleep(0.1)
        
        callback(None)
        self.__logger.debug("CGMeter reading thread stopped")
        
    def initialize(self, whichone : str = 'all'):
        try:
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

    