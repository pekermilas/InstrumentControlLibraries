# -*- coding: utf-8 -*-
"""
Created on Mon Jan  5 15:56:54 2026

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

class sdg6022X:

    def __init__(self, port = None):
        # self.port = port or "COM3"
        self.port = port or 'GPIB0::23::INSTR'
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
                self.dev.write_termination = '\n'
                self.dev.baud_rate = 9600 # Min : 300, Max : 19200
            
                self.dev.write("*RST")
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
    
# ----------------------- SECTION SETUP ------------------------------- #
    def setup_deviceIdentity(self):
        # (Manual p.59)
        if not self.dev is None:
            returnVal = self.query('*IDN?')
        else:
            returnVal = -1
        return returnVal

    def setup_recallSettings(self, settingPos = 0):
        # (Manual p.59)
        if not self.dev is None:
            self.write('*RCL ' + str(settingPos))
            returnVal = 0
        else:
            returnVal = -1
        return returnVal
    
    def setup_saveSettings(self, settingPos = 0):
        # (Manual p.59)
        if not self.dev is None:
            self.write('*SAV ' + str(settingPos))
            returnVal = 0
        else:
            returnVal = -1
        return returnVal
    
    def setup_reset(self, settingPos = 0):
        # (Manual p.59)
        if not self.dev is None:
            self.write('*RST')
            returnVal = 0
        else:
            returnVal = -1
        return returnVal

# ----------------------- SECTION OUTPUT ------------------------------- #
    def output_setOutputAmplitude(self, amplVal = 0, amplUnit = 'VP'):
        # (Manual p.59)
        if not self.dev is None:
            if amplUnit = 'VP' or amplUnit = 'VR' or amplUnit = 'DB':
                self.write('AMPL ' + str(amplVal) + amplUnit)
                returnVal = 0
            else:
                self.write('AMPL ' + str(amplVal) + 'VP')
                returnVal = 1
        else:
            returnVal = -1
        return returnVal
    
    def output_getOutputAmplitude(self):
        # (Manual p.59)
        if not self.dev is None:
            returnVal = self.query('AMPL?')
        else:
            returnVal = -1
        return returnVal




# ----------------------- SECTION STATUS REPORT------------------------------- #
    def statusReport_clearRegisters(self):
        # (Manual p.59)
        if not self.dev is None:
            self.write('*CLS')
            returnVal = 0
        else:
            returnVal = -1
        return returnVal

    def statusReport_setEventStatusByte(self, byteVal = 1):
        # (Manual p.59)
        if not self.dev is None:
            self.write('*ESE ' + str(byteVal))
            returnVal = 0
        else:
            returnVal = -1
        return returnVal

    def statusReport_getEventStatusByte(self):
        # (Manual p.59)
        if not self.dev is None:
            returnVal = self.query('*ESE?')
        else:
            returnVal = -1
        return returnVal









