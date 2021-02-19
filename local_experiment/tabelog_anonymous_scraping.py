import re
from bs4 import BeautifulSoup as bs4
import lxml.html

#Web-Scraping
COMPANY_NAME = "Tabelog"
BRAND_NAME = "Anonymous"
XYFlag = True

#--------------------------------------------------
import requests
page = requests.get("https://tabelog.com/tokyo/A1308/A130801/13002751/").text
#--------------------------------------------------

# def scrape_from_page(page):
#prepare for lists
facilityNameList = []
facilityAddressList = []
latitudeList= []
longitudeList = []
category1List = []
category2List = []
category3List = []
priceRangeList = []
googleMapScoreList = []
nGoogleMapQuotesList = []
tabelogScoreList = []
nTabelogQuotesList = []
nTabelogSavesList = []
nTablesList = []
facilitySizeList = []
openHourList = []
openDateList = []
closeDateList = []
URLList = []

html = bs4(page,"lxml")

try:
    evaluationContainer = html.find("div", id="js-header-rating")

    try:
        tabelogScore = evaluationContainer.find("div", id="js-detail-score-open").get_text().strip()
        tabelogScoreList.append(tabelogScore)
    except ValueError:
        tabelogScore = "unknown"
        tabelogScoreList.append(tabelogScore)

    try:
        nTabelogQuotes = evaluationContainer.find("span", class_="rdheader-rating__review").find("em").get_text().strip()
        nTabelogQuotesList.append(nTabelogQuotes)
    except ValueError:
        nTabelogQuotes = "uknown"
        nTabelogQuotesList.append(nTabelogQuotes)

    try:
        nTabelogSaves = evaluationContainer.find("span", class_="rdheader-rating__hozon-target").find("em").get_text().strip()
        nTabelogSavesList.append(nTabelogSaves)
    except ValueError:
        nTabelogSaves = "unknown"
        nTabelogSavesList.append(nTabelogSaves)

except ValueError:
    tabelogScoreList.append("unknown")
    nTabelogQuotesList.append("unknown")
    nTabelogSavesList.append("unknown")

try:
    mapInfo = html.find("img", class_="js-map-lazyload")['data-original']
    latitude = re.search(r"markers.*?%7C\d+\.\d+,",mapInfo).group().replace(r"markers=color:red%7C","").replace(",","")
    latitudeList.append(latitude)
    longitude = re.search(r"markers.*?%7C\d+\.\d+,\d+\.\d+&",mapInfo).group().replace(r"markers=color:red%7C","").replace(latitude,"").replace("&","").replace(",","")
    longitudeList.append(longitude)
except ValueError:
    latitude = "unknown"
    latitudeList.append(latitude)
    longitude = "unknown"
    longitudeList.append(longitude)

try:
    #Getting InfoTable
    storeInfoContainer = html.find("div", id="rst-data-head")
    storeInfoKeys = [t.get_text().replace("\n","").replace(" ","") for t in storeInfoContainer.find_all("th")]
    storeInfoValues = [t.get_text().replace("\n","").replace(" ","") for t in storeInfoContainer.find_all("td")]

    try:
        idx_category2 = storeInfoKeys.index("ジャンル")
        category2 = storeInfoValues[idx_category2]
        category2List.append(category2)
    except ValueError:
        category2 = "unknown"
        category2List.append(category2)

    try:
        idx_openHour = storeInfoKeys.index("営業時間・定休日")
        openHour = storeInfoValues[idx_openHour]
        openHourList.append(openHour)
    except ValueError:
        openHour = "unknown"
        openHourList.append(openHour)
    
    try:
        idx_priceRange = storeInfoKeys.index("予算")
        priceRange = storeInfoValues[idx_priceRange]
        priceRangeList.append(priceRange)
    except ValueError:        
        try:
            idx_priceRange = storeInfoKeys.index("予算（口コミ集計）")
            priceRange = storeInfoValues[idx_priceRange]
            priceRangeList.append(priceRange)
        except ValueError:
            priceRange = "unknown"
            priceRangeList.append(priceRange)

    try:
        idx_facilityName = storeInfoKeys.index("店名")
        facilityName = storeInfoValues[idx_facilityName]
        facilityNameList.append(facilityName)
    except ValueError:
        facilityName = "unknown"
        facilityNameList.append(facilityName)

    try:
        idx_facilityAddress = storeInfoKeys.index("住所")
        facilityAddress = re.sub("大きな地図を見る.*","",storeInfoValues[idx_facilityAddress])
        facilityAddressList.append(facilityAddress)
    except ValueError:
        facilityAddress = "unknown"
        facilityAddressList.append(facilityAddress)

    try:
        idx_nofTable = storeInfoKeys.index("席数")
        nTables = storeInfoValues[idx_nofTable]
        nTablesList.append(nTables)
    except ValueError:
        nTables = "unknown"
        nTablesList.append(nTables)

    try:
        idx_openDate = storeInfoKeys.index("オープン日")
        openDate = storeInfoValues[idx_openDate]
        openDateList.append(openDate)
    except ValueError:
        openDate = "unknown"
        openDateList.append(openDate)

    try:
        idx_URL = storeInfoKeys.index("ホームページ")
        URL = storeInfoValues[idx_URL]
        URLList.append(URL)
    except ValueError:
        URL = "unknown"
        URLList.append(URL)
    
    # other no data categories
    facilitySizeList.append("-")
    closeDateList.append("-")
    googleMapScoreList.append("-")
    nGoogleMapQuotesList.append("-")
    category1List.append("food")
    category3List.append("-")
    
except AttributeError:
    pass

# geocoding.geocoding(XYFlag, COMPANY_NAME, BRAND_NAME, facilityNameList, facilityAddressList, latitudeList, longitudeList, category1List, category2List, category3List, priceRangeList, nTablesList, facilitySizeList, googleMapScoreList, nGoogleMapQuotesList, tabelogScoreList, nTabelogQuotesList, nTabelogSavesList, openHourList, openDateList, closeDateList, URLList)
print(XYFlag, COMPANY_NAME, BRAND_NAME, facilityNameList, facilityAddressList, latitudeList, longitudeList, category1List, category2List, category3List, priceRangeList, nTablesList, facilitySizeList, googleMapScoreList, nGoogleMapQuotesList, tabelogScoreList, nTabelogQuotesList, nTabelogSavesList, openHourList, openDateList, closeDateList, URLList)