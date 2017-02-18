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
    allCheckin = fqDb.find({"venueId":venueid})
    inDaysCheckin = {}
    #pick data from 'days' before today
    for checkin in allCheckin:
        thisDate = datetime.datetime.strptime(checkin['datetime'],"%a %b %d %Y %H:%M:%S GMT+0700 (%Z)")
        if thisDate >= startDate:
            thisDateStr = thisDate.strftime("%Y-%m-%d")
            round = timeToRound(thisDate.strftime("%H:%M"))-1
            if thisDateStr not in inDaysCheckin:
                inDaysCheckin[thisDateStr] = []
                inDaysCheckin[thisDateStr].insert(round,checkin['count'])
            else:
                try:
                    oldCount = inDaysCheckin[thisDateStr][round]
                    inDaysCheckin[thisDateStr][round] = (oldCount+checkin['count'])/2    
                except IndexError:
                    inDaysCheckin[thisDateStr].insert(round,checkin['count'])  
    return inDaysCheckin
 
# print(getCheckinByPlace("4b0587fdf964a52034ab22e3",3))
# print(list(fqDb.find().sort("_id", -1).limit(1)))
