
d1 = [0,1,2,3,4,5,6,7,8,9]
d2 = [1,1,2,3,4,5,6,7,8,8]
d3 = [2,1,2,3,4,5,6,7,8,10]
 
table = [d3,d3,d3,d2,d2,d2,d1]

next_time = 0
current_time = 9
current_value = table[-1][9]
table_len = len(table)-1

equal_dense = []
#[{index,next_value},{...},...]
 
#find equal dense
for index in range(table_len):
    if table[index][current_time] == current_value:
        equal_dense.append({"index":index,"next_value":table[index+1][next_time]})

while len(equal_dense) == 0:
    count = 1
    for index in range(table_len):          
        if table[index][current_time] == current_value-count or table[index][current_time] == current_value+count:
            print
            equal_dense.append({"index":index,"next_value":table[index+1][next_time]})
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

# print(equal_dense)          
    

print(predict)


