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
    template_text = open('publish_metadata_template.xml', 'r').read()
    env = Environment()
    env.undefined = SilentUndefined
    j2t = env.from_string(template_text)
    data = {
        'assets': [{
            'id': '1231231231',
            'title_list': [{
                'text': 'Title Text'
            }],
            'asset_type': 'MOVIE'
        }],
        'material': {
            'material_refs': [{
                'text': 'https://emptestdata.blob.core.windows.net/sources/Sintel/sintel.mp4'
            }]
        }
    }

    render = j2t.render(data=data)
    print(render)
    parser = etree.XMLParser(remove_blank_text=True)
    root = etree.fromstring(bytes(render, encoding='utf8'), parser=parser)

    print(etree.tostring(root, pretty_print=True).decode())
