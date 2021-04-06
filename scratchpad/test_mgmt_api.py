from decouple import config  # https://pypi.org/project/python-decouple/
from rbm_mott_cli.mgmt_api_client.mgmt_api import ManagementApiClient
from rbm_mott_cli.request_maker import RequestMaker

import logging
logging.basicConfig(level=logging.DEBUG)

API_KEY_ID = config('MGMT_API_KEY_ID', default=None)
API_KEY_SECRET = config('MGMT_API_KEY_SECRET', default=None)

client = ManagementApiClient(RequestMaker(), api_key_id=API_KEY_ID, api_key_secret=API_KEY_SECRET,
                             cu='Matt', bu='MattTV')

print(client.add_asset_tag(asset_id='rDxKcon8ZuQ', tag_id='GOAL'))
print(client.add_asset_tag(asset_id='rDxKcon8ZuQ_0D9739', tag_id='GOAL_7EFE8B'))
