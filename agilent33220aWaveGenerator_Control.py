# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 15:02:32 2026

@author: pekermilas
"""

# Example Call for this library
# ---------------------------------------------
# import siglentWaveGenerator_Control as sgd
# dev = sgd.sdg6022X()
# dev.open()
# dev.setBasicWaveParams(shape="SQUARE",freq=100, ampl=1, offst=0, duty=50, phse=0)
# dev.getBasicWaveParams()
# dev.setWaveModulationParams(modSrcType="INT",modSrcShape="SQUARE",modSrcFreq=100,modDepth=50, modState="ON")
# dev.setWaveModulationParams(modType="AM",modSrcType="INT",modSrcShape="SQUARE",modSrcFreq=100,modDepth=50, modState="ON")
# dev.getWaveModulationParams()
# dev.setOutputState(output="ON")
# dev.setOutputState(output="OFF")
# dev.close()

import pyvisa as visa
import os
import numbers
import time
import binascii
import os

# os.chdir("C:/Users/pekermilas/Documents/GitHub/InstrumentControlLibraries/")

class agi33220A:

    def __init__(self, port = None):
        # self.port = port or "COM3"
        self.port = port or 'USB0::2391::1031::MY44036454::INSTR'
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

# ----------------------- SECTION SYSTEM ------------------------------- # 
    def systemID(self):
        if not self.dev is None:
            returnVal = self.query('*IDN')
        else:
            returnVal = -1
        return returnVal

    def operationComplete(self):
        if not self.dev is None:
            returnVal = self.query("*OPC?")
        else:
            returnVal = -1
        return returnVal

    def resetDevice(self):
        if not self.dev is None:
            returnVal = self.write('*RST')
        else:
            returnVal = -1
        return returnVal

# ----------------------- SECTION APPLY ------------------------------- # 
    def setBasicWaveParams(self, shape="SQUARE", freq=None, 
                           period=None, ampl=None, offst=None):
        waveShapes = ['SINE', 'SQUARE', 'RAMP', 'PULSE', 'NOISE', 
                      'DC', 'ARBS']
        if not self.dev is None:
            if shape in waveShapes:
                
        else:
            returnVal = -1
        return returnVal















