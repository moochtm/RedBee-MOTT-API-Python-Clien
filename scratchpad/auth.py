from base64 import b64encode
import requests


def get_auth_header(username: str, password: str) -> str:
    user_and_pass = "{}:{}".format(username, password)
    encoded_user_pass = str(b64encode(user_and_pass.encode("utf-8")), "utf-8")
    return 'Basic {}'.format(encoded_user_pass)


url = 'https://management.api.redbee.live/v2/customer/Matt/businessunit/MattTV/productoffering'
user = "aQRhyWFMM0wIDZ1CQHu3"
password = "HlhmnLpMfCHE0V0XuRUkLhtEiaxI6rIey35lySrvjsTnlqlwRxEg4Yjbfh4FKbIDGUVZMqFj1pdDtk6KimF2VOkKhdggJ0n1nw9s"

default_headers = {'Content-Type': 'application/xml',
                   'Authorization': get_auth_header(user, password)}

response = requests.get(url, headers=default_headers)
print(response.text)