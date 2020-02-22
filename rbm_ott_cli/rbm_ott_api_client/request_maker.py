import requests
import urllib
import logging

import status


class RequestMaker:
    def __init__(self):
        self.default_host = ""
        self.default_headers = {}
        self.default_params = {}

    def __request(self, method='GET', host='', url='', headers={}, params={}, data=None):

        if host == '':
            host = self.default_host

        url = host + url
        headers = {**self.default_headers, **headers}
        params = urllib.parse.urlencode(params)

        logging.debug('------------------------------------------------')
        logging.debug('sending {0} request'.format(method))
        logging.debug('url = {0}'.format(url))
        logging.debug('headers = {0}'.format(headers))
        logging.debug('params = {0}'.format(params))
        logging.debug('data = {0}'.format(data))

        response = requests.request(method, url, headers=headers, params=params, data=data)

        logging.debug('response.status_code = {0}'.format(response.status_code))
        logging.debug('response.headers = {0}'.format(response.headers))
        logging.debug('response.text = {0}'.format(response.text))

        return response

    def get(self, **kwargs):
        response = self.__request(**kwargs)
        return response

    def post(self, **kwargs):
        response = self.__request(method='POST', **kwargs)
        return response
