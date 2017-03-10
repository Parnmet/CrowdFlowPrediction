from pymongo import MongoClient
import CheckinData
import PredictionService
import schedule
import time
import datetime
import json

def job():
    print(datetime.datetime.now().strftime("%H:%M"))
    allPlace = PredictionService.allPlace()['places']
    for place in allPlace:
        latlng = repr(place['lat'])+","+repr(place['lng'])
        # print(latlng)
        den = PredictionService.getNextDensity(latlng)
        # print(den)
        predict = den['density'][0] 
        # jsonPredict = json.dumps(predict)   
        CheckinData.savePredictCheckin(predict)

schedule.every(3).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)