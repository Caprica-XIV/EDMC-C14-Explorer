import logging
import os
import random
import threading
from time import sleep
import tkinter as tk
from typing import Any, Dict, Mapping, MutableMapping, Optional
from tkinter import ttk
from config import config, appname
from theme import theme

from elements.C14Signals import SignalsC14
from elements.C14Compass import CompassC14
from elements.C14Hudinfo import HudInfoC14
from elements.C14Pip import PipC14
from elements.C14Altimeter import AltimeterC14
from elements.C14Biomes import BiomesC14
from C14Flags import FlagsC14

VERSION = "0.4.2"
plugin_name = os.path.basename(os.path.dirname(__file__))
logger = logging.getLogger(f'{appname}.{plugin_name}')

# If the Logger has handlers then it was already set up by the core code, else
# it needs setting up here.
if not logger.hasHandlers():
    level = logging.INFO  # So logger.info(...) is equivalent to print()

    logger.setLevel(level)
    logger_channel = logging.StreamHandler()
    logger_formatter = logging.Formatter(f'%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d:%(funcName)s: %(message)s')
    logger_formatter.default_time_format = '%Y-%m-%d %H:%M:%S'
    logger_formatter.default_msec_format = '%s.%03d'
    logger_channel.setFormatter(logger_formatter)
    logger.addHandler(logger_channel)

class ExplorerCThis:
    """Holds module globals."""
    def __init__(self, scale: int):
        self.frame: Optional[tk.Frame]
        self.signals = SignalsC14()
        self.compass = CompassC14(logger, scale)
        self.altimeter = AltimeterC14(logger, scale)
        self.hudinfo = HudInfoC14(logger, scale)
        self.pips = PipC14(logger, scale)
        self.biomes = BiomesC14(logger)
        self.f_system: Optional[tk.Frame]
        self.f_biomes: Optional[tk.Frame]
        self.nearBody = -1
        self.plugin_dir = ''
        self.ui_scale = scale
        
this = ExplorerCThis(config.get_int('ui_scale'))


def plugin_start3(plugin_dir: str) -> str:
    this.plugin_dir = plugin_dir
    # this.ui_scale = config.get_int('ui_scale')
    return plugin_name +" "+ VERSION
    

def plugin_stop():
    """
    EDMC is closing
    """
    this.compass.getOut = True
    this.compass.dismiss()

def show_system():
    this.f_biomes.grid_remove()
    this.f_system.grid(row=0,column=0,sticky=tk.SW+tk.E)
    
def show_biomes():
    this.f_system.grid_remove()
    this.f_biomes.grid(row=0,column=0,sticky=tk.SW+tk.E)

def plugin_app(parent: tk.Frame) -> tk.Frame:
    """
    TK widgets for the EDMarketConnector main window
    """
    this.frame = tk.Frame(parent)
    # row du hud compass pip altimetre fuel hull g
    row0 = tk.Frame(this.frame, border=None)
    row0.grid(row=0,sticky=tk.E+tk.W, column=0)
    this.compass.setup_frame(row0)
    this.altimeter.setup_frame(row0)
    this.pips.setup_frame(row0)
    this.hudinfo.setup_frame(row0, plugin_dir=this.plugin_dir)
    
    # row du tab pour signaux, bio etc
    row1 = tk.Frame(this.frame, border=None)
    row1.grid(row=1,sticky=tk.E+tk.W, column=0, pady=5)   
    
    row1_1 = tk.Frame(row1, border=None)
    row1_1.grid(row=0,sticky=tk.E+tk.W, column=0)   

    bt_System = tk.Button(row1_1, text='System', command=show_system)
    bt_System.grid(row=0,column=0,sticky=tk.W)

    bt_Biomes = tk.Button(row1_1, text='Biomes', command=show_biomes)
    bt_Biomes.grid(row=0,column=1,sticky=tk.W)

    row1_2 = tk.Frame(row1, border=1)
    row1_2.grid(row=1,sticky=tk.E+tk.W, column=0)   

    this.f_system = tk.Frame(row1_2, border=2)
    this.f_system.grid(row=0,sticky=tk.SW+tk.E, column=0)
    this.signals.setup_frame(this.f_system)    
    
    # tab biomes
    this.f_biomes = tk.Frame(row1_2, border=2)
    # f_biomes.grid(row=0,sticky=tk.E+tk.W, column=0)
    this.biomes.setup_frame(this.f_biomes)
    
    theme.update(this.frame)
    open_signals()
    
    return this.frame


def dashboard_entry(cmdr: str, is_beta: bool, entry: Dict[str, Any]):
    """
    Mise à jour du fichier status.json
    """
    if 'Fuel' in entry:
        this.hudinfo.set_fuel_main(entry['Fuel']['FuelMain'], entry['Fuel']['FuelReservoir'])
    if 'Latitude' in entry:
        this.compass.set_Latitude( entry['Latitude'] )
        open_compass()
    if 'Longitude' in entry:
        this.compass.set_Longitude( entry['Longitude'] )
        open_compass()
    if 'Heading' in entry:
        this.compass.set_Heading( entry['Heading'] )
        open_compass()
    if 'Altitude' in entry:
        this.altimeter.set_Altitude( entry['Altitude'] )
        open_compass()
    if 'Pips' in entry:
        this.pips.set_pip(entry['Pips'][0], entry['Pips'][1], entry['Pips'][2])
    if 'Body' in entry:
        this.altimeter.set_SurfaceGravity(this.signals.get_SurfaceGravity(entry['Body']))
    if 'Gravity' in entry:
        this.altimeter.set_SurfaceGravity(entry['Gravity']*10.0)
    if 'Health' in entry:
        # on foot health
        this.hudinfo.set_HullHealth(entry['Health'])
    if 'Flags' in entry:
        flag = entry['Flags']
        this.hudinfo.set_ShieldsUp((flag & FlagsC14.flag_ShieldsUp))
    if 'Flags2' in entry:
        #decoupage de la valeur selon les flag et signification
        flag = entry['Flags2']
        this.hudinfo.set_ModeOnFoot((flag & FlagsC14.flag2_OnFoot))
        
