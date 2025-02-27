import json
class FlaskAppResponseMiddleware(object):
    def __init__(self):
        self.url = 'http://192.168.168.105:5000/browse'
        self.headers = {'Content-Type': 'application/json'}
    def process_request(self, request, spider):
        if request.meta.get('flask_app'):
            if request.url != self.url:
                body = dict(url=request.url, proxy = request.meta.get('proxy'))
                req = request.replace(
                    url=self.url, body=json.dumps(body), method='POST')
                req.headers.update(self.headers)
                return req