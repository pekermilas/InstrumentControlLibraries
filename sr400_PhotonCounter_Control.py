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
# Composition with Helper Classes python

# class mode:
#     # aaa
#     print("mode")
    
# class levels:
#     # bbb
#     print("levels")
    
# class gates:
#     # ccc
#     print("gates")
    
# class front_panel:
#     # ddd
#     print("front panel")
    
# class store_recall:
#     # eee
#     print("store recall")
    
# class interface:
#     # fff
#     print("interface")
    
# class data:
#     # ggg
#     print("data")

class sr400:

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

# Section MODE:
    def mode_countMode(self, mode = None):
        # (Manual p.41)
        modeDict = {'A,B': 0, 'A-B': 1, 'A+B': 2, 'A*B': 3}
        if mode is None:
            returnVal = self.query('CM').rstrip()
        if mode in list(modeDict):
            self.write('CM ' + '%G' %modeDict[mode])
            returnVal = 0
        else:
            self.write('CM ' + '%G' %0)
            returnVal = -1
        return returnVal

    def mode_counterToInput(self, counter = 'A', counterInput = None):
        counterDict = {'A': 0, 'B': 1, 'T': 2}
        if counterInput is None:
            returnVal = self.query('CI '+ '%G' %counterDict[counter]).rstrip()
        else:
            if counter == 'A':
                if counterInput == 0 or counterInput == 1:
                    self.write('CI '+ '%G' %counterDict[counter] + ',' + '%G' %counterInput)
                    returnVal = 0
                else:
                    self.write('CI '+ '%G' %counterDict[counter] + ',' + '%G' %0)
                    returnVal = -1
            if counter == 'B':
                if counterInput == 1 or counterInput == 2:
                    self.write('CI '+ '%G' %counterDict[counter] + ',' + '%G' %counterInput)
                    returnVal = 0
                else:
                    self.write('CI '+ '%G' %counterDict[counter] + ',' + '%G' %1)
                    returnVal = -1
            if counter == 'T':
                if counterInput == 0 or counterInput == 2 or counterInput == 3:
                    self.write('CI '+ '%G' %counterDict[counter] + ',' + '%G' %counterInput)
                    returnVal = 0
                else:
                    self.write('CI '+ '%G' %counterDict[counter] + ',' + '%G' %0)
                    returnVal = -1
        return returnVal
        
    def mode_counterPreset(self, counter = 'B', counterPreset = None):
        # counterPreset is not ins seconds! It is number of cycles of 10MHz clock
        counterDict = {'B': 1, 'T': 2}
        if counterPreset is None:
            returnVal = self.query('CP '+ '%G' %counterDict[counter]).rstrip()
        else:
            if 1 <= counterPreset <= 9E11:
                self.write('CP '+ '%G' %counterDict[counter] + ',' + '%G' %counterPreset)
                returnVal = 0
            else:
                self.write('CP '+ '%G' %counterDict[counter] + ',' + '%G' %9E11)
                returnVal = -1
        return returnVal
        
    def mode_scanPeriods(self, num = 0):
        if num == 0:
            returnVal = self.query('NP').rstrip()
        else:
            if 1 <= num <= 2000:
                self.write('NP ' + str(num))
                returnVal = 0
            else:
                maxNum = 2000
                self.write('NP ' + + '%G' %maxNum)
                returnVal = -1
        return returnVal

    def mode_scanPosition(self):
        return self.query('NN').rstrip()

    def mode_scanEnd(self, scanMode = None):
        if scanMode is None:
            returnVal = self.query('NE').rstrip()
        else:
            if scanMode == 0 or scanMode == 1:
                self.write('NE '+ '%G' %scanMode)
                returnVal = 0
            else:
                self.write('NE '+ '%G' %0)
                returnVal = -1
        return returnVal

    def mode_dwellTime(self, dwellTime = None):
        if dwellTime is None:
            returnVal = self.query('DT').rstrip()
        else:
            if 2E-3 <= dwellTime <= 6E1:
                self.write('DT ' + '%G' %dwellTime)
                returnVal = 0
            else:
                if dwellTime==0:
                    self.write('DT ' + '%G' %dwellTime)
                    returnVal = 1
                if dwellTime <= 2E-3:
                    self.write('DT ' + '%G' %2E-3)
                    returnVal = -1
                if dwellTime >= 6E1:
                    self.write('DT ' + '%G' %6E1)
                    returnVal = -1
        return returnVal

    def mode_analogSource(self, counter = None):
        sourceDict = {'A': 0, 'B': 1, 'A-B': 2, 'A+B': 3}
        if counter is None:
            returnVal = self.query('AS').rstrip()
        else:
            if counter in list(sourceDict):
                self.write('AS ' + '%G' %sourceDict[counter])
                returnVal = 0
            else:
                self.write('AS ' + '%G' %0)
                returnVal = -1
        return returnVal



        
