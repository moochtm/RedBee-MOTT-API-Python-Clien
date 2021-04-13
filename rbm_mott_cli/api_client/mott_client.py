# https://hub.packtpub.com/elegant-restful-client-python-exposing-remote-resources/
import requests
from exposure_api import ExposureApiClient
from management_api import ManagementApiClient
from customer_portal_api import CustomerPortalApiClient
import rbm_mott_cli.utils.ingest_metadata as ingest_metadata

import logging
logging.basicConfig(level=logging.DEBUG)
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

    #########################################################################
    # TAGS
    #########################################################################

    def get_tags(self, params: dict = None):
        logger.info('-'*60)
        logger.info(f'{str(type(self).__name__)}::{"get_tags"}')

        # build params
        default_params = {
            'pageSize': 100
        }
        params = params or {}
        final_params = {**default_params, **params}

        # make api calls
        cp_api_response = get_all_pages(func=self.cp_api_client.get_tags, params=final_params)
        return cp_api_response['items']

    def post_tags(self, tags_data):
        logger.info('-'*60)
        logger.info(f'{str(type(self).__name__)}::{"post_tags"}')

        # render tags_data
        data = ingest_metadata.create(tags_data)
        print(data)

        # make api calls
        return self.mgmt_api_client.post_tags(data=data)

    #########################################################################
    # TAG
    #########################################################################

    def get_tag(self, tag_id: str):
        logger.info('-'*60)
        logger.info(f'{str(type(self).__name__)}::{"get_tag"}')

        # make api calls
        return self.exp_api_client.get_tag(tag_id=tag_id)

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
        return self.cp_api_client.delete_tag(tag_id=tag_id, params=final_params)


if __name__ == '__main__':
    mott = MottClient(cu='Matt', bu='MattTV',
                      mgmt_api_key_id='aQRhyWFMM0wIDZ1CQHu3',
                      mgmt_api_key_secret='HlhmnLpMfCHE0V0XuRUkLhtEiaxI6rIey35lySrvjsTnlqlwRxEg4Yjbfh4FKbIDGUVZMqFj1pdDtk6KimF2VOkKhdggJ0n1nw9s',
                      cp_api_session_auth='e9b68e26-0d54-4edb-a60a-777bc7c6941b')
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
