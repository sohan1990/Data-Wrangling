""" 
Formatting the data into the below mentioned dictionary form:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

and saving it as a json file. 
Also replacing the incorrect street names with an uniform and correct
replacement.

input: boston.osm
output: boston.json

"""
import xml.etree.ElementTree as ET
import xml.etree.cElementTree as cET
import re
from collections import defaultdict
import pprint
import codecs
import json


filename = 'boston.osm'

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
ADDR = re.compile(r'^addr:([a-z|_]+)*$')
COLON = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
LOWER = re.compile(r'^([a-z]|_)*$')

CREATED = ['version', 'changeset', 'timestamp', 'user', 'uid']
POSITION = ['lat', 'lon']
BASIC = ['id', 'visible']


mapping = {  'Ave'  : 'Avenue',
             'Ave.' : 'Avenue',
             'Ext'  : 'Exit',
             'Pl'   : 'Plaza',
             'Rd'   : 'Road',
             'ST'   : 'Street',
             'St'   : 'Street',
             'St.'  : 'Street',
             'St,'  : 'Street',
             'st'   : 'Street',
             'Sq'   : 'Square',
             'Sq.'  : 'Square',
             'Hwy'  : 'Highway'}

def correct_name(street_name, dict = mapping):
    name = street_name.split()[0:-1]
    value = street_name.split()[-1]
    if value in dict:
        value = dict[value]
    name = name + [value]

    return " ".join(name)

def format_element(elem, basic_fields=BASIC , position_fields=POSITION, created_fields=CREATED,
                   problem_chars=PROBLEMCHARS, addr_chars=ADDR, colon_chars=COLON, lower_chars=LOWER):
    created = {}
    pos = []
    address = {}
    entry = {}


    if elem.tag == 'node' or elem.tag == 'way':
        # Entering the basic tags
        entry['id'] = elem.attrib['id']
        entry['type'] = elem.tag
        entry['visible'] = 'true'
        #if elem.tag == 'way':
        #    print elem.attrib
        # Entering the tags for the created sub-field
        for item in created_fields:
            created[item] = elem.attrib[item]
        entry['created'] = created
        # Entering the tags for the position sub-filed
        for item in position_fields:
            try:
                pos.append(elem.attrib[item])
            except:
                pos.append(None)
        entry['pos'] = pos
        # Entering the sub-tags
        for item in elem.iter('tag'):
            key = item.attrib['k']
            value = item.attrib['v']
            # if tag contains problem characters
            if problem_chars.search(key):
                pass
            # if tag contains normal lower character entries
            elif lower_chars.search(key):
                entry[key] = value
            # if the tag contains an address
            elif addr_chars.search(key):
                if 'addr:street' in key:
                    value = correct_name(value)
                key = key.split(':')[-1]
                address[key] = value
        if address != {}:
            entry['address'] = address
            #print address
    return entry


# Main body
new_record = []
file_out = "{}.json".format(filename.split('.')[0])

with codecs.open(file_out, "w") as f:
    for event, elem in cET.iterparse(filename):
        formatted_element = format_element(elem)

        if formatted_element != {}:
            #pprint.pprint(formatted_element)
            new_record.append(formatted_element)
            f.write(json.dumps(formatted_element) + "\n")
