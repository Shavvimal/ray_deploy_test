# To test Requests
import requests
body = {"pnl": 100}
response = requests.post("http://localhost:8000/double", json=body)
print(response.json())