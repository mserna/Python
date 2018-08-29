# weather_catcher.py
# Author: Matthew Serna
# Date: May 13, 2018
# This python app will make API calls via openwatherapi
# It will store 3 locations' weather data onto MongoDB db
# It will refresh data every 5 seconds of weather
# It will grab data from database and display via terminal

import requests
import configparser
from pymongo import MongoClient
import datetime
from pprint import pprint
import time

# Config.ini
config = configparser.ConfigParser()
file = open("config.ini", "w")

# MongoDB variables
connection = MongoClient('mongodb://localhost:27017/WEATHER_DATABASE')
weatherdb = connection.WEATHER_DATABASE
my_cities = weatherdb.mycities

def print_func2(city, weather, tempF, tempC):
    print('City: ' + city)
    print('Weather: ' + weather)
    print('Temperature (in Fahrenheit): ' + str(tempF) + '°F')
    print('Temperature (in Celsius): ' + str(tempC) + '°C')
    print()


def config_write(section, city, city_index, format_weather, format_temp_f, format_temp_c):
    config.add_section(section)
    config.set(section, 'City', str(city[city_index]))
    config.set(section, 'Weather', str(format_weather))
    config.set(section, 'TempF', str(format_temp_f))
    config.set(section, 'TempC', str(format_temp_c))
    config.write(file)
    config


def print_from_mongodb():
    print('Grabbing data from database')
    cursor = my_cities.find({})
    index = 0

    for document in cursor:
        db_city = document["city"]
        db_weather = document["weather"]
        db_tempF = document["temperatureF"]
        db_tempC = document["temperatureC"]
        print_func2(db_city, db_weather, db_tempF, db_tempC)
        index += 1


def write_to_mongodb(city, weather, tempf, tempc):
    myrecord = {
        "city": city,
        "weather": weather,
        "temperatureF": tempf,
        "temperatureC": tempc,
        "date": datetime.datetime.utcnow()
    }

    weatherdb.mycities.insert(myrecord)


def city_weather_main():
    api_key = '3fb3856e867cfc33768356fd0e50692c'
    api_address = 'http://api.openweathermap.org/data/2.5/weather?appid=' + api_key + '&q='
    city = input('Enter 3 cities (separate using commas): ').split(',')

    # Add refresh rate
    config.add_section('Refresh Rate')
    config.set('Refresh Rate', 'frequency', str(5))

    # Populates config file is null
    for city_index in range(0, 3):
        section = 'City ' + str(city_index)
        weather_url = api_address + city[city_index]
        json_data = requests.get(weather_url).json()
        format_weather = json_data['weather'][0]['main']
        temp = json_data['main']['temp']
        format_temp_f = round(temp * (9 / 5) - 459.67, 2)
        format_temp_c = round(temp - 273.15, 2)

        # Overwrite Config file with new data
        try:
            config_write(section, city, city_index, format_weather, format_temp_f, format_temp_c)
            print('Write config.ini file: success')
        except ValueError:
            print('Write config.ini file : failed')

        # Write to MongoDB
        if weatherdb.mycities != None:
            write_to_mongodb(city[city_index], format_weather, format_temp_f, format_temp_c)

    # Close file and save
    file.close()


city_weather_main()

while True:
    print_from_mongodb()
    time.sleep(int(config.get('Refresh Rate', 'frequency')))

