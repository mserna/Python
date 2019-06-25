import pytest
from alert_api import AlertsAPI
from send_email import Emailer

""" Email class """
email = Emailer()
def test_grab_contacts():
	assert email.grab_contacts() == True

def test_grab_sender_details():
	assert email.grab_sender_details() == True

def test_create_graph():
	test_particle_lst = [0,1,0.22,0.12]
	test_date_lst = ['2019-02-03T00:00:00','2019-02-04T00:00:00','2019-02-05T00:00:00']
	assert email.create_graph(test_particle_lst,test_date_lst)

def test_send_email():
	test_schema = {
		"alert_text": "pytest",
		"level": 'TESTING',
		"link": "No link"
	}
	assert email.send_email(test_schema) is None

# """ AlertsAPI class """
alert = AlertsAPI()
test_json_data = {
		"alert_text": "Space weather TEST: > 10 MeV proton flux currently at 0",
		"level": 'TEST'
	}
def test_post():
	test_url = 'https://httpbin.org/post'
	assert alert.post(test_url,test_json_data) == 200

def test_create_record():
	assert alert.create_record({},'TEST',0) == test_json_data
