""" This class will calculate MeV threshold breaches """
import os
import json
import requests
from pprint import pprint
import time
import datetime
import configparser
from alert_api import AlertsAPI
from send_email import Emailer
import schedule

# Config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Thresholds map
thresholds = {
	'WARNING': 1, #MeV - Sends WARNING email
	'ALERT': 10, #MeV - Sends ALERT email and API call
	'CRITICAL': 100, #MeV - Sends CRITICAL email and API call
	'INFO': '<1'#MeV - Sends INFO email and API call
}

# Used to format time_tag key
pattern = '%Y-%m-%dT%H:%M:%S'

# Instantiate AlertsAPI object
alert = AlertsAPI()

# Instantiate Emailer object
email = Emailer()

# Calculate info elap time
info_rate = config.getint('Info', 'rate')

# Calculate info frequency the script runs
frequency = config.getint('Refresh Rate', 'frequency')

url = 'https://services.swpc.noaa.gov/json/goes/15/goes15_integral_protons_5m.json'

request = requests.get(url)

json_data = json.loads(request.text.encode('utf-8'))


def check_levels(json_data):

	# Get API url from config file
	headers = {'Authorization': 'Bearer %s' % (config.get('API','token'))}
	url = config.get('API', 'url')

	level = list(thresholds.keys())[3]
	data = alert.create_record(alert.schema, level, 0)
	particle_data = []
	time_data = []

	""" CHARTING """
	# creates records and stores into list for creating graph:
	for record in json_data:
		cpgt10 = record['cpgt10']
		time_tag = str(record['time_tag'])
		string1 = time_tag.split('T')[0]
		string2 = time_tag.split("T")[1].split(":")[0]
		time_tag = string1 + " " + string2 + ":00"
		particle_data.append(cpgt10)
		if time_tag not in time_data:
			time_data.append(time_tag)
	
	email.create_graph(particle_data, time_data)

	""" ALERTING """
	# Parse JSON data to grab values
	for record in json_data[0:1]:

		# Convert to epoch time
		time_tag = int(time.mktime(time.strptime(record['time_tag'], pattern)))
		cpgt10 = record['cpgt10']

		if cpgt10 >= thresholds['WARNING'] and cpgt10 < thresholds['ALERT']:
			level = list(thresholds.keys())[2]
			data = alert.create_record(alert.schema, level, cpgt10)
			email.send_email(data)

		elif cpgt10 >= thresholds['ALERT'] and cpgt10 < thresholds['CRITICAL']:
			level = list(thresholds.keys())[3]
			data = alert.create_record(alert.schema, level, cpgt10)
			alert.post(url, data)
			email.send_email(data)

		elif cpgt10 >= thresholds['CRITICAL']:
			level = list(thresholds.keys())[1]
			data = alert.create_record(alert.schema, level, cpgt10)
			alert.post(url, data)
			email.send_email(data)

		else:
			pass


def check_info(json_data):

	# Get API url from config file
	headers = {'Authorization': 'Bearer %s' % (config.get('API','token'))}
	url = config.get('API', 'url')

	level = list(thresholds.keys())[3]
	data = alert.create_record(alert.schema, level, 0)
	particle_data = []
	time_data = []
	check = False

	""" CHARTING """
	# creates records and stores into list for creating graph:
	for record in json_data:
		cpgt10 = record['cpgt10']
		time_tag = str(ecord['time_tag'])
		string1 = time_tag.split('T')[0]
		string2 = time_tag.split("T")[1].split(":")[0]
		time_tag = string1 + " " + string2 + ":00"
		particle_data.append(cpgt10)
		if time_tag not in time_data:
			time_data.append(time_tag)
	
	email.create_graph(particle_data, time_data)

	""" ALERTING """
	# Parse JSON data to grab values
	for record in json_data[0:18]:
		if record['cpgt10'] < thresholds['WARNING']:
			check = True

	if check == True:
		level = list(thresholds.keys())[0]
		data = alert.create_record(alert.schema, level, cpgt10)
		alert.post(url, data)
		email.send_email(data)


def main(): check_levels(json_data)


def main2(): check_info(json_data)


# Scheduler for checking alerts
schedule.every(frequency).minutes.do(main)

# Scheduler for checking info 
schedule.every(info_rate).minutes.do(main2)

while True:
  schedule.run_pending()
  time.sleep(10) # Sleep for 10 seconds

# Remove img file if there
try:
	os.remove('chart.png')
except Exception:
	print("No img found")

