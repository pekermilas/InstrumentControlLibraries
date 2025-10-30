# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import serial
import serial.tools.list_ports
import numpy as np
import os
import time

class civilLaser:

    def __init__(self, port = None):
        pcPorts = [tuple(p) for p in list(serial.tools.list_ports.comports())]
        self.port = port or [i[0] for i in pcPorts if not i[1].find('Arduino ')==-1][0]
        self.baudrate = 9600
        self.dsrdtr = True
        self.dev = None
        self.onoff = False
        self.timeout = None
    
    def open(self):
        if self.dev is None:
            try:
                self.dev = serial.Serial()
                self.dev.port = self.port
                self.dev.baudrate = self.baudrate
                self.dev.dsrdtr = self.dsrdtr
                self.dev.open()
                time.sleep(0.2)
            except IndexError:
                returnVal = -1
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
            print("Nothing to do!")
            returnVal = -1

        return returnVal
    
    def runLaser(self, laserIndex = 0, laserPower = 0):
        if not self.dev is None:
            msgString = str(laserIndex)+','+str(laserPower)
            self.dev.write(msgString.encode())
        
            while(self.dev.inWaiting()==0):
                pass
            temp = int(self.dev.readline().decode('utf-8').strip())
            returnVal = 0
            if int(temp) == laserIndex:
                print("Hello there!")
            
            if laserPower>0 : 
                self.onoff = True
            else:
                self.onoff = false
        
        else:
            print("Nothing to do!")
            returnVal = -1
        
        return returnVal

# def connectArduino():
#     pcPorts = [tuple(p) for p in list(serial.tools.list_ports.comports())]
#     # port = [i[0] for i in pcPorts if not i[0].find('/dev/ttyACM')==-1][0]
#     # port = [i[0] for i in pcPorts if not i[0].find('/dev/ttyAMA')==-1][0]
#     port = 'COM14'
#     pofbConf.port = port
    
#     try:
#         arduino = serial.Serial()
#         arduino.baudrate = 9600
#         arduino.port = port
#         arduino.dsrdtr=True
#         arduino.open()
#         time.sleep(0.2)
#         Arduino_onoff = True
#         arduino.timeout = None
#     except IndexError:
#         Arduino_onoff = False
    
#     maxTimeDelay=2.0

#     pofbConf.arduino = arduino
#     pofbConf.Arduino_onoff = Arduino_onoff
    
#     return 0
    
# def disconnArduino():
#     arduino = pofbConf.arduino
#     Arduino_onoff = pofbConf.Arduino_onoff
#     if Arduino_onoff:
#         arduino = arduino
#         arduino.close()
#         Arduino_onoff = False
#     else:
#         print("Nothing to do!")
        
#     return 0
    
# def pulseTeensyForRabi():
#     arduino = pofbConf.arduino
#     Arduino_onoff = pofbConf.Arduino_onoff
    
#     dataLen = len(np.arange(pofbConf.tInitial,pofbConf.tFinal,pofbConf.tIncrem))+1
    
#     if Arduino_onoff:
#         msgString = str(pofbConf.tON)+','+str(pofbConf.t1)+','+str(pofbConf.t2)
#         msgString = msgString+','+str(pofbConf.t3)+','+str(pofbConf.t4)+','+str(pofbConf.t5)
#         msgString = msgString+','+str(pofbConf.t6)+','+str(pofbConf.t7)+','+str(pofbConf.tOFF1)
#         msgString = msgString+','+str(pofbConf.tREAD)+','+str(pofbConf.tRST)+','+str(pofbConf.tOFF2)
#         msgString = msgString+','+str(pofbConf.tFinal)+','+str(pofbConf.tIncrem)
#         msgString = msgString+','+str(pofbConf.numRepeat)+','+str(pofbConf.samplingSize)
#         msgString = msgString+','+str(pofbConf.rfF)+','+str(pofbConf.rfP)
#         msgString = msgString+','+str(pofbConf.rfDf)+','+str(pofbConf.rfNf)
#         msgString = msgString+','+str(pofbConf.expType)+','+str(pofbConf.testType)
        
        
#         print(msgString)
#         arduino.write(msgString.encode())
        
#         while(arduino.inWaiting()==0):
#             pass
        
#         line = []
#         while True:
#             temp = arduino.readline().decode('utf-8').strip()
#             line = np.append(line, temp)
#             if len(line)==dataLen:
#                 break
#         data = np.array([i.split("\t") for i in line], dtype=float)
 
#     else:
#          print("Nothing to do!")
         
#     return data
    

# if __name__ == '__main__':

#     print('Teensy controller is loaded!') 