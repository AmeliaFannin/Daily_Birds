import requests
import json

def get_all_report():
    r = requests.get('http://ebird.org/ws1.1/data/obs/geo/recent?lng=-71.31&lat=42.46&dist=1&back=1&maxResults=500&locale=en_US&fmt=json&includeProvisional=true')
    return r.text

def get_notable_report():
    r = requests.get('http://ebird.org/ws1.1/data/notable/geo/recent?lng=-71.31&lat=42.46&dist=1&back=1&maxResults=500&detail=simple&locale=en_US&fmt=json')
    return r.text

print get_all_report()
print get_notable_report()