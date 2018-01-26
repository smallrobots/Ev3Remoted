#################################################################################################
# ev3_remoted.Ev3RobotMessage class                                                                  #
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

import socket
import json
import threading
import ev3_remoted.ev3_robot_model
from time import sleep
from enum import IntEnum
import ev3_remoted


class MessageType(IntEnum):
    subscribe = 1
    unsubscribe = 2
    command = 3
    robot_status = 4


class Ev3RobotMessage(object):
    """Base class for the robot message
This class can be used for inbound and outbound message"""

    # Constructor
    def __init__(self, message_id = 0, 
                 robot_name = "",
                 robot_address = "",
                 robot_port = "",
                 remote_controller_name = "",
                 remote_controller_address = "", 
                 remote_controller_port = "",
                 message_function = MessageType.subscribe):
        """Default constructor
Message_function can be on of 'subscribe, unsubscribe, command or robot_status'"""
        self.message_id = message_id                          
        self.robot_name = robot_name    
        self.robot_address = robot_address
        self.robot_port = robot_port
        self.remote_controller_name = remote_controller_name
        self.remote_controller_address = remote_controller_address
        self.remote_controller_port = remote_controller_port
        self.message_function = message_function

    # Methods
    @staticmethod
    def object_decoder(obj):
        """Decoder from json stream"""
        decoded_object = Ev3RobotMessage()
        decoded_object.message_id = obj['message_id']
        decoded_object.robot_name = obj['robot_name']
        decoded_object.robot_address = obj['robot_address']
        decoded_object.robot_port = obj['robot_port']
        decoded_object.remote_controller_name = obj['remote_controller_name']
        decoded_object.remote_controller_address = obj['remote_controller_address']
        decoded_object.remote_controller_port = obj['remote_controller_port']
        decoded_object.message_function = obj['message_function']
        return decoded_object

    # Encoder to json stream
    @staticmethod
    def json_default(obj):
        return obj.__dict__


