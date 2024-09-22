from epos_setup import *
from main import *
import time
import threading

mode = 1    # 0 = got_to_position, 1 = move_to_position

# enable maxon motor
#epos_1, keyhandle_1, NodeID_1, pErrorCode_1, pDeviceErrorCode_1 = epos_setup(2, b'USB0')
epos_2, keyhandle_2, NodeID_2, pErrorCode_2, pDeviceErrorCode_2 = epos_setup(1, b'USB1')


# This should work as per the documentation, but it might be motor dependent
#set_motor_to_sinus_commuted_mode(epos_1, keyhandle_1, NodeID_1, pErrorCode_1)
#set_motor_to_sinus_commuted_mode(epos_2, keyhandle_2, NodeID_2, pErrorCode_2)

#enable_epos(epos_1, keyhandle_1, NodeID_1, pErrorCode_1)
enable_epos(epos_2, keyhandle_2, NodeID_2, pErrorCode_2)

while True:
    if mode == 0:
        # Create threads for moving to position 15000
        #thread1 = threading.Thread(target=go_to_position_thread, args=(epos_1, keyhandle_1, NodeID_1, pErrorCode_1, 15000))
        thread2 = threading.Thread(target=go_to_position_thread, args=(epos_2, keyhandle_2, NodeID_2, pErrorCode_2, 15000))
    else:
        # Create threads for moving to position 15000
        #thread1 = threading.Thread(target=move_to_position_thread, args=(epos_1, keyhandle_1, NodeID_1, pErrorCode_1, 15000))
        thread2 = threading.Thread(target=move_to_position_thread, args=(epos_2, keyhandle_2, NodeID_2, pErrorCode_2, 15000))
    # Start threads
    #thread1.start()
    thread2.start()

    # Wait for threads to complete
    #thread1.join()
    thread2.join()

    time.sleep(0.5)

    if mode == 0:
        # Create threads for moving to position -15000
        #thread1 = threading.Thread(target=go_to_position_thread, args=(epos_1, keyhandle_1, NodeID_1, pErrorCode_1, -15000))
        thread2 = threading.Thread(target=go_to_position_thread, args=(epos_2, keyhandle_2, NodeID_2, pErrorCode_2, -15000))
    else:
        # Create threads for moving to position -15000
        #thread1 = threading.Thread(target=move_to_position_thread, args=(epos_1, keyhandle_1, NodeID_1, pErrorCode_1, -15000))
        thread2 = threading.Thread(target=move_to_position_thread, args=(epos_2, keyhandle_2, NodeID_2, pErrorCode_2, -15000))

    # Start threads
    #thread1.start()
    thread2.start()

    # Wait for threads to complete
    #thread1.join()
    thread2.join()

    time.sleep(0.5)

"""
while True:
    go_to_position(epos_1, keyhandle_1, NodeID_1, pErrorCode_1, 15000)
    go_to_position(epos_2, keyhandle_2, NodeID_2, pErrorCode_2, 15000)
    time.sleep(0.5)
    go_to_position(epos_1, keyhandle_1, NodeID_1, pErrorCode_1, -15000)
    go_to_position(epos_2, keyhandle_2, NodeID_2, pErrorCode_2, -15000)
    time.sleep(0.5)
"""