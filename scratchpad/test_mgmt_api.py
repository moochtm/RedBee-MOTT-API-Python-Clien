from decouple import config  # https://pypi.org/project/python-decouple/
from rbm_mott_cli.mgmt_api_client.mgmt_api import ManagementApiClient
from rbm_mott_cli.request_maker import RequestMaker

import logging
logging.basicConfig(level=logging.DEBUG)

API_KEY_ID = config('RBM_MOTT_API_KEY_ID', default=None)
API_KEY_SECRET = config('RBM_MOTT_API_KEY_SECRET', default=None)

client = ManagementApiClient(RequestMaker(), api_key_id=API_KEY_ID, api_key_secret=API_KEY_SECRET,
                             cu='Matt', bu='MattTV')

response = client.remove_asset_tag(asset_id="73b398c3-d19e-4b21-9876-3ab67a58a9fd_0D9739",
                                   tag_id="football_7EFE8B")

response = client.add_asset_tag(asset_id="73b398c3-d19e-4b21-9876-3ab67a58a9fd_0D9739",
                                   tag_id="football_7EFE8B")