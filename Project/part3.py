"""
Correct the json file entries and save the corrected data in a new file
"""
import codecs
import json
import numpy as np
import re


def load_data(file):

    data = []
    with codecs.open('boston.json') as f:
        for line in f:
            data.append(json.loads(line))

    return data

def audit_keys(data_in, key):
    key_types = {}
    for entry in data_in:
        try:
            for elem in entry[key]:
                if elem in key_types:
                    key_types[elem].append(entry[key][elem])
                else:
                    key_types[elem] = [entry[key][elem]]
        except:
            pass

    return key_types

def unique_keys(data, key, key_list):
    address_keys = audit_keys(data, key)
    for keys in key_list:
        val = np.array(address_keys[keys])
        print '{}:{}'.format(str(keys),len(np.unique(val)))

def replace_street(data):
    for entry in data:
        try:
            if 'address' in entry:
                for item in entry['address']:
                    if item == 'city' and entry['address'][item] in city_replacements:
                        entry['address'][item] = city_replacements[entry['address'][item]]
                    if item == 'country' and entry['address'][item] in country_replacements:
                        entry['address'][item] = country_replacements[entry['address'][item]]
                    if item == 'state' and entry['address'][item] in state_replacements:
                        entry['address'][item] = state_replacements[entry['address'][item]]
        except:
            pass

    return data

def audit_postcode(data):
    postcode_list = {}
    for item in data:
        try:
            postcode = item['address']['postcode']
            if postcode in postcode_list:
                postcode_list[postcode] += 1
            else:
                postcode_list[postcode] = 1
        except:
            pass
    print postcode_list

## MAIN BODY
# Loading data from the json file
file = 'boston.json'
data = load_data(file)
#print data

# Auditing street data for unique address keys from the json file
address_keys = audit_keys(data, 'address')
print len(address_keys)
keys = address_keys.keys()
print keys

"""
MORE STREET ERRORS
STEPS TO CORRECT:
1. Check for unique data in city, country and states
2. List data to be replaced
3. Replace the errors from the data set
"""
unique_keys(data,'address',['city', 'country','state'])

city_replacements = { 'BOSTON' : 'Boston',
                      'Boston, MA' : 'Boston',
                      'Cambridge, MA' : 'Cambridge',
                      'Cambridge, Massachusetts' : 'Cambridge',
                      'boston' : 'Boston',
                      'somerville' : 'Somerville'}
country_replacements = { 'USA' : 'US' }
state_replacements = {'Massachusetts' : 'MA',
                      'MA- MASSACHUSETTS' : 'MA',
                      'Ma' : 'MA',
                      'ma' : 'MA'}

data = replace_street(data)
unique_keys(data,'address',['city', 'country','state'])

"""
OTHER ERRORS OUTSIDE STREET:
1. POSTAL CODE : missing value, characters present, add-ons present
2. correct errors
"""
# audit for errors
audit_postcode(data)
# correct errors:
code_re = re.compile(r'^([a-zA-Z])+')
for item in data:
    try:
        postcode = item['address']['postcode']
        if '-' in postcode:
            item['address']['add-on'] = postcode.split('-')[1]
            item['address']['postcode'] = postcode.split('-')[0]
        elif len(postcode.split()) > 1:
            item['address']['postcode'] = postcode.split()[1]
        elif code_re.search(postcode):
            # searching and replacing missing values
            for entry in data:
                if entry['address']['city'] == item['address']['city'] and \
                    entry['address']['street'] == item['address']['street'] and item != entry:
                    item['address']['postcode'] = entry['address']['postcode']
                    break
    except: pass
# check corrections
audit_postcode(data)


"""
SAVING THE DATA CORRECTED ABOVE IN A NEW JSON FILE
NAMED: boston_corrected.json
"""

file_out = 'boston_corrected.json'
with codecs.open(file_out, "w") as f:
    for event in data:
        f.write(json.dumps(event) + "\n")

