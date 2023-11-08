# To test Requests
import requests

url_dev = "http://localhost:8000"
url_prod = "http://k8s-default-rayclust-739f2d7083-1916008357.eu-west-2.elb.amazonaws.com"

body = {"input_value": 1}
response = requests.post(f"{url_prod}/double", json=body)
print(response.json())
