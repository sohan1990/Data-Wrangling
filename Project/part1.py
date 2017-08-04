""" 
Reading the data from the osm file and looking at the tags and sub tags
Also looking at the street descriptions to make a list of incorrect
inputs that is required to be changed

input: boston.osm
output: None
"""

import xml.etree.ElementTree as ET
import xml.etree.cElementTree as cET
import re
from collections import defaultdict
import pprint



def count_tags(file):
    tags = {}
    for event, elem in cET.iterparse(file):
        if elem.tag in tags.keys():
            tags[elem.tag] += 1
        else:
            tags[elem.tag] = 1
    return tags

def count_secondary_tags(file):
    sec_tags = {}
    for event, elem in cET.iterparse(file):
        if elem.tag =='tag' and 'k' in elem.attrib:
            if elem.get('k') in sec_tags:
                sec_tags[elem.get('k')] += 1
            else:
                sec_tags[elem.get('k')] = 1

    sec_tags = sorted(sec_tags.items(), key = lambda x:x[1], reverse=True)
    return sec_tags

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def audit(file):

    for event, elem in cET.iterparse(file, events = ('start',)):
        if elem.tag =='way' or elem.tag == 'node':
            for tag in elem.iter('tag'):
                if tag.attrib['k'] == 'addr:street':
                    #print tag.attrib
                    audit_street_type(street_types, tag.attrib['v'])


filename = 'boston.osm'

# count tags
tags = count_tags(filename)
print len(tags)
print tags

# count secondary tags
sec_tags = count_secondary_tags(filename)
print len(sec_tags)
print sec_tags

# Check for irregular street names
expected = ['Street', 'Avenue', 'Boulevard', 'Place', 'Drive', 'Lane',
            'Court', 'Square', 'Lane', 'Road', 'Trail', 'Commons',
            'Broadway', 'Center', 'Highway', 'Park', 'Plaza']

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
street_types = defaultdict(set)

audit(filename)
pprint.pprint(dict(street_types))

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
             'Sq'   : 'Square'   }
