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

# os.chdir('C:/Users/admin/Documents/GitHub/InstrumentControlLibraries')

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

# -------------------------TEST HERE ONWARDS---------------------      
    def check_status_byte(self, bit = 0):
        # All in manual p.48-49
        # 0 : Checks if parameter change
        # 1 : Checks if count finished
        # 2 : Checks if scan finished
        # 3 : Checks if overrun
        # 4 : Checks if gate error
        # 5 : Checks if recall error
        # 6 : Checks if SQR
        # 7 : Checks if command error
        return bool(int(self.query('SS '+str(bit)).rstrip())) 
        
    def check_secondary_status_byte(self, bit = 0):    
        # All in manual p.48-49
        # 0 : Checks if triggered
        # 1 : Checks if inhibited
        # 2 : Checks if counting
        return bool(int(self.query('SI '+str(bit)).rstrip())) 

    def count_restart(self):
        self.write('CR') # (Manual p.45) Resets counters
        self.write('CS') # (Manual p.44) Starts counters

	def count_reset(self):
        self.write('CR') # (Manual p.45) Resets counters

    def count_stop(self):
        self.write('CH') # (Manual p.45) Stops counters

    def count_start(self):
        self.write('CS') # (Manual p.45) Starts counters

    def gate_delay(self, channel = 'A'):
        # (Manual p.44) Reports gate delay position
        delay = float(self.query('GZ ' + ('0' if channel == 'A' else '1'))).rstrip())
        return delay

    def gate_delay_set(self, channel = 'A', delay = 0.0):
        # (Manual p.44) Select gate 'A' or 'B', defaults to 'A'
		# The selected gate delay is set to t seconds 
        # where 0 <= t <= 999.2E-3, defaults to 0.0
        if 0 <= delay <= 999.2E-3:
            self.write('GD ' + ('0,' if channel == 'A' else '1,') + '%G' %delay)
        else:
            print('setting delay to 999.2E-3.')
            tMax = 999.2E-3
            self.write('GD ' + ('0,' if channel == 'A' else '1,') + '%G' %tMax)

    def gate_mode(self, channel = 'A', mode = 'CW', read = False):
        # (Manual p.43) Select gate 'A' or 'B', defaults to 'A'
       