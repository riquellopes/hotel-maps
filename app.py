#coding: utf-8
import json
from flask import Flask, request, abort, url_for, render_template, jsonify, Response
from flask_debugtoolbar import DebugToolbarExtension
from instagram import client, subscriptions
from locate_pack.hotelurbano import HotelUrbano, LocatePackException

app = Flask(__name__)
app.config.from_object('settings')
toolbar = DebugToolbarExtension(app)
api = client.InstagramAPI(**app.config['CONFIG'])

@app.route('/')
def home():
	return render_template('index.html', **locals())

@app.route('/offer.json', methods=['GET'])
def gallery_offer():
	try:
		h = HotelUrbano(request.args['q'])
		media = api.media_search(lat=h.lat, lng=h.lng, distance=2000, count=100)
		offer = {
			"id":h.id,
			"title":h.title,
			"description":h.description,
			"src":h.image,
			"lat":h.lat,
			"lng":h.lng,
			"link":request.args['q']
		}
		photo = []
		for m in media:
			photo.append({"lat":m.location.point.latitude, 
						  "lng":m.location.point.longitude, 
						  "distance":h.distance(m.location.point.latitude, m.location.point.longitude),
						  "src":m.images['thumbnail'].url, 
						  "comment":"", "link":m.link})
		return Response(json.dumps({"offer":offer, "photos":photo}, ensure_ascii=False), mimetype='application/json; charset=utf-8')
	except LocatePackException as e:
		return jsonify(msg="Error", status=500)
		
#def get_galery():
#	code = request.values.get('code')
#	try:
#		access_token, user_info = api.exchange_code_for_access_token(code)
#		if not access_token:
#			abort(500)
#		api = client.InstagramAPI(access_token=access_token)
#		recent_media, next = api.user_recent_media()
#		photos = []
#		for media in recent_media:
#			photos.append('<img src="%s"/>' % media.images['thumbnail'].url)
#		return ''.join(photos)
#	except ValueError, e:
#		return e