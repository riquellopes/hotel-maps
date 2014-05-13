#coding: utf-8
try:
	from local_config import *
except ImportError:
	from os import path, environ
	DEBUG=environ.get('DEBUG')
	APP_ID=environ.get('APP_ID')
	SECRET_KEY=environ.get('SECRET_KEY')
	CONFIG = {
		'client_id':environ.get('CLIENT_ID'),
		'client_secret':environ.get('CLIENT_SECRET'),
		'redirect_uri':environ.get('REDIRECT_URI')
	}

