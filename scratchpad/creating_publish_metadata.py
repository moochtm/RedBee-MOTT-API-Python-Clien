import logging
from jinja2 import Template, Environment, Undefined
from lxml import etree


DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
NAMESPACE = '{http://video-metadata.emp.ebsd.ericsson.net/publish-metadata/v1}'


def filter_nested_dict(value, default, path):
    keys = path.split('.')
    for key in keys:
        try:
            value = value[key]
        except KeyError:
            return default
    return value


class SilentUndefined(Undefined):
    '''
    Don't break pageloads because vars arent there!
    '''
    def _fail_with_undefined_error(self, *args, **kwargs):
        return ''


if __name__ == '__main__':
    template_text = open('/Users/home/Downloads/youtube-dl/youtube_mott_metadata_template.xml', 'r').read()
    env = Environment()
    env.undefined = SilentUndefined
    j2t = env.from_string(template_text)
    data = {
        'assets': [{
            'id': '1231231231',
            'title_list': [{
                'text': 'Title Text'
            }],
            'asset_type': 'movie'
        }],
        'material': {
            'material_refs': [{
                'text': 'https://emptestdata.blob.core.windows.net/sources/Sintel/sintel.mp4'
            }]
        }
    }
    data = {
        'asset': {
            'id': 'jeff'
        }
    }

    render = j2t.render(data=data)
    print(render)
    # print(render)
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

    # remove empty nodes
    while len(root.xpath(".//*[not(node())]")) > 0:
        for element in root.xpath(".//*[not(node())]"):
            element.getparent().remove(element)

    print(etree.tostring(root, pretty_print=True).decode())
