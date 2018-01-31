#################################################################################################
# ev3_remoted.Ev3Receiver class                                                                 #
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
import threading
import ev3_remoted
import ev3_remoted.ev3_robot_model
from ev3_remoted.ev3_robot_model import Ev3RobotModel
from ev3_remoted.ev3_robot_message import MessageType
from ev3_remoted.ev3_robot_message import Ev3RobotMessage

# Logger settings
#import logging

#logger = logging.getLogger()
#handler = logging.StreamHandler()
#formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
#handler.setFormatter(formatter)
#logger.addHandler(handler)

# Change the following line to set desired log details
#logger.setLevel(logging.DEBUG)


class Ev3Receiver(threading.Thread):
    """TCP/UDP Receiver thread class definition"""

    # Constants
    __default_buffer_size = 1500
    __default_host_name = "localhost"
    __default_host_port = 60001
    __default_controller_host_port = 60002
    __default_timeout = 0.20
    __default_remote_controllers_list = []
    
    def __init__(self, robot_model = Ev3RobotModel(),
                 buffer_size = __default_buffer_size,
                 host_name = __default_host_name,
                 host_port = __default_host_port,
                 controller_host_port = __default_controller_host_port,
                 remote_controllers_list = __default_remote_controllers_list):
        """ Initialize a new ev3_server with attributes """

        # Call base class constructor
        super(Ev3Receiver, self).__init__()

        # Assign UDP parameters
        self.buffer_size = buffer_size
        self.host_name = host_name
        self.host_port = host_port
        self.controller_host_port = controller_host_port
        self.remote_controllers_list = remote_controllers_list

        # Assign the robot model
        if isinstance(robot_model, ev3_remoted.ev3_robot_model.Ev3RobotModel):
            self.robot_model = robot_model
        else:
            raise ValueError("Smallrobots.it \nArgument robot_model must be of type ev3_robot_model")

        # Set a boolean flag needed to stop the server
        self.__stop_server = False

    # Thread worker function definition
    def run(self):
        """Thread worker function definition"""
        # Create the inbound socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = (self.host_name, int(self.host_port))

        # Bind the inbound socket
        server_socket.settimeout(self.__default_timeout)
        try:
            ev3_remoted.ev3_logger.info("Ev3Receiver: starting...")
            ev3_remoted.ev3_logger.info("Ev3Receiver: binding socket at server address:" + str(server_address))
            server_socket.bind(server_address)
            ev3_remoted.ev3_logger.info("Ev3Receiver: socket bound")
        except Exception as theException:
            ev3_remoted.ev3_logger.critical("Ev3Receiver: Exception in routine run() + " + str(theException))
            raise theException

        # Main loop
        while not self.__stop_server:
            try:
                # Wait for incoming messages
                ev3_remoted.ev3_logger.debug("Ev3Receiver: waiting an incoming message")
                remote_controller_message, remote_controller_address = server_socket.recvfrom(self.buffer_size)
            except socket.timeout:
                # time out
                ev3_remoted.ev3_logger.debug("Ev3Receiver: timeout")
                continue

            # Check that the sender and the message are not void
            if remote_controller_address is not None and remote_controller_message:
                ev3_remoted.ev3_logger.debug("Ev3Receiver: message received from " + str(remote_controller_address))
                ev3_remoted.ev3_logger.debug("Ev3Receiver: message body:  " + str(remote_controller_message))
                # Ok, process the message
                decoded_message = self.robot_model.process_incoming_message(remote_controller_message)
                try:
                    if self.robot_model.remote_controller_address is not None \
                            and self.robot_model.remote_controller_port is not None:  # \
                            # and type(self.robot_model.remote_controller_port) is int:
                        # remote_controller_address and remote_controller_port seem valid
                        self.update_remote_controllers_list((self.robot_model.remote_controller_address,
                                                             int(self.robot_model.remote_controller_port)),
                                                             decoded_message.message_function)
                        # self.update_remote_controllers_list((self.robot_model.remote_controller_address,
                        #                                      self.robot_model.remote_controller_port),
                        #                                     decoded_message.message_function)
                        # self.update_remote_controllers_list(remote_controller_address,
                        #                                     decoded_message.message_function)
                    else:
                        continue
                except ValueError:
                    # Most probably the controller port is invalid
                    ev3_remoted.ev3_logger.critical("Ev3Receiver: ValueError: self.robot_model.remote_controller_port = " +
                                                    str(self.robot_model.remote_controller_port))
                    continue
            else:
                # Proceed with next message
                continue

        # Close the socket before exiting
        server_socket.close()
        ev3_remoted.ev3_logger.info("Ev3Receiver: released socket at server address:" + str(server_address))

    # Stop this thread
    def stop(self):
        """Stop this thread"""
        ev3_remoted.ev3_logger.info("Ev3Receiver: stopping...")
        self.__stop_server = True
        self.join()
        ev3_remoted.ev3_logger.info("Ev3Receiver: stopped")

    # Update the list of remote controllers if needed
    def update_remote_controllers_list(self, remote_controller_address, message_type):
        # cycle flag
        found = False
        # search cycle
        for remote_controller in self.remote_controllers_list:
            if remote_controller == remote_controller_address:
                found = True
                break

        ev3_remoted.ev3_logger.debug("Ev3Receiver: message_type is: " + str(message_type))
        if message_type == MessageType.subscribe and not found:
            # add the new remote_controller to the list
            self.remote_controllers_list.append(remote_controller_address)
        elif message_type == MessageType.unsubscribe and found:
            # remote the remote_controller from the list
            self.remote_controllers_list.remove(remote_controller_address)


