""" This class will handle Alerts """

import json
import requests
from pprint import pprint

class AlertsAPI(object):

	def __init__(self):
		self.schema = {
			"alert_text": "Space weather INFO: > 10 MeV proton flux currently at 0",
			"level": 'INFO',
			"link": "https://www.swpc.noaa.gov/products/goes-proton-flux"
		}

	@classmethod
	def post(self,url,data):
		try:
			res = requests.post(url, json=data)
		except Exception as e:
			print("Could not POST, error {}".format(e))

		return res.status_code

	@classmethod
	def create_record(self,json, level, value):
		json['alert_text'] = "Space weather {level}: > 10 MeV proton flux currently at {value}".format(level=level, value=value)
		json['level'] = level

		# Returns schema in JSON format
		return json

