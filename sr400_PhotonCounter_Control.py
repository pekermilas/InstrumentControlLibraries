# -*- coding: utf-8 -*-
"""
Created on Thu Sep 25 08:35:50 2025

@author: admin
"""
# EXAMPLE CALLS
# t = sr400.sr400()
# t.open()
# t.dev.query('SS 1')

# EXAMPLE CALLS
# import sr400_PhotonCounter_Control as sr400
# t = sr400.sr400()
# t.open()
# t.frontPanel_messageString('hello there!')
# t.close()


# I need to write proper default mechanism for all the methods
# which uses read argument for their cases of not given the other
# parameter!!!

import pyvisa as visa
import os
import numbers

class sr400:

    def __init__(self, port = None):
        # self.port = port or "COM3"
        self.port = port or 'GPIB0::23::INSTR'
        self.dev = None
        self.visaLib = 'ni-visa' # or 'py-visa'
        self.rm = None
            
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
                self.dev.baud_rate = 19200 # Min : 300, Max : 19200
            
                # self.dev.write("*RST")
                self.dev.query("SS 1")
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

# ----------------------- SECTION MODE START ------------------------------- #
    def mode_countMode(self, mode = None):
        # (Manual p.41)
        modeDict = {'A,B': 0, 'A-B': 1, 'A+B': 2, 'A*B': 3}
        if mode is None:
            returnVal = self.query('CM').rstrip()
        else:
            if mode in list(modeDict):
                self.write('CM ' + str(modeDict[mode]))
                returnVal = 0
            else:
                self.write('CM ' + str(0))
                returnVal = -1
        return returnVal

    def mode_counterToInput(self, counter = 'A', counterInput = None):
        counterDict = {'A': 0, 'B': 1, 'T': 2}
        if counter in list(counterDict):
            if counterInput is None:
                returnVal = self.query('CI '+ str(counterDict[counter])).rstrip()
            else:
                if counter == 'A':
                    if counterInput == 0 or counterInput == 1:
                        self.write('CI '+ str(counterDict[counter]) + ',' + str(counterInput))
                        returnVal = 0
                    else:
                        self.write('CI '+ str(counterDict[counter]) + ',' + str(0))
                        returnVal = -1
                if counter == 'B':
                    if counterInput == 1 or counterInput == 2:
                        self.write('CI '+ str(counterDict[counter]) + ',' + str(counterInput))
                        returnVal = 0
                    else:
                        self.write('CI '+ str(counterDict[counter]) + ',' + str(1))
                        returnVal = -1
                if counter == 'T':
                    if counterInput == 0 or counterInput == 2 or counterInput == 3:
                        self.write('CI '+ str(counterDict[counter]) + ',' + str(counterInput))
                        returnVal = 0
                    else:
                        self.write('CI '+ str(counterDict[counter]) + ',' + str(0))
                        returnVal = -1
        else:
            self.query('CI '+ str(counterDict['A'])).rstrip()
            returnVal = -1
        return returnVal
        
    def mode_counterPreset(self, counter = 'B', counterPreset = None):
        # counterPreset is not ins seconds! It is number of cycles of 10MHz clock
        counterDict = {'B': 1, 'T': 2}
        if counter in list(counterDict):
            if counterPreset is None:
                returnVal = self.query('CP '+ str(counterDict[counter])).rstrip()
            else:
                if 1 <= counterPreset <= 9E11:
                    self.write('CP '+ str(counterDict[counter]) + ',' + str(int(counterPreset)))
                    returnVal = 0
                elif counterPreset < 1:
                    self.write('CP '+ str(counterDict[counter]) + ',' + str(1))
                    returnVal = -1
                elif counterPreset > 9E11:
                    self.write('CP '+ str(counterDict[counter]) + ',' + str(9E11))
                    returnVal = -1
                else:
                    self.query('CP '+ str(counterDict[counter])).rstrip()
                    returnVal = -1
        else:
            self.query('CP '+ str(counterDict['B'])).rstrip()
            returnVal = -1

        return returnVal
        
    def mode_scanPeriods(self, num = None):
        if num is None:
            returnVal = self.query('NP').rstrip()
        else:
            if isinstance(num, numbers.Number):
                if 1 <= num <= 2000:
                    self.write('NP ' + str(num))
                    returnVal = 0
                elif num < 1:
                    self.write('NP ' + str(1))
                    returnVal = -1
                else:
                    self.write('NP ' + str(2000))
                    returnVal = -1
            else:
                self.query('NP').rstrip()
                returnVal = -1
        return returnVal

    def mode_scanPosition(self):
        return self.query('NN').rstrip()

    def mode_scanEndMode(self, scanMode = None):
        if scanMode is None:
            returnVal = self.query('NE').rstrip()
        else:
            if isinstance(scanMode, numbers.Number):
                if scanMode == 0 or scanMode == 1:
                    self.write('NE '+ str(scanMode))
                    returnVal = 0
                else:
                    self.write('NE '+ str(0))
                    returnVal = -1
            else:
                self.query('NE').rstrip()
                returnVal = -1
        return returnVal

    def mode_dwellTime(self, dwellTime = None):
        if dwellTime is None:
            returnVal = self.query('DT').rstrip()
        else:
            if isinstance(dwellTime, numbers.Number):
                if 2E-3 <= dwellTime <= 6E1:
                    self.write('DT ' + str(dwellTime))
                    returnVal = 0
                else:
                    if dwellTime==0:
                        self.write('DT ' + str(dwellTime))
                        returnVal = 1
                    elif dwellTime < 2E-3:
                        self.write('DT ' + str(2E-3))
                        returnVal = -1
                    else:
                        self.write('DT ' + str(6E1))
                        returnVal = -1
            else:
                self.query('DT').rstrip()
                returnVal = -1
        return returnVal

    def mode_analogSource(self, counter = None):
        sourceDict = {'A': 0, 'B': 1, 'A-B': 2, 'A+B': 3}
        if counter is None:
            returnVal = self.query('AS').rstrip()
        else:
            if counter in list(sourceDict):
                self.write('AS ' + str(sourceDict[counter]))
                returnVal = 0
            else:
                self.write('AS ' + str(0))
                returnVal = -1
        return returnVal

    def mode_analogOutputScale(self, outputScale = None):
        if outputScale is None:
            returnVal = self.query('AM').rstrip()
        else:
            if isinstance(outputScale, numbers.Number):
                if 0 <= outputScale <= 7:
                    self.write('AM ' + str(int(outputScale)))
                    returnVal = 0
                elif outputScale < 0:
                    self.write('AM ' + str(0))
                    returnVal = -1
                else:
                    self.write('AM ' + str(7))
                    returnVal = -1
            else:
                self.query('AM').rstrip()
                returnVal = -1
        return returnVal

    def mode_setDisplayMode(self, dispMode = None):
        dispModeDict = {'continuous': 0, 'hold': 1}
        if dispMode is None:
            returnVal = self.query('SD').rstrip()
        else:
            if dispMode in list(dispModeDict):
                self.write('SD '+ str(dispModeDict[dispMode]))
                returnVal = 0
            else:
                self.query('SD').rstrip()
                returnVal = -1
        return returnVal