#------------------------------OLD CODE-----------------------------------------
#     def simulate_button(self, botton = 'STOP'):
#         keydict = {'DOWN': 0, 'RIGHT': 1, 'LEVEL': 2, 'SETUP': 3, 
#                    'COM': 4, 'STOP': 5, 'LOCAL': 6, 'RESET': 7,'LEFT': 8, 
#                    'UP': 9, 'MODE': 10, 'AGATE': 11,'BGATE': 12, 'START': 13}
#         self.write('CK ' + str(keydict[botton]))
#         return 0

#     def read_cursor(self):
#         cursordict = {'0\r': 'LEFT', '1\r': 'RIGHT', '2\r': 'INACTIVE'}
#         return cursordict[self.query('SC')]
          
#     def check_ready(self):
#         return bool(int(self.query('SS 1')))
   
#     def read_last_count(self, channel = 'ch1'):
#         if self.check_ready():
#             if channel == 'ch1':
#                 count = int(self.query('QA').rstrip())
#             if channel == 'ch2':
#                 count = int(self.query('QB').rstrip())
#         else:
#             count = -1
#         return count

#     def read_count_now(self, channel = 'ch1'):
#         if channel == 'ch1':
#             count = int(self.query('XA').rstrip())
#         if channel == 'ch2':
#             count = int(self.query('XB').rstrip())
#         return count

#     def read_buffer_count(self, channel = 'ch1', point = 1):
#         # This is on the fly query of measured counts!!!
#         # Min point is 1 and Max point is 2000. Anything out
#         # of these limits produce error so -1!!!
#         if channel == 'ch1':
#             count = int(self.query('QA ' + str(point)).rstrip())
#         if channel == 'ch2':
#             count = int(self.query('QB ' + str(point)).rstrip())
#         return count
        
#     def read_secondary_status_byte(self, bit = 0):    
#         # All in manual p.48-49
#         # 0 : Checks if triggered
#         # 1 : Checks if inhibited
#         # 2 : Checks if counting
#         return bool(int(self.query('SI '+str(bit)).rstrip())) 

#     def count_restart(self):
#         self.write('CR') # (Manual p.45) Resets counters
#         self.write('CS') # (Manual p.44) Starts counters
#         return 0
    
#     def count_reset(self):
#         self.write('CR') # (Manual p.45) Resets counters
#         return 0
    
#     def count_stop(self):
#         self.write('CH') # (Manual p.45) Stops counters
#         return 0
    
#     def count_start(self):
#         self.write('CS') # (Manual p.45) Starts counters
#         return 0

#     def gate_delay(self, channel = 'A'):
#         # (Manual p.44) Reports gate delay position
#         delay = float(self.query('GZ ' + ('0' if channel == 'A' else '1'))).rstrip()
#         return delay

#     def gate_delay_set(self, channel = 'A', delay = 0.0):
#         # (Manual p.44) Select gate 'A' or 'B', defaults to 'A'
# 		# The selected gate delay is set to t seconds 
#         # where 0 <= t <= 999.2E-3, defaults to 0.0
#         if 0 <= delay <= 999.2E-3:
#             self.write('GD ' + ('0,' if channel == 'A' else '1,') + '%G' %delay)
#         else:
#             print('setting delay to 999.2E-3.')
#             tMax = 999.2E-3
#             self.write('GD ' + ('0,' if channel == 'A' else '1,') + '%G' %tMax)
#         return 0
    
