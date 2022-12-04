
import logging
from typing import Optional
import tkinter as tk
from theme import theme

class HudInfoC14():
    def __init__(self, logger: logging.Logger) -> None:
        self.logger = logger
        self.parent_frame: Optional[tk.Frame]
        self.fuelMain: Optional[tk.Label]
        self.ShieldsUp: Optional[tk.Label]
        self.HullHealth: Optional[tk.Label]
        self.SurfaceGravity: Optional[tk.Label]
        self.FuelCapacity = 1
        self.ModeSRV = False

    def setup_frame(self, parent: tk.Frame):
        self.parent_frame = parent

        self.fuelMain = tk.Label(self.parent_frame, text="", padx=10)
        self.fuelMain.grid(row=0,sticky=tk.W, column=0)
        self.HullHealth = tk.Label(self.parent_frame, text="", padx=10)
        self.HullHealth.grid(row=0,sticky=tk.W, column=1)
        self.SurfaceGravity = tk.Label(self.parent_frame, text="", padx=10)
        self.SurfaceGravity.grid(row=0,sticky=tk.W, column=2)
        self.ShieldsUp = tk.Label(self.parent_frame, text="", padx=10)
        self.ShieldsUp.grid(row=0,sticky=tk.W, column=3)
        
        theme.update(self.parent_frame)
        
    def set_ModeSRV(self, value: bool):
            self.ModeSRV = value
            
    def set_fuel_main(self, value: float, reserve: float):
        fuel = value + reserve
        if self.FuelCapacity == 1 or self.ModeSRV:
            self.fuelMain.config(text="Fuel: "+str(int(100 * fuel/0.5))+'%')
        else:
            self.fuelMain.config(text="Fuel: "+str(int(100 * fuel / self.FuelCapacity))+'%')
        
    def set_FuelCapacity(self, value: float):
        self.FuelCapacity = value
        
    def set_HullHealth(self, value: float):
        color = "green"
        if value < 0.80:
            color = "orange"
        if value < 0.20:
            color = "red"
        self.HullHealth.config(text="Hull: "+str(int(100 * value))+"%", foreground=color)
        
    def set_ShieldsUp(self, value: bool):
        if value:
            self.ShieldsUp.config(text="Shield UP", foreground='cyan')
        else:
            self.ShieldsUp.config(text="Shield DOWN", foreground='red')
            
    def set_SurfaceGravity(self, value: float):
        if value < 0:
            self.SurfaceGravity.config(text="", foreground='green')
        if value < 1.0:
            self.SurfaceGravity.config(text="G: "+ str(value), foreground='green')
        elif value < 2.0:
            self.SurfaceGravity.config(text="G: "+ str(value), foreground='orange')
        else:
            self.SurfaceGravity.config(text="G: "+ str(value), foreground='red')
