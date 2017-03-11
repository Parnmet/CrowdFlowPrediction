from math import cos, asin, sqrt
import math
import csv
import CheckinData

def findDistance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a))

def getBoundFromLL(lat,lng,radiusInKm):
    kmInLongitudeDegree = 111.320 * math.cos( lat / 180.0 * math.pi)
    deltaLat = float(radiusInKm) / 111.1
    deltaLong = float(radiusInKm) / kmInLongitudeDegree
    minLat = lat - deltaLat  
    maxLat = lat + deltaLat
    minLng = lng - deltaLong 
    maxLng = lng + deltaLong
    return [minLat,maxLat,minLng,maxLng]

def findPlaceInRadius(lat,lng,radiusInKm):
    bound = getBoundFromLL(lat,lng,radiusInKm+0.1)
    places = CheckinData.findInRadiusVenue(bound[0],bound[1],bound[2],bound[3])
    inRadiusPlace = []
    for place in places:
        findLat = place['location']['lat']
        findLng = place['location']['lng']
        distance = findDistance(lat,lng,findLat,findLng)
        if(distance<=radiusInKm) and lat!=findLat and lng!=findLng:
            newPlace = {}
            newPlace['venueId']=place['id']
            newPlace['name']=place['name']
            newPlace['lat']=findLat
            newPlace['lng']=findLng
            inRadiusPlace.append(newPlace)
    return inRadiusPlace
