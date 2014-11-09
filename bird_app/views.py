from bird_app import app
from flask import render_template, request
from flask.ext.geoip import GeoIP
from datetime import *
import requests
import json
import time

gi = GeoIP(app)

@app.route('/')
def index():
    distance = 25
    location = get_user_location()
    results = bird_count(location, distance)
    notables = notable_sightings(location, distance)
    return render_template('bird_count.html',
                            date = time.strftime("%A, %B %d, %Y"),
                            miles = distance,
                            lat = round(location['latitude'], 2),
                            long = round(location['longitude'], 2),
                            bird_names = sorted(results),
                            bird_counts = results,
                            user_city = location['city'],
                            user_state = location['region_code'],
                            notable_sightings = notables)

# uses ip address and GeoIP to get user location info
def get_user_location():
    user_ip = request.remote_addr

    # subs in default ip address when running in localhost
    if user_ip == '127.0.0.1':
        # user_ip = '50.133.222.179'
        # for different sample, Miami, Fl
        user_ip = '131.94.186.10'

    location = gi.record_by_addr(user_ip)
    return location
    
# makes up the request url
def all_sightings_url(longitude, latitude, distance):
    return 'http://ebird.org/ws1.1/data/obs/geo/recent?lng={longitude}&lat={latitude}&dist={distance}&back=1&maxResults=500&locale=en_US&fmt=json'.format(**locals()) 

# gets report of sightings from ebird API
def get_all_report(location, distance):
    r = requests.get(all_sightings_url(location['longitude'], location['latitude'], distance))
    return json.loads(r.text)

# filters and tallies sightings reported to ebird
def bird_count(location, distance):
    count = dict()

    fmt = "%Y-%m-%d %H:%M"
    current_day = time.strftime("%d")

    # handles NameError issue with info from e-bird API
    false = 'false'
    true = 'true'

    info = get_all_report(location, distance)

    for i in info:
        observed_day = datetime.strptime(i['obsDt'],fmt).strftime("%d")

        # ensures only today's sightings
        if observed_day == current_day:
            name = i['comName']

            # sets default value if howMany not reported
            if 'howMany' in i:
                number_observed = i['howMany']
            else:
                number_observed = 1

            # checks for name key
            if name in count:

                # adds howMany to number_observed
                count[name] += number_observed

            else:
                # add name and number_observed to dict
                count[name] = number_observed

    return count

# Notable Sightings Methods Below


# creates notable sightings url
def notable_sightings_url(longitude, latitude, distance):
    return 'http://ebird.org/ws1.1/data/notable/geo/recent?lng={longitude}&lat={latitude}&dist={distance}&back=1&maxResults=500&detail=simple&locale=en_US&fmt=json'.format(**locals())

# gets report of sightings from ebird API
def get_notables_report(location, distance):
    r = requests.get(notable_sightings_url(location['longitude'], location['latitude'], distance))
    return json.loads(r.text)
    
# makes list of notable species names
def notable_sightings(location, distance):
    notables = []

    fmt = "%Y-%m-%d %H:%M"
    current_day = time.strftime("%d")

    # handles NameError issue with info from e-bird API
    false = 'false'
    true = 'true'

    info = get_notables_report(location, distance)

    for i in info:
        observed_day = datetime.strptime(i['obsDt'],fmt).strftime("%d")

        # ensures only today's sightings
        if observed_day == current_day:
            name = i['comName']
            notables.append(name)
    return notables




