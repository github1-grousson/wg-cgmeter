#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
## The main application window

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
import platform
import logging
import logging.handlers
import wgkinter as wk

''' Personal imports '''
from constants import APP_NAME, APP_VERSION, APP_CG_FILENAME
from gui.cgwindowbase import CGWindowBase
from modules.cg_meter import CGMeter
from gui.cgcalibrationwindow import CGCalibrationWindow

class CGMainApp(CGWindowBase):
    """The main application window"""
    def __init__(self, master=None):
        super().__init__(master)
        self.__logger = logging.getLogger(APP_NAME)

        self.version = APP_VERSION
        self.message = "Starting..."
                        
        self.__buttons = {}
        c_vars = vars(self)
        for c_var in c_vars:
            if type(c_vars[c_var]).__name__ == 'Button':
                self.__buttons[c_var] = c_vars[c_var]


        self.disable_buttons()
    
    ''' Private methods call by threads'''
    def __initialize_cggauges(self):
        self.mainwindow.configure(cursor="watch")
        self.mainwindow.update()
        self.message = "Initializing CG gauges..."
        self.__cgmeter = CGMeter(APP_CG_FILENAME)
        self.__cgmeter.initialize()
        self.message = "Inialization done."
        self.message = ""
        self.enable_buttons('btn_calibrate','btn_tare','btn_start', 'btn_exit')
        self.mainwindow.configure(cursor="")

    def __tare_cggauges(self):
        try:
            self.mainwindow.configure(cursor="watch")
            self.mainwindow.update()
            self.message = "Taring CG gauges..."
            self.__cgmeter.tare()
            self.message = "Taring done."
            wk.MessageDialog(self.mainwindow, "CG Meter Tare", "Tare done successfully.")
            
        except BaseException as e:
            self.logger.error("Taring failed: " + str(e))
            wk.MessageDialog(self.mainwindow, "CG Meter Tare", "Tare failed.\n" + str(e))
        finally:
            self.mainwindow.configure(cursor="")
            self.message = ""
            self.enable_buttons('btn_calibrate','btn_tare','btn_start', 'btn_exit')    
       
    ''' Override methods'''
    def run(self):
        self.mainwindow.after(1500, self.__initialize_cggauges)
        uname = platform.uname()
        if uname.system != 'Windows':
            # below, does not work on windows platform
            self.mainwindow.attributes('-topmost', True)
        else:
            self.mainwindow.lift()
            
        super().run()

    ''' Handlers methods'''
    def on_exit(self):
        self.__goodbye()

    def on_calibrate(self):
        self.disable_buttons()
        try:
            cal = CGCalibrationWindow(self.mainwindow)

        except BaseException as e:
            self.__logger.error("Calibration failed: " + str(e))
            wk.MessageDialog(self.mainwindow, "CG Meter Calibration", "Calibration failed.\n" + str(e))
        finally:
            self.enable_buttons('btn_calibrate','btn_tare','btn_start', 'btn_exit')


    def on_tare(self):
        self.disable_buttons()
        answer = wk.YesNoDialog(self.mainwindow, title="CG Meter Tare", question="Remove all weights from the CG meter.\nDo you wan't to continue ?")
        if answer.result == True:
            self.mainwindow.after(500, self.__tare_cggauges)
        else:    
            self.enable_buttons('btn_calibrate','btn_tare','btn_start', 'btn_exit')

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
        self.__logger.debug(value)
        self.lb_message_txt.set(value)
        self.mainwindow.update()

    @property
    def version(self):
        return self.lb_version_txt.get()

    @version.setter
    def version(self, value):
        self.lb_version_txt.set(value)

    ''' Public methods'''
    def disable_buttons(self, *except_buttons):
        for button in self.__buttons:
            if button not in except_buttons:
                self.__buttons[button].config(state="disabled")

    def enable_buttons(self, *which_buttons):
        for button in self.__buttons:
            if button in which_buttons:
                self.__buttons[button].config(state="normal")
        