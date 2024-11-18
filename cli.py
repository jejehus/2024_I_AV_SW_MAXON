from epos_setup import epos_setup
from main import *
import time

AMOUNT_OF_MOTORS = 0
RPI = 0
PATH_LIB_WIN = ''
motors = []


def motor_selector():
    amount_of_motors = int(input(''))
    set_motors(amount_of_motors)
    if amount_of_motors == 1:
        print('You have selected 1 motor')
    elif amount_of_motors == 2:
        print('You have selected 2 motors')
    else:
        print('Invalid input, please enter a valid number')
        motor_selector()


def set_motors(amount_of_motors):
    global AMOUNT_OF_MOTORS
    AMOUNT_OF_MOTORS = amount_of_motors


def set_environment(env_type):
    global RPI
    RPI = env_type


def set_path(path):
    global PATH_LIB_WIN
    PATH_LIB_WIN = path


def enable():
    for motor in motors:
        enable_epos(motor[0], motor[1], motor[2], motor[3])


def disable():
    for motor in motors:
        disable_epos(motor[0], motor[1], motor[2], motor[3])


def go_home():
    for motor in motors:
        go_home_motor(motor[0], motor[1], motor[2], motor[3])


def set_home():
    for motor in motors:
        set_home_position(motor[0], motor[1], motor[2], motor[3])
    main()


def get_current_position_motors():
    for motor in motors:
        print(get_current_position(motor[0], motor[1], motor[2], motor[3]))


def move():
    print('Please enter the maximum and minimum position you would like to move the motors to.')
    max_position = int(input('Max position: '))
    min_position = int(input('Min position: '))
    num_of_movements = int(input('Please enter the amount of movements you would like to make: '))
    while num_of_movements > 0:
        for motor in motors:
            move_to_position(motor[0], motor[1], motor[2], motor[3], max_position)
        time.sleep(1)
        for motor in motors:
            move_to_position(motor[0], motor[1], motor[2], motor[3], min_position)
        time.sleep(1)

        num_of_movements -= 1


def intro():
    message_home = """
        
        ___    ____  ________  ____________   _____   ________
       /   |  / __ \/ ____/ / / /  _/ ____/  /  _/ | / / ____/
      / /| | / /_/ / /   / /_/ // // __/     / //  |/ / /     
     / ___ |/ _, _/ /___/ __  // // /___   _/ // /|  / /____  
    /_/  |_/_/ |_|\____/_/ /_/___/_____/  /___/_/ |_/\____(_) 
    
    
    """

    message_amount_select = """
    Welcome to the Maxon Motor interface, to start, please select the your environment (RPI = 1, PC = 0).
    """
    print(message_home + message_amount_select)
    set_environment(int(input()))
    if RPI == 0:
        set_path(input('Please enter the path to the EposCmd64.dll file (C:/PATH-TO-LIB/EposCmd64.dll): '))
    mode = input('Please select the mode you would like to use (0 = Position mode, 1 = Velocity mode): ')
    print('Please select the amount of motors you would like to control.')
    motor_selector()
    print('Setting up motors...')
    for i in range(AMOUNT_OF_MOTORS):
        motors.append(epos_setup(RPI, i, b'USB' + str(i).encode(), PATH_LIB_WIN, mode))
        print('Motor ' + str(i + 1) + ' setup complete')
    print('If you dont see any errors, the motors are ready to be controlled.')
    main()


def main():
    while True:
        choice = 0
        print('You can now choose the following options, remember to enable the motors before moving them.')
        print('• Enable Motors (1)', 'green')
        print('• Disable Motors (2)', 'green')
        print('• Go Home (3)', 'green')
        print('• Set Home (4)', 'green')
        print('• Move Motors (5)', 'green')
        print('• Get position (6)', 'green')
        choice = int(input())
        if choice == 1:
            enable()
        elif choice == 2:
            disable()
        elif choice == 3:
            go_home()
        elif choice == 4:
            set_home()
        elif choice == 5:
            move()
        elif choice == 6:
            get_current_position_motors()
        else:
            print('Invalid input, please enter a valid number')
            main()


intro()