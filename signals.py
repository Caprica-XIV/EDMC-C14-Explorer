import tkinter as tk
from typing import Any, Mapping, MutableMapping, Optional
from theme import theme

class SignalsC14():
    def __init__(self):
        self.lbl: Optional[tk.Label]
        self.lbl_signal: Optional[tk.Label]
        self.parent_frame: Optional[tk.Frame]
        self.frame_signal: Optional[tk.Frame]
        self.map_ids = []
        self.map_belt_ids = []
        self.mapped = list((0,0))
        self.map_bodies = list((0,0))
        self.map_geo = 0
        self.map_bio = 0
        self.map_rings = 0
        self.map_belts = 0
        self.map_signals = 0
        self.map_UIA = 8
        self.map_others = list((0,0))
        self.map_new_scan = False  

    def setup_frame(self, parent: tk.Frame):
        self.parent_frame = parent
        self.frame_signal = tk.Frame(parent, border=None)
        self.frame_signal.grid(row=0,sticky=tk.SW, column=0)

        self.lbl_signal = tk.Label(self.frame_signal, text="Signals: ?")
        self.lbl_signal.grid(row=0, sticky=tk.W, column=0, padx=10)

    def update_signals_frame(self):
        """ maj des signaux affichés """

        self.frame_signal.destroy()
        self.frame_signal = tk.Frame(self.parent_frame, border=None)
        self.frame_signal.grid(row=0,sticky=tk.SW, column=0)
        
        self.lbl_signal = tk.Label(self.frame_signal, text="Total: "+str(self.mapped[0])+"/"+str(self.mapped[1]))
        self.lbl_signal.grid(row=0, sticky=tk.W, column=0, padx=10)

        col = 0
        row = 1

        if self.map_bodies[1] > 0:
            lbl = tk.Label(self.frame_signal, text="Bodies: "+str(self.map_bodies[0])+"/"+str(self.map_bodies[1]))
            lbl.grid(row=row, column=col, sticky=tk.W)        
            col+=1
        if self.map_others[1] > 0:
            lbl = tk.Label(self.frame_signal, text="Others: "+str(self.map_others[0])+"/"+str(self.map_others[1]))
            lbl.grid(row=row, column=col, sticky=tk.W, padx=4)
            col+=1
        if self.map_UIA > 0:
            lbl = tk.Label(self.frame_signal, text="UIA: "+str(self.map_UIA))
            lbl.grid(row=row, column=col, sticky=tk.W, padx=4)
            col+=1
        if self.map_belts > 0:
            lbl = tk.Label(self.frame_signal, text="Asteroids: "+str(self.map_belts))
            lbl.grid(row=row, column=col, sticky=tk.W, padx=4)

        col=0
        row+=1
        
        if self.map_geo > 0:
            lbl = tk.Label(self.frame_signal, text="Geological: "+str(self.map_geo))
            lbl.grid(row=row, column=col, sticky=tk.W)
            col+=1
        if self.map_bio > 0:
            lbl = tk.Label(self.frame_signal, text="Biological: "+str(self.map_bio))
            lbl.grid(row=row, column=col, sticky=tk.W, padx=4)
            col+=1
        if self.map_rings > 0:
            lbl = tk.Label(self.frame_signal, text="Rings: "+str(self.map_rings))
            lbl.grid(row=row, column=col, sticky=tk.W)
            
        col=0
        row+=1
        if self.map_signals > 0:
            lbl = tk.Label(self.frame_signal, text="Signals: "+str(self.map_signals))
            lbl.grid(row=row, column=col, sticky=tk.W, padx=4)
            col+=1
            
        theme.update(self.frame_signal)
        
    def journal_FSDJump(self):
        # We arrived at a new system!
        self.lbl_signal.config(text="Signals: ?")
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
            
    def journal_Scan(self, entry: MutableMapping[str, Any]):
        self.map_new_scan = True
        bId = entry['BodyID']
        update = False
        if 'Belt' in entry['BodyName']:
            if bId not in self.map_belt_ids:
                # Ceinture d'astéroid non mappé
                self.map_belt_ids.append(bId) 
                self.map_belts += 1
                self.map_others[0] += 1
                self.mapped[0] += 1
                update = True
        elif bId not in self.map_ids:
            # body non mappé
            self.map_ids.append(bId)
            self.map_bodies[0] += 1
            self.mapped[0] += 1
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
                    # self.map_others[1] -= sgnl['Count']
                    # self.mapped[0] += sgnl['Count']
                    self.update_signals_frame()
                if 'Biological' in sgnl['Type']:
                    self.map_bio += sgnl['Count']
                    # self.map_others[1] -= sgnl['Count']
                    # self.mapped[0] += sgnl['Count']
                    self.update_signals_frame()

    def journal_SAASignalsFound(self, entry: MutableMapping[str, Any]):
        update = False
        if 'Signals' in entry:
            for sgnl in entry['Signals']:
                self.map_signals += sgnl['Count']
                update = True
                # on détermine le type et le count
                # if 'Guardian' in sgnl['Type']:
                #     self.map_signals += sgnl['Count']
                #     update_signals_frame()
                # if 'Thargoid' in sgnl['Type']:
                #     self.map_signals += sgnl['Count']
                #     update_signals_frame()  
        if update:
            self.update_signals_frame()
        