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
import pandas as pd

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

# Device definition and settings!!! 
device = session.connect_device('dev32271')

# odmrc.antennaNo = input("Please enter Antenna No: ")

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

# Device definition and related commands
# Check connected devices
dev = session.devices

# # Connect 
# device = session.connect_device('dev32271')

device.demods[0].enable(True)
device.imps[0].enable(True)

time.sleep(2)

device.demods[0].sample.subscribe()
dataDemods = session.poll()
device.demods[0].sample.unsubscribe()

device.imps[0].sample.subscribe()
dataImps = session.poll()
device.imps[0].sample.unsubscribe()

fig, ax = plt.subplots(ncols=2, nrows=2)
ax[0,0].plot(dataImps[device.imps[0].sample]['timestamp'],dataImps[device.imps[0].sample]['param0']) # Impedance (Re)
ax[0,1].plot(dataImps[device.imps[0].sample]['timestamp'],dataImps[device.imps[0].sample]['param1']) # Impedance (Im)
ax[1,0].plot(dataImps[device.imps[0].sample]['timestamp'],np.abs(dataImps[device.imps[0].sample]['z']))      # Abs(Z)
ax[1,1].plot(dataDemods[device.demods[0].sample]['timestamp'],dataDemods[device.demods[0].sample]['auxin0']) # Aux Input 1
# plt.plot(dataDemods[device.demods[0].sample]['timestamp'],dataDemods[device.demods[0].sample]['phase']) # Not sure!
# plt.plot(dataDemods[device.demods[0].sample]['timestamp'],dataDemods[device.demods[0].sample]['y']) # Not sure!
plt.show()
# # DO NOT SAVE multiple parameters in one file using the software. It
# # appends the first parameter data to second as as new rows. This
# # creates a confusion about where the old data finishes and where the
# # new data starts!!! 

# # Below is their new convention!!!!
# devs = list(device)
# pars = [0] * len(devs)
# for i in range(len(devs)):
#     pars[i] = devs[i][1]['Node'].split('/')[1:]

# pars = pd.DataFrame(pars)
# tabs = list(set(pars.iloc[:,1]))

# a = [list(device.tu)[i][1]['Options'] for i in range(len(list(device.tu))) 
#  if str(list(device.tu)[i][0])=='/dev32271/tu/thresholds/0/input']

# # a = list(device.tu)
# # a[0][0]
# # a[0][1].keys()
# # a[0][1]['Options']

# # There is a[1] and more....


