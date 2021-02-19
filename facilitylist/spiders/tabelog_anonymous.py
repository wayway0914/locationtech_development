import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from s3pipeline import Page
import re

class StorelistSpider(CrawlSpider):
	#Naming Rule: "scrapingcompanyname_brandname"
	name = "tabelog_anonymous"

	# #パッチ間で永続的な状態を維持
	# self.logger.info(self.state.get("state_key1"))
	# self.state["state_key1"] = {"key":"value"}
	# self.state["state_key2"] = 0

	#Allowd Domains: should be set so as not to go outside target company/brand
	allowed_domains = ["tabelog.com"]
	start_urls = []

	#Target Category
	with open('tabelogCategoryList.txt') as f2:
		for q2 in f2:
			with open('prefectureList.txt') as f1:
				for q1 in f1:
					#start_urls can be either list or tuple with ",", and it can be multiple
					start_urls.append("https://tabelog.com/" + q1 + "/" + "rstLst/" + q2 + "/")

	#rules to follow links:
	rules = (
		#follow area link first, then category link next, check list pages and go to the details
		Rule(LinkExtractor(
			allow=r"/\w+/A\d+/rstLst/\w+/$",
			restrict_xpaths = "//*[@id='js-leftnavi-area-panels']",
			unique = True,)),
		Rule(LinkExtractor(
			allow=r"/\w+/A\d+/rstLst/\w+/\d+/$",
			restrict_xpaths = "//*[@id='container']/div[15]/div[4]/div/div[7]/div/ul",
			unique = True,),
			follow=True),
		Rule(LinkExtractor(
			allow=r"/\w+/A\d+/A\d+/\d+/$",
			restrict_xpaths = "//*[@id='container']/div[15]/div[4]/div/div[6]",
			unique = True,
		), callback="page_parse"),
	)

	def page_parse(self, response):
		#Could not know how to save files in corresponding prefecture and category
		yield Page.from_response(response)