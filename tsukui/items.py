import scrapy

class TsukuiItem(scrapy.Item):
	facilityName = scrapy.Field()
	facilityAddress = scrapy.Field()
	facilityServices = scrapy.Field()
