"""
Performing various data analysis on the data through mongodb
"""
import pprint
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client.examples

# DATA OVERVIEW
# NO OF DOCS
print 'No of data',db.boston.count()
# NO OF WAYS
print 'No of way',db.boston.find({'type':'way'}).count()
# NO OF NODES
print 'No of node',db.boston.find({'type':'node'}).count()
# NO OF UNIQUE USERS
top_users = db.boston.aggregate([{"$match":{"created.user":{"$exists":1}}},
                                {"$group":{"_id":"$created.user", "count":{"$sum":1}}},
                                {"$sort":{"count":-1}}])
user = []
for item in top_users:
    user.append(item['_id'])
print "No of unique users: {}".format(len(user))
# TOP CONTRIBUTING USER
print "Top user: ",user[0]

# NO OF ONE TIME USERS
one_time_user = db.boston.aggregate([{"$match":{"created.user":{"$exists":1}}},
                                {"$group":{"_id":"$created.user", "count":{"$sum":1}}},
                                {"$group":{"_id":"$count", "count":{"$sum":1}}},
                                {"$sort":{"count":-1}},
                                {"$limit":1}])
for item in one_time_user:
    print "No of one time users: ",item['count']


# MOST ENTRIES ACCORDING TO POSTAL CODES
postcode = db.boston.aggregate([{"$match":{"address.postcode":{"$exists":1}}},
                                {"$group":{"_id":"$address.postcode", "count":{"$sum":1}}},
                                {"$sort":{"count":-1}}])
                                #{"$limit":10}])
print 'Descending order of postcodes:'
for item in postcode:
    print '{} entries for postal code: {}'.format(item['count'], item['_id'])

# MOST ENTRIES ACCORDING TO STREET
street = db.boston.aggregate([{"$match":{"address.street":{"$exists":1}}},
                              {"$group":{"_id":"$address.street", "count":{"$sum":1}}},
                              {"$sort":{"count":-1}}, {"$limit":10}])
print '\nDescending order of street count:'
for item in street:
    print '{} entries for street: {}'.format(item['count'], item['_id'])


# 10 MOST APPEARING AMENITIES
print "\nAmenities"
amenity = db.boston.aggregate([{"$match":{"amenity":{"$exists":1}}},
                               {"$group":{"_id":"$amenity", "count":{"$sum":1}}},
                               {"$sort":{"count":-1}},
                               {"$limit":10}])
for amn in amenity:
    print amn

# Parking places can be broken down into
print "\nParking places:"
parking = db.boston.aggregate([{"$match":{"amenity":{"$exists":1}, "amenity":"parking"}},
                               {"$group":{"_id":"$parking", "count":{"$sum":1}}},
                               {"$sort":{"count":-1}}
                               ])
for item in parking:
    print item

# Parking places can be broken down into
print "\nRestaurants:"
restaurant = db.boston.aggregate([{"$match":{"amenity":{"$exists":1}, "amenity":"restaurant"}},
                                  {"$group":{"_id":"$cuisine", "count":{"$sum":1}}},
                                  {"$sort":{"count":-1}},
                                  {"$limit": 10}])
for item in restaurant:
    print item

# Place of worship can be broken down into
print "\nReligions:"
religion = db.boston.aggregate([{"$match":{"amenity":{"$exists":1}, "amenity":"place_of_worship"}},
                                {"$group":{"_id":"$religion", "count":{"$sum":1}}},
                                {"$sort":{"count":-1}}
                                ])
for item in religion:
    print item
