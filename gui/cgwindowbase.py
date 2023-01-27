#!/usr/bin/python3
import os
import tkinter as tk
import wgkinter as wk
import logging
from PIL import Image, ImageTk
import constants as const

class CGWindowBase:
    def __init__(self, master=None):
        # build ui
        self.mainwindow = tk.Tk() if master is None else tk.Toplevel(master)
        self.mainwindow.configure(background="#252526")
        self.mainwindow.geometry("800x480+0+0")
        self.mainwindow.attributes('-fullscreen', True)
        #self.mainwindow.overrideredirect("True")
        self.top_frame = tk.Frame(self.mainwindow)
        self.top_frame.configure(background="#323233", pady=2)
        
        self.lb_message = tk.Label(self.mainwindow)
        self.lb_message_txt = tk.StringVar()
        self.lb_message.configure(
            background="#323233",
            font="{Arial} 10 {italic}",
            foreground="white",
            textvariable=self.lb_message_txt)
        self.lb_message.place(anchor="nw", x=1, y=4)
        
        frame1 = tk.Frame(self.top_frame)
        frame1.configure(background="#323233")
        self.lb_title = tk.Label(frame1)
        self.lb_title.configure(
            background="#323233",
            font="{Arial} 14 {}",
            foreground="white",
            text='CG Meter')
        self.lb_title.pack(side="left")
        self.lb_version = tk.Label(frame1)
        self.lb_version_txt = tk.StringVar(value='v0.0')
        self.lb_version.configure(
            background="#323233",
            font="{Arial} 8 {}",
            foreground="white",
            text='v0.0',
            textvariable=self.lb_version_txt)
        self.lb_version.pack(anchor="s", side="left")
        frame1.grid(column=0, row=0)
        self.lb_author = tk.Label(self.top_frame)
        self.lb_author.configure(
            background="#323233",
            font="{Arial} 6 {italic}",
            foreground="white",
            text='by WGS')
        self.lb_author.grid(column=1, row=0, sticky="s", padx="0 5")
        self.top_frame.pack(fill="x", side="top")
        self.top_frame.columnconfigure(0, weight=1)
        
        self.content_frame = tk.Frame(self.mainwindow)
        self.content_frame.configure(background="#252526")
        # self.img = tk.Label(self.content_frame)
        # self.img_top_view_800 = tk.PhotoImage(file="gui/top_view_800.png")
        # self.img.configure(image=self.img_top_view_800, borderwidth=0)
        # self.img.pack(side="top")
        logging.getLogger(const.APP_NAME).debug(f"Loading image {os.path.join(const.APP_ROOT_FOLDER,'gui','top_view_800.png')}")
        self.img = Image.open(os.path.join(const.APP_ROOT_FOLDER,"gui","top_view_800.png"))
        self.sketch = ImageTk.PhotoImage(self.img)
        self.canvas = tk.Canvas(self.content_frame, width=self.img.size[0], height=self.img.size[1])
        self.canvas.create_image(0, 0, image=self.sketch, anchor="nw")
        self.canvas.configure(background="#252526", borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top",fill="both", expand="yes")

        self.lb_cg_position = []
        self.lb_cg_position.append(wk.Label(self.content_frame))
        self.lb_cg_position.append(wk.Label(self.content_frame))
        for i in range(2):
            self.lb_cg_position[i].configure(highlightbackground="#007fd4", highlightthickness=1, text=f'{0} mm')
        
        self.lb_cg_position[0].place(anchor="w", relx=0, rely=0, x=const.ORIGIN[0], y=20, width=200)
        self.lb_cg_position[1].place(anchor="w", relx=0, rely=0.5, width=80)

        self.lb_weights = {}
        self.lb_weights['total'] = wk.Label(self.content_frame)
        self.lb_weights['mwheels'] = wk.Label(self.content_frame)
        self.lb_weights['RightWheel'] = wk.Label(self.content_frame)
        self.lb_weights['TailWheel'] = wk.Label(self.content_frame)
        self.lb_weights['LeftWheel'] = wk.Label(self.content_frame)
        for key in self.lb_weights:
            self.lb_weights[key].configure(highlightbackground="#007fd4", highlightthickness=1, text=f'{0} g')
            self.lb_weights[key].place(anchor="center", relx=0, rely=0, width=80)
        
        self.lb_weights['RightWheel'].place(x=const.RWHEEL[0], y=const.RWHEEL[1])
        self.lb_weights['LeftWheel'].place(x=const.LWHEEL[0], y=const.LWHEEL[1])
        self.lb_weights['TailWheel'].place(x=const.TWHEEL[0], y=const.TWHEEL[1])
        self.lb_weights['mwheels'].place(x=const.LWHEEL[0], y=378)
        self.lb_weights['total'].place(x=378, y=378)

        for key in self.lb_weights:
            self.lb_weights[key].place_hide()

        self.content_frame.pack(
            expand="true",
            fill="both",
            padx=5,
            pady=5,
            side="top")
        self.bottom_frame = tk.Frame(self.mainwindow)
        self.bottom_frame.configure(background="#252526", height=30)
        self.btn_calibrate = wk.Button(self.bottom_frame)
        self.btn_calibrate.configure(text='Calibrate', width=10)
        self.btn_calibrate.pack(padx="3 0", side="left")
        self.btn_calibrate.configure(command=self.on_calibrate)
        self.btn_tare = wk.Button(self.bottom_frame)
        self.btn_tare.configure(text='Tare', width=10)
        self.btn_tare.pack(padx="3 0", side="left")
        self.btn_tare.configure(command=self.on_tare)
        self.btn_start = wk.Button(self.bottom_frame)
        self.btn_start.configure(text='Start', width=5)
        self.btn_start.pack(padx="30 0", side="left")
        self.btn_start.configure(command=self.on_start)
        self.btn_stop = wk.Button(self.bottom_frame)
        self.btn_stop.configure(text='Stop', width=5)
        self.btn_stop.pack(side="left")
        self.btn_stop.configure(command=self.on_stop)
        self.btn_exit = wk.Button(self.bottom_frame)
        self.btn_exit.configure(text='Exit', width=10)
        self.btn_exit.pack(padx=3, pady=3, side="right")
        self.btn_exit.configure(command=self.on_exit)
        self.bottom_frame.pack(fill="x", side="top")

        # Main widget
        self.root = self.mainwindow
        self.mainwindow = self.mainwindow
        

    def run(self):
        self.mainwindow.mainloop()

    def on_calibrate(self):
        pass

    def on_tare(self):
        pass

    def on_start(self):
        pass

    def on_stop(self):
        pass

    def on_exit(self):
        pass


if __name__ == "__main__":
    raise Exception("This is a module, not a program. It should not be run directly.")
