import csv
import json
import spider
import os
import logging
"""
import data from csv ,compare data from spider, save them into json.

To-DO:
- [ ] make a teacher list
- [ ] make a department list
- [ ] join and compare data from csv and spider
- [ ] store data to json

usefull json visualizer : http://chris.photobooks.com/json/default.htm
"""


def time_converter(text):
    """
    '未定或彈性' '三D56' '二78三CD'
    convert '三D56' into '[{'day':'三','section':'D'},{'day':'三','section':'5'},{'day':'三','section':'6'}]'

    各節次上課時間對照表 http://aca.nccu.edu.tw/p3-register_choose_Ln_timeMatch.asp
    """
    result = list()
    text = str(text)
    WEEK = '一二三四五六日'
    SECTION = 'AB1234CD5678EFGH'
    week = None
    if text == '未定或彈性' or text == '':
        return None
    else:
        for char in text:
            if char in WEEK:
                week = char
            elif char in SECTION:
                result.append({'day': week, 'section': char})
    return result

if __name__ == '__main__':
    """
    此python檔被呼叫時的進入點
    """

    # set logging
    logger = logging.getLogger('data.py')
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler('log.txt', 'w', 'utf-8')
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    # set logging

    fileName = '1061-course'
    csvfile = open('1061.csv', mode='r', encoding='utf-8')
    header, *csvDatas = csv.reader(csvfile)
    # csv 讀檔

    print(header)
    print(csvDatas[1])

    """
    get spiderDatas
    """
    spiderDatas = list()  # for store datas from spider

    if (not os.path.isfile('{0}-spider.json'.format(fileName))) or (os.path.getsize('{0}-spider.json'.format(fileName)) == 0):
            # if there is not jsonfile here or have a empyt jsonfile,
            # call spider function to get datas
            # or get spiderDatas from exist jsonFile

        with open('{0}-spider.json'.format(fileName), mode='w', encoding='utf-8') as jsonfile:
            errorNum = 0
            successNum = 0
            failNum = 0
            # counter for stats

            for index, token in enumerate((row[0] for row in csvDatas)):
                # 取出全部的課程代號進行迭代
                result = spider.get_course(token)
                spiderDatas.append(result)
                if result['status'] == 'success':
                    successNum += 1
                    logger.info(str(index) + " " +
                                result['課程名稱'] + " " + result['課程代號'])
                elif result['status'] == 'fail':
                    failNum += 1
                    logger.warning(
                        str(index) + " 無法取得課程(無資料): " + str(token))
                elif result['status'] == 'error':
                    errorNum += 1
                    logger.error(str(index) + ' Error: ' + str(token))

            logger.info('Get data from net ,And success: {0}, fail: {1}, error:{2}'.format(
                successNum, failNum, errorNum))
            json.dump(spiderDatas, jsonfile)
            # dump spiderDatas into jsonfile
    else:
        with open('{0}-spider.json'.format(fileName), mode='r', encoding='utf-8') as jsonfile:
            spiderDatas = json.load(jsonfile)
            # get spiderDatas from exist jsonFile

            errorNum = 0
            successNum = 0
            failNum = 0
            # counter for stats

            for index, data in enumerate(spiderDatas):
                if data['status'] == 'success':
                    successNum += 1
                    logger.info(str(index) +
                                " " + data['課程名稱'] +
                                " " + data['課程代號']
                                )
                elif data['status'] == 'fail':
                    failNum += 1
                    logger.warning(str(index) +
                                   " 無法取得課程(無資料): " +
                                   str(data['課程代號'])
                                   )
                elif data['status'] == 'error':
                    errorNum += 1
                    logger.info(str(index) +
                                ' Error token: ' +
                                str(data['課程代號'])
                                )

            logger.info('open exist jsonFile. success: {0}, fail: {1}, error:{2}'.format(
                successNum, failNum, errorNum))

    """
    compare spiderDatas and csvDatas and store into the result json file
    """
    result = list()
    with open('{0}-result.json'.format(fileName), mode='w', encoding='utf-8') as resultFile:
        for index, data in enumerate(spiderDatas):
            if data['status'] == 'fail' or data['status'] == 'error':
                data['課程名稱'] = csvDatas[index][2]
                data['CourseName'] = csvDatas[index][3]
                data['修別'] = csvDatas[index][10]
                data['學分數'] = csvDatas[index][1]
                data['選課人數'] = -1  # CSV沒有這個資料
                data['開課單位'] = csvDatas[index][6]
                data['授課老師'] = csvDatas[index][4]
                data['先修科目'] = '無'
                data['上課時間'] = csvDatas[index][7]
                data['Course Department'] = 'none'  # CSV沒有這個資料
                data['Instructor'] = csvDatas[index][5]
                data['Prerequisite'] = 'none'  # CSV沒有這個資料
                data['Session'] = 'none'  # CSV沒有這個資料
                data['課程簡介'] = '無課程簡介'

            data['開課單位'] = data['開課單位'].split('、')
            data['授課老師'] = data['授課老師'].split('、')
            data['上課時間'] = time_converter(data['上課時間'])
            result.append(data)

        json.dump(result, resultFile)
