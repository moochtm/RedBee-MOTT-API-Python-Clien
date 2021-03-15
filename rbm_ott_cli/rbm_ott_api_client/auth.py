import logging
import uuid


class Auth():
    def __init__(self, customer, request_maker, business_unit=None):
        self.id = id
        self._customer = customer
        self._business_unit = business_unit
        self._request_maker = request_maker

    def auth(self):
        url = 'authentication'
        response = json.loads(self._request_maker.get(url=url).text.encode('utf-8'))
        return response