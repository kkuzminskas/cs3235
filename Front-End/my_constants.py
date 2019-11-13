from win32api import GetSystemMetrics

# Pin detection
MIN_TIME = 4800

# get the size of the screen
WIDTH = GetSystemMetrics(0)
HEIGHT =  GetSystemMetrics(1)
TOP = 70

# Connect w/ eye tribe
HOST = "localhost"
PORT = 6555
# MAX_LOOP = 600
MAX_LOOP = 10


# calibration
CHECK_CALIBRATION = {
    "category": "tracker",
    "request" : "get",
    "values": [ "push", "iscalibrated" ]
}
CALLIBRATION_EXE = "C:\Program Files (x86)\EyeTribe\Client\EyeTribeUIWin.exe"
