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

os.chdir('C:/Users/admin/Documents/GitHub/InstrumentControlLibraries')

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

    def read_buffer_count(self, channel = 'ch1', point = 1):
        # This is on the fly query of measured counts!!!
        # Min point is 1 and Max point is 2000. Anything out
        # of these limits produce error so -1!!!
        if channel == 'ch1':
            count = int(self.query('QA ' + str(point)).rstrip())
        if channel == 'ch2':
            count = int(self.query('QB ' + str(point)).rstrip())
        return count

# -------------------------PUT THESE TOGETHER AS STATUS BYTE--------------------- 
    def check_param_change(self):
        return bool(int(self.query('SS 0').rstrip()))

    def check_count_finish(self):
        return bool(int(self.query('SS 1').rstrip()))

    def check_scan_finish(self):
        return bool(int(self.query('SS 2').rstrip()))

    def check_overrun(self):
        return bool(int(self.query('SS 3').rstrip()))

    def check_gate_error(self):
        # (Manual p.48) This bit is set whenever a gate is 
        # missed. This can occur if a gate delay or width 
        # exceeds the trigger period minus 1 µs
        return bool(int(self.query('SS 4').rstrip()))

    def check_recall_error(self):
        # (Manual p.48) This bit is set if a recall from a stored 
        # setting detects an error in the recalled data. If an 
        # error is found, the instrument setup is not altered.
        return bool(int(self.query('SS 5').rstrip()))

    def check_SRQ(self):
        # (Manual p.49)
        return bool(int(self.query('SS 6').rstrip()))

    def check_command_error(self):
        # (Manual p.49)
        return bool(int(self.query('SS 7').rstrip()))

# -------------------------PUT THESE TOGETHER AS SECONDARY STATUS BYTE--------------------- 
    def check_triggered(self):
        return bool(int(self.query('SI 0').rstrip()))

    def check_inhibited(self):
        return bool(int(self.query('SI 1').rstrip()))

    def check_counting(self):
        return bool(int(self.query('SI 2').rstrip()))


    def count_restart(self):
        self.write('CR') # (Manual p.45) Resets counters
        self.write('CS') # (Manual p.44) Starts counters








# -------------------------TEST HERE ONWARDS---------------------             