#     def gate_mode(self, channel = 'A', mode = 'CW', read = False):
#         # (Manual p.43) Select gate 'A' or 'B', defaults to 'A'
#         # param channel: DESCRIPTION, defaults to 'A'
# 		# param mode: If it is changed to SCAN, the delay begins 
#         # scanning from the start position on the next count period. 
#         # If it is changed to FIXED, the delay returns to the start 
#         # position immediately, defaults to 'CW'
# 		# param query: True for asking, defaults to False for setting
#         gate_mode_dict = {'CW':0, 'FIXED':1, 'SCAN': 2}
#         if read:
#             returnVal = self.query('GM '+ ('0' if channel == 'A' else '1')).rstrip()
#         else:
#             if mode in list(gate_mode_dict):
#                 self.write('GM '+ ('0,' if channel == 'A' else '1,') + str(gate_mode_dict[mode]))
#                 returnVal = 0
#             else:
#                 print('Non-valid gate mode!')
#                 returnVal = -1
#         return returnVal
    
#     def gate_scan_step(self, channel = 'A', step:float = 0.0, read = False):
#         # (Manual p.43)
#         if read:
#             returnVal = self.query('GY '+ ('0' if channel == 'A' else '1')).rstrip()
#         else: 
#             if 0 <= step <= 999.2E-3:
#                 self.write('GY ' + ('0,' if channel == 'A' else '1,') + '%G' %step)
#                 returnVal = 0
#             else:
#                 print('stetting range  to  99.92E-3.')
#                 stepMax = 99.92E-3
#                 self.write('GY ' + ('0,' if channel == 'A' else '1,') + '%G' %stepMax)
#                 returnVal = 0
#         return returnVal

#     def gate_width(self, channel = 'A', window = 0.0, read = False):
#         # (Manual p.44)
#         if read:
#             returnVal = self.query('GW '+ ('0' if channel == 'A' else '1')).rstrip()
#         else:
#             if 0.005E-6 <= window <= 999.2E-3:
#                 self.write('GW ' + ('0,' if channel == 'A' else '1,') + '%G' %window)
#                 returnVal = 0
#             else:
#                 widthMax = 999.2E-3
#                 self.write('GW ' + ('0,' if channel == 'A' else '1,') + '%G' %window)
#                 returnVal = 0
#         return returnVal

#     def lcd_message(self, message = None):
#         if message is None:
#             self.write('MS')
#         else:
#             if len(message) <= 24: 
#                 self.write('MS '+ message)
#             else:
#                 self.write('MS '+ message[:24])
#         return 0

#     def display_mode(self, conti = True):
#         self.write('SD ' + ('0' if conti else '1'))
#         return 0

#     def scan_periods(self, num = 0):
#         if num == 0:
#             returnVal = self.query('NP').rstrip()
#         else:
#             if 1 <= num <= 2000:
#                 self.write('NP ' + str(num))
#                 returnVal = 0
#             else:
#                 maxNum = 2000
#                 self.write('NP ' + str(maxNum))
#                 returnVal = -1
#         return returnVal

#     def scan_position(self):
#         return self.query('NN').rstrip()
    
#     def scan_end_mode(self, mode = 'STOP', read = False):
#         if read:
#             status = bool(int(self.query('NE').rstrip()))
#             returnVal = 'STOP' if status else 'START'
#         else:
#             self.write('NE ' + ('0' if mode=='STOP' else '1'))
#             returnVal = 0
#         return returnVal

#     def reset_all(self):
#         self.write('CL')
#         return 0

#     def count_mode(self, mode = None):
#         # (Manual p.41)
#         if mode is None:
#             returnVal = self.query('CM').rstrip()
#         if mode == 'A,B': # Both A and B for T preset
#             self.write('CM 0')
#             returnVal = 0
#         if mode == 'A-B': # A-B for T preset
#             returnVal = 1
#             self.write('CM 1')
#         if mode == 'A+B': # A+B for T preset
#             returnVal = 2
#             self.write('CM 2')
#         if mode == 'A*B': # A for B preset
#             returnVal = 3
#             self.write('CM 3')
#         return returnVal