# ----------------------- SECTION MODE END ------------------------------- #
##################






# --------------------- SECTION LEVELS START ----------------------------- #
    def levels_triggerSlope(self, trigSlope = None): # CHECK THE DEFAULT!!!
        tSlopeDict = {'rise': 0, 'fall': 1}
        if trigSlope is None:
            returnVal = self.query('TS').rstrip()
        else:
            if trigSlope in list(tSlopeDict):
                self.write('TS '+ str(tSlopeDict[trigSlope]))
                returnVal = 0
            else:
                self.query('TS').rstrip()
                returnVal = -1
        return returnVal

    def levels_triggerLevel(self, trigLevel = None): # CHECK THE DEFAULT!!!
        if trigLevel is None:
            returnVal = self.query('TL').rstrip()
        else:
            if isinstance(trigLevel, numbers.Number):
                if -2.0 <= trigLevel <= 2.0:
                    self.write('TL '+ str(trigLevel))
                    returnVal = 0
                elif trigLevel < -2.0:
                    self.write('TL '+ str(-2.0))
                    returnVal = -1
                else:
                    self.write('TL '+ str(2.0))
                    returnVal = -1
            else:
                self.query('TL').rstrip()
                returnVal = -1
            
        return returnVal

    def levels_discriminatorSlope(self, disc = 'A', discSlope = None):  # CHECK THE DEFAULT!!!
        discDict = {'A': 0, 'B': 1, 'T':2}
        discSlopeDict = {'rise': 0, 'fall': 1}
        if disc in list(discDict):
            if discSlope is None:
                returnVal = self.query('DS ' + str(discDict[disc])).rstrip()
            else:
                if discSlope in list(discSlopeDict):
                    self.write('DS '+ str(discDict[disc]) + ',' + 
                               str(discSlopeDict[discSlope]))
                    returnVal = 0
                else:
                    self.query('DS ' + str(discDict[disc])).rstrip()
                    returnVal = -1
                    
        else:
            self.query('DS ' + str(discDict['A'])).rstrip()
            returnVal = -1
            
        return returnVal

    def levels_discriminatorMode(self, disc = 'A', discMode = None):  # CHECK THE DEFAULT!!!
        discDict = {'A': 0, 'B': 1, 'T':2}
        discModeDict = {'fixed': 0, 'scan': 1}
        if disc in list(discDict):
            if discMode is None:
                returnVal = self.query('DM ' + str(discDict[disc])).rstrip()
            else:
                if discMode in list(discModeDict):
                    self.write('DM '+ str(discDict[disc]) + ',' + 
                               str(discModeDict[discMode]))
                    returnVal = 0
                else:
                    self.query('DM ' + str(discDict[disc])).rstrip()
                    returnVal = -1
        else:
            self.query('DM ' + str(discDict['A'])).rstrip()
            returnVal = -1
        
        return returnVal

    def levels_discriminatorScanStepSize(self, disc = 'A', stepSize = None):  # CHECK THE DEFAULT!!!
        discDict = {'A': 0, 'B': 1, 'T':2}    
        if disc in list(discDict):
            if stepSize is None:
                returnVal = self.query('DY ' + str(discDict[disc])).rstrip()
            else:
                if isinstance(stepSize, numbers.Number):
                    if -2.0 <= stepSize <= 2.0:
                        self.write('DY '+ str(discDict[disc]) + ',' + str(stepSize))
                        returnVal = 0
                    elif stepSize < -2.0:
                        self.write('DY '+ str(discDict[disc]) + ',' + str(-2.0))
                        returnVal = -1
                    else:
                        self.write('DY '+ str(discDict[disc]) + ',' + str(2.0))
                        returnVal = -1
                else:
                    self.query('DY ' + str(discDict[disc])).rstrip()
                    returnVal = -1
        else:
            self.query('DY ' + str(discDict['A'])).rstrip()
            returnVal = -1
            
        return returnVal

    def levels_discriminatorLevel(self, disc = 'A', discLevel = None):  # CHECK THE DEFAULT!!!
        discDict = {'A': 0, 'B': 1, 'T':2}
        if disc in list(discDict):
            if discLevel is None:
                returnVal = self.query('DL ' + str(discDict[disc])).rstrip()
            else:
                if isinstance(discLevel, numbers.Number):
                    if -0.3 <= discLevel <= 0.3:
                        self.write('DL '+ str(discDict[disc]) + ',' + str(discLevel))
                        returnVal = 0
                    elif discLevel < -0.3:
                        self.write('DL '+ str(discDict[disc]) + ',' + str(-0.3))
                        returnVal = -1
                    else:
                        self.write('DL '+ str(discDict[disc]) + ',' + str(0.3))
                        returnVal = -1
                else:
                    self.query('DL ' + str(discDict[disc])).rstrip()
                    returnVal = -1
        else:
            self.query('DL ' + str(discDict['A'])).rstrip()
            
        return returnVal
    
    def levels_discriminatorLevelDuringScan(self, disc = 'A'):  # CHECK THE DEFAULT!!!
        discDict = {'A': 0, 'B': 1, 'T':2}
        if disc in list(discDict):
            returnVal = self.query('DZ ' + str(discDict[disc])).rstrip()
        else:
            returnVal = self.query('DZ ' + str(discDict['A'])).rstrip()
        return returnVal
    
    def levels_rearPanelPortMode(self, port = 'port1', portMode = None):  # CHECK THE DEFAULT!!!
        portDict = {'port1': 1, 'port2': 2}
        portModeDict = {'fixed': 0, 'scan': 1}
        if port in list(portDict):
            if portMode is None:
                returnVal = self.query('PM ' + str(portDict[port])).rstrip()
            else:
                if portMode in list(portModeDict):
                    self.write('PM '+ str(portDict[port]) + ',' + 
                               str(portModeDict[portMode]))
                    returnVal = 0
                else:
                    self.query('PM ' + str(portDict[port])).rstrip()
                    returnVal = -1
        else:
            self.query('PM ' + str(portDict['port1'])).rstrip()
            returnVal = -1
            
        return returnVal
    
    def levels_rearPanelPortScanStepSize(self, port = 'port1', stepSize = None):  # CHECK THE DEFAULT!!!
        portDict = {'port1': 1, 'port2': 2}
        if port in list(portDict):
            if stepSize is None:
                returnVal = self.query('PY ' + str(portDict[port])).rstrip()
            else:
                if isinstance(stepSize, numbers.Number):
                    if -0.5 <= stepSize <= 0.5:
                        self.write('PY '+ str(portDict[port]) + ',' + str(stepSize))
                        returnVal = 0
                    elif stepSize < -0.5:
                        self.write('PY '+ str(portDict[port]) + ',' + str(-0.5))
                        returnVal = -1
                    else:
                        self.write('PY '+ str(portDict[port]) + ',' + str(0.5))
                        returnVal = -1
                else:
                    self.query('PY ' + str(portDict[port])).rstrip()
                    returnVal = -1
        else:
            self.query('PY ' + str(portDict['port1'])).rstrip()
            returnVal = -1
            
        return returnVal

    def levels_rearPanelPortOutputLevel(self, port = 'port1', voltLevel = None):  # CHECK THE DEFAULT!!!
        portDict = {'port1': 1, 'port2': 2}
        if port in list(portDict):
            if voltLevel is None:
                returnVal = self.query('PL ' + str(portDict[port])).rstrip()
            else:
                if isinstance(voltLevel, numbers.Number):
                    if -10.0 <= voltLevel <= 10.0:
                        self.write('PL '+ str(portDict[port]) + ',' + str(voltLevel))
                        returnVal = 0
                    elif voltLevel < -10.0:
                        self.write('PL '+ str(portDict[port]) + ',' + str(-10.0))
                        returnVal = -1
                    else:
                        self.write('PL '+ str(portDict[port]) + ',' + str(10.0))
                        returnVal = -1
                else:
                    self.query('PL ' + str(portDict[port])).rstrip()
                    returnVal = -1
        else:
            self.query('PL ' + str(portDict['port1'])).rstrip()
            returnVal = -1
            
        return returnVal

    def levels_rearPanelPortLevelDuringScan(self, port = 'port1'):  # CHECK THE DEFAULT!!!
        portDict = {'port1': 1, 'port2': 2}
        if port in list(portDict):
            returnVal = self.query('PZ ' + str(portDict[port])).rstrip()
        else:
            returnVal = self.query('PZ ' + str(portDict['port1'])).rstrip()
        return returnVal
