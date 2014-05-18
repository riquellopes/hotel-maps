#coding: utf-8
import re
import json
from urlparse import parse_qs
from BeautifulSoup import BeautifulSoup
from model import Base, LocatePackException

class HotelUrbano(Base):
	
	def _extract_geo_loc(self):
		soup = BeautifulSoup( self._fetch() )
		try:
			q = json.dumps( parse_qs(soup.findAll('iframe', {'class':'bdFull'})[0].get('src')) )
			geo = json.loads(q)['ll'][0].split(',')
		except IndexError as e:
			raise LocatePackException(e)
			
		self.lat = float(geo[0])
		self.lng = float(geo[1])
		
		## Get other informations about pack by OpenGraph.
		data = self._extract_open_graph()
		self.title = data['title']
		self.description = data['description']
		self.image = data['image']
		
		return super(HotelUrbano, self)._extract_geo_loc()