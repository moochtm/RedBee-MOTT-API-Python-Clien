
from rbm_mott_cli.mgmt_api_client.mgmt_api import ManagementApiClient

import logging
logging.basicConfig(level=logging.DEBUG)


api = ManagementApiClient('5988fd37-8ef4-4c56-bfb9-8aecbdfa5d1e')
print(api.customer('Matt').business_unit('MattTV').asset().post_new_asset())
# print(api.customer('Matt').business_unit('MattTV').product().get_products())
# print(api.customer('Matt').business_unit('MattTV').product().find_product_by_name(name='free_product'))

# print(api.customer('Matt').business_unit('MattTV').tag().get_tag('tag_id_0D9739'))
# print(api.customer('Matt').tag().post_tag("widzew łódź", 'other', {'en': 'blah - customer level'}))

# print(api.customer('Matt').business_unit('MattTV').tag().post_tag('tag_id', 'other', {'en': 'blah - business unit level'}))
# # print(api.upload('image.jpg'))
# # print(api.customer('RussianPremierLeague').tag().find_tags_with_title('Russian Premier Liga'))

# print(api.customer('Matt').business_unit('MattTV').product_offering().get_product_offerings())