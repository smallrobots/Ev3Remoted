#!/usr/bin/env python3

#################################################################################################
# ev3_remoted.ev3_server class                                                                  #
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
from ev3_remoted.ev3_robot_model import Ev3RobotModel
from ev3_remoted.ev3_sender import Ev3Sender
from ev3_remoted.ev3_receiver import Ev3Receiver

# Logger settings
#import logging

#logger = logging.getLogger()
#handler = logging.StreamHandler()
#formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
#handler.setFormatter(formatter)
#logger.addHandler(handler)

# Change the following line to set desired log details
#logger.setLevel(logging.DEBUG)


class Ev3Server(object):
    """Server class for remote control of a Lego Ev3 Brick 
with Ev3Dev firmware."""

    # Constants
    __default_buffer_size = 1500
    __default_host_name = "localhost"
    __default_host_port = 60001
    __default_controller_host_port = 60002
    __default_controller_host_address = "127.0.0.1"

    # Initialize a new ev3_server with attributes
    def __init__(self, robot_model = Ev3RobotModel(),
                 buffer_size = __default_buffer_size,
                 host_name = __default_host_name,
                 host_port = __default_host_port,
                 controller_host_port = __default_controller_host_port,
                 controller_host_address = __default_controller_host_address):
        """ Initialize a new ev3_server with attributes """

        # Assign UDP parameters
        self.__buffer_size = buffer_size
        self.__host_name = host_name
        self.__host_port = host_port
        self.__controller_host_port = controller_host_port
        self.__controller_host_address = controller_host_address

        # Check and assign the robot model
        if isinstance(robot_model, Ev3RobotModel):
            self.__robot_model = robot_model
        else:
            raise ValueError("Smallrobots.it \nArgument robot_model must be of type ev3_robot_model")

        # Initialize a dictionary of remote_controllers
        # self.remote_controllers_list = [('0.0.0.0', 0)]
        self.remote_controllers_list = []

        # Initialize the sender and the receiver
        self.sender = Ev3Sender(robot_model = self.__robot_model,
                                buffer_size = self.__buffer_size,
                                host_address = self.__host_name,
                                host_port = self.__host_port,
                                controller_host_port = self.__controller_host_port,
                                controller_host_address = self.__default_controller_host_address,
                                remote_controllers_list = self.remote_controllers_list)

        self.receiver = Ev3Receiver(robot_model = self.__robot_model,
                                    buffer_size = self.__buffer_size,
                                    host_name = self.__host_name,
                                    host_port = self.__host_port,
                                    controller_host_port = self.__controller_host_port,
                                    remote_controllers_list = self.remote_controllers_list)

        if self.sender.remote_controllers_list is not self.receiver.remote_controllers_list:
            ev3_remoted.ev3_logger.critical("Ev3Server: sender and receiver do not share the remote_controllers_list")
        else:
            ev3_remoted.ev3_logger.debug("Ev3Server: sender and receiver correctly share same remote_controllers_list")

    # Properties
    @property
    def is_running(self):
        """Property that returns True if the ev3_server is correctly running, False otherwise"""
        sender_alive = self.sender.isAlive()
        receiver_alive = self.receiver.isAlive()
        ev3_remoted.ev3_logger.debug("Ev3Server: sender_alive = " + str(sender_alive))
        ev3_remoted.ev3_logger.debug("ev3_server: receiver_alive = " + str(receiver_alive))
        return sender_alive and receiver_alive

    @property
    def buffer_size(self):
        """Buffer size propery"""
        return self.__buffer_size

    @buffer_size.setter
    def buffer_size(self, value):
        self.__buffer_size = value
        self.sender.buffer_size = value
        self.receiver.buffer_size = value

    @property
    def host_name(self):
        """Host name property"""
        return self.__host_name

    @host_name.setter
    def host_name(self, value):
        self.__host_name = value
        self.sender.host_name = value
        self.receiver.host_name = value

    @property
    def host_port(self):
        """Host port property"""
        return self.__host_port

    @host_port.setter
    def host_port(self, value):
        self.__host_port = value
        self.sender.host_port = value
        self.receiver.host_port = value

    @property
    def controller_host_address(self):
        """Controller Host Address property"""
        return self.__controller_host_address

    @controller_host_address.setter
    def controller_host_address(self, value):
        self.__controller_host_address = value
        self.sender.controller_host_address = value
        self.receiver.controller_host_address = value

    @property
    def controller_host_port(self):
        """Controller Host Port property"""
        return self.__controller_host_port

    @controller_host_port.setter
    def controller_host_port(self, value):
        self.__controller_host_port = value
        self.sender.controller_host_port = value
        self.receiver.controller_host_port = value

    @property
    def robot_model(self):
        """Robot model property"""
        return self.__robot_model

    @robot_model.setter
    def robot_model(self, value):
        self.__robot_model = value
        self.sender.robot_model = value
        self.receiver.robot_model = value

    # Methods
    # Start the server
    def start(self):
        """Start the server"""
        # Start the receiver thread
        try:
            ev3_remoted.ev3_logger.info("Ev3Server: Receiver thread starting...")
            self.receiver.start()
            ev3_remoted.ev3_logger.info("Ev3Server: Receiver thread started")
        except BaseException as e:
            ev3_remoted.ev3_logger.critical("Ev3Server: Raised exception during receiver startup: " + str(e))

        # Start the sender thread
        try:
            ev3_remoted.ev3_logger.info("Ev3Server: Sender thread starting...")
            self.sender.start()
            ev3_remoted.ev3_logger.info("Ev3Server: Sender thread started")
        except BaseException as e:
            ev3_remoted.ev3_logger.critical("Ev3Server: Raised exception during Sender startup: " + str(e))

    # Stop the server
    def stop(self):
        """Stop the server"""
        self.receiver.stop()
        self.sender.stop()
