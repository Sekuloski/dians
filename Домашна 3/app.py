from flask import Flask, render_template, request, url_for
import json

app = Flask(__name__)
app.debug = True

class Place:
    def __init__(self, lat, lon, name):
        self.lat = lat
        self.lon = lon
        self.name = name

    def get_name(self):
        return self.name
    
    def get_larger_map(self):
        return "https://www.openstreetmap.org/?mlat=" + str(self.lat) + "&mlon=" + str(self.lon) + "#map=16/" + str(self.lat) + "/" + str(self.lon)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/restaurant', methods=['GET'])
def dropdown_restaurant():
    cities = get_cities('restaurant')
    return render_template('restaurant.html', cities=cities)

@app.route('/fastfood', methods=['GET'])
def dropdown_fastfood():
    cities = get_cities('fastfood')
    return render_template('fastfood.html', cities=cities)

@app.route('/restaurant/choices', methods=['GET'])
def restaurant_places():
    city = request.args.get('city')
    places = get_places('restaurant', city)
    print(city)
    return render_template('selected_city.html', places=places)

@app.route('/fastfood/choices', methods=['GET'])
def fastfood_places():
    city = request.args.get('city')
    places = get_places('fastfood', city)
    print(city)
    return render_template('selected_city.html', places=places)

def get_places(selection, city):
    if selection == 'restaurant':
        with open('Домашна 3/static/json/restaurant_places.json') as json_file:
            data = json.load(json_file)[city]
            places = []

            for place in data:
                lat = place['lat']
                lon = place['lon']
                name = place['tags']['name']
                place = Place(lat, lon, name)
                places.append(place)

        return places
    if selection == 'fastfood':
        with open('Домашна 3/static/json/fast_food_places.json') as json_file:
            data = json.load(json_file)[city]
            places = []

            for place in data:
                lat = place['lat']
                lon = place['lon']
                name = place['tags']['name']
                place = Place(lat, lon, name)
                places.append(place)

        return places

def get_cities(selection):
    if selection == 'restaurant':
        with open('Домашна 3/static/json/restaurant_places.json') as json_file:
            data = json.load(json_file)
            cities_sk = []

            for key in data.keys():
                cities_sk.append(key)
        return cities_sk
    if selection == 'fastfood':
        with open('Домашна 3/static/json/fast_food_places.json') as json_file:
            data = json.load(json_file)
            cities_sk = []

            for key in data.keys():
                cities_sk.append(key)
        return cities_sk

if __name__ == "__main__":
    app.run()
