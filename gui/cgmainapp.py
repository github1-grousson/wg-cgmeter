'''
 # @ Author: Wilfried Grousson
 # @ Created: 2023-01-12
 # @ License: MIT
 # @ Description: The main application window
 '''

''' Personal imports '''
from gui.cgwindowbase import CGWindowBase

class CGMainApp(CGWindowBase):
    def __init__(self, master=None):
        super().__init__(master)

        self.message = ""
       
    ''' Override methods'''
    def on_exit(self):
        self.__goodbye()

    def on_calibrate(self):
        pass

    def on_tare(self):
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
