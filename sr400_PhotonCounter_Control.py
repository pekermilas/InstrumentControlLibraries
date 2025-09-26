# -*- coding: utf-8 -*-
"""
Created on Thu Sep 25 08:35:50 2025

@author: admin
"""
# EXAMPLE CALLS
# t = sr400.sr400()
# t.open()
# t.dev.query('SS 1')

# EXAMPLE CALLS
# t = sr400.sr400()
# t.open()
# t.dev.query('SS 1')

import pyvisa as visa
import os

# os.chdir('C:/Users/admin/Desktop/PEKER/PulseWorks/PhotonCountersControl')

class sr400(object):

    def __init__(self, port = None):
        # self.port = port or "COM3"
        self.port = port or 'GPIB0::23::INSTR'
        self.dev = None
        self.visaLib = 'ni-visa' # or 'py-visa'
        self.rm = None
            
    def open(self):
        if self.dev is None:
            if self.visaLib == 'py-visa':
                self.rm = visa.ResourceManager('@py')
            if self.visaLib == 'ni-visa':
                self.rm = visa.ResourceManager()
                
            try:
                self.dev = self.rm.open_resource(self.port)
                self.dev.read_termination = '\n'
                self.dev.write_termination = '\n'
                self.dev.baud_rate = 19200 # Min : 300, Max : 19200
            
                # self.dev.write("*RST")
                self.dev.query("SS 1")
            except:    
                self.dev = None

    def close(self):
        if not self.dev is None:
            self.dev.close()
            self.dev = None
            self.rm.close()
            self.rm = None

    def read(self):
        return self.dev.read()
    
    def write(self, writeStr = None):
        if not self.dev is None:
            self.dev.write(writeStr)

    def write(self, writeStr = None):
        if not self.dev is None:
            self.dev.write(writeStr)

    def query(self, queryStr = None):
        if not self.dev is None:
            return self.dev.query(queryStr)

    def simulate_button(self, botton = 'STOP'):
        keydict = {'DOWN': 0, 'RIGHT': 1, 'LEVEL': 2, 'SETUP': 3, 
                   'COM': 4, 'STOP': 5, 'LOCAL': 6, 'RESET': 7,'LEFT': 8, 
                   'UP': 9, 'MODE': 10, 'AGATE': 11,'BGATE': 12, 'START': 13}
        self.write('CK ' + str(keydict[botton]))

    def read_cursor(self):
        cursordict = {'0\r': 'LEFT', '1\r': 'RIGHT', '2\r': 'INACTIVE'}
        return cursordict[self.query('SC')]
          
    def check_ready(self):
        return bool(int(self.query('SS 1')))
# -------------------------TEST HERE ONWARDS---------------------    
    def read_last_count(self, channel = 'ch1'):
        if self.check_ready():
            if channel == 'ch1':
                count = int(self.query('QA').rstrip())
            if channel == 'ch2':
                count = int(self.query('QB').rstrip())
        else:
            count = -1
        return count

    def read_count_now(self, channel = 'ch1'):
        if channel == 'ch1':
            count = int(self.query('XA').rstrip())
        if channel == 'ch2':
            count = int(self.query('XB').rstrip())
        return count
            
            