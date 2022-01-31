import json
import webbrowser
import os
from unidecode import unidecode
from gmplot import gmplot

chrome_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
edge_path = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
webbrowser.register('edge', None, webbrowser.BackgroundBrowser(edge_path))

if __name__ == '__main__':
    print("Choose type of establishment: ")
    print("1. Restaurant")
    print("2. Fast Food")

    if int(input()) == 1:  # Restaurant
        with open('restaurant_places.json') as json_file:
            data = json.load(json_file)
            cities_en = []
            cities_sk = []

            for key in data.keys():
                cities_sk.append(key)
                cities_en.append(unidecode(key))

            for city in range(len(cities_sk)):
                print(str(city + 1) + ". " + str(cities_sk[city]))

            print("Choose City or Village: ")
            city = int(input()) - 1
            restaurants = data[cities_sk[city]]

            for restaurant in range(len(restaurants)):
                print(str(restaurant + 1) + ". " + (restaurants[restaurant]['tags']['name']))
            print("Choose restaurant: ")

            restaurant = int(input()) - 1
            lon = restaurants[restaurant]['lon']
            lat = restaurants[restaurant]['lat']
            gmap = gmplot.GoogleMapPlotter(lat, lon, 15)
            gmap.marker(lat, lon, 'cornflowerblue')
            gmap.draw("my_map.html")

    else:  # Fast Food
        with open('fast_food_places.json') as json_file:
            data = json.load(json_file)
            cities_en = []
            cities_sk = []

            for key in data.keys():
                cities_sk.append(key)
                cities_en.append(unidecode(key))
            print("Choose City or Village: ")

            for city in range(len(cities_sk)):
                print(str(city + 1) + ". " + str(cities_sk[city]))
            city = int(input()) - 1
            restaurants = data[cities_sk[city]]

            for restaurant in range(len(restaurants)):
                print(str(restaurant + 1) + ". " + (restaurants[restaurant]['tags']['name']))
            print("Choose restaurant: ")

            restaurant = int(input()) - 1
            lon = restaurants[restaurant]['lon']
            lat = restaurants[restaurant]['lat']
            gmap = gmplot.GoogleMapPlotter(lat, lon, 15)
            gmap.marker(lat, lon, 'cornflowerblue')
            gmap.draw("my_map.html")

    url = "my_map.html"
    webbrowser.get('edge').open("file://" + os.path.abspath(url), new=2)