# ----------------------- SECTION LEVELS END ----------------------------- #
##################
# ----------------------- SECTION GATES START --------------------------- #
    def gates_gateMode(self, gate = 'A', gateMode = None):  # CHECK THE DEFAULT!!!
        gateDict = {'A': 1, 'B': 2}
        gateModeDict = {'cw': 0, 'fixed': 1, 'scan': 2}
        if gate in list(gateDict):
            if gateMode is None:
                returnVal = self.query('GM ' + str(gateDict[gate])).rstrip()
            else:
                if gateMode in list(gateModeDict):
                    self.write('GM '+ str(gateDict[gate]) + ',' + 
                               str(gateModeDict[gateMode]))
                    returnVal = 0
                else:
                    self.query('GM ' + str(gateDict[gate])).rstrip()
                    returnVal = -1
        else:
            self.query('GM ' + str(gateDict['A'])).rstrip()
            returnVal = -1
        
        return returnVal

    def gates_gateScanStepSize(self, gate = 'A', stepSize = None):  # CHECK THE DEFAULT!!!
        gateDict = {'A': 1, 'B': 2}
        if gate in list(gateDict):
            if stepSize is None:
                returnVal = self.query('GY ' + str(gateDict[gate])).rstrip()
            else:
                if isinstance(stepSize, numbers.Number):
                    if 0.0 <= stepSize <= 99.92E-3:
                        self.write('GY '+ str(gateDict[gate]) + ',' +str(stepSize))
                        returnVal = 0
                    elif stepSize < 0.0:
                        self.write('GY '+ str(gateDict[gate]) + ',' + str(0.0))
                        returnVal = -1
                    else:
                        self.write('GY '+ str(gateDict[gate]) + ',' + str(99.92E-3))
                        returnVal = -1
                else:
                    self.query('GY ' + str(gateDict[gate])).rstrip()
                    returnVal = -1
        else:
            self.query('GY ' + str(gateDict['A'])).rstrip()
            returnVal = -1
        
        return returnVal

    def gates_gateDelay(self, gate = 'A', gateDelay = None):  # CHECK THE DEFAULT!!!
        gateDict = {'A': 1, 'B': 2}
        if gate in list(gateDict):
            if gateDelay is None:
                returnVal = self.query('GD ' + str(gateDict[gate])).rstrip()
            else:
                if isinstance(gateDelay, numbers.Number):
                    if 0.0 <= gateDelay <= 999.2E-3:
                        self.write('GD '+ str(gateDict[gate]) + ',' + str(gateDelay))
                        returnVal = 0
                    elif gateDelay < 0.0:
                        self.write('GD '+ str(gateDict[gate]) + ',' + str(0.0))
                        returnVal = -1
                    else:
                        self.write('GD '+ str(gateDict[gate]) + ',' + str(999.2E-3))
                        returnVal = -1
                else:
                    self.query('GD ' + str(gateDict[gate])).rstrip()
                    returnVal = -1
        else:
            self.query('GD ' + str(gateDict[gate])).rstrip()
            returnVal = -1
            
        return returnVal

    def gates_delayPosition(self, gate = 'A'):
        gateDict = {'A': 1, 'B': 2}
        if gate in list(gateDict):
            returnVal = self.query('GZ ' + str(gateDict[gate])).rstrip()
        else:
            returnVal = self.query('GZ ' + str(gateDict['A'])).rstrip()
        return returnVal

    def gates_gateWidth(self, gate = 'A', gateWidth = None):  # CHECK THE DEFAULT!!!
        gateDict = {'A': 1, 'B': 2}
        if gateWidth is None:
            returnVal = self.query('GW ' + '%G' %gateDict[gate]).rstrip()
        else:
            if 0.005E-6 <= stepSize <= 999.2E-3:
                self.write('GW '+ '%G' %gateDict[gate] + ',' +'%G' %stepSize)
                returnVal = 0
            elif stepSize < 0.005E-6:
                self.write('GW '+ '%G' %gateDict[gate] + ',' +'%G' %0.005E-6)
                returnVal = -1
            elif stepSize > 999.2E-3:
                self.write('GW '+ '%G' %gateDict[gate] + ',' +'%G' %999.2E-3)
                returnVal = -1
            else:
                self.write('GW '+ '%G' %gateDict[gate] + ',' +'%G' %0.1)
                returnVal = -1
        return returnVal
