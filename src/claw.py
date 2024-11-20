from vex import *
from main import controller

claw = Motor(Ports.PORT12)

claw.set_stopping(BrakeType.HOLD)


def on_close_button_pressed():
    claw.spin(direction=REVERSE)

def on_open_button_pressed():
    claw.spin(direction=FORWARD)
    


def on_button_released():
    claw.stop()



# controller event handlers
controller.buttonL1.pressed(on_open_button_pressed)
controller.buttonL1.released(on_button_released)
controller.buttonL2.pressed(on_close_button_pressed)
controller.buttonL2.released(on_button_released)
