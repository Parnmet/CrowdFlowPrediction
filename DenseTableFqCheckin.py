import DensePrediction
import json
import datetime
import csv

weekDay = ['05-12-2016','06-12-2016','17-01-2017','18-01-2017','19-01-2017','23-01-2017','24-01-2017','25-01-2017','26-01-2017','30-01-2017','31-01-2017','01-02-2017','02-02-2017']
weekEnd = ['04-12-2016','20-01-2017','21-01-2017','22-01-2017','29-01-2017','03-02-2017']

allPeriod = 288
dayToPredict = 7
Start = "2017-01-25"
dayStart = datetime.datetime.strptime(Start, "%Y-%m-%d")
End = "2017-01-25"
dayEnd = datetime.datetime.strptime(End, "%Y-%m-%d")

dayCheckStart = dayStart-datetime.timedelta(days=dayToPredict)

table = []
prediction = {}
prediction['predict'] = []
csvPredict = []
csvDate = []

filename ="fqCheckinFile1FEB_4b0587fdf964a52034ab22e3"

with open(filename+'.json') as json_data:
    checkinJSON = json.load(json_data)
    CheckinList = checkinJSON['checkin']

    #init 30 day table for predict
    for i in range(dayToPredict):
        dayCheckString = dayCheckStart.strftime("%Y-%m-%d")
        dayGet = [_  for _ in CheckinList if _["date"] == dayCheckString]
        if dayGet != []:
            dayList = dayGet[0]['dense']
        else:
            dayList = ["-"]*allPeriod
        table.append(dayList)
        dayCheckStart+= datetime.timedelta(days=1)
    
    dayPredict = dayStart
    
    #allDayPediction
    while dayPredict <= dayEnd:
        dayPredictString = dayPredict.strftime("%Y-%m-%d")        
        realdense = [_  for _ in CheckinList if _["date"] == dayPredictString]
        if realdense != []:
            dayList = realdense[0]['dense']
        else:
            dayList = ["-"]*allPeriod 
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
    with open('predict_'+filename+'.json', 'w') as outfile:
        json.dump(prediction, outfile)
    
    csvRow = [list(i) for i in zip(*csvPredict)]
    with open('predict_'+filename+'.csv', 'w', newline='') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerows([csvDate])
        a.writerows(csvRow)
    # print(csvRow)

    


