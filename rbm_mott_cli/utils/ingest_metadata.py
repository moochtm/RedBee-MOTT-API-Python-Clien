import os
import copy
from xml.sax.saxutils import escape
from datetime import datetime
from io import StringIO

from jinja2 import Template, Environment, Undefined
from lxml import etree
from slugify import slugify
import pycountry  # https://pypi.org/project/pycountry/
import requests

import xmlschema
xsd = xmlschema.XMLSchema("/Users/home/Code/RedBee-MOTT-API-Python-Client/rbm_mott_cli/utils/ingest.xsd")

import logging
logger = logging.getLogger(__name__)

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
NAMESPACE = '{http://video-metadata.emp.ebsd.ericsson.net/publish-metadata/v1}'
XSD_URL = 'https://raw.githubusercontent.com/EricssonBroadcastServices/EMP-api/master/asset-ingest/publish-xml/src/main/xsd/publish-metadata.xsd'

this_file_dir, _ = os.path.split(os.path.abspath(__file__))
default_template_path = os.path.join(this_file_dir, 'publish_metadata_template.xml')


#########################################################################
# INGEST METADATA CREATION
#########################################################################

class SilentUndefined(Undefined):
    def _fail_with_undefined_error(self, *args, **kwargs):
        logger.warning(self._undefined_message)
        return ''


def create(data, template_fp=None, verbose=False):
    # pre-process data
    xml_escape_dict(data)

    # set up jinja2 environment
    env = Environment()
    env.undefined = SilentUndefined
    env.filters['slugify'] = slugify_text
    env.filters['remove_url_params'] = remove_url_params
    env.filters['format_datetime'] = format_datetime
    env.filters['get_2char_lang_code'] = get_2char_lang_code
    env.filters['get_language'] = get_language

    # get template text
    if template_fp is None:
        template_fp = default_template_path
    with open(template_fp, 'r', encoding='utf8') as f:
        template_text = f.read()

    # render
    j2t = env.from_string(template_text)
    render = j2t.render(data=data)

    parser = etree.XMLParser(remove_blank_text=True, remove_comments=True)
    root = etree.fromstring(bytes(render, encoding='utf8'), parser=parser)

    # strip whitespace from text and tail
    for elem in root.iter('*'):
        if elem.text is not None:
            elem.text = elem.text.strip()
        if elem.tail is not None:
            elem.tail = elem.tail.strip()
        if elem.text is not None and not elem.text.strip():
            elem.text = None
        # remove attribute if empty
        for key in elem.keys():
            if not elem.get(key):
                elem.attrib.pop(key)

    # remove empty nodes APART from some that are allowed to be empty
    protected_elements = ['audio']
    found_protected = 0
    while len(root.xpath(".//*[not(node())]")) > found_protected:
        for element in root.xpath(".//*[not(node())]"):
            if etree.QName(element).localname in protected_elements:
                found_protected += 1
                continue
            element.getparent().remove(element)

    if verbose:
        print(data)

    return etree.tostring(root, pretty_print=True, encoding='UTF-8').decode()


def split_ingest_metadata(metadata, node_type):
    parser = etree.XMLParser(remove_blank_text=True, remove_comments=True)

    root = etree.fromstring(bytes(metadata, encoding='utf8'), parser=parser)

    # find all <data> child nodes that are NOT the wanted node type and remove them
    # for node in root.xpath(f"//data/*[not(self::{node_type})]"):
    for node in root.xpath(f"//ns:data/*[not(self::ns:{node_type})]",
                           namespaces={"ns": "http://video-metadata.emp.ebsd.ericsson.net/publish-metadata/v1"}):
        node.getparent().remove(node)

    # create copy of root with just <data> node in it
    root_copy = copy.deepcopy(root)
    data_copy_xpath = root_copy.xpath(f"//ns:data",
                                namespaces={"ns": "http://video-metadata.emp.ebsd.ericsson.net/publish-metadata/v1"})
    data_copy = data_copy_xpath[0]
    for child in data_copy:
        data_copy.remove(child)

    # find all <data> child nodes that ARE the wanted node type
    # for each find, copy into data_copy, add tostring to result, and then remove from data_copy
    results = []
    for node in root.xpath(f"//ns:data/*[self::ns:{node_type}]",
                           namespaces={"ns": "http://video-metadata.emp.ebsd.ericsson.net/publish-metadata/v1"}):
        data_copy.append(node)

        # validate xml
        xsd.validate(root_copy)

        results.append(etree.tostring(root_copy, pretty_print=True, encoding='UTF-8').decode())
        data_copy.remove(node)

    return results


#########################################################################
# JINJA2 FILTERS
#########################################################################

def slugify_text(text):
    return slugify(text)


def remove_url_params(url):
    return url[:url.find('?')]


def get_2char_lang_code(lang_code, default='--'):
    lang = pycountry.languages.lookup(lang_code)
    try:
        return lang.alpha_2
    except AttributeError:
        return default


def get_language(lang_code, default='--'):
    lang = pycountry.languages.lookup(lang_code)
    try:
        return lang.name
    except AttributeError:
        return default


def fix_country_code(country_code):
    country = pycountry.countries.lookup(country_code)
    return country.alpha_2


def format_datetime(dt, format=None):
    if not isinstance(dt, str):
        return dt.strftime(DATE_FORMAT)
    datetime_object = datetime.strptime(dt, format)
    return datetime_object.strftime(DATE_FORMAT)


#########################################################################
# XML validation
#########################################################################

def download_schema_string():
    r = requests.get(XSD_URL)
    print(r.content)

#########################################################################
# HELPER FUNCTIONS
#########################################################################

def xml_escape_dict(d):
    for k, v in d.items():
        if isinstance(v, dict):
            xml_escape_dict(v)
        elif isinstance(v, str):
            d[k] = escape(v)


if __name__ == "__main__":
    download_schema_string()