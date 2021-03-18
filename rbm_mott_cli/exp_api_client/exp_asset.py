import logging
import uuid
import json


class Asset:
    def __init__(self, customer, request_maker, business_unit=None) -> json:
        self._customer = customer
        self._business_unit = business_unit
        self._request_maker = request_maker

    def get_assets(self, params: dict = None, get_all_assets: bool = True, get_all_fields: bool = True):
        url = 'v1/customer/{0}/businessunit/{1}/content/asset'.format(self._customer, self._business_unit)

        # Build params
        if params is None:
            params = {}
        if get_all_assets:
            params.update({
                'onlyPublished': False,
                'includeTvShow': True
            })
        if get_all_fields:
            params.update({
                'fieldSet': 'ALL'
            })
        default_params = {
            'pageNumber': 1,
            'pageSize': 200
        }
        final_params = {**default_params, **params}

        # get initial response
        response = self._request_maker.get(url=url, params=final_params)
        response = json.loads(response.text.encode('utf8'))
        final_response = response

        if get_all_assets:
            while response['pageNumber'] * response['pageSize'] < response['totalCount']:
                print(final_params)
                final_params['pageNumber'] = final_params['pageNumber'] + 1
                response = self._request_maker.get(url=url, params=final_params)
                response = json.loads(response.text.encode('utf8'))
                final_response['items'].extend(response['items'])
                final_response['pageSize'] = final_response['pageSize'] + response['pageSize']

        return final_response['items']


"""
DEBUG:root:response.text = {
  "items" : [ {
    "assetId" : "PanVC_0D9739",
    "localized" : [ {
      "images" : [ {
        "url" : "https://redbee.ctl.cdn.ebsd.ericsson.net/imagescaler001/matt/matttv/assets/PanVC_0D9739/posters/08a043950b6323e3a5dcf217108bdfee/08a043950b6323e3a5dcf217108bdfee-4898f0576c03c8e5b718b24b0179ffe4-150x100.jpg"
      }, {
        "url" : "https://redbee.ctl.cdn.ebsd.ericsson.net/imagescaler001/matt/matttv/assets/PanVC_0D9739/posters/08a043950b6323e3a5dcf217108bdfee/08a043950b6323e3a5dcf217108bdfee.jpg"
      } ],
      "locale" : "en",
      "title" : "PanVC"
    } ],
    "type" : "TV_CHANNEL"
  }, {
    "assetId" : "vchannel_0D9739",
    "localized" : [ {
      "images" : [ ],
      "locale" : "en",
      "title" : "My First Virtual Channel"
    } ],
    "type" : "TV_CHANNEL"
  }, {
    "assetId" : "q243srq24q244_0D9739",
    "localized" : [ {
      "description" : "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
      "images" : [ {
        "url" : "https://redbee.ctl.cdn.ebsd.ericsson.net/imagescaler001/matt/matttv/assets/q243srq24q244_0D9739/posters/618a295827249d61b33ec479d393b205/618a295827249d61b33ec479d393b205-a747ca206cd6226bc7007d2aac21b8ed-169x100.jpg"
      }, {
        "url" : "https://redbee.ctl.cdn.ebsd.ericsson.net/imagescaler001/matt/matttv/assets/q243srq24q244_0D9739/posters/618a295827249d61b33ec479d393b205/618a295827249d61b33ec479d393b205.jpg"
      } ],
      "locale" : "en",
      "title" : "Title in English - update"
    } ],
    "type" : "MOVIE"
  } ],
  "pageNumber" : 1,
  "pageSize" : 50,
  "totalCount" : 3"""