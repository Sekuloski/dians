from flask import Flask, render_template, request, url_for
import json

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/cities', methods=['GET'])
def dropdown():
    cities = get_cities('restaurant')
    return render_template('index.html', cities=cities)

def get_cities(selection):
    with open('restaurant_places.json') as json_file:
        data = json.load(json_file)
        cities_sk = []

        for key in data.keys():
            cities_sk.append(key)
    return cities_sk

if __name__ == "__main__":
    app.run()
