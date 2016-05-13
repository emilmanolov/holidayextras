import json

class PresenterFactory(object):
    def get_presenter(self, request):
        header_accept = request.headers['ACCEPT']
        if header_accept.startswith('application/json'):
            return JsonPresenter(json)
        elif header_accept.startswith('application/xml'):
            return XmlPresenter()

class JsonPresenter(object):

    def __init__(self, json):
        self.json = json

    def get_headers(self):
        return {'Content-Type': 'application/json'}

    def get_body(self, data):
        return self.json.dumps(data, indent=2)

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
