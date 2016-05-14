import json

class PresenterFactory(object):
    def get_presenter(self, request, response):
        return JsonPresenter(response, json)
        #header_accept = request.headers['ACCEPT']
        #if header_accept.startswith('application/json'):
        #    return JsonPresenter(response, json)
        #elif header_accept.startswith('application/xml'):
        #    return XmlPresenter()

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

    def get_headers(self):
        return {'Content-Type': 'application/xml'}

    def get_body(self, data):
        return self._serialize(data)

    def _serialize(self, root):
        xml = ''
        for key in root.keys():
            if isinstance(root[key], dict):
                xml = '%s<%s>\n%s</%s>\n' % (xml, key, self._serialize(root[key]), key)
            elif isinstance(root[key], list):
                xml = '%s<%s>' % (xml, key)
                for item in root[key]:
                    xml = '%s%s' % (xml, self._serialize(item))
                xml = '%s</%s>' % (xml, key)
            else:
                value = root[key]
                xml = '%s<%s>%s</%s>\n' % (xml, key, value, key)
        return xml
