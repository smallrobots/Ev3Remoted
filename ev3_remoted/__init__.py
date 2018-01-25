#################################################################################################
# ev3_remoted package                                                                           #
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

# Class in this package
from .ev3_receiver import Ev3Receiver
from .ev3_remote_controller import Ev3RemoteController
from .ev3_robot_message import MessageType
from .ev3_robot_message import Ev3RobotMessage
from .ev3_sender import Ev3Sender
from .ev3_server import Ev3Server

# Logger
import logging

# Create the logger used in this package
ev3_logger = logging.getLogger(__name__)
ev3_logger.setLevel(logging.DEBUG)

# Logger settings
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
ev3_logger.addHandler(handler)

# First message
ev3_logger.info("Logger created for the ev3_remoted package")


