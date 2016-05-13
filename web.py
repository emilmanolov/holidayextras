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
        response = Response()
        self.dispatch(request, response)
        start_response(response.status, response.headers)
        return response.body

    def dispatch(self, request, response):
        controller_class, params = self.url_map.match(request.path)
        controller = controller_class(request, response)
        method_name = request.method.lower()
        controller_method = getattr(controller, method_name)
        controller_method(**params)
        #presenter = presenters.PresenterFactory().get_presenter(request)
        #response = presenter.get_response()
        try:
            pass
        except Exception as e:
            response.status = '500 INTERNAL SERVER ERROR'
            response.body = 'Server Error.'
            raise e

#class Dispatcher(object):
#
#    def __init__(self, url_map):
#        self.url_map = url_map
#
#    def dispatch(self, request, response):
#        try:
#            controller_class, params = self.url_map.match(request.path)
#            controller = controller_class(request, response)
#            #presenter = presenters.PresenterFactory().get_presenter(request)
#            #response = presenter.get_response()
#        except Exception:
#            response.status = '500'
#            response.headers = []
#            response.body = 'Server Error.'
#
#    def _invoke(self, controller, request):
#        method_name = request.method.lower()
#        controller_method = getattr(controller, method_name)
#        return controller_method(**params)

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
        #controller = getattr(controllers, "Get%s" % controller_name)

class Request(object):
    """ HTTP Request """

    def __init__(self, env):
        self._env = env
        self._body = None
        self.GET = urlparse.parse_qs(self._env.get('QUERY_STRING'))
        self.POST = {}
        """
        if self._env['CONTENT_TYPE'].startswith('multipart/form-data'):
            post_env = self._env.copy()
            post_env['QUERY_STRING'] = ''
            post_data = cgi.FieldStorage(fp=self._env['wsgi.input'],
                                         environ=post_env,
                                         keep_blank_values=True)
            for field in post_data:
                if isinstance(post_data[field], list):
                    # Since it's a list of multiple items, we must have seen more than
                    # one item of the same name come in. Store all of them.
                    self.POST[field] = [fs.value for fs in post_data[field]]
                elif post_data[field].filename:
                    # We've got a file.
                    self.POST[field] = post_data[field]
                else:
                    self.POST[field] = post_data[field].value
        else:
            self.POST = urlparse.parse_qs(self._env['wsgi.input'].read(self.content_length))
        """

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
        return json.dumps(self.body, indent=2)

class Response(object):
    """Value object representing the HTTP response"""

    def __init__(self, body='', status='200 OK', headers=[]):
        self.status = status
        self.headers = headers
        self.body = body

    def add_header(self, key, value):
        self.headers.append((key, value))
        return
