from cgi import escape
from urlparse import parse_qs
from flask import jsonify
from werkzeug.serving import WSGIRequestHandler


class Interceptor(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        print 'Inside call'
        if not (str(environ.get('PATH_INFO')).startswith("/mobile") or str(environ.get('PATH_INFO')).startswith("/login")):
            if environ.get('HTTP_AUTHORIZATION') is not None:
                enc_auth_string = environ.get('HTTP_AUTHORIZATION')
                plain_auth_token = enc_auth_string.decode("base64")
                if plain_auth_token.split(':')[1] != '1234':
                    start_response('403 Permission Denied', [('Content-Type', 'application/json')])
                    return ["Wrong OTP"]
            else:
                print "Authorization needed for this operation"
                start_response('403 Permission Denied', [('Content-Type', 'application/json')])
                return ["Wrong OTP"]

        return self.app(environ, start_response)