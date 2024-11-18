from vex import *
from main import remote_control_code_enabled
from drive import left_drive_smart,left_motor_a,left_motor_b,right_drive_smart,right_motor_a,right_motor_b


def autonomous_loop_function_controler_1():
    if remote_control_code_enabled == False:
        print("autonomous code enabled")
    pass
    wait(20, MSEC)