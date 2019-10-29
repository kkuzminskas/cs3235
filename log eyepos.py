import random
import constants
from pygaze import libscreen
from pygaze import libtime
from pygaze import liblog
from pygaze import libinput
from pygaze import eyetracker

# start timing
libtime.expstart()

# create display object
disp = libscreen.Display()

# create eyetracker object
tracker = eyetracker.EyeTracker(disp, trackertype='eyetribe')

# create keyboard object

# create logfile object
log = liblog.Logfile()

# create screens
inscreen = libscreen.Screen()
inscreen.draw_text(text="Recording data", fontsize=24)

# # # # #
# run the experiment

# calibrate eye tracker
# tracker.calibrate()

# show instructions
disp.fill(inscreen)
disp.show()

tracker.start_recording()

while (True):
    # get gaze position
    gazePos = tracker.sample()
    currTime = libtime.get_time()/100
    tracker.log("time: %d gaze pos x %d gaze pos y %d" % (currTime, gazePos[0], gazePos[1]))

# end the experiment
log.close()
tracker.close()
disp.close()
libtime.expend()
