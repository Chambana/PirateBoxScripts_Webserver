from dronekit_sitl import SITL
from pymavlink import mavutil
import math, time
from dronekit import LocationGlobal
from HTMLParser import HTMLParser
import time
from dronekit import connect, VehicleMode
from multiprocessing import Process

#/opt/piratebox/www/cgi-bin/data.pso
#datafilename = os.environ["SHOUTBOX_CHATFILE"]

class MyHTMLParser(HTMLParser):
    saved = list()
    def handle_starttag(self, tag, attrs):
        #print "Encountered a start tag:", tag
        pass
    def handle_endtag(self, tag):
        #print "Encountered an end tag :", tag
        #print self.saved
        pass
    def handle_data(self, data):
        #print "Encountered some data  :", data
        if data!=' ':
            self.saved.append(data)
def condition_yaw(heading, relative=False):
    print "DEBUG:  sending yaw commmand with heading", heading
    if relative:
        is_relative=1 #yaw relative to direction of travel
    else:
        is_relative=0 #yaw is an absolute angle
    # create the CONDITION_YAW command using command_long_encode()
    msg = vehicle.message_factory.command_long_encode(
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_CMD_CONDITION_YAW, #command
        0, #confirmation
        heading,    # param 1, yaw in degrees
        0,          # param 2, yaw speed deg/s
        1,          # param 3, direction -1 ccw, 1 cw
        is_relative, # param 4, relative offset 1, absolute angle 0
        0, 0, 0)    # param 5 ~ 7 not used
    # send command to vehicle
    vehicle.send_mavlink(msg)
def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print "Basic pre-arm checks"
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print " Waiting for vehicle to initialise..."
        time.sleep(1)

    print "Arming motors"
    # Copter should arm in GUIDED mode
    vehicle.mode    = VehicleMode("GUIDED")
    vehicle.armed   = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print " Waiting for arming..."
        time.sleep(1)

    print "Taking off!"
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print " Altitude: ", vehicle.location.global_relative_frame.alt
        #Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95:
            print "Reached target altitude"
            break
        time.sleep(1)
def setup_aircraft():
    vehicle.mode=VehicleMode("GUIDED")
    time.sleep(3)
    arm_and_takeoff(3)
    time.sleep(3)
    #vehicle.simple_goto(LocationGlobal(-34.364114, 149.166022, 30))
    print "Initial yaw=", math.degrees(vehicle._yaw)
def check_for_uav_command(line):
    for entry in line:
       if entry.lower() == "turn right":
           print "Found a Turn Right Chat Command!"
           condition_yaw(heading=15, relative=True)
       if entry.lower() == "turn left":
           print "Found a Turn Left Chat Command!"
           condition_yaw(heading=345, relative=True)
def chatroom_scanner():
    last_parsed_timestamp = None
    parser = MyHTMLParser()
    # read 1 line (the first line) and check it against the timestamp to see if new
    try:
        while 1:
            print "yaw=", math.degrees(vehicle._yaw)
            chatfile = open("./data.txt", 'r')
            buf = chatfile.readline()
            print buf

            parser.feed(buf)
            if parser.saved[0]!=last_parsed_timestamp:
                print "saving new timestamp", parser.saved[0]
                last_parsed_timestamp=parser.saved[0]
                check_for_uav_command(parser.saved)
            else:
                print "No New Chat Data"
                time.sleep(1)
            chatfile.close()
            parser.saved=None
            parser.saved=list()
    except Exception, e:
        print "Exception in file read loop",str(e)

print "Connecting to vehicle on: 'udp:127.0.0.1:14551'"
vehicle = connect('udp:127.0.0.1:14551', wait_ready=True)
setup_aircraft()

proc = Process(target=chatroom_scanner, args=())
proc.start()
#p.join()

print "RETURN TO MAIN EXECUTION"




#EXTRA

# Close vehicle object before exiting script
#vehicle.close()

# print "Start simulator (SITL)"
#
# sitl = SITL()
# sitl.download('copter', '3.3', verbose=True)
# sitl_args = ['-I0', '--model', 'quad', '--home=-35.363261,149.165230,584,353']
# sitl.launch(sitl_args, await_ready=True, restart=True)

# Import DroneKit-Python

# while 1:
#     yaw_direction = raw_input('Type left or right to yaw UAV: ')
#     if yaw_direction=='right':
#         condition_yaw(heading=15, relative=True)
#     elif yaw_direction=='left':
#         condition_yaw(heading=345, relative=True)
#     else:
#         print "invalid input"
#
#     print "yaw=", math.degrees(vehicle._yaw)

# Get some vehicle attributes (state)
# print "Get some vehicle attribute values:"
# print " GPS: %s" % vehicle.gps_0
# print " Battery: %s" % vehicle.battery
# print " Last Heartbeat: %s" % vehicle.last_heartbeat
# print " Is Armable?: %s" % vehicle.is_armable
# print " System status: %s" % vehicle.system_status.state
# print " Mode: %s" % vehicle.mode.name    # settable
# Shut down simulator
#sitl.stop()
#print("Completed")