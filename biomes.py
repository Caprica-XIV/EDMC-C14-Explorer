import logging
from typing import Any, MutableMapping, Optional
import tkinter as tk
from theme import theme

class BiomesC14():
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.parent_frame: Optional[tk.Frame]
        self.biomes_frame: Optional[tk.Frame]
        self.biomes = []
        self.bodies = []
        self.state_body=''

    def setup_frame(self, parent: tk.Frame):
        self.parent_frame = parent
        self.biomes_frame = tk.Frame(self.parent_frame)
        theme.update(self.parent_frame)
        
    def popup(self):
        # self.biomes_frame.grid(row=0, sticky=tk.E+tk.W, column=0)
        a=2
        
    def dismiss(self):
        # self.biomes_frame.grid_remove()
        a=2
            
    def get_body(self, entry: MutableMapping[str, Any]):
        """ Retourne l'objet json interne représentant le body et ses biomes """
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
            split= entry['BodyName'].split(' ')
            if '0123456789' in split[-1]:
                short=split[-1]
            else:
                short=split[len(split)-2] + split[-1]
        elif 'System' in entry:
            name = entry['System']
        else:
            name = self.state_body
        
        self.bodies.append({'id': id,
                            'name': name,
                            'short': short,
                            'biologicals': 0,
                            'biomes': []
                            })
    
    def CodexEntry(self, entry: MutableMapping[str, Any]):
        """ action lors d'un scan en ship"""
        if 'Category' not in entry or 'Biology' not in entry['Category']: return
        species = entry['Name_Localised']
        self.scanEntrySpecies(species, entry)        
        
    def ScanOrganic(self, entry: MutableMapping[str, Any]):
        """ action lors d'un scan a pieds """
        if 'ScanOrganic' not in entry['event']: return
        species = entry['Species_Localised']
        self.scanEntrySpecies(species, entry)
        
    def scanEntrySpecies(self, species: str, entry: MutableMapping[str, Any]):
        """ analyse le scan et définit si nouveau ou en cours """
        body = self.get_body(entry)
        found=False
        for bio in body['biomes']:
            if species in bio['species']:
                found=True
                if 'ScanType' in entry and 'Analyse' in entry['ScanType']:
                    bio['scans'] = 3
                else:    
                    bio['scans'] += (1 if 'CodexEntry' not in entry['event'] else 0)
                break
        if not found:
            if 'ScanType' in entry and 'Analyse' in entry['ScanType']:
                body['biomes'].append({
                    'species': species,
                    'scans': 3
                })
            else:
                body['biomes'].append({
                    'species': species,
                    'scans': (1 if 'CodexEntry' not in entry['event'] else 0)
                })
        self.update_frame()
    
    def journal_FSDJump(self):
        self.biomes = []
        self.bodies = []
        self.update_frame()
    
    def journal_FSSBodySignals(self, entry: MutableMapping[str, Any]):
        update=False
        if 'Signals' in entry:
            for sgnl in entry['Signals']:
                if 'Biological' in sgnl['Type']:
                    # on ajoute les info dans le détail
                    body = self.get_body(entry)
                    body['biologicals'] = sgnl['Count']
                    update=True
        if update : 
            self.update_frame()
                            
    def journal_SAASignalsFound(self, entry: MutableMapping[str, Any]):
        if 'Genuses' in entry:
            body = self.get_body(entry)
            for gen in entry['Genuses']:
                # dejà présent ?
                found = False
                for i in range(len(self.biomes)):
                    if gen['Genus_Localised'] in self.biomes[i]:
                        # connu, on ajoute le body
                        found = True
                        self.biomes[i] += ', '+ body['short']
                        break
                if not found:
                    self.biomes.append(gen['Genus_Localised'] +' on '+ body['short'])
                
            self.update_frame()
            self.popup()
    
    def update_frame(self):
        self.biomes_frame.destroy()
        self.biomes_frame = tk.Frame(self.parent_frame)
        self.biomes_frame.grid(row=0, sticky=tk.SW, column=0)
        
        row=0
        col=0
        for bio in self.biomes:
            lbl = tk.Label(self.biomes_frame, text=bio)
            lbl.grid(row=row, sticky=tk.W, column=col)
            col=1-col
            row += 1 if col == 0 else 0
        
        row +=1
        col=0
        
        # frm = tk.Frame(self.biomes_frame)
        # frm.grid(row=row, sticky=tk.SW+tk.E, column=0, columnspan=2)
        
        for body in self.bodies:
            for bio in body['biomes']:
                info = '#'+ str(body['short']) +' '+ str(bio['species']) +': '+ str(bio['scans']) +'/3'              
                lbl = tk.Label(self.biomes_frame, text=info)
                lbl.grid(row=row, sticky=tk.W+tk.E, column=0, columnspan=2)
                row += 1
        
        theme.update(self.biomes_frame)
        theme.update(self.parent_frame)