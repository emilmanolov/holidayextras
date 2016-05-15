""" HTTP content negotioation module. """
import json

class PresenterFactory(object):
    """ Creates a proper presenter object based on the 'Accept' header
        in the HTTP request.
    """
    def get_presenter(self, request, response):
        header_accept = request.headers['ACCEPT']
        if 'application/json' in header_accept:
            return JsonPresenter(response, json)
        elif 'application/xml' in header_accept:
            return XmlPresenter(response)
        else:
            return TextPresenter(response)


class JsonPresenter(object):

    def __init__(self, response, json):
        self.response = response
        self.json = json

    @property
    def status(self):
        return self.response.status

    @property
    def headers(self):
        headers = self.response.headers
        headers.append(('Content-Type', 'application/json'))
        return headers

    @property
    def body(self):
        return self.json.dumps(self.response.body, indent=2)


class XmlPresenter(object):

    def __init__(self, response):
        self.response = response

    @property
    def status(self):
        return self.response.status

    @property
    def headers(self):
        headers = self.response.headers
        headers.append(('Content-Type', 'application/xml'))
        return headers

    @property
    def body(self):
        xml = self._serialize(self.response.body)
        return str(xml)

    def _serialize(self, data, root_name='item'):

        def get_node(tag, value):
            return '<{tag}>{value}</{tag}>'.format(tag=tag, value=value)

        xml = ''
        if isinstance(root[key], dict):
            for key in data.keys():
                xml = xml + get_node(key, data[key])

        return get_node(root_name, xml)


class TextPresenter(object):

    def __init__(self, response):
        self.response = response

    @property
    def status(self):
        return self.response.status

    @property
    def headers(self):
        headers = self.response.headers
        headers.append(('Content-Type', 'text/plain'))
        return headers

    @property
    def body(self):
        return str(self.response.body)
