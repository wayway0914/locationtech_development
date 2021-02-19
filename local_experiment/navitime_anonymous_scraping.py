import re
from bs4 import BeautifulSoup as bs4
import lxml.html

COMPANY_NAME = "Navitime"
BRAND_NAME = "Anonymous"
XYFlag = False

#--------------------------------------------------
import requests
page = requests.get("https://www.navitime.co.jp/category/0101/").text
#--------------------------------------------------

# def scrape_from_page(page):
# prepare for lists
facilityNameList = []
facilityAddressList = []
latitudeList= []
longitudeList = []
category1List = []
category2List = []
category3List = []
priceRangeList = []
googleMapScoreList = []
tabelogScoreList = []
nTablesList = []
facilitySizeList = []
openHourList = []
openDateList = []
closeDateList = []
URLList = []

html = bs4(page, "lxml")

Wrapper = html.find("div", id="spot-list")
facilityContainers = Wrapper.find_all("div", class_="spot-text")

for facilityContainer in facilityContainers:
    #facility name
    facilityName = facilityContainer.find("dt", class_="spot-name").get_text().replace("\n","").replace(" ","").replace("\t","") 

    #facility address
    facilityInfoTable = facilityContainer.find("dl", class_="spot-detail-section")
    facilityInfoTableKeys = [t.get_text().replace("\n","").replace(" ","") for t in facilityInfoTable.find_all("dt")]
    facilityInfoTableValues = [t.get_text().replace("\n","").replace(" ","") for t in facilityInfoTable.find_all("dd")]
    idx_facilityAddress = facilityInfoTableKeys.index("住所")
    facilityAddress = facilityInfoTableValues[idx_facilityAddress].replace("\n","").replace(" ","").replace("\t","") 

    #Category1
    categoryLocator = html.find("ul", id="breadcrumb")
    categoryDepth = len(categoryLocator.find_all("li"))
    category1 = categoryLocator.find_all("li")[categoryDepth - 1].text.replace("＞","").replace(" ","").replace("  ","")
    category1List.append(category1)

    #other no data categories
    nTablesList.append("-")
    facilitySizeList.append("-")
    URLList.append("-")
    openDateList.append("-")
    closeDateList.append("-")
    googleMapScoreList.append("-")
    tabelogScoreList.append("-")
    category2List.append("-")
    category3List.append("-")
    priceRangeList.append("-")

    #store in the list
    facilityNameList.append(facilityName)
    facilityAddressList.append(facilityAddress)

print(XYFlag, COMPANY_NAME, BRAND_NAME, facilityNameList, facilityAddressList, latitudeList, longitudeList, category1List, category2List, category3List, priceRangeList, nTablesList, facilitySizeList, googleMapScoreList, tabelogScoreList, openHourList, openDateList, closeDateList, URLList)
# geocoding.geocoding(XYFlag, COMPANY_NAME, BRAND_NAME, facilityNameList, facilityAddressList, latitudeList, longitudeList, category1List, category2List, category3List, priceRangeList, nTablesList, facilitySizeList, googleMapScoreList, tabelogScoreList, openHourList, openDateList, closeDateList, URLList)