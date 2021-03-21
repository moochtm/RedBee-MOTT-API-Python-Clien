


"""
{
    "assetId": "LouieDrawMeACakeS1E30_F8AC88b",
    "audioTracks": [
        "DANISH"
    ],
    "changed": "2021-03-11T17:53:09.759Z",
    "created": "2021-03-11T10:12:12.911Z",
    "customData": null,
    "episode": "30",
    "externalReferences": [],
    "linkedEntities": [],
    "live": false,
    "localized": [
        {
            "description": "Yoko har planlagt en picnic, men hun har glemt kagen. Det er en katastrofe! Hvad skal de gøre?",
            "images": [
                {
                    "height": 1024,
                    "orientation": "LANDSCAPE",
                    "type": "poster",
                    "url": "https://redbee.ctl.cdn.ebsd.ericsson.net/imagescaler001/nordisk/nfdemo/assets/LouieDrawMeACakeS1E30_F8AC88b/posters/0b24ac8c233b4c014adf0563aeb293d1/0b24ac8c233b4c014adf0563aeb293d1.jpg",
                    "width": 1820
                }
            ],
            "locale": "en",
            "longDescription": "Yoko har planlagt en picnic, men hun har glemt kagen. Det er en katastrofe! Hvad skal de gøre? Louie og Yoko tegner en lækker kage, så alle deres gæster kan hygge sig.",
            "shortDescription": "",
            "sortingTitle": "Louie, tegn en kage",
            "title": "Louie, tegn en kage"
        },
        {
            "description": "",
            "images": [],
            "locale": "da",
            "longDescription": "",
            "shortDescription": "",
            "sortingTitle": "Louie, draw me a cake",
            "title": "Louie, draw me a cake"
        }
    ],
    "parentalRatings": [],
    "participants": [
        {
            "function": "Director",
            "name": "Frédéric Mège",
            "personId": "72ce6a00-ba52-4c73-a373-f788d0c55645"
        },
        {
            "function": "Director",
            "name": "Frédérick Chaillou",
            "personId": "fb57b753-516f-48e4-a5cf-6585e300b7eb"
        }
    ],
    "productionCountries": [
        "FR"
    ],
    "productionYear": 2005,
    "publications": [
        {
            "countries": [],
            "customData": null,
            "devices": [],
            "fromDate": "2021-03-11T17:50:00Z",
            "products": [
                "free_product_F8AC88b"
            ],
            "availabilityKeys": [
                "free_product_F8AC88b",
                "LouieDrawMeACakeS1E30_F8AC88b_free_product_F8AC88b"
            ],
            "publicationDate": "2021-03-11T17:50:00Z",
            "publicationId": "f771f082-1787-4a7e-a35c-0fea02bc50b2_F8AC88b",
            "services": [],
            "toDate": "2026-03-11T17:50:00Z"
        }
    ],
    "season": "1",
    "seasonId": "67b40aca-a3e2-47e5-932c-3d30195196e4_F8AC88b",
    "spokenLanguages": [],
    "subtitles": [],
    "tags": [
        {
            "tagValues": [
                {
                    "tagId": "kids_F8AC88b"
                }
            ],
            "type": "other"
        }
    ],
    "tvShowId": "ba42aa81-b77b-4e27-8c82-ea38b07939d8_F8AC88b",
    "tvShow": {
        "localizedData": [
            {
                "description": "Har du nogensinde drømt om at udforske en ø eller rejse til månen? Længes du efter at være racerkører eller snakke med en venlig bjørn? Det er ikke noget problem! Alt er muligt sammen med Louie! Med hans og Yokos hjælp lærer du at tegne, mens du har det sjovt!",
                "images": [],
                "locale": "en",
                "sortingTitle": "Louie",
                "title": "Louie"
            }
        ]
    },
    "type": "EPISODE",
    "duration": 407000
}
"""
"""
<?xml version="1.0" encoding="UTF-8"?>
<publish-metadata xmlns="http://video-metadata.emp.ebsd.ericsson.net/publish-metadata/v1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://video-metadata.emp.ebsd.ericsson.net/publish-metadata/v1 publish-metadata-1.0.xsd">
    <data>
{% if data.assets %}
        <asset>
            <id>{{assetId}}</id>
            <provider>provider1</provider>
            <productionYear>2017</productionYear>
            <titleList>
                <title language="en">Title for {{assetId}} in English</title>
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
{% endif %}
{% if data.materials %}
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
{% endif %}
{% if data.publications %}
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
{% if data.publications %}
        {% if data.asset_type %}<assetType>{% data.asset_type %}</assetType>{% endif %}
        {% if data.asset_type %}<seriesId>{% data.series_id %}</seriesId>{% endif %}
        {% if data.asset_type %}<seasonId>{% data.season_id %}</seasonId>{% endif %}
        {% if data.asset_type %}<episodeNumber>{% data.episode_number %}</episodeNumber>{% endif %}
    </data>
</publish-metadata>
"""