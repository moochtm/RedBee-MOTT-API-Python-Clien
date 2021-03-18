from base64 import b64encode

from .exp_customer import Customer

# https://apidocs.emp.ebsd.ericsson.net/


class ExposureApiClient:
    def __init__(self, request_maker):
        self._request_maker = request_maker
        self._request_maker.default_host = 'https://exposure.api.redbee.live:443/'

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

    def customer(self, id):
        return Customer(customer_id=id, request_maker=self._request_maker)
