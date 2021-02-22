import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from s3pipeline import Page
import re

class FacilitylistSpider(CrawlSpider):
	#Naming Rule: "scrapingcompanyname_brandname"
	name = "navitime_anonymous"

	#Allowd Domains: should be set so as not to go outside target company/brand
	allowed_domains = ["navitime.co.jp"]

	#start_urls can be either list or tuple with ",", and it can be multiple
	start_urls=("https://www.navitime.co.jp/category/",)

	#rules to follow links:
	rules = (
		Rule(LinkExtractor(
			allow=r"\w+/category/\w+/$",
			restrict_xpaths = "//*[@id='left_pane']",
			unique = True,)),
		Rule(LinkExtractor(
			allow=r"\w+/category/\w+/\?page=\d*$",
			restrict_xpaths = "//*[@id='left_pane']/ul[1]",
			unique = True,
		), callback="page_parse", follow = True),
	)

	def page_parse(self, response):
		yield Page.from_response(response)