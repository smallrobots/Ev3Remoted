#!/usr/bin/env python3

#################################################################################################
# Unit testing for ev3_remoted.ev3_robot_model class                                            #
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
from ev3_remoted.ev3_robot_message import MessageType
import sys, os
from time import sleep
import json

import ev3_remoted.ev3_server
import ev3_remoted.ev3_robot_model
import ev3_remoted.ev3_robot_message

class ev3_robot_message_ut(unittest.TestCase):
    def test_01(self):
        """ Test unit framework """
        self.assertTrue(1,"Unit test framework working")

    def test_02(self):
        """Test for ev3_robot_message instatiation"""
        robot_message = ev3_remoted.ev3_robot_message.Ev3RobotMessage()
        self.assertIsNotNone(robot_message)

    def test_03(self):
        """Property - 1"""
        for i in range (0,1000):
            robot_message = ev3_remoted.ev3_robot_message.Ev3RobotMessage(message_id = i)
            self.assertEqual(robot_message.message_id, i)

    def test_04(self):
        """Property - 2"""
        for i in range (0,1000):
            robot_message = ev3_remoted.ev3_robot_message.Ev3RobotMessage()
            self.assertEqual(robot_message.message_id, 0)
            robot_message.message_id = i
            self.assertEqual(robot_message.message_id, i)

    def test_05(self):
        """Property - 3"""
        robot_name_1 = "Mazinga Z"
        robot_name_2 = "Venus"
        robot_message = ev3_remoted.ev3_robot_message.Ev3RobotMessage(robot_name = robot_name_1)
        self.assertEqual(robot_message.robot_name, robot_name_1)
        robot_message.robot_name = robot_name_2
        self.assertEqual(robot_message.robot_name, robot_name_2)

    def test_06(self):
        """Property - 4"""
        remote_controller_1 = "Tetsuya"
        remote_controller_2 = "Actarus"
        robot_message = ev3_remoted.ev3_robot_message.Ev3RobotMessage(remote_controller_name = remote_controller_1)
        self.assertEqual(robot_message.remote_controller_name, remote_controller_1)
        robot_message.remote_controller_name = remote_controller_2
        self.assertEqual(robot_message.remote_controller_name, remote_controller_2)

    def test_07(self):
        """json encoding and decoding"""
        robot_name_1 = "Mazinga Z"
        remote_controller_1 = "Tetsuya"
        robot_message_1 = ev3_remoted.ev3_robot_message.Ev3RobotMessage(0, robot_name_1, remote_controller_1)

        # encoding
        data_str = json.dumps(robot_message_1, default = robot_message_1.json_default)

        # decoding
        robot_message_2 = json.loads(data_str, object_hook = robot_message_1.object_decoder)

        # check
        self.assertEqual(robot_message_1.message_id, robot_message_2.message_id)
        self.assertEqual(robot_message_1.remote_controller_name, robot_message_2.remote_controller_name)
        self.assertEqual(robot_message_1.robot_name, robot_message_2.robot_name)

    def test_08(self):
        """json encoding and decoding to bytes"""
        robot_name_1 = "Mazinga Z"
        remote_controller_1 = "Tetsuya"
        robot_message_1 = ev3_remoted.ev3_robot_message.Ev3RobotMessage(0, robot_name_1, remote_controller_1)

        # encoding
        data_str = json.dumps(robot_message_1, default = robot_message_1.json_default)
        data_bytes = str.encode(data_str, encoding = 'utf-8')

        # decoding
        received_str = str(data_bytes, 'utf-8')
        robot_message_2 = json.loads(received_str, object_hook = robot_message_1.object_decoder)

        # check
        self.assertEqual(robot_message_1.message_id, robot_message_2.message_id)
        self.assertEqual(robot_message_1.remote_controller_name, robot_message_2.remote_controller_name)
        self.assertEqual(robot_message_1.robot_name, robot_message_2.robot_name)
        
    def test_09(self):
        """Test message_type class"""
        self.assertEqual(ev3_remoted.ev3_robot_message.MessageType.subscribe, 1)
        self.assertEqual(ev3_remoted.ev3_robot_message.MessageType.unsubscribe, 2)
        self.assertEqual(ev3_remoted.ev3_robot_message.MessageType.command, 3)
        self.assertEqual(ev3_remoted.ev3_robot_message.MessageType.robot_status, 4)

if __name__ == '__main__':
    unittest.main()
