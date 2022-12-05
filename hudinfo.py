import logging
import tkinter as tk
import threading
from typing import Optional
from time import sleep
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
        self.Hull = 100
        self.Fuel = 100
        self.Shield = True

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
            self.Fuel = int(100 * fuel/0.5)
        else:
            self.Fuel = int(100 * fuel / self.FuelCapacity)
        if self.Fuel > 100.0:
            self.Fuel = int(fuel*100) / 100.0
        color = "green"
        if self.Fuel < 80:
            color = "orange"
        if self.Fuel < 20:
            color = "red"
            threading.Thread(target=self.fuel_blink, daemon=True, name='C14 fuel blink').start()
        self.fuelMain.config(text="Fuel: "+str(self.Fuel)+'%', foreground=color)
        
    def set_FuelCapacity(self, value: float):
        self.FuelCapacity = value
        
    def set_HullHealth(self, value: float):
        self.hull = int(100 * value)
        color = "green"
        if value < 0.80:
            color = "orange"
        if value < 0.20:
            color = "red"
            threading.Thread(target=self.hull_blink, daemon=True, name='C14 hull blink').start()
        self.HullHealth.config(text="Hull: "+str(self.hull)+"%", foreground=color)
        
    def set_ShieldsUp(self, value: bool):
        this.Shield = value
        if value:
            self.ShieldsUp.config(text="Shield UP", foreground='cyan')
        else:
            self.ShieldsUp.config(text="Shield DOWN", foreground='red')
            threading.Thread(target=self.shield_blink, daemon=True, name='C14 shield blink').start()
            
    def set_SurfaceGravity(self, value: float):
        g = int(value*10+0.5) / 100.0
        # g = value
        if g < 0:
            self.SurfaceGravity.config(text="", foreground='green')
        elif g < 1.0:
            self.SurfaceGravity.config(text="G: "+ str(g), foreground='green')
        elif g < 2.0:
            self.SurfaceGravity.config(text="G: "+ str(g), foreground='orange')
        else:
            self.SurfaceGravity.config(text="G: "+ str(g), foreground='red')
            

    def hull_blink(self):
        """ loop de changement de couleur bref de l'indicateur de niveau de hull """
        color=['red', 'orange']
        ind=0
        while self.hull < 20:
            self.HullHealth.config(text="Hull: "+str(self.hull)+"%", foreground=color[ind])
            ind = 1-ind
            sleep(0.5)
            
    def fuel_blink(self):
        """ loop de changement de couleur bref de l'indicateur de niveau de fuel """
        color=['red', 'orange']
        ind=0
        while self.Fuel < 20:
            self.fuelMain.config(text="Fuel: "+str(self.Fuel)+'%', foreground=color[ind])
            ind = 1-ind
            sleep(0.5)
            
    def shield_blink(self):
        """ loop de changement de couleur bref de l'indicateur de niveau de shield """
        color=['red', 'orange']
        ind=0
        while not self.Shield:
            self.ShieldsUp.config(text="Shield DOWN", foreground=color[ind])
            ind = 1-ind
            sleep(0.5)