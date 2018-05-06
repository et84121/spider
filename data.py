import csv,json,spider
"""
import data from csv ,compare data from spider, save them into json. 

To-DO:
- [ ] make a teacher list
- [ ] make a department list
- [ ] join and compare data from csv and spider 
- [ ] store data to json

"""
def store(token , index , csv_spider ) :
    result = dict()

    if csv_spider == True :
        result['課程代號'] = token
        result['課程名稱'] = datas[index][2]
        result['CourseName'] = datas[index][3]
        result['修別'] = datas[index][10]
        result['學分數'] =  datas[index][1]
        result['選課人數'] = -1 #CSV沒有這個資料
        result['開課單位'] = datas[index][6]
        result['授課老師'] = datas[index][4]
        result['先修科目'] = '無'
        result['上課時間'] = [{'day': datas[index][7][0],'節':datas[index][7][1]},{'day': datas[index][7][0],'節':datas[index][7][-1]}]
        result['Course Department'] = 'none'#CSV沒有這個資料
        result['Instructor'] = datas[index][5]
        result['Prerequisite'] = 'none' #CSV沒有這個資料
        result['Session'] = 'none' #CSV沒有這個資料
        result['課程簡介'] = '無課程簡介'
        
        return result    

    else :
        return spider.get_course(token)[1]
    


    

fileName = '1061-course'
jsonfile = open('{0}.json'.format(fileName),mode='w',encoding='utf-8')
csvfile = open('1061.csv',mode='r',encoding='utf-8')

header, *datas = csv.reader(csvfile)

print(header)
print(datas[1])

tokenList = list()

#store功能測試用
#tokenList.append(csv_store('000217002' , 0 , True) ) 
#print("儲存測試 : " + tokenList[0]['課程名稱']+  ' 000217002 ' +  tokenList[0]['授課老師'] +  tokenList[0]['Instructor'] + " " +  tokenList[0]['開課單位'])
#print("測試2 :" + str(tokenList[0]['學分數'])[0] + "學分 ")
#print("測試3 : 上課星期 : " + tokenList[0]['上課時間'][0]['day'] + " 開始 : " +  tokenList[0]['上課時間'][0]['節'] + " 結束 : " + tokenList[0]['上課時間'][1]['節']  )

for index, token in enumerate((data[0] for data in datas)): 
 # 取出全部的課程代號進行迭代
    try:
        if spider.get_course(token)[0] :
            tokenList.append(store(token , index , True)) 
        else:
            tokenList.append(store(token , index , False)) 
        
        #print("儲存測試 : " + tokenList[index]['課程名稱'] + ' ' + token + ' ' + tokenList[index]['授課老師'] +  tokenList[index]['Instructor'] + " " +  tokenList[index]['開課單位'])
        #print("測試2 :" + str(tokenList[index]['學分數'])[0] + "學分 ")
        #print("測試3 : 上課星期 : " + tokenList[index]['上課時間'][0]['day'] + " 開始 : " +  tokenList[index]['上課時間'][0]['節'] + " 結束 : " + tokenList[index]['上課時間'][1]['節']  )

        #print("CSV: " + datas[index][2] + " " + token + " " + (datas[index][1][0]) + "學分 " + datas[index][4] +  datas[index][5] + " " + datas[index][6])
        #print("網路端: " + spider_datas[index]['課程名稱']+ " " + token + " " + str(spider_datas[index]['學分數']) + "學分 " + spider_datas[index]['授課老師'] +  spider_datas[index]['Instructor'] + " " + spider_datas[index]['開課單位'])
        #print()
        #print(spider_datas[index]['課程名稱']+ " " + spider_datas[index]['開課系級'])
        #print(spider_datas[index][4] + spider_datas[index][5] )
    except Exception as e:
        print(str(e))
    
    json.dumps(tokenList)

