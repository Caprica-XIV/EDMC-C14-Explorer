import logging
from typing import Any, MutableMapping, Optional
import tkinter as tk
from theme import theme

class GeologicalsC14():
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.parent_frame: Optional[tk.Frame]
        self.geos_frame: Optional[tk.Frame]
        self.geos = []
        self.bodies = []
        self.state_body=''

    def setup_frame(self, parent: tk.Frame):
        self.parent_frame = parent
        self.geos_frame = tk.Frame(self.parent_frame)
        theme.update(self.parent_frame)
        
    def get_body(self, entry: MutableMapping[str, Any]):
        """ Retourne l'objet json interne représentant le body et ses geos """
        for bdy in self.bodies:
            if 'BodyID' in entry and bdy['id'] == entry['BodyID']:
                if 'BodyName' in entry and len(bdy['short']) < 1:
                    bdy['name'] = entry['BodyName']
                    split=entry['BodyName'].split(' ')
                    if '0123456789' in split[-1]:
                        bdy['short']=split[-1]
                    else:
                        bdy['short']=split[len(split)-2] + split[-1]
                        
                return bdy
            elif 'Body' in entry and bdy['id'] == entry['Body']:
                return bdy
        
        self.create_body(entry)
        return self.bodies[-1]
    
    def create_body(self, entry: MutableMapping[str, Any]):
        """ Crée l'objet nécessaire à la gestion """
        id = entry['BodyID'] if 'BodyID' in entry else entry['Body']
        name = ''
        short = ''
        if 'BodyName' in entry:
            name = entry['BodyName']
        else:
            name = self.state_body
        split= name.split(' ')
        if '0123456789' in split[-1]:
            short=split[-1]
        elif len(split) > 1:
            short=split[len(split)-2] + split[-1]
        
        self.bodies.append({'id': id,
                            'name': name,
                            'short': short,
                            'geologicals': 0,
                            'geos': []
                            })
    
    def CodexEntry(self, entry: MutableMapping[str, Any]):
        """ action lors d'un scan en ship"""
        if 'SubCategory' not in entry or 'Geology' not in entry['SubCategory']: return
        species = entry['Name_Localised']
        self.scanEntrySpecies(species, entry)        
        
    def scanEntrySpecies(self, species: str, entry: MutableMapping[str, Any]):
        """ analyse le scan et définit si nouveau ou en cours """
        body = self.get_body(entry)
        found=False
        for bio in body['geos']:
            if species in bio['species']:
                found=True
                if 'ScanType' in entry and 'Analyse' in entry['ScanType']:
                    bio['scans'] = 3
                else:    
                    bio['scans'] += (1 if 'CodexEntry' not in entry['event'] else 0)
                break
        if not found:
            if 'ScanType' in entry and 'Analyse' in entry['ScanType']:
                body['geos'].append({
                    'species': species,
                    'scans': 3,
                    'max': 3
                })
            else:
                body['geos'].append({
                    'species': species,
                    'scans': (1 if ('CodexEntry' not in entry['event'] or 'Geology' in entry['SubCategory']) else 0),
                    'max': 1 if ('CodexEntry' in entry['event'] and 'Geology' in entry['SubCategory']) else 3
                })
        self.update_frame()
    
    def journal_FSDJump(self):
        self.geos = []
        self.bodies = []
        self.update_frame()
    
    def journal_FSSBodySignals(self, entry: MutableMapping[str, Any]):
        update=False
        if 'Signals' in entry:
            for sgnl in entry['Signals']:
                if 'Geological' in sgnl['Type']:
                    # on ajoute les info dans le détail
                    body = self.get_body(entry)
                    body['geologicals'] = sgnl['Count']
                    self.geos.append(str(sgnl['Count']) +' geologicals on '+ body['short'])
                    update=True
        if update : 
            self.update_frame()
                            
    def journal_SAASignalsFound(self, entry: MutableMapping[str, Any]):
        # on traite de la même façon
        self.journal_FSSBodySignals(entry)
    
    def update_frame(self):
        self.geos_frame.destroy()
        self.geos_frame = tk.Frame(self.parent_frame)
        self.geos_frame.grid(row=0, sticky=tk.SW, column=0)
        
        row=0
        col=0
        for bio in self.geos:
            lbl = tk.Label(self.geos_frame, text=bio)
            lbl.grid(row=row, sticky=tk.W, column=col)
            col=1-col
            row += 1 if col == 0 else 0
        
        row +=1
        col=0
        
        # frm = tk.Frame(self.geos_frame)
        # frm.grid(row=row, sticky=tk.SW+tk.E, column=0, columnspan=2)
        
        for body in self.bodies:
            for bio in body['geos']:
                info = '#'+ str(body['short']) +' '+ str(bio['species']) +': '+ str(bio['scans']) +'/'+ str(bio['max'])              
                lbl = tk.Label(self.geos_frame, text=info)
                lbl.grid(row=row, sticky=tk.W, column=0, columnspan=2)
                row += 1
        
        theme.update(self.geos_frame)
        theme.update(self.parent_frame)