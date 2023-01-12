'''
 # @ Author: Wilfried Grousson
 # @ Created: 2023-01-12
 # @ License: MIT
 # @ Description: The main application window
 '''
import os
import time
import logging
import logging.handlers
import tkinter.messagebox as tk

''' Personal imports '''
from constants import APP_NAME, APP_CG_FILENAME
from gui.cgwindowbase import CGWindowBase
from modules.cg_meter import CGMeter

class CGMainApp(CGWindowBase):
    def __init__(self, master=None):
        super().__init__(master)
        self.__logger = logging.getLogger(APP_NAME)

        self.message = "Starting..."
                
        self.__buttons = {}
        c_vars = vars(self)
        for c_var in c_vars:
            if type(c_vars[c_var]).__name__ == 'Button':
                self.__buttons[c_var] = c_vars[c_var]


        self.disable_buttons('btn_exit')
    
    ''' Private methods'''
    def __initialize_cggauges(self):
        self.message = "Initializing CG gauges..."
        self.mainwindow.update()
        self.__cgmeter = CGMeter(APP_CG_FILENAME)
        self.__cgmeter.initialize()
        self.message = "Inialization done."
        self.message = ""
        self.enable_buttons('btn_calibrate','btn_tare','btn_start')
       
    ''' Override methods'''
    def run(self):
        self.mainwindow.after(1500, self.__initialize_cggauges)
        super().run()

    ''' Handlers methods'''
    def on_exit(self):
        self.__goodbye()

    def on_calibrate(self):
        pass

    def on_tare(self):
        tk.showinfo("Tare", "Tare done")
        pass

    def on_start(self):
        self.btn_start.toogle()
        self.btn_stop.toogle()
        self.btn_exit.disable()
        pass

    def on_stop(self):
        self.btn_start.toogle()
        self.btn_stop.toogle()
        self.btn_exit.enable()
        pass

    ''' Private methods'''
    def __goodbye(self):
        self.mainwindow.destroy()

    ''' Getter/setter Property methods'''
    @property
    def message(self):
        return self.lb_message_txt.get()

    @message.setter
    def message(self, value):
        self.lb_message_txt.set(value)
        self.__logger.debug(value)

    ''' Public methods'''
    def disable_buttons(self, *except_buttons):
        for button in self.__buttons:
            if button not in except_buttons:
                self.__buttons[button].config(state="disabled")

    def enable_buttons(self, *which_buttons):
        for button in self.__buttons:
            if button in which_buttons:
                self.__buttons[button].config(state="normal")
        