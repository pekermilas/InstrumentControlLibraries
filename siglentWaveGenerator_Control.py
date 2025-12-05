# -*- coding: utf-8 -*-
"""
Created on Fri Dec  5 08:33:16 2025

@author: pekermilas
"""

import pyvisa as visa
import os
import numbers
import time
import binascii
import os

os.chdir("C:/Users/pekermilas/Desktop/BirolAbeyLabWorks/SiglentWaveGeneratorControl//")

class sdg6022X:

    def __init__(self, port = None):
        # self.port = port or "COM3"
        self.port = port or 'USB0::0xF4EC::0x1101::SDG6XBAX2R0314::INSTR'
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
                self.dev.write_termination = '\n'
                self.dev.baud_rate = 19200 # Min : 300, Max : 19200
            
                self.dev.write("*RST")
                # self.dev.query("*IDN?")
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
    
# ----------------------- SECTION DEVICE SETTINGS ------------------------------- #    
    def resetDevice(self):
        if not self.dev is None:
            returnVal = self.write('*RST')
        else:
            returnVal = -1
        return returnVal

    def operationComplete(self):
        if not self.dev is None:
            returnVal = self.query("*OPC?")
        else:
            returnVal = -1
        return returnVal

    def setPortState(self, port="C1", output="OFF", 
                     load="HiZ", polarity="NOR"):
        if not self.dev is None:
            inputString = port + ":OUTP " + output + ",LOAD," + load + 
            ",PLRT," + polarity
            self.write(inputString)
            returnVal = 1
        else:
            returnVal = -1
        return returnVal

    def getPortState(self, port="C1"):
        if not self.dev is None:
            returnVal = self.query(port+":OUTP?")
        else:
            returnVal = -1
        return returnVal
    