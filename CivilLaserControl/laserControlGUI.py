# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 18:34:02 2025

@author: OzturkLab
"""

import numpy as np
import matplotlib.pyplot as plt
import time

import tkinter as tk
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

import civilLaserControl as cvlc


def laserRun(laserIndex):
    laser.runLaser()
    if laser.getLaserPower()>0:
        if int(laser.getLaserIndex())==0:
            redLaserButton.config(image=onRed)
        if int(laser.getLaserIndex())==1:
            greenLaserButton.config(image=onGreen)
        if int(laser.getLaserIndex())==2:
            blueLaserButton.config(image=onBlue)
    else:
        if int(laser.getLaserIndex())==0:
            redLaserButton.config(image=off)
        if int(laser.getLaserIndex())==1:
            greenLaserButton.config(image=off)
            print(laser.getLaserPower())
        if int(laser.getLaserIndex())==2:
            blueLaserButton.config(image=off)
            print(laser.getLaserPower())
        
    return 0

def valueChanged(lIndex):
    if lIndex==0:
        laser.setLaser(0,int(currentRedPower.get()))
    if lIndex==1:
        laser.setLaser(1,int(currentGreenPower.get()))
    if lIndex==2:
        laser.setLaser(2,int(currentBluePower.get()))

    return 0

def resizeImage(image, w = 50, h = 50):
    img = Image.open(image)
    img = img.resize((w,h))
    return img

root = tk.Tk()
root.geometry("300x300")
tabControl = ttk.Notebook(root)

onRed = ImageTk.PhotoImage(resizeImage('toggleOnRed_128.png', 100,90))
onGreen = ImageTk.PhotoImage(resizeImage('toggleOnGreen_128.png', 100,90))
onBlue = ImageTk.PhotoImage(resizeImage('toggleOnBlue_128.png', 100,90))
off = ImageTk.PhotoImage(resizeImage('toggleOff_128.png', 100,90))


laser = cvlc.civilLaser()
laser.open()

redLaserButton = tk.Button(root, image=off, bd=0, command=lambda: laserRun(0))
redLaserButton.grid(row=1, column=0)
greenLaserButton = tk.Button(root, image=off, bd=0, command=lambda: laserRun(1))
greenLaserButton.grid(row=2, column=0)
blueLaserButton = tk.Button(root, image=off, bd=0, command=lambda: laserRun(2))
blueLaserButton.grid(row=3, column=0)

currentRedPower = tk.StringVar(value=0)
redSpinbox = ttk.Spinbox(root, from_=0, to=255, textvariable=currentRedPower, 
                         wrap=True, font=("Segoe UI", 24), width=10, 
                         command=lambda: valueChanged(0))
redSpinbox.grid(row=1, column=1)

currentGreenPower = tk.StringVar(value=0)
greenSpinbox = ttk.Spinbox(root, from_=0, to=255, textvariable=currentGreenPower, 
                         wrap=True, font=("Segoe UI", 24), width=10, 
                         command=lambda: valueChanged(1))
greenSpinbox.grid(row=2, column=1)

currentBluePower = tk.StringVar(value=0)
blueSpinbox = ttk.Spinbox(root, from_=0, to=255, textvariable=currentBluePower, 
                         wrap=True, font=("Segoe UI", 24), width=10, 
                         command=lambda: valueChanged(2))

blueSpinbox.grid(row=3, column=1)


def on_closing():
    laser.runLaser()
    laser.close()
    root.destroy()
    # sys.stdout.write = sys.stdout.write
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
