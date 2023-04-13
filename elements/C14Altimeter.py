import logging
from typing import Optional
import tkinter as tk
from theme import theme

class AltimeterC14():
    def __init__(self, logger: logging.Logger, scale: int):
        self.logger = logger
        self.ui_scale = scale
        self.parent_frame: Optional[tk.Frame]
        self.alt_canvas: Optional[tk.Canvas]
        self.Altitude = 0
        self.lastAltitude = -1
        self.SurfaceGravity = 1.0
        self.lastGravity = -1.0
        self.g_ind = 2
        self.colors = ['red','orange', 'orange']

    def scale(self, value: int) -> int:
        return int(value * self.ui_scale / 100.0)

    def setup_frame(self, parent: tk.Frame):
        self.parent_frame = parent
        self.alt_canvas = tk.Canvas(self.parent_frame, 
                                    height=self.scale(50), 
                                    width=self.scale(50), 
                                    border=None, borderwidth=0)
        self.alt_canvas.grid(row=0, sticky=tk.W, column=3, padx=5)
        theme.update(self.parent_frame)
    
    def set_Altitude(self, value: any):
        self.Altitude = value
        self.update_alt_canvas()
        
    def set_SurfaceGravity(self, value: float):
        self.SurfaceGravity = int(value*10.0+0.5) / 100.0
        self.update_alt_canvas()

    def update_alt_canvas(self):
        if self.Altitude == self.lastAltitude and self.SurfaceGravity == self.lastGravity:
            return
        self.lastAltitude = self.Altitude
        self.alt_canvas.delete('all')
        self.update_canvas_gravity()
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

        # if palier == 50:
        # en dessous de 500m, rouge
        y = (-ch/palier) * 50 + ch
        self.alt_canvas.create_rectangle(self.scale(0), self.scale(y), 
                                        self.scale(10), self.scale(ch),
                                        fill="red", activefill="red")
        if palier > 50:
            # en dessous de 500m, rouge 
            y = (-ch/palier) * 50 + ch
            j = (-ch/palier) * 100 + ch
            self.alt_canvas.create_rectangle(self.scale(0), self.scale(y),
                                             self.scale(10), self.scale(j),
                                             fill="red", activefill="red")
        if palier > 100:
            # en dessous de 500m, rouge
            y = (-ch/palier) * 100 + ch
            j = (-ch/palier) * 500 + ch
            self.alt_canvas.create_rectangle(self.scale(0), self.scale(y), 
                                             self.scale(10), self.scale(j), 
                                             fill="red", activefill="red")
        if palier > 500:
            # 500m à 1Km orange
            y = (-ch/palier) * 500 + ch
            j = (-ch/palier) * 1_000 + ch
            self.alt_canvas.create_rectangle(self.scale(0), self.scale(y), 
                                             self.scale(10), self.scale(j), 
                                             fill="orange", activefill="orange")
        if palier > 1000:
            # 1Km a 2Km Jaune
            y = (-ch/palier) * 1_000 + ch
            j = (-ch/palier) * 2_000 + ch
            self.alt_canvas.create_rectangle(self.scale(0), self.scale(y), 
                                             self.scale(10), self.scale(j), 
                                             fill="yellow", activefill="yellow")
        if palier > 2000:
            # 2Km à 10Km vert
            y = (-ch/palier) * 2_000 + ch
            j = (-ch/palier) * 10_000 + ch
            self.alt_canvas.create_rectangle(self.scale(0), self.scale(y), 
                                             self.scale(10), self.scale(j), 
                                             fill="green", activefill="green")
        if palier > 10000:
            # 10Km à 300Km bleu
            y = (-ch/palier) * 10_000 + ch
            j = (-ch/palier) * 30_000 + ch
            self.alt_canvas.create_rectangle(self.scale(0), self.scale(y), 
                                             self.scale(10), self.scale(j), 
                                             fill="cyan", activefill="cyan")
        if palier > 30000:
            # 10Km à 300Km bleu
            y = (-ch/palier) * 30_000 + ch
            j = (-ch/palier) * 300_000 + ch
            self.alt_canvas.create_rectangle(self.scale(0), self.scale(y), 
                                             self.scale(10), self.scale(j), 
                                             fill="blue", activefill="cyan")

        # barre
        self.alt_canvas.create_line(self.scale(2), self.scale(0), 
                                    self.scale(2), self.scale(ch), 
                                    fill="orange", activefill="orange")
        # tick
        y = (-ch/palier) * self.Altitude + ch
        self.alt_canvas.create_line(self.scale(0), self.scale(y), 
                                    self.scale(25), self.scale(y), 
                                    fill="orange", activefill="orange")
        # value
        al = int(self.Altitude)
        unit = ' m'
        if al < 1000:
            unit = ' m'
        else:
            al = int(al/1000)
            unit = ' Km'
        self.alt_canvas.create_text(self.scale(19),
                                    self.scale(y-6),
                                    text= str(al)+unit,
                                    fill="black", font='Arial 6')
        self.alt_canvas.create_text(self.scale(20),
                                    self.scale(y-5),
                                    text= str(al)+unit,
                                    fill="orange", font='Arial 6')
        
    def update_canvas_gravity(self):       
        """Affiche le niveau de gravité"""
        self.lastGravity = self.SurfaceGravity
        if self.SurfaceGravity < 0: return
        if self.SurfaceGravity <= 1.0:
            self.g_ind = 2
        elif self.SurfaceGravity < 2.0:
            self.g_ind = 1
        else:
            self.g_ind = 1 - self.g_ind
            if self.g_ind < 0: self.g_ind = 0
        self.alt_canvas.create_text(self.scale(35), 
                                    self.scale(45), 
                                    text= 'G:'+ str(self.SurfaceGravity), 
                                    fill='black', font='Arial 6')
        self.alt_canvas.create_text(self.scale(36), 
                                    self.scale(46), 
                                    text= 'G:'+ str(self.SurfaceGravity), 
                                    fill=self.colors[self.g_ind], font='Arial 6')
