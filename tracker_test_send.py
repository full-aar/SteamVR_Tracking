import triad_openvr
import time
import sys

# For OSC
import argparse
from pythonosc import udp_client

v = triad_openvr.triad_openvr()
# v.print_discovered_objects()

# OSC
parser = argparse.ArgumentParser()
#parser.add_argument("--ip", default="192.168.86.12")
parser.add_argument("--ip", default="127.0.0.1")
parser.add_argument("--port", type=int, default=5005)
args = parser.parse_args()
client = udp_client.SimpleUDPClient(args.ip, args.port)


if len(sys.argv) == 1:
    interval = 1/250
elif len(sys.argv) == 2:
    interval = 1/float(sys.argv[1])
else:
    print("Invalid number of arguments")
    interval = False
    
if interval:
    while(True):
        start = time.time()
        txt = ""
        if (v.devices["tracker_1"].get_pose_quaternion()):
            for each in v.devices["tracker_1"].get_pose_quaternion():
                txt += "%.4f" % each
                txt += " "
            print("\r" + txt, end="")
            client.send_message("/pose", txt)    # Send OSC message
            sleep_time = interval-(time.time()-start)
            if sleep_time>0:
                time.sleep(sleep_time)
