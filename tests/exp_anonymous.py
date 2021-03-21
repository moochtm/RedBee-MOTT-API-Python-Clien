import requests



url = 'https://management.api.redbee.live/v2/customer/Matt/businessunit/MattTV/productoffering'
user = "aQRhyWFMM0wIDZ1CQHu3"
password = "HlhmnLpMfCHE0V0XuRUkLhtEiaxI6rIey35lySrvjsTnlqlwRxEg4Yjbfh4FKbIDGUVZMqFj1pdDtk6KimF2VOkKhdggJ0n1nw9s"

default_headers = {'Content-Type': 'application/xml',
                   'Authorization': get_auth_header(user, password)}

response = requests.get(url, headers=default_headers)
print(response.text)