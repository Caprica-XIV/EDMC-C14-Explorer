import logging
import os
import tkinter as tk
import threading
from typing import Optional
from time import sleep
from theme import theme

class HudInfoC14():
    def __init__(self, logger: logging.Logger, scale: int) -> None:
        self.logger = logger
        self.ui_scale = scale
        self.parent_frame: Optional[tk.Frame]
        self.canvas: Optional[tk.Frame]
        self.pngShip: Optional[tk.PhotoImage]
        self.pngSRV: Optional[tk.PhotoImage]
        self.pngOnFoot: Optional[tk.PhotoImage]
        
        self.FuelCapacity = 1
        self.ModeSRV = False
        self.ModeOnFoot = False
        self.Hull = 100
        self.Health = 100
        self.HullSRV = 100
        self.Fuel = 100
        self.Shield = True
        self.loop = False
        self.colors = ['red','orange', 'orange']
        self.h_ind = 2
        self.f_ind = 2


    def scale(self, value: int) -> int:
        return int(value * self.ui_scale / 100.0)

    def setup_frame(self, parent: tk.Frame, plugin_dir: str):
        self.parent_frame = parent
        self.canvas = tk.Canvas(self.parent_frame, 
                                height=self.scale(50), 
                                width=self.scale(50), 
                                border=None, borderwidth=0)
        self.canvas.grid(row=0, sticky=tk.W+tk.E, column=5, columnspan=3, padx=5)
        
        self.pngShip = tk.PhotoImage(file=os.path.join(plugin_dir, "icons", "ship.png"))
        self.pngSRV = tk.PhotoImage(file=os.path.join(plugin_dir, "icons", "srv.png"))
        self.pngOnFoot = tk.PhotoImage(file=os.path.join(plugin_dir, "icons", "onFoot.png"))
        
        theme.update(self.parent_frame)
        self.update_canvas()
        
    def set_ModeSRV(self, value: bool):
            self.ModeSRV = value
            # if value: self.ModeOnFoot = False
            self.update_canvas()
                    
    def set_ModeOnFoot(self, value: bool):
            # if value: self.ModeSRV = False
            self.ModeOnFoot = value
            self.update_canvas()
            
    def set_fuel_main(self, value: float, reserve: float):
        fuel = value + reserve
        if self.FuelCapacity <= 1 or self.ModeSRV:
            self.Fuel = int(100 * fuel/0.5)
        else:
            self.Fuel = int(100 * fuel / self.FuelCapacity)
        if self.Fuel > 100.0:
            self.Fuel = int(fuel*100) / 100.0
        if self.Fuel < 20:
            threading.Thread(target=self.blink_loop, daemon=True, name='C14 blink').start()
        self.update_canvas()
        
    def set_FuelCapacity(self, value: float):
        self.FuelCapacity = value
        
    def set_HullHealth(self, value: float):
        if self.ModeOnFoot:
            self.Health = int(100 * value)
        elif self.ModeSRV:
            self.HullSRV = int(100 * value)
        else:
            self.Hull = int(100 * value)
        if value < 0.20:
            threading.Thread(target=self.blink_loop, daemon=True, name='C14 blink').start()
        self.update_canvas()
        
    def set_ShieldsUp(self, value: bool):
        self.Shield = value
        self.update_canvas()

    def blink_loop(self):
        """ loop de changement de couleur bref de l'indicateur de niveau de hull """
        if self.loop: return
        self.loop=True
        val = 100
        if self.ModeOnFoot:
            val = self.Health
        elif self.ModeSRV:
            val = self.HullSRV
        else:
            val = self.Hull
        while val < 20 or self.Fuel < 20:
            self.update_canvas()
            sleep(0.5)
            if self.ModeOnFoot:
                val = self.Health
            elif self.ModeSRV:
                val = self.HullSRV
            else:
                val = self.Hull
        self.loop = False
            
    def update_canvas(self):
        """ maj du dessin selon le mode et le niveau de hull, fuel, shield, gravity """
        self.canvas.delete('all')
        # image de fond.
        self.update_canvas_image()
        # arc de bouclier
        self.update_canvas_shield()
        # arc de hull
        self.update_canvas_hull()
        # barre de fuel
        self.update_canvas_fuel()
        
    def update_canvas_image(self):
        """ maj de l'image de fond suivant le mode en cours"""
        if self.ModeOnFoot:
            self.canvas.create_image(self.scale(26), 
                                     self.scale(22), 
                                     image=self.pngOnFoot)
        elif self.ModeSRV:
            self.canvas.create_image(self.scale(25), 
                                     self.scale(23), 
                                     image=self.pngSRV)
        else:
            self.canvas.create_image(self.scale(27), 
                                     self.scale(21), 
                                     image=self.pngShip)
        
    def update_canvas_shield(self):
        """Dessine un demi arc bleu si bouclier up"""
        if self.Shield:
            self.canvas.create_arc(self.scale(4), self.scale(4), 
                                   self.scale(48), self.scale(44),
                                start=15, extent=150, outline="cyan", fill="", style=tk.ARC)
            self.canvas.create_arc(self.scale(5), self.scale(5), 
                                   self.scale(47), self.scale(43),
                                start=15, extent=150, outline="blue", fill="", style=tk.ARC)
            self.canvas.create_arc(self.scale(7), self.scale(7), 
                                   self.scale(45), self.scale(42),
                                start=15, extent=150, outline="cyan", fill="", style=tk.ARC)
            self.canvas.create_arc(self.scale(8), self.scale(8), 
                                   self.scale(44), self.scale(41),
                                start=15, extent=150, outline="blue", fill="", style=tk.ARC)
        
    def update_canvas_hull(self):
        """Affiche le niveau de Hull"""
        val = 100
        if self.ModeOnFoot:
            val = self.Health
        elif self.ModeSRV:
            val = self.HullSRV
        else:
            val = self.Hull
        
        if val > 50:
            self.h_ind = 2
        elif val > 20:
            self.h_ind = 1
        else:
            self.h_ind = 1 - self.h_ind
            if self.h_ind < 0: self.h_ind = 0
            
        self.canvas.create_text(self.scale(11), self.scale(33), text= str(val)+'%', fill='black', font='Arial 6')
        self.canvas.create_text(self.scale(12), self.scale(34), text= str(val)+'%', fill=self.colors[self.h_ind], font='Arial 6')
        # arc depuis le text jusque sur le coté, pour représenter une jauge de hull
        self.canvas.create_arc(self.scale(11), self.scale(18), 
                               self.scale(45), self.scale(33),
                                start=val - 100, extent=-val, outline="red", fill="red", style=tk.ARC)
        self.canvas.create_arc(self.scale(11), self.scale(20), 
                               self.scale(47), self.scale(35),
                                start=val - 100, extent=-val, outline="red", fill="red", style=tk.ARC)
        self.canvas.create_arc(self.scale(11), self.scale(19), 
                               self.scale(46), self.scale(34),
                                start=val - 100, extent=-val, outline="orange", fill="orange", style=tk.ARC)
    
    
    def update_canvas_fuel(self):
        """Affiche le niveau de fuel"""
        self.Fuel = int(self.Fuel)
        if self.Fuel > 50:
            self.f_ind = 2
        elif self.Fuel > 20:
            self.f_ind = 1
        else:
            self.f_ind = 1 - self.f_ind
            if self.f_ind < 0: self.f_ind = 0
        self.canvas.create_text(self.scale(11), self.scale(45), text= str(self.Fuel)+'%', fill='black', font='Arial 6')
        self.canvas.create_text(self.scale(12), self.scale(46), text= str(self.Fuel)+'%', fill=self.colors[self.f_ind], font='Arial 6')
        # arc depuis le text jusque sur le coté, pour représenter une jauge de hull
        x = int(((49-22) / 100) * self.Fuel + 22)
        self.canvas.create_rectangle(self.scale(22), self.scale(46), 
                                     self.scale(x), self.scale(49), 
                                     fill="orange", activefill="orange")
        self.canvas.create_rectangle(self.scale(22), self.scale(46), 
                                     self.scale(49), self.scale(49), 
                                     fill="", activefill="", outline="orange")
        