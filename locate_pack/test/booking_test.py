#coding: utf-8
import unittest
from nose.tools import assert_true, assert_equals
from mock import patch
from locate_pack.booking import Booking
from hotelurbano_test import OpenGraphTest
from pack_test import MockUrlLib

class BookingTest(unittest.TestCase):
	
	@patch('locate_pack.model.urllib2.urlopen')
	@patch('locate_pack.model.OpenGraph')
	def test_the_method__extract_geo_loc_should_be_extract_information_about_pack_123(self, e, u):
		u.return_value = MockUrlLib('booking_1')
		e.return_value = OpenGraphTest(
			title='\u2605\u2605\u2605\u2605 Best Western Plus Sol Ipanema Hotel, Rio de Janeiro, Brazil',
			description='Best Western Plus Sol Ipanema offers a superb location on the Ipanema Beach seafront, within a vibrant area of bars and restaurants.*',
			image='http://q-ec.bstatic.com/images/hotel/max300/252/25216239.jpg'
		)
		d = Booking('http://www.booking.com/hotel/br/best-western-sol-ipanema.en-gb.html')._extract_geo_loc()
		assert_equals(d.lat, -22.986452891152172)
		assert_equals(d.lng, -43.203330055603146)
		assert_equals(d.title, '\u2605\u2605\u2605\u2605 Best Western Plus Sol Ipanema Hotel, Rio de Janeiro, Brazil')
		assert_equals(d.description, 'Best Western Plus Sol Ipanema offers a superb location on the Ipanema Beach seafront, within a vibrant area of bars and restaurants.*')
		assert_equals(d.image, 'http://q-ec.bstatic.com/images/hotel/max300/252/25216239.jpg')