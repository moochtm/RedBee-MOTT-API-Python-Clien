from base64 import b64encode
import json

"""
This module contains a client for the RBM MOTT Management API
The client handles all REST API calls. It does not manipulate the responses.
https://mgmtapidocs.emp.ebsd.ericsson.net/
"""


class ManagementApiClient:
    def __init__(self,  request_maker, cu, bu, api_key_id, api_key_secret):
        self._request_maker = request_maker
        self._request_maker.default_host = 'https://management.api.redbee.live'
        self._cu = cu
        self._bu = bu

        self._request_maker.default_headers = {
            'Authorization': get_auth_header(api_key_id, api_key_secret)
        }

        test_call = self.get_product()

#########################################################################
# CLASS HELPER FUNCTIONS
#########################################################################

    def _cu_bu_path(self) -> str:
        """
        helper function that constructs and returns the "@"customer/business unit"
        part of API call URLs.
        """
        if self._bu is None:
            return 'customer/{}'.format(self._cu)
        else:
            return 'customer/{}/businessunit/{}'.format(self._cu, self._bu)

#########################################################################
# REST API CALLS
#########################################################################

#########################################################################
# TESTING
#########################################################################

    def test(self):
        url = '/v1/{}/tag'.format(self._cu_bu_path())
        response = self._request_maker.get(url=url)

#########################################################################
# INGEST
#########################################################################

    def post_asset(self, body):
        url = '/v1/{}/asset'.format(self._cu_bu_path())

        response = self._request_maker.post(url=url, data=body)
        if response.status_code != 200:
            msg = "Status Code: {}, Message: {}".format(response.json()['httpCode'],
                                                        response.json()['message'])
            raise RuntimeError(msg)
        return response.json()

    def delete_asset(self, asset_id):
        url = '/v1/{}/asset/{}'.format(self._cu_bu_path(), asset_id)

        response = self._request_maker.delete(url=url)
        if response.status_code >= 300:
            msg = "Status Code: {}, Message: {}".format(response.json()['httpCode'],
                                                        response.json()['message'])
            raise RuntimeError(msg)
        return response.json()

#########################################################################
# ASSETS
#########################################################################

    def get_assets(self, params: dict = None):
        url = '/v1/{}/asset'.format(self._cu_bu_path())

        # build params
        if params is None:
            params = {}
        default_params = {
            'pageNumber': 1,
            'pageSize': 1,
        }
        final_params = {**default_params, **params}
        response = self._request_maker.get(url=url, params=params)
        if response.status_code != 200:
            return {}
        return response.json()

    def get_asset(self, asset_id):
        url = '/v1/{}/asset/{}'.format(self._cu_bu_path(), asset_id)
        response = self._request_maker.get(url=url)
        if response.status_code != 200:
            return {}
        return response.json()

    def get_asset_materials(self, asset_id):
        url = '/v1/{}/asset/{}/material'.format(self._cu_bu_path(), asset_id)
        response = self._request_maker.get(url=url)
        if response.status_code != 200:
            return {}
        return response.json()

    def get_asset_publications(self, asset_id):
        url = '/v1/{}/asset/{}/publication'.format(self._cu_bu_path(), asset_id)
        response = self._request_maker.get(url=url)
        if response.status_code != 200:
            return {}
        return response.json()

    def delete_asset_tag(self, asset_id, tag_id):
        url = '/v1/{}/asset/{}/tag/{}'.format(self._cu_bu_path(), asset_id, tag_id)
        self._request_maker.delete(url=url)

    def add_asset_tag(self, asset_id, tag_id):
        # TODO get this working!
        #url = '/v1/{}/asset/{}/tag/{}'.format(self._cu_bu_path(), asset_id, tag_id)
        #data = {}
        #self._request_maker.post(url=url)
        #return
        url = '/v1/{}/asset/{}/tag?mergeMode=ADD'.format(self._cu_bu_path(), asset_id)
        #url = '/v1/{}/asset/{}/tag'.format(self._cu_bu_path(), asset_id)
        data = {'tagRefs': [tag_id]}
        self._request_maker.post(url=url, json=data)

#########################################################################
# MATERIALS
#########################################################################

    def get_material(self):
        raise NotImplementedError
        # METHOD NOT ALLOWED
        # url = '/v1' + self._cu_bu_path() + '/material'
        # return self._request_maker.get(url=url).json()

#########################################################################
# PRODUCTS
#########################################################################

    def get_product(self):
        url = '/v1/{}/product'.format(self._cu_bu_path())
        response = self._request_maker.get(url=url)
        if response.status_code != 200:
            msg = "Status Code: {}, Message: {}".format(response.json()['httpCode'],
                                                        response.json()['message'])
            raise RuntimeError(msg)
        return response.json()

#########################################################################
# PUBLICATIONS
#########################################################################

    def get_publications(self):
        url = '/v1/{}/publication'.format(self._cu_bu_path())
        response = self._request_maker.get(url=url)
        if response.status_code != 200:
            msg = "Status Code: {}, Message: {}".format(response.json()['httpCode'],
                                                        response.json()['message'])
            raise RuntimeError(msg)
        return response.json()


#########################################################################
# SERIES
#########################################################################

    def get_series(self):
        url = '/v1/{}/series'.format(self._cu_bu_path())
        response = self._request_maker.get(url=url)
        if response.status_code != 200:
            msg = "Status Code: {}, Message: {}".format(response.json()['httpCode'],
                                                        response.json()['message'])
            raise RuntimeError(msg)
        return response.json()


#########################################################################
# MODULE HELPER FUNCTIONS
#########################################################################

def get_auth_header(username: str, password: str) -> str:
    user_and_pass = "{}:{}".format(username, password)
    encoded_user_pass = str(b64encode(user_and_pass.encode("utf-8")), "utf-8")
    return 'Basic {}'.format(encoded_user_pass)
