from request_maker import Request

import logging
logging.basicConfig(level=logging.DEBUG)

"""
This module contains a client for the RBM MOTT Exposure API
The client handles all REST API calls. It does not manipulate the responses.
https://apidocs.emp.ebsd.ericsson.net/
"""


class ExposureApiClient:
    def __init__(self, cu: str, bu: str):
        self.host = 'https://exposure.api.redbee.live:443'
        self._cu = cu
        self._bu = bu
        self.default_headers = {}

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
    # ASSETS
    #########################################################################

    @Request(method='get')
    def get_assets(self, params: dict = None):
        return {
            'url': f'{self.host}/v1/{self.cu_bu}/content/asset',
            'params': params or {}
        }

    @Request(method='get')
    def get_asset(self, asset_id: str, params: dict = None):
        return {
            'url': f'{self.host}/v1/{self.cu_bu}/content/asset/{asset_id}',
            'params': params or {}
        }

    #########################################################################
    # EVENTS
    #########################################################################

    @Request(method='get')
    def get_events_by_date(self, params: dict = None):
        return {
            'url': f'{self.host}/v1/{self.cu_bu}/content/asset',
            'params': params or {}
        }

    #########################################################################
    # SYSTEM
    #########################################################################

    @Request(method='get')
    def get_system_config(self, params: dict = None):
        return {
            'url': f'{self.host}/v1/{self.cu_bu}/systemConfig',
            'params': params or {}
        }

    #########################################################################
    # TAGS
    #########################################################################

    @Request(method='get')
    def get_tags(self, params: dict = None):
        return {
            'url': f'{self.host}/v1/{self.cu_bu}/tag',
            'params': params or {}
        }

    @Request(method='get')
    def get_tag(self, tag_id: str):
        return {
            'url': f'{self.host}/v1/{self.cu_bu}/tag/{tag_id}'
        }
