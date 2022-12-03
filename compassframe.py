import logging
import threading
import tkinter as tk
from typing import Optional
from theme import theme

class CompassFrame(tk.Tk):
    def __init__(self, logger: logging.Logger, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.logger = logger
        self.w=500
        self.h=80
        self.Heading = -1
        self.frame: Optional[tk.Frame]
        self.canvas: Optional[tk.Canvas]
        self.attributes('-topmost',True)
        self.overrideredirect(True)
        self.attributes('-alpha', 0.7)
        # get screen width and height
        # calculate x and y coordinates for the Tk root window
        ws = self.winfo_screenwidth() # width of the screen
        x = (ws/2) - (self.w/2)
        self.geometry('%dx%d+%d+%d' % (self.w, self.h, x, 40))
        
    def setup_frame(self):
        self.frame = tk.Frame(self, width=self.w, height=self.h)
        self.frame.pack(side="top", fill="both", expand = True)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.canvas = tk.Canvas(self.frame, width=self.w, height=(self.h-20))
        self.canvas.grid(row=0, sticky=tk.W, column=0)
        self.canvas.bind('<<C14CompassFrameUpdate>>', self.on_compassframe_update)
        theme.update(self.frame)
        
    def set_Heading(self, value: int):
        self.Heading = value
        # self.on_compassframe_update()
        threading.Thread(target=self.launcher, daemon=True).start()
    
    def launcher(self):
        self.canvas.event_generate('<<C14CompassFrameUpdate>>', when='now')
        
    def on_compassframe_update(self):
        self.canvas.delete('all')
        self.canvas.create_text(50, 45, text='Has been update', fill='orange', font='Arial 10')
        self.logger.info("sisi le canvas est a jour")
    
