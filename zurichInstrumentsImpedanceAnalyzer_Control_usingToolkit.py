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
device.factory_reset()
# odmrc.antennaNo = input("Please enter Antenna No: ")

# First paragraph in Cemil's notes 
session.daq_server.set('/dev32271/tu/thresholds/0/input', 59)
session.daq_server.set('/dev32271/tu/thresholds/0/activationtime', 0.006)
session.daq_server.set('/dev32271/tu/thresholds/0/deactivationtime', 0.003)
session.daq_server.set('/dev32271/tu/logicunits/0/inputs/0/not', 1)

# Second paragraph in Cemil's notes
session.daq_server.set('/dev32271/auxouts/0/outputselect', 13)
session.daq_server.set('/dev32271/auxouts/0/scale', -2)
session.daq_server.set('/dev32271/auxouts/0/offset', -2)
session.daq_server.set('/dev32271/auxouts/0/limitlower', -10)
session.daq_server.set('/dev32271/auxouts/0/limitupper', 0)


# Third paragraph in Cemil's notes
session.daq_server.set('/dev32271/sigouts/0/add', 1)

# Fourth paragraph in Cemil's notes
session.daq_server.set('/dev32271/imps/0/freq', 501000)
session.daq_server.set('/dev32271/imps/0/mode', 1)
session.daq_server.set('/dev32271/imps/0/maxbandwidth', 10000)
session.daq_server.set('/dev32271/imps/0/auto/inputrange', 0)
session.daq_server.set('/dev32271/imps/0/current/range', 0.01)
session.daq_server.set('/dev32271/imps/0/voltage/range', 3)
session.daq_server.set('/dev32271/imps/0/omegasuppression', 80)
session.daq_server.set('/dev32271/imps/0/demod/rate', 60000)

session.daq_server.set('/dev32271/triggers/out/0/source', 36)
session.daq_server.set('/dev32271/imps/0/output/on', 1)

# session.daq_server.set('/dev32271/demods/0/trigger', 1)
# session.daq_server.set('/dev32271/scopes/0/enable', 1)
# session.daq_server.set('/dev32271/scopes/0/trigenable', 1)
# session.daq_server.set('/dev32271/scopes/0/trigrising', 1)
# session.daq_server.set('/dev32271/scopes/0/trigchannel', 14)

# Device definition and related commands
# Check connected devices
dev = session.devices

# # Connect 
# device = session.connect_device('dev32271')

# A module can be figured by checking the names on the ModuleHandler page
# https://docs.zhinst.com/zhinst-toolkit/en/latest/_autosummary/zhinst.toolkit.session.ModuleHandler.html#zhinst.toolkit.session.ModuleHandler
# For example: 
# using the link name create_pid_advisor_module()
# we can create pid advisor module as following
# pidAdvisor = session.modules.pid_advisor
# 
# A awg module for example, using the same logic will use
# the link with name create_awg_module()
# awg = session.modules.awg


# # Trigger tests
# t = session.daq_server.dataAcquisitionModule()
# t.read() # Reads the parameters
daq_module = session.modules.daq
# scope = session.modules.scope

daq_module.type(6)
daq_module.triggernode('/dev32271/demods/0/sample.TrigOut1')
# daq_module.triggernode('/dev32271/demods/0/sample.AuxIn0.avg')
# daq_module.triggernode('/dev32271/demods/0/sample.R.avg')
# daq_module.triggernode('/dev32271/imps/0/sample.Param0.avg')
# daq_module.triggernode('/dev32271/imps/0/sample.Param1.avg')
daq_module.clearhistory(1)
# daq_module.clearhistory(1)
daq_module.bandwidth(0)
daq_module.grid.cols(1024)
daq_module.grid.repetitions(1)
daq_module.endless(0)
device.imps[0].enable(True)
daq_module.subscribe('/dev32271/demods/0/sample.AuxIn0.avg')
daq_module.subscribe('/dev32271/demods/0/sample.R.avg')
daq_module.subscribe('/dev32271/imps/0/sample.Param0.avg') # ???
daq_module.subscribe('/dev32271/imps/0/sample.Param1.avg') # ???
daq_module.forcetrigger()
# daq_module.subscribe('/dev32271/demods/0/sample.*')
# daq_module.subscribe('/dev32271/imps/0/sample.*')
# daq_module.device.demods[0].sample.subscribe()
# daq_module.device.imps[0].sample.subscribe()
daq_module.execute()

data = daq_module.read()
print(list(data))

fig, ax1 = plt.subplots()
# Plot first set of data on ax1
x1 = list(data['/dev32271/imps/0/sample.param1.avg'][0])[-3]
y1 = list(data['/dev32271/imps/0/sample.param1.avg'][0])[-4][0]

ax1.plot(x1,y1, 'g-')
# ax1.set_xlabel('X-axis Data')
# ax1.set_ylabel('Primary Y-axis (Quadratic)', color='g')
# ax1.tick_params(axis='y', labelcolor='g')

ax2 = ax1.twinx()

# Plot second set of data on ax2
x2 = list(data['/dev32271/demods/0/sample.auxin0.avg'][0])[-3]
y2 = list(data['/dev32271/demods/0/sample.auxin0.avg'][0])[-4][0]
ax2.plot(x2,y2, 'b-')
# ax2.set_ylabel('Secondary Y-axis (Linear)', color='b')
# ax2.tick_params(axis='y', labelcolor='b')

daq_module.unsubscribe('*')

# # Check command_table in command_table.py

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

# Disconnect from the device !!! 
device = session.disconnect_device('dev32271')
