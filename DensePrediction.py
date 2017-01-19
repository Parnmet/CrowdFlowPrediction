
d1 = [0,1,2,3,4,5,6,7,8,7]
d2 = [1,2,4,4,4,5,6,7,8,8]
d3 = [2,3,2,3,4,5,6,7,8,9]
newd = [1,2]
 
table = [d1,d1,d1,d3,d3,d3,d2,newd]

allPeriod = 10
last_length = len(table[-1])
if last_length == allPeriod:
    current_time = allPeriod-1
    next_time = 0    
else:
    current_time = last_length-1
    next_time = current_time+1  
table_len = len(table)-1  
current_value = table[-1][current_time]

equal_dense = []
#[{index,next_value},{...},...]
 
#find equal dense
for index in range(table_len): 
    if table[index][current_time] == current_value:
        if last_length == allPeriod:
            equal_dense.append({"index":index,"next_value":table[index+1][next_time]})
        else:
            equal_dense.append({"index":index,"next_value":table[index][next_time]})
count = 1
          
while len(equal_dense) == 0:
    for index in range(table_len): 
        if (table[index][current_time] == current_value-count) or (table[index][current_time] == current_value+count):            
            if last_length == allPeriod:
                equal_dense.append({"index":index,"next_value":table[index+1][next_time]})
            else:
                equal_dense.append({"index":index,"next_value":table[index][next_time]})     
    count+=1

if len(equal_dense) == 1:
    predict = equal_dense[0]['next_value']
elif len(equal_dense) > 1:
    freq = [] 
    #[{value,latest_index,freq},{...},...]
    for e in equal_dense:
        found = False
        for f in freq:
            if e['next_value'] == f['value']:
                if e['index'] > f['latest_index']:
                    f['latest_index'] = e['index']
                f['freq'] +=1
                found = True
                break
        if len(freq) == 0 or found == False:
            freq.append({"value":e['next_value'],"latest_index":e['index'],"freq":1})
    if len(freq) == 1:
        predict = freq[0]['value']
    elif len(freq)>1:
        max_freq = max(freq, key=lambda k: k['freq'])['freq']
        filterList = list(filter(lambda d: d['freq'] in [max_freq], freq)) 
        max_index = max(filterList, key=lambda k: k['latest_index'])
        predict=max_index['value']

print(predict)


