#
# -*- coding: utf-8 -*-
# pylint: disable=missing-function-docstring, missing-module-docstring
# pylint: disable=missing-class-docstring, redefined-outer-name

import os

import pytest

import tomcatmanager as tm

###
#
# helper class
#
###
class TomcatServer:
    # pylint: disable=too-few-public-methods
    def __init__(self):
        self.url = None
        self.user = None
        self.password = None
        self.warfile = None
        self.contextfile = None
        self.connect_command = None


###
#
# add command line options
#
###
def pytest_addoption(parser):
    parser.addoption(
        "--mocktomcat",
        action="store",
        default=tm.TomcatMajorMinor.highest_supported().value,
        choices=list(map(lambda v: v.value, tm.TomcatMajorMinor.supported())),
        help="test against a specific mock version of Tomcat",
    )
    parser.addoption(
        "--url",
        action="store",
        default=None,
        help="url of tomcat manager to test against instead of mock server",
    )
    parser.addoption(
        "--user", action="store", default=None, help="use to authenticate at url"
    )
    parser.addoption(
        "--password", action="store", default=None, help="use to authenticate at url"
    )
    parser.addoption(
        "--warfile",
        action="store",
        default=None,
        help="path to deployable war file on the tomcat server",
    )
    parser.addoption(
        "--contextfile",
        action="store",
        default=None,
        help="path to context.xml file on the tomcat server",
    )


###
#
# fixtures
#
###

# use a fixture to return a class with a bunch
# of assertion helper methods
@pytest.fixture
def assert_tomcatresponse():
    """
    Assertions for every command that should complete successfully.
    """

    class AssertResponse:
        def success(self, r):
            """Assertions on TomcatResponse for calls that should be successful."""
            assert (
                r.status_code == tm.StatusCode.OK
            ), 'message from server: "{}"'.format(r.status_message)
            assert r.status_message
            r.raise_for_status()

        def failure(self, r):
            """Assertions on TomcatResponse for calls that should fail."""
            assert r.status_code == tm.StatusCode.FAIL
            with pytest.raises(tm.TomcatError):
                r.raise_for_status()

        def info(self, r):
            """Assertions on TomcatResponse for info-type commands that should be successful."""
            self.success(r)
            assert r.result

    return AssertResponse()


###
#
# fixtures for testing TomcatManager()
#
###
@pytest.fixture(scope="session")
def tomcat_manager_server(request):
    """start a local http server which provides a similar interface to a
    real Tomcat Manager app"""
    url = request.config.getoption("--url")
    tms = TomcatServer()
    if url:
        # use the server info specified on the command line
        tms.url = url
        tms.user = request.config.getoption("--user")
        tms.password = request.config.getoption("--password")
        tms.warfile = request.config.getoption("--warfile")
        tms.contextfile = request.config.getoption("--contextfile")
        tms.connect_command = "connect {} {} {}".format(tms.url, tms.user, tms.password)
        return tms
    else:
        # go start up a fake server
        mockver = request.config.getoption("--mocktomcat")
        if mockver == tm.TomcatMajorMinor.V10_0.value:
            from tests.mock_server_10_0 import start_mock_server_10_0

            return start_mock_server_10_0(tms)
        elif mockver == tm.TomcatMajorMinor.V9_0.value:
            from tests.mock_server_9_0 import start_mock_server_9_0

            return start_mock_server_9_0(tms)
        elif mockver == tm.TomcatMajorMinor.V8_5.value:
            from tests.mock_server_8_5 import start_mock_server_8_5

            return start_mock_server_8_5(tms)
        elif mockver == tm.TomcatMajorMinor.V8_0.value:
            from tests.mock_server_8_0 import start_mock_server_8_0

            return start_mock_server_8_0(tms)
        elif mockver == tm.TomcatMajorMinor.V7_0.value:
            from tests.mock_server_7_0 import start_mock_server_7_0

            return start_mock_server_7_0(tms)


@pytest.fixture
def tomcat(tomcat_manager_server):
    tmcat = tm.TomcatManager()
    tmcat.connect(
        tomcat_manager_server.url,
        tomcat_manager_server.user,
        tomcat_manager_server.password,
    )
    return tmcat


@pytest.fixture
def localwar_file():
    """return the path to a valid war file"""
    return os.path.dirname(__file__) + "/tests/war/sample.war"


@pytest.fixture
def safe_path():
    """a safe path we can deploy apps to"""
    return "/tomcat-manager-test-app"


@pytest.fixture
def server_info():
    return """Tomcat Version: Apache Tomcat/8.0.32 (Ubuntu)
OS Name: Linux
OS Version: 4.4.0-89-generic
OS Architecture: amd64
JVM Version: 1.8.0_131-8u131-b11-2ubuntu1.16.04.3-b11
JVM Vendor: Oracle Corporation
"""