def journal_entry(
    cmdr: str, is_beta: bool, system: str, station: str, entry: MutableMapping[str, Any], state: Mapping[str, Any]
) -> None:
    """
    Methode de scrutation de maj du journal ED par EDMC
    """
    
    if state['Body']:
        this.biomes.state_body=state['Body']
        
    if state['Modules']:
        for itm in state['Modules']:
            if 'FuelTank' in itm:                                
                tank = state['Modules']['FuelTank']['Item']
                if 'size6' in tank:
                    this.hudinfo.set_FuelCapacity(64)
                if 'size5' in tank:
                    this.hudinfo.set_FuelCapacity(32)
                if 'size4' in tank:
                    this.hudinfo.set_FuelCapacity(16)
                if 'size3' in tank:
                    this.hudinfo.set_FuelCapacity(8)
                if 'size2' in tank:
                    this.hudinfo.set_FuelCapacity(4)
                if 'size1' in tank:
                    this.hudinfo.set_FuelCapacity(2)
                if 'size0' in tank:
                    this.hudinfo.set_FuelCapacity(1)
            
    
    if entry['event'] == 'Location':
        if 'Latitude' in entry: this.compass.set_Latitude( entry['Latitude'] )
        if 'Longitude' in entry: this.compass.set_Longitude( entry['Longitude'] )
        if( entry['Docked']): open_compass()
        else: open_signals()
    
    if entry['event'] == 'LeaveBody':
        this.nearBody = 0
        this.altimeter.set_SurfaceGravity(-1)
        open_signals()
            
    if entry['event'] == 'ApproachBody':
        this.nearBody = 1
        this.altimeter.set_SurfaceGravity(this.signals.get_SurfaceGravity(entry['BodyID']))
        open_compass()
        
    if entry['event'] == 'FSDJump':
        this.altimeter.set_SurfaceGravity(-1)
        this.signals.journal_FSDJump()
        this.biomes.journal_FSDJump()
        open_signals()
        
    if entry['event'] == 'FSSDiscoveryScan':
        this.signals.journal_FSSDiscoveryScan(entry)
        open_signals()
        
    if entry['event'] == 'Scan':
        this.signals.journal_Scan(entry)
        open_signals()
            
    if entry['event'] == 'FSSBodySignals':
        this.signals.journal_FSSBodySignals(entry)
        this.biomes.journal_FSSBodySignals(entry)
        open_signals()
                    
    if entry['event'] == 'SAASignalsFound':
        if 'Genuses' in entry:
            this.biomes.journal_SAASignalsFound(entry)
            show_biomes()
        if 'Signals' in entry:
            this.signals.journal_SAASignalsFound(entry)

    if entry['event'] == 'LaunchSRV':
        this.hudinfo.set_ModeSRV(True)
        open_compass()

    if entry['event'] == 'DockSRV':
        this.hudinfo.set_ModeSRV(False)
    
    if entry['event'] == 'Embark':
        this.hudinfo.set_ModeOnFoot(False)
        this.hudinfo.set_ModeSRV(entry['SRV'])
    
    if entry['event'] == 'Loadout':
        this.hudinfo.set_FuelCapacity(entry['FuelCapacity']['Main'])
        this.hudinfo.set_HullHealth(entry['HullHealth'])
        
    if entry['event'] == 'LoadGame':
        this.hudinfo.set_FuelCapacity(entry['FuelCapacity'])
    
    if entry['event'] == 'HullDamage': # and entry['PlayerPilot']:
        this.hudinfo.set_HullHealth(entry['Health'])
        
    if entry['event'] == 'Synthesis':
        if entry['Name'] == 'Repair Premium':
            this.hudinfo.set_HullHealth(1.0)
        if entry['Name'] == 'Repair Basic':
            this.hudinfo.set_HullHealth(1.0)
        if entry['Name'] == 'Repair Standard':
            this.hudinfo.set_HullHealth(1.0)
        
        if entry['Name'] == 'Fuel Premium':
            this.hudinfo.set_fuel_main(0, 1.0)
        if entry['Name'] == 'Fuel Basic':
            this.hudinfo.set_fuel_main(0, 1.0)
        if entry['Name'] == 'Fuel Standard':
            this.hudinfo.set_fuel_main(0, 1.0)
    
    if entry['event'] == 'ShieldState':
        this.hudinfo.set_ShieldsUp(entry['ShieldsUp'])
    
    if entry['event'] == 'CodexEntry':
        this.biomes.CodexEntry(entry)
    
    if entry['event'] == 'ScanOrganic':
        this.biomes.ScanOrganic(entry)
            

def open_compass():
    if this.nearBody != 0:
        this.signals.dismiss()
        this.compass.popup()
        this.altimeter.popup()

def open_signals():
    this.compass.dismiss()
    this.altimeter.dismiss()
    this.biomes.dismiss()
    this.signals.popup()
    
def open_biomes():
    this.signals.dismiss()
    this.biomes.popup()
