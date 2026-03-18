# -*- coding: utf-8 -*-
"""
Created on Thu Jan  1 17:19:26 2026

@author: peker
"""
# EXAMPLE CALLS
# t = sr400.sr400()
# t.open()
# t.dev.query('SS 1')

# EXAMPLE CALLS
# import hpRfGenerator_Control as hprf
# t = hprf.hp83752B()
# t.open()
# t.goto_freq()
# t.close()

import pyvisa as visa
import os
import numbers
import time
import binascii
import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import minimize_scalar
from scipy.optimize import fsolve
from scipy import interpolate

class rfUtilityClass:
    def set_frequencies(self, fStart=2870, fStop=2870, numFreqs=1):
        freqs = np.linspace(fStart,fStop,numFreqs)
        return freqs

class hp8648C(rfUtilityClass):
    def __init__(self, port = None):
        self.port = port or 'GPIB0::7::INSTR'
        self.dev = None
        self.visaLib = 'ni-visa' # or 'py-visa'
        self.rm = None
# ----------------------- SECTION CORE ------------------------------- #
    def open(self):
        if self.dev is None:
            if self.visaLib == 'py-visa':
                self.rm = visa.ResourceManager('@py')
            if self.visaLib == 'ni-visa':
                self.rm = visa.ResourceManager()
                
            try:
                self.dev = self.rm.open_resource(self.port)
                self.dev.read_termination = '\n'
            
                self.dev.write("*RST")
                self.dev.query("*OPC?")
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

# ---------------------- SECTION RUNTIME ------------------------------ #
    def goto_freq(self, freq=500, power=-30):
        if not self.dev is None:
            strFreq = "FREQ:CW " + str(freq) + " MHZ"
            self.write(strFreq) # Set frequency to 500MHz
            strTurnOn = "POW:AMPL " + str(power) + "DBM;:OUTP:STAT ON"
            self.write(strTurnOn) # Set power to -30dB and turn on the RF
            self.query("*OPC?")
            returnVal=0
        else:
            returnVal=-1
        return returnVal
    
    def rf_off(self):
        if not self.dev is None:
            self.write("OUTP:STAT OFF")
            self.query("*OPC?")
            returnVal=0
        else:
            returnVal=-1
        return returnVal

    def rf_disconn(self): 
        if not self.dev is None:
            self.close()
            returnVal=0
        else:
            returnVal=-1
        return returnVal


class hp8341B(rfUtilityClass):
    def __init__(self, port = None):
        self.port = port or 'GPIB0::19::INSTR'
        self.dev = None
        self.visaLib = 'ni-visa' # or 'py-visa'
        self.rm = None
# ----------------------- SECTION CORE ------------------------------- #
    def open(self):
        if self.dev is None:
            if self.visaLib == 'py-visa':
                self.rm = visa.ResourceManager('@py')
            if self.visaLib == 'ni-visa':
                self.rm = visa.ResourceManager()
                
            try:
                self.dev = self.rm.open_resource(self.port)
                self.dev.read_termination = '\n'
            
                self.dev.write("IP")
                time.sleep(2)
                self.dev.write("OS")
                # self.dev.read_all()
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

# ---------------------- SECTION RUNTIME ------------------------------ #
    def goto_freq(self, freq=500, power=-30):
        if not self.dev is None:
            strFreq = "CW " + str(freq) + "MZ"
            self.write(strFreq) # Set frequency to 500MHz
            strTurnOn = "PL" + str(power) + "DB" + "RF1"
            self.write(strTurnOn) # Set power to 0dB and turn on the RF
            self.write("OS")
            # self.read_raw()
            returnVal=0
        else:
            returnVal=-1
        return returnVal
    
    def rf_off(self):
        if not self.dev is None:
            self.write("RF0")
            self.write("OS")
            # self.read_all()
            returnVal=0
        else:
            returnVal=-1
        return returnVal

    def rf_disconn(self): 
        if not self.dev is None:
            self.close()
            returnVal=0
        else:
            returnVal=-1
        return returnVal


class hp83752B(rfUtilityClass):
    def __init__(self, port = None):
        self.port = port or 'GPIB0::21::INSTR'
        self.dev = None
        self.visaLib = 'ni-visa' # or 'py-visa'
        self.rm = None
# ----------------------- SECTION CORE ------------------------------- #
    def open(self):
        if self.dev is None:
            if self.visaLib == 'py-visa':
                self.rm = visa.ResourceManager('@py')
            if self.visaLib == 'ni-visa':
                self.rm = visa.ResourceManager()
                
            try:
                self.dev = self.rm.open_resource(self.port)
                self.dev.read_termination = '\n'
            
                self.dev.write("*RST")
                self.dev.query("*OPC?")
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

# ---------------------- SECTION RUNTIME ------------------------------ #
    def goto_freq(self, freq=500, power=-30):
        if not self.dev is None:
            strFreq = "FREQuency:CW "+str(freq)+"MHZ"
            self.write(strFreq) # Set frequency to 500MHz
            strPowerLvl = "POWer:LEVel " + str(power) + " DBM"
            self.write(strPowerLvl) # Set power to 0dB and turn on the RF
            strTurnOn = "OUTPut:STATe ON"
            self.write(strTurnOn)
            self.query("*OPC?")
            returnVal=0
        else:
            returnVal=-1
        return returnVal
    
    def rf_off(self):
        if not self.dev is None:
            self.write("OUTPut:STATe OFF")
            self.query("*OPC?")
            returnVal=0
        else:
            returnVal=-1
        return returnVal

    def rf_disconn(self): 
        if not self.dev is None:
            self.close()
            returnVal=0
        else:
            returnVal=-1
        return returnVal

