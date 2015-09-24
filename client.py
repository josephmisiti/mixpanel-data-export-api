import hashlib
import urllib
import urllib2
import time
import json
import pprint;

"""

    This is a modified version of the following script:
    
    https://mixpanel.com/docs/api-documentation/data-export-api#libs-python
    
    Which is adapted to support the Data Export API:
    
    https://mixpanel.com/docs/api-documentation/exporting-raw-data-you-inserted-into-mixpanel

"""

class MixpanelExportAPI(object):

    ENDPOINT = 'http://data.mixpanel.com/api'
    VERSION = '2.0'

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    def request(self, methods, params, format='json'):
        """
            methods - List of methods to be joined, e.g. ['events', 'properties', 'values']
                      will give us http://mixpanel.com/api/2.0/events/properties/values/
            params - Extra parameters associated with method
        """
        params['api_key'] = self.api_key
        params['expire'] = int(time.time()) + 600   # Grant this request 10 minutes.
        params['format'] = format
        if 'sig' in params: del params['sig']
        params['sig'] = self.hash_args(params)

        request_url = '/'.join([self.ENDPOINT, str(self.VERSION)] + methods) + '/?' + self.unicode_urlencode(params)
        request = urllib2.urlopen(request_url, timeout=120)
        data = request.read()
        data = data.split("\n")
        
        response = []
        for d in data:
            if len(d) == 0: continue
            response.append(json.loads(d))
        return response

    def unicode_urlencode(self, params):
        """
            Convert lists to JSON encoded strings, and correctly handle any
            unicode URL parameters.
        """
        if isinstance(params, dict):
            params = params.items()
        for i, param in enumerate(params):
            if isinstance(param[1], list):
                params[i] = (param[0], json.dumps(param[1]),)

        return urllib.urlencode(
            [(k, isinstance(v, unicode) and v.encode('utf-8') or v) for k, v in params]
        )

    def hash_args(self, args, secret=None):
        """
            Hashes arguments by joining key=value pairs, appending a secret, and
            then taking the MD5 hex digest.
        """
        for a in args:
            if isinstance(args[a], list): args[a] = json.dumps(args[a])

        args_joined = ''
        for a in sorted(args.keys()):
            if isinstance(a, unicode):
                args_joined += a.encode('utf-8')
            else:
                args_joined += str(a)

            args_joined += '='

            if isinstance(args[a], unicode):
                args_joined += args[a].encode('utf-8')
            else:
                args_joined += str(args[a])

        hash = hashlib.md5(args_joined)

        if secret:
            hash.update(secret)
        elif self.api_secret:
            hash.update(self.api_secret)
        return hash.hexdigest()


if __name__ == '__main__':
    api = MixpanelExportAPI(
        api_key = MIXPANEL_API_KEY,
        api_secret = MIXPANEL_API_SECRET
    )    
    data = api.request(['export'], {
        'from_date': '2015-09-01',
        'to_date': '2015-09-2',
        'event': ['play video'],
    })    
    pprint.pprint(data)