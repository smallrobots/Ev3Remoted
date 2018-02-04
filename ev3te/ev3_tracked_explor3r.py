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
        try:
            self.left_motor = ev3.LargeMotor('outB')
            self.right_motor = ev3.LargeMotor('outC')
            self.head_motor = ev3.MediumMotor('outA')

            # Init robot sensors
            # self.color_sensor = ev3.ColorSensor()
            # assert self.color_sensor.connected
            # self.color_sensor.mode = 'COL-REFLECT'
        except Exception as theException:
            ev3te.ev3te_logger.critical("Ev3TrackedExplor3r: Exception in routine __init__() + "
                                            + str(theException))

    # Process the incoming message
    def process_incoming_message(self, message):
        """Process the incoming message"""
        # Call the parent method
        ev3te.ev3te_logger.debug("Ev3TrackedExplor3r.process_incoming_message() - Processing a received message")
        super().process_incoming_message(message)

        # Decode the message
        message_str = str(message, 'utf-8')
        decoded_message = json.loads(message_str, object_hook = Ev3TrackedExplor3rMessage.object_decoder)

        # Use the message fields here
        # Actuate the main motors
        ev3te.ev3te_logger.debug("Ev3TrackedExplor3r.process_incoming_message() - Actuating main motors")
        try:
            ev3te.ev3te_logger.debug("Ev3TrackedExplor3r.process_incoming_message() - Forward Command: " +
                                     str(decoded_message.forward_command))
            ev3te.ev3te_logger.debug("Ev3TrackedExplor3r.process_incoming_message() - Turn Command: " +
                                     str(decoded_message.turn_command))
            if abs(decoded_message.forward_command > 5 or decoded_message.turn_command > 5):
                if decoded_message.turn_command != 0:
                    # delta = 1.0 * decoded_message.forward_command / decoded_message.turn_command
                    delta = decoded_message.turn_command
                else:
                    delta = 0

                left_speed = decoded_message.forward_command - delta
                if left_speed > 1000:
                    left_speed = 1000
                if left_speed < -1000:
                    left_speed = -1000

                right_speed = decoded_message.forward_command + delta
                if right_speed > 1000:
                    right_speed = 1000
                if right_speed < -1000:
                    right_speed = -1000

                ev3te.ev3te_logger.debug("Ev3TrackedExplor3r.process_incoming_message() - delta: " +
                                         str(delta))
                ev3te.ev3te_logger.debug("Ev3TrackedExplor3r.process_incoming_message() - left_speed: " +
                                         str(left_speed))
                ev3te.ev3te_logger.debug("Ev3TrackedExplor3r.process_incoming_message() - right_speed: " +
                                         str(right_speed))

                self.left_motor.run_forever(speed_sp = -left_speed)
                self.right_motor.run_forever(speed_sp = -right_speed)
            else:
                self.left_motor.stop(stop_action = "coast")
                self.right_motor.stop(stop_action = "coast")
        except Exception as theException:
            ev3_remoted.ev3_logger.critical("Ev3TrackedExplor3r: Exception in routine process_incoming_message() + "
                                            + str(theException))

        return decoded_message
