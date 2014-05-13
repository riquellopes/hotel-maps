#coding: utf-8
from flask import Flask, request, abort
from flask_debugtoolbar import DebugToolbarExtension
from instagram import client, subscriptions

app = Flask(__name__)
app.config.from_object('settings')
toolbar = DebugToolbarExtension(app)
insta_client = client.InstagramAPI(**app.config['CONFIG'])

@app.route('/')
def home():
	url = insta_client.get_authorize_url(scope=['likes', 'comments'])
	return '<a href="%s">Me conectar com instagram</a>' % url

@app.route('/photos/access-token')
def get_galery():
	code = request.values.get('code')
	try:
		access_token, user_info = insta_client.exchange_code_for_access_token(code)
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