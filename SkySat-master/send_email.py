""" This class will handle Emails """

import configparser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import formatdate

from pygooglechart import Chart
from pygooglechart import SimpleLineChart
from pygooglechart import XYLineChart
from pygooglechart import SparkLineChart
from pygooglechart import Axis

import smtplib
import ssl
import json
import gviz_api

config = configparser.ConfigParser()
config.read('config.ini')

class Emailer:

	@classmethod
	def grab_sender_details(self):
		self.EMAIL = config.get('Emails', 'sender_email')
		self.PASSWORD = config.get('Emails', 'sender_password')
		return True

	@classmethod
	def grab_contacts(self):
		contacts_lst = config.get('Emails', 'emails')
		self.contacts_lst = contacts_lst.split(',')
		return True

	@classmethod
	def create_graph(self, particle_data, time_data):
		# Set the vertical range from 0 to 2
		max_y = 2

		# Chart size of 500x500 pixels and specifying the range for the Y axis
		chart = SimpleLineChart(500, 500, y_range=[0, max_y])

		# Add the chart data
		data = particle_data

		chart.add_data(data)

		# Set the line color blue
		chart.set_colours(['0000FF'])

		# Set the vertical stripes
		chart.fill_linear_stripes(Chart.CHART, 0, 'CCCCCC', 0.2, 'FFFFFF', 0.2)

		# Set the horizontal dotted lines
		chart.set_grid(0, 25, 5, 5)

		# The Y axis labels 
		left_axis = ['0.25','0.5', '0.75', '1']
		left_axis[0] = ''
		chart.set_axis_labels(Axis.LEFT, left_axis)
		left_axis2 = "Proton Flux"[::-1]
		chart.set_axis_labels(Axis.LEFT, left_axis2)	

		# X axis labels
		chart.set_axis_labels(Axis.BOTTOM, time_data[0:3][::-1])
		chart.set_axis_labels(Axis.BOTTOM, "Time")

		chart.download('chart.png')
		return True

	@classmethod
	def send_email(self, data):
		# Grab information from config file
		self.grab_sender_details()
		self.grab_contacts()

		try:

			context = ssl.create_default_context()
			smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
			smtp_server.starttls()
			# smtp_server.ehlo()
			smtp_server.login(str(self.EMAIL), str(self.PASSWORD))
			
			for email in self.contacts_lst:
				message = MIMEMultipart("alternative")
				message["Subject"] = "SkySat Mission Ops"
				message["From"] = str(self.EMAIL)
				message['Date'] = formatdate(localtime = True)
				message["To"] = email

				# Create plain-text message
				text = "SkySat email\n{data} \nLink: {link}".format(data=data["alert_text"],link=data['link'])
				
				# Create image message
				with open('chart.png', 'rb') as fp:
					img_file = MIMEImage(fp.read())

				# Turn these into plain/html MIMEText objects
				part1 = MIMEText(text, "plain")
				# part2 = MIMEImage(img_file)

				message.attach(part1)
				message.attach(img_file)

				smtp_server.sendmail(self.EMAIL, email , str(message))
        		del message

			smtp_server.quit()

		except Exception as e:
			import traceback
			print("Emailling failure with error: {}".format(e))
			print(traceback.print_exc())

