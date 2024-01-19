I'm trying to control a VID28 step motor connected directly to a Raspberry Pico with a microPython program.
The 2 axes are connected to needles. The needles contains a small magnet for callibration with a reed switch.
The code is in my repository 'motorvid28.py'

It's working correctly but there is a bug ! The motor miss some steps.
I tried different values of time for the pulses and for the interval between steps. It's better at low speed but not perfect.
The most probable reason is the power. The motor ask for a min of 3.5v and Pico delivers at best 3.3v, thus not enough torque.
I could add a chip (vid66 or equivalent) to have a separate power suply for the motor but given it's almost good, I keep trying with the code. Furthermore, the wiring is very simple when it's directly from Pico to Vid28 and the cost is really low.

Well I see that you use mostly Arduino and C (with a cool library stepper.h) but may be someone have an idea to solve my problem...

