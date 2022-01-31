import requests
import json
from geopy.geocoders import Nominatim
from flask import Flask

app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    return "Hello"


@app.route('/restaurants', methods=['GET'])
def restaurants():
    with open('json/restaurant_places.json') as json_file:
        data = json.load(json_file)
        return data


@app.route('/fast_food', methods=['GET'])
def fast_food():
    with open('json/fast_food_places.json') as json_file:
        data = json.load(json_file)
        return data


@app.route('/update', methods=['GET'])
def update():
    get_fast_food_places()
    get_restaurant_places()


def get_fast_food_places():
    global overpass_url, overpass_query, response, fast_food_places
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = """
    [out:json];
    area["ISO3166-1"="MK"][admin_level=2];
    (node["amenity"="fast_food"](area);
     way["amenity"="fast_food"](area);
     rel["amenity"="fast_food"](area);
    );
    out center;
    """
    response = requests.get(overpass_url, params={'data': overpass_query})
    fast_food_places = response.json()['elements']
    fast_food_dict = {}

    for fast_food in fast_food_places:
        tags = fast_food['tags']
        if 'name' in tags:
            locator = Nominatim(user_agent='myGeocoder')
            coordinates = str(fast_food['lat']) + ', ' + str(fast_food['lon'])
            location = locator.reverse(coordinates)
            address = location.raw['address']
            if 'city' in address:
                city = address['city']
                if city in fast_food_dict:
                    fast_food_dict[city].append(fast_food)
                else:
                    fast_food_dict[city] = [fast_food]
            elif 'village' in address:
                village = address['village']
                if village in fast_food_dict:
                    fast_food_dict[village].append(fast_food)
                else:
                    fast_food_dict[village] = [fast_food]

    json_file = json.dumps(fast_food_dict)
    f = open("json/fast_food_places.json", "w")
    f.write(json_file)
    f.close()


def get_restaurant_places():
    global overpass_url, overpass_query, response
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = """
    [out:json];
    area["ISO3166-1"="MK"][admin_level=2];
    (node["amenity"="restaurant"](area);
     way["amenity"="restaurant"](area);
     rel["amenity"="restaurant"](area);
    );
    out center;
    """
    response = requests.get(overpass_url, params={'data': overpass_query})
    restaurants = response.json()['elements']
    restaurant_dict = {}
    for restaurant in restaurants:
        tags = restaurant['tags']
        if 'name' in tags:
            locator = Nominatim(user_agent='myGeocoder')
            coordinates = str(restaurant['lat']) + ', ' + str(restaurant['lon'])
            location = locator.reverse(coordinates)
            address = location.raw['address']
            if 'city' in address:
                city = address['city']
                if city in restaurant_dict:
                    restaurant_dict[city].append(restaurant)
                else:
                    restaurant_dict[city] = [restaurant]
            elif 'village' in address:
                village = address['village']
                if village in restaurant_dict:
                    restaurant_dict[village].append(restaurant)
                else:
                    restaurant_dict[village] = [restaurant]
    json_file = json.dumps(restaurant_dict)
    f = open("restaurant_places.json", "w")
    f.write(json_file)
    f.close()


if __name__ == '__main__':
    app.run()
