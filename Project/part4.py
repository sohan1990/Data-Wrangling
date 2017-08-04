"""
Insert the data from the corrected file into mongodb
"""
import xml.etree.cElementTree as cET
import re
from collections import defaultdict
import pprint
import codecs
import json
from pymongo import MongoClient


# Check for irregular street names
expected = ['Street', 'Avenue', 'Boulevard', 'Place', 'Drive', 'Lane',
            'Court', 'Square', 'Lane', 'Road', 'Trail', 'Commons',
            'Broadway', 'Center', 'Highway', 'Park', 'Plaza']

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


def load_data(file):
    data = []
    with codecs.open('boston_corrected.json') as f:
        for line in f:
            data.append(json.loads(line))
    return data

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def audit(file):
    for elem in data:
        if 'address' in elem:
            try:
                audit_street_type(street_types, elem['address']['street'])
            except:
                pass

def get_db():
    client = MongoClient('localhost:27017')
    db = client.examples
    return db

filename = 'boston_corrected.json'
data = load_data(filename)

street_types = defaultdict(set)
audit(data)
#pprint.pprint(dict(street_types))

# connect to Mongodb
db = get_db()
# insert data
db.boston.drop()
db.boston.insert(data)
