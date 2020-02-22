import logging
import uuid


class Asset:
    def __init__(self, customer, request_maker, business_unit=None, id=None):
        self.id = id
        self._customer = customer
        self._business_unit = business_unit
        self._request_maker = request_maker

    def list(self):
        url = 'api/v3/customer/{0}/businessunit/{1}/asset'.format(self._customer, self._business_unit)
        print(self._request_maker.get(url=url))

    def info(self):
        if self.id is None:
            return False

        bu = ''
        if self._business_unit is not None:
            bu = 'businessunit/{0}/'.format(self._business_unit)

        url = 'api/v3/customer/{0}/{1}asset/{2}'.format(self._customer, bu, self.id)
        print(self._request_maker.get(url=url))

    def post_new_asset(self):
        if self._business_unit is None:
            url = 'v1/customer/{0}/asset'
            url = url.format(self._customer)
        else:
            url = 'v1/customer/{0}/businessunit/{1}/asset'
            url = url.format(self._customer, self._business_unit)

        body_xml = """<?xml version="1.0" encoding="UTF-8"?>
        <publish-metadata xmlns="http://video-metadata.emp.ebsd.ericsson.net/publish-metadata/v1" \
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation=\
        "http://video-metadata.emp.ebsd.ericsson.net/publish-metadata/v1 publish-metadata-1.0.xsd">
            <data>
                <asset>
                    <id>q243srq24q244</id>
                    <titleList>
                        <title language="en">Title in English - update</title>
                    </titleList>
                    <assetType>movie</assetType>
                </asset>
                <material>
                    <materialRef>https://emptestdata.blob.core.windows.net/sources/Sintel/sintel.mp4</materialRef>
                </material>
            </data>
        </publish-metadata>"""
        body = body_xml  # .format(tag_id, tag_type_id, tag_names)
        logging.debug(body)

        response = self._request_maker.post(url=url, data=body)
        return response


"""
<?xml version="1.0" encoding="UTF-8"?>
<publish-metadata xmlns="http://video-metadata.emp.ebsd.ericsson.net/publish-metadata/v1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://video-metadata.emp.ebsd.ericsson.net/publish-metadata/v1 publish-metadata-1.0.xsd">
    <data>
        <asset>
            <id>{{assetId}}</id>
            <provider>provider1</provider>
            <productionYear>2017</productionYear>
            <titleList>
                <title language="en">Title for {{assetId}} in Englisth</title>
                <title language="sv">Title for {{assetId}} in Swedish</title>
            </titleList>
            <descriptionList>
                <description language="en" length="short">A short description in English</description>
                <description language="sv" length="short">A short description in Swedish</description>
                <description language="en" length="medium">A medium description in English</description>
                <description language="sv" length="medium">A medium description in Swedish</description>
                <description language="en" length="long">A long description in English</description>
                <description language="sv" length="long">A long description in Swedish</description>
            </descriptionList>
            <tagList>
                <tagIdRef>genre_drama</tagIdRef>
                <tagIdRef>genre_thriller</tagIdRef>
            </tagList>
            <imageList>
            	 <image language="sv">
                    <id></id>
                    <url>http://myhost.se/myPath/MyImageInSv.jpg</url>
                    <width>1280</width>
                    <height>720</height>
                    <purpose>banner</purpose>
                    <orientation>landscape</orientation>
                </image>
                <image language="en">
                    <id>image2</id>
                    <url>http://myhost.se/myPath/MyImageInEn.jpg</url>
                    <width>1280</width>
                    <height>720</height>
                    <purpose>banner</purpose>
                    <orientation>landscape</orientation>
                </image>
            </imageList>
            <parentalRatingList>
                <parentalRating>
                    <rating>15</rating>
                    <scheme>age</scheme>
                    <country>EN</country>
                </parentalRating>
                <parentalRating>
                    <rating>15</rating>
                    <scheme>age</scheme>
                    <country>SE</country>
                </parentalRating>
            </parentalRatingList>
            <assetType>movie</assetType>
        </asset>
        <material>
            <materialRef>
                https://emptestdata.blob.core.windows.net/sources/Sintel/sintel.mp4
                <audioList>
    				<audio channels="2" language="da" order="LR"/>
    				<audio channels="2s-2" language="fi" order="LR"/>
    				<audio channels="4s-2" language="no" order="LR"/>
    				<audio channels="6s-2" language="sv" order="LR"/>
				</audioList>
            </materialRef>
            <DRMEnabled>true</DRMEnabled>
            <subtitleList>
                <subtitle language="en">https://emptestdata.blob.core.windows.net/sources/Sintel/sintel_en.vtt</subtitle>
                <subtitle language="sv">https://emptestdata.blob.core.windows.net/sources/Sintel/sintel_se.vtt</subtitle>
            </subtitleList>
        </material>
        <publicationList>
            <publication>
                <id>{{assetId}}</id>
                <startTime>2020-01-24T00:00:00.000Z</startTime>
                <endTime>2025-01-24T00:00:00.000Z</endTime>
                <publishTime>2019-12-01T00:00:00.000Z</publishTime>
                <publicationRights>
                    <productList>
                        <product>{{productId}}</product>
                    </productList>
                </publicationRights>
            </publication>
        </publicationList>
        <assetType>episode</assetType>
        <seriesId>{{seriesId}}</seriesId>
        <seasonId>{{seasonId}}</seasonId>
        <episodeNumber>{{episodeNumber}}</episodeNumber>
    </data>
</publish-metadata>
"""
