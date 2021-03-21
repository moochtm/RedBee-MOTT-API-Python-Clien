import logging
import uuid

# http://badgerfish.ning.com
from xmljson import badgerfish as bf  # https://xmljson.readthedocs.io/en/latest/
from lxml.html import Element, tostring  # https://pypi.org/project/lxml/
import xml.dom.minidom


DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
NAMESPACE_MAP = {None: 'http://video-metadata.emp.ebsd.ericsson.net/publish-metadata/v1'}


class Ingest:
    def __init__(self, customer, request_maker, business_unit=None):
        self._cu = customer
        self._bu = business_unit
        self._rm = request_maker

    def post_asset(self, data: dict):
        if self._bu is None:
            url = 'v1/customer/{0}/asset'
            url = url.format(self._cu)
        else:
            url = 'v1/customer/{0}/businessunit/{1}/asset'
            url = url.format(self._cu, self._bu)

        body = bf.etree(data, root=Element('publish-metadata', nsmap=NAMESPACE_MAP))
        body = tostring(body)
        dom = xml.dom.minidom.parseString(body)
        body = dom.toprettyxml()
        print(body)
        response = self._rm.post(url=url, data=body)
        return response.text

    def get_asset(self, data: dict):
        if self._bu is None:
            url = 'v1/customer/{0}/asset'
            url = url.format(self._cu)
        else:
            url = 'v1/customer/{0}/businessunit/{1}/asset'
            url = url.format(self._cu, self._bu)

        response = self._rm.get(url=url)
        return response.text




