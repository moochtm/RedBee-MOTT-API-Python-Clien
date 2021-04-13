from request_maker import Request
from base64 import b64encode
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

"""
This module contains a client for the RBM MOTT Management API
The client handles all REST API calls. It does not manipulate the responses.
https://mgmtapidocs.emp.ebsd.ericsson.net/
"""


class ManagementApiClient:
    def __init__(self, cu, bu, api_key_id, api_key_secret):
        self._cu = cu
        self._bu = bu
        self.host = 'https://management.api.redbee.live'
        self.default_headers = {
            'Authorization': get_auth_header(api_key_id, api_key_secret),
            'Content-Type': 'application/xml;charset=UTF-8'
        }

        # do a test call to check cu/bu, auth and host
        self.get_product()

    #########################################################################
    # CLASS HELPER FUNCTIONS
    #########################################################################

    @property
    def cu_bu(self) -> str:
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

    @Request(method='get')
    def test(self, params: dict = None, body=None):
        return {
            'url': f'{self.host}/v1/{self.cu_bu}/tag',
            'params': params or {},
            'body': body
        }

    #########################################################################
    # ASSETS
    #########################################################################

    @Request(method='get')
    def get_assets(self, params: dict = None):
        return {
            'url': f'{self.host}/v1/{self.cu_bu}/asset',
            'params': params or {}
        }

    @Request(method='post')
    def post_assets(self, data):
        return {
            'url': f'{self.host}/v1/{self.cu_bu}/asset',
            'data': data
        }

    #########################################################################
    # ASSET
    #########################################################################

    @Request(method='get')
    def get_asset(self, asset_id):
        return {
            'url': f'{self.host}/v1/{self.cu_bu}/asset/{asset_id}'
        }

    @Request(method='delete')
    def delete_asset(self, asset_id):
        return {
            'url': f'{self.host}/v1/{self.cu_bu}/asset/{asset_id}'
        }

    @Request(method='get')
    def get_asset_materials(self, asset_id):
        return {
            'url': f'{self.host}/v1/{self.cu_bu}/asset/{asset_id}/material'
        }

    @Request(method='get')
    def get_asset_publications(self, asset_id):
        return {
            'url': f'{self.host}/v1/{self.cu_bu}/asset/{asset_id}/publication'
        }

    @Request(method='delete')
    def delete_tag_from_asset(self, asset_id, tag_id):
        return {
            'url': f'{self.host}/v1/{self.cu_bu}/asset/{asset_id}/tag/{tag_id}'
        }

    #########################################################################
    # MATERIALS
    #########################################################################

    #########################################################################
    # PRODUCTS
    #########################################################################

    @Request(method='get')
    def get_product(self):
        return {
            'url': f'{self.host}/v1/{self.cu_bu}/product'
        }

    #########################################################################
    # PUBLICATIONS
    #########################################################################

    #########################################################################
    # SERIES
    #########################################################################

    @Request(method='post')
    def post_series(self, data):
        return {
            'url': f'{self.host}/v1/{self.cu_bu}/series',
            'data': data
        }

    #########################################################################
    # TAGS
    #########################################################################

    @Request(method='post')
    def post_tags(self, data):
        return {
            'url': f'{self.host}/v1/{self.cu_bu}/tag',
            'data': data
        }

    #########################################################################
    # TAG
    #########################################################################

    @Request(method='delete')
    def delete_tag(self, tag_id):
        return {
            'url': f'{self.host}/v1/{self.cu_bu}/tag/{tag_id}'
        }

#########################################################################
# MODULE HELPER FUNCTIONS
#########################################################################

def get_auth_header(username: str, password: str) -> str:
    user_and_pass = "{}:{}".format(username, password)
    encoded_user_pass = str(b64encode(user_and_pass.encode("utf-8")), "utf-8")
    return 'Basic {}'.format(encoded_user_pass)
