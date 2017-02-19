from pymongo import MongoClient
import datetime

client = MongoClient("10.0.1.3")
db = client.SocialData
fqDb = db.FQ_CHECKIN

def timeToRound(timeStr):
    #time format HH:MM
    time = timeStr.split(":")
    secs = ((int(time[0])*60+int(time[1]))/5)+1
    return secs

def getCheckinByPlace(venueid,days):

    todayDate = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    startDate = todayDate-datetime.timedelta(days=days-1)
    allCheckin = fqDb.find({"venueId":venueid}).limit(20000)
    inDaysCheckin = {}
    #pick data from 'days' before today
    for checkin in allCheckin:
        thisDate = datetime.datetime.strptime(checkin['datetime'],"%a %b %d %Y %H:%M:%S GMT+0700 (%Z)")
        if thisDate >= startDate:
            thisDateStr = thisDate.strftime("%Y-%m-%d")
            round = timeToRound(thisDate.strftime("%H:%M"))-1
            # if thisDate>=todayDate:
            #     print(thisDate.strftime("%H:%M"))
            #     print(round)
            if thisDateStr not in inDaysCheckin:
                if thisDate < todayDate:
                    inDaysCheckin[thisDateStr] = ["-"]*288
                    inDaysCheckin[thisDateStr][round] = checkin['count']
                else:
                    # currentTime = datetime.datetime.now().strftime("%H:%M")
                    # inDaysCheckin[thisDateStr] = ["-"]*timeToRound(currentTime)   
                    inDaysCheckin[thisDateStr] = []     
                    inDaysCheckin[thisDateStr].insert(round,checkin['count'])
            else:
                try:
                    oldCount = inDaysCheckin[thisDateStr][round]
                    if oldCount == "-":
                        inDaysCheckin[thisDateStr][round] = checkin['count']
                    else:
                        inDaysCheckin[thisDateStr][round] = (oldCount+checkin['count'])/2    
                except IndexError:
                    inDaysCheckin[thisDateStr].insert(round,checkin['count'])  

    countCheckin = {}
    countCheckin['checkin'] = []
    for date,dense in inDaysCheckin.items():    
        oneDay = {}
        oneDay['date'] = date
        oneDay['dense'] = dense
        countCheckin['checkin'].append(oneDay)
    return countCheckin

def findMaxOfPlace(venueid):
    return fqDb.find({"venueId":venueid}).sort("count",-1).limit(1)[0]['count']

def findAllVenue():
    allVenue = db.FQ_VENUE.find()
    venuelist = []
    for venue in allVenue:
        newVenue = {}
        newVenue['venueId'] = venue['id']
        newVenue['name'] = venue['name']
        newVenue['lat'] = venue['location']['lat']
        newVenue['lng'] = venue['location']['lng']
        venuelist.append(newVenue)
    return venuelist

def findVenueByLl(lat,lng):
    venue = db.FQ_VENUE.find_one({"location.lat":lat})
    if venue != None:
        newVenue = {}
        newVenue['venueId'] = venue['id']
        newVenue['name'] = venue['name']
        newVenue['lat'] = venue['location']['lat']
        newVenue['lng'] = venue['location']['lng']
        return newVenue
    return None
# print(getCheckinByPlace("4b0587fdf964a52034ab22e3",2))
# print(list(fqDb.find().sort("_id", -1).limit(1)))
# print(findMaxOfPlace("4b0587fdf964a52034ab22e3"))
# print(findVenueByLl(13.74601902837004,100.53421212920541))