import DensePrediction
import json
import datetime
import csv

# to test with entered day to use to predict  

allDays = ['2017-01-17','2017-01-18','2017-01-19','2017-01-20','2017-01-21','2017-01-22','2017-01-23','2017-01-24','2017-01-25','2017-01-26','2017-01-29','2017-01-30','2017-01-31','2017-02-01','2017-02-02','2017-02-03','2017-02-04','2017-02-05']

# weekDays = ['2016-12-05','2016-12-06','2017-01-17','2017-01-18','2017-01-19','2017-01-20','2017-01-23','2017-01-24','2017-01-25','2017-01-26','2017-01-30','2017-01-31','2017-02-01','2017-02-02','2017-02-03']
# # weekDays = ['2016-12-05','2016-12-06','2017-01-17','2017-01-18','2017-01-19','2017-01-23','2017-01-24','2017-01-25','2017-01-26','2017-01-30','2017-01-31','2017-02-01','2017-02-02']
# weekEnd = ['2016-12-04','2017-01-20','2017-01-21','2017-01-22','2017-01-29','2017-02-03']

# print(len(weekDaysFri))
allPeriod = 288
dayUseToPredict = 14
daysUse = allDays
# print(len(allDays))
table = []
prediction = {}
prediction['predict'] = []
csvPredict = []
csvDate = []

filename ="fqCheckinFile_5FEB_SiamParagon"

with open(filename+'.json') as json_data:
    checkinJSON = json.load(json_data)
    CheckinList = checkinJSON['checkin']
    CheckinList.sort(key=lambda item:item['date'])
    # print(CheckinList)
    carry =-1 
    round =0
    for weekDayOut in daysUse:
        weekUseToPredict = []
        table = []
        for day in daysUse:
            if day != weekDayOut:
                weekUseToPredict.append(day)

        if round > dayUseToPredict:
            carry+=1
        # print(round)
        # print("=====")
        # print(weekDayOut)
        # print("-----")
        
        #init table for predict
        for i in range(len(daysUse)):         
            if daysUse[i] != weekDayOut and i>carry:
                # print(daysUse[i])
                dayGet = [_  for _ in CheckinList if _["date"] == daysUse[i]]
                if dayGet != []:
                    dayList = dayGet[0]['dense']
                else:
                    dayList = ["-"]*allPeriod
                table.append(dayList)
            if len(table) == dayUseToPredict:
                break

        realdense = [_  for _ in CheckinList if _["date"] == weekDayOut]
        if realdense != []:
            dayList = realdense[0]['dense']
        else:
            dayList = ["-"]*allPeriod
        oneDayPredict = []
        #1 day prediction
        for i in range(allPeriod):
                        
            #addRealDense
            if len(table[-1]) == allPeriod:
                oneDayPredict.append(dayList[i])
                table.append([dayList[i]])
            elif table[-1][-1] == "-":
                oneDayPredict.append(dayList[i]) 
                table[-1].append(dayList[i])                               
            else:                    
                if dayList[i] != "-":             
                    predict = DensePrediction.findNextDense(table)
                    oneDayPredict.append(predict)
                else:        
                    oneDayPredict.append("-")
                table[-1].append(dayList[i])
                
            # print(len(table[-1]))
            # print(len(oneDayPredict))
        # print("---------")
        csvPredict.append(oneDayPredict)
        csvDate.append(weekDayOut)
        prediction['predict'].append({"date":weekDayOut,"dense":oneDayPredict}) 
        round+=1

#output prediction
    with open('predict_'+filename+'.json', 'w') as outfile:
        json.dump(prediction, outfile)
    
    csvRow = [list(i) for i in zip(*csvPredict)]
    with open('predict_use_'+str(dayUseToPredict)+filename+'.csv', 'w', newline='') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerows([csvDate])
        a.writerows(csvRow)
    # print(csvRow)

    


