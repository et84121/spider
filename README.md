爬蟲
===

## 用途
從課程大綱網站爬出課程資料，進而比對原有之靜態課程資料，順便另存資料為json格式，方便後續匯入資料庫。

## 相依性
`pip install BeautifulSoup4 Requests`

## 功能

- 從教學大綱抓取資料(spider.py 模組)  
    - 三種狀態 (成功、資料不存在、其它錯誤ex.TimeOut) 
- 將spider爬回的資料先存成json檔，加速後續資料操作.
- 實作log功能可有效知道爬取狀態
- 與csv資料互相比較取優值
- 上課時間、開課單位、老師等欄位分割為列表

## 結果格式 飯粒
![](https://i.imgur.com/1pUkzIa.png)

### FireCat跟carterchou是同一個人