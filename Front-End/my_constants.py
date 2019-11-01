from win32api import GetSystemMetrics

# Pin detection
MIN_TIME = 4800

# get the size of the screen
WIDTH = GetSystemMetrics(0)
HEIGHT =  GetSystemMetrics(1)
TOP = 10

# Connect w/ eye tribe
HOST = "localhost"
PORT = 6555
# MAX_LOOP = 600
MAX_LOOP = 600


# calibration
CHECK_CALIBRATION = {
    "category": "tracker",
    "request" : "get",
    "values": [ "push", "iscalibrated" ]
}