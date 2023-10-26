# To test Requests
import requests
body = {"pnl": 450}
response = requests.post("http://k8s-default-rayclust-ea43e56ec0-2050158618.eu-west-2.elb.amazonaws.com/double", json=body)
print(response.json())