# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 18:34:02 2025

@author: OzturkLab
"""

import numpy as np
import matplotlib.pyplot as plt
import time
import platform

import tkinter as tk
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

import civilLaserControl as cvlc


class CustomSpinbox(tk.Spinbox):
    def __init__(self, master=None, **kwargs):
        tk.Spinbox.__init__(self, master, **kwargs)
        # Bind mouse wheel events
        self.bind('<MouseWheel>', self.mouseWheel)
        # Linux/X11 bindings
        self.bind('<Button-4>', self.mouseWheel)
        self.bind('<Button-5>', self.mouseWheel)

    def mouseWheel(self, event):
        # Platform-specific logic for direction and delta
        if platform.system() == 'Windows':
            if event.delta > 0:
                self.invoke('buttonup')
            else:
                self.invoke('buttondown')
        elif platform.system() == 'Darwin': # macOS
            if event.delta > 0:
                self.invoke('buttonup')
            else:
                self.invoke('buttondown')
        else: # Linux/X11
            if event.num == 4:
                self.invoke('buttonup')
            elif event.num == 5:
                self.invoke('buttondown')
       
        # Optional: You can also call a command associated with the Spinbox here
        # if 'command' in self.config():
        #     self.config()['command']()

def on_spinbox_change(*args):
    # This function is called when the Spinbox value changes
    # You can get the value and perform immediate updates here
    global redPower
    global greenPower
    global bluePower
    global laserPower
    global laserState
    laserPowerOld = np.array([redPower,greenPower,bluePower])
    redPower = currentRedPower.get()
    greenPower = currentGreenPower.get()
    bluePower = currentBluePower.get()
    laserPowerNew = np.array([redPower,greenPower,bluePower])
    laserPower = np.array([redPower,greenPower,bluePower])
    
    if not (laserPowerOld==laserPowerNew).all():
        laserButton.config(image=update)
    return 0

def laserRun():
    global laserPower
    global laserState
    print(laserPower)
    laserState = [1 if int(i)>0 else 0 for i in laserPower]
    laser.laserPower = laserPower
    if sum(laserState)==0:
        laserButton.config(image=off)
    else:
        laserButton.config(image=on)
        
    laser.runLaser()
    return 0

def resizeImage(image, w = 50, h = 50):
    img = Image.open(image)
    img = img.resize((w,h))
    return img

root = tk.Tk()
root.geometry("300x300")
tabControl = ttk.Notebook(root)

on = ImageTk.PhotoImage(resizeImage('toggleON.png', 80,80))
off = ImageTk.PhotoImage(resizeImage('toggleOFF.png', 80,80))
update = ImageTk.PhotoImage(resizeImage('toggleRefresh.png', 80,80))

laser = cvlc.civilLaser()
laser.open()

redPower = 0
greenPower = 0
bluePower = 0
laserPower = np.zeros(3)
laserState = [0,0,0]

currentRedPower = tk.StringVar(value=0)
redSpinbox = CustomSpinbox(root, from_=0, to=255, textvariable=currentRedPower, 
                         wrap=True, font=("Segoe UI", 24), width=10,
                         command=on_spinbox_change)
redSpinbox.grid(row=1, column=1, padx=55, pady=10)

currentGreenPower = tk.StringVar(value=0)
greenSpinbox = CustomSpinbox(root, from_=0, to=255, textvariable=currentGreenPower, 
                         wrap=True, font=("Segoe UI", 24), width=10,
                         command=on_spinbox_change)
greenSpinbox.grid(row=2, column=1, padx=55, pady=10)

currentBluePower = tk.StringVar(value=0)
blueSpinbox = CustomSpinbox(root, from_=0, to=255, textvariable=currentBluePower, 
                         wrap=True, font=("Segoe UI", 24), width=10,
                         command=on_spinbox_change)
blueSpinbox.grid(row=3, column=1, padx=55, pady=10)

laserButton = tk.Button(root, image=off, bd=0, command=laserRun)
laserButton.grid(row=4, column=1)

def on_closing():
    laser.runLaser()
    laser.close()
    root.destroy()
    # sys.stdout.write = sys.stdout.write
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()







# root = tk.Tk()
# root.title("Spinbox Mouse Wheel Update")

# spinbox_var = tk.StringVar(value=0) # Use a StringVar to easily track changes

# # Create an instance of the custom spinbox
# spinbox = CustomSpinbox(root, from_=0, to=100, increment=1, textvariable=spinbox_var, command=on_spinbox_change)
# spinbox.pack(pady=20)

# root.mainloop()
