import CheckinData
import DenseTableFqCheckin

def findVenueId(latlng):
    return "4b0587fdf964a52034ab22e3"

def getCurrentDensity(latlng):
    return None

def getNextDensity(latlng):
    venueId = findVenueId(latlng)
    checkinJSON = CheckinData.getCheckinByPlace(venueId,DenseTableFqCheckin.dayUseToPredict+1)
    prediction = DenseTableFqCheckin.predictNextDenseFromcheckin(checkinJSON)
    return prediction

print(getNextDensity(""))