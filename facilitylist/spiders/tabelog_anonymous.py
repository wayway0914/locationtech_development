from scrapy.spiders import CrawlSpider, Rule
import scrapy
from scrapy.linkextractors import LinkExtractor
from s3pipeline import Page
import re
from bs4 import BeautifulSoup as bs4
import lxml
import requests
from time import sleep

class StorelistSpider(CrawlSpider):
	# Naming Rule: "scrapingcompanyname_brandname"
	name = "tabelog_anonymous"

	# should set not to go outside from target URL
	allowed_domains = ["tabelog.com"]
	tabelog_targetCategory = ""
	tabelog_prefectureName = ""
	tabelog_categoryCount = 0
	tabelog_prefectureCount = 0
	tabelog_cityCount = 0
	tabelog_pageCount = 1

	def start_requests(self):
		#SKIP-SETTINGS: Starting Position
		nStartCategory = 107
		nStartPrefecture = 34
		nStartCity = 3
		nStartPage = 4

		#Target Category
		with open('tabelogCategoryList.txt') as f1:
			self.tabelog_categoryCount = 0
			for q1 in f1:
				self.tabelog_categoryCount += 1

				#SKIP-CONDITIONS
				if self.tabelog_categoryCount < nStartCategory:
					continue
				else:
					pass

				self.tabelog_targetCategory = q1

				#Target Prefecture
				with open('prefectureList.txt') as f2:
					self.tabelog_prefectureCount = 0
					for q2 in f2:
						self.tabelog_prefectureCount += 1

						#SKIP-CONDITIONS
						if self.tabelog_prefectureCount < nStartPrefecture:
							continue
						else:
							pass

						self.tabelog_prefectureName = q2
						url_cp = 'https://tabelog.com/'+ q2.strip() + '/rstLst/' + q1.strip()

						#Store city-wide urls in list
						html_cp = requests.get(url_cp)
						soup_cp = bs4(html_cp.text, "lxml")
						cityListWrapper = soup_cp.select_one("#tabs-panel-balloon-pref-area")

						#initialize cityList
						url_cpcList = []
						url_cpcList = cityListWrapper.select("li.list-balloon__list-item > a.c-link-arrow")

						self.tabelog_cityCount = 0
						for url_cpc in url_cpcList:
							self.tabelog_cityCount += 1

							#SKIP-CONDITIONS
							if self.tabelog_cityCount < nStartCity:
								continue
							else:
								pass

							html_cpc = requests.get(url_cpc.get("href"))
							soup_cpc = bs4(html_cpc.text, "lxml")

							#Calculate maximum page
							storeCountWrapper = soup_cpc.select_one("div.c-page-count")
							storeCount = int(storeCountWrapper.select("span.c-page-count__num")[2].text)
							maxPage = min(60, (storeCount - 1)//20 + 1)

							self.tabelog_pageCount = 0							
							#go to each page
							for i in range(1, maxPage + 1):
								self.tabelog_pageCount += 1

								#SKIP-CONDITIONS
								if self.tabelog_pageCount < nStartPage:
									continue
								else:
									pass	

								url_cpcp = url_cpc.get("href") + str(i)

								#Get urls for each facilities
								html_cpcp = requests.get(url_cpcp)
								soup_cpcp = bs4(html_cpcp.text, "lxml")

								url_facilities = []
								facilitiesInfoWrapper = soup_cpcp.select_one("div.js-rstlist-info")
								facilityURLWrappers = facilitiesInfoWrapper.select("a.cpy-rst-name")

								for facilityURLWrapper in facilityURLWrappers:
									url_facilities.append(facilityURLWrapper.attrs["href"])

								for url_facility in url_facilities:
									yield scrapy.Request(url_facility, callback=self.page_parse)

							nStartPage = 0
						nStartCity = 0
				nStartPrefecture = 0

	def page_parse(self, response):
		scrapingLog = "Scraping: " + "Category #" + str(self.tabelog_categoryCount) + " " + self.tabelog_targetCategory.strip() + " -- Prefecture #" + str(self.tabelog_prefectureCount) + " " + self.tabelog_prefectureName.strip() + " -- city #" + str(self.tabelog_cityCount) + " -- page #" + str(self.tabelog_pageCount)
		print(scrapingLog)
		yield Page.from_response(response)