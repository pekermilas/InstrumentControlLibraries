# -*- coding: utf-8 -*-
"""
Created on Mon Oct 13 21:22:47 2025

@author: peker
"""

import pyvisa as visa
import os
import numbers
import time

import sr400_PhotonCounter_Control as sr400

# This is the Python implementation of the example on p.56
# Original was written in Visual Basic

pcounter = sr400.sr400()
pcounter.open()
# pcounter.interface_fullReset()
# pcounter.mode_counterToInput(counter = 'A', counterInput = '10MHz')
pcounter.mode_counterToInput(counter = 'A', counterInput = 'input1')
pcounter.frontPanel_counterReset()
# pcounter.mode_scanPeriods(num = 4)
# pcounter.frontPanel_counterStart()

# for i in range(50):
#     # print(pcounter.interface_readStatusByte(bit = 1))
#     pcounter.interface_readStatusByte(bit = 1)
#     time.sleep(0.2)

# for i in range(4):
#     # while(not bool(int(pcounter.interface_readStatusByte(bit = 1)))):
#     while(int(pcounter.data_readCounterFinished('A', scanPoint=i+1))<0):
#         pass
#     print(pcounter.data_readCounterFinished(counter = 'A' , scanPoint=i+1))

# pcounter.data_readCounterFinished(counter = 'A', scanPoint = 4)

for i in range(100):
    print(pcounter.query('FA'))


# while(not bool(int(pcounter.interface_readStatusByte(bit = 1)))):
#     pass

# print(pcounter.data_readCounterFinished(counter = 'A'))
    
# for i in range(1):
#     while(not bool(int(pcounter.interface_readStatusByte(bit = 1)))):
#         pass

#     print(pcounter.data_readCounterNow(counter = 'A'))


# pcounter.data_readCounterFinished(counter = 'A', scanPoint = 1)

# For loop should wait before trying to print the data
# for i in range(10):
    # print(pcounter.data_readCounterFinished(counter = 'A', scanPoint = i))


# pcounter.frontPanel_messageString('hello there!')
pcounter.close()
