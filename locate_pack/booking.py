#coding: utf-8
from BeautifulSoup import BeautifulSoup
from model import Base

class Booking(Base):
	
	def _extract_geo_loc(self):
		soup = BeautifulSoup( self._fetch() )
		self.lat = float(soup.find('meta', {'property':'booking_com:location:latitude'})['content'])
		self.lng = float(soup.find('meta', {'property':'booking_com:location:longitude'})['content'])
		data = self._extract_open_graph()
		self.title = data['title']
		self.description = data['description']
		self.image = data['image']
		return super(Booking, self)._extract_geo_loc()