'''
 # @ Author: Wilfried Grousson
 # @ Created: 2023-01-11
 # @ License: MIT
 # @ Description: A load cell module
 '''
import logging
import constants
if not constants.EMULATE_HX711:
    from hx711 import HX711
else:
    from modules.hx711_emulator import HX711

class CGModule ():
    def __init__(self):
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

    @property
    def initialized(self):
        return self.__initialized

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

    def initialize(self) -> bool:
        
        result = False
        try:
            self.__logger.debug("Initializing CGModule :%s", self.__name)
            self.__hx = HX711(dout_pin=self.__dout_pin, pd_sck_pin=self.__pd_sck_pin)
            err = self.__hx.zero()
            # check if successful
            if err:
                raise Exception('Tare is unsuccessful during initialization, please check GPIO pins.')

            self.__hx.set_scale_ratio(self.__ratio)
            self.__initialized = True
            self.__logger.debug("CGModule :%s is OK", self.__name)
            result = True
        
        except BaseException as e:
            self.__logger.error("Error initializing CGModule(%s): " + str(e), self.__name)
        
        return result

    def tare(self) :
        try:
            if not self.__initialized:
                raise Exception("not initialized")

            self.__logger.debug("Taring CGModule :%s", self.__name)
            self.__hx.zero()
            self.__logger.debug("Taring Done")
        
        except BaseException as e:
            self.__logger.error("Error taring CGModule(%s): %s",self.__name,str(e))

    def calibrate(self, known_weight_grams : float) :
        try:
            if not self.__initialized:
                raise Exception("not initialized")

            self.__logger.debug("Calibrating CGModule :%s", self.__name)
            reading = self.__hx.get_raw_data_mean()
            if reading:  # always check if you get correct value or only False
                self.__logger.debug('Data subtracted by offset but still not converted to units:%d',reading)
            else:
                raise ValueError('Cannot get raw mean, invalid data')

            reading = self.__hx.get_data_mean()
            if reading:
                self.__logger.debug('Mean value from HX711 subtracted by offset:%d', reading)
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
                self.__logger.debug('Calibration ratio for %s:%f', self.__name, self.__ratio)
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
