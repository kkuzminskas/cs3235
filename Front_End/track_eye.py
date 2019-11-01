import time
import os
import socket
import sys
import json
import subprocess
import turtle
from my_constants import *

def get_data():

    # Create a socket (SOCK_STREAM means a TCP socket)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        a = 0
        f = open("test.txt", "w+")
        global RUNNING
        while RUNNING:
            # data = json.dumps(CHECK_CALIBRATION)
            data = " "
            sock.sendall(bytes(data + "\n", "utf-8"))

            # Receive data from the server and shut down
            received = str(sock.recv(2048), "utf-8")
            
            # print("Sent:     {}".format(data))
            # print("Received: {}".format(received))
            f.write(received)
            if a > MAX_LOOP:
                break;
            a+=1
    print(a)
    print("closed")
    f.close()

