# https://hub.packtpub.com/elegant-restful-client-python-exposing-remote-resources/
import requests
from api_client.exposure_api import ExposureApiClient
from api_client.management_api import ManagementApiClient
from api_client.customer_portal_api import CustomerPortalApiClient

import utils.ingest_metadata as ingest_metadata
from utils.logging_utils import log_function_call

from decouple import config  # https://pypi.org/project/python-decouple/

import logging
logger = logging.getLogger(__name__)

"""
SHOULD NOT DO LISTS OF THINGS - LET CLI DO THAT WITH PROGRESS BAR
-----------------------------------------------------------------
Mott.Tags.create_tag(http args)

tags = mott.get_tags(http args)
tags = mott.get_used_tags(http args)
tag = mott.get_tag(http args)
mott.post_tags(http args)



Mott.Tags.Tag(http args) or id/locale/text << basically any property of tags
for tag in tags:
    tag.delete()


Mott.Publications

with progress_bar:
    with mott.assets as assets:
        for page in assets.get(args)

"""


#########################################################################
# HELPER FUNCTIONS
#########################################################################

def get_all_pages(func, params):
    # TODO - handle non 200 responses?
    params = params.copy()
    params.update({'pageNumber': 1})

    response_json = func(params=params).json()
    buffer_json = response_json

    while response_json['pageNumber'] * response_json['pageSize'] < response_json['totalCount']:
        print(params)
        params['pageNumber'] = params['pageNumber'] + 1
        response_json = func(params=params).json()
        buffer_json['items'].extend(response_json['items'])
        buffer_json['pageSize'] = buffer_json['pageSize'] + response_json['pageSize']
    return buffer_json


class MottClient:
    def __init__(self, cu: str, bu: str, mgmt_api_key_id: str, mgmt_api_key_secret: str, cp_api_session_auth: str):
        self.mgmt_api_client = ManagementApiClient(cu=cu, bu=bu,
                                                   api_key_id=mgmt_api_key_id,
                                                   api_key_secret=mgmt_api_key_secret)
        self.exp_api_client = ExposureApiClient(cu=cu, bu=bu)
        self.cp_api_client = CustomerPortalApiClient(cu=cu, bu=bu, session_auth=cp_api_session_auth)

    #########################################################################
    # ASSETS
    #########################################################################

    def get_assets(self, params: dict = None):
        logger.info('-'*60)
        logger.info(f'{str(type(self).__name__)}::{"get_assets"}')
        # build params
        default_params = {
            'fieldSet': 'ALL',
            'onlyPublished': False,
            'pageSize': 200
        }
        params = params or {}
        final_params = {**default_params, **params}

        # make api calls
        mgmt_api_response = get_all_pages(func=self.mgmt_api_client.get_assets, params=final_params)
        exp_api_response = get_all_pages(func=self.exp_api_client.get_assets, params=final_params)
        mgmt_api_response_items = mgmt_api_response['items']
        exp_api_response_items = exp_api_response['items']

        # merge api response items
        for mgmt_item in mgmt_api_response_items:
            mgmt_item_id = mgmt_item['id']
            exp_item_match = next((exp_item for exp_item in exp_api_response_items if exp_item['assetId'] == mgmt_item_id), None)
            if exp_item_match is not None:
                mgmt_item.update(exp_item_match)

        return mgmt_api_response_items

    @log_function_call
    def post_assets(self, data):
        # make api calls
        response = self.mgmt_api_client.post_assets(data=data)
        return response.json() if response.status_code == 200 else False

    #########################################################################
    # ASSET
    #########################################################################

    def get_asset_materials(self, asset_id: str):
        logger.info('-'*60)
        logger.info(f'{str(type(self).__name__)}::{"get_asset_materials"}')

        # make api calls
        # TODO - return materials or False
        return self.mgmt_api_client.get_asset_materials(asset_id=asset_id)

    #########################################################################
    # MATERIALS
    #########################################################################

    @log_function_call
    def post_materials(self, data):
        # make api calls
        response = self.mgmt_api_client.post_materials(data=data)
        return response.json() if response.status_code == 200 else False

    #########################################################################
    # PUBLICATIONS
    #########################################################################

    @log_function_call
    def post_publications(self, data):
        # make api calls
        response = self.mgmt_api_client.post_publications(data=data)
        return response.json() if response.status_code == 200 else False

    #########################################################################
    # SEASONS
    #########################################################################

    @log_function_call
    def post_seasons(self, data):
        # make api calls
        response = self.mgmt_api_client.post_seasons(data=data)
        return response.json() if response.status_code == 200 else False

    #########################################################################
    # SERIES
    #########################################################################

    @log_function_call
    def post_series(self, data):
        # make api calls
        response = self.mgmt_api_client.post_series(data=data)
        return response.json() if response.status_code == 200 else False

    #########################################################################
    # TAGS
    #########################################################################

    @log_function_call
    def get_tags(self, params: dict = None):
        # build params
        default_params = {
            'pageSize': 100
        }
        params = params or {}
        final_params = {**default_params, **params}

        # make api calls
        cp_api_response = get_all_pages(func=self.cp_api_client.get_tags, params=final_params)
        return cp_api_response['items']

    @log_function_call
    def post_tags(self, data):
        # make api calls
        response = self.mgmt_api_client.post_tags(data=data)
        return response.json() if response.status_code == 200 else False

    #########################################################################
    # TAG
    #########################################################################

    def get_tag(self, tag_id: str):
        logger.info('-'*60)
        logger.info(f'{str(type(self).__name__)}::{"get_tag"}')

        # make api calls
        response = self.exp_api_client.get_tag(tag_id=tag_id)
        return response.json() if response.status_code == 200 else False

    def delete_tag(self, tag_id: str, params: dict = None):
        logger.info('-'*60)
        logger.info(f'{str(type(self).__name__)}::{"delete_tag"}')

        # build params
        default_params = {
            'force': True
        }
        params = params or {}
        final_params = {**default_params, **params}

        # make api calls
        # TODO - return True or False
        return self.cp_api_client.delete_tag(tag_id=tag_id, params=final_params)


if __name__ == '__main__':

    mott = MottClient(cu='Matt', bu='MattTV',
                      mgmt_api_key_id=config('MGMT_API_KEY_ID'),
                      mgmt_api_key_secret=config('MGMT_API_KEY_SECRET'),
                      cp_api_session_auth=config('CP_API_SESSION_AUTH'))
    tags_data = {
        'default_language': 'en',
        'tags': [
            {
                "scheme": "other",
                "tagId": "hit_7EFE8B",
                "children": [],
                "created": "2020-02-12T21:01:41.927Z",
                "localized": [
                    {
                        "locale": "en",
                        "title": "удар"
                    }
                ],
                "parents": []
            }
        ]
    }
    print(len(mott.get_tags()))
    current_tags = mott.get_tags()
    for tag in current_tags:
        mott.delete_tag(tag['id'])
    print(len(mott.get_tags()))
