from base64 import b64encode

from .mgmt_upload import Upload
from .mgmt_asset import Asset
from .mgmt_tag import Tag
from .mgmt_product import Product, ProductOffering


# https://mgmtapidocs.emp.ebsd.ericsson.net/


class ManagementApiClient:
    def __init__(self,  request_maker, cu, bu, api_key_id=None, api_key_secret=None, bearer_token=None,):
        self._request_maker = request_maker
        self._request_maker.default_host = 'https://management.api.redbee.live/'

        if api_key_id and api_key_secret:
            self._request_maker.default_headers = {'Content-Type': 'application/xml',
                                                   'Authorization': get_auth_header(api_key_id, api_key_secret)}
        elif bearer_token:
            self._request_maker.default_headers = {'Content-Type': 'application/xml',
                                                   'Authorization': 'Bearer %s' % bearer_token}
        else:
            raise ValueError("No authentication info provided. Either API Key Id/Secret or Bearer token required.")

    # CALLS

    def get_organisations(self):
        raise NotImplementedError
        # url = 'api/v1/organizationunits'
        # print(self._request_maker.get(url=url))

    # OBJECTS

    def upload(self, path):
        return Upload(path=path, request_maker=self._request_maker)

    def tag(self):
        return Tag(customer=self._cu, business_unit=self._bu, request_maker=self._request_maker)

    def product(self):
        return Product(customer=self._cu, business_unit=self._bu, request_maker=self._request_maker)

    def product_offering(self):
        return ProductOffering(customer=self._cu, business_unit=self._bu, request_maker=self._request_maker)

    def asset(self):
        return Asset(customer=self._cu, business_unit=self._bu, request_maker=self._request_maker)


def get_auth_header(username: str, password: str) -> str:
    user_and_pass = "{}:{}".format(username, password)
    encoded_user_pass = str(b64encode(user_and_pass.encode("utf-8")), "utf-8")
    return 'Basic {}'.format(encoded_user_pass)
