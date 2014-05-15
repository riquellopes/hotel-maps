#coding: utf-8
from flask import Flask, request, abort, url_for
from flask_debugtoolbar import DebugToolbarExtension
from instagram import client, subscriptions
from locate_pack.hotelurbano import HotelUrbano

app = Flask(__name__)
app.config.from_object('settings')
toolbar = DebugToolbarExtension(app)
api = client.InstagramAPI(**app.config['CONFIG'])

@app.route('/')
def home():
	response = """
		<form action='{0}'>
			<label>Url Oferta:</label>
			<input type='text' name='q'/>
			<input type='submit'/>
		</form>
	""".format(url_for('gallery_offer'))
	return response

@app.route('/gallery-offer', methods=['GET'])
def gallery_offer():
	h = HotelUrbano(request.args['q'])
	media_popular = api.media_search(lat=h.lat, lng=h.lng, distance=2000, count=50)
	photos = []
	for media in media_popular:
		photos.append("<a href='{1}' target='_blank'><img src='{0}'/ title='{2}'></a>".format(media.images['thumbnail'].url, media.link, media.caption))
	return ''.join(photos)
	
@app.route('/photos/access-token')
def get_galery():
	code = request.values.get('code')
	try:
		access_token, user_info = api.exchange_code_for_access_token(code)
		if not access_token:
			abort(500)
			
		api = client.InstagramAPI(access_token=access_token)
		recent_media, next = api.user_recent_media()
		photos = []
		for media in recent_media:
			photos.append('<img src="%s"/>' % media.images['thumbnail'].url)
		return ''.join(photos)
	except ValueError, e:
		return e