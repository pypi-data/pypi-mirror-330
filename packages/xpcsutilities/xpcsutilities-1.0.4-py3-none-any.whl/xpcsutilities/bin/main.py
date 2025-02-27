#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 12:02:31 2021

@author: opid02
"""

import argparse
from PyQt5.QtWidgets import QApplication
from xpcsutilities.gui.mainwindow import MainWindow
import logging
import sys

logging.basicConfig(format='%(levelname)s %(name)s:%(lineno)d %(message)s',
                    handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)

def main():
    
    parser = argparse.ArgumentParser(description="Display XPCS result files")
    
    parser.add_argument('-v', dest='verbose', action='store_true', default=False, help='Verbose mode (minimum message level=debug)')
    parser.add_argument('--quiet', dest='quiet', action='store_true', default=False, help='Quiet mode (minimum message level=warning)')
    
    args = parser.parse_args()
    
    print(args)
            
    # Set the log level of each package according to the defined verbosity
    loglevel = logging.INFO
    
    if args.verbose:
        loglevel = logging.DEBUG
    elif args.quiet:
        loglevel = logging.WARNING
        
    logger.setLevel(loglevel)
    
        
    for name in logging.root.manager.loggerDict:
        if name.startswith('xpcsutilities'):
            logger.debug(name)
            logging.getLogger(name).setLevel(loglevel)
            
    
    app = QApplication([])
    
    win = MainWindow()
    
    sys.exit(app.exec_())