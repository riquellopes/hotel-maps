#coding: utf-8
import unittest
from nose.tools import assert_true, assert_raises, assert_equals, assert_false
from mock import patch
from locate_pack.pack import Base

class MockUrlLib(object):
	
	def __init__(self, _file, _type='html', code=200, msg='OK', headers={'content-type': 'text/plain; charset=utf-8'}):
		self.file_test = ("%s.%s" % (_file, _type))
		self.code = code
		self.msg = msg
		self.headers = headers
		
	def read(self):
		handle = open(self.file_test)
		html = "".join( handle )
		return html

class Dummy(Base):
	
	def _extract_geo_loc(self):
		pass
		
class PackTest(unittest.TestCase):
	
	@patch('locate_pack.urllib2.urlopen')
	def test_method_fetch_should_be_get_valid_html_of_site(self, u):
		"""
			Method fetch should be get a valid html of site.
		"""
		mock = MockUrlLib('48795')
		u.return_value=mock
		d = Dummy('http://www.hotelurbano.com/pacote/rio-de-janeiro-angra-dos-reis-melia-angra/48795')._fetch()
		assert_equals(d, mock.read())
	
	@patch('locate_pack.urllib2.urlopen')
	def test_method_should_be_extract_information_open_graph(self, u):
		pass