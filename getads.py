import scrapy
from scrapy import Request

class GetcatSpider(scrapy.Spider):
    name = 'getcat'
    allowed_domains = ['seattle.craigslist.org/search/est/cta']
    start_urls = ['http://seattle.craigslist.org/search/est/cta/']

    def parse(self, response):
        vehicles= response.xpath('//div[@class="result-info"]')

        for vehicle in vehicles:
            title= vehicle.xpath('h3/a/text()').extract_first()
            price= vehicle.xpath('span/span[@class="result-price"]/text()').extract_first()
            neigh= vehicle.xpath('span/span[@class="result-hood"]/text()').extract_first().strip()[1:-1]
            URL= vehicle.xpath('h3/a/@href').extract_first()

            yield Request(URL, callback=self.parse_page, dont_filter=True,
                meta={'Title': title,'Price': price,'Neighborhood': neigh, "URL":URL})

        rel_next_url= response.xpath('//a[@class="button next"]/@href').extract_first()
        abs_next_url= response.urljoin(rel_next_url)
        yield Request(abs_next_url, callback=self.parse, dont_filter=True)

    def parse_page(self, response):
        title=response.meta.get('Title')
        price=response.meta.get('Price')
        neigh=response.meta.get('Neighborhood')
        URL= response.meta.get('URL')
        desc= response.xpath('//meta[@name="description"]/@content').extract_first()

        yield{'Title': title,'Price': price,'Neighborhood': neigh, "URL":URL,"Description": desc}