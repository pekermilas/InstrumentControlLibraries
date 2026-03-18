# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 08:53:22 2022

@author: Ozturk-Lab1
"""

import pyvisa as visa
import time
import numpy as np
import matplotlib.pyplot as plt

import cryoMicConfig as cmc

from scipy.optimize import minimize_scalar
from scipy.optimize import fsolve
import skrf as rf
from scipy import interpolate


def set_rf(port='GPIB0::7::INSTR'):
    rm = cmc.resman
    port = odmrc.portRfgen
    gpibIdx = int(port[7:-7])
    
    try:
        cmc.rfc = rm.open_resource(port)
                
        if gpibIdx==7:
            sweeper=0
        if gpibIdx==19:
            sweeper=1
        if gpibIdx==21:
            sweeper=2
            
        cmc.rfc.read_termination = '\n'
        cmc.sweeper = sweeper
    except:
        cmc.rfc = -1
        cmc.sweeper = -1
        
    return 0

def rf_linear_freq_grid(fstart,fstop,fnum):
    
    freqGrid = np.linspace(fstart,fstop,fnum)
    
    return freqGrid
    
def rf_geometric_freq_grid(fstart,fstop,fnum):

    fi = fstart
    ff = fstop
    fm = (fstart+fstop)/2
    n = float(fnum//2)
    D = 0.5
    def f(r):
        return  (D*(r**n-1)/(r-1) - (fm-fi))**2
    
    res = minimize_scalar(f, bounds=(0, 1), method='bounded')
    r = res.x
    
    diffs = np.zeros(n)
    for i in range(n):
        diffs[i] = D*r**i 
        
    freqsL = np.zeros(n+1)
    for i in range(n+1):
        freqsL[i] = np.round(fi+np.sum(diffs[:i]),3)
        
    steps = freqsL-fi
    freqsR = ff-steps[::-1]
    freqs = np.unique(np.vstack((freqsL,freqsR)).flatten())
    cmc.freqGrid = freqs

    return 0

def rf_power_modulation(fname='', varyPower=False, power=-30):
    if not varyPower:
        pows = np.ones(len(cmc.freqGrid))*power
        # odmrc.powerGrid = pows

    else:
        if not fname:
            pows = np.ones(200)*power
            # odmrc.powerGrid = pows
        else:
            temp = rf.Network(fname)['2500-3200mhz']
            X = cmc.freqGrid*1e6
            # print(X)
            # print(temp.f)
            yIntp = interpolate.interp1d(temp.f, temp.s_db[:,0,0], kind='cubic')
            Y = yIntp(X)
            
            powTransmit = 10.*np.log10(1.-10.**(yIntp(X)/10.))
            powInit = power - powTransmit
            # odmrc.powerGrid = powInit
            pows = powInit
    
    cmc.powerGrid = pows
    return pows

def goto_freq(freq=500, power=-30):
    
    rfc = cmc.rfc
    if cmc.sweeper==0:
        strFreq = "FREQ:CW "+str(freq)+" MHZ"
        rfc.write(strFreq) # Set frequency to 500MHz
        strTurnOn = "POW:AMPL "+str(power)+"DBM;:OUTP:STAT ON"
        rfc.write(strTurnOn) # Set power to 0dB and turn on the RF
        rfc.query("*OPC?")

    if cmc.sweeper==1:
        strFreq = "CW "+str(freq)+"MZ"
        rfc.write(strFreq) # Set frequency to 500MHz
        strTurnOn = "PL"+str(power)+"DB"+"RF1"
        rfc.write(strTurnOn) # Set power to 0dB and turn on the RF
        rfc.write("OS")
        rfc.read_raw()

    if cmc.sweeper==2:
        strFreq = "FREQuency:CW "+str(freq)+"MHZ"
        rfc.write(strFreq) # Set frequency to 500MHz
        strPowerLvl = "POWer:LEVel "+str(power)+" DBM"
        rfc.write(strPowerLvl) # Set power to 0dB and turn on the RF
        strTurnOn = "OUTPut:STATe ON"
        rfc.write(strTurnOn)
        rfc.write("*OPC?")
        rfc.read()
    
    if cmc.sweeper==-1:
        print('No sythesizer is present! Aborting!')
    
    return 0
    
def rf_off():
    
    rfc = cmc.rfc
    if cmc.sweeper==0:
        rfc.write("OUTP:STAT OFF")
        rfc.query("*OPC?")
        
    if cmc.sweeper==1:
        rfc.write("RF0")
        rfc.write("OS")
        rfc.read_raw()
        
    if cmc.sweeper==2:
        rfc.write("OUTPut:STATe OFF")
        rfc.write("*OPC?")
        rfc.read()
    
    if cmc.sweeper==-1:
        print('No sythesizer is present! Aborting!')
    
    return 0

def rf_disconn(): 
    rfc = cmc.rfc
    if not rfc==-1:
        rfc.close()
    
    return 0

if __name__ == '__main__':
    print("RF Lib is loaded.")
    set_rf()
    goto_freq()
    time.sleep(5)
    rf_off()
    rf_disconn()
