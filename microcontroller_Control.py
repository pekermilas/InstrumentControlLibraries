# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 11:53:08 2026

@author: admin
"""
import pyvisa as visa
import os
import numbers
import time
import binascii
import os
import numpy as np
import matplotlib.pyplot as plt
import serial
import serial.tools.list_ports

class teensy:
    def __init__(self, port = None):
        self.port = port or 'COM12'
        self.dev = None
        self.rm = None
    
    def read(self):
        return self.dev.readline().decode('utf-8').strip()
    
    def write(self, writeStr = None):
        if not self.dev is None:
            self.dev.write(writeStr)
            returnVal = 0
        else:
            returnVal = -1
        return returnVal

    def close(self):
        if not self.dev is None:
            self.dev.close()
            self.dev = None
            returnVal = 0
        else:
            returnVal = -1
        return returnVal
    
    def connectArduino(self):
        try:
            self.dev = serial.Serial()
            self.dev.baudrate = 9600
            self.dev.port = self.port
            self.dev.dsrdtr=True
            self.dev.open()
            time.sleep(0.2)
            self.dev.timeout = None
        except IndexError:
            print('Could not find Microcontroller' )
        
        maxTimeDelay=2.0
    
        return 0
    
    def disconnArduino(self):
        if not self.dev is None:
            self.close()
        else:
            print("Nothing to do!")
            
        return 0
    
    def pulseTeensyForRabi(self, t1=1000, t2=1000, t3=1000, t4=1000, repeats=1000):
        if not self.dev is None:
            msgString = str(t1)+','+str(t2)+','+str(t3)+','+str(t4)+','+str(repeats)
            print(msgString)
            self.write(msgString.encode())
            
            # while(self.dev.inWaiting()==0):
            #     pass
            
            # line = []
            # while True:
            #     temp = self.read()
            #     line = np.append(line, temp)
            #     if temp=='DONE':
            #         break
     
        else:
             print("Nothing to do!")
             
        return 0
    
    def waitArduino(self):
        if not self.dev is None:
            while(self.dev.inWaiting()==0):
                pass
            
            temp = self.read()
            while True:
                temp = self.read()
                if temp=='DONE':
                    break

            print("Nothing to do!")
            
        return 0