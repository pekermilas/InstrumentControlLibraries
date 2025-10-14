# -*- coding: utf-8 -*-
"""
Created on Mon Oct 13 21:22:47 2025

@author: peker
"""

import pyvisa as visa
import os
import numbers

import sr400_PhotonCounter_Control as sr400

# This is the Python implementation of the example on p.56
# Original was written in Visual Basic

pcounter = sr400.sr400()
pcounter.open()
pcounter.mode_counterToInput(counter = 'A', counterInput = '10MHz')
pcounter.frontPanel_counterReset()
pcounter.frontPanel_counterStart()
pcounter.data_readCounterFinished(counter = 'A', scanPoint = 1)

for i in range(500):
    


counter.frontPanel_messageString('hello there!')
counter.close()