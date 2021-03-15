from .request_maker import RequestMaker
from .customer import Customer
from .upload import Upload


class ApiClient:
    def __init__(self, api_id=None, api_secret=None, bearer_token=None):
        self._request_maker = RequestMaker()
        self._request_maker.default_host = 'https://managementapi.emp.ebsd.ericsson.net/'
        self._request_maker.default_headers = {'Content-Type': 'application/xml',
                                               'Authorization': 'Bearer %s' % bearer_token}

    # CALLS

    def get_organisations(self):
        raise NotImplementedError
        # url = 'api/v1/organizationunits'
        # print(self._request_maker.get(url=url))

    # OBJECTS

    def customer(self, id):
        return Customer(customer_id=id, request_maker=self._request_maker)

    def upload(self, path):
        return Upload(path=path, request_maker=self._request_maker)
