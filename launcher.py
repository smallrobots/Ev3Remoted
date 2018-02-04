#################################################################################################
# Ev3TrackedExplor3r                                                                            #
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
import os
from ev3_remoted import *
import ev3te
from ev3te.ev3_tracked_explor3r import Ev3TrackedExplor3r


class Launcher(object):
    """Main class used to launcher the Ev3TrackedExplor3r with remote control"""

    @staticmethod
    def get_ip_address():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        socket_name = s.getsockname()[0]
        s.close()
        return socket_name

    def __init__(self):
        """ Default constructor """
        self.local_ip_address = self.get_ip_address()
        self.local_ip_port = "15999"
        self.robot_model = Ev3TrackedExplor3r()
        self.server = Ev3Server(host_name = self.local_ip_address, host_port = self.local_ip_port,
                                robot_model = self.robot_model)

    def start(self):
        """ Starting point for this application """
        # Check whether the operating system is Windows based or Unix based
        os.system('cls' if os.name == 'nt' else 'clear')

        # Present splash screen
        print("**********************************************************************")
        print("* Ev3 Tracked Explor3r                                               *")
        print("* Smallrobots.it                                                     *")
        print("*                                                                    *")
        print("* Local Ev3 host IP Address: " + self.local_ip_address + "                         *")
        print("* Local Ev3 host IP Port:    " + self.local_ip_port + "                                   *")
        print("*                                                                    *")
        print("* Connect to the IP address and port above with the the remote app.  *")
        print("*                                                                    *")
        print("* Press ctrl-c to stop the Local Ev3 host server                     *")
        print("**********************************************************************")
        self.server.start()
        #self.tracked_explor3r.start()


# Main code
a_launcher = Launcher()
a_launcher.start()
