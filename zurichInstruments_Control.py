# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 16:06:33 2026

@author: pekermilas
"""

import time
import zhinst.core
import zhinst.toolkit as zt
import zhinst.ziPython as zi
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

discovery = zi.ziDiscovery()
device_id = discovery.find('dev32271')
device_props = discovery.get(device_id)

class ziDevice:

    def __init__(self, devSerial = None):
        self.devSerial = devSerial or 'dev32271'
        self.session = None
        self.device = None
        self.rm = None
        self.consts = dict()
        
    def connectDevice(self):
        discovery = zi.ziDiscovery()
        device_id = discovery.find(self.devSerial)
        device_props = discovery.get(device_id)
        
        # Session definition and settings!!! 
        self.session = zt.session.Session(server_host=device_props['serveraddress'], 
                                          server_port=device_props['serverport'], 
                                          allow_version_mismatch=True)

        # Device definition and settings!!! 
        self.device = self.session.connect_device(self.devSerial)
        
    def getConstants(self):
        self.consts['Oscillation Frequency'] = input("Please enter Oscillation Frequency in Hz: ")
        self.consts['Max bandwidth'] = input("Please enter Maximum Bandwidth in Hz: ")
        
    
    
    def setConstants(self):
        
        self.session.daq_server.set('/dev32271/imps/0/freq', 501000)
        self.session.daq_server.set('/dev32271/imps/0/maxbandwidth', 10000)
        self.session.daq_server.set('/dev32271/imps/0/auto/inputrange', ???)
        self.session.daq_server.set('/dev32271/imps/0/current/range', ???)
        self.session.daq_server.set('/dev32271/imps/0/voltage/range', ???)
        self.session.daq_server.set('/dev32271/imps/0/omegasuppression', ???)
        self.session.daq_server.set('/dev32271/imps/0/demod/rate', ???)
        self.session.daq_server.set('/dev32271/imps/0/mode', 1)
        
        self.session.daq_server.set('/dev32271/tu/thresholds/0/input', 59)
        self.session.daq_server.set('/dev32271/tu/thresholds/0/activationtime', 0.006)
        self.session.daq_server.set('/dev32271/tu/thresholds/0/deactivationtime', 0.003)
        self.session.daq_server.set('/dev32271/tu/logicunits/0/inputs/0/not', 1)
        
        self.session.daq_server.set('/dev32271/auxouts/0/outputselect', 13)
        self.session.daq_server.set('/dev32271/auxouts/0/scale', -3)
        self.session.daq_server.set('/dev32271/auxouts/0/offset', -2)
        self.session.daq_server.set('/dev32271/auxouts/0/limitlower', -2)
        self.session.daq_server.set('/dev32271/auxouts/0/limitupper', 0)
        
        self.session.daq_server.set('/dev32271/sigouts/0/add', 1)

        self.session.daq_server.set('/dev32271/triggers/out/0/source', 1)





# MFIA DLTS Configuration

# Set up
# Connect Aux Input 1 to Aux Output 1 (BNC cable)
# Connect Aux Output 2 to Trigger In (Back side) (BNC cable)
# Connect the DUT using a breadboard or test fixture MFITF.
# Connect data to USB

# LabOne Software settings

# Start LabOne Softwarwe
# On Impedance Analyzer window, under Measurement Control
# 	Change Mode to Advance by toggling 
# 	+Set "Osc Frequency" to the maximum value. For our instrument it is "510.00000000k"
# 	+Go to "Bandwidth Control" and set it to 10KHz.
# 	+Go to Range Control and select "Manual" from drop down menu. 
#   +Set the limits to Current range = 10m and Voltage range = 3V.
# 	+Set Max Bandwidth (Hz) = 10k, 
#   +w (omega) suppression = 80dB.
# 	+Set Rate (Sa/s) = 60k.
# 	+Go to "Equivalent Circuit" and select "4 Terminal"
# 	
# Open TU (Threshold Unit) tab from the menu on the left edge of the screen.
# 	+On signal selecton select "TU Output Value" from the dropdown list.
# 	+Set pulse values as seconds using State Enable and State Disable options (example 6ms/2ms).
# 	+On the right hand side from "Logic Units" tab turn on the option-1 corresponding to "TU Output Value".
# 	
# Open Aux tab from the menu on the left edge of the screen.
# 	+Go to Aux Output tab and select "TU Output Value".
# 	+Set voltage (pulse) depth by inserting a value in "Scale" (example: -2V)
# 	+Set offset by entering a value to Offset. (Note: Total pulse depth is determined by scale. If you add offset, the pulse level will be Scale + Offset values.
# 	+Set lower and upper voltage limits (example:-10V,0V)
# 	
# Open Lock-in tab from the menu on the left edge of the screen.
# 	+On the right hand side, under "Signal Outputs" turn on "Add" option to generate square pulse.
# 	
# Open DIO tab from the menu on the left edge of the screen.
# 	+Go to Trigger Out section, select Threshold 1 under signal option.
# 	
# Open Plotter tab from the menu on the left edge of the screen.
# 	Select the desired channels to view.
# 		For capacitance: Impedance 1 Sample Rep in F.
# 		For square pulse: Select "Auxiliary Input 1" and click on "Add Signal" and click on the box to add to the plotter.
# 		
# Open DAQ tab from the menu on the left edge of the screen.
# 	Go to Control
# 	Select the desired channels to view.
# 		For capacitance: Impedance 1 Sample Rep in F.
# 		For square pulse: Select "Auxiliary Input 1" and click on "Add Signal" and click on the box to add to the plotter.
# 	Go to Settings
# 		Trigger Settings --> Select Demod 1 Trig Out 1, Trigger Type: HW Trigger, Trigger Edge: Positive
# 		Horizontal --> Hold off time(s): 200um, Hold off count: 0, Delay (s): -1m, Refresh rate (Hz): 5
# 	Go to Grid
# 		Grid Settings --> Mode: Exact (on-grid), Operation: Average, Columns: 2048, Repetions: Depends on the desired averaging count (Example: 20)
# 	Data is shown under History. Can be saved in different formats.	

# Note:
# Test Sample: Schottky diode connection -->
# 	Use MFITF test fixture.
# 	Attach the silver band side to the LCUR and the other lead to HCUR.
# 	Expected capacitance value is around 100pF at -2V bias (V_R = 2V)

# Test Sample: BPW 21 Photodiode -->
# 	Use a breadboard for 4-terminal connection.
# 	Attach the lead close to the tab on the package to the HCUR. Attach the other lead to LCUR.MFIA DLTS Configuration

# Set up
# Connect Aux Input 1 to Aux Output 1 (BNC cable)
# Connect Aux Output 2 to Trigger In (Back side) (BNC cable)
# Connect the DUT using a breadboard or test fixture MFITF.
# Connect data to USB

# LabOne Software settings

# Start LabOne Softwarwe
# On Impedance Analyzer window, under Measurement Control
# 	Change Mode to Advance by toggling 
# 	Set "Osc Frequency" to the maximum value. For our instrument it is "510.00000000k"
# 	Go to "Bandwidth Control" and set it to 10KHz.
# 	Go to Range Control and select "Manual" from drop down menu. Set the limits to Current range = 10m and Voltage range = 3V.
# 	Set Max Bandwidth (Hz) = 10k, w (omega) suppression = 80dB.
# 	Set Rate (Sa/s) = 60k.
# 	Go to "Equivalent Circuit" and select "4 Terminal"
# 	
# Open TU (Threshold Unit) tab from the menu on the left edge of the screen.
# 	On signal selecton select "TU Output Value" from the dropdown list.
# 	Set pulse values as seconds using State Enable and State Disable options (example 6ms/2ms).
# 	On the right hand side from "Logic Units" tab turn on the option-1 corresponding to "TU Output Value".
# 	
# Open Aux tab from the menu on the left edge of the screen.
# 	Go to Aux Output tab and select "TU Output Value".
# 	Set voltage (pulse) depth by inserting a value in "Scale" (example: -2V)
# 	Set offset by entering a value to Offset. (Note: Total pulse depth is determined by scale. If you add offset, the pulse level will be Scale + Offset values.
# 	Set lower and upper voltage limits (example:-10V,0V)
# 	
# Open Lock-in tab from the menu on the left edge of the screen.
# 	On the right hand side, under "Signal Outputs" turn on "Add" option to generate square pulse.
# 	
# Open DIO tab from the menu on the left edge of the screen.
# 	Go to Trigger Out section, select Threshold 1 under signal option.
# 	
# Open Plotter tab from the menu on the left edge of the screen.
# 	Select the desired channels to view.
# 		For capacitance: Impedance 1 Sample Rep in F.
# 		For square pulse: Select "Auxiliary Input 1" and click on "Add Signal" and click on the box to add to the plotter.
# 		
# Open DAQ tab from the menu on the left edge of the screen.
# 	Go to Control
# 	Select the desired channels to view.
# 		For capacitance: Impedance 1 Sample Rep in F.
# 		For square pulse: Select "Auxiliary Input 1" and click on "Add Signal" and click on the box to add to the plotter.
# 	Go to Settings
# 		Trigger Settings --> Select Demod 1 Trig Out 1, Trigger Type: HW Trigger, Trigger Edge: Positive
# 		Horizontal --> Hold off time(s): 200um, Hold off count: 0, Delay (s): -1m, Refresh rate (Hz): 5
# 	Go to Grid
# 		Grid Settings --> Mode: Exact (on-grid), Operation: Average, Columns: 2048, Repetions: Depends on the desired averaging count (Example: 20)
# 	Data is shown under History. Can be saved in different formats.	

# Note:
# Test Sample: Schottky diode connection -->
# 	Use MFITF test fixture.
# 	Attach the silver band side to the LCUR and the other lead to HCUR.
# 	Expected capacitance value is around 100pF at -2V bias (V_R = 2V)

# Test Sample: BPW 21 Photodiode -->
# 	Use a breadboard for 4-terminal connection.
# 	Attach the lead close to the tab on the package to the HCUR. Attach the other lead to LCUR.





