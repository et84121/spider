爬蟲
===

## 用途
從課程大綱網站爬出課程資料，進而比對原有之靜態課程資料，順便另存資料為json格式，方便後續匯入資料庫。

## 相依性
`pip install BeautifulSoup4 Requests`


CSV備註
===
## 缺少的資料 :
1. 選課人數
2. 英文的系所
3. 先修科目
4. 年級
5. 課程簡介


csv_store(課程代號 , 0為從CSV取值、1為從爬蟲中取值 )
===
## 會回傳一個字典回來 
課程代號、課程名稱、CourseName、修別、學分數、選課人數

開課單位、授課老師、先修科目、上課時間[{day:節}{day:節}]

Course Department、Instructor、Prerequisite、 Session、課程簡介