# ----------------------- SECTION GATES END ----------------------------- #
##################
# ------------------ SECTION FRONT PANEL START -------------------------- #
    def frontPanel_counterStart(self):
        self.write('CS')
        return 0
    
    def frontPanel_counterStop(self):
        self.write('CH')
        return 0

    def frontPanel_counterReset(self):
        self.write('CR')
        return 0

    def frontPanel_pressButton(self, button = 'down cursor'):
        buttonDict = {'down cursor': 0, 'right cursor': 1, 'level': 2,
                      'setup': 3, 'com': 4, 'stop': 5, 'local': 6,
                      'reset': 7, 'left cursor': 8, 'up cursor': 9,
                      'mode': 10, 'agate': 11, 'bgate': 12, 'start': 13}
        if button in list(buttonDict):
            self.write('CK '+ str(buttonDict[button]))
            returnVal = 0
        else:
            self.write('CK '+ str(buttonDict['stop']))
            returnVal = -1
        return returnVal

    def frontPanel_cursorPosition(self):  # CHECK THE DEFAULT!!!
        cursorDict = {0: 'returned for left', 1: 'returned for right',
                      2: 'inactive'}
        returnVal = cursorDict[self.query('SC').rstrip()]
        return returnVal

    def frontPanel_modeInhibit(self, mode = 'local'):
        modeInhibDict = {0: 'local', 1: 'remote', 2: 'lock-out'}
        if mode in list(modeInhibDict):
            self.write('MI '+ str(modeInhibDict[mode]))
            returnVal = 0
        else:
            self.write('MI '+ str(0))
            returnVal = -1
        return returnVal

    def frontPanel_messageString(self, mssg = None):
        self.write('MS '+ str(mssg))
        return 0
    
    def frontPanel_menuDisplay(self, select = 'count'):
        displayDict = {'count': [1,1], 'A': [1,2], 'B': [1,3],'T': [1,4], 
                       'n-periods': [1,5], 'at-n':[1,6], 'd/a-out': [1,7], 
                       'd/a-range': [1,8], 'display': [1,9], 'a-gate': [2,1],
                       'a-delay': [2,2], 'a-width': [2,3], 'b-gate': [3,1],
                       'b-delay': [3,2], 'b-width': [3,3], 'trig-slope': [4,1],
                       'trig-lvl': [4,2], 'a-disc-slope': [4,3], 
                       'a-disc-mode': [4,4], 'a-disc-lvl': [4,5],
                       'b-disc-slope': [4,6], 'b-disc-mode': [4,7],
                       'b-disc-lvl': [4,8], 't-disc-slope': [4,9],
                       't-disc-mode': [4,10], 't-disc-lvl': [4,11],
                       'port1-mode': [4,12], 'port1-lvl': [4,13],
                       'port2-mode': [4,12], 'port2-lvl': [4,13],
                       'gpib-addr': [5,1], 'rs232-baud': [5,2],
                       'rs232-bits': [5,3], 'rs232-parity': [5,4],
                       'rs232-wait': [5,5], 'rs232-echo': [5,6], 'data': [5,7],
                       'lcd-contrast': [6,1], 'store': [6,2], 'recall': [6,3]}
        if select in list(displayDict):
            self.write('MD '+ str(displayDict[select][0]) + ',' +
                       str(displayDict[select][1]))
            returnVal = 0
        else:
            self.write('MD '+ str(1) + ',' + str(1))
            returnVal = -1
        return returnVal

    def frontPanel_getMenuNumber(self):  # CHECK THE DEFAULT!!!
        return self.read('MM').rstrip()

    def frontPanel_getMenuLine(self):
        return self.read('ML').rstrip()
