This program controls a VID28 step motor connected directly to a Raspberry Pico with a microPython program.
The 2 axes are connected to needles. The needles contains a small magnet for callibration with a reed switch.
The code is in my repository 'motorvid28.py' and can be tested with 'motorvid28-test.py'
The schematic is Pico-vid28.pdf and the datasheet in Vid28.pdf  

To move the motors there is several levels , top / Dow :  
1 : The class motorVid28() with instances for two needles (BN end SN). To initiate the class :  
1.1 : Definition of the pins used by the motor. Note that pins B and C receive same data BUT must be connected to 2 pins (for power).  
1.2 : The SEQUENCE of pulses sent to the pins according to the datasheet  
1.3 : The timing TIMEPULSE and TIMESTEP.  
1.4 : The number od steps corresponding to 360°. Only 180 steps for direct control. 720 with a driver like VID66 (not used)  
1.5 : Pin used by the reed switches for calibration  
2 : The method moveSteps() to move a number of steps (ex 45 for 90°)  
3 : The method moveOneStep() to move one step according to the SEQUENCE  
4 : The method _motorcontrol() sending the pulses to the motor  
5 : The method calibrateNeedle() to move steps until the reed switch sense the magnet of the needle
 
