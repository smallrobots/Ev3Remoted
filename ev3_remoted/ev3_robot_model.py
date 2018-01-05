#################################################################################################
# ev3_remoted.Ev3RobotModel class                                                                  #
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

from ev3_remoted.ev3_robot_message import Ev3RobotMessage
import json


class Ev3RobotModel(object):
    """Base class for the ev3_remoted robot"""

    # Default constants
    __default_robot_name = "EV3 Remoted Robot"

    # Class constructor
    def __init__(self, robot_name=__default_robot_name, server = None):
        """Class constructor """
        self.__robot_name = robot_name
        self.__sent_messages = 0
        self.__processed_messages = 0
        self.__server = server
        self.remote_controller_name = ''
        self.remote_controller_address = ''
        self.remote_controller_port = 0

    # Properties
    # robot_name
    @property
    def robot_name(self):
        """Gets or sets the name of this robot"""
        return self.__robot_name

    @robot_name.setter
    def robot_name(self,value):
        self.__robot_name = value

    # Server
    @property
    def server(self):
        """Gets or sets the server for this robot_model"""
        return self.__server

    @server.setter
    def server(self,value):
        self.__server = value

    # sent_messages
    @property
    def sent_messages(self):
        """Gets the total number of messages sent"""
        return self.__sent_messages

    # received_messages
    @property
    def processed_messages(self):
        """Gets the total number of messages received"""
        return self.__processed_messages

    # Methods
    def process_incoming_message(self, message):
        """Process a message"""
        # Test if message argument is of type string
        # if (not isinstance(message, bytes)):
        #    raise ValueError("message argument must be of type bytes")

        try:
            # Update the ev3_robot_model with the processed message
            message_str = str(message, 'utf-8')
            decoded_message = json.loads(message_str,
                                         object_hook = Ev3RobotMessage.object_decoder)
            self.remote_controller_name = decoded_message.remote_controller_name
            self.remote_controller_address = decoded_message.remote_controller_address
            self.remote_controller_port = decoded_message.remote_controller_port
        except Exception as theException:
            # Something went wrong with the decoding
            # For the moment just print the Exception
            # must be further investigated
            print(theException)
        finally:
            # Increment the number of processed messages
            self.__processed_messages += 1
            return decoded_message

    def create_outbound_message(self):
        """Create a new outbound message"""
        # Create a default message
        message = ""
        # Increment the number of outbound message created
        self.__sent_messages = self.__sent_messages + 1
        return message



