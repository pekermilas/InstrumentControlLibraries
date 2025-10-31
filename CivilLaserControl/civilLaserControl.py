# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import serial
import serial.tools.list_ports
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
        self.laserIndex = 0
        self.laserPower = 0
        
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

    def setLaser(self, lIndex = 0, lPower = 0):
        self.laserIndex = lIndex
        self.laserPower = lPower
        return 0

    def setLaserPower(self, lPower = None):
        if lPower is None:
            self.laserPower = 0
        else:
            self.laserPower = lPower
        return 0

    def getLaserIndex(self):
        return self.laserIndex
    
    def getLaserPower(self):
        return self.laserPower

    def runLaser(self):
        if not self.dev is None:
            msgString = str(self.laserIndex)+','+str(self.laserPower)
            self.dev.write(msgString.encode())
        
            while(self.dev.inWaiting()==0):
                pass
            temp = int(self.dev.readline().decode('utf-8').strip())
            
            if int(temp) == self.laserIndex:
                returnVal = 0
            else:
                returnVal = -1
                
            if self.laserPower>0: 
                self.onoff = True
            else:
                self.onoff = False
        
        else:
            print("Nothing to do!")
            returnVal = 1
        
        return returnVal

