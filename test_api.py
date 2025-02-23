import requests

url = "http://127.0.0.1:5000/store_entry"
data = {"text": "I feel very anxious about my exam"}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=data, headers=headers)
print(response.json())
