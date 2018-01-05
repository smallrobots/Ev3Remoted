#!/usr/bin/env python3

#################################################################################################
# Unit testing for ev3_remoted.ev3_sender class                                            #
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

import unittest
from ev3_remoted import ev3_sender
from time import sleep

class ev3_sender_ut(unittest.TestCase):

    # Constants
    __default_buffer_size = 1500
    __default_host_name = "localhost"
    __default_host_port = 60001
    __default_controller_host_port = 60002
    __default_controller_host_address = "127.0.0.1"
    __default_remote_controllers_list = []

    def test_1(self):
        """ Test unit framework """
        self.assertTrue(1, "Unit test framework working")

    def test_2(self):
        """ Creating the sender thread """
        self.sender = ev3_sender.Ev3Sender(buffer_size = self.__default_buffer_size,
                                           host_address = self.__default_host_name,
                                           host_port = self.__default_host_port,
                                           controller_host_port = self.__default_controller_host_port,
                                           controller_host_address = self.__default_controller_host_address,
                                           remote_controllers_list = self.__default_remote_controllers_list)
        # Test creation
        self.assertIsNotNone(self.sender)

    def test_3(self):
        """ Starting and stopping the sender """
        self.sender = ev3_sender.Ev3Sender(buffer_size = self.__default_buffer_size,
                                           host_address = self.__default_host_name,
                                           host_port = self.__default_host_port,
                                           controller_host_port = self.__default_controller_host_port,
                                           controller_host_address = self.__default_controller_host_address,
                                           remote_controllers_list = self.__default_remote_controllers_list)

        # Start
        self.assertEqual(self.sender.isAlive(), False)
        self.sender.start()
        sleep(0.1)
        self.assertEqual(self.sender.isAlive(), True)

        # Stop
        self.sender.stop()
        sleep(0.1)
        self.assertEqual(self.sender.isAlive(), False)


if __name__ == '__main__':
    unittest.main()
