from main import *
import time

# enable maxon motor
enable_epos()

while True:
    go_to_position(17000)
    time.sleep(0.5)
    go_to_position(-17000)
    time.sleep(0.5)