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

# I need to write proper default mechanism for all the methods
# which uses read argument for their cases of not given the other
# parameter!!!

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
            returnVal = 0
        else:
            returnVal = -1
        return returnVal

    def close(self):
        if not self.dev is None:
            self.dev.close()
            self.dev = None
            self.rm.close()
            self.rm = None
            returnVal = 0
        else:
            returnVal = -1
        return returnVal
    
    def read(self):
        return self.dev.read()
    
    def write(self, writeStr = None):
        if not self.dev is None:
            self.dev.write(writeStr)
            returnVal = 0
        else:
            returnVal = -1
        return returnVal
    
    def query(self, queryStr = None):
        if not self.dev is None:
            return self.dev.query(queryStr)

    def simulate_button(self, botton = 'STOP'):
        keydict = {'DOWN': 0, 'RIGHT': 1, 'LEVEL': 2, 'SETUP': 3, 
                   'COM': 4, 'STOP': 5, 'LOCAL': 6, 'RESET': 7,'LEFT': 8, 
                   'UP': 9, 'MODE': 10, 'AGATE': 11,'BGATE': 12, 'START': 13}
        self.write('CK ' + str(keydict[botton]))
        return 0

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
        return 0
    
    def count_reset(self):
        self.write('CR') # (Manual p.45) Resets counters
        return 0
    def count_stop(self):
        self.write('CH') # (Manual p.45) Stops counters
        return 0
    
    def count_start(self):
        self.write('CS') # (Manual p.45) Starts counters
        return 0

    def gate_delay(self, channel = 'A'):
        # (Manual p.44) Reports gate delay position
        delay = float(self.query('GZ ' + ('0' if channel == 'A' else '1'))).rstrip()
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
        return 0
    
    def gate_mode(self, channel = 'A', mode = 'CW', read = False):
        # (Manual p.43) Select gate 'A' or 'B', defaults to 'A'
        # param channel: DESCRIPTION, defaults to 'A'
		# param mode: If it is changed to SCAN, the delay begins 
        # scanning from the start position on the next count period. 
        # If it is changed to FIXED, the delay returns to the start 
        # position immediately, defaults to 'CW'
		# param query: True for asking, defaults to False for setting
        gate_mode_dict = {'CW':0, 'FIXED':1, 'SCAN': 2}
        if read:
            returnVal = self.query('GM '+ ('0' if channel == 'A' else '1')).rstrip()
        else:
            if mode in list(gate_mode_dict):
                self.write('GM '+ ('0,' if channel == 'A' else '1,') + str(gate_mode_dict[mode]))
                returnVal = 0
            else:
                print('Non-valid gate mode!')
                returnVal = -1
        return returnVal
    
    def gate_scan_step(self, channel = 'A', step:float = 0.0, read = False):
        # (Manual p.43)
        if read:
            returnVal = self.query('GY '+ ('0' if channel == 'A' else '1')).rstrip()
        else: 
            if 0 <= step <= 999.2E-3:
                self.write('GY ' + ('0,' if channel == 'A' else '1,') + '%G' %step)
                returnVal = 0
            else:
                print('stetting range  to  99.92E-3.')
                stepMax = 99.92E-3
                self.write('GY ' + ('0,' if channel == 'A' else '1,') + '%G' %stepMax)
                returnVal = 0
        return returnVal

    def gate_width(self, channel = 'A', window = 0.0, read = False):
        # (Manual p.44)
        if read:
            returnVal = self.query('GW '+ ('0' if channel == 'A' else '1')).rstrip()
        else:
            if 0.005E-6 <= window <= 999.2E-3:
                self.write('GW ' + ('0,' if channel == 'A' else '1,') + '%G' %window)
                returnVal = 0
            else:
                widthMax = 999.2E-3
                self.write('GW ' + ('0,' if channel == 'A' else '1,') + '%G' %window)
                returnVal = 0
        return returnVal

    def lcd_message(self, message = None):
        if message is None:
            self.write('MS')
        else:
            if len(message) <= 24: 
                self.write('MS '+ message)
            else:
                self.write('MS '+ message[:24])
        return 0

    def display_mode(self, conti = True):
        self.write('SD ' + ('0' if conti else '1'))
        return 0

    def scan_periods(self, num = 0):
        if num == 0:
            returnVal = self.query('NP').rstrip()
        else:
            if 1 <= num <= 2000:
                self.write('NP ' + str(num))
                returnVal = 0
            else:
                maxNum = 2000
                self.write('NP ' + str(maxNum))
                returnVal = -1
        return returnVal

    def scan_position(self):
        return self.query('NN').rstrip()
    
    def scan_end_mode(self, mode = 'STOP', read = False):
        if read:
            status = bool(int(self.query('NE').rstrip()))
            returnVal = 'STOP' if status else 'START'
        else:
            self.write('NE ' + ('0' if mode=='STOP' else '1'))
            returnVal = 0
        return returnVal

	def reset_all(self):
        self.write('CL')
        return 0

    def count_mode(self, mode = None):
        if mode is None:
            self.query('CM').rstrip()
        if mode == 0:
            # Both A and B for T preset
        if mode == 1:
            # A-B for T preset
        if mode == 2:
            # A+B for T preset
        if mode == 3:
            # A for B preset
            
            







































