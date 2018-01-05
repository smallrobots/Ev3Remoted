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

import socket
import json
import threading
import ev3_remoted.ev3_robot_model
import ev3_remoted.ev3_sender
import ev3_remoted.ev3_receiver

class Ev3RemoteController(object):
    """Description of a remote controller"""

    # Constants
    __default_controller_name = "Default"
    __default_controller_host_port = 60002
    __default_controller_host_address = "127.0.0.1"
    __default_is_active_controller = False

    # Initialize a new ev3_remote_controller with attributes
    def __init__(self, 
                 name = __default_controller_name,
                 host_port = __default_controller_host_port,
                 host_address = __default_controller_host_address,
                 is_active_controller = __default_is_active_controller
                 ):
        """Default constructor"""
        self.__name = name
        self.__address = host_address
        self.__port = host_port
        self.is_active_controller = is_active_controller


