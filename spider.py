from bs4 import BeautifulSoup
import requests

def get_course(token,school_year=106,semester=2):
    """
    Course data will be returned with a dict. 
    """
    num = str(token)[0:6]
    s = str(token)[8:9]
    gop = str(token)[6:8]

    res = requests.get('http://newdoc.nccu.edu.tw/teaschm/1062/schmPrv.jsp-yy={3}&smt={4}&num={0}&gop={1}&s={2}.html'.format(num,gop,s,school_year,semester))
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'lxml')
    
    try:
        result = dict()

        result['課程代號'] = token
        result['課程名稱'] = soup.find(id='CourseName').get_text().rstrip()
        result['CourseName'] = soup.find(id='CourseNameEn').get_text().rstrip()
        result['修別'] = soup.h4.get_text()[3].rstrip()
        result['學分數'] = int( (soup.find_all('i','sylview-icontext sylview-icontextB'))[0].get_text()[0] )
        result['選課人數'] = int( (soup.find_all('i','sylview-icontext sylview-icontextB'))[1].get_text() )
        
        li = soup.find('ul','nav nav-divider').find_all('span','Zh')
        result['開課單位'] = li[0].get_text()[5:].rstrip()
        result['授課老師'] = li[1].get_text()[5:].rstrip()
        result['先修科目'] = li[2].get_text()[5:].rstrip()
        result['上課時間'] = li[3].get_text()[5:].rstrip()
        # Python rstrip() 删除 string 字符串末尾的指定字符（默认为空格）.

        li = soup.find('ul','nav nav-divider').find_all('span','En')
        result['Course Department'] = li[0].get_text()[18:].rstrip()
        result['Instructor']        = li[1].get_text()[11:].rstrip()
        result['Prerequisite']      = li[2].get_text()[13:-1].rstrip()
        result['Session']           = li[3].get_text()[8:].rstrip()

        result['課程簡介'] = soup.find('div','col-sm-7 sylview--mtop col-p-6').p.get_text().rstrip()

        return True,result
    except Exception as e:
        """
            ex URL:http://newdoc.nccu.edu.tw/teaschm/1062/schmPrv.jsp-yy=106&smt=2&num=000219&gop=55&s=2.html
            經濟學 000219552 cann't find
        """
        if soup.body.h1.get_text() == '找不到網頁':
            print('\n!!! Could not find course: {0}!!!\n'.format(token))
            print(str(e)+'\n')
            return False

    
# token = 300820001

if __name__ == '__main__':
    print(get_course(token='000219552')[1].values())
    
"""
課程名稱:大數據分析實務
CourseName:Big Data Analysis
修別：選
學分數:3
選課人數:13
開課單位：商院碩士
授課老師：白佩玉、黃秉德、蔡瑞煌、鄭宗記
先修科目：
上課時間：四EFG
Course Department:Selective courses of master level,College of Commerce
Instructor:
Prerequisite()
Session: thu18-21
課程簡介:本課由企管系、資管系、統計系三系教師共同規劃，期能協助商院同學能熟悉大數據相關理論與分析工具，透過實際案例之演練，建立大數據分析能力，以解決企業問題。
"""


"""
Note

http://wa.nccu.edu.tw/QryTor/courseSyllabus.aspx?view=614f626a744857696b624e702f7a78333230664f42413d3d
2018/5/3 08:49

test upper link if its token would out of data
"""