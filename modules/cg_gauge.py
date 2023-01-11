'''
 # @ Author: Wilfried Grousson
 # @ Created: 2023-01-11
 # @ License: MIT
 # @ Description: A load cell module
 '''


import time
import logging
import constants
from hx711 import HX711

class CGModule ():
    def __init__(self):
        #self.__running = False
        self.__name = "Unknown"
        self.__ratio = 0.0
        self.__dout_pin = 0
        self.__pd_sck_pin = 0
        self.__position = [0.0,0.0]
        self.__logger = logging.getLogger(constants.APP_NAME)
        self.__initialized = False
       
    def __set_values__(self, data : dict):
        try:
            self.__ratio = data["ratio"]
            self.__dout_pin = data["gpio"]["dt"]
            self.__pd_sck_pin = data["gpio"]["sck"]
            self.__position = data["position"]

        except Exception as e:
            self.__logger.error("Error setting CGModule(%s) values: " + str(e), self.__name)

    def __write_values__(self, data : dict):
        try:
            data["ratio"] = self.__ratio
            data["gpio"]["dt"] = self.__dout_pin
            data["gpio"]["sck"] = self.__pd_sck_pin
            data["position"] = self.__position

        except Exception as e:
            self.__logger.error("Error writing CGModule(%s) values: " + str(e), self.__name)

    ''' Deprecate module threading
    def displayValue(self, callback):
        self.__logger.debug("CGModule(%s) started", self.__name)
        self.__running = True
        while self.__running:
            weight = self.getWeight(10)
            #self.__logger.info("CGModule(%s) weight:%.2f", self.__name, weight)
            callback(self.__name, weight)
            time.sleep(0.01)

        callback(self.__name, 0.0)
        #del self.__thread
        self.__logger.debug("CGModule(%s) stopped", self.__name)
        return
    

    def start(self, callback : callable):
        try:
            if not self.__initialized:
                raise Exception("Not initialized")

            self.__running = True
            self.__thread = threading.Thread(name=f'CGModule{self.__name}Thread',target=self.displayValue, args=(callback,))
            self.__thread.start()

        except BaseException as e:
            self.__logger.error("Error starting CGModule(%s): %s", self.__name,  str(e))

    def stop(self):
        try:
            if not self.__initialized:
                raise Exception("Not initialized")
        
            self.__running = False
            #self.__thread.join()
            #del self.__thread
        
        except BaseException as e:
            self.__logger.error("Error stopping CGModule(%s): %s", self.__name,  str(e))

    def wait(self):
        self.__thread.join()
    '''

    @property
    def name(self):
        return self.__name

    @property
    def ratio(self):
        return self.__ratio
    
    @ratio.setter
    def ratio(self, value):
        self.__ratio = value

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = value

    """
    def loadConfig_Deprecated(self, configfilename : str, config : str = "Default"):
        try:
            with open(configfilename) as json_file:
                data = json.load(json_file)
                self.__name = config
                self.__set_values__(data["Modules"][config])
                
        except Exception as e:
            self.__logger.error("Error loading CGModule(%s) config: " + str(e), self.__name)
    """

    def loadConfig(self, config : str, module_cfg : dict):
        try:
            self.__name = config
            self.__set_values__(module_cfg)

        except Exception as e:
            self.__logger.error("Error loading CGModule(%s) config: " + str(e), self.__name)

    def saveConfig(self, module_cfg : dict):
        try:         
            
            self.__write_values__(module_cfg)

        except Exception as e:
            self.__logger.error("Error saving CGModule(%s) config: %s", self.__name,  str(e))

    """
    def saveConfig_Deprecated(self, configfilename : str):
        try:
            
            with open(configfilename, "r") as json_file:
                data = json.load(json_file)
            
            self.__write_values__(data["Modules"][self.__name])

            with open(configfilename, "w") as json_file:
                json.dump(data, json_file, indent=4)
        
        except Exception as e:
            self.__logger.error("Error saving CGModule(%s) config: " + str(e), self.__name)
    """

    def initialize(self) -> bool:
        
        result = False
        try:
            self.__logger.info("Initializing CGModule :%s", self.__name)
            self.__hx = HX711(dout_pin=self.__dout_pin, pd_sck_pin=self.__pd_sck_pin)
            err = self.__hx.zero()
            # check if successful
            if err:
                raise Exception('Tare is unsuccessful during initialization, please check GPIO pins.')

            self.__hx.set_scale_ratio(self.__ratio)
            self.__initialized = True
            result = True
        
        except BaseException as e:
            self.__logger.error("Error initializing CGModule(%s): " + str(e), self.__name)
        
        return result

    def tare(self) :
        try:
            if not self.__initialized:
                raise Exception("not initialized")

            self.__logger.info("Taring CGModule :%s", self.__name)
            self.__hx.zero()
            self.__logger.info("Taring Done")
        
        except BaseException as e:
            self.__logger.error("Error taring CGModule(%s): %s",self.__name,str(e))

    def calibrate(self, known_weight_grams : float) :
        try:
            if not self.__initialized:
                raise Exception("not initialized")

            self.__logger.info("Calibrating CGModule :%s", self.__name)
            reading = self.__hx.get_raw_data_mean()
            if reading:  # always check if you get correct value or only False
                self.__logger.debug('Data subtracted by offset but still not converted to units:%d',reading)
            else:
                raise ValueError('Cannot get raw mean, invalid data')

            reading = self.__hx.get_data_mean()
            if reading:
                self.__logger.info('Mean value from HX711 subtracted by offset:%d', reading)
                try:
                    value = float(known_weight_grams)
                    self.__logger.debug('Calibration weight %f grams',value)
                except ValueError:
                    reason = str.format(f'Expected integer or float and I have got:{ known_weight_grams}')
                    raise ValueError(reason)

                # set scale ratio for particular channel and gain which is
                # used to calculate the conversion to units. Required argument is only
                # scale ratio. Without arguments 'channel' and 'gain_A' it sets
                # the ratio for current channel and gain.
                self.__ratio = reading / value  # calculate the ratio for channel A and gain 128
                self.__logger.info('Calibration ratio for %s:%f', self.__name, self.__ratio)
                self.__hx.set_scale_ratio(self.__ratio)  # set ratio for current channel
            
            else:
                raise ValueError('Cannot calculate mean value. Try debug mode. Variable reading:%s', str(reading))

            self.__logger.info("Calibration Done")
        
        except BaseException as e:
            self.__logger.error("Error calibrating CGModule(%s): %s ", self.__name, str(e))
            raise e

    def getWeight(self, readings : int = 30) -> float:
        
        result = 0.0
        try:
            if not self.__initialized:
                raise Exception("not initialized")
                
            result = self.__hx.get_weight_mean(readings)

        except BaseException as e:
            self.__logger.error("Error getting CGModule(%s) weight: %s", self.__name,  str(e))
        
        return result
