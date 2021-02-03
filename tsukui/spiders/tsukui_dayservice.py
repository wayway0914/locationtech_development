import scrapy
from s3pipeline import Page
from bs4 import BeautifulSoup as bs

class AddressSpider(scrapy.Spider):
	#Naming Rule: "companyname_burandname"
	name = "tsukui_dayservice"

	#Allowd Domains: should be set so as not to go outside target company/brand
	allowed_domains = ["tsukui.net"]

	#start_urls can be either list or tuple, and also can be multiple
	start_urls=("https://www.tsukui.net/search/list/?i_division=2&page=1&i_service=22",)

	def parse(self, response):
		yield Page.from_response(response)

		# next_page = response.css("li.btnnext a::attr(href)").get()
		# if next_page is not None:
		# 	yield response.follow(next_page, callback = self.parse)