from vex import *
from main import controller

lift = Motor(Ports.PORT5)

lift.set_stopping(BrakeType.HOLD)


def on_up_button_pressed():
    lift.spin(direction=REVERSE)
    print("lift up")

def on_down_button_pressed():
    lift.spin(direction=FORWARD)
    print("lift down")
    


def on_button_released():
    lift.stop()



# controller event handlers
controller.buttonR1.pressed(on_up_button_pressed)
controller.buttonR1.released(on_button_released)
controller.buttonR2.pressed(on_down_button_pressed)
controller.buttonR2.released(on_button_released)
