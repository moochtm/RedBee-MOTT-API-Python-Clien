import logging
import uuid
import json


class Tag:
    def __init__(self, customer, request_maker, business_unit=None) -> json:
        self._customer = customer
        self._business_unit = business_unit
        self._request_maker = request_maker

    def get_tags(self, params: dict = None, get_all_tags: bool = True):
        url = 'v1/customer/{0}/businessunit/{1}/tag'.format(self._customer, self._business_unit)

        # Build params
        if params is None:
            params = {}
        default_params = {
            'pageNumber': 1,
            'pageSize': 200,
        }
        final_params = {**default_params, **params}

        # get initial response
        response = self._request_maker.get(url=url, params=final_params)
        response = json.loads(response.text.encode('utf8'))
        final_response = response

        # go through all pages to get all tags
        if get_all_tags:
            while response['pageNumber'] * response['pageSize'] < response['totalCount']:
                print(final_params)
                final_params['pageNumber'] = final_params['pageNumber'] + 1
                response = self._request_maker.get(url=url, params=final_params)
                response = json.loads(response.text.encode('utf8'))
                final_response['items'].extend(response['items'])
                final_response['pageSize'] = final_response['pageSize'] + response['pageSize']

        return final_response['items']
