#!/usr/bin/python
#-*-coding: utf-8 -*-
import CheckinData
import DenseTableFqCheckin
import datetime
import math


def allVenue():
    place = CheckinData.findAllVenue()
    return place

def allPlace():
    place = allVenue()
    allplace = {}
    allplace['places'] = []
    for p in place:
        p.pop('venueId', None)
        allplace['places'].append(p)
    return allplace

def findPlace(latlng):
    ll = latlng.split(",")
    foundPlace = CheckinData.findVenueByLl(float(ll[0]),float(ll[1]))
    return foundPlace

def getCurrentDensity(latlng):
    dense = {}
    dense['density']=[]
    place = findPlace(latlng)
    if place != None:
        venueId = place['venueId']
        checkinJSON = CheckinData.getCheckinByPlace(venueId,1)
        max = CheckinData.findMaxOfPlace(venueId)
        time = datetime.datetime.now().strftime("%H:%M")

        place.pop('venueId', None)        
        current = {}
        current['place'] =place
        current['time'] = datetime.datetime.now().strftime("%H:%M")
        current['date'] = datetime.datetime.now().strftime("%Y-%m-%d")
        current['density'] = findDenseLevel(max,checkinJSON['checkin'][0]['dense'][-1])  
        dense['density'].append(current)
        print("now: "+str(checkinJSON['checkin'][0]['dense'][-1]))
    return dense

def getNextDensity(latlng):
    place = findPlace(latlng)
    dense = {}
    dense['density']=[]
    if place != None:
        venueId = place['venueId']
        max = CheckinData.findMaxOfPlace(venueId)    
        checkinJSON = CheckinData.getCheckinByPlace(venueId,DenseTableFqCheckin.dayUseToPredict+1)
        prediction = DenseTableFqCheckin.predictNextDenseFromcheckin(checkinJSON)
        place.pop('venueId', None) 
        next = {}
        next['place'] =place
        next['time'] = prediction['time']
        next['date'] = prediction['date']
        next['density'] = findDenseLevel(max,prediction['dense'])  
        dense['density'].append(next)
        print("next 5 min: "+str(checkinJSON['checkin'][0]['dense'][-1]))
    return dense
def findDenseLevel(max,count):
    if count != "-":
        range = math.ceil(((1.0+max)/3))
        if count < range:
            return "LOW"
        elif count < range*2:
            return "MEDIUM"
        else:
            return "HIGH"
    return "LOW"


def getNextPredictCheckinNumber(latlng):
    place = findPlace(latlng)
    dense = {}
    if place != None:
        venueId = place['venueId']
        checkinJSON = CheckinData.getCheckinByPlace(venueId,DenseTableFqCheckin.dayUseToPredict+1)
        prediction = DenseTableFqCheckin.predictNextDenseFromcheckin(checkinJSON)
        place.pop('venueId', None) 
        dense['place'] =place
        dense['time'] = prediction['time']
        dense['date'] = prediction['date']
        dense['density'] = prediction['dense']
        # print(prediction['dense'])
        # print("next 5 min: "+str(checkinJSON['checkin'][0]['dense'][-1]))
    return dense
# print(getNextDensity(""))
# print(getCurrentDensity(""))
# print(allVenue())
# print( findPlace("13.74601902837004,100.53435495832393"))