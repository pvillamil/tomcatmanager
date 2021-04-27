#
# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 Jared Crapo
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# pylint: disable=too-many-lines, too-many-public-methods

"""
Mock up a Tomcat Manager application that behaves like tomcat version 7.0.x
"""

import socket
import threading

from http.server import HTTPServer

from tests.mock_server_nossl import MockRequestHandlerNoSSL


class MockRequestHandler70(MockRequestHandlerNoSSL):
    """Handle HTTP Requests like Tomcat Manager 7.0.x"""

    def get_server_info(self):
        """Send the server information."""
        self.send_text(
            """OK - Server info
Tomcat Version: [Apache Tomcat/7.0.108]
OS Name: [Linux]
OS Version: [5.4.0-72-generic]
OS Architecture: [amd64]
JVM Version: [14.0.2+12-Ubuntu-120.04]
JVM Vendor: [Private Build]"""
        )


###
#
#
###
def start_mock_server_7_0(tms):
    """Start a mock Tomcat Manager application

    :return: a tuple: (url, user, password) where the server is accessible
    """
    # pylint: disable=unused-variable
    # go find an unused port
    sock = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    sock.bind(("localhost", 0))
    address, port = sock.getsockname()
    sock.close()

    tms.url = "http://localhost:{}/manager".format(port)
    tms.user = MockRequestHandler70.USER
    tms.password = MockRequestHandler70.PASSWORD
    tms.warfile = "/path/to/server.war"
    tms.contextfile = "path/to/context.xml"
    tms.connect_command = "connect {} {} {}".format(tms.url, tms.user, tms.password)

    mock_server = HTTPServer(("localhost", port), MockRequestHandler70)
    mock_server_thread = threading.Thread(target=mock_server.serve_forever)
    mock_server_thread.daemon = True
    mock_server_thread.start()

    return tms
