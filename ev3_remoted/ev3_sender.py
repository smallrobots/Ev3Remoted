#################################################################################################
# ev3_remoted.Ev3Sender class                                                                   #
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
from ev3_remoted.ev3_robot_message import Ev3RobotMessage
from ev3_remoted.ev3_robot_message import MessageType
from time import sleep
import ev3_remoted

# Logger settings
#import logging

#logger = logging.getLogger()
#handler = logging.StreamHandler()
#formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
#handler.setFormatter(formatter)
#logger.addHandler(handler)

# Change the following line to set desired log details
#logger.setLevel(logging.DEBUG)


class Ev3Sender(threading.Thread):
    """Sender Thread"""

    # Constants
    __default_buffer_size = 1500
    __default_host_address = 'localhost'
    __default_host_port = 60001
    __default_controller_host_port = 60002
    __default_controller_host_address = '127.0.0.1'
    __default_remote_controllers_list = []
    
    def __init__(self, robot_model = ev3_remoted.ev3_robot_model.Ev3RobotModel(),
                 buffer_size = __default_buffer_size,
                 host_address = __default_host_address,
                 host_port = __default_host_port,
                 controller_host_port = __default_controller_host_port,
                 controller_host_address = __default_controller_host_address,
                 remote_controllers_list = __default_remote_controllers_list):
        """ Initialize a new ev3_server with attributes """

        # Call base class constructor
        super(Ev3Sender, self).__init__()

        # Assign UDP parameters
        self.buffer_size = buffer_size
        self.host_name = host_address
        self.host_port = host_port
        self.controller_host_port = controller_host_port
        self.controller_host_address = controller_host_address
        self.remote_controllers_list = remote_controllers_list

        # Assign the robot model
        if isinstance(robot_model, ev3_remoted.ev3_robot_model.Ev3RobotModel):
            self.robot_model = robot_model
        else:
            raise ValueError("Smallrobots.it \nArgument robot_model must be of type ev3_robot_model")

        # Assign periodicity
        self.__default_timeSample = 0.1

        # Set a boolean flag needed to stop the server
        self.__stop_server = False
        
    # Thread worker function definition
    def run(self):
        """Thread worker function definition"""
        try:
            # Open the outbound socket
            outbound_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            # Cycle until a stop request is received
            while not self.__stop_server:
                # Check if the remote_controllers_list contains something
                ev3_remoted.ev3_logger.debug("ev3_sender: run() - remote_controllers_list - " + str(self.remote_controllers_list))
                if len(self.remote_controllers_list) != 0:
                    # Send to every known address a message with the robot status
                    for controller_address in self.remote_controllers_list:
                        message = Ev3RobotMessage()
                        message.message_function = MessageType.robot_status
                        message_str = json.dumps(message, default=message.json_default)
                        encoded_message = str.encode(message_str, encoding = 'utf-8')
                        ev3_remoted.ev3_logger.debug("ev3_sender: run() - controller_address - " + str(controller_address))
                        outbound_socket.sendto(encoded_message, controller_address)
                sleep(self.__default_timeSample)

        except Exception as theException:
            # Something went wrong with the decoding
            # For the moment just print the Exception
            # must be further investigated
            print(theException)
        finally:
            # Close the socket
            outbound_socket.close()

    # Stop this thread
    def stop(self):
        """Stop this thread"""
        self.__stop_server = True
        self.join()



