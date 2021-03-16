import logging
import json
# from .mgmt_asset import Asset


class BusinessUnit:
    def __init__(self, business_unit, customer, request_maker):
        self.id = business_unit
        self._customer = customer
        self._request_maker = request_maker
        self.sessionToken = self._auth()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def _auth(self):
        url = 'v2/customer/{0}/businessunit/{1}/auth/anonymous'.format(self._customer, self.id)
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
        return response['sessionToken']


#    def asset(self, id=None):
#        return Asset(id=id, customer=self._customer, business_unit=self.id, request_maker=self._request_maker)
