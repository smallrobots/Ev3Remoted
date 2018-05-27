#################################################################################################
# ev3te package                                                                                 #
# Version 1.0                                                                                   #
#                                                                                               #
# Happily shared under the MIT License (MIT)                                                    #
#                                                                                               #
# Copyright(c) 2017 SmallRobots.it                                                              #
#                                                                                               #
# Permission is hereby granted, free of charge, to any person obtaining                         #
# a copy of this software and associated documentation files (the "Software"),                  #
# to deal in the Software without restriction, including without limitation the rights          #
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies              #
# of the Software, and to permit persons to whom the Software is furnished to do so,            #
# subject to the following conditions:                                                          #
#                                                                                               #
# The above copyright notice and this permission notice shall be included in all                #
# copies or substantial portions of the Software.                                               #
#                                                                                               #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,           #
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR      #
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE            #
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,           #
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE         #
# OR OTHER DEALINGS IN THE SOFTWARE.                                                            #
#                                                                                               #
# Visit http://www.smallrobots.it for tutorials and videos                                      #
#                                                                                               #
# Credits                                                                                       #
# The Ev3TrackedExlpor3r is built with Lego Mindstorms Ev3 and Lego Technic Parts               #
#################################################################################################

import ev3_remoted
import ev3te
from ev3_remoted.ev3_robot_model import *
from ev3dev import ev3 as ev3


class Ev3TrackedExplor3rMessage(Ev3RobotMessage):
    def __init(self):
        super(Ev3TrackedExplor3rMessage, self).__init__()
        # Telemetry fields
        self.left_motor_speed = 0
        self.right_motor_speed = 0
        self.head_motor_position = 0
        self.single_ir_reading = 0
        # Command fields
        self.turn_head_command = 0
        self.is_continuous_scan_activated = False
        self.ircs_scan_list = []
        self.rover_selected = 0

    @staticmethod
    def object_decoder(obj):
        decoded_object = super(Ev3TrackedExplor3rMessage, Ev3TrackedExplor3rMessage).object_decoder(obj)
        # Decode message fields here
        decoded_object.left_motor_speed = obj['left_motor_speed']
        decoded_object.right_motor_speed = obj['right_motor_speed']
        decoded_object.turn_head_command = obj['turn_head_command']
        decoded_object.single_ir_reading = obj['single_ir_reading']
        decoded_object.head_motor_position = obj['head_motor_position']
        decoded_object.is_continuous_scan_activated = obj['is_continuous_scan_activated']
        decoded_object.ircs_scan_list = obj['ircs_scan_list']
        decoded_object.rover_selected = obj['rover_selected']
        return decoded_object
