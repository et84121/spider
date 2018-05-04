import csv,json,spider
"""
import data from csv ,compare data from spider, save them into json. 

To-DO:
- [ ] make a teacher list
- [ ] make a department list
- [ ] join and compare data from csv and spider 

"""
fileName = '1061-course'
jsonfile = open('{0}.json'.format(fileName),mode='w',encoding='utf-8')
csvfile = open('1061.csv',mode='r',encoding='utf-8')

header, *datas = csv.reader(csvfile)

print(header)
print(datas[0])

tokenList = list()

spider_datas = list()
for index, token in enumerate((data[0] for data in datas)): 
# 取出全部的課程代號進行迭代
    spider_datas.append(spider.get_course(token))
    try:
        print(spider_datas[index]['課程名稱']+ " " + token)
    except Exception as e:
        print(str(e))