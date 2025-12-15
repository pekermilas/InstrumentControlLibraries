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
        inputString = port + ":BSWV WVTP,"
        if not self.dev is None:
            if (shape=="SINE" or shape=="SQUARE" or shape=="RAMP" or 
                shape=="PULSE" or shape=="ARB" or shape=="PRBS"):
                inputString = inputString + str(shape)
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
    
    def setWaveModulationParams(self, port="C1", modType="AM", modState=None,
                                modSrcType=None, modSrcShape=None, modSrcFreq=None,
                                modDepth=None, modDev=None, modKeyFreq=None,
                                modHopFreq=None, modCarrShape=None, modCarrFreq=None,
                                modCarrPhse=None, modCarrAmpl=None, modCarrOfst=None, 
                                modCarrSymm=None, modCarrDuty=None, modCarrRise=None,
                                modCarrFall=None, modCarrDelay=None):
        missingPar = 0
        inputString = port + ":MDWV "
        if not self.dev is None:
            if (modType=="AM" or modType=="DSBAM" or modType=="FM" or 
                modType=="PM" or modType=="PWM" or modType=="ASK" or
                modType=="FSK" or modType=="PSK" or modType=="CARR"):
                
                inputString = inputString + str(modType)
                
                if not modState is None:
                    inputString = inputString + ",STATE," + str(modState)
                else:
                    print("Missing Parameter: mod state in ON/OFF")
                    missingPar+=1

            if (modType=="AM" or modType=="DSBAM" or modType=="FM" or 
                modType=="PM" or modType=="PWM" or modType=="ASK" or
                modType=="FSK" or modType=="PSK"):
                if not modSrcType is None:
                    inputString = inputString + ",SRC," + str(modSrcType)
                else:
                    print("Missing Parameter: mod source type in INT/EXT")
                    missingPar+=1
                
            if (modType=="AM" or modType=="DSBAM" or modType=="FM" or 
                modType=="PM" or modType=="PWM"):
                if modSrcType=="INT":
                    if not modSrcShape is None:
                        if (modSrcShape=="SINE" or modSrcShape=="SQUARE" or
                            modSrcShape=="TRIANGLE" or modSrcShape=="UPRAMP" or
                            modSrcShape=="DNRAMP" or modSrcShape=="NOISE" or 
                            modSrcShape=="ARB"):
                            inputString = inputString + ",MDSP," + str(modSrcShape)
                        else:
                            print("Unknown source shape")
                            missingPar+=1
                    else:
                        print("Missing Parameter: mod source shape (SINE, SQUARE, etc.)")
                        missingPar+=1
                else:
                    print("Mode source type is not INT")

            if (modType=="AM" or modType=="DSBAM" or modType=="FM" or 
                modType=="PM" or modType=="PWM", modType=="CARR"):
                if modSrcType=="INT":
                    if not modSrcFreq is None:
                        inputString = inputString + ",FRQ," + str(modSrcFreq)
                    else:
                        print("Missing Parameter: mod source frequency in Hz")
                        missingPar+=1
                else:
                    print("Mode source type is not INT")

            if (modType=="AM"):
                if modSrcType=="INT":
                    if not modDepth is None:
                        inputString = inputString + ",DEPTH," + str(modDepth)
                    else:
                        print("Missing Parameter: mod depth in percentage")
                        missingPar+=1
                else:
                    print("Mode source type is not INT")

            if (modType=="FM" or modType=="PM" or modType=="PWM"):
                if modSrcType=="INT":
                    if not modDev is None:
                        inputString = inputString + ",DEVI," + str(modDev)
                    else:
                        print("Missing Parameter: mod deviation in Hz")
                        missingPar+=1
                else:
                    print("Mode source type is not INT")

            if (modType=="ASK" or modType=="FSK" or modType=="PSK"):
                if modSrcType=="INT":
                    if not modKeyFreq is None:
                        inputString = inputString + ",KFRQ," + str(modKeyFreq)
                    else:
                        print("Missing Parameter: mod key frequency in Hz")
                        missingPar+=1
                else:
                    print("Mode source type is not INT")
                    missingPar+=1

            if (modType=="FSK"):
                if modSrcType=="INT":
                    if not modHopFreq is None:
                        inputString = inputString + ",HFRQ," + str(modHopFreq)
                    else:
                        print("Missing Parameter: mod hop frequency in Hz")
                        missingPar+=1
                else:
                    print("Mode source type is not INT")

            if (modType=="CARR"):
                if not modCarrShape is None:
                    if (modCarrShape=="SINE" or modCarrShape=="SQUARE" or 
                        modCarrShape=="RAMP" or modCarrShape=="ARB"  or 
                        modCarrShape=="PULSE"):
                        inputString = inputString + ",WVTP," + str(modCarrShape)
                    else:
                        print("Unknown carrier modulation wave shape")
                        missingPar+=1
                else:
                    print("Missing Parameter: carrier mod wave shape")
                    missingPar+=1

            if (modType=="CARR"):
                if not modCarrFreq is None:
                    inputString = inputString + ",FRQ," + str(modCarrFreq)
                else:
                    print("Missing Parameter: carrier mod wave freq in Hz")
                    missingPar+=1

            if (modType=="CARR"):
                if not modCarrPhse is None:
                    inputString = inputString + ",PHSE," + str(modCarrPhse)
                else:
                    print("Missing Parameter: carrier mod wave phase in degrees")
                    missingPar+=1

            if (modType=="CARR"):
                if not modCarrAmpl is None:
                    inputString = inputString + ",AMP," + str(modCarrAmpl)
                else:
                    print("Missing Parameter: carrier mod wave amplitude in V")
                    missingPar+=1
            
            if (modType=="CARR"):
                if not modCarrOfst is None:
                    inputString = inputString + ",OFST," + str(modCarrOfst)
                else:
                    print("Missing Parameter: carrier mod wave offset in V")
                    missingPar+=1

            if (modType=="CARR"):
                if modCarrShape=="RAMP":
                    if not modCarrSymm is None:
                        inputString = inputString + ",SYM," + str(modCarrSymm)
                    else:
                        print("Missing Parameter: carrier mod wave symmetry in percentage")
                        missingPar+=1
                else:
                    print("Mode carrier shape is not RAMP")

            if (modType=="CARR"):
                if (modCarrShape=="SQUARE" or modCarrShape=="PULSE"):
                    if not modCarrDuty is None:
                        inputString = inputString + ",DUTY," + str(modCarrDuty)
                    else:
                        print("Missing Parameter: carrier mod wave duty cycle in percentage")
                        missingPar+=1
                else:
                    print("Mode carrier shape is not SQUARE or PULSE")

            if (modType=="CARR"):
                if modCarrShape=="PULSE":
                    if not modCarrRise is None:
                        inputString = inputString + ",RISE," + str(modCarrRise)
                    else:
                        print("Missing Parameter: carrier mod wave rise time in seconds")
                        missingPar+=1
                    if not modCarrFall is None:
                        inputString = inputString + ",FALL," + str(modCarrFall)
                    else:
                        print("Missing Parameter: carrier mod wave fall time in seconds")
                        missingPar+=1
                    if not modCarrDelay is None:
                        inputString = inputString + ",DLY," + str(modCarrDelay)
                    else:
                        print("Missing Parameter: carrier mod wave delay time in seconds")
                        missingPar+=1
                else:
                    print("Mode carrier shape is not PULSE")
        else:
            missingPar+=1
        
        if missingPar>0:
            returnVal = -1
        else:
            returnVal = 1
            self.write(inputString)
        
        return returnVal

    def getWaveModulationParams(self, port="C1"):
        if not self.dev is None:
            returnVal = self.query(port+":MDWV?")
        else:
            returnVal = -1
        return returnVal
    
    def setSweepWaveParams(self, port="C1", swpdState=None, swpTime=None, 
                           swpStartFrq=None, swpStopFrq=None, swpMode=None,
                           swpDir=None, swpTrigSrc=None, swpManTrig=None,
                           swpTrigOut=None, swpTrigEdge=None, swpCarrWvTyp=None,
                           swpCarrFrq=None, swpCarrPhse=None, swpCarrAmpl=None,
                           swpCarrOfst=None, swpCarrSymm=None, swpCarrDuty=None):
        missingPar = 0
        inputString = port + ":SWWV "
        if not self.dev is None:
            if not swpState is None:
                inputString = inputString + ",STATE," + str(swpState)
            else:
                print("Missing Parameter: sweep state in ON/OFF")
                missingPar+=1
            if not swpTime is None:
                inputString = inputString + ",TIME," + str(swpTime)
            else:
                print("Missing Parameter: sweep time in seconds")
                missingPar+=1
            if not swpStartFrq is None:
                inputString = inputString + ",START," + str(swpStartFrq)
            else:
                print("Missing Parameter: sweep start frequency in Hz")
                missingPar+=1
            if not swpStopFrq is None:
                inputString = inputString + ",STOP," + str(swpStopFrq)
            else:
                print("Missing Parameter: sweep stop frequency in Hz")
                missingPar+=1
            if not swpMode is None:
                inputString = inputString + ",SWMD," + str(swpMode)
            else:
                print("Missing Parameter: sweep mode in LINE or LOG")
                missingPar+=1
            if not swpDir is None:
                inputString = inputString + ",DIR," + str(swpDir)
            else:
                print("Missing Parameter: sweep direction in UP or DOWN")
                missingPar+=1
            if not swpTrigSrc is None:
                inputString = inputString + ",TRSR," + str(swpTrigSrc)
            else:
                print("Missing Parameter: trigger source in EXT or INT or MAN")
                missingPar+=1

            # if (swpTrigSrc=="MAN"):
            #     if not swpManTrig is None:
            #         inputString = inputString + ",MTRIG," + str(swpManTrig)
            # else:
            #     print("Missing Parameter: trigger ???")
            #     missingPar+=1

            if (swpTrigSrc=="EXT" or swpTrigSrc=="MAN"):
                if not swpTrigEdge is None:
                    inputString = inputString + ",EDGE," + str(swpTrigEdge)
                else:
                    print("Missing Parameter: trigger edge in RISE or FALL")
                    missingPar+=1                

            if not swpCarrWvTyp is None:
                if (swpCarrWvTyp=="SINE" or swpCarrWvTyp=="SQUARE" or
                    swpCarrWvTyp=="RAMP" or swpCarrWvTyp=="ARB"):
                        inputString = inputString + ",CARRY,WVTP," + str(swpCarrWvTyp)
                else:
                    print("Unknown sweeper carrier wave type")
                    missingPar+=1
                if not swpCarrFrq is None:
                    inputString = inputString + ",FRQ," + str(swpCarrFrq)
                else:
                    print("Missing Parameter: sweeper carrier wave frequency in Hz")
                    missingPar+=1
                if not swpCarrPhse is None:
                    inputString = inputString + ",PHSE," + str(swpCarrPhse)
                else:
                    print("Missing Parameter: sweeper carrier wave phase in degrees")
                    missingPar+=1
                if not swpCarrAmpl is None:
                    inputString = inputString + ",AMP," + str(swpCarrAmpl)
                else:
                    print("Missing Parameter: sweeper carrier wave amplitude in V")
                    missingPar+=1
                if not swpCarrOfst is None:
                    inputString = inputString + ",OFST," + str(swpCarrOfst)
                else:
                    print("Missing Parameter: sweeper carrier wave offset in V")
                    missingPar+=1
                if swpCarrWvTyp=="RAMP":
                    if not swpCarrSymm is None:
                        inputString = inputString + ",SYM," + str(swpCarrSymm)
                    else:
                        print("Missing Parameter: sweeper carrier wave symmetry in percentage")
                        missingPar+=1
                if swpCarrWvTyp=="SQUARE":
                    if not swpCarrDuty is None:
                        inputString = inputString + ",DUTY," + str(swpCarrDuty)
                    else:
                        print("Missing Parameter: sweeper carrier wave duty cycle in percentage")
                        missingPar+=1
            else:
                print("Missing Parameter: sweeper carrier wave type")
                missingPar+=1
        else:
            missingPar+=1
        
        if missingPar>0:
            returnVal = -1
        else:
            returnVal = 1
            self.write(inputString)
        
        return returnVal
    
    def getSweepWaveParams(self, port="C1"):
        if not self.dev is None:
            returnVal = self.query(port+":SWWV?")
        else:
            returnVal = -1
        return returnVal

    def setBurstWaveParams(self, port="C1", brstdState=None, brstPrd=None, 
                           brstStartPhs=None, brstGate=None, brstTrigSrc=None,
                           brstManTrig=None, brstTrigDly=None, brstTrigPlrty=None,
                           brstTrigOutMod=None, brstTrigEdge=None, brstTrigCycTime=None,
                           brstCarrWvTyp=None, brstCarrFrq=None, brstCarrPhse=None, 
                           brstCarrAmpl=None, brstCarrOfst=None, brstCarrSymm=None, 
                           brstCarrDuty=None, brstCarrRise=None, brstCarrFall=None,
                           brstCarrDly=None, brstCarrStd=None, brstCarrMean=None):
        missingPar = 0
        inputString = port + ":BTWV "
        if not self.dev is None:
            if not brstdState is None:
                inputString = inputString + ",STATE," + str(brstdState)
            else:
                print("Missing Parameter: burst state in ON/OFF")
                missingPar+=1
            if not brstPrd is None:
                inputString = inputString + ",PRD," + str(brstPrd)
            else:
                print("Missing Parameter: burst period in seconds")
                missingPar+=1
            if not brstStartPhs is None:
                inputString = inputString + ",STPS," + str(brstStartPhs)
            else:
                print("Missing Parameter: burst start phase in degrees")
                missingPar+=1
            if not brstGate is None:
                inputString = inputString + ",GATE_NCYC," + str(brstGate)
            else:
                print("Missing Parameter: burst mode in GATE or NCYC")
                missingPar+=1
            if not brstTrigSrc is None:
                inputString = inputString + ",TRSR," + str(brstTrigSrc)
            else:
                print("Missing Parameter: burst trigger source in EXT or INT or MAN")
                missingPar+=1
            if not brstTrigDly is None:
                inputString = inputString + ",DLAY," + str(brstTrigDly)
            else:
                print("Missing Parameter: burst delay in seconds")
                missingPar+=1
            if not brstTrigPlrty is None:
                inputString = inputString + ",PLRT," + str(brstTrigPlrty)
            else:
                print("Missing Parameter: burst gate polarity in NEG or POS")
                missingPar+=1
            if not brstTrigOutMod is None:
                inputString = inputString + ",TRMD," + str(brstTrigOutMod)
            else:
                print("Missing Parameter: burst trigger out mode in RISE or FALL or OFF")
                missingPar+=1
            if not brstTrigEdge is None:
                inputString = inputString + ",EDGE," + str(brstTrigEdge)
            else:
                print("Missing Parameter: burst trigger edge in RISE or FALL")
                missingPar+=1
            if not brstTrigCycTime is None:
                inputString = inputString + ",TIME," + str(brstTrigCycTime)
            else:
                print("Missing Parameter: burst trigger edge in cycle number/integer")
                missingPar+=1
            if not brstCarrWvTyp is None:
                if (brstCarrWvTyp=="SINE" or brstCarrWvTyp=="SQUARE" or 
                    brstCarrWvTyp=="RAMP" or brstCarrWvTyp=="ARB" or 
                    brstCarrWvTyp=="PULSE" or brstCarrWvTyp=="NOISE"):
                    inputString = inputString + ",CARRY,WVTP" + str(brstCarrWvTyp)
                else:
                    print("Unknown sweeper carrier wave type")
                    missingPar+=1
                if not brstCarrFrq is None:
                    inputString = inputString + ",FRQ," + str(brstCarrFrq)
                else:
                    print("Missing Parameter: burst carrier frequency in Hz")
                    missingPar+=1
                if not brstCarrPhse is None:
                    inputString = inputString + ",PHSE," + str(brstCarrPhse)
                else:
                    print("Missing Parameter: burst carrier phase in degrees")
                    missingPar+=1
                if not brstCarrAmpl is None:
                    inputString = inputString + ",AMP," + str(brstCarrAmpl)
                else:
                    print("Missing Parameter: burst carrier amplitude in V")
                    missingPar+=1
                if not brstCarrOfst is None:
                    inputString = inputString + ",OFST," + str(brstCarrOfst)
                else:
                    print("Missing Parameter: burst carrier offset in V")
                    missingPar+=1
                if brstCarrWvTyp=="RAMP":
                    if not brstCarrSymm is None:
                        inputString = inputString + ",SYM," + str(brstCarrSymm)
                    else:
                        print("Missing Parameter: burst carrier symmetry in V")
                        missingPar+=1
                if brstCarrWvTyp=="PULSE":
                    if not brstCarrRise is None:
                        inputString = inputString + ",RISE," + str(brstCarrRise)
                    else:
                        print("Missing Parameter: burst carrier rise time in seconds")
                        missingPar+=1
                    if not brstCarrFall is None:
                        inputString = inputString + ",FALL," + str(brstCarrFall)
                    else:
                        print("Missing Parameter: burst carrier fall time in seconds")
                        missingPar+=1
                    if not brstCarrDly is None:
                        inputString = inputString + ",DLY," + str(brstCarrDly)
                    else:
                        print("Missing Parameter: burst carrier delay time in seconds")
                        missingPar+=1
                if brstCarrWvTyp=="NOISE":
                    if not brstCarrStd is None:
                        inputString = inputString + ",STDEV," + str(brstCarrStd)
                    else:
                        print("Missing Parameter: burst carrier stdev in V")
                        missingPar+=1
                    if not brstCarrMean is None:
                        inputString = inputString + ",MEAN," + str(brstCarrMean)
                    else:
                        print("Missing Parameter: burst carrier mean in V")
                        missingPar+=1
            else:
                print("Missing Parameter: burst carrier wave type")
                missingPar+=1
        else:
            missingPar+=1
        
        if missingPar>0:
            returnVal = -1
        else:
            returnVal = 1
            self.write(inputString)
        return 0

    def getBurstWaveParams(self, port="C1"):
        if not self.dev is None:
            returnVal = self.query(port+":BTWV?")
        else:
            returnVal = -1
        return returnVal

















