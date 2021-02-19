import scrapy

class facilitylist(scrapy.Item):
	facilityName = scrapy.Field()
	facilityAddress = scrapy.Field()
	facilityServices = scrapy.Field()
