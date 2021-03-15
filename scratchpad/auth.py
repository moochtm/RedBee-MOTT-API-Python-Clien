import requests
from requests.auth import HTTPDigestAuth
url = 'https://httpbin.org/digest-auth/auth/user/pass'
user = "aQRhyWFMM0wIDZ1CQHu3"
password = "HlhmnLpMfCHE0V0XuRUkLhtEiaxI6rIey35lySrvjsTnlqlwRxEg4Yjbfh4FKbIDGUVZMqFj1pdDtk6KimF2VOkKhdggJ0n1nw9s"
url = "https://management.api.redbee.live:443/authentication"
response = requests.post(url, auth=HTTPDigestAuth(user, password))

print(response.text)