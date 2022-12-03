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

VERSION = "0.1.0"
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
        
this = ExplorerCThis()


def plugin_start3(plugin_dir: str) -> str:
    return plugin_name +" "+ VERSION
    

def plugin_stop():
    """
    EDMC is closing
    """
    this.compass.dismiss()


def plugin_app(parent: tk.Frame) -> tk.Frame:
    """
    TK widgets for the EDMarketConnector main window
    """
    this.frame = tk.Frame(parent)
    this.signals.setup_frame(this.frame)
    this.compass.setup_frame(this.frame)
    theme.update(this.frame)

    return this.frame


def dashboard_entry(cmdr: str, is_beta: bool, entry: Dict[str, Any]):
    """
    Mise à jour du fichier status.json
    """
    if 'Fuel' in entry and entry['Fuel']:
        this.compass.set_fuel_main(entry['Fuel']['FuelMain'], entry['Fuel']['FuelReservoir'])
    if 'Latitude' in entry and entry['Latitude']:
        this.compass.set_Latitude( entry['Latitude'] )
        check_open_compass()
    if 'Longitude' in entry and entry['Longitude']:
        this.compass.set_Longitude( entry['Longitude'] )
        check_open_compass()
    if 'Heading' in entry and entry['Heading']:
        this.compass.set_Heading( entry['Heading'] )
        check_open_compass()
    if 'Altitude' in entry and entry['Altitude']:
        this.compass.set_Altitude( entry['Altitude'] )
        check_open_compass()


def journal_entry(
    cmdr: str, is_beta: bool, system: str, station: str, entry: MutableMapping[str, Any], state: Mapping[str, Any]
) -> None:
    """
    Methode de scrutation de maj du journal ED par EDMC
    """
    if entry['event'] == 'FSDJump':
        this.signals.journal_FSDJump()
        
    if entry['event'] == 'FSSDiscoveryScan':
        this.signals.journal_FSSDiscoveryScan(entry)
        
    if entry['event'] == 'Scan':
        this.signals.journal_Scan(entry)
            
    if entry['event'] == 'FSSBodySignals':
        this.signals.journal_FSSBodySignals(entry)
                    
    if entry['event'] == 'SAASignalsFound':
        this.signals.journal_SAASignalsFound(entry)

    if entry['event'] == 'LaunchSRV':
        this.compass.set_ModeSRV(True)
        logger.info("-- ouverture du compass --")
        check_open_compass()

    if entry['event'] == 'DockSRV':
        this.compass.set_ModeSRV(False)
        logger.info("-- fermeture du compass --")
        this.compass.dismiss()
    
    if entry['event'] == 'Loadout':
        this.compass.set_FuelCapacity(entry['FuelCapacity']['Main'])
        this.compass.set_HullHealth(entry['HullHealth'])
    
    if entry['event'] == 'HullDamage': # and entry['PlayerPilot']:
        this.compass.set_HullHealth(entry['Health'])
        
    if entry['event'] == 'Synthesis':
        if entry['Name'] == 'Repair Premium':
            this.compass.set_HullHealth(0.99)
        if entry['Name'] == 'Repair Basic':
            this.compass.set_HullHealth(0.99)
        if entry['Name'] == 'Repair Standard':
            this.compass.set_HullHealth(0.99)
        
        if entry['Name'] == 'Fuel Premium':
            this.compass.set_fuel_main(0, 0.99)
        if entry['Name'] == 'Fuel Basic':
            this.compass.set_fuel_main(0, 0.99)
        if entry['Name'] == 'Fuel Standard':
            this.compass.set_fuel_main(0, 0.99)
        
    # if state['HullValue']:
    #     this.compass.set_HullHealth(state['HullValue'])
        
    # if entry['ShieldsUp']:
    #     this.compass.set_ShieldsUp(entry['ShieldsUp'])
            

def check_open_compass():
    if this.compass.getOut:
        logger.info("-- ouverture du compass --")
        this.compass.popup()
        threading.Thread(target=worker, daemon=True, name='C14 compass_loop').start()
        
def worker():
    logger.info("compass loop start")
    this.compass.getOut = False
    while not this.compass.getOut:
        try:
            this.compass.update_canvas()
            this.compass.update_alt_canvas()
        except Exception as e:
            logger.info("plantage", exc_info=e)
        sleep(1/10)
    logger.info("compass loop ends")
    
