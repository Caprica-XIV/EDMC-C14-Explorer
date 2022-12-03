import logging
import math
from typing import Optional
import tkinter as tk
from compassframe import CompassFrame
from theme import theme

class CompassC14():
    """
    Controller of CompassFrame
    """
    def __init__(self, logger: logging.Logger,):
        self.logger = logger
        self.parent_frame: Optional[tk.Frame]
        self.window: Optional[CompassFrame]
        self.compass_frame: Optional[tk.Frame]
        self.canvas: Optional[tk.Canvas]
        self.alt_canvas: Optional[tk.Canvas]
        self.fuelMain: Optional[tk.Label]
        self.ShieldsUp: Optional[tk.Label]
        self.HullHealth: Optional[tk.Label]
        self.getOut = True
        self.ModeSRV = False
        self.Altitude = 0
        self.Latitude = 0
        self.Longitude = 0
        self.prev_Latitude = 0
        self.prev_Longitude = 0
        self.Heading = 0
        self.lastHeading = -1
        self.lastAltitude = -1
        self.FuelCapacity = 1
        
    def setup_frame(self, parent: tk.Frame):
        self.parent_frame = parent
        self.compass_frame = tk.Frame(self.parent_frame, border=None)
        self.compass_frame.grid(row=1,sticky=tk.E+tk.W, column=0)
        self.canvas = tk.Canvas(self.compass_frame, height=50, width=200)
        self.canvas.grid(row=0, sticky=tk.W+tk.E, column=0, columnspan=3)
        self.alt_canvas = tk.Canvas(self.compass_frame, height=50, width=20)
        self.alt_canvas.grid(row=0, sticky=tk.E, column=3, padx=5)
        
        ff = tk.Frame(self.compass_frame, border=None)
        ff.grid(row=2,sticky=tk.SW, column=0)
        self.fuelMain = tk.Label(ff, text="", padx=10)
        self.fuelMain.grid(row=0,sticky=tk.W, column=0)
        self.HullHealth = tk.Label(ff, text="", padx=10)
        self.HullHealth.grid(row=0,sticky=tk.W, column=1)
        self.ShieldsUp = tk.Label(ff, text="", padx=10)
        self.ShieldsUp.grid(row=0,sticky=tk.W, column=2)
        
        theme.update(self.compass_frame)
             
    def popup(self):
        # self.window = CompassFrame(self.logger)
        # self.window.setup_frame()
        a=0

    def dismiss(self):
        self.getOut = True
        self.canvas.delete('all')
        # if self.window:
        #     self.window.destroy()
    
    def set_ModeSRV(self, value: bool):
        self.ModeSRV = value
            
    def set_Latitude(self, value: any):
        self.prev_Latitude = self.Latitude
        self.Latitude = value
        
    def set_Longitude(self, value: any):
        self.prev_Longitude = self.Longitude
        self.Longitude = value
            
    def set_Heading(self, value: any):
        self.Heading = value
            
    def set_Altitude(self, value: any):
        self.Altitude = value
            
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
            self.ShieldsUp.config(text="Shield UP")
        else:
            self.ShieldsUp.config(text="Shield DOWN")

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
        
    def update_canvas(self):
        # il faut compute l'angle (heading) depuis lat long car
        # la valeur de heading ne se rafraichit pas en cam externe!
        dLonx = self.Longitude - self.prev_Longitude
        dLaty = self.Latitude - self.prev_Latitude
        v = math.sqrt( dLonx*dLonx + dLaty*dLaty )
        if v == 0:
            return
        # ajustement selon le cadran
        if dLonx >=0 and dLaty >=0:
            # cadran : de 270 à 0 (360)
            A = 360-int(math.degrees(math.acos(abs(dLaty)/v)))
        elif dLonx <=0 and dLaty >=0:
            # cadran de 0 à 90
            A = int(math.degrees(math.acos(abs(dLaty)/v)))
        elif dLonx <=0 and dLaty <=0:
            # cadran de 90 à 180
            A = 90 + int(math.degrees(math.acos(abs(dLonx)/v)))
        elif dLonx >=0 and dLaty <=0:
            # cadran de 180 à 270
            A = 180 + int(math.degrees(math.acos(abs(dLaty)/v)))
        
        self.Heading = A
        if self.Heading == self.lastHeading:
            return
        self.lastHeading = self.Heading
        # self.window.set_Heading(self.Heading)
        self.canvas.delete('all')
        # Nord: heading = 0
        # Ouest:heading = 90
        # Sud:  heading = 180
        # Est:  heading = 270
        cw = self.canvas.winfo_width()
        ch = self.canvas.winfo_height() - 20
        # repère centrale
        self.canvas.create_line(int(cw/2 -5), ch+20, int(cw/2), ch-10+20, fill="orange", activefill="orange")
        self.canvas.create_line(int(cw/2 +5), ch+20, int(cw/2), ch-10+20, fill="orange", activefill="orange")
        # on veut la position au centre, et environ 180°
        ps = self.Heading - 90
        pe = self.Heading + 90
        # relation entre x canvas et la plage ps->pe
        # x(0) = ps.A +B => B = -ps.A
        # x(cw) = pe.A -ps.A => x(cw) = A.(pe -ps) => A = cw / (pe-ps)
        A = cw / (pe - ps)
        B = -ps * A
        # on veux un trait tous les 10°
        start=ps
        while start % 10 != 0:
            start+=1
        end=pe
        while end % 10 != 0:
            end+=1
        for head in range(start, end, 10):
            x0 = int(head * A + B)
            y0 = 0
            x1 = x0
            if head == 0 or head == 90 or head == -90 or head == 180 or head == 270 or head == 360 or head == 450:
                y1 = ch-1
                self.draw_letter(head, x0)
            else:
                y1 = int(ch/2)
                if head == 40 or head == 130 or head == 220 or head == 310 or head == -40 or head == 400:
                    self.draw_letter(head+5, int((head+5) * A + B))
            self.canvas.create_line(x0, y0, x1, y1, fill="orange", activefill="orange")
        
    def draw_letter(self, head: int, pos: int):
        if head == 0 or head == 360:
            self.draw_north(pos)
        elif head == 45 or head == 405:
            self.draw_north_east(pos)
        elif head == 90 or head == 450:
            self.draw_east(pos)
        elif head == 135:
            self.draw_south_east(pos)
        elif head == 180:
            self.draw_south(pos)
        elif head == 225:
            self.draw_south_west(pos)
        elif head == 270 or head ==-90:
            self.draw_west(pos)
        elif head == 315 or head == -45:
            self.draw_north_west(pos)

        
    def draw_north(self, pos: int):
        self.canvas.create_text(pos, 45, text='N', fill='orange', font='Arial 10')
    def draw_south(self, pos: int):
        self.canvas.create_text(pos, 45, text='S', fill='orange', font='Arial 10')
    def draw_east(self, pos: int):
        self.canvas.create_text(pos, 45, text='E', fill='orange', font='Arial 10')
    def draw_west(self, pos: int):
        self.canvas.create_text(pos, 45, text='W', fill='orange', font='Arial 10')
    def draw_north_west(self, pos: int):
        self.canvas.create_text(pos, 25, text='NW', fill='orange', font='Arial 10')
    def draw_north_east(self, pos: int):
        self.canvas.create_text(pos, 25, text='NE', fill='orange', font='Arial 10')
    def draw_south_west(self, pos: int):
        self.canvas.create_text(pos, 25, text='SW', fill='orange', font='Arial 10')                
    def draw_south_east(self, pos: int):
        self.canvas.create_text(pos, 25, text='SE', fill='orange', font='Arial 10')
        