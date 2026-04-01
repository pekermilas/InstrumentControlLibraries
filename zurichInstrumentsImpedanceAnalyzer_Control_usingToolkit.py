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

# Device definition and related commands
# Check connected devices
dev = session.devices

# Coonect 
device = session.connect_device('dev32271')

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

# sample_nodes = [
#     device.demods[0].sample.auxin0,
#     device.imps[0].sample.param0,
#     device.imps[0].sample.param1,
#     device.imps[0].sample.z
# ]

# TOTAL_DURATION = 5 # [s]
# SAMPLING_RATE = 30000 # Number of points/second
# BURST_DURATION = 0.2 # Time in seconds for each data burst/segment.

# num_cols = int(np.ceil(SAMPLING_RATE * BURST_DURATION))
# num_bursts = int(np.ceil(TOTAL_DURATION / BURST_DURATION))

# daq_module = session.modules.daq
# daq_module.device(device)
# daq_module.type(0) # continuous acquisition
# daq_module.grid.mode(2)
# daq_module.count(num_bursts)
# daq_module.duration(BURST_DURATION)
# daq_module.grid.cols(num_cols)

# daq_module.save.fileformat(1)
# daq_module.save.filename('zi_toolkit_acq_example')
# daq_module.save.saveonread(1)

# for node in sample_nodes:
#     daq_module.subscribe(node)
    
# clockbase = device.clockbase()


# def read_and_plot_data(daq_module, results, ts0):
#     daq_data = daq_module.read(raw=False, clk_rate=clockbase)
#     progress = daq_module.raw_module.progress()[0]
#     for node in sample_nodes:
#         # Check if node data available
#         if node in daq_data.keys():
#             for sig_burst in daq_data[node]:
#                 results[node].append(sig_burst)
#                 if np.any(np.isnan(ts0)):
#                   ts0 = sig_burst.header['createdtimestamp'][0] / clockbase
#                 # Convert from device ticks to time in seconds.
#                 t0_burst = sig_burst.header['createdtimestamp'][0] / clockbase
#                 t = (sig_burst.time + t0_burst) - ts0
#                 value = sig_burst.value[0, :]
#                 # Plot the data
#                 ax1.plot(t, value)
#                 ax1.set_title(f"Progress of data acquisition: {100 * progress:.2f}%.")
#                 fig.canvas.draw()
#                 plt.pause(0.001)
#     return results, ts0


# ts0 = np.nan
# timeout = 1.5 * TOTAL_DURATION
# start_time = time.time()
# results = {x: [] for x in sample_nodes}

# fig = plt.figure()
# ax1 = fig.add_subplot(111)
# ax1.set_xlabel("Time ($s$)")
# ax1.set_ylabel("Subscribed signals")
# ax1.set_xlim([0, TOTAL_DURATION])
# ax1.grid()

# # Start recording data
# daq_module.execute()

# while time.time() - start_time < timeout:
#     results, ts0 = read_and_plot_data(daq_module, results, ts0)
#     if daq_module.raw_module.finished():
#         # Once finished, call once more to get the potential remaining data.
#         results, ts0 = read_and_plot_data(daq_module, results, ts0)
#         break

#     time.sleep(BURST_DURATION)

# # daq.set('/dev32271/system/shutdown', 1)


# # #subscription and set up trigger for measurement
# # mfli.daq.signals_clear()
# # #add the 2nd parameter of impedance, 
# # #default Cp, as the only signal of interest
# # imp_param1 = mfli.daq.signals_add('imp0','param1') 
# # mfli.daq.type('edge') #set edge trigger mode, default, rise 
# # #change to your device number
# # mfli.daq.triggernode('/DEV4562/imps/0/sample.param1') 
# # mfli.daq.findlevel(1) #automatic search for level
# # #500 is arbitraty chosen. 
# # #The duration by default equals to 500Sa/13kSa/s=38ms
# # mfli.daq.grid_cols(500) 
# # mfli.daq.measure() #start the daq module

# # #save data for plotting
# # result = mfli.daq.results[imp_param1]
# # plt.plot(result.time, result.value[0])
# # plt.xlabel('Time (s)')
# # plt.ylabel('Capacitance (F)')
# # plt.title("Transient capacitance")