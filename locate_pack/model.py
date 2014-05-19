#coding: utf-8
import abc
import json
import hashlib
import urllib2
from opengraph import OpenGraph

class LocatePackException(Exception):
	pass
	
class Base(object):
	__metaclass__ = abc.ABCMeta
	
	def __init__(self, url):
		self.url = url
		self._extract_geo_loc()
		
	def _fetch(self):
		"""
			Get content of offer.
		"""
		return urllib2.urlopen(self.url).read()
		
	@abc.abstractmethod
	def _extract_geo_loc(self):
		"""
			Get geo location of offer.
		"""
		return self
	
	def _extract_open_graph(self):
		"""
			Get all information by OpenGraph.
		"""
		self.generate_id()
		return OpenGraph(url=self.url)
		
	def generate_id(self):
		"""
			Generate key.
		"""
		self.id = hashlib.md5(self.url).hexdigest()
	
	def _get_geo_location_by_google(self):
		"""
			Method get information about offer by google maps.
		"""
		pass
	
	def distance(self, lat, lng):
		"""
			Method calculation the distancie of offer and picture.
		"""
		from geopy.distance import vincenty
		offer = (self.lat, self.lng)
		picture = (lat, lng)
		return vincenty(offer, picture).meters