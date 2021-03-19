import logging
import uuid
import requests
import json


class Entitlement:
    def __init__(self, customer, request_maker, business_unit=None) -> json:
        self._customer = customer
        self._business_unit = business_unit
        self._request_maker = request_maker

    def asset_play_request(self, asset_id, params: dict = None, get_all_assets: bool = True, get_all_fields: bool = True):
        url = 'v2/customer/{0}/businessunit/{1}/entitlement/{2}/play'.format(self._customer,
                                                                                                         self._business_unit,
                                                                                                         asset_id)

        # Build params
        if params is None:
            params = {}
        default_params = {}
        final_params = {**default_params, **params}

        # get initial response
        response = self._request_maker.get(url=url, params=final_params)
        response = json.loads(response.text.encode('utf8'))
        print(response)

        # TODO: need to get example of ingesting pre-transcoded assets.
        hls = [f for f in response['formats'] if f['format'] == 'HLS'][0]
        print(hls)
        self.get_HLS_manifest(mediaLocator=hls['mediaLocator'])

        return


    def get_HLS_manifest(self, mediaLocator):
        response = requests.get(url=mediaLocator)
        print(response.text)


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