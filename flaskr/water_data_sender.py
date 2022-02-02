from flask import request

import time
import requests
import csv

water_data = []


def parse_data(file_name):
    file = open(file_name)
    csvreader = csv.reader(file)

    for row in csvreader:
        water_data.append(row)

    return water_data


def send_data(data, aquarium_id, sleepTime, url):
    while(True):
        index = 0;
        for row in water_data:
            if index == 0:
                index += 1
                continue;
            payload = {'aquarium_id': aquarium_id, 'pH': row[0],'oxygen':row[1], 'bacteria':row[2], 'temperature':row[3]}
            requests.post(url, data = payload)
            print(f'water updated: hH: {row[0]}, oxygen: {row[1]}, bacteria: {row[2]}, temperature: {row[3]}\n')
            time.sleep(sleepTime)

