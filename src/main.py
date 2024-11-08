
from vex import *


brain=Brain()

controller=Controller()


motor = Motor(Ports.PORT5)

motor.set_stopping(BrakeType.HOLD)


def on_up_button_pressed():
    motor.spin(direction=REVERSE)

def on_down_button_pressed():
    motor.spin(direction=FORWARD)
    


def on_button_released():
    motor.stop()


controller.buttonR1.pressed(on_up_button_pressed)
controller.buttonR1.released(on_button_released)
controller.buttonR2.pressed(on_down_button_pressed)
controller.buttonR2.released(on_button_released)


        
