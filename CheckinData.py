from pymongo import MongoClient
import datetime
import DenseTableFqCheckin

client = MongoClient("10.0.1.3")
db = client.SocialData
fqDb = db.FQ_CHECKIN
db2 = client.Predict

def timeToRound(timeStr):
    #time format HH:MM
    time = timeStr.split(":")
    secs = ((int(time[0])*60+int(time[1]))/5)+1
    return secs

def findNextDateTime():
    dateNow = datetime.datetime.now()
    round = timeToRound(dateNow.strftime("%H:%M"))
    dateNext = None
    if round+1>288:
        round=1
        dateNext = dateNow+ datetime.timedelta(days=1)
    else:
        round+=1 
        dateNext = dateNow.replace(hour=0, minute=0, second=0, microsecond=0)   
    len = (round-1)*5
    dateNext = dateNext + datetime.timedelta(minutes=len)
    return dateNext

def getCheckinByPlace(venueid,days):

    todayDate = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    startDate = todayDate-datetime.timedelta(days=days-1)
    allCheckin = fqDb.find({"venueId":venueid}).sort("_id",-1).limit(10000)
    # print(startDate)
    inDaysCheckin = {}
    #pick data from 'days' before today
    for checkin in allCheckin:
        thisDate = datetime.datetime.strptime(checkin['datetime'],"%a %b %d %Y %H:%M:%S GMT+0700 (%Z)")
        # print(thisDate)
        if thisDate >= startDate:
            # print(thisDate)
            thisDateStr = thisDate.strftime("%Y-%m-%d")
            round = timeToRound(thisDate.strftime("%H:%M"))-1
            
            # print(round)
            # if thisDate>=todayDate:
            #     if(round>20):
            #         print(thisDate.strftime("%H:%M"))
                # print(round)
            if thisDateStr not in inDaysCheckin:
                if thisDate < todayDate:
                    inDaysCheckin[thisDateStr] = ["-"]*288
                    inDaysCheckin[thisDateStr][round] = checkin['count']
                else:
                    # currentTime = datetime.datetime.now().strftime("%H:%M")
                    # inDaysCheckin[thisDateStr] = ["-"]*timeToRound(currentTime)   
                    # print(timeToRound(datetime.datetime.now().strftime("%H:%M")))
                    inDaysCheckin[thisDateStr] = ["-"]*(timeToRound(datetime.datetime.now().strftime("%H:%M"))-1)     
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
    # for day in inDaysCheckin:
    #     print(len(inDaysCheckin[day]))
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

def findInRadiusVenue(minLat,maxLat,minLng,maxLng):
    return db.FQ_VENUE.find({
        "location.lat": {"$gte": minLat,"$lte": maxLat},
        "location.lng": {"$gte": minLng,"$lte": maxLng}
        })    

def savePredictCheckin(predict):
    # print(predict)
    # print(db2.DENSE_FQCHECKIN.count())
    db2.DENSE_FQCHECKIN.insert_one(predict)

def findPredictByPlace(lat,lng):
    return db2.DENSE_FQCHECKIN.find({"place.lat":lat,"place.lng":lng})

def getCurrentPredictByPlace(lat,lng):
    dateNext = findNextDateTime()
    last = db2.DENSE_FQCHECKIN.find_one({"place.lat":lat,"place.lng":lng,"date":dateNext.strftime("%Y-%m-%d"),"time":dateNext.strftime("%H:%M")})
    # for l in last:
    return last
    # return None
    