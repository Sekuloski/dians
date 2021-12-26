from flask import Flask, render_template, request, url_for
import json

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/restaurant', methods=['GET'])
def dropdown_restaurant():
    cities = get_cities('restaurant')
    return render_template('selected_food_type.html', cities=cities)

@app.route('/fastfood', methods=['GET'])
def dropdown_fastfood():
    cities = get_cities('fastfood')
    return render_template('selected_food_type.html', cities=cities)

def get_cities(selection):
    if selection == 'restaurant':
        with open('restaurant_places.json') as json_file:
            data = json.load(json_file)
            cities_sk = []

            for key in data.keys():
                cities_sk.append(key)
        return cities_sk
    if selection == 'fastfood':
        with open('fast_food_places.json') as json_file:
            data = json.load(json_file)
            cities_sk = []

            for key in data.keys():
                cities_sk.append(key)
        return cities_sk

if __name__ == "__main__":
    app.run()
