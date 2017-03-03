import scrapy

class IMDBSpider(scrapy.Spider):
	name = "imdb"

	def start_requests(self):
		urls = [
			'http://www.imdb.com/list/ls058011111/?start=1&view=compact&sort=listorian:asc'
		]
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		names = []
		trs_odd = response.xpath("//tr[@class='list_item compact odd']")
		trs_even = response.xpath("//tr[@class='list_item compact even']")
		for tr in trs_odd:
			names.append(u' '.join(tr.xpath("./td[2]/a/text()").extract()).encode('utf-8').strip())
		for tr in trs_even:
			names.append(u' '.join(tr.xpath("./td[2]/a/text()").extract()).encode('utf-8').strip())
		next_page = response.xpath("//div[@class='pagination']/a")
		f = open ("people_name.txt", "a")
		for name in names:
			f.write(name + "\n")
		f.close()
		if (next_page is not None) and (len(next_page) == 1):
			next_page = next_page[0].xpath("./@href").extract()
			yield scrapy.Request(response.urljoin(next_page[0]), callback=self.parse)
		if (next_page is not None) and (len(next_page) == 2):
			next_page =  next_page[1].xpath("./@href").extract()
			yield scrapy.Request(response.urljoin(next_page[0]), callback=self.parse)