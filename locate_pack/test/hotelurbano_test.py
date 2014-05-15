#coding: utf-8
import unittest
from nose.tools import assert_true, assert_equals, assert_raises
from mock import patch
from locate_pack.hotelurbano import HotelUrbano
from locate_pack.model import LocatePackException
from pack_test import MockUrlLib
import hashlib

class OpenGraphTest(dict):
	
	def __init__(self, *args, **kwargs):
		for k in kwargs:
			self[k] = kwargs.get(k)
		dict.__init__(self)

def generate_id(text):
	return hashlib.md5(text).hexdigest()
		
class HotelUrbanoTest(unittest.TestCase):
	
	@patch('locate_pack.model.urllib2.urlopen')
	@patch('locate_pack.model.OpenGraph')
	def test_o_method__extract_geo_loc_should_be_extract_geo_location_of_48795(self, u, e):
		e.return_value=MockUrlLib('48795')
		u.return_value=OpenGraphTest(
			title='Angra dos Reis, Meliá Angra, 7x de R$ 60,00',
			description='Resort em Meio à Natureza com Gratuidade para Criança*',
			image='http://cdn.hotelurbano.com/images/ofertas/0/48/48795/HU_angra_dos_reis_melia_angra_001_all_normal.jpg'
		)
		d = HotelUrbano('http://www.hotelurbano.com/pacote/rio-de-janeiro-angra-dos-reis-melia-angra/48795')._extract_geo_loc()
		assert_equals(d.lat, -22.948568)
		assert_equals(d.lng, -44.33145)
		assert_equals(d.title, 'Angra dos Reis, Meliá Angra, 7x de R$ 60,00')
		assert_equals(d.description, 'Resort em Meio à Natureza com Gratuidade para Criança*')
		assert_equals(d.image, 'http://cdn.hotelurbano.com/images/ofertas/0/48/48795/HU_angra_dos_reis_melia_angra_001_all_normal.jpg')
		assert_equals(d.id, generate_id(d.url))
		
	@patch('locate_pack.model.urllib2.urlopen')
	@patch('locate_pack.model.OpenGraph')
	def test_o_method__extract_geo_loc_should_be_extract_geo_location_of_47170(self, u, e):
		e.return_value=MockUrlLib('47170')
		u.return_value=OpenGraphTest(
			title='Orlando, Continental Plaza Hotel Kissimmee, 10x de R$ 149,00',
			description='Aéreo de 7 Cidades + Hotel e Aluguel de Carro*',
			image='http://cdn.hotelurbano.com/images/ofertas/0/47/47170/aereo___carro___2015_002_normal.jpg'
		)
		d = HotelUrbano('http://www.hotelurbano.com/pacote/florida-orlando-continental-plaza-hotel-kissimme/47170')._extract_geo_loc()
		assert_equals(d.lat, 28.342418)
		assert_equals(d.lng, -81.598158)
		assert_equals(d.title, 'Orlando, Continental Plaza Hotel Kissimmee, 10x de R$ 149,00')
		assert_equals(d.description, 'Aéreo de 7 Cidades + Hotel e Aluguel de Carro*')
		assert_equals(d.image, 'http://cdn.hotelurbano.com/images/ofertas/0/47/47170/aereo___carro___2015_002_normal.jpg')
		assert_equals(d.id, generate_id(d.url))
	
	@patch('locate_pack.model.urllib2.urlopen')
	def test_case_offer_does_not_(self, u):
		u.return_value=MockUrlLib('36301_sem_mapa')
		with assert_raises(LocatePackException):
			d = HotelUrbano('http://www.hotelurbano.com/pacote/florida-orlando-continental-plaza-hotel-kissimme/47170')._extract_geo_loc()
		