# ------------------- SECTION FRONT PANEL END --------------------------- #
















##################
# ------------------- SECTION INTERFACE START --------------------------- #
    def interface_fullReset(self):
        self.write('CL')
        return 0

    def interface_readStatusByte(self, bit = None):
        # All in manual p.48-49
        # 0 : Checks if parameter change
        # 1 : Checks if count finished
        # 2 : Checks if scan finished
        # 3 : Checks if overrun
        # 4 : Checks if gate error
        # 5 : Checks if recall error
        # 6 : Checks if SQR
        # 7 : Checks if command error
        if bit is None:
            returnVal = self.query('SS').rstrip()
        elif 0 <= bit <= 7:
            returnVal = self.query('SS '+ '%G' %bit).rstrip()
        else:
            returnVal = self.query('SS').rstrip()
        return returnVal

    def interface_readSecondaryStatusByte(self, bit = None):
        # All in manual p.48-49
        # 0 : Checks if triggered
        # 1 : Checks if inhibited
        # 2 : Checks if counting
        if bit is None:
            returnVal = self.query('SI').rstrip()
        elif 0 <= bit <= 2:
            returnVal = self.query('SI '+ '%G' %bit).rstrip()
        else:
            returnVal = self.query('SI').rstrip()
        return returnVal

    def interface_gpibServiceRequest(self, value = None):  # CHECK THE DEFAULT!!!
        if value is None:
            returnVal = self.query('SV').rstrip()
        elif 0 <= value <= 255:
            returnVal = self.query('SV '+ '%G' %value).rstrip()
        else:
            returnVal = self.query('SV').rstrip()
        return returnVal

    def interface_rs232CharWaitInterval(self, multiples = None):  # CHECK THE DEFAULT!!!
        if multiples is None:
            returnVal = self.query('SW').rstrip()
        elif 0 <= value <= 25:
            returnVal = self.query('SW '+ '%G' %multiples).rstrip()
        else:
            returnVal = self.query('SW').rstrip()
        return returnVal

    def interface_rs232EndOfRecordChars(self, codes = [None, None, None, None]):
        if codes[0] is None:
            self.write('SE')
        elif codes[1] is None:
            j = codes[0] if 0 <= codes[0] <= 127 else 127
            self.write('SE '+ '%G' %j)
        elif codes[2] is None:
            j = codes[0] if 0 <= codes[0] <= 127 else 127
            k = codes[1] if 0 <= codes[1] <= 127 else 127
            self.write('SE '+ '%G' %j + ',' + '%G' %k)
        elif codes[3] is None:
            j = codes[0] if 0 <= codes[0] <= 127 else 127
            k = codes[1] if 0 <= codes[1] <= 127 else 127
            l = codes[2] if 0 <= codes[2] <= 127 else 127
            self.write('SE '+ '%G' %j + ',' + '%G' %k + ',' + 
                       '%G' %l)
        else:
            j = codes[0] if 0 <= codes[0] <= 127 else 127
            k = codes[1] if 0 <= codes[1] <= 127 else 127
            l = codes[2] if 0 <= codes[2] <= 127 else 127
            m = codes[0] if 0 <= codes[3] <= 127 else 127
            self.write('SE '+ '%G' %j + ',' + '%G' %k + ',' + 
                       '%G' %l + ',' + '%G' %m)
        return 0
