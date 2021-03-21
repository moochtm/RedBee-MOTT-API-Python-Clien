


"""
post /v1/customer/{customer}/asset
post /v1/customer/{customer}/businessunit/{businessUnit}/asset

GET /v1/customer/{customer}/businessunit/{businessUnit}/asset/{}/material'

DELETE /v1/customer/{customer}/businessunit/{businessUnit}/asset/{}/tag/{}'

ADD TAG TO ASSET
+ '/asset/{}/tag?mergeMode=ADD'
                                 .format(asset_id),
                                 headers={'Authorization': get_auth_header(self._api_key, self._api_secret)},
                                 json={"tagRefs": tags_to_add}, verify=ENV[self._env]['verify'])
"""
