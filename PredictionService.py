#!/usr/bin/python
#-*-coding: utf-8 -*-
import CheckinData
import DenseTableFqCheckin
import datetime
import math
import FlowPrediction

ladkrabang = ['4df8d001814dd2985fdd35d8','4bf774814a67c9288ec623cf','4bb9a4a198c7ef3b61373202','4af833a6f964a5205a0b22e3','4c034d0cf56c2d7fa6c71c66']

def allVenue():
    place = CheckinData.findAllVenue()
    places = []
    for p in place:
        if(p['venueId'] not in ladkrabang):
            places.append(p)
    return places

def allPlace():
    place = allVenue()
    allplace = {}
    allplace['places'] = []
    for p in place:
        if(p['venueId'] not in ladkrabang):
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

def getNextDensity(latlng,predictTime):
    place = findPlace(latlng)
    dense = {}
    dense['density']=[]
    if place != None:
        venueId = place['venueId']
        max = CheckinData.findMaxOfPlace(venueId)    
        checkinJSON = CheckinData.getCheckinByPlace(venueId,DenseTableFqCheckin.dayUseToPredict+1)
        prediction = DenseTableFqCheckin.predictNextDenseFromcheckin(checkinJSON,predictTime)
        place.pop('venueId', None) 
        next = {}
        next['place'] =place
        next['time'] = prediction['time']
        next['date'] = prediction['date']
        next['density'] = findDenseLevel(max,prediction['dense'])  
        dense['density'].append(next)
        print("next"+str(predictTime)+"min: "+str(checkinJSON['checkin'][0]['dense'][-1]))
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

def getNextPredictCheckinNumber(latlng,predictTime):
    place = findPlace(latlng)
    dense = {}
    if place != None:
        venueId = place['venueId']
        checkinJSON = CheckinData.getCheckinByPlace(venueId,DenseTableFqCheckin.dayUseToPredict+1)
        prediction = DenseTableFqCheckin.predictNextDenseFromcheckin(checkinJSON,predictTime)
        place.pop('venueId', None) 
        dense['place'] =place
        dense['time'] = prediction['time']
        dense['date'] = prediction['date']
        dense['density'] = prediction['dense']
        # print(prediction['dense'])
        # print("next 5 min: "+str(checkinJSON['checkin'][0]['dense'][-1]))
    return dense

def getCurrentFlow(latlng):
    allPlace = None
    if latlng:
        allPlace = [findPlace(latlng)]
    else:
        allPlace = allVenue()
    # print(allPlace)
    if allPlace != None and allPlace[0] != None:
        for place in allPlace:
            next1 = CheckinData.getCurrentCheckinByPlace(place['venueId'])
            now1 = CheckinData.getPreviousCheckinByPlace(place['venueId'])
            if(next1 and now1 and next1['count'] != "-" and now1['count'] != "-" ):
                place['dif'] = int(next1['count']) - int(now1['count'])
                place['date'] = next1['date']
                place['time'] = next1['time']
            else:
                place['dif'] = 0
                place['date'] = "-"
                place['time'] = "-"
                
        sortedPlace = sorted(allPlace, key=lambda k: k['dif'])
        return FlowPrediction.getFlowPrediction(sortedPlace)
    else:
        return {"crowdFlow":[]}

def getNextFlow(latlng,predictTime):
    allPlace = None
    if latlng:
        allPlace = [findPlace(latlng)]
    else:
        allPlace = allVenue()
    # print(allPlace)
    if allPlace != None and allPlace[0] != None:
        for place in allPlace:
            now1 = CheckinData.getCurrentCheckinByPlace(place['venueId'])
            next1 = getNextPredictCheckinNumber(repr(place['lat'])+","+repr(place['lng']),predictTime)
            # print(now1)
            # print(next1)
            if(next1 and now1 and next1['density'] != "-" and now1['count'] != "-" ):
                place['dif'] = int(next1['density']) - int(now1['count'])
                place['date'] = next1['date']
                place['time'] = next1['time']
            else:
                place['dif'] = 0
                place['date'] = "-"
                place['time'] = "-"
                
        sortedPlace = sorted(allPlace, key=lambda k: k['dif'])
        return FlowPrediction.getFlowPrediction(sortedPlace)
    else:
        return {"crowdFlow":[]}
    