from ctypes import *
import time

# Variables
# Platform
RPI = 0  # 0 = False, 1 = True

# RPI PATHS
path_ftd_rpi = '/home/icarus/libftd2xx.so.1.4.8'
path_lib_rpi = '/home/icarus/libEposCmd.so.6.8.1.0'

# Windows PATHS
path_lib_win = 'C:/Users/yann/PycharmProjects/Maxon-interface/EposCmd64.dll'


def epos_setup(NodeID):
    # EPOS Variables
    ret = 0
    keyhandle = 0

    VELOCITY = 6000    # RPM
    ACCELERATION = 80000    # RPM/s
    DECELERATION = 80000    # RPM/s

    pErrorCode = c_uint()
    pDeviceErrorCode = c_uint()

    # Load libraries
    if RPI:
        cdll.LoadLibrary(path_ftd_rpi)
        cdll.LoadLibrary(path_lib_rpi)
        epos = CDLL(path_lib_rpi)
        # open epos4 using rjs
        keyhandle = epos.VCS_OpenDevice(b'EPOS4', b'MAXON SERIAL V2', b'RS232', b'/dev/ttyS0', byref(pErrorCode))
    else:
        cdll.LoadLibrary(path_lib_win)
        epos = CDLL(path_lib_win)
        keyhandle = epos.VCS_OpenDevice(b'EPOS4', b'MAXON SERIAL V2', b'USB', b'USB0', byref(pErrorCode))


    if keyhandle != 0:
        print('EPOS4 opened')

        # Set operation mode to profile position mode
        ret = epos.VCS_ActivateProfilePositionMode(keyhandle, NodeID, byref(pErrorCode))

        # Set position profile
        ret = epos.VCS_SetPositionProfile(keyhandle, NodeID, VELOCITY, ACCELERATION, DECELERATION, byref(pErrorCode))

    else:
        print('EPOS4 not opened')
    return epos, keyhandle, NodeID, pErrorCode, pDeviceErrorCode