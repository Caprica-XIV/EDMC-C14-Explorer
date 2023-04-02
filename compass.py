import logging
import math
from time import sleep
from typing import Optional
import tkinter as tk
from theme import theme

class CompassC14():
    """
    Controller of CompassFrame
    """
    def __init__(self, logger: logging.Logger, scale: int):
        self.logger = logger
        self.ui_scale = scale
        self.parent_frame: Optional[tk.Frame]
        self.canvas: Optional[tk.Canvas]
        self.Latitude = 0
        self.Longitude = 0        
        self.prev_Longitude = 0
        self.prev_Latitude = 0
        self.Heading = 0
        self.lastHeading = -1
        self.lastA = -1
        self.arc = False
        self.getOut = True
        self.update = True 
        
    def scale(self, value: int) -> int:
        return int(value * self.ui_scale / 100.0)
        
    def setup_frame(self, parent: tk.Frame):
        self.parent_frame = parent
        self.canvas = tk.Canvas(self.parent_frame, 
                                height=self.scale(50), 
                                width=self.scale(50), 
                                border=None, borderwidth=0)
        self.canvas.grid(row=0, sticky=tk.W+tk.E, column=0)
        theme.update(self.parent_frame)
        
    def worker(self):
        self.logger.info("Compass loop start")
        self.getOut = False
        while not self.getOut:
            if self.update: self.update_canvas()
            sleep(1/10)
             
    def popup(self):
        # self.canvas.grid(row=0, sticky=tk.W+tk.E, column=0, columnspan=3)
        self.arc = True
        self.update_canvas()
        
    def dismiss(self):
        # self.canvas.grid_remove()
        self.arc = False
        if self.canvas:
            self.update_canvas()
            
    def set_Latitude(self, value: any):
        self.prev_Latitude = self.Latitude
        self.Latitude = value
        if self.prev_Latitude != self.Latitude: self.update = True
        
    def set_Longitude(self, value: any):
        self.prev_Longitude = self.Longitude
        self.Longitude = value
        if self.prev_Longitude != self.Longitude: self.update = True
            
    def set_Heading(self, value: any):  
        self.Heading = value
        if self.lastHeading != self.Heading: self.update = True
        
    def update_canvas(self):
        if not self.update: return
        self.update = False
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
        if self.arc:
            self.canvas.create_arc(self.scale(4),self.scale(4),
                                   self.scale(46),self.scale(46),
                                style=tk.PIESLICE,
                                start=angle-10+90,
                                extent=20,
                                outline="cyan", fill="blue")
        self.canvas.create_text(self.scale(26), self.scale(8), text='N', fill='orange', font='Arial 10')
        self.canvas.create_text(self.scale(26), self.scale(44), text='S', fill='orange', font='Arial 10')
        self.canvas.create_text(self.scale(45), self.scale(26), text='E', fill='orange', font='Arial 10')
        self.canvas.create_text(self.scale(10), self.scale(26), text='W', fill='orange', font='Arial 10')
    
    # def display_rect_compass(self, angle: int):
    #     # Nord: heading = 0
    #     # Ouest:heading = 90
    #     # Sud:  heading = 180
    #     # Est:  heading = 270
    #     cw = self.canvas.winfo_width()
    #     ch = self.canvas.winfo_height() - 20
    #     # repère centrale
    #     self.canvas.create_line(int(cw/2 -5), ch+20, int(cw/2), ch-10+20, fill="orange", activefill="orange")
    #     self.canvas.create_line(int(cw/2 +5), ch+20, int(cw/2), ch-10+20, fill="orange", activefill="orange")
    #     # on veut la position au centre, et environ 180°
    #     ps = angle - 90
    #     pe = angle + 90
    #     # relation entre x canvas et la plage ps->pe
    #     # x(0) = ps.A +B => B = -ps.A
    #     # x(cw) = pe.A -ps.A => x(cw) = A.(pe -ps) => A = cw / (pe-ps)
    #     A = cw / (pe - ps)
    #     B = -ps * A
    #     # on veux un trait tous les 10°
    #     start=ps
    #     while start % 10 != 0:
    #         start+=1
    #     end=pe
    #     while end % 10 != 0:
    #         end+=1
    #     for head in range(end, start, -10):
    #         x0 = int(head * A + B)
    #         y0 = 0
    #         x1 = x0
    #         if head == 0 or head == 90 or head == -90 or head == 180 or head == 270 or head == 360 or head == 450:
    #             y1 = ch-1
    #             self.draw_letter(head, x0)
    #         else:
    #             y1 = int(ch/2)
    #             if head == 40 or head == 130 or head == 220 or head == 310 or head == -40 or head == 400:
    #                 self.draw_letter(head+5, int((head+5) * A + B))
    #         self.canvas.create_line(x0, y0, x1, y1, fill="orange", activefill="orange")
        
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
        self.canvas.create_text(self.scale(pos), self.scale(45), text='N', fill='orange', font='Arial 10')
    def draw_south(self, pos: int):
        self.canvas.create_text(self.scale(pos), self.scale(45), text='S', fill='orange', font='Arial 10')
    def draw_east(self, pos: int):
        self.canvas.create_text(self.scale(pos), self.scale(45), text='E', fill='orange', font='Arial 10')
    def draw_west(self, pos: int):
        self.canvas.create_text(self.scale(pos), self.scale(45), text='W', fill='orange', font='Arial 10')
    def draw_north_west(self, pos: int):
        self.canvas.create_text(self.scale(pos), self.scale(25), text='NW', fill='orange', font='Arial 10')
    def draw_north_east(self, pos: int):
        self.canvas.create_text(self.scale(pos), self.scale(25), text='NE', fill='orange', font='Arial 10')
    def draw_south_west(self, pos: int):
        self.canvas.create_text(self.scale(pos), self.scale(25), text='SW', fill='orange', font='Arial 10')                
    def draw_south_east(self, pos: int):
        self.canvas.create_text(self.scale(pos), self.scale(25), text='SE', fill='orange', font='Arial 10')
        