#     def dwell_time(self, dwell = None):
#         # (Manual p.42) Dwell time is in seconds!
#         if dwell is None:
#             returnVal = self.query('DT')
#         if dwell == 0:
#             self.write('DT 0')
#             returnVal = 'external'
#         if 2E-3 <= dwell <= 6E1:
#             self.write('DT %g' %dwell)
#             returnVal = str(dwell)
#         if 6E1 <= dwell <= 2E-3:
#             maxDwell = 6E1
#             self.write('DT %g' %maxDwell)
#             returnVal = str(maxDwell)
#         return returnVal
# # -------------------------TEST HERE ONWARDS---------------------      
#     def read_status_byte(self, bit = 0):
#         # All in manual p.48-49
#         # 0 : Checks if parameter change
#         # 1 : Checks if count finished
#         # 2 : Checks if scan finished
#         # 3 : Checks if overrun
#         # 4 : Checks if gate error
#         # 5 : Checks if recall error
#         # 6 : Checks if SQR
#         # 7 : Checks if command error
#         return bool(int(self.query('SS '+str(bit)).rstrip())) 

#     def set_discriminator_mode(self, channel = None, fixed = True):
#         # (Manual p.42) Dwell time is in seconds!
#         # Select A(0),B(1),T(2) channel, None for query
#         # True for FIXED, False for SCAN
#         if channel is None:
#             returnVal = [self.query('DM 0').rstrip(), self.query('DM 1').rstrip(), 
#                          self.query('DM 2').rstrip()]
#         else:
#             self.write('DM '+ str(channel) + (',0' if fixed else ',1'))
#             returnVal = 0
#         return returnVal

#     def set_gate_trigger(self, slope = None, level = None):
#         returnVal = 0
#         if slope is None:
#             self.query('TS').rstrip()
#         if slope == 'RISE':
#             self.write('TS 0')
#         if slope == 'FALL':
#             self.write('TS 1')
#         if not (slope == 'FALL' or slope == 'RISE'):
#             self.write('TS 0')
#             returnVal = -1

#         if level is None:
#             self.query('TL').rstrip()
#         if -2.0 <= level <= 2.0:
#             self.write('TL '+ '%G' %level)
#         if 2.0 <= level <= -2.0:
#             midLevel = 0.0
#             self.write('TL '+ '%G' %midLevel)
#             returnVal = -1
        
#         return returnVal
            
#     def set_discriminator_trigger(self, channel = None, slope = None, level = None):
#         returnVal = 0
#         if slope is None:
#             self.query('TS').rstrip()
#         if slope == 'RISE':
#             self.write('TS 0')
#         if slope == 'FALL':
#             self.write('TS 1')
#         if not (slope == 'FALL' or slope == 'RISE'):
#             self.write('TS 0')
#             returnVal = -1

#         if level is None:
#             self.query('TL').rstrip()
#         if -2.0 <= level <= 2.0:
#             self.write('TL '+ '%G' %level)
#         if 2.0 <= level <= -2.0:
#             midLevel = 0.0
#             self.write('TL '+ '%G' %midLevel)
#             returnVal = -1
        
#         return returnVal
    
    
    
    
# #     def set_discriminator_level(self, channel = 'ch1', level = 0.0, slope = True):
# # # 		THIS IS STRAIGHT WRONG, SEE p.42 and p.43
# #         """
# # 		:param channel: target channel, allowed string 'ch1', 'ch2', 'trigger'
# # 		:param level: gate trigger level, level in [-2.000, 2.000] Resolution is .001 V.
# # 		:param slope: gate trigger slope. True for RISE or positive, False for FALL or negative
# # 		"""
# # 		if channel == 'trigger':
# # 			self.write('TS ' + ('0' if slope else '1'))
# # 			self.write('TL ' + str(level))
# # 		else:
# # 			self.write('DS ' + ('0' if channel=='ch1' else '1') \
# # 						+ (',0' if slope else ',1'))
# # 			self.write('DL ' + ('0' if channel=='ch1' else '1') \
# # 						+ str(level))







































