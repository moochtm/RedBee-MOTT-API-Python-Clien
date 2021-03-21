import json
import xml.etree.ElementTree as ET

NAMESPACE = '{http://video-metadata.emp.ebsd.ericsson.net/publish-metadata/v1}'


class Objdict(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            # return empty list so that __getattr__ = false and __iter__ length = 0
            return []
            # raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)


def get_publish_metadata(src) -> ET:
    src = Objdict(src)

    publish_metadata = ET.Element('{}publish-metadata'.format(NAMESPACE))
    data = ET.SubElement(publish_metadata, '{}data'.format(NAMESPACE))

    if src.asset:
        asset = ET.SubElement(data, '{}asset'.format(NAMESPACE))

    return ET.tostring(publish_metadata)

template = """
<?xml version="1.0" encoding="UTF-8"?>
<publish-metadata xmlns="http://video-metadata.emp.ebsd.ericsson.net/publish-metadata/v1">
    <data>
        {% for asset in data.assets %}
        <asset>
            <id>{{ asset.id }}</id>
            <provider>{{ asset.provider }}</provider>
            <productionYear>{{ asset.production_year }}</productionYear>
            <titleList>
                {% for title in asset.title_list %}
                <title language="{{ title.language }}">{{ title.text }}</title>
                {% endfor %}
            </titleList>
            <descriptionList>
                {% for d in asset.description_list %}
                <description language="{{ d.language }}" length="{{ d.len }}">{{ d.text }}</description>
                {% endfor %}
            </descriptionList>
            <tagList>
                {% for t in asset.tag_list %}
                <tagIdRef>t.tag_id_ref</tagIdRef>
                {% endfor %}
            </tagList>
            <imageList>
                {% for i in asset.image_list %}
                <image language="{{ i.lang }}">
                    <id>{{ i.id }}</id>
                    <url>{{ i.url }}</url>
                    <width>{{ i.width }}</width>
                    <height>{{ i.height }}</height>
                    <purpose>{{ i.purpose }}</purpose>
                    <orientation>{{ i.orientation }}</orientation>
                </image>
                {% endfor %}
            </imageList>
            <parentalRatingList>
                {% for pr in asset.parental_rating_list %}
                <parentalRating>
                    <rating>{{ pr.rating }}</rating>
                    <scheme>{{ pr.scheme }}</scheme>
                    <country>{{ pr.country }}</country>
                </parentalRating>
                {% endfor %}
            </parentalRatingList>
            <assetType>{{ asset.asset_type | lower }}</assetType>
            <seriesId>{{ asset.series_id }}</seriesId>
            <seasonId>{{ asset.season_id }}</seasonId>
            <episodeNumber>{{ asset.episode_number }}</episodeNumber>
        </asset>
        {% endfor %}
        <material>
            {% for mref in data.material.material_refs %}
            <materialRef>{{ mref.text }}
                <audioList>
                    {% for aud in mref.audio_list %}
                    <audio channels="{{ aud.chs }}" language="{{ aud.lang }}" order="{{ aud.order }}"/>
                    {% endfor %}
                </audioList>
                <DRMEnabled>{{ mref.drm_enabled | lower }}</DRMEnabled>
                <subtitleList>
                    {% for sub in mref.subtitle_list %}
                    <subtitle language="{{ sub.lang }}">{{ sub.text }}</subtitle>
                    {% endfor %}
                </subtitleList>
            </materialRef>
            {% endfor %}
        </material>
        <publicationList>
            {% for pub in data.publication_list %}
            <publication>
                <id>{{ pub.asset_id }}</id>
                <startTime>{{ pub.start_time }}</startTime>
                <endTime>{{ pub.end_time }}</endTime>
                <publishTime>{{ pub.publish_time }}</publishTime>
                <publicationRights>
                    <productList>
                        {% for prod in pub.publication_rights.product_list %}
                        <product>{{ prod.id }}</product>
                        {% endfor %}
                    </productList>
                </publicationRights>
            </publication>
            {% endfor %}
        </publicationList>
    </data>
</publish-metadata>
"""

if __name__ == '__main__':
    data = {
        'publish-metadata': {
            '@xlmns': {
               '$': 'http://video-metadata.emp.ebsd.ericsson.net/publish-metadata/v1'
            },
            'data': {
                'asset': {
                    'id': '1231231231',
                    'title_list': [{
                        'text': 'Title Text'
                    }],
                    'asset_type': 'MOVIE'
                },
                'material': {
                    'material_refs': [{
                        'text': 'https://emptestdata.blob.core.windows.net/sources/Sintel/sintel.mp4'
                    }]
                }
            }
        }
    }
    result = get_publish_metadata(data)
    print(result)
