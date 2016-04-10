import subprocess
import time

def run_camera_controller():
    subprocess.Popen("/opt/vc/bin/raspistill -o /opt/piratebox/www/drone.jpg -t 21600000 -tl 1000 -w 320 -h 240", shell=True)

