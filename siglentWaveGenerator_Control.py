# -*- coding: utf-8 -*-
"""
Created on Fri Dec  5 08:33:16 2025

@author: pekermilas
"""
# Example Call for this library
# ---------------------------------------------
# import siglentWaveGenerator_Control as sgd
# dev = sgd.sdg6022X()
# dev.open()
# dev.setBasicWaveParams(shape="SQUARE",freq=100, ampl=1, offst=0, duty=50, phse=0)
# dev.setOutputState(output="ON")
# dev.setOutputState(output="OFF")
# dev.close()

import pyvisa as visa
import os
import numbers
import time
import binascii
import os

os.chdir("C:/Users/pekermilas/Documents/GitHub/InstrumentControlLibraries/")

class sdg6022X:

    def __init__(self, port = None):
        # self.port = port or "COM3"
        self.port = port or 'USB0::0xF4EC::0x1101::SDG6XBAX2R0314::INSTR'
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

# ----------------------- SECTION SIGNAL ------------------------------- #    
    def setOutputState(self, port="C1", output="OFF", 
                     load="HiZ", polarity="NOR"):
        if not self.dev is None:
            inputString = port + ":OUTP " + output + ",LOAD," + load + ",PLRT," + polarity
            self.write(inputString)
            returnVal = 1
        else:
            returnVal = -1
        return returnVal

    def getOutputState(self, port="C1"):
        if not self.dev is None:
            returnVal = self.query(port+":OUTP?")
        else:
            returnVal = -1
        return returnVal
    
    def setBasicWaveParams(self, port="C1", shape="SQUARE", freq=None, 
                           period=None, ampl=None, offst=None, symm=None, 
                           duty=None, phse=None, stdev=None, mean=None, 
                           width=None, rise=None, fall=None, dly=None, 
                           hlev=None, llev=None, bandstate="OFF", 
                           bandwidth=None, length=None, edge=None, 
                           diffstate=None, bitrate=None):
        missingPar = 0
        if not self.dev is None:
            if (shape=="SINE" or shape=="SQUARE" or shape=="RAMP" or 
                shape=="PULSE" or shape=="ARB" or shape=="PRBS"):
                inputString = port + ":BSWV WVTP," + str(shape)
                if not freq is None:
                    inputString = inputString + ",FRQ," + str(freq) # In Hz
                    period = None
                if not period is None:
                    inputString = inputString + ",PERI," + str(period) # In s
                    freq = None
                
                if not (ampl is None and offst is None):
                    inputString = inputString + ",AMP," + str(ampl) # In V, peak-to-peak
                    inputString = inputString + ",OFST," + str(offst) # In V, peak-to-peak
                    hlev = None
                    llev = None
                if (not ampl is None and offst is None) or (not offst is None and ampl is None):
                    print("Missing Amplitude or Offset!")
                    missingPar+=1
                if ampl is None and offst is None:
                    if not (hlev is None and llev is None):
                        inputString = inputString + ",HLEV," + str(hlev) # In V
                        inputString = inputString + ",LLEV," + str(llev) # In V
                        ampl = None
                        offst = None
                    if (not hlev is None and llev is None) or (not llev is None and hlev is None):
                        print("Missing HLEV or LLEV!")
                        missingPar+=1
                    if hlev is None and llev is None:
                        print("Missing wave parameters")
                        missingPar+=1

            if shape=="RAMP":
                if not symm is None:
                    inputString = inputString + ",SYM," + str(symm) # In percentage
                else:
                    print("Missing Parameter: symmetry in percentage")
                    missingPar+=1
            
            if shape=="SQUARE" or shape=="PULSE":
                if not duty is None:
                    inputString = inputString + ",DUTY," + str(duty) # In degrees
                else:
                    print("Missing Parameter: duty in percentage")
                    missingPar+=1
                    
            if (shape=="SINE" or shape=="SQUARE" or shape=="RAMP" or 
                shape=="ARB" or shape=="PRBS"):
                if not phse is None:
                    inputString = inputString + ",PHSE," + str(phse) # In degrees
                else:
                    print("Missing Parameter: phase in degrees")
                    missingPar+=1
            
            if shape=="PULSE":
                if not duty is None:
                    inputString = inputString + ",DUTY," + str(duty) # In percentage
                else:
                    print("Missing Parameter: duty in percentage")
                    missingPar+=1
                if not width is None:
                    inputString = inputString + ",WIDTH," + str(width) # In s
                else:
                    print("Missing Parameter: width in seconds")
                    missingPar+=1
                if not rise is None:
                    inputString = inputString + ",RISE," + str(rise) # In s
                else:
                    print("Missing Parameter: rise in seconds")
                    missingPar+=1
                if not fall is None:
                    inputString = inputString + ",FALL," + str(fall) # In s
                else:
                    print("Missing Parameter: fall in seconds")
                    missingPar+=1
                if not dly is None:
                    inputString = inputString + ",DLY," + str(dly) # In s
                else:
                    print("Missing Parameter: delay in seconds")
                    missingPar+=1
            
            if shape=="NOISE":
                if not stdev is None:
                    inputString = inputString + ",STDEV," + str(stdev) # In V
                else:
                    print("Missing Parameter: stdev in volts")
                    missingPar+=1
                if not mean is None:
                    inputString = inputString + ",MEAN," + str(mean) # In V
                else:
                    print("Missing Parameter: mean in volts")
                    missingPar+=1
                if not bandstate is None:
                    inputString = inputString + ",BANDSTATE," + str(bandstate) # ON or OFF
                else:
                    print("Missing Parameter: bandstate in ON/OFF")
                    missingPar+=1
                if not bandwidth is None:
                    inputString = inputString + ",BANDWIDTH," + str(bandwidth) # In Hz
                else:
                    print("Missing Parameter: bandwidth in hertz")
                    missingPar+=1

            if shape=="DC":
                if not offst is None:
                    inputString = inputString + ",OFST," + str(offst) # In V
                else:
                    print("Missing Parameter: offset in volts")
                    missingPar+=1
            
            if shape=="PRBS":
                if not length is None:
                    inputString = inputString + ",LENGTH," + str(length) # In 3 to 32
                else:
                    print("Missing Parameter: length in 3 to 32")
                    missingPar+=1
                if not edge is None:
                    inputString = inputString + ",EDGE," + str(edge) # In s
                else:
                    print("Missing Parameter: edge in seconds")
                    missingPar+=1
                if not diffstate is None:
                    inputString = inputString + ",LENGTH," + str(diffstate) # In on/off
                else:
                    print("Missing Parameter: length in ON/OFF")
                    missingPar+=1
                if not bitrate is None:
                    inputString = inputString + ",BITRATE," + str(bitrate) # In bps
                else:
                    print("Missing Parameter: length in bitsPerSecond")
                    missingPar+=1
            if not (shape=="SINE" or shape=="SQUARE" or shape=="RAMP" or 
                shape=="PULSE" or shape=="NOISE" or shape=="ARB" or 
                shape=="DC" or shape=="PRBS"):
                print("Unknown waveform.")
                missingPar+=1
                print(shape)
        else:
            missingPar+=1
        
        if missingPar>0:
            returnVal = -1
        else:
            returnVal = 1
            self.write(inputString)
        
        return returnVal
    
    def getBasicWaveParams(self, port="C1"):
        if not self.dev is None:
            returnVal = self.query(port+":BSWV?")
        else:
            returnVal = -1
        return returnVal
    
    def setWaveModulationParams(self, port="C1", modType=None, modState=None,
                                modSrcType=None, modWvShape=None, modFreq=None,
                                modDepth=None, modDev=None, modKeyFreq=None,
                                modHopFreq=None, modPhse=None, modAmpl=None,
                                modOfst=None, modSymm=None, modDuty=None):
        if not self.dev is None:
            returnVal = 0
        else:
            returnVal = 1
        return returnVal
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    