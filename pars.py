import requests

def send_get_request(endpoint):
    url = f'http://192.168.0.17/{endpoint}'
    requests.get(url)

def send_post_request(endpoint, data):
    url = f'http://192.168.0.17/{endpoint}'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    requests.post(url, headers=headers, data=data)


def brightness(value):
    send_post_request("brightness", data="brightness="+str(value))

def rgb(r, g, b):
    send_post_request("color", data='red='+str(r)+'&green='+str(g)+'&blue='+str(b) )

def rainbow():
    send_get_request("mode1")

def transfusion():
    send_get_request("mode2")