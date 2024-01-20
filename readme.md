I'm trying to control a VID28 step motor connected directly to a Raspberry Pico with a microPython program.
The 2 axes are connected to needles. The needles contains a small magnet for callibration with a reed switch.
The code is in my repository 'motorvid28.py'

It's working correctly but there is a bug ! The motor miss some steps.
I tried different values of time for the pulses and for the interval between steps. It's better at low speed but not perfect.
The most probable reason is the power. The motor ask for a min of 3.5v and Pico delivers at best 3.3v, thus not enough torque.
I could add a chip (vid66 or equivalent) to have a separate power suply for the motor but given it's almost good, I keep trying with the code. Furthermore, the wiring is very simple when it's directly from Pico to Vid28 and the cost is really low.

To move the motors there is several levels , top / Dow :
1 : The class motorVid28() with instances for two needles (BN end SN). To initiate the class :
1.1 : Definition of the pins used by the motor. Note that pins B and C are connected
1.2 : The SEQUENCE of pulses sent to the pins according to the datasheet of Vid28
1.3 : The timing TIMEPULSE and TIMESTEP. There is also TIMESTOP but not important
1.4 : The number od steps corresponding to 360°. Only 180 steps for direct control. 720 with a driver like VID66 (not used)
1.5 : Pin used by the reed switches for calibration
2 : The method moveSteps() to move a number of steps (ex 45 for 90°)
3 : The method moveOneStep() to move one step according to the SEQUENCE
4 : The method _motorcontrol() sending the pulses to the motor
5 : The method calibrateNeedle() to move steps until the reed switch sense the magnet of the needle

The critical part is the timing. Very different results occurs by slightly changing  TIMEPULSE and TIMESTEP
    TIMEPULSE = 1ms TIMESTEP = 1ms : Very fast moves but not reliable
    TIMEPULSE = 5ms TIMESTEP = 1ms : Fast but missing steps once in a while
    TIMEPULSE = 1ms TIMESTEP = 5ms : Very fast but not reliable at all
    TIMEPULSE = 5ms TIMESTEP = 5ms : Fair speed but still missing steps
    TIMEPULSE = 10ms TIMESTEP = 1ms : Fair speed but missing many steps
    TIMEPULSE = 10ms TIMESTEP = 5ms : Slow but missing many steps
    TIMEPULSE = 15ms TIMESTEP = 5ms : Very slow and painfull !
    TIMEPULSE = 7ms TIMESTEP = 2ms : So far the best

The inner shaft (BN) is giving mor problems than the outer shaft (SN).    
