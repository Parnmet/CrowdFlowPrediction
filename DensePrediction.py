
d1 = [0,1,2,3,4,5,6,7,8,9]
d2 = [1,1,2,3,4,5,6,7,8,8]
table = [d1,d2,d2,d2,d2,d2,d1]

next_time = 0
current_time = 9
current_value = table[-1][9]
table_len = len(table)-1

equal_dense = []
#[{index,next_value},{...},...]

#find equal dense
for index in range(table_len):
    if table[index][9] == current_value:
        equal_dense.append({"index":index,"next_value":table[index+1][0]})

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
# else:
#     for index in range(table_len):
#         if table[index][9] == current_value-(index+1):
            
    

print(predict)


