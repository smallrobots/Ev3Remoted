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
from ev3te.ev3_tracked_explor3r_message import *
from ev3_remoted.ev3_robot_model import *
from ev3dev import ev3 as ev3


class Ev3TrackedExplor3r (Ev3RobotModel):
    """Main class for the Ev3 Tracked Explor3r"""

    # Default main constructor
    def __init__(self):
        """Default main constructor for the Ev3TrackedExplor3r class"""
        # Call parent constructor
        super(Ev3TrackedExplor3r, self).__init__()

        # Init robot sensors and actuators
        try:
            # Init robot actuators
            self.left_motor = ev3.LargeMotor('outB')    # Address is importat for motors
            self.right_motor = ev3.LargeMotor('outC')
            self.head_motor = ev3.MediumMotor('outA')

            # Init robot sensors
            self.color_sensor = ev3.ColorSensor()       # Address is not really important for sensors
            self.color_sensor.mode = 'COL-REFLECT'      # if there are not two instance of the same type
            self.ir_sensor = ev3.InfraredSensor()       # of sensor
            self.ir_sensor.mode = 'IR-PROX'
        except Exception as theException:
            # Most probably one of the sensors or one of the actuators is not connected
            ev3te.ev3te_logger.critical("Ev3TrackedExplor3r: Exception in routine __init__() + "
                                        + str(theException))
        # Init status fields
        self.ir_reading_update_counter = 0
        self.ir_samples_to_skip = 5
        self.ir_last_reading = 0

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
            # Main motors
            self.actuate_main_motors(decoded_message)
            # Head motor
            self.actuate_head_motor(decoded_message)
        except Exception as theException:
            ev3_remoted.ev3_logger.critical("Ev3TrackedExplor3r: Exception in routine process_incoming_message() + "
                                            + str(theException))
        return decoded_message

    # Actuate the head medium motor
    def actuate_head_motor(self, decoded_message):
        """Actuate the head medium motor"""
        try:
            if abs(decoded_message.turn_head_command) > 5:
                head_motor_speed = decoded_message.turn_head_command
                ev3te.ev3te_logger.debug("Ev3TrackedExplor3r.process_incoming_message() - delta: " +
                                         str(head_motor_speed))
                self.head_motor.run_forever(speed_sp = head_motor_speed)
            else:
                self.head_motor.stop(stop_action = "coast")
        except Exception as theException:
            ev3_remoted.ev3_logger.critical("Ev3TrackedExplor3r: Exception in routine actuate_head_motor() + "
                                            + str(theException))

    # Actuate the main motors
    def actuate_main_motors(self, decoded_message):
        """Actuate the main motors taking decoded_message as input"""
        try:
            if abs(decoded_message.forward_command) > 5 or abs(decoded_message.turn_command) > 5:
                delta = decoded_message.turn_command

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
            ev3_remoted.ev3_logger.critical("Ev3TrackedExplor3r: Exception in routine actuate_main_motots() + "
                                            + str(theException))

    # Create an outbound status message
    def create_outbound_message(self):
        # Call parent method
        message = super().create_outbound_message()

        # Get specific status
        message.left_motor_speed = self.get_left_motor_speed()
        message.right_motor_speed = self.get_right_motor_speed()
        message.single_ir_reading = self.get_single_ir_reading()
        message.head_motor_position = self.get_head_motor_position()

        return message

    # Get the left motor speed
    def get_left_motor_speed(self):
        try:
            ret_value = self.left_motor.duty_cycle
        except Exception as theException:
            ev3te.ev3te_logger.critical("Ev3TrackedExplor3r.get_left_motor_speed() - " + str(theException))
            ret_value = 0
        return ret_value

    # Get the left motor speed
    def get_right_motor_speed(self):
        try:
            ret_value = self.right_motor.duty_cycle
        except Exception as theException:
            ev3te.ev3te_logger.critical("Ev3TrackedExplor3r.get_right_motor_speed() - " + str(theException))
            ret_value = 0
        return ret_value

    # Get a single reading from the IR Sensor
    def get_single_ir_reading(self):
        if self.ir_reading_update_counter > self.ir_samples_to_skip:
            try:
                self.ir_last_reading = self.ir_sensor.proximity
            except Exception as theException:
                ev3te.ev3te_logger.critical("Ev3TrackedExplor3r.get_single_ir_reading() - " + str(theException))
            finally:
                self.ir_reading_update_counter = 0
        else:
            self.ir_reading_update_counter += 1
        ret_value = self.ir_last_reading
        return ret_value

    # Get head motor position
    def get_head_motor_position(self):
        try:
            ret_value = self.head_motor.position
        except Exception as theException:
            ev3te.ev3te_logger.critical("Ev3TrackedExplor3r.get_head_motor_position() - " + str(theException))
            ret_value = 0
        return ret_value


