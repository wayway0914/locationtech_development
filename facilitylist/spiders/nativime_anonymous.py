import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from s3pipeline import Page
import re

class FacilitylistSpider(CrawlSpider):
	#Naming Rule: "scrapingcompanyname_brandname"
	name = "navitime_anonymous"

	# #パッチ間で永続的な状態を維持
	# self.logger.info(self.state.get("state_key1"))
	# self.state["state_key1"] = {"key":"value"}
	# self.state["state_key2"] = 0

	#Allowd Domains: should be set so as not to go outside target company/brand
	allowed_domains = ["navitime.co.jp"]

	#start_urls can be either list or tuple with ",", and it can be multiple
	start_urls=("https://www.navitime.co.jp/category/",)

	#rules to follow links:
	rules = (
		Rule(LinkExtractor(
			allow=r"/\w+category/\w+/$",
			restrict_xpaths = "//*[@id='left_pane']",
			unique = True,
		), callback="page_parse"),
	)

	def page_parse(self, response):
		yield Page.from_response(response)

		# next_page = response.xpath("//*[@id='left_pane']/ul[1]/li[8]").get()
		# if next_page is not None:
		# 	yield response.follow(next_page, callback = self.page_parse)