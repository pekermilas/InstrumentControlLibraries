# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 13:28:06 2026

@author: pekermilas
"""
import time
import zhinst.core
import zhinst.toolkit as zt
import zhinst.ziPython as zi
import numpy as np
import matplotlib.pyplot as plt

discovery = zi.ziDiscovery()
device_id = discovery.find('dev32271')
device_props = discovery.get(device_id)

# This is the new toolkit version of definitions
# First the session is defined. Then the device.
# Parameter definitions in the old-school zhinst.core 
# kind of approach, now will occur in session

# Session definition and settings!!! 
session = zt.session.Session(server_host=device_props['serveraddress'], 
                             server_port=device_props['serverport'], 
                             allow_version_mismatch=True)

# First paragraph in Cemil's notes 
session.daq_server.set('/dev32271/tu/thresholds/0/input', 59)
session.daq_server.set('/dev32271/tu/thresholds/0/activationtime', 0.006)
session.daq_server.set('/dev32271/tu/thresholds/0/deactivationtime', 0.003)
session.daq_server.set('/dev32271/tu/logicunits/0/inputs/0/not', 1)

# Second paragraph in Cemil's notes
session.daq_server.set('/dev32271/auxouts/0/outputselect', 13)
session.daq_server.set('/dev32271/auxouts/0/scale', -3)
session.daq_server.set('/dev32271/auxouts/0/limitlower', -2)
session.daq_server.set('/dev32271/auxouts/0/limitupper', 0)

# Third paragraph in Cemil's notes
session.daq_server.set('/dev32271/sigouts/0/add', 1)

# Fourth paragraph in Cemil's notes
session.daq_server.set('/dev32271/imps/0/freq', 501000)
session.daq_server.set('/dev32271/imps/0/mode', 1)
session.daq_server.set('/dev32271/imps/0/maxbandwidth', 10000)

# Device definition and relatd commands
# Check connected devices
dev = session.devices

# Coonect 
device = session.connect_device('dev32271')

device.demods[0].enable(True)
device.imps[0].enable(True)

device.demods[0].sample.subscribe()
dataDemods = session.poll()
device.demods[0].sample.unsubscribe()

device.imps[0].sample.subscribe()
dataImps = session.poll()
device.imps[0].sample.unsubscribe()

plt.plot(dataImps[device.imps[0].sample]['timestamp'],dataImps[device.imps[0].sample]['param0'])
plt.plot(dataImps[device.imps[0].sample]['timestamp'],dataImps[device.imps[0].sample]['param1'])

# daq.set('/dev32271/system/shutdown', 1)


# #subscription and set up trigger for measurement
# mfli.daq.signals_clear()
# #add the 2nd parameter of impedance, 
# #default Cp, as the only signal of interest
# imp_param1 = mfli.daq.signals_add('imp0','param1') 
# mfli.daq.type('edge') #set edge trigger mode, default, rise 
# #change to your device number
# mfli.daq.triggernode('/DEV4562/imps/0/sample.param1') 
# mfli.daq.findlevel(1) #automatic search for level
# #500 is arbitraty chosen. 
# #The duration by default equals to 500Sa/13kSa/s=38ms
# mfli.daq.grid_cols(500) 
# mfli.daq.measure() #start the daq module

# #save data for plotting
# result = mfli.daq.results[imp_param1]
# plt.plot(result.time, result.value[0])
# plt.xlabel('Time (s)')
# plt.ylabel('Capacitance (F)')
# plt.title("Transient capacitance")