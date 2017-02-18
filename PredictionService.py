import CheckinData
import DenseTableFqCheckin
import datetime

def findVenueId(latlng):
    return "4b0587fdf964a52034ab22e3"

def getCurrentDensity(latlng):
    venueId = findVenueId(latlng)
    checkinJSON = CheckinData.getCheckinByPlace(venueId,1)
    time = datetime.datetime.now().strftime("%H:%M")
    dense = {}
    dense['current']=[]
    current = {}
    current['time'] = datetime.datetime.now().strftime("%H:%M")
    current['date'] = datetime.datetime.now().strftime("%Y-%m-%d")
    current['dense'] = checkinJSON['checkin'][0]['dense'][-1]  
    dense['current'].append(current)
    return dense

def getNextDensity(latlng):
    venueId = findVenueId(latlng)
    checkinJSON = CheckinData.getCheckinByPlace(venueId,DenseTableFqCheckin.dayUseToPredict+1)
    prediction = DenseTableFqCheckin.predictNextDenseFromcheckin(checkinJSON)
    return prediction

print(getNextDensity(""))
print(getCurrentDensity(""))
