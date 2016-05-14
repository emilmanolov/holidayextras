""" WSGI application """
try:
    # Python 3
    import urllib.parse as urlparse
except ImportError:
    # Python 2.7
    import urlparse

import cgi
import re
import json
import presenters

class WebApp(object):
    """ WSGI Application """

    def __init__(self):
        self.url_map = []

    def set_url_map(self, url_map):
        self.url_map = url_map

    def __call__(self, environ, start_response):
        """ Everything here is run in a separate thread, so special
            attention is needed when accessing (mutating) global data
            (including properties of this class), in order to prevent
            race conditions. """
        return self.wsgi_app(environ, start_response)

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.get_response(request)
        start_response(response.status, response.headers)
        return response.body

    def get_response(self, request):
        try:
            controller_class, params = self.url_map.match(request.path)
            controller = controller_class(request)
            method_name = request.method.lower()
            controller_method = getattr(controller, method_name)
            response = controller_method(**params)
            response = presenters.PresenterFactory().get_presenter(request, response)
            return response
        except Exception as e:
            response = Response()
            response.add_header('Content-Type', 'text/plain')
            response.status = '500 INTERNAL SERVER ERROR'
            response.body = 'Server Error.'
            return response

class UrlMap:

    def __init__(self, url_map):
        self.url_map = []
        for url, cls in url_map:
            self.add_rule(url, cls)

    def add_rule(self, url, cls):
        re_url = re.compile("^%s$" % url)
        self.url_map.append((re_url, url, cls))

    def match(self, url):
        for url_map in self.url_map:
            match = url_map[0].search(url)
            if match is not None:
                return (url_map[2], match.groupdict())
        raise Exception("No URL handler found!")


class Request(object):
    """ HTTP Request """

    def __init__(self, env):
        self._env = env
        self._body = None

    @property
    def path(self):
        return self._env.get('PATH_INFO', '')

    @property
    def uri(self):
        return self._env.get('REQUEST_URI', '')

    @property
    def method(self):
        return self._env.get('REQUEST_METHOD', '')

    @property
    def query(self):
        return self._env.get('QUERY_STRING', '')

    @property
    def headers(self):
        headers = {}
        if self._env.get('CONTENT_TYPE'):
            headers['Content-Type'] = self._env['CONTENT_TYPE']
        if self._env.get('CONTENT_LENGTH'):
            headers['Content-Length'] = self._env['CONTENT_LENGTH']
        for key in self._env:
            if key.startswith('HTTP_'):
                headers[key[5:].replace('_', '-')] = self._env[key]
        return headers

    @property
    def content_length(self):
        try:
            return int(self._env.get('CONTENT_LENGTH', '0'))
        except ValueError:
            pass

    @property
    def body(self):
        if self._body == None:
            if self.content_length:
                self._body = self._env['wsgi.input'].read(self.content_length)
        return self._body

    @property
    def json(self):
        return json.loads(self.body)

class Response(object):
    """ Value object representing the HTTP response. """

    def __init__(self, body='', status='200 OK', headers=[]):
        self.status = status
        self.headers = headers
        self.body = body

    def add_header(self, key, value):
        self.headers.append((key, value))
