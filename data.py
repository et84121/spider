import csv
import json
import spider
import os
"""
import data from csv ,compare data from spider, save them into json. 

To-DO:
- [ ] make a teacher list
- [ ] make a department list
- [ ] join and compare data from csv and spider 
- [ ] store data to json

"""


def store(token, index, csv_spider):
    result = dict()

    if csv_spider == True:
        result['課程代號'] = token
        result['課程名稱'] = datas[index][2]
        result['CourseName'] = datas[index][3]
        result['修別'] = datas[index][10]
        result['學分數'] = datas[index][1]
        result['選課人數'] = -1  # CSV沒有這個資料
        result['開課單位'] = datas[index][6]
        result['授課老師'] = datas[index][4]
        result['先修科目'] = '無'
        result['上課時間'] = [{'day': datas[index][7][0], '節':datas[index][7][1]}, {
            'day': datas[index][7][0], '節':datas[index][7][-1]}]
        result['Course Department'] = 'none'  # CSV沒有這個資料
        result['Instructor'] = datas[index][5]
        result['Prerequisite'] = 'none'  # CSV沒有這個資料
        result['Session'] = 'none'  # CSV沒有這個資料
        result['課程簡介'] = '無課程簡介'

        return result

    else:
        return spider.get_course(token)[1]


if __name__ == '__main__':
    """
    此python檔被呼叫時的進入點
    """
    fileName = '1061-course'
    csvfile = open('1061.csv', mode='r', encoding='utf-8')

    header, *datas = csv.reader(csvfile)
    # csv 讀檔

    print(header)
    print(datas[1])

    """
    get spiderDatas
    """    
    spiderDatas = list()  # for store datas from spider

    if ( not os.path.isfile('{0}.json'.format(fileName)) ) or ( os.path.getsize('{0}.json'.format(fileName)) == 0 ):
        # if there is not jsonfile here or have a empyt jsonfile, call spider function to get datas
        # or get spiderDatas from exist jsonFile

        with open('{0}.json'.format(fileName), mode='w', encoding='utf-8') as jsonfile:
            for index, token in enumerate((row[0] for row in datas)):
                # 取出全部的課程代號進行迭代
                tmp, tmp1 = spider.get_course(token)
                # if tmp is true means spider have geted the data from web
                spiderDatas.append(tmp1)
                if tmp:
                    print(str(index) + " " + tmp1['課程名稱']+ " " + tmp1['課程代號'])
                else:
                    print(str(index) + " cannot get course: " + str(token))
                
            json.dump(spiderDatas, jsonfile)
            # dump spiderDatas into jsonfile
    else:
        with open('{0}.json'.format(fileName), mode='r', encoding='utf-8') as jsonfile:
            spiderDatas = json.load(jsonfile)
            # get spiderDatas from exist jsonFile
