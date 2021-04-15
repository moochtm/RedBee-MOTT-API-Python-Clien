from api_client.request_maker import Request
from base64 import b64encode
import logging

logger = logging.getLogger(__name__)

"""
This module contains a client for the Customer Portal MOTT Management API
The client handles all REST API calls. It does not manipulate the responses.
https://mgmtapidocs.emp.ebsd.ericsson.net/
"""


class CustomerPortalApiClient:
    def __init__(self, cu, bu, session_auth):
        self._cu = cu
        self._bu = bu
        self.host = 'https://redbee.live/portal'
        self.default_headers = {
            'Authorization': f'Bearer {session_auth}',
            'Content-Type': 'application/xml;charset=UTF-8',
        }

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
    # TAGS
    #########################################################################

    @Request(method='get')
    def get_tags(self, params: dict = None):
        return {
            'url': f'{self.host}/api/v1/{self.cu_bu}/tag',
            'params': params or {}
        }

    #########################################################################
    # TAG
    #########################################################################

    @Request(method='delete')
    def delete_tag(self, tag_id, params: dict = None):
        return {
            'url': f'{self.host}/api/v1/{self.cu_bu}/tag/{tag_id}',
            'params': params or {}
        }
