import argparse
import collections
import csv
import json
import glob
import math
import os
import pandas as pd
import re
from requests import get
import string
import sys
import time
import xml


class Bike():
    def __init__(self, baseURL, station_info, station_status):
        # initialize the instance
        self.baseURL = baseURL

        # provides for each docking station, the ID, name, lat and long, and total capacity
        baseInfo = baseURL + station_info
        self.station_info = get(baseInfo).text

        # how many bikes and how many docks are avaiable at any given time
        baseStatus = baseURL + station_status
        self.station_status = get(baseStatus).text

    def total_bikes(self):
        # return the total number of bikes available
        s = json.loads(self.station_status)

        total_bikes = 0

        for station in s['data']['stations']:
            total_bikes = total_bikes + station['num_bikes_available']
        # get data from station_status
        # retrieve the number of bikes from the file
        return total_bikes

    def total_docks(self):
        # return the total number of docks available
        s = json.loads(self.station_status)

        total_docks = 0

        for station in s['data']['stations']:
            total_docks = total_docks + station['num_docks_available']

        return total_docks

    def percent_avail(self, station_id):
        # return the percentage of available dock
        # return how many docks are available at a specified station over all the docks in the entire bike network
        # if the station id is invalid return an empty string
        # loop through every station id to make sure station exists
        s = json.loads(self.station_status)
        total_docks = 0
        available_bikes = 0
        station_id = str(station_id)

        for station in s['data']['stations']:
            #get id
            id = station['station_id']
            #if the id == station id then use that station's info 
            if station_id == id:
                available_bikes = station['num_bikes_available']
                total_docks = station['num_docks_available']
                break
        #case for if there is an invalid id
        if total_docks == 0:
            return ""
        else:
            return str(int((total_docks / (total_docks + available_bikes)) * 100)) + "%"

    def closest_stations(self, latitude, longitude):
        

        #use the latitude and longitude given, and the distance method to find the nearest stops
        #for each station calculate the difference return the ones with the 3 nearest distance difference
        #return a dictionary of the station ID and the 
        s = json.loads(self.station_info)
        stations_with_distance = []
        for station in s['data']['stations']:
            station_id = station['station_id']
            station_lat = station['lat']
            station_lon = station['lon']
            station_distance = self.distance(latitude, longitude, station_lat, station_lon)
            stations_with_distance.append((station_id, station_distance))
        stations_with_distance.sort(key=lambda x: x[1])

        closest_stations = {}
        #for each of the 3 closest stations find the name of the station and add them to the dictionary
        for st in stations_with_distance[:3]:
            id = st[0]
            station_name = ''
            for station in s['data']['stations']:
                if id == station['station_id']:
                    station_name = station['name']
                    update = {id : station_name}
                    closest_stations.update(update)

        return closest_stations

    def closest_bike(self, latitude, longitude):
        # return the station with available bikes closest to the given coordinates

        #loop through each of the stations with the distance and id 
        #check for each station that there are bikes avaiable
        s_info = json.loads(self.station_info)
        s_status = json.loads(self.station_status)
        stations_with_distance = []

        for station in s_info['data']['stations']:
            station_id = station['station_id']
            station_lat = float(station['lat'])
            station_lon = float(station['lon'])
            station_distance = self.distance(latitude, longitude, station_lat, station_lon)
            stations_with_distance.append((station_id, station_distance))
        stations_with_distance.sort(key=lambda x: x[1])


        closest_station = {}
       
        for st in stations_with_distance:
            id = st[0]
            station_name = ''
            for station in s_status['data']['stations']:
                if 0 < int(station['num_bikes_available']):
                    for station in s_info['data']['stations']:
                     if id == station['station_id']:
                        update ={id: station['name']}
                        closest_station.update(update)
            break

        return closest_station

    def station_bike_avail(self, latitude, longitude):
        # return the station id and available bikes that correspond to the station with the given coordinates
        s_info = json.loads(self.station_info)
        s_status = json.loads(self.station_status)
        
        result = {}

        for station in s_info['data']['stations']:
            station_lat = float(station['lat'])
            station_lon = float(station['lon'])
            #if it is 0 then we have found the one we want to check
            if latitude == station_lat and longitude == station_lon:
                id = station['station_id']
                for st in s_status['data']['stations']:
                    if id == st['station_id']:
                        update = {id : st['num_bikes_available']}
                        result.update(update)
        return result

    def distance(self, lat1, lon1, lat2, lon2):
        p = 0.017453292519943295
        a = 0.5 - math.cos((lat2-lat1)*p)/2 + math.cos(lat1*p) * \
            math.cos(lat2*p) * (1-math.cos((lon2-lon1)*p)) / 2
        return 12742 * math.asin(math.sqrt(a))


# testing and debugging the Bike class

if __name__ == '__main__':
    instance = Bike('https://db.cs.pitt.edu/courses/cs1656/data',
                    '/station_information.json', '/station_status.json')
    print('------------------total_bikes()-------------------')
    t_bikes = instance.total_bikes()
    print(type(t_bikes))
    print(t_bikes)
    print()

    print('------------------total_docks()-------------------')
    t_docks = instance.total_docks()
    print(type(t_docks))
    print(t_docks)
    print()

    print('-----------------percent_avail()------------------')
    p_avail = instance.percent_avail(342885)  # replace with station ID
    print(type(p_avail))
    print(p_avail)
    print()

    print('----------------closest_stations()----------------')
    # replace with latitude and longitude
    c_stations = instance.closest_stations(40.444618, -79.954707)
    print(type(c_stations))
    print(c_stations)
    print()

    print('-----------------closest_bike()-------------------')
    # replace with latitude and longitude
    c_bike = instance.closest_bike(40.444618, -79.954707)
    print(type(c_bike))
    print(c_bike)
    print()

    print('---------------station_bike_avail()---------------')
    # replace with exact latitude and longitude of station
    s_bike_avail = instance.station_bike_avail(40.445834, -80.008882)
    print(type(s_bike_avail))
    print(s_bike_avail)
