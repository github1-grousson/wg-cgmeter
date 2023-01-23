#!/usr/bin/python3
import tkinter as tk
import wgkinter as wk

class CGWindowBase:
    def __init__(self, master=None):
        # build ui
        self.mainwindow = tk.Tk() if master is None else tk.Toplevel(master)
        self.mainwindow.configure(background="#252526")
        self.mainwindow.geometry("800x480")
        self.mainwindow.overrideredirect("True")
        self.top_frame = tk.Frame(self.mainwindow)
        self.top_frame.configure(background="#323233", pady=2)
        self.lb_message = tk.Label(self.top_frame)
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
        self.img = tk.Label(self.content_frame)
        self.img_top_view_800 = tk.PhotoImage(file="gui/top_view_800.png")
        self.img.configure(image=self.img_top_view_800, borderwidth=0)
        self.img.pack(side="top")
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
    app = CGWindowBase()
    app.run()
