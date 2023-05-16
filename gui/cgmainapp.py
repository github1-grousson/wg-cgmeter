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
import time
import platform
import logging
import logging.handlers

''' Personal imports '''
import wgkinter as wk
from constants import APP_NAME, APP_VERSION, APP_CG_FILENAME, MAIN_PLANE
from gui.cgwindowbase import CGWindowBase
from modules.cg_meter import CGMeter
from gui.cgcalibrationwindow import CGCalibrationWindow
from utils.planemanager import PlaneManager
from utils.drawings import Circle, RoundedRectangle

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

        self.ref_cg_dwg = None
        self.cg_dwg = None
    
    ''' Private methods call by threads'''
    def __initialize_cgmeter(self):
        self.mainwindow.configure(cursor="watch")
        self.mainwindow.update()
        self.message = "Loading default plane..."
        #initalize the plane manager & UI
        PlaneManager().load()
        try:
            PlaneManager().set_current_plane_by_name(MAIN_PLANE)
        except ValueError as ve:
            self.__logger.error("Error loading plane: " + str(ve))
            self.message = "Error loading  plane: " + MAIN_PLANE +", loading default"            
        except BaseException as e:
            self.__logger.error("Error loading plane: " + str(e))

        self.__update_UI()

        self.message = "Initializing CG gauges..."
        CGMeter().initialize(APP_CG_FILENAME)
                
        self.message = "Inialization done."
        self.message = ""
        self.enable_buttons('btn_calibrate','btn_tare','btn_start', 'btn_exit')
        self.mainwindow.configure(cursor="")

    def __tare_cggauges(self):
        try:
            self.mainwindow.configure(cursor="watch")
            self.mainwindow.update()
            self.message = "Taring CG gauges..."
            CGMeter().tare()
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
        self.mainwindow.after(1500, self.__initialize_cgmeter)
        uname = platform.uname()
        if uname.system != 'Windows':
            # below, does not work on windows platform
            self.mainwindow.attributes('-topmost', True)
        else:
            self.mainwindow.lift()

        #self.mainwindow.bind('<Motion>', self.on_motion)
            
        super().run()

    ''' Handlers methods'''
    def on_motion(self, event):
        self.message = ("x: " + str(event.x) + " y: " + str(event.y))
        
        if self.cg_dwg is not None:
            self.cg_dwg.move_to((event.x, event.y))
        
    def on_exit(self):
        self.__goodbye()

    def on_calibrate(self):
        self.disable_buttons()
        try:
            CGCalibrationWindow(self.mainwindow)

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
        self.disable_buttons('btn_stop')
        self.enable_buttons('btn_stop')

        for key in self.lb_weights:
            self.lb_weights[key].place_show()

        for label in self.lb_cg_position:
            label.place_show()

        self.cg_dwg.show()

        self.message = "Reading..."
        CGMeter().start_reading(self.on_display_readings)
                
    def on_stop(self):
        
        CGMeter().stop_reading()

        time.sleep(1.5)

        for key in self.lb_weights:
            self.lb_weights[key].place_hide()

        for label in self.lb_cg_position:
            label.place_hide()

        self.cg_dwg.move_to((-100,-100))
        self.cg_dwg.change_color('white')
        self.cg_dwg.hide()

        self.disable_buttons()
        self.enable_buttons('btn_calibrate','btn_tare','btn_start', 'btn_exit')
        self.message = ""
        
    def on_display_readings(self, weights):
        try:
            if weights is not None:
                self.__display_weights_values(weights)
                CGpos = self.__display_cg_values(weights)
                if CGpos is not None:
                    self.__draw_cg(CGpos)

        except BaseException as e:
                self.__logger.error("Error displaying results: " + str(e))
                
        finally:
            self.mainwindow.update()

    ''' Private methods'''
    def __update_UI(self):
        plane = PlaneManager().get_current_plane()

        if plane is None:
            raise Exception("No plane defined.")

        self.lb_model_name.set(plane.name)


        point1 = (plane.cgx_range[0], plane.cgy_range[1])
        point2 = (plane.cgx_range[1], plane.cgy_range[0])

        point1 = plane.mm_to_screen(point1)
        point2 = plane.mm_to_screen(point2)
        
        if self.ref_cg_dwg is not None:
            self.ref_cg_dwg.delete()

        self.ref_cg_dwg = RoundedRectangle(self.canvas, point1, point2, color = '#007fd4')
        self.ref_cg_dwg.draw()

        if self.cg_dwg is not None:
            self.cg_dwg.delete()

        self.cg_dwg = Circle(self.canvas, plane.mm_to_screen((0,0)))
        self.cg_dwg.draw()
        self.cg_dwg.hide()

    def __display_weights_values(self, weights):
        try:
            if weights is None:
                for key in self.lb_weights:
                    self.lb_weights[key].text = ""
                
            else:
                total_weight = 0
                mwheels_weight = 0
                for mod_name, weight in weights.items():
                    if mod_name == "LeftWheel":
                        self.lb_weights[mod_name].text = f'{int(round(weight))} g'
                        mwheels_weight += weight
                        total_weight += weight
                    elif mod_name == "RightWheel":
                        self.lb_weights[mod_name].text = f'{int(round(weight))} g'
                        mwheels_weight += weight
                        total_weight += weight
                    elif mod_name == "TailWheel":
                        self.lb_weights[mod_name].text = f'{int(round(weight))} g'
                        total_weight += weight
                
                self.lb_weights['mwheels'].text = f'{int(round(mwheels_weight))} g'
                self.lb_weights['total'].text = f'{int(round(total_weight))} g'
                
        except BaseException as e:
                self.__logger.error("Error displaying weights: " + str(e))
                
    def __display_cg_values(self, weights) -> tuple[int,int]:
        try:
            the_plane = PlaneManager().get_current_plane()
            CG = the_plane.plane_cg_by_weigth(weights)
            
            # we start with the x axis
            CGx = CG[0]
            CGXmin = the_plane.cgx_range[0]
            CGXmax = the_plane.cgx_range[1]
            cgx_text = ""
            if CGx < CGXmin:
                cgx_text = f'{CGx} mm [ {CGXmin} - {CGXmax} ]'
            elif CGx > CGXmax:
                cgx_text = f'[ {CGXmin} - {CGXmax} ] {CGx} mm'
            else:
                cgx_text = f'{CGXmin} [ {CGx} mm ] {CGXmax}'

            if self.lb_cg_position[0] is not None:
                self.lb_cg_position[0].text = cgx_text
                self.lb_cg_position[0]['foreground'] = the_plane.color_in_range(CGx,'x')
            
            # now the y axis                     
            if self.lb_cg_position[1] is not None:
                self.lb_cg_position[1].text = f'{CG[1]} mm'
                self.lb_cg_position[1]['foreground'] = the_plane.color_in_range(CG[1],'y')
                        
            return CG

        except BaseException as e:
            self.__logger.debug("Error displaying CG positions: " + str(e))
            self.lb_cg_position[0].text = f'NaN'
            self.lb_cg_position[0]['foreground'] = 'white'
            self.lb_cg_position[1].text = f'NaN'
            self.lb_cg_position[1]['foreground'] = 'white'
            return None

    def __draw_cg(self, cg_position : tuple[int,int]):
        try:
            plane = PlaneManager().get_current_plane()
            self.cg_dwg.move_to(plane.mm_to_screen(cg_position))
            self.cg_dwg.change_color(plane.color_in_range(cg_position[0],'x'))
           
        except BaseException as e:
            self.__logger.debug("Error drawing CG: " + str(e))     

    def __goodbye(self):
        self.mainwindow.destroy()

    ''' Getter/setter Property methods'''
    @property
    def message(self):
        return self.lb_message_txt.get()

    @message.setter
    def message(self, value):
        self.__logger.info(value)
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
        
if __name__ == "__main__":
    raise Exception("This is a module, not a program. It should not be run directly.")