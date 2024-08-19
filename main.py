# Import
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

# EPOS Variables
NodeID_1 = 1
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


# Functions
def WaitAcknowledged():
    object_index = 0x6041
    object_sub_index = 0x0
    number_of_bytes_to_read = 0x02
    pnumber_of_bytes_read = c_uint()
    pData = c_uint()
    mask_bit_12 = 0x1000
    i = 0

    while True:
        ret = epos.VCS_GetObject(keyhandle, NodeID, object_index, object_sub_index, byref(pData),
                                 number_of_bytes_to_read, byref(pnumber_of_bytes_read), byref(pErrorCode))
        bit_12 = mask_bit_12 & pData.value

        if i > 20:
            return 0
        if bit_12 == mask_bit_12:
            time.sleep(1)
            i += 1
        else:
            return 1


def check_error(ret, function_name, value):
    if ret == 0:
        print('Error ' + function_name)
        return 0
    else:
        return value


def get_position():
    object_index = 0x6064
    object_sub_index = 0x00
    number_of_bytes_to_read = 0x04
    number_of_bytes_read = c_uint()
    pData = c_uint()
    ret = epos.VCS_GetObject(keyhandle, NodeID, object_index, object_sub_index, byref(pData), number_of_bytes_to_read,
                             byref(number_of_bytes_read), byref(pErrorCode))
    if ret == 1:
        return pData.value
    else:
        print('Error reading position')
        return 0


def get_position_is():
    pPositionIs = c_long()
    ret = epos.VCS_GetPositionIs(keyhandle, NodeID, byref(pPositionIs), byref(pErrorCode))
    return check_error(ret, 'get position is', pPositionIs.value)


def go_to_position(position):
    ret = epos.VCS_MoveToPosition(keyhandle, NodeID, position, 0, 0, byref(pErrorCode))
    print(check_error(ret, 'go to position', 1))
    ret = WaitAcknowledged()


def go_home():
    current_position = get_position()
    go_to_position(-current_position)
    

def enable_epos():
    ret = epos.VCS_SetEnableState(keyhandle, NodeID, byref(pErrorCode))
    print(check_error(ret, 'enable epos', 1))


def disable_epos():
    ret = epos.VCS_SetDisableState(keyhandle, NodeID, byref(pErrorCode))