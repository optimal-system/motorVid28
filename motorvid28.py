"""
motorvid28.py - Optimal System (O.Moreau)
=====================================
Code for Raspberry Pico using Micropython

Control of a stepping motor VID28-05 (or BKA30D-R5) with 2 coax shafts and 2 needles
Each motor has 4 pins connected to the Pico (A,B,C,D).
plus 1 pin for calibration with 2 Reed Switches (normally Open)
"""
__version__ = 1.240123

import time
from machine import Pin

class motorVid28() :
    
    def __init__(self,pins) : 
        self.A         = Pin(pins[0],Pin.OUT,0)
        self.B         = Pin(pins[1],Pin.OUT,0)
        self.C         = Pin(pins[2],Pin.OUT,0)
        self.D         = Pin(pins[3],Pin.OUT,0)
        self.SWITCH    = Pin(pins[4],Pin.IN,Pin.PULL_UP)
        self.TIMEPULSE = 6    # in milliseconds. Must be between 3 and 10
        self.TIMESTEP  = 0    # optional to slow down movement
        self.STEPS     = 180  # only 180 steps when direct control by Pico
        self.SEQUENCE  = [    # according to datasheet. Pin B anc C get same pulses
                [1, 0, 1],
                [0, 0, 1],
                [0, 1, 1],
                [0, 1, 0],
                [1, 1, 0],
                [1, 0, 0],
                [0, 0, 0],
                ]
        self.LENSEQ = len(self.SEQUENCE)-1
        self.CW  = 1
        self.CCW = 0

    def _motorcontrol(self,pulse):
        self.A.value(pulse[0])
        self.B.value(pulse[1])
        self.C.value(pulse[1])
        self.D.value(pulse[2])
        time.sleep_ms(self.TIMEPULSE)

    def moveOneStep(self,direction):
        for i in range(self.LENSEQ):
            if   direction == self.CW :
                self._motorcontrol(self.SEQUENCE[i])
            elif direction == self.CCW :
                self._motorcontrol(self.SEQUENCE[self.LENSEQ-1-i])

    def moveSteps(self, direction, steps):
        for i in range(steps) :
            self.moveOneStep(direction)
        time.sleep_ms(self.TIMESTEP) # 

    def calibrateNeedle(self,direction,adjust=0,name="") :
        nv = self.SWITCH.value()
        if nv == 0 :
            self.moveSteps(direction, self.STEPS/4) # Move out of Reed switch zone before recalibration
        for i in range (self.STEPS) :
            nv = self.SWITCH.value()
            if nv == 1 :
                self.moveSteps(direction, 1)  # Keep moving until the Reed switch is detected
            elif nv == 0 :
                self.moveSteps(direction, adjust) # Optinal adjustment of the needle to reach a starting position
                self.stop()
                break
            
    def stop(self) :
        self._motorcontrol(self.SEQUENCE[6])
        time.sleep_ms(self.TIMEPULSE)

