import tkinter as tk
from typing import Any, Mapping, MutableMapping, Optional
from theme import theme

class SignalsC14():
    def __init__(self):
        self.lbl: Optional[tk.Label]
        self.lbl_signal: Optional[tk.Label]
        self.parent_frame: Optional[tk.Frame]
        self.frame_signal: Optional[tk.Frame]
        self.entries = []
        self.map_ids = []
        self.map_belt_ids = []
        self.mapped = list((0,0))
        self.map_bodies = list((0,0))
        self.map_geo = 0
        self.map_bio = 0
        self.map_rings = 0
        self.map_belts = 0
        self.map_signals = 0
        self.map_UIA = 0
        self.map_others = list((0,0))
        self.map_new_scan = False
        self.PlanetClass = dict()
        self.terraformables = 0
        self.landables = 0
        self.ed_discovered = 0
        self.ed_mapped = 0

    def setup_frame(self, parent: tk.Frame):
        self.parent_frame = parent
        self.frame_signal = tk.Frame(parent, border=None)
        self.frame_signal.grid(row=0,sticky=tk.N+tk.S+tk.E+tk.W, column=0)

        self.lbl_signal = tk.Label(self.frame_signal, text="Waiting for honk")
        self.lbl_signal.grid(row=0, sticky=tk.W, column=0, padx=4)
        
        theme.update(self.parent_frame)
        
    def update_signals_frame(self):
        """ maj des signaux affichés """

        self.frame_signal.destroy()
        self.frame_signal = tk.Frame(self.parent_frame, border=None)
        self.frame_signal.grid(row=0,sticky=tk.SW, column=0)
        
        col=0
        row=0
        
        self.lbl_signal = tk.Label(self.frame_signal, text="Total: "+str(self.mapped[0])+"/"+str(self.mapped[1]))
        self.lbl_signal.grid(row=0, sticky=tk.W, column=0)
        col=1-col
        if self.ed_discovered >= 0:
            lbl = tk.Label(self.frame_signal, text="Discovered: "+str(self.ed_discovered)+"/"+str(self.map_bodies[1]))
            lbl.grid(row=row, column=col, sticky=tk.W)        
            col=1-col
            row += 1 if col == 0 else 0
        if self.ed_mapped >= 0:
            lbl = tk.Label(self.frame_signal, text="Mapped: "+str(self.ed_mapped)+"/"+str(self.map_bodies[1]))
            lbl.grid(row=row, column=col, sticky=tk.W)
            col=1-col
            row += 1 if col == 0 else 0
            
        # col=0
        

        if self.map_bodies[1] > 0:
            lbl = tk.Label(self.frame_signal, text="Bodies: "+str(self.map_bodies[0])+"/"+str(self.map_bodies[1]))
            lbl.grid(row=row, column=col, sticky=tk.W)        
            col=1-col
            row += 1 if col == 0 else 0
        if self.map_others[1] > 0:
            lbl = tk.Label(self.frame_signal, text="Others: "+str(self.map_others[0])+"/"+str(self.map_others[1]))
            lbl.grid(row=row, column=col, sticky=tk.W)
            col=1-col
            row += 1 if col == 0 else 0
        if self.map_UIA > 0:
            lbl = tk.Label(self.frame_signal, text="UIA: "+str(self.map_UIA))
            lbl.grid(row=row, column=col, sticky=tk.W)
            col=1-col
            row += 1 if col == 0 else 0
        if self.map_belts > 0:
            lbl = tk.Label(self.frame_signal, text="Asteroids: "+str(self.map_belts))
            lbl.grid(row=row, column=col, sticky=tk.W)
            row += 1 if col == 0 else 0

        # col=0
        # row+=1
        
        if self.map_geo > 0:
            lbl = tk.Label(self.frame_signal, text="Geological: "+str(self.map_geo))
            lbl.grid(row=row, column=col, sticky=tk.W)
            col=1-col
            row += 1 if col == 0 else 0
        if self.map_bio > 0:
            lbl = tk.Label(self.frame_signal, text="Biological: "+str(self.map_bio))
            lbl.grid(row=row, column=col, sticky=tk.W)
            col=1-col
            row += 1 if col == 0 else 0
        if self.map_rings > 0:
            lbl = tk.Label(self.frame_signal, text="Rings: "+str(self.map_rings))
            lbl.grid(row=row, column=col, sticky=tk.W)
            row += 1 if col == 0 else 0

        # col=0
        # row+=1
        
        if self.terraformables > 0:
            lbl = tk.Label(self.frame_signal, text="Terraformables: "+str(self.terraformables))
            lbl.grid(row=row, column=col, sticky=tk.W)
            col=1-col
            row += 1 if col == 0 else 0
        if self.landables > 0:
            lbl = tk.Label(self.frame_signal, text="Landables: "+str(self.landables))
            lbl.grid(row=row, column=col, sticky=tk.W)
            col=1-col
            row += 1 if col == 0 else 0
        if self.map_signals > 0:
            lbl = tk.Label(self.frame_signal, text="Signals: "+str(self.map_signals))
            lbl.grid(row=row, column=col, sticky=tk.W)
            col=1-col
            row += 1 if col == 0 else 0
            
        col=0
        row+=1
        for body in self.PlanetClass:
            lbl = tk.Label(self.frame_signal, text=str(body) +": "+ str(self.PlanetClass[body]))
            lbl.grid(row=row, column=col, sticky=tk.W)
            row+=1
        
        # self.frame_signal.pack()
        theme.update(self.frame_signal)
        
    def journal_FSDJump(self):
        # We arrived at a new system!
        self.lbl_signal.config(text="Waiting for honk")
        self.entries = []
        self.map_ids = []
        self.map_belt_ids = []
        self.mapped[0] = self.map_UIA
        self.mapped[1] = self.map_UIA
        self.map_bodies[0] = 0
        self.map_bodies[1] = 0
        self.map_others[0] = self.map_UIA
        self.map_others[1] = self.map_UIA
        self.map_geo = 0
        self.map_bio = 0
        self.map_rings = 0
        self.map_belts = 0
        self.map_signals = 0
        self.map_new_scan = False
        self.PlanetClass = dict()
        self.terraformables = 0
        self.landables = 0
        self.ed_discovered = 0
        self.ed_mapped = 0
        self.update_signals_frame()
                 
    def journal_FSSDiscoveryScan(self, entry: MutableMapping[str, Any]):
        # maj du nombre de scan attendu
        self.map_bodies[1] = int(entry['BodyCount'])
        self.map_others[1] = int(entry['NonBodyCount'])
        # self.map_others[0] += self.map_UIA
        self.mapped[1] = self.map_bodies[1] + self.map_others[1]
        # self.mapped[0] += self.map_UIA
        if not self.map_new_scan:
            self.mapped[0] += int(entry['Progress'] * self.map_bodies[1])
            self.map_bodies[0] = int(entry['Progress'] * self.map_bodies[1])
        self.update_signals_frame()
    
    def get_SurfaceGravity(self, id: int):
        for body in self.entries:
            if 'BodyID' in body and body['BodyID'] == id and 'SurfaceGravity' in body:
                return body['SurfaceGravity']
        return 0
        
    def body_scan(self, entry: MutableMapping[str, Any]):
        """ Gestion d'un nouveau scan d'un corps celeste """
        self.entries.append(entry)
        self.map_bodies[0] += 1
        self.mapped[0] += 1
        # compteur de type de body
        if 'PlanetClass' in entry:
            if entry['PlanetClass'] not in self.PlanetClass:
                self.PlanetClass[entry['PlanetClass']] = 0
            self.PlanetClass[entry['PlanetClass']] += 1
        if 'TerraformState' in entry and len(entry['TerraformState']) > 0: self.terraformables += 1
        if 'Landable' in entry and entry['Landable']: self.landables += 1
        if 'WasDiscovered' in entry and entry['WasDiscovered']: self.ed_discovered +=1
        if 'WasMapped' in entry and entry['WasMapped']: self.ed_mapped +=1
                
    def journal_Scan(self, entry: MutableMapping[str, Any]):
        """ Gestion des données lors d'un scan """
        self.map_new_scan = True
        bId = entry['BodyID']
        update = False
        if 'Belt' in entry['BodyName'] and bId not in self.map_belt_ids:
            # Ceinture d'astéroid non mappé
            self.map_belt_ids.append(bId) 
            self.map_belts += 1
            self.map_others[0] += 1
            self.mapped[0] += 1
            update = True
        elif bId not in self.map_ids:
            # body non mappé
            self.map_ids.append(bId)
            self.body_scan(entry)
            update = True
        if 'Rings' in entry:
            # on a découvert des signaux d'anneaux de type other si belt
            for ring in entry['Rings']:
                if 'Belt' not in ring['Name']:
                    self.map_rings += 1
                    # self.mapped[0] += 1
                    # self.map_others[0] += 1
            update = True
        if update:
            self.update_signals_frame()

    def journal_FSSBodySignals(self, entry: MutableMapping[str, Any]):
        if 'Signals' in entry:
            for sgnl in entry['Signals']:
                # on détermine le type et le count
                if 'Geological' in sgnl['Type']:
                    self.map_geo += sgnl['Count']
                    self.update_signals_frame()
                if 'Biological' in sgnl['Type']:
                    self.map_bio += sgnl['Count']
                    self.update_signals_frame()

    def journal_SAASignalsFound(self, entry: MutableMapping[str, Any]):
        update = False
        if 'Signals' in entry:
            for sgnl in entry['Signals']:
                self.map_signals += sgnl['Count']
                update = True
        if update:
            self.update_signals_frame()
        