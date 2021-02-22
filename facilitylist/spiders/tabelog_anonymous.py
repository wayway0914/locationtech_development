from scrapy.spiders import CrawlSpider, Rule
import scrapy
from scrapy.linkextractors import LinkExtractor
from s3pipeline import Page
import re
from bs4 import BeautifulSoup as bs4
import lxml
import requests
from time import sleep

# class StorelistSpider(CrawlSpider):
# 	#Naming Rule: "scrapingcompanyname_brandname"
# 	name = "tabelog_anonymous"

# 	#Allowd Domains: should be set so as not to go outside target company/brand
# 	allowed_domains = ["tabelog.com"]
# 	start_urls = []

# 	#Target Category
# 	with open('tabelogCategoryList.txt') as f2:
# 		for q2 in f2:
# 			with open('prefectureList.txt') as f1:
# 				for q1 in f1:
# 					#start_urls can be either list or tuple with ",", and it can be multiple
# 					start_urls.append("https://tabelog.com/" + q1 + "/" + "rstLst/" + q2 + "/")

# 	#rules to follow links:
# 	rules = (
# 		#follow area link first, then category link next, check list pages and go to the details
# 		Rule(LinkExtractor(
# 			allow=r"/\w+/A\d+/rstLst/\w+/$",
# 			restrict_xpaths = "//*[@id='js-leftnavi-area-panels']",
# 			unique = True,)),
# 		Rule(LinkExtractor(
# 			allow=r"/\w+/A\d+/rstLst/\w+/\d+/$",
# 			restrict_xpaths = "//*[@id='container']/div[15]/div[4]/div/div[7]/div/ul",
# 			unique = True,),
# 			follow=True),
# 		Rule(LinkExtractor(
# 			allow=r"/\w+/A\d+/A\d+/\d+/$",
# 			restrict_xpaths = "//*[@id='container']/div[15]/div[4]/div/div[6]",
# 			unique = True,
# 		), callback="page_parse"),
# 	)

# 	def page_parse(self, response):
# 		#Could not know how to save files in corresponding prefecture and category
# 		yield Page.from_response(response)


class StorelistSpider(CrawlSpider):
	# Naming Rule: "scrapingcompanyname_brandname"
	name = "tabelog_anonymous"

	# should set not to go outside from target URL
	allowed_domains = ["tabelog.com"]
	targetCategory = ""
	prefectureName = ""
	cityCount = 0
	page = 0

	def start_requests(self):
		#Target Category
		with open('tabelogCategoryList.txt') as f1:
			for q1 in f1:
				global targetCategory
				targetCategory = q1

				#Target Prefecture
				with open('prefectureList.txt') as f2:
					for q2 in f2:
						global prefectureName
						prefectureName = q2
						url_cp = 'https://tabelog.com/'+ q2.strip() + '/rstLst/' + q1.strip()

						#Store city-wide urls in list
						html_cp = requests.get(url_cp)
						soup_cp = bs4(html_cp.text, "lxml")
						cityListWrapper = soup_cp.select_one("#js-leftnavi-area-panels")

						#initialize cityList
						url_cpcList = []
						url_cpcList = cityListWrapper.select("li.list-balloon__list-item > a.c-link-arrow")

						global cityCount
						cityCount = 0

						for url_cpc in url_cpcList:
							html_cpc = requests.get(url_cpc.get("href"))
							soup_cpc = bs4(html_cpc.text, "lxml")

							#Calculate maximum page
							storeCountWrapper = soup_cpc.select_one("div.c-page-count")
							storeCount = int(storeCountWrapper.select("span.c-page-count__num")[2].text)
							maxPage = min(60, (storeCount - 1)//20 + 1)
							cityCount += 1

							global page
							page = 0
							
							#go to each page
							for i in range(1, maxPage + 1):
								url_cpcp = url_cpc.get("href") + str(i)

								#Get urls for each facilities
								html_cpcp = requests.get(url_cpcp)
								soup_cpcp = bs4(html_cpcp.text, "lxml")

								url_facilities = []
								facilitiesInfoWrapper = soup_cpcp.select_one("div.js-rstlist-info")
								facilityURLWrappers = facilitiesInfoWrapper.select("a.cpy-rst-name")
								page += 1

								for facilityURLWrapper in facilityURLWrappers:
									url_facilities.append(facilityURLWrapper.attrs["href"])

								for url_facility in url_facilities:
									yield scrapy.Request(url_facility, callback=self.page_parse)

	def page_parse(self, response):
		scrapingLog = "Scraping: " + targetCategory.strip() + " -- " + prefectureName.strip() + " -- city#" + str(cityCount).strip() + " -- page " + str(page).strip()
		print(scrapingLog)
		yield Page.from_response(response)