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
import sys, os
from time import sleep

#sys.path.insert(0, os.path.dirname(".."))
import ev3_remoted.ev3_server
import ev3_remoted.ev3_robot_model

class ev3_robot_model_ut(unittest.TestCase):
    def test_1(self):
        """ Test unit framework """
        self.assertTrue(1,"Unit test framework working")

    def test_2(self):
        """Test for ev3_robot_model instatiation"""
        robot_model = ev3_remoted.ev3_robot_model.Ev3RobotModel()
        self.assertIsNotNone(robot_model)

    def test_3(self):
        """Robot name property - 1"""
        robot_model = ev3_remoted.ev3_robot_model.Ev3RobotModel()
        self.assertEqual("EV3 Remoted Robot", robot_model.robot_name)

    def test_4(self):
        """Robot name property - 2"""
        robot_name = "Mazinga Z"
        robot_model = ev3_remoted.ev3_robot_model.Ev3RobotModel(robot_name = robot_name)
        self.assertEqual(robot_name, robot_model.robot_name)

    def test_5(self):
        """Robot name property - 3"""
        robot_name = "Mazinga Z"
        robot_model = ev3_remoted.ev3_robot_model.Ev3RobotModel()
        robot_model.robot_name = robot_name
        self.assertEqual(robot_name, robot_model.robot_name)

    def test_6(self):
        """Processed messages count - 1"""
        robot_model = ev3_remoted.ev3_robot_model.Ev3RobotModel()
        self.assertEqual(0, robot_model.processed_messages)

    def test_7(self):
        """Processed messages count - 2"""
        robot_model = ev3_remoted.ev3_robot_model.Ev3RobotModel()
        self.assertEqual(0, robot_model.processed_messages)
        message = "Wow".encode()
        robot_model.process_incoming_message(message)
        self.assertEqual(1, robot_model.processed_messages)

    def test_8(self):
        """Processed messages count - 3"""
        robot_model = ev3_remoted.ev3_robot_model.Ev3RobotModel()
        self.assertEqual(0, robot_model.processed_messages)
        message = "This is a secret".encode()
        
        number_of_tests = 1000 
        for i in range(0,number_of_tests):
            robot_model.process_incoming_message(message)
        
        self.assertEqual(number_of_tests, robot_model.processed_messages)

if __name__ == '__main__':
    unittest.main()
