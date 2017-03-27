from pymongo import MongoClient
import CheckinData
import PredictionService
import schedule
import time
import datetime
import json
import FlowPrediction

def job():
    print(datetime.datetime.now().strftime("%H:%M"))
    allPlace = PredictionService.allPlace()['places']
    for place in allPlace:
        latlng = repr(place['lat'])+","+repr(place['lng'])
        # print(latlng)
        predict = PredictionService.getNextPredictCheckinNumber(latlng,5)
        # print(den)
        # jsonPredict = json.dumps(predict)   
        CheckinData.savePredictCheckin(predict)

def flow():
    predicts = FlowPrediction.getFlowPrediction(None)
    for predict in predicts['crowdFlow']:
        CheckinData.savePredictFlow(predict)
        
schedule.every(1).minutes.do(job)
schedule.every(3).minutes.do(flow)

# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)