#!/usr/bin/env python3

#################################################################################################
# Unit Testing for class ev3_remoted.ev3_server                                                 #
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
import time
import socket
import json
import random

import ev3_remoted
from ev3_remoted.ev3_server import Ev3Server
from ev3_remoted.ev3_robot_model import Ev3RobotModel
from ev3_remoted.ev3_robot_message import Ev3RobotMessage
from ev3_remoted.ev3_robot_message import MessageType


class ev3_server_ut(unittest.TestCase):
    __remote_host_address = "127.0.0.1"
    __remote_host_port = "60001"
    __default_timeout = 0.5
    __default_buffer_size = 1500

    def test_01(self):
        """Test unit test framework """
        self.assertTrue(1,"Unit test framework working")

    def test_02(self):
        """Instantiate ev3_server class """
        server = ev3_remoted.ev3_server.Ev3Server()
        self.assertIsNotNone (server)

    def test_03(self):
        """Default attributes """
        server = ev3_remoted.ev3_server.Ev3Server()
        self.assertIsNotNone(server)
        self.assertEqual(server.host_name, "localhost")
        self.assertEqual(server.host_port, 60001)
        self.assertEqual(server.controller_host_port, 60002)
        self.assertEqual(server.buffer_size, 1500)
        self.assertIsInstance(server.robot_model, ev3_remoted.ev3_robot_model.Ev3RobotModel)

    def test_04(self):
        """Constructor with arguments """
        robot_model = ev3_remoted.ev3_robot_model.Ev3RobotModel()
        server = ev3_remoted.ev3_server.Ev3Server(robot_model)
        self.assertIsNotNone (server)
        self.assertEqual(server.host_name, "localhost")
        self.assertEqual(server.host_port, 60001)
        self.assertEqual(server.controller_host_port, 60002)
        self.assertEqual(server.buffer_size, 1500)
        self.assertIsInstance(server.robot_model, ev3_remoted.ev3_robot_model.Ev3RobotModel)

    def test_05(self):
        """Constructor with bad arguments type """
        self.assertRaises(ValueError, ev3_remoted.ev3_server.Ev3Server, ("robot_model", 100))

    def test_06(self):
        """Check sender and receiver"""
        robot_model = ev3_remoted.ev3_robot_model.Ev3RobotModel()
        server = ev3_remoted.ev3_server.Ev3Server(robot_model)
        self.assertIsNotNone(server.sender)
        self.assertIsNotNone(server.receiver)

    def test_07(self):
        """Start the sender and receiver thread"""
        # Create a new server
        server = ev3_remoted.ev3_server.Ev3Server()
        # Check that server is not yet running
        self.assertEqual(server.is_running, False)
        # Check server runs
        server.start()
        sleep(0.1)        
        self.assertEqual(server.is_running, True)
        # Check server stops
        server.stop()
        sleep(1.5)
        self.assertEqual(server.is_running, False)

    def test_08(self):
        """Start the sender and receiver thread 10 times"""
        for i in range(1,10):
            # Create a new server
            server = ev3_remoted.ev3_server.Ev3Server()
            # Check that server is not yet running
            self.assertEqual(server.is_running, False)
            # Check server runs
            server.start()
            sleep(0.1)        
            self.assertEqual(server.is_running, True)
            # Check server stops
            server.stop()
            sleep(0.2)
            self.assertEqual(server.is_running, False)

    def test_09(self):
        """Instantiate a robot_model and associate it to a server"""
        # Define a robot class and instantiant an instance
        class my_robot_class(ev3_remoted.ev3_robot_model.Ev3RobotModel):
            def __init__(self):
                super(my_robot_class,self).__init__()
                self.my_important_variable = 150.1
        my_robot = my_robot_class()   
        
        # Instantiate a server
        server = ev3_remoted.ev3_server.Ev3Server(robot_model = my_robot)
        # Check that server is not yet running
        self.assertEqual(server.is_running, False)
        # Check server runs
        server.start()
        sleep(0.1)        
        self.assertEqual(server.is_running, True)
        # Check server stops
        server.stop()
        sleep(0.2)
        self.assertEqual(server.is_running, False)

    def test_10(self):
        """Instantiate a robot_model and associate it to a server, then launch the server,
then a UDP packet is sent to the server"""
        # Define a robot class and instantiant an instance
        class my_robot_class(ev3_remoted.ev3_robot_model.Ev3RobotModel):
            def __init__(self):
                super(my_robot_class,self).__init__()
                self.my_important_variable = 150.1
        my_robot = my_robot_class()   
        
        # Instantiate a server
        server = ev3_remoted.ev3_server.Ev3Server(robot_model = my_robot)
        server.host_name = self.__remote_host_address

        # Check that server is not yet running
        self.assertEqual(server.is_running, False)
        # Check server runs
        server.start()
        sleep(0.1)        
        self.assertEqual(server.is_running, True)

        # Prepare a UDP message and send it
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = (self.__remote_host_address, int(self.__remote_host_port))
        message = 'E.T. Calling Home'
        encoded_message = message.encode('utf8')
            
        sent = 0
        try:
            sent = sock.sendto(encoded_message, server_address)
        finally:
            sock.close()
            
        # Check server stops
        server.stop()
        sleep(0.2)
        self.assertEqual(server.is_running, False)

    def test_11(self):
        """Instantiate a robot_model and associate it to a server, then launch the server,
then a UDP packet is sent to the server
Then check that the robot_model has processed the message"""
        # Define a robot class and instantiant an instance
        class my_robot_class(ev3_remoted.ev3_robot_model.Ev3RobotModel):
            def __init__(self):
                super(my_robot_class,self).__init__()
                self.my_important_variable = 150.1
        my_robot = my_robot_class()   
        
        # Hostport
        remote_host_port = 60011

        # Instantiate a server
        server = ev3_remoted.ev3_server.Ev3Server(robot_model = my_robot)
        server.host_name = self.__remote_host_address
        server.host_port = remote_host_port

        # Assert host port
        self.assertEqual(server.host_port, remote_host_port)
        self.assertEqual(server.receiver.host_port, remote_host_port)

        # Assert that No outbound message has been processed yet
        self.assertEqual(server.robot_model.processed_messages, 0)

        # Check that server is not yet running
        self.assertEqual(server.is_running, False)
        # Check server runs
        server.start()
        sleep(0.1)        
        self.assertEqual(server.is_running, True)

        # Prepare a UDP message and send it
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = (self.__remote_host_address, int(remote_host_port))
        message = 'E.T. Calling Home'
        encoded_message = message.encode('utf8')
            
        sent = 0
        try:
            sent = sock.sendto(encoded_message, server_address)
        finally:
            sock.close()
            
        # Check server stops
        server.stop()
        sleep(0.2)
        self.assertEqual(server.is_running, False)

        # Assert that the outbound message has been sent
        self.assertEqual(sent, len(message))

        # Assert that the outbound message has been processed
        self.assertEqual(server.robot_model.processed_messages, 1)

    def test_12(self):
        """Property testing"""
        # Instantiate a server
        server = ev3_remoted.ev3_server.Ev3Server()

        for buffer_size in range (500,4096):
            server.buffer_size = buffer_size

            self.assertEqual(server.buffer_size, buffer_size)
            self.assertEqual(server.sender.buffer_size, buffer_size)
            self.assertEqual(server.receiver.buffer_size, buffer_size)

    def test_13(self):
        """Property testing"""
        # Instantiate a server
        server = ev3_remoted.ev3_server.Ev3Server()

        partialAddress = "192.168.1."

        for fourthOctet in range (1,254):
            completeAddress = partialAddress + str(fourthOctet)
            server.host_name = completeAddress

            self.assertEqual(server.host_name, completeAddress)
            self.assertEqual(server.sender.host_name, completeAddress)
            self.assertEqual(server.receiver.host_name, completeAddress)

    def test_14(self):
        """Property testing"""
        # Instantiate a server
        server = ev3_remoted.ev3_server.Ev3Server()

        for host_port in range (500,61000):
            server.host_port = host_port

            self.assertEqual(server.host_port, host_port)
            self.assertEqual(server.sender.host_port, host_port)
            self.assertEqual(server.receiver.host_port, host_port)

    def test_15(self):
        """Property testing"""
        # Instantiate a server
        server = ev3_remoted.ev3_server.Ev3Server()

        for controller_host_port in range (500,61000):
            server.controller_host_port = controller_host_port

            self.assertEqual(server.controller_host_port, controller_host_port)
            self.assertEqual(server.sender.controller_host_port, controller_host_port)
            self.assertEqual(server.receiver.controller_host_port, controller_host_port)

    def test_16(self):
        """Property testing"""
        # Instantiate a server
        server = ev3_remoted.ev3_server.Ev3Server()

        # Instantiate a robot model
        robot_name = "Mazinga Z"
        robot_model = ev3_remoted.ev3_robot_model.Ev3RobotModel(robot_name)

        # Associate to the server
        server.robot_model = robot_model

        # Test
        self.assertEqual(server.robot_model.robot_name, robot_name)
        self.assertEqual(server.sender.robot_model.robot_name, robot_name)
        self.assertEqual(server.receiver.robot_model.robot_name, robot_name)
    
    def test_17(self):
        """Instantiate a robot_model_message
Instantiate a robot_model and associate it to a server, then launch the server,
then a UDP packet is sent to the server
Then check that the robot_model has processed the message
Then check that the robot_model has been updated according to the message received"""
        class my_robot_message(ev3_remoted.ev3_robot_message.Ev3RobotMessage):
            def __init(self):
                super(my_robot_message, self).__init__()
                self.my_important_status = 0
                self.my_important_set_point = 0

            @staticmethod
            def object_decoder(obj):
                decoded_object = my_robot_message()
                decoded_object = super(my_robot_message, my_robot_message).object_decoder(obj)
                decoded_object.my_important_set_point = obj['my_important_set_point']
                return decoded_object

        # Define a robot class and instantiant an instance
        class my_robot_class(ev3_remoted.ev3_robot_model.Ev3RobotModel):
            def __init__(self):
                super(my_robot_class, self).__init__()
                self.my_important_status = 150.1
                self.my_important_set_point = 25

            def process_incoming_message(self, message):
                super().process_incoming_message(message)
                message_str = str (message,'utf-8')
                decodedMessage = json.loads(message_str, object_hook=my_robot_message.object_decoder)
                self.my_important_set_point = decodedMessage.my_important_set_point
                return decodedMessage
                

        my_robot = my_robot_class() 
        
        # Hostport
        remote_host_port = 60011

        # Instantiate a server
        server = ev3_remoted.ev3_server.Ev3Server(robot_model = my_robot)
        server.host_name = self.__remote_host_address
        server.host_port = remote_host_port

        # Assert host port
        self.assertEqual(server.host_port, remote_host_port)
        self.assertEqual(server.receiver.host_port, remote_host_port)

        # Assert that No outbound message has been processed yet
        self.assertEqual(server.robot_model.processed_messages, 0)

        # Check that server is not yet running
        self.assertEqual(server.is_running, False)
        # Check server runs
        server.start()
        sleep(0.1)        
        self.assertEqual(server.is_running, True)

        # Prepare a UDP message and send it
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = (self.__remote_host_address, int(remote_host_port))
        message = my_robot_message()
        message.my_important_set_point = 100
        message_str = json.dumps(message, default=message.json_default)
        encoded_message = str.encode(message_str, encoding = 'utf-8')

        sent = 0
        try:
            sent = sock.sendto(encoded_message, server_address)
        finally:
            sock.close()
            
        # Check server stops
        server.stop()
        sleep(0.2)
        self.assertEqual(server.is_running, False)

        # Assert that the outbound message has been sent
        self.assertEqual(sent, len(message_str))

        # Assert that the outbound message has been processed
        self.assertEqual(server.robot_model.processed_messages, 1)

        # Assert that the robot status has been updated
        self.assertEqual(server.robot_model.my_important_set_point, message.my_important_set_point)

    def test_18(self):
        """Instantiate a robot_model_message
Instantiate a robot_model and associate it to a server, then launch the server,
then a UDP packet is sent to the server
Then check that the robot_model has processed the message
Then check that the robot_model has been updated according to the message received
Test is repeated 100 times"""
        class my_robot_message(ev3_remoted.ev3_robot_message.Ev3RobotMessage):
            def __init(self):
                super(my_robot_message, self).__init__()
                self.my_important_status = 0
                self.my_important_set_point = 0

            @staticmethod
            def object_decoder(obj):
                decoded_object = my_robot_message()
                decoded_object = super(my_robot_message, my_robot_message).object_decoder(obj)
                decoded_object.my_important_set_point = obj['my_important_set_point']
                return decoded_object

        # Define a robot class and instantiant an instance
        class my_robot_class(ev3_remoted.ev3_robot_model.Ev3RobotModel):
            def __init__(self):
                super(my_robot_class, self).__init__()
                self.my_important_status = 150.1
                self.my_important_set_point = 25
            def process_incoming_message(self, message):
                super().process_incoming_message(message)
                message_str = str (message,'utf-8')
                decodedMessage = json.loads(message_str, object_hook=my_robot_message.object_decoder)
                self.my_important_set_point = decodedMessage.my_important_set_point
                return decodedMessage

        my_robot = my_robot_class() 
        
        # Hostport
        remote_host_port = 60012

        # Instantiate a server
        server = ev3_remoted.ev3_server.Ev3Server(robot_model = my_robot)
        server.host_name = self.__remote_host_address
        server.host_port = remote_host_port

        # Assert host port
        self.assertEqual(server.host_port, remote_host_port)
        self.assertEqual(server.receiver.host_port, remote_host_port)

        # Assert that No outbound message has been processed yet
        self.assertEqual(server.robot_model.processed_messages, 0)

        # Check that server is not yet running
        self.assertEqual(server.is_running, False)
        # Check server runs
        server.start()
        sleep(0.1)        
        self.assertEqual(server.is_running, True)

        # Open the outbound socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = (self.__remote_host_address, int(remote_host_port))

        # Repeat 100 times
        numberOfMessages = 100
        tolerance = 0.2
        my_important_set_point = random.randrange(0, 1000)

        for i in range(0, numberOfMessages):
            # Prepare a UDP message and send it         
            message = my_robot_message()
            message.my_important_set_point = my_important_set_point
            message_str = json.dumps(message, default=message.json_default)
            encoded_message = str.encode(message_str, encoding = 'utf-8')

            sent = 0
            sent = sock.sendto(encoded_message, server_address)

            # Assert that the outbound message has been sent
            self.assertEqual(sent, len(message_str))

            # Wait a bit
            sleep(0.1)

            # Assert that the robot status has been updated
            self.assertEqual(server.robot_model.my_important_set_point, my_important_set_point)
                        
        # Check server stops
        server.stop()
        sleep(0.2)
        self.assertEqual(server.is_running, False)

        # Assert that all the outbound messages have been processed
        self.assertAlmostEqual(server.robot_model.processed_messages, numberOfMessages, delta = tolerance*numberOfMessages)

    def test_19(self):
        """Instantiate a robot_model_message
Instantiate a robot_model and associate it to a server, then launch the server,
then a UDP packet is sent to the server
Check that the first message received transfers that host address and port to reply back"""
        class my_robot_message(ev3_remoted.ev3_robot_message.Ev3RobotMessage):
            def __init(self):
                super(my_robot_message, self).__init__()
                self.my_important_status = 0
                self.my_important_set_point = 0

            @staticmethod
            def object_decoder(obj):
                decoded_object = super(my_robot_message, my_robot_message).object_decoder(obj)
                decoded_object.my_important_set_point = obj['my_important_set_point']
                return decoded_object

        # Define a robot class and instantiate an instance
        class my_robot_class(ev3_remoted.ev3_robot_model.Ev3RobotModel):
            def __init__(self):
                super(my_robot_class, self).__init__()
                self.my_important_status = 150.1
                self.my_important_set_point = 25

            def process_incoming_message(self, message):
                super().process_incoming_message(message)
                message_str = str (message,'utf-8')
                decodedMessage = json.loads(message_str, object_hook=my_robot_message.object_decoder)
                self.my_important_set_point = decodedMessage.my_important_set_point
                return decodedMessage

        my_robot = my_robot_class() 
        
        # Hostport
        remote_host_port = 60013

        # Instantiate a server
        server = ev3_remoted.ev3_server.Ev3Server(robot_model = my_robot)
        server.host_name = self.__remote_host_address
        server.host_port = remote_host_port

        # Assert server host port
        self.assertEqual(server.host_port, remote_host_port)
        self.assertEqual(server.receiver.host_port, remote_host_port)

        # Open the outbound socket
        outbound_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = (self.__remote_host_address, int(remote_host_port))

        # Check that server is not yet running
        self.assertEqual(server.is_running, False)

        # Check server runs
        server.start()
        sleep(0.1)        
        self.assertEqual(server.is_running, True)

        # Prepare the first UDP message and send it    
        remote_controller_name = "Test 19"
        remote_controller_address = "127.0.0.1"
        remote_controller_port = 65000
        
        message = my_robot_message()
        message.remote_controller_name = remote_controller_name
        message.remote_controller_address = remote_controller_address
        message.remote_controller_port = remote_controller_port
        message.message_function = MessageType.subscribe
        message.my_important_set_point = 10
        message_str = json.dumps(message, default=message.json_default)
        encoded_message = str.encode(message_str, encoding = 'utf-8')

        sent = outbound_socket.sendto(encoded_message, server_address)

        # Assert that the outbound message has been sent
        self.assertEqual(sent, len(message_str))

        # Wait a bit
        sleep(1)

        # Assert that the outbound message has been processed
        self.assertEqual(server.robot_model.processed_messages, 1)

        # Assert that the robot status has been updated
        print("Test19: (remote_controller_address, remote_controller_port) - "
              + str((remote_controller_address, remote_controller_port)))
        print("Test19: server.remote_controllers_list - " + str(server.remote_controllers_list))
        self.assertEqual(True, (remote_controller_address, remote_controller_port) in server.remote_controllers_list)
                        
        # Check server stops
        server.stop()
        sleep(0.2)
        self.assertEqual(server.is_running, False)

    def test_20(self):
        """Instantiate a robot_model_message with a _subscribe_ command
           Checks that the sever start sending periodic messages with robot status
           until a message with _unsubscribe_ command is received"""
        class MyRobotMessage(Ev3RobotMessage):
            def __init(self):
                super(MyRobotMessage, self).__init__()
                self.my_important_status = 0
                self.my_important_set_point = 0

            @staticmethod
            def object_decoder(obj):
                decoded_object = super(MyRobotMessage, MyRobotMessage).object_decoder(obj)
                decoded_object.my_important_set_point = obj['my_important_set_point']
                return decoded_object

        # Define a robot class and instantiate an instance
        class MyRobotClass(Ev3RobotModel):
            def __init__(self):
                super(MyRobotClass, self).__init__()
                self.my_important_status = 150.1
                self.my_important_set_point = 25

            def process_incoming_message(self, message):
                super().process_incoming_message(message)
                message_str = str(message, 'utf-8')
                decoded_message = json.loads(message_str, object_hook=MyRobotMessage.object_decoder)
                self.my_important_set_point = decoded_message.my_important_set_point
                return decoded_message

        my_robot = MyRobotClass()
        
        # Robot port
        robot_host_port = 60013
        robot_host_address = "192.168.1.152"

        # Instantiate a server
        robot_server = Ev3Server(robot_model = my_robot)
        robot_server.host_name = robot_host_address
        robot_server.host_port = robot_host_port

        # Assert server host port
        self.assertEqual(robot_server.host_port, robot_host_port)
        self.assertEqual(robot_server.receiver.host_port, robot_host_port)

        # Open the outbound socket and declare the server_address
        # This test case acts as the remote_controller
        outbound_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        robot_server_address = (robot_host_address, int(robot_host_port))

        # Check that server is not yet running
        self.assertEqual(robot_server.is_running, False)

        # Check server runs
        print("ev3_server_ur.test_20: server starting...")
        try:
            robot_server.start()
            sleep(5)
            print("ev3_server_ur.test_20: No exception raised")
        except BaseException as e:
            print("ev3_server_ur.test_20: Exception raised: " + str(e))

        self.assertEqual(robot_server.is_running, True)

        # Prepare the first UDP message and send it    
        remote_controller_name = "Test 20"
        remote_controller_address = "192.168.1.152"
        remote_controller_port = 65000

        # Define a message of type subscribe
        message = MyRobotMessage()
        message.remote_controller_name = remote_controller_name
        message.remote_controller_address = remote_controller_address
        message.remote_controller_port = remote_controller_port
        message.my_important_set_point = 10
        message.message_function = MessageType.subscribe
        message_str = json.dumps(message, default = message.json_default)
        print("Test20: message_str - " + message_str)
        encoded_message = str.encode(message_str, encoding = 'utf-8')

        print(robot_server_address)

        number_of_message_sent = 10
        for x in range(0, number_of_message_sent):
            try:
                sent = outbound_socket.sendto(encoded_message, robot_server_address)
                print("Test20: message sent at robot_server with address - " + str(robot_server_address))
            except BaseException as theException:
                print(theException)

            # Assert that the outbound message has been sent
            self.assertEqual(sent, len(message_str))

            sleep(0.1)

        # Wait a bit
        sleep(1)

        # Assert that the outbound message has been processed
        self.assertEqual(robot_server.robot_model.processed_messages, number_of_message_sent)

        # Checks that the server has updated the list of remote controllers
        print("Test20: robot_server.remote_controllers_list - " + str(robot_server.remote_controllers_list))
        print("Test20: (remote_controller_address, remote_controller_port) - " +
              str((remote_controller_address, remote_controller_port)))
        self.assertEqual(True, (remote_controller_address, remote_controller_port) in
                         robot_server.remote_controllers_list)
        
        # Create the inbound socket 
        inbound_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        remote_controller = (remote_controller_address, int(remote_controller_port))

        # Bind the inbound socket
        inbound_sock.bind(remote_controller)
        inbound_sock.settimeout(self.__default_timeout)

        number_of_message_received = 0
        start_time = time.time()
        current_time = time.time()
        # Main loop
        while current_time - start_time < 10:
            try:
                current_time = time.time()
                print(current_time - start_time)
                data, robot_server_address_as_received = inbound_sock.recvfrom(self.__default_buffer_size)
                number_of_message_received = number_of_message_received + 1
            except socket.timeout:
                continue

        # Check at least 10 messages have been received
        # self.assertEqual(10, number_of_message_received)
        self.assertGreater(number_of_message_received, 10)

        ####
        # Now send an unsubscribe message
        ####

        # Define a message of type unsubscribe
        message = MyRobotMessage()
        message.remote_controller_name = remote_controller_name
        message.remote_controller_address = remote_controller_address
        message.remote_controller_port = remote_controller_port
        message.my_important_set_point = 10
        message.message_function = MessageType.unsubscribe
        message_str = json.dumps(message, default = message.json_default)
        print("Test20: message_str - " + message_str)
        encoded_message = str.encode(message_str, encoding = 'utf-8')

        print(robot_server_address)

        number_of_message_sent = 1
        for x in range(0, number_of_message_sent):
            try:
                sent = outbound_socket.sendto(encoded_message, robot_server_address)
                print("Test20: message sent at robot_server with address - " + str(robot_server_address))
            except BaseException as theException:
                print(theException)

            # Assert that the outbound message has been sent
            self.assertEqual(sent, len(message_str))

            sleep(0.1)

        # Check that server stops sending message because of the unsubscribe message
        number_of_message_received = 0
        start_time = time.time()
        current_time = time.time()
        # Main loop
        while current_time - start_time < 10:
            try:
                current_time = time.time()
                data, robot_server_address_as_received = inbound_sock.recvfrom(self.__default_buffer_size)
                number_of_message_received = number_of_message_received + 1
            except socket.timeout:
                continue

        # Check at least 10 messages have been received
        # self.assertEqual(10, number_of_message_received)
        self.assertLess(number_of_message_received, 10)

        # Check server stops
        robot_server.stop()
        sleep(0.2)
        self.assertEqual(robot_server.is_running, False)

if __name__ == '__main__':
    unittest.main()
