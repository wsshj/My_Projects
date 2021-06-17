import requests

url = "http://localhost:8000/login/"
data = {"username":"BF80108", "password":"123456"}

res = requests.post(url=url,data=data)
print(res.text)