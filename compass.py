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
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.parent_frame: Optional[tk.Frame]
        self.canvas: Optional[tk.Canvas]
        self.Latitude = 0
        self.Longitude = 0        
        self.prev_Longitude = 0
        self.prev_Latitude = 0
        self.Heading = 0
        self.lastHeading = -1
        self.lastA = -1
        
        
    def setup_frame(self, parent: tk.Frame):
        self.parent_frame = parent
        self.canvas = tk.Canvas(self.parent_frame, height=50, width=50, border=None, borderwidth=0)
        self.canvas.grid(row=0, sticky=tk.W+tk.E, column=0, columnspan=3)
        theme.update(self.parent_frame)
             
    def popup(self):
        self.canvas.grid(row=0, sticky=tk.W+tk.E, column=0, columnspan=3)
        
    def dismiss(self):
        self.canvas.grid_remove()
            
    def set_Latitude(self, value: any):
        self.prev_Latitude = self.Latitude
        self.Latitude = value
        
    def set_Longitude(self, value: any):
        self.prev_Longitude = self.Longitude
        self.Longitude = value
            
    def set_Heading(self, value: any):  
        self.Heading = value
        
    def update_canvas(self):
        angle=0
        # il faut compute l'angle (heading) depuis lat long car
        # la valeur de heading ne se rafraichit pas en cam externe!
        dLonx = self.Longitude - self.prev_Longitude
        dLaty = self.Latitude - self.prev_Latitude
        v = math.sqrt( dLonx*dLonx + dLaty*dLaty )
        if v != 0:
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
            angle = A
            if angle == self.lastA:
                return
            self.lastA = angle
        elif self.Heading != self.lastHeading:
            # il semblerait qu'a pied, le heading soit inversé +/-
            angle = -1*self.Heading
            self.lastHeading = self.Heading
        else:
            return
        self.canvas.delete('all')
        # self.display_rect_compass(angle)
        self.display_round_compass(angle)
        
    def display_round_compass(self, angle: int):
        self.canvas.create_arc(4,4,46,46,
                               style=tk.PIESLICE,
                               start=angle-10+90,
                               extent=20,
                               outline="cyan", fill="blue")
        self.canvas.create_text(25, 10, text='N', fill='orange', font='Arial 10')
        self.canvas.create_text(25, 45, text='S', fill='orange', font='Arial 10')
        self.canvas.create_text(45, 25, text='E', fill='orange', font='Arial 10')
        self.canvas.create_text(10, 25, text='W', fill='orange', font='Arial 10')
    
    def display_rect_compass(self, angle: int):
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
        ps = angle - 90
        pe = angle + 90
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
        for head in range(end, start, -10):
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
            self.draw_north_west(pos)
        elif head == 90 or head == 450:
            self.draw_west(pos)
        elif head == 135:
            self.draw_south_west(pos)
        elif head == 180:
            self.draw_south(pos)
        elif head == 225:
            self.draw_south_east(pos)
        elif head == 270 or head ==-90:
            self.draw_east(pos)
        elif head == 315 or head == -45:
            self.draw_north_east(pos)

        
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
        