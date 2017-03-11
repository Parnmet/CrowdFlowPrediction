import CheckinData
import LocationDistance

def findDenseDifference():
    radius = 0.4 #km
    allPlace = CheckinData.findAllVenue()
    for place in allPlace:
        print(""+"== "+place['name'])
        # print(place)
        inRadiusPlaces = LocationDistance.findPlaceInRadius(place['lat'],place['lng'],radius)
        for inRPlace in inRadiusPlaces:
            print(inRPlace['name'])

            #startPredictFlow here
