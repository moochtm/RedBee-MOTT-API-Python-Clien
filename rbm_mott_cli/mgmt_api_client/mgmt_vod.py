
import json
import requests
import subprocess


class Vod:
    def __init__(self, config):
        self.config = config
        self.materialRef = ''

    def ingest(self, info):
        url = 'https://go2.enigmatv.io/api/v3/customer/%s/businessunit/%s/ingest/vod' % (self.config.customer,
                                                                                         self.config.business_unit)
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % self.config.access_token}
        data = json.loads("""
        {
          "publication": {
            "businessUnit": {
              "id": ""
            },
            "fromDate": "",
            "toDate": "",
            "purgeDate": "",
            "publicationDate": "",
            "products": [
              {
                "id": "free_product_BAFCEF",
                "name": "free_product"
              }
            ]
          },
          "drmEnabled": false,
          "shortcuts": {
            "introOffsetMs": "",
            "creditsOffsetMs": ""
          },
          "materialRef": "",
          "title": "",
          "name": "",
          "ads": {
            "preRoll": "",
            "postRoll": "",
            "midRollOffsetsMs": []
          }
        }
            """)

        data['publication']['businessUnit']['id'] = self.config.business_unit
        data['publication']['fromDate'] = info['fromDate']
        data['publication']['toDate'] = info['toDate']
        data['publication']['purgeDate'] = info['purgeDate']
        data['publication']['publicationDate'] = info['publicationDate']
        data['title'] = info['title']
        data['name'] = info['name']
        data['materialRef'] = info['materialRef']

        data = json.dumps(data)

        print(data)

        response = requests.request("POST", url, headers=headers, data=data)
        print(response.text.encode('utf8'))
        return json.loads(response.text.encode('utf8'))
