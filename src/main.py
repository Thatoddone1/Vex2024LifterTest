
from vex import *
from drive import rc_auto_loop_function_controller_1


brain=Brain()

controller=Controller(PRIMARY)



# define variable for remote controller enable/disable
remote_control_code_enabled = True

rc_auto_loop_thread_controller_1 = Thread(rc_auto_loop_function_controller_1)

        
