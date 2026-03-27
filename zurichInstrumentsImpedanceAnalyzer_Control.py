import time
import zhinst.core
import zhinst.ziPython as zi
import matplotlib.pyplot as plt

discovery = zi.ziDiscovery()
device_id = discovery.find('dev32271')
device_props = discovery.get(device_id)
daq = zi.ziDAQServer(device_props['serveraddress'], 
                     device_props['serverport'], 
                     device_props['apilevel'], 
                     allow_version_mismatch=True)


# First paragraph in Cemil's notes 
daq.set('/dev32271/tu/thresholds/0/input', 59)
daq.set('/dev32271/tu/thresholds/0/activationtime', 0.006)
daq.set('/dev32271/tu/thresholds/0/deactivationtime', 0.003)
daq.set('/dev32271/tu/logicunits/0/inputs/0/not', 1)

# Second paragraph in Cemil's notes
daq.set('/dev32271/auxouts/0/outputselect', 13)
daq.set('/dev32271/auxouts/0/scale', -3)
daq.set('/dev32271/auxouts/0/limitlower', -2)
daq.set('/dev32271/auxouts/0/limitupper', 0)

# Third paragraph in Cemil's notes
daq.set('/dev32271/sigouts/0/add', 1)

# Fourth paragraph in Cemil's notes
daq.set('/dev32271/imps/0/freq', 501000)
daq.set('/dev32271/imps/0/mode', 1)
daq.set('/dev32271/imps/0/maxbandwidth', 10000)

# Fifth paragraph in Cemil's notes




# daq = zhinst.core.ziDAQServer('192.168.176.30', 8004, 6, allow_version_mismatch=True)
# # Starting module impedanceModule on 2026/03/24 16:50:40
# impedance = daq.impedanceModule()
# impedance.set('device', 'dev32271')
# impedance.set('mode', 5)
# impedance.set('path', 'C:\\Users\\pekermilas\\AppData\\Roaming\\Zurich Instruments\\LabOne\\WebServer\\setting')
# impedance.execute()
# # To read the acquired data from the module, use a
# # while loop like the one below. This will allow the
# # data to be plotted while the measurement is ongoing.
# # Note that any device nodes that enable the streaming
# # of data to be acquired, must be set before the while loop.
# # result = 0
# # while impedance.progress() < 1.0 and not impedance.finished():
# #     time.sleep(1)
# #     result = impedance.read()
# #     print(f"Progress {float(impedance.progress()[0]) * 100:.2f} %\r")
# impedance.set('validation', 1)
# impedance.set('filename', 'last_compensation')
# impedance.set('filename', 'last_compensation')
# # Starting module sweep on 2026/03/24 16:50:40
# sweeper = daq.sweep()
# sweeper.set('device', 'dev32271')
# sweeper.set('xmapping', 1)
# sweeper.set('historylength', 100)
# sweeper.set('settling/inaccuracy', 0.01)
# sweeper.set('averaging/sample', 20)
# sweeper.set('averaging/tc', 15)
# sweeper.set('averaging/time', 0.1)
# sweeper.set('bandwidth', 10)
# sweeper.set('maxbandwidth', 100)
# sweeper.set('bandwidthoverlap', 1)
# sweeper.set('omegasuppression', 80)
# sweeper.set('order', 8)
# sweeper.set('gridnode', '/dev32271/oscs/0/freq')
# sweeper.set('save/directory', 'C:\\Users\\pekermilas\\Documents\\Zurich Instruments\\LabOne\\WebServer')
# sweeper.set('averaging/sample', 20)
# sweeper.set('averaging/tc', 15)
# sweeper.set('averaging/time', 0.1)
# sweeper.set('bandwidth', 10)
# sweeper.set('bandwidthoverlap', 1)
# sweeper.set('start', 1000)
# sweeper.set('stop', 1000000)
# sweeper.set('maxbandwidth', 100)
# sweeper.set('omegasuppression', 80)
# sweeper.set('order', 8)
# sweeper.set('stop', 1000000)
# daq.set('/dev32271/sigouts/0/add', 0)
# daq.set('/dev32271/sigouts/0/add', 1)
# daq.set('/dev32271/imps/0/confidence/qfactor/enable', 1)
# daq.set('/dev32271/imps/0/confidence/suppression/enable', 0)
# daq.set('/dev32271/imps/0/confidence/compensation/enable', 0)
# daq.set('/dev32271/imps/0/confidence/lowdut2t/enable', 0)
# daq.set('/dev32271/imps/0/confidence/opendetect/enable', 0)
# daq.set('/dev32271/imps/0/confidence/underflow/enable', 0)
# daq.set('/dev32271/imps/0/confidence/overflow/enable', 0)
# daq.set('/dev32271/imps/0/confidence/freqlimit/enable', 0)
# daq.set('/dev32271/imps/0/confidence/qfactor/enable', 0)
# daq.set('/dev32271/imps/0/confidence/oneperiod/enable', 0)
# daq.set('/dev32271/imps/0/bias/enable', 1)
# daq.set('/dev32271/tu/logicunits/0/inputs/0/not', 1)
# daq.set('/dev32271/tu/thresholds/0/deactivationtime', 0.001)
# daq.set('/dev32271/auxouts/0/scale', -2)
# daq.set('/dev32271/imps/0/ac', 1)
# daq.set('/dev32271/imps/0/ac', 0)
# daq.set('/dev32271/system/extclk', 1)
# daq.set('/dev32271/imps/0/freq', 1000000)
# # daq.set('/dev32271/auxouts/0/scale', nan)
# daq.set('/dev32271/auxouts/0/scale', -1)
# daq.set('/dev32271/imps/0/mode', 1)
# daq.set('/dev32271/imps/0/mode', 0)
# daq.set('/dev32271/imps/0/mode', 1)
# daq.set('/dev32271/imps/0/mode', 0)
# daq.set('/dev32271/imps/0/mode', 1)
# daq.set('/dev32271/imps/0/freq', 10000)
# daq.set('/dev32271/imps/0/freq', 500000)
# daq.set('/dev32271/imps/0/freq', 1000000)
# daq.set('/dev32271/imps/0/maxbandwidth', 1000)
# daq.set('/dev32271/imps/0/maxbandwidth', 10)
# daq.set('/dev32271/imps/0/maxbandwidth', 10000)
# daq.set('/dev32271/tu/thresholds/0/activationtime', 0.004)
# daq.set('/dev32271/tu/thresholds/0/deactivationtime', 0.002)
# daq.set('/dev32271/auxouts/0/scale', -2)
# daq.set('/dev32271/auxouts/0/scale', -1)
# daq.set('/dev32271/tu/thresholds/0/activationtime', 6)
# daq.set('/dev32271/tu/thresholds/0/deactivationtime', 2)
# daq.set('/dev32271/tu/thresholds/0/activationtime', 0.006)
# daq.set('/dev32271/tu/thresholds/0/deactivationtime', 0.002)
