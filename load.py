import logging
import os
import random
import threading
from time import sleep
import tkinter as tk
from typing import Any, Dict, Mapping, MutableMapping, Optional
from config import config, appname
from theme import theme

from signals import SignalsC14
from compass import CompassC14
from hudinfo import HudInfoC14
from pip import PipC14
from altimeter import AltimeterC14

VERSION = "0.3.0"
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

    def __init__(self):
        self.frame: Optional[tk.Frame]
        self.signals = SignalsC14()
        self.compass = CompassC14(logger)
        self.altimeter = AltimeterC14(logger)
        self.hudinfo = HudInfoC14(logger)
        self.pips = PipC14(logger)
        self.getOut = True 
        self.nearBody = -1
        
this = ExplorerCThis()


def plugin_start3(plugin_dir: str) -> str:
    return plugin_name +" "+ VERSION
    

def plugin_stop():
    """
    EDMC is closing
    """
    this.getOut = True
    this.compass.dismiss()


def plugin_app(parent: tk.Frame) -> tk.Frame:
    """
    TK widgets for the EDMarketConnector main window
    """
    this.frame = tk.Frame(parent)
    row0 = tk.Frame(this.frame, border=None)
    row0.grid(row=0,sticky=tk.E+tk.W, column=0)
    
    row0_1 = tk.Frame(row0, border=None)
    row0_1.grid(row=0,sticky=tk.E+tk.W, column=0, columnspan=4)
    row0_2 = tk.Frame(row0, border=None)
    row0_2.grid(row=0,sticky=tk.W, column=4)
    
    row1 = tk.Frame(this.frame, border=None)
    row1.grid(row=1,sticky=tk.E+tk.W, column=0)
    
    
    this.signals.setup_frame(row0_1)
    this.compass.setup_frame(row0_1)
    this.altimeter.setup_frame(row0_1)
    
    this.pips.setup_frame(row0_2)
    
    this.hudinfo.setup_frame(row1)
    
    theme.update(this.frame)
    
    open_signals()
    
    threading.Thread(target=worker, daemon=True, name='C14 canvas loop').start()
    
    return this.frame


def dashboard_entry(cmdr: str, is_beta: bool, entry: Dict[str, Any]):
    """
    Mise à jour du fichier status.json
    """
    if 'Fuel' in entry and entry['Fuel']:
        this.hudinfo.set_fuel_main(entry['Fuel']['FuelMain'], entry['Fuel']['FuelReservoir'])
    if 'Latitude' in entry and entry['Latitude']:
        this.compass.set_Latitude( entry['Latitude'] )
        open_compass()
    if 'Longitude' in entry and entry['Longitude']:
        this.compass.set_Longitude( entry['Longitude'] )
        open_compass()
    if 'Heading' in entry and entry['Heading']:
        this.compass.set_Heading( entry['Heading'] )
        open_compass()
    if 'Altitude' in entry and entry['Altitude']:
        this.altimeter.set_Altitude( entry['Altitude'] )
        open_compass()
    if 'Pips' in entry:
        this.pips.set_pip(entry['Pips'][0], entry['Pips'][1], entry['Pips'][2])
    if 'Body' in entry:
        this.hudinfo.set_SurfaceGravity(this.signals.get_SurfaceGravity(entry['Body']))


def journal_entry(
    cmdr: str, is_beta: bool, system: str, station: str, entry: MutableMapping[str, Any], state: Mapping[str, Any]
) -> None:
    """
    Methode de scrutation de maj du journal ED par EDMC
    """
    if entry['event'] == 'Location':
        this.compass.set_Latitude( entry['Latitude'] )
        this.compass.set_Longitude( entry['Longitude'] )
        if( entry['Docked']): open_compass()
        else: open_signals()
    
    if entry['event'] == 'LeaveBody':
        this.nearBody = 0
        this.hudinfo.set_SurfaceGravity(-1)
        open_signals()
            
    if entry['event'] == 'ApproachBody':
        this.nearBody = 1
        this.hudinfo.set_SurfaceGravity(this.signals.get_SurfaceGravity(entry['BodyID']))
        if entry['BodyID'] in this.signals.biomes:
            this.pips.set_biomes(this.signals.biomes[entry['BodyID']])
        open_compass()
        
    if entry['event'] == 'FSDJump':
        this.hudinfo.set_SurfaceGravity(-1)
        this.signals.journal_FSDJump()
        open_signals()
        
    if entry['event'] == 'FSSDiscoveryScan':
        this.signals.journal_FSSDiscoveryScan(entry)
        open_signals()
        
    if entry['event'] == 'Scan':
        this.signals.journal_Scan(entry)
        open_signals()
            
    if entry['event'] == 'FSSBodySignals':
        this.signals.journal_FSSBodySignals(entry)
        open_signals()
                    
    if entry['event'] == 'SAASignalsFound':
        this.signals.journal_SAASignalsFound(entry)
        open_signals()

    if entry['event'] == 'LaunchSRV':
        this.hudinfo.set_ModeSRV(True)
        open_compass()

    if entry['event'] == 'DockSRV':
        this.hudinfo.set_ModeSRV(False)
    
    if entry['event'] == 'Loadout':
        this.hudinfo.set_FuelCapacity(entry['FuelCapacity']['Main'])
        this.hudinfo.set_HullHealth(entry['HullHealth'])
        
    if entry['event'] == 'LoadGame':
        this.hudinfo.set_FuelCapacity(entry['FuelCapacity'])
    
    if entry['event'] == 'HullDamage': # and entry['PlayerPilot']:
        this.hudinfo.set_HullHealth(entry['Health'])
        
    if entry['event'] == 'Synthesis':
        if entry['Name'] == 'Repair Premium':
            this.hudinfo.set_HullHealth(0.99)
        if entry['Name'] == 'Repair Basic':
            this.hudinfo.set_HullHealth(0.99)
        if entry['Name'] == 'Repair Standard':
            this.hudinfo.set_HullHealth(0.99)
        
        if entry['Name'] == 'Fuel Premium':
            this.hudinfo.set_fuel_main(0, 0.99)
        if entry['Name'] == 'Fuel Basic':
            this.hudinfo.set_fuel_main(0, 0.99)
        if entry['Name'] == 'Fuel Standard':
            this.hudinfo.set_fuel_main(0, 0.99)
    
    if entry['event'] == 'ShieldState':
        this.hudinfo.set_ShieldsUp(entry['ShieldsUp'])
            

def open_compass():
    if this.nearBody != 0:
        this.signals.dismiss()
        this.compass.popup()
        this.altimeter.popup()

def open_signals():
    this.compass.dismiss()
    this.altimeter.dismiss()
    this.signals.popup()
        
def worker():
    logger.info("loop start")
    this.getOut = False
    while not this.getOut:
        try:
            this.compass.update_canvas()
            this.altimeter.update_alt_canvas()
            this.pips.update_pip_canvas()
        except Exception as e:
            logger.info("plantage", exc_info=e)
        sleep(1/10)