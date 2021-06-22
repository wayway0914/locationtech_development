import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from s3pipeline import Page
import re
from bs4 import BeautifulSoup as bs4
import lxml
import requests
from time import sleep

class FacilitylistSpider(CrawlSpider):
	#Naming Rule: "scrapingcompanyname_brandname"
	name = "navitime_anonymous"

	#Allowd Domains: should be set so as not to go outside target company/brand
	allowed_domains = ["navitime.co.jp"]
	navitime_categoryCount = 0
	navitime_prefectureCount = 0
	navitime_cityCount = 0
	navitime_townCount = 0
	navitime_pageCount = 1

	def start_requests(self):
		#SKIP-SETTINGS : Starting Position
		nStartCategory = 230
		nLastCategory = 321
		nStartPrefecture = 46
		nStartCity = 0
		nStartTown = 0
		nStartPage = 0

		with open("navitimeCategoryList.txt") as f:
			self.navitime_categoryCount = 0
			for q in f.readlines()[0:nLastCategory]:
				self.navitime_categoryCount += 1
				self.navitime_prefectureCount = 0
				self.navitime_cityCount = 0
				self.navitime_townCount = 0

				#SKIP-CONDITIONS
				if self.navitime_categoryCount < nStartCategory:
					continue
				else:
					pass

				url_c= "https://www.navitime.co.jp/category/" + str(q).strip()
				html_c = requests.get(url_c)
				soup_c = bs4(html_c.text, "lxml")

				#Scrape prefectures:
				try:
					prefectureWrapperContent = soup_c.select_one("ul.address-list")
					urlList_cpObject = prefectureWrapperContent.select("a[href]")
				except AttributeError:
					continue

				for url_cpObject in urlList_cpObject:
					self.navitime_prefectureCount += 1
					self.navitime_cityCount = 0
					self.navitime_townCount = 0
					#SKIP-CONDITIONS
					if self.navitime_prefectureCount < nStartPrefecture:
						continue
					else:
						pass

					url_cp = url_cpObject.get("href")
					itemCount_cp = re.search(r"\d+",url_cpObject.text).group()

					#less than 50 pages
					if int(itemCount_cp) <= 15*50:
						print("Crawling Prefecture-wise Pages", url_cpObject.text.strip())
						# self.paging(url_cp)
						#Repeat until nextPageButton dissapear
						self.navitime_pageCount = 1
						while True:
							html = requests.get(url_cp)
							soup = bs4(html.text, "lxml")
							nextPageButton = soup.select_one("span.next")

							#each detail pages
							url_detailObjectList = soup.select("li.spot-section")
							for url_detailObject in url_detailObjectList:
								data_provid = url_detailObject.get("data-provid")
								data_spotid = url_detailObject.get("data-spotid")
								url_detail = "https://www.navitime.co.jp/poi?spot=" + str(data_provid) + "-" + str(data_spotid) + "&ncm=1"
								yield scrapy.Request(url_detail, callback = self.page_parse)

							if nextPageButton is not None:
								self.navitime_pageCount += 1
								url_cp = url_cpObject.get("href") + "?page=" + str(self.navitime_pageCount)
							else:
								break

					#more than 50 pages
					else:
						#Scrape cities:
						html_cp = requests.get(url_cp)
						soup_cp = bs4(html_cp.text, "lxml")

						try:
							cityWrapperContent = soup_cp.select_one("ul.address-list")
							urlList_cpcObject = cityWrapperContent.select("a[href]")
						except AttributeError:
							continue

						for url_cpcObject in urlList_cpcObject:
							self.navitime_cityCount += 1
							self.navitime_townCount = 0

							#SKIP-CONDITIONS
							if self.navitime_cityCount < nStartCity:
								continue
							else:
								pass

							url_cpc = url_cpcObject.get("href")
							itemCount_cpc = re.search(r"\d+",url_cpcObject.text).group()

							#less than 50 pages
							if int(itemCount_cpc) <= 15*50:
								print("Crawling City-wise Pages", url_cpcObject.text.strip())
								# self.paging(url_cpc)
								#Repeat until nextPageButton dissapear
								self.navitime_pageCount = 1
								while True:
									html = requests.get(url_cpc)
									soup = bs4(html.text, "lxml")
									nextPageButton = soup.select_one("span.next")

									#each detail pages
									url_detailObjectList = soup.select("li.spot-section")
									for url_detailObject in url_detailObjectList:
										data_provid = url_detailObject.get("data-provid")
										data_spotid = url_detailObject.get("data-spotid")
										url_detail = "https://www.navitime.co.jp/poi?spot=" + str(data_provid) + "-" + str(data_spotid) + "&ncm=1"
										yield scrapy.Request(url_detail, callback = self.page_parse)

									if nextPageButton is not None:
										self.navitime_pageCount += 1
										url_cpc = url_cpcObject.get("href") + "?page=" + str(self.navitime_pageCount)
									else:
										break

							#more than 50 pages
							else:
								#Scrape towns:
								html_cpc = requests.get(url_cpc)
								soup_cpc = bs4(html_cpc.text, "lxml")

								try:
									townWrapperContent = soup_cp.select_one("ul.address-list")
									urlList_cpctObject = townWrapperContent.select("a[href]")
								except AttributeError:
									continue

								for url_cpctObject in urlList_cpctObject:
									self.navitime_townCount += 1

									#SKIP-CONDITION
									if self.navitime_townCount < nStartTown:
										continue
									else:
										pass

									url_cpct = url_cpctObject.get("href")
									# self.paging(url_cpct)
									#Repeat until nextPageButton dissapear
									print("Crawling Town-wise Pages", url_cpctObject.text.strip())
									self.navitime_pageCount = 1
									while True:
										html = requests.get(url_cpct)
										soup = bs4(html.text, "lxml")
										nextPageButton = soup.select_one("span.next")

										#each detail pages
										url_detailObjectList = soup.select("li.spot-section")
										for url_detailObject in url_detailObjectList:
											data_provid = url_detailObject.get("data-provid")
											data_spotid = url_detailObject.get("data-spotid")
											url_detail = "https://www.navitime.co.jp/poi?spot=" + str(data_provid) + "-" + str(data_spotid) + "&ncm=1"
											yield scrapy.Request(url_detail, callback = self.page_parse)

										if nextPageButton is not None:
											self.navitime_pageCount += 1
											url_cpct = url_cpctObject.get("href") + "?page=" + str(self.navitime_pageCount)
										else:
											break

							nStartTown = 1
					nStartCity = 1
				nStartPrefecture = 1		

	# def paging(self, url):
	# 	#Repeat until nextPageButton dissapear
	# 	while True:
	# 		html = requests.get(url)
	# 		soup = bs4(html.text, "lxml")
	# 		nextPageButton = soup.select_one("span.next")

	# 		#each detail pages
	# 		url_detailObjectList = soup.select("a.spot-link-text[href]")
	# 		for url_detailObject in url_detailObjectList:
	# 			url_detail = url_detailObject.get("href")

	# 			if url_detailObject.text == "詳細を見る":
	# 				yield scrapy.Request(url_detail, callback = self.page_parse)
	# 				sleep(5)
	# 			else:
	# 				pass

	# 		if nextPageButton is not None:
	# 			self.navitime_pageCount += 1
	# 			url = url_cpObject.get("href") + "?page=" + str(self.navitime_pageCount)
	# 		else:
	# 			break

	def page_parse(self, response):
		scrapingLog = "Scraping: categoryCount :" + str(self.navitime_categoryCount).strip() + " -- prefectureCount: " + str(self.navitime_prefectureCount).strip() + " -- cityCount: " + str(self.navitime_cityCount).strip() + " -- townCount: " + str(self.navitime_townCount).strip() + " -- page " + str(self.navitime_pageCount).strip()
		print(scrapingLog)
		yield Page.from_response(response)