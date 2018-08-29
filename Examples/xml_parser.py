# Parse XML dynatrace file and grab relevant information
# Converts all data into JSON
# By Matthew Serna
# 06/22/2018

# Uses eTree to parse XML files
import xml.etree.ElementTree as ET
import xmljson
from json import dumps

try:
    tree = ET.parse('Matts_Dashboard.xml')
    root = tree.getroot()
except Exception:
    print('Unable to load xml file')

file = open('some_file.txt','w')


def xml_parser():
    for msrmnt in root.iter('measurement'):
        # Parse XML and send to JSON converter


def conv_xml_to_json():

    return json

# Temp function to see if JSON wrote correctly
def file_writer(json):
    for line in json:
        file.write(line)
    file.close()


def main():
    xml_parser()
    # Does that look correct
    file_writer(conv_xml_to_json())


main()
