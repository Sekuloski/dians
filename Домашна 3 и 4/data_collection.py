import requests
import json
from geopy.geocoders import Nominatim

if __name__ == '__main__':

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
    fast_food_dict = {}

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
    f = open("fast_food_places.json", "w")
    f.write(json_file)
    f.close()

    json_file = json.dumps(restaurant_dict)
    f = open("restaurant_places.json", "w")
    f.write(json_file)
    f.close()
