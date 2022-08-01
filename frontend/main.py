import requests

x = requests.get('http://172.17.0.2:5000/api/')

print(x.text)