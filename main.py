# Import
from ctypes import *
import time
import threading


# Functions
def WaitAcknowledged(epos, keyhandle, NodeID, pErrorCode):
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


def get_position(epos, keyhandle, NodeID, pErrorCode):
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


def get_position_is(epos, keyhandle, NodeID, pErrorCode):
    pPositionIs = c_long()
    ret = epos.VCS_GetPositionIs(keyhandle, NodeID, byref(pPositionIs), byref(pErrorCode))
    return check_error(ret, 'get position is', pPositionIs.value)


def go_to_position(epos, keyhandle, NodeID, pErrorCode, position):
    ret = epos.VCS_MoveToPosition(keyhandle, NodeID, position, 0, 0, byref(pErrorCode))
    print(check_error(ret, 'go to position', 1))
    ret = WaitAcknowledged(epos, keyhandle, NodeID, pErrorCode)


def move_to_position(epos, keyhandle, NodeID, pErrorCode, position):
    ret = epos.VCS_MoveToPosition(keyhandle, NodeID, position, 1, 1, byref(pErrorCode))
    print(check_error(ret, 'move to position', 1))
    ret = WaitAcknowledged(epos, keyhandle, NodeID, pErrorCode)


def go_home(epos, keyhandle, NodeID, pErrorCode):
    current_position = get_position(epos, keyhandle, NodeID, pErrorCode)
    go_to_position(epos, keyhandle, NodeID, pErrorCode, -current_position)


def enable_epos(epos, keyhandle, NodeID, pErrorCode):
    ret = epos.VCS_SetEnableState(keyhandle, NodeID, byref(pErrorCode))
    print(pErrorCode, NodeID)
    print(check_error(ret, 'enable epos', 1))


def disable_epos(epos, keyhandle, NodeID, pErrorCode):
    ret = epos.VCS_SetDisableState(keyhandle, NodeID, byref(pErrorCode))


def set_motor_to_sinus_commuted_mode(epos, keyhandle, NodeID, pErrorCode):
    ret = epos.VCS_SetMotorType(keyhandle, NodeID, 0x2, byref(pErrorCode))
    print(check_error(ret, 'set motor', 1))


def go_to_position_thread(epos, keyhandle, NodeID, pErrorCode, position):
    go_to_position(epos, keyhandle, NodeID, pErrorCode, position)


def move_to_position_thread(epos, keyhandle, NodeID, pErrorCode, position):
    move_to_position(epos, keyhandle, NodeID, pErrorCode, position)