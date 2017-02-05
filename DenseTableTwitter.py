import DensePrediction
import json
import datetime
import csv

# d1 = [0,1,2,3,4,5,6,7,8,7]
# d2 = [1,2,4,4,4,5,6,7,8,8]
# d3 = [2,3,2,3,4,5,6,7,8,9]
# newd = [1,2]
 
# table = [d1,d1,d1,d3,d3,d3,d2,newd]
# table

allPeriod = 288
dayToPredict = 30
Start = "2017-01-01"
dayStart = datetime.datetime.strptime(Start, "%Y-%m-%d")
End = "2017-01-20"
dayEnd = datetime.datetime.strptime(End, "%Y-%m-%d")

dayCheckStart = dayStart-datetime.timedelta(days=dayToPredict)

table = []
prediction = {}
prediction['predict'] = []
csvPredict = []
csvDate = []

#Twitter
with open('SanamluangTweet_None.json') as json_data:
    tweetJSON = json.load(json_data)
    tweetList = tweetJSON['tweet']

    #init 30 day table for predict
    for i in range(dayToPredict):
        dayCheckString = dayCheckStart.strftime("%Y-%m-%d")
        dayGet = [_  for _ in tweetList if _["date"] == dayCheckString]
        if dayGet != []:
            dayList = dayGet[0]['dense']
        else:
            dayList = [0]*allPeriod
        table.append(dayList)
        dayCheckStart+= datetime.timedelta(days=1)
    
    dayPredict = dayStart
    
    #allDayPediction
    while dayPredict <= dayEnd:
        dayPredictString = dayPredict.strftime("%Y-%m-%d")        
        realdense = [_  for _ in tweetList if _["date"] == dayPredictString]
        if realdense != []:
            dayList = realdense[0]['dense']
        else:
            dayList = [0]*allPeriod 
        oneDayPredict = []
        #1 day prediction
        for i in range(allPeriod):
            predict = DensePrediction.findNextDense(table)
            oneDayPredict.append(predict)
            #addRealDense
            if len(table[-1]) == allPeriod:
                table.append([dayList[i]])
            else:
                table[-1].append(dayList[i])
        csvPredict.append(oneDayPredict)
        csvDate.append(dayPredictString)
        prediction['predict'].append({"date":dayPredictString,"dense":oneDayPredict})
        dayPredict += datetime.timedelta(days=1)        

#output prediction
    with open('SanamluangTweet_Predict.json', 'w') as outfile:
        json.dump(prediction, outfile)
    
    csvRow = [list(i) for i in zip(*csvPredict)]
    with open('SanamluangTweet_Predict.csv', 'w', newline='') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerows([csvDate])
        a.writerows(csvRow)
    # print(csvRow)


