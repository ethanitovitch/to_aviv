from pip._vendor.distlib.compat import raw_input
import requests
import pandas as pd
import numpy as np
import math
from datetime import datetime
import time


def datetime_from_utc_to_local(utc_datetime):
    date = datetime.fromtimestamp(int(utc_datetime))
    return date


def degreesToRadians(degrees):
    return degrees * math.pi / 180


def distanceInKmBetweenEarthCoordinates(lat1, lon1, lat2, lon2):
    earthRadiusKm = 6371

    dLat = degreesToRadians(lat2 - lat1)
    dLon = degreesToRadians(lon2 - lon1)

    lat1 = degreesToRadians(lat1)
    lat2 = degreesToRadians(lat2)

    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.sin(dLon / 2) * math.sin(dLon / 2) * math.cos(lat1) * math.cos(
        lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return (earthRadiusKm * c)


def getAirports(lat, long, radius):
    cities = []

    airports = pd.read_csv('data/airport-codes.csv')

    airports = airports.loc[airports['type'] == 'large_airport'].values[:, :]

    for airport in airports:
        location = airport[11].split(',')

        distance = distanceInKmBetweenEarthCoordinates(lat, long, float(location[0]), float(location[1]))

        if distance < radius:
            print(airport[9])
            cities.append(airport[9])

    return cities


def findCheapest(from_cities, to_cities, from_date, to_date, stopovers, max_price):
    cheapest = None

    for from_city in from_cities:

        for to_city in to_cities:

            print("From: " + str(from_city) + " To: " + str(to_city))

            parameters = {
                'fly_from': from_city,
                'fly_to': to_city,
                'date_from': from_date,
                'date_to': to_date,
                'return_from': '03/08/2019',
                'return_to': '04/08/2019',
                'adults': '3',
                'children': '0',
                'curr': 'CAD',
                'max_stopovers': stopovers,
                'flight_type': 'oneway'
            }

            request = requests.get('https://api.skypicker.com/flights', parameters).json()

            for route in request["data"]:

                if cheapest is None:
                    cheapest = route

                if int(route['price']) < int(cheapest['price']):
                    cheapest = route

                if int(route['price']) < max_price:
                    departure = datetime_from_utc_to_local(route['dTime'])
                    price = route['price']
                    from_city = from_city

                    result = "From: " + str(from_city) + " Depart: " + str(departure) + " Price: " + str(
                        price) + " Details:"

                    for flight in route['route']:
                        result += " From: " + str(flight['mapIdfrom']) + " To: " + str(
                            flight['mapIdto']) + " Depart: " + str(datetime_from_utc_to_local(flight['dTime']))

                    print(result)

    return cheapest


if __name__ == "__main__":
    # start_city = raw_input("Start City? ")
    # end_city = raw_input("End City? ")
    # radius = raw_input("What Radius Are You Willing To Drive? ")
    # start_date = raw_input("Start Date? ")
    # end_date = raw_input("End Date? ")
    #
    # cities = getCities(start_city, radius)

    to_airports = getAirports(33.9399, 151.1753, 550)
    cheapest = findCheapest(to_airports, ['AKL'], '19/07/2019', '22/07/2019', 1, 10000)
    print(cheapest)

    # print("Return")
    #
    # city = 'SPU'
    #
    # from_airports = ['SPU']
    # cheapest = findCheapest(from_airports, to_airports, '02/08/2019', '3/08/2019', 1, 5000)
    # print(cheapest)
    # cheapest = findCheapest(start_city, end_city, start_date, end_date)

    # print("This the cheapest way to get from " + start_city + " to " + end_city + " between " + start_date + " and " + end_date)
