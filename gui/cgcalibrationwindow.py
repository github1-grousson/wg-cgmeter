#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
## The CG gauges calibration window

Author: Wilfried Grousson
Created Date: 2023/01/20
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
from constants import APP_NAME, APP_ROOT_FOLDER
import tkinter as tk
import wgkinter as wk
from wgkinter.modal import NoTitleBarModalDialog
from modules.cg_meter import CGMeter

class CGCalibrationWindow(NoTitleBarModalDialog):
    """The calibration modal dialog box to calibrate the different modules
    """
    def __init__(self,master=None):
        """constructor

        Args:
            master (tk.Tk, optional): The parent window. Defaults to None.

        """
        super().__init__(master, title = "Calibration",geometry="800x450")

        """DO NOT ADD CODE BELOW THIS LINE AS IT WILL BE CALLED ONLY WHEN DIALOG IS DESTROYED"""
    
    def buttonbox(self, parent):
        """Add the buttons to the dialog box. This method is overriden from the parent class
        
        Args:
            parent (tk.Frame): The parent frame
        """
        btn_ok = wk.Button(parent)
        btn_ok.configure(text='Finish', width=10)
        btn_ok.pack(padx=5, pady=5, side="right")
        btn_ok.configure(command=self.on_ok)
        self.bind("<Return>", self.on_ok)
        self.bind("<Escape>", self.on_cancel)
        parent.pack(fill="x", side="bottom")

    def position(self):
        self.geometry("+0+30")

    def body(self, master):
        """Add the body of the dialog box. This method is overriden from the parent class
        
        Args:
            master (tk.Frame): The parent frame
            
        Returns:
            The initial focus widget
        """
        cal_weight = tk.Frame(master)
        cal_weight.configure(background="#252526", width=300)
        label_weigth = wk.Label(cal_weight)
        label_weigth.configure(text='Enter the calibration weight in grams :')
        label_weigth.pack(side="left")
        entry_weight = wk.Entry(cal_weight)
        self.calibration_weigth = tk.IntVar(value=CGMeter().calibration_weight())
        entry_weight.configure(textvariable=self.calibration_weigth, width=10)
        entry_weight.pack(side="left", ipady=2)
        cal_weight.pack(fill="x", padx=200, pady=20, side="top")
        cal_frame = tk.LabelFrame(master)
        cal_frame.configure(
            background="#252526",
            foreground="white",
            text='Calibrate')
        img = tk.Label(cal_frame)
        logging.getLogger(APP_NAME).debug(f"Loading image {os.path.join(APP_ROOT_FOLDER,'gui','top_view_450.png')}")
        self.img_extra_top_view = tk.PhotoImage(file=os.path.join(APP_ROOT_FOLDER,"gui","top_view_450.png"))
        img.configure(
            borderwidth=0,
            image=self.img_extra_top_view,
            text='label2')
        img.pack(pady=20, side="top")

        btn_rwheel = wk.Button(cal_frame)
        btn_rwheel.configure(text='Right Wheel', width=10)
        btn_rwheel.place(anchor="center", relx=0.25, rely=0.2, x=0, y=0)
        btn_rwheel.configure(command=lambda button="RightWheel": self.on_calibrate(button))
        btn_twheel = wk.Button(cal_frame)
        btn_twheel.configure(text='Tail Wheel', width=10)
        btn_twheel.place(anchor="center", relx=0.86, rely=0.5, x=0, y=0)
        btn_twheel.configure(command=lambda button="TailWheel": self.on_calibrate(button))
        btn_lwheel = wk.Button(cal_frame)
        btn_lwheel.configure(text='Left Wheel', width=10)
        btn_lwheel.place(anchor="center", relx=0.25, rely=0.77, x=0, y=0)
        btn_lwheel.configure(command=lambda button="LeftWheel": self.on_calibrate(button))
        cal_frame.pack(fill="x", padx=100, pady="10 0", side="top")

        self.__buttons = {
            "RightWheel": btn_rwheel,
            "TailWheel": btn_twheel,
            "LeftWheel": btn_lwheel
        }

        return entry_weight

    def __disable_buttons(self):
        for button in self.__buttons.values():
            button.configure(state="disabled")

    def __enable_buttons(self):
        for button in self.__buttons.values():
            button.configure(state="normal")
        
    def on_calibrate(self, module_name):
        logger = logging.getLogger(APP_NAME)
        logger.debug(f"Calbrating {module_name}")
        try:
            known_weight_grams = self.calibration_weigth.get()
        except BaseException as e:
            wk.MessageDialog(self, "Error", "The calibration weight must be a number")
            logger.error(f"The calibration weight must be a number: {str(e)}")
            return

        if known_weight_grams <= 0:
            wk.MessageDialog(self, "Error", "The calibration weight must be greater than 0")
            logger.error("The calibration weight must be greater than 0")
            return
        
        dlg = wk.YesNoDialog(self, "Calibration", f"Calibrate {module_name} with {known_weight_grams} grams ?")
        try:
            if dlg.result is True:
                logger.debug(f"Calibrating module {module_name} with known weight of {known_weight_grams}")
                self.configure(cursor="watch")
                self.__disable_buttons()
                self.update()
                CGMeter().calibrate_module(module_name, known_weight_grams)
                self.configure(cursor="")
                self.__enable_buttons()
                wk.MessageDialog(self, "Calibration", f"{module_name} calibrated with success")
                
        except Exception as e:
            logger.error(f"Error during calibration: {str(e)}")
            wk.MessageDialog(self, "Error", f"Error during calibration : {e}")

  
if __name__ == "__main__":
    raise Exception("This is a module, not a program. It should not be run directly.")