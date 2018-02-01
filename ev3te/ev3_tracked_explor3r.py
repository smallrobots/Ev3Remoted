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
from ev3_remoted.ev3_robot_model import *
from ev3dev import ev3 as ev3


class Ev3TrackedExplor3rMessage(Ev3RobotMessage):
    def __init(self):
        super(Ev3TrackedExplor3rMessage, self).__init__()
        # Add message fields here
        # self.my_important_set_point = 0

    @staticmethod
    def object_decoder(obj):
        decoded_object = super(Ev3TrackedExplor3rMessage, Ev3TrackedExplor3rMessage).object_decoder(obj)
        # Decode message fields here
        # decoded_object.my_important_set_point = obj['my_important_set_point']
        return decoded_object


class Ev3TrackedExplor3r (Ev3RobotModel):
    """Main class for the Ev3 Tracked Explor3r"""

    # Default main constructor
    def __init__(self):
        """Default main constructor for the Ev3TrackedExplor3r class"""
        # Call parent constructor
        super(Ev3TrackedExplor3r, self).__init__()

        # Init robot actuators
        self.left_motor = ev3.LargeMotor('outD')
        self.right_motor = ev3.LargeMotor('outA')
        self.head_motor = ev3.MediumMotor('outC')

        # Init robot sensors
        self.color_sensor = ev3.ColorSensor()
        assert self.color_sensor.connected
        self.color_sensor.mode = 'COL-REFLECT'

    # Process the incoming message
    def process_incoming_message(self, message):
        """Process the incoming message"""
        # Call the parent method
        super().process_incoming_message(message)

        # Decode the message
        message_str = str(message, 'utf-8')
        decoded_message = json.loads(message_str, object_hook = Ev3TrackedExplor3rMessage.object_decoder)

        # Use the message fields here
        # self.my_important_set_point = decoded_message.my_important_set_point

        return decoded_message