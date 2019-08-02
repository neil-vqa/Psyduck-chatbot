
import requests, json

key = '3648b9c73a787ec1eacf07bfe3d549da/'

def forecaster(coords):
    coordinates = coords
    optional = '?exclude=minutely,daily,alerts,flags&units=si'
    url = 'https://api.darksky.net/forecast/' + key + coordinates + optional
    res = requests.get(url)
    result = json.loads(res.text)
    output1 = result['currently']
    output2 = result['hourly']['summary']

    return output1, output2