# -------------------- SECTION INTERFACE END ---------------------------- #
##################
# ------------------ SECTION STORE/RECALL START ------------------------- #
    def storerecall_storeSettings(self, location = 1):
        if 1 <= location <= 9:
            self.write('ST '+ '%G' %location)
            returnVal = 0
        elif location < 1:
            self.write('ST '+ '%G' %1)
            returnVal = 1
        elif location > 9:
            self.write('ST '+ '%G' %9)
            returnVal = 1
        else:
            self.write('ST '+ '%G' %9)
            returnVal = -1
        return returnVal

    def storerecall_recallSettings(self, location = 0):
        if 0 <= location <= 9:
            self.write('ST '+ '%G' %location)
            returnVal = 0
        else:
            self.write('ST '+ '%G' %0)
            returnVal = -1
        return returnVal
# ------------------- SECTION STORE/RECALL END -------------------------- #
##################
# ---------------------- SECTION DATA START ----------------------------- #
    def data_readCounterFinished(self, counter = 'A', scanPoint = None):   # CHECK THE DEFAULT!!!
        if counter == 'A' or counter == 'B':
            if scanPoint is None:
                returnVal = self.query('Q'+str(counter)).rstrip()
            else:
                if 1 <= scanPoint <= 2000:
                    returnVal = self.query('Q' + str(counter) + ' ' + str(m)).rstrip()
                elif scanPoint < 1:
                    returnVal = self.query('Q' + str(counter) + ' ' + str(1)).rstrip()
                elif scanPoint > 2000:
                    returnVal = self.query('Q' + str(counter) + ' ' + str(2000)).rstrip()
                else:
                    returnVal = self.query('Q'+str(counter)).rstrip()
        else:
            returnVal = self.query('QA').rstrip()
        return returnVal

    def data_startNewScan(self, counter = 'A'):
        if counter == 'A' or counter == 'B' or counter == 'T':
            returnVal = self.query('F'+str(counter)).rstrip()
        else:
            returnVal = self.query('FA').rstrip()
        return returnVal
    
    def data_readCounterNow(self, counter = 'A', scanPoint = None):
        if counter == 'A' or counter == 'B':
            returnVal = self.query('X'+str(counter)).rstrip()
        else:
            returnVal = self.query('XA').rstrip()
        return returnVal
# ----------------------- SECTION DATA END ------------------------------ #


