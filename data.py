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

"""


def store(token, index, csv_spider):
    result = dict()

    if csv_spider is True:
        result['課程代號'] = token
        result['課程名稱'] = csvDatas[index][2]
        result['CourseName'] = csvDatas[index][3]
        result['修別'] = csvDatas[index][10]
        result['學分數'] = csvDatas[index][1]
        result['選課人數'] = -1  # CSV沒有這個資料
        result['開課單位'] = csvDatas[index][6]
        result['授課老師'] = csvDatas[index][4]
        result['先修科目'] = '無'
        result['上課時間'] = [{'day': csvDatas[index][7][0], '節':csvDatas[index][7][1]}, {
            'day': csvDatas[index][7][0], '節':csvDatas[index][7][-1]}]
        result['Course Department'] = 'none'  # CSV沒有這個資料
        result['Instructor'] = csvDatas[index][5]
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

    header, *csvDatas = csv.reader(csvfile)
    # csv 讀檔

    print(header)
    print(csvDatas[1])

    """
    get spiderDatas
    """
    spiderDatas = list()  # for store datas from spider

    if (not os.path.isfile('{0}.json'.format(fileName))) or (os.path.getsize('{0}.json'.format(fileName)) == 0):
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
                # if status is true means spider have geted the data from web
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

            logger.info('success: {0}, fail: {1}, error:{2}'.format(
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
                elif data['status'] == 'fail':
                    failNum += 1
                elif data['status'] == 'error':
                    errorNum += 1

            logger.info('open exist jsonFile.success: {0}, fail: {1}, error:{2}'.format(
                successNum, failNum, errorNum))
