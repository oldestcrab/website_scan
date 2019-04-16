import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from website_scan.items import GenecopoeiaaScanItem
from website_scan.settings import IGNORE_URL

class GenecopoeiaaScanSpider(CrawlSpider):
    name = 'genecopoeiaa_scan'
    allowed_domains = ['www.genecopoeia.com']
    start_urls = ['https://www.genecopoeia.com']
    url_deny =  '|'.join(IGNORE_URL)
    page_pattern = LinkExtractor(allow=(), deny=(url_deny), allow_domains=('www.genecopoeia.com'))
    rules = [
        Rule(page_pattern, callback='parse_url', follow=True)
    ]

    def parse_url(self, response):
        # print(response.request.url)
        # print(response.url)
        # print(response.status)
        # print('=============')
        item = GenecopoeiaaScanItem()
        item['url'] = response.url
        item['code'] = response.status
        item['response_url'] = response.request.url

        yield item