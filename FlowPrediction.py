import CheckinData
import LocationDistance
import PredictionService

def findPlace(latlng):
    ll = latlng.split(",")
    foundPlace = CheckinData.findVenueByLl(float(ll[0]),float(ll[1]))
    # print(foundPlace)
    return foundPlace

def sortByDifference(allPlace):
    for place in allPlace:
        now1 = CheckinData.getCurrentCheckinByPlace(place['venueId'])
        next1 = CheckinData.getCurrentPredictByPlace(place['lat'],place['lng'])
        # print("-")
        # print(next1)
        # print(now1)
        
        if(next1 and now1 and next1['density'] != "-" and now1['count'] != "-" ):
            place['dif'] = int(next1['density']) - int(now1['count'])
            place['date'] = next1['date']
            place['time'] = next1['time']
        else:
            place['dif'] = 0
            place['date'] = "-"
            place['time'] = "-"
            
    sortedPlace = sorted(allPlace, key=lambda k: k['dif'])
    return sortedPlace 

def getFlowPrediction(ll):
    radius = 0.4 #km
    allPlace = None
    if ll:
        allPlace = [findPlace(ll)]
    else:
        allPlace = CheckinData.findAllVenue()
    # print(allPlace)
    if allPlace != None and allPlace[0] != None:
        sortedPlaces = sortByDifference(allPlace)
    else:
        return {"crowdFlow":[]}
    # (- place)    
    # negativePlaces = [elem for elem in sortedPlaces if elem['dif'] <0]
    print(sortedPlaces)    
    print("===")
    predictions ={}
    predictions['crowdFlow'] = []
    for place in sortedPlaces:
        predict = {}
        predict['place'] = {}
        predict['place']['lat'] = place['lat']
        predict['place']['lng'] = place['lng']
        predict['place']['name'] = place['name']        
        predict['date'] = place['date']
        predict['time'] = place['time']
        predict['nextPlace'] =[]
        
        if place['dif'] <0:  
            print("-----")
            print("place : ")
            print(place)
            #getPlaceinRadius
            inRadiusPlaces = LocationDistance.findPlaceInRadius(place['lat'],place['lng'],radius)
            #filter place in R from sortedPlaces (+ place in R)
            inRVenueIds = [d['venueId'] for d in inRadiusPlaces]
            print("nearby :")
            nearbyPlace = list(filter(lambda d: d['venueId'] in inRVenueIds, sortedPlaces))
            nearbyPlace = [elem for elem in nearbyPlace if elem['dif'] > 0]
            #add distance for all nearby place
            for nearby in nearbyPlace:
                nearby['distance'] = LocationDistance.findDistance(place['lat'],place['lng'],nearby['lat'],nearby['lng'])
            #sort nearby place ASC 
            # sortedNearbyPlace = sorted(nearbyPlace, key=lambda k: k['dif'],reverse=True)
            print(nearbyPlace)
            #findClosetNumber
            if len(nearbyPlace)>0:
                nextPlace = {}
                target = place['dif']*-1
                print(target)
                stock2 = []
                for n, i in enumerate(nearbyPlace):
                    stock2.append((abs(i["dif"]-target), i["distance"], n))

                closetPlace = nearbyPlace[sorted(stock2)[0][2]]
                foundPlace = [elem for elem in sortedPlaces if elem['venueId'] == closetPlace['venueId']]
                print("found")
                print(foundPlace)
                print("sort")
                foundPlace[0]['dif'] += int(place['dif'])
                print(sortedPlaces)

                nextPlace['lat'] = closetPlace['lat']
                nextPlace['lng'] = closetPlace['lng']
                nextPlace['name'] = closetPlace['name']
                nextPlace['order'] = 1
                predict['nextPlace'].append(nextPlace)
                print(nextPlace)

        predictions['crowdFlow'].append(predict)
        
    print("prediction: ")
    print(predictions)
    return predictions
    

