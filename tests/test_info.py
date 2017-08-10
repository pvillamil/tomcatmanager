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

import requests
import io
import pytest

import tomcatmanager as tm

from test_manager import TestManagerBase


###
#
# test the info type commands, i.e. commands that don't really do anything, they
# just return some information from the server
#
###
class TestInfo(TestManagerBase):

	def test_list(self, tomcat):
		r = tomcat.list()
		self.info_assertions(r)
		assert isinstance(r.apps, list)
	
	def test_server_info(self, tomcat):
		r = tomcat.server_info()
		self.info_assertions(r)
		assert isinstance(r.server_info, tm.models.ServerInfo)
	
	def test_status_xml(self, tomcat):
		r = tomcat.status_xml()
		self.info_assertions(r)
		assert r.result == r.status_xml
		
		assert isinstance(r.status_xml, list)
		assert r.status_xml[0][:6] == '<?xml '

	def test_vm_info(self, tomcat):
		r = tomcat.vm_info()
		self.info_assertions(r)
		assert r.result == r.vm_info

	def test_ssl_connector_ciphers(self, tomcat):
		r = tomcat.ssl_connector_ciphers()
		self.info_assertions(r)
		assert r.result == r.ssl_connector_ciphers
	
	def test_thread_dump(self, tomcat):
		r = tomcat.thread_dump()
		self.info_assertions(r)
		assert r.result == r.thread_dump

	def test_resources_list(self, tomcat):
		r = tomcat.resources()
		self.info_assertions(r)
		assert isinstance(r.resources, dict)

	def test_resources_named_class(self, tomcat):
		r = tomcat.resources('org.apache.catalina.users.MemoryUserDatabase')
		self.info_assertions(r)
		assert isinstance(r.resources, dict)
		assert len(r.resources) == 1
	
	def test_resources_named_class_not_registered(self, tomcat):
		r = tomcat.resources('com.example.Nothing')
		self.info_assertions(r)
		assert isinstance(r.resources, dict)
		assert len(r.resources) == 0

	def test_find_leakers(self, tomcat):
		r = tomcat.find_leakers()
		self.success_assertions(r)
		
		assert isinstance(r.leakers, list)
		# make sure we don't have duplicates
		assert len(r.leakers) == len(set(r.leakers))

	def test_sessions_no_path(self, tomcat):
		"""sessions requires a path"""
		r = tomcat.sessions('')
		self.failure_assertions(r)
		
	def test_sessions(self, tomcat):
		r = tomcat.sessions('/manager')
		self.info_assertions(r)
		assert r.result == r.sessions