from guizero import App, PushButton, Box, Text, TextBox, Drawing
import logging
import os
import constants
import time
from constants import LOG_LEVEL
from modules import cg_meter
if not constants.EMULATE_HX711:
    import RPi.GPIO as GPIO


"""
export DISPLAY=:0;
"""

class MainWidow:
    def __init__(self):
        
        # Setup logging
        self.__init_logging()
        self.__logger.info("========== Starting " + constants.APP_NAME + " v" + constants.APP_VERSION + " ==========")

        self.app = App()
        #self.app.tk.wm_attributes('-fullscreen','true')
        #self.app.tk.geometry('%dx%d+%d+%d' % (800, 480, 0, 0))
        self.app.tk.geometry("800x480")
        self.app.tk.overrideredirect("True")
        self.app.when_closed = self.goodbye

        self.__init_gui()
        
        self.app.after(1000, self.__initialize_gauges)

    def __init_logging(self):
        self.__logger = logging.getLogger(constants.APP_NAME)
        self.__logger.setLevel(LOG_LEVEL)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s|%(module)s - %(levelname)s - %(message)s'))
        stream_handler.setLevel(LOG_LEVEL)
        self.__logger.addHandler(stream_handler)

        log_file = os.path.join(os.path.realpath(os.path.dirname(__file__)), "log")
        if not os.path.exists(log_file):
            os.makedirs(log_file)

        file_handler = logging.FileHandler(log_file + "/main.log")
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        file_handler.setLevel(LOG_LEVEL)
        self.__logger.addHandler(file_handler)
        
    def __init_gui(self):

        # Title @ top
        self.title_box = Box(self.app, width="fill", align="top", border=True)
        Text(self.title_box, text="WGS CG Meter", size=40, font="Times New Roman", color="black")

        # Content @ center
        self.content_box = Box(self.app, width="fill", align="top", border=False)
        self.message_box = Text(self.content_box, text="")
        self.lwheel_value = Text(self.content_box, text="")
        self.rwheel_value = Text(self.content_box, text="")
        self.twheel_value = Text(self.content_box, text="")
        self.tweight_value = Text(self.content_box, text="")

        
        self.form_box = Box(self.content_box, width="fill", align="left", border=False)
        #Text(self.form_box, grid=[0,1], text="Message:", align="left")
        
        
        # Buttons @ bottom
        self.buttons_box = Box(self.app, width="fill", align="bottom", border=True)
        self.btn_exit = PushButton(self.buttons_box, text="Exit", command=self.on_exit, align="right", padx=50)
        self.btns = {}
        self.btns["cal"] = PushButton(self.buttons_box, text="Calibrate", command=self.on_calibrate, align="left", padx=50, enabled=False)
        self.btns["tare"] = PushButton(self.buttons_box, text="Tare", command=self.on_tare, align="left", padx=50, enabled=False)
        self.btns["read"] = PushButton(self.buttons_box, text="Read", command=self.on_read, align="left", padx=50, enabled=False)
        self.btns["stop"] = PushButton(self.buttons_box, text="Stop", command=self.on_stop, align="left", padx=50, enabled=False)
        

    def __initialize_gauges(self):
        
        try:
            self.message_box.value = "Initializing..."
            self.app.update()
            self.__logger.info("Initializing gauges")
            self.__cgmeter = cg_meter.CGMeter(os.path.join(os.path.dirname(__file__),constants.APP_CONFIG_DIR,constants.APP_CG_CONFIG))
            self.__cgmeter.initialize()
            self.__logger.info("Initializing done")
            self.message_box.value = ""
            for btn in self.btns.values():
                if btn.text != "Stop":
                    btn.enabled = True
            
        except BaseException as e:
            self.__logger.error("Error initializing gauges: " + str(e))

    def display(self):
        self.app.display()

    def goodbye(self):
        self.__logger.info("========== Ending " + constants.APP_NAME + " v" + constants.APP_VERSION + " ==========")
        self.on_stop()
        time.sleep(1)
        self.app.destroy()

    def on_exit(self):
        self.goodbye()

    def on_calibrate(self):
        self.btns["tare"].toggle()
        self.btns["cal"].toggle()
        self.app.update()
        whichone = ['LeftWheel', 'RightWheel']
        for w in whichone:    
            self.app.info("Calibrate", f"Place the calibration weight on the {w} scale")
            value = self.app.question("Calibrate", "What is the weight of the calibration weight (in grams) ?")
            try:
                if value is not None:
                    weight = float(value)
                    self.__cgmeter.calibrate_module(w, weight)
                    self.app.info("Calibrate", "Calibration complete, you can remove the weight")
                
            except ValueError:
                reason = str.format(f'Expected integer or float and I have got:{ value}')
                self.app.error("Calibrate", reason)
            except BaseException as e:
                msg = f"Calibration error : \n{str(e)}"
                self.app.info("Calibrate", msg)
        
        self.btns["tare"].toggle()
        self.btns["cal"].toggle()
           
    def on_tare(self):
        self.btns["tare"].toggle()
        self.btns["cal"].toggle()
        self.app.update()
        
        self.__cgmeter.tare()
        
        self.app.info("Tare", "Tare complete")
        self.btns["tare"].toggle()
        self.btns["cal"].toggle()

    def on_read(self):
        for btn in self.btns.values():
            btn.disable()
        
        self.btns["stop"].enable()
        #self.__cgmeter.read_by_module(self.on_weight_update_module)
        self.__cgmeter.start_reading(self.on_weights_update)
        
    def on_stop(self):
        for btn in self.btns.values():
            btn.enable()
        self.btns["stop"].disable()
        #self.__cgmeter.stop_by_module()
        self.__cgmeter.stop_reading()

    def on_weights_update(self, weights):
        try:
            if weights is None:
                self.rwheel_value.value = ""
                self.lwheel_value.value = ""
                self.twheel_value.value = ""
                self.tweight_value.value = ""
            else:
                total_weight = 0
                for mod_name, weight in weights.items():
                    if mod_name == "LeftWheel":
                        self.lwheel_value.value = f'{mod_name}: {round(weight,1)} g'
                        total_weight += weight
                    elif mod_name == "RightWheel":
                        self.rwheel_value.value = f'{mod_name}: {round(weight,1)} g'
                        total_weight += weight
                    elif mod_name == "TailWheel":
                        self.twheel_value.value = f'{mod_name}: {round(weight,1)} g'
                        total_weight += weight
                
                self.tweight_value.value = f'Total weight: {round(total_weight,1)} g'

                self.app.update()
        except BaseException as e:
                self.__logger.error("Error updating weights: " + str(e))

                
    def on_weight_update_module(self, name, weight):
        try:
            if name == "LeftWheel":
                self.lwheel_value.value = f'{name}: {round(weight,1)} g'
            elif name == "RightWheel":
                self.rwheel_value.value = f'{name}: {round(weight,1)} g'
            else:
                self.message_box.value = f'{name}: Unknown module' 
            self.app.update()
        except BaseException as e:
            self.__logger.error("Error updating weight: " + str(e))
        
if __name__ == "__main__":
    try:
        if not constants.EMULATE_HX711:
            GPIO.setmode(GPIO.BCM)
        main_window = MainWidow()
        main_window.display()
        SystemExit(0)
    except Exception as e:
        print(e)
    finally:
        if not constants.EMULATE_HX711:
            GPIO.cleanup()