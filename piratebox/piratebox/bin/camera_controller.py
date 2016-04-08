import subprocess
import time

def run_camera_controller():
    subprocess.Popen("/opt/vc/bin/raspistill -o /opt/piratebox/share/Shared/drone_pic.jpg -t 21600000 -tl 1000", shell=True)

