import requests

base = 'http://127.0.0.1:5000/'

responce = requests.get(base+'video/2')

print(responce.json())

responce = requests.patch(base+'video/2' , {'views':1000000 , 'likes': 10000 , 'name': 'b_b'})

print(responce.json())

responce = requests.get(base+'video/2')

print(responce.json())