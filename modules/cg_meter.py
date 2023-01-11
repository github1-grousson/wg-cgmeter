'''
 # @ Author: Wilfried Grousson
 # @ Created: 2023-01-11
 # @ License: MIT
 # @ Description: a collection of cg gauge modules
 '''
import json
import logging
import constants
from . import cg_gauge

class CGMeter :
    def __init__(self, configfile : str):
        self.__logger = logging.getLogger(constants.APP_NAME)

        self.__configfile = configfile
        self.__load_from_file()

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

    def read(self, callback : callable, whichone : str = 'all') :
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

    def stop(self, whichone : str = 'all'):
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