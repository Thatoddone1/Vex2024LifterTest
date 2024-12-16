from vex import *

#CONFIG

brain=Brain()
controller=Controller(PRIMARY)

####### lift STUFF ↓ #######    

lift1 = Motor(Ports.PORT5, GearSetting.RATIO_36_1)
lift2 = Motor(Ports.PORT8, GearSetting.RATIO_36_1)

lift1.set_stopping(BrakeType.HOLD)
lift2.set_stopping(BrakeType.HOLD)


def on_up_button_pressed():
    lift1.spin(direction=REVERSE)
    lift2.spin(direction=FORWARD)

def on_down_button_pressed():
    lift1.spin(direction=FORWARD)
    lift2.spin(direction=REVERSE)
    
def on_lift_button_released():
    lift1.stop()
    lift2.stop()

# controller event handlers
controller.buttonR1.pressed(on_up_button_pressed)
controller.buttonR1.released(on_lift_button_released)
controller.buttonL1.pressed(on_down_button_pressed)
controller.buttonL1.released(on_lift_button_released)

####### CLAW CODE ↓ ########

claw = Motor(Ports.PORT12)

claw.set_stopping(BrakeType.HOLD)
claw.set_velocity(15, PERCENT)


def on_close_button_pressed():
    claw.spin(direction=REVERSE)
    print(claw.position())

def on_open_button_pressed():
    claw.spin(direction=FORWARD)
    
def on_claw_button_released():
    claw.stop()

# controller event handlers
controller.buttonR2.pressed(on_open_button_pressed)
controller.buttonR2.released(on_claw_button_released)
controller.buttonL2.pressed(on_close_button_pressed)
controller.buttonL2.released(on_claw_button_released)

####### DRIVE STUFF ↓ ########
# motors and drive train setup
left_motor_a = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
left_motor_b = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
left_drive_smart = MotorGroup(left_motor_a, left_motor_b)
right_motor_a = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)
right_motor_b = Motor(Ports.PORT4, GearSetting.RATIO_18_1, True)
right_drive_smart = MotorGroup(right_motor_a, right_motor_b)
drivetrain = DriveTrain(left_drive_smart, right_drive_smart, 319.19, 355.59999999999997, 266.7, MM, 1)

#varibles needed for the controoler loop
drivetrain_l_needs_to_be_stopped_controller = False
drivetrain_r_needs_to_be_stopped_controller = False

# define a task that will handle monitoring inputs from controller
def rc_auto_loop_function_controller():
    global drivetrain_l_needs_to_be_stopped_controller, drivetrain_r_needs_to_be_stopped_controller, remote_control_code_enabled
    # process the controller input every 20 milliseconds
    # update the motors based on the input values
    while True:
        if remote_control_code_enabled:
            
            # calculate the drivetrain motor velocities from the controller joystick axies
            # left = axis3 + axis1
            # right = axis3 - axis1
            if controller.axis3.position() > 0:
                drivetrain_left_side_speed = ((controller.axis3.position()**2) - 15)/150
            else:
                drivetrain_left_side_speed = -((controller.axis3.position()**2) - 15)/150
            if controller.axis2.position() > 0:
                drivetrain_right_side_speed = ((controller.axis2.position()**2) - 15)/150
            else:
                drivetrain_right_side_speed = -((controller.axis2.position()**2) - 15)/150
            
            # check if the value is inside of the deadband range
            if drivetrain_left_side_speed < 5 and drivetrain_left_side_speed > -5:
                # check if the left motor has already been stopped
                if drivetrain_l_needs_to_be_stopped_controller:
                    # stop the left drive motor
                    left_drive_smart.stop()
                    # tell the code that the left motor has been stopped
                    drivetrain_l_needs_to_be_stopped_controller = False
            else:
                # reset the toggle so that the deadband code knows to stop the left motor next
                # time the input is in the deadband range
                drivetrain_l_needs_to_be_stopped_controller = True
            # check if the value is inside of the deadband range
            if drivetrain_right_side_speed < 5 and drivetrain_right_side_speed > -5:
                # check if the right motor has already been stopped
                if drivetrain_r_needs_to_be_stopped_controller:
                    # stop the right drive motor
                    right_drive_smart.stop()
                    # tell the code that the right motor has been stopped
                    drivetrain_r_needs_to_be_stopped_controller = False
            else:
                # reset the toggle so that the deadband code knows to stop the right motor next
                # time the input is in the deadband range
                drivetrain_r_needs_to_be_stopped_controller = True
            
            # only tell the left drive motor to spin if the values are not in the deadband range
            if drivetrain_l_needs_to_be_stopped_controller:
                left_drive_smart.set_velocity(drivetrain_left_side_speed, PERCENT)
                left_drive_smart.spin(FORWARD)
            # only tell the right drive motor to spin if the values are not in the deadband range
            if drivetrain_r_needs_to_be_stopped_controller:
                right_drive_smart.set_velocity(drivetrain_right_side_speed, PERCENT)
                right_drive_smart.spin(FORWARD)
            # check the buttonL1/buttonL2 status
            # to control scooper_motor
        # wait before repeating the process
        wait(20, MSEC)

# define variable for remote controller enable/disable
remote_control_code_enabled = True

rc_auto_loop_thread_controller = Thread(rc_auto_loop_function_controller)
