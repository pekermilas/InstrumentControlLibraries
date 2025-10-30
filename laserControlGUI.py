# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 18:34:02 2025

@author: OzturkLab
"""

import numpy as np
import matplotlib.pyplot as plt
import time
import matplotlib.animation as animation
import glob
import ctypes
import sys

from pomegranate import *

# import cryoMicConfig as cmc
# import spectraTools
# import LaserControl
# import ASEQControl as asq

import tkinter as tk
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import civilLaserControl as cvlc

def getScanStage():
    if cmc.textlinecount>10:
        cmc.textbox.delete("1.0", END)
        cmc.textlinecount=0

    stage = cmc.stageSelection.get()
    if stage:
        if stage=='Stepper':
            cmc.textbox.insert(END, 'Selected stage: '+stage + '\n')
            cmc.textlinecount+=1
            cmc.scanStage = 0
        if stage=='Piezo':
            cmc.textbox.insert(END, 'Selected stage: '+stage + '\n')
            cmc.textlinecount+=1
            cmc.scanStage = 1
    else:
        errMessg = 'Default stage is (Stepper) selected'
        cmc.textbox.insert(END, errMessg + '\n')
        # cmc.textbox.insert('1.0', errMessg + '\n')
        cmc.textlinecount+=1
        cmc.scanStage = 0

    return 0

root = tk.Tk()
root.geometry("300x300")
tabControl = ttk.Notebook(root)

    
stageSelection = tk.ttk.Combobox(root, width="20", font=("Segoe UI", 14))
stageSelection["values"] = ["Red","Green", "Blue"]
stageSelection.current(0)
stageSelection.grid(row=0, column=0, padx=4, pady=20)
# stageSelectionButton = tk.Button(root, text='Select scan stage', font=("Segoe UI", 14), 
                                 # bd=1, command=getScanStage)
stageSelectionButton = tk.Button(root, text='Select scan stage', font=("Segoe UI", 14), 
                                 bd=1)
stageSelectionButton.grid(row=1, column=0, padx=4, pady=0)


laser = cvlc.civilLaser()
laser.open()

def on_closing():
    laser.runLaser()
    laser.close()
    root.destroy()
    # sys.stdout.write = sys.stdout.write
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

# cmc.on = PhotoImage(file='on.PNG')
# cmc.off = PhotoImage(file='off.PNG')
# cmc.onArduino = PhotoImage(file='onArduino.PNG')
# cmc.offArduino = PhotoImage(file='offArduino.PNG')
# cmc.textlinecount = 0

# # Stage Manual Operation Tab
# cmc.moveTab = ttk.Frame(cmc.tabControl)
# mvT.construct_moveTab()