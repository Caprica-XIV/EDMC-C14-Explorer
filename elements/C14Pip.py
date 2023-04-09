import logging
from typing import Optional
import tkinter as tk
from theme import theme

class PipC14():
    def __init__(self, logger: logging.Logger, scale: int):
        self.logger = logger
        self.ui_scale = scale
        self.parent_frame: Optional[tk.Frame]
        self.pip_canvas: Optional[tk.Canvas]
        self.sys = 0
        self.mot = 0
        self.arm = 0
        self.value = 0
        self.prev_value = 0

    def scale(self, value: int) -> int:
        return int(value * self.ui_scale / 100.0)

    def setup_frame(self, parent: tk.Frame):
        self.parent_frame = parent
        self.pip_canvas = tk.Canvas(self.parent_frame, 
                                    height=self.scale(50), 
                                    width=self.scale(30), 
                                    border=None, borderwidth=0)
        self.pip_canvas.grid(row=0, sticky=tk.W, column=4)
        theme.update(self.parent_frame)
    
    def popup(self):
        # self.pip_canvas.grid(row=0, sticky=tk.W, column=0)
        a = 2
    
    def dismiss(self):
        # self.pip_canvas.grid_remove()
        self.pip_canvas.delete('all')
        
    def set_pip(self, sys: int, mot: int, arm: int):
        self.sys = sys
        self.arm = arm
        self.mot = mot
        self.value = int(str(sys)+str(mot)+str(arm))
        self.update_pip_canvas()

    def draw_tick(self, x: int, y: int):
        col = "yellow"
        if y < 40:
            col = "orange"
        if y < 20:
            col = "red"
        self.pip_canvas.create_rectangle(self.scale(x),   self.scale(y), 
                                         self.scale(x+8), self.scale(y+4), 
                                         fill=col)
    
    def draw_pip(self, index: int, val: int):
        x = index * 10 + 2
        y = 2
        if val > 0:
            for i in range(0, val):
                self.draw_tick(x, 50-y)
                y += 5

    def update_pip_canvas(self):
        if self.value == self.prev_value:
            return
        self.prev_value = self.value
        self.pip_canvas.delete('all')
        self.draw_pip(0,self.sys)
        self.draw_pip(1,self.mot)
        self.draw_pip(2,self.arm)