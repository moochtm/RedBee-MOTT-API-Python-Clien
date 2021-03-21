from base64 import b64encode
import logging
import json

from .exp_asset import Asset
from .exp_entitlement import Entitlement
from .exp_system import System
from .exp_tag import Tag

# https://apidocs.emp.ebsd.ericsson.net/


class ExposureApiClient:
    def __init__(self, request_maker, cu, bu):
        self._request_maker = request_maker
        self._request_maker.default_host = 'https://exposure.api.redbee.live:443/'
        self._cu = cu
        self._bu = bu

# TODO: Exposure API uses different sort of authentication
#        if api_key_id and api_key_secret:
        self._request_maker.default_headers = {'Content-Type': 'application/json'}
#        elif bearer_token:
#            self._request_maker.default_headers = {'Content-Type': 'application/xml',
#                                                   'Authorization': 'Bearer %s' % bearer_token}
#        else:
#            raise ValueError("No authentication info provided. Either API Key Id/Secret or Bearer token required.")

    # CALLS

    # OBJECTS

    def _auth(self):
        url = 'v2/customer/{0}/businessunit/{1}/auth/anonymous'.format(self._cu, self._bu)
        data = """{
            "device": {
                "height": 0,
                "width": 0,
                "model": "",
                "name": "",
                "os": "",
                "osVersion": "",
                "manufacturer": "",
                "type": "WEB"
            },
            "deviceId": "12345"
        }"""
        response = self._request_maker.post(url=url, data=data)
        if response.status_code != 200:
            logging.error("Auth error: response code is not 200.")
            raise PermissionError("Auth error: response code is not 200.")

        response = json.loads(response.text.encode('utf-8'))
        self._request_maker.default_headers.update({'Authorization': 'Bearer %s' % response['sessionToken']})

    def asset(self):
        return Asset(customer=self._cu, business_unit=self._bu, request_maker=self._request_maker)

    def entitlement(self):
        return Entitlement(customer=self._cu, business_unit=self._bu, request_maker=self._request_maker)

    def system(self):
        return System(customer=self._cu, business_unit=self._bu, request_maker=self._request_maker)

    def tag(self):
        return Tag(customer=self._cu, business_unit=self._bu, request_maker=self._request_maker)
