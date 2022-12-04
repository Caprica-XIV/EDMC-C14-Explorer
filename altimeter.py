import logging
from typing import Optional
import tkinter as tk
from compassframe import CompassFrame
from theme import theme

class AltimeterC14():
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.parent_frame: Optional[tk.Frame]
        self.alt_canvas: Optional[tk.Canvas]
        self.Altitude = 0
        self.lastAltitude = -1

    def setup_frame(self, parent: tk.Frame):
        self.parent_frame = parent
        self.alt_canvas = tk.Canvas(self.parent_frame, height=50, width=20, border=None, borderwidth=0)
        self.alt_canvas.grid(row=0, sticky=tk.E, column=3, padx=5)
        theme.update(self.parent_frame)
             
    def popup(self):
        self.alt_canvas.grid(row=0, sticky=tk.E, column=3, padx=5)
        
    def dismiss(self):
        self.alt_canvas.grid_remove()
            
    def set_Altitude(self, value: any):
        self.Altitude = value

    def update_alt_canvas(self):
        if self.Altitude == self.lastAltitude:
            return
        self.lastAltitude = self.Altitude
        self.alt_canvas.delete('all')
        ch = 49
        palier = 50
        if self.Altitude > 0.75 * palier:
            palier = 100
        if self.Altitude > 0.75 * palier:
            palier = 500
        if self.Altitude > 0.75 * palier:
            palier = 2000
        if self.Altitude > 0.75 * palier:
            palier = 5000
        if self.Altitude > 0.75 * palier:
            palier = 10000
        if self.Altitude > 0.75 * palier:
            palier = 300_000
        if self.Altitude > 0.75 * palier:
            palier = 500_000

        if palier == 50:
            # en dessous de 500m, rouge
            y = (-ch/palier) * 50 + ch
            self.alt_canvas.create_rectangle(10, y, 20, ch, fill="red", activefill="red")
        if palier > 50:
            # en dessous de 500m, rouge 
            y = (-ch/palier) * 50 + ch
            j = (-ch/palier) * 100 + ch
            self.alt_canvas.create_rectangle(10, y, 20, j, fill="red", activefill="red")
        if palier > 100:
            # en dessous de 500m, rouge
            y = (-ch/palier) * 100 + ch
            j = (-ch/palier) * 500 + ch
            self.alt_canvas.create_rectangle(10, y, 20, j, fill="red", activefill="red")
        if palier > 500:
            # 500m à 1Km orange
            y = (-ch/palier) * 500 + ch
            j = (-ch/palier) * 1_000 + ch
            self.alt_canvas.create_rectangle(10, y, 20, j, fill="orange", activefill="orange")
        if palier > 1000:
            # 1Km a 2Km Jaune
            y = (-ch/palier) * 1_000 + ch
            j = (-ch/palier) * 2_000 + ch
            self.alt_canvas.create_rectangle(10, y, 20, j, fill="yellow", activefill="yellow")
        if palier > 2000:
            # 2Km à 10Km vert
            y = (-ch/palier) * 2_000 + ch
            j = (-ch/palier) * 10_000 + ch
            self.alt_canvas.create_rectangle(10, y, 20, j, fill="green", activefill="green")
        if palier > 10000:
            # 10Km à 300Km bleu
            y = (-ch/palier) * 10_000 + ch
            j = (-ch/palier) * 30_000 + ch
            self.alt_canvas.create_rectangle(10, y, 20, j, fill="cyan", activefill="cyan")
        if palier > 30000:
            # 10Km à 300Km bleu
            y = (-ch/palier) * 30_000 + ch
            j = (-ch/palier) * 300_000 + ch
            self.alt_canvas.create_rectangle(10, y, 20, j, fill="blue", activefill="cyan")

        # barre
        self.alt_canvas.create_line(15, 0, 15, ch, fill="orange", activefill="orange")
        # tick
        y = (-ch/palier) * self.Altitude + ch
        self.alt_canvas.create_line(5, y, 25, y, fill="orange", activefill="orange")