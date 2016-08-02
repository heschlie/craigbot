import scrapy
from craigbot.items import CraigslistSampleItem


class MySpider(scrapy.Spider):
    name = 'craig'
    allowed_domains = ['craigslist.org']
    start_urls = ['http://sfbay.craigslist.org/search/pta?query=subaru+sti']

    def parse(self, response):

        self.parse_posts(response)

        next_button = response.xpath('//a[@class="button next"]')[0]
        if next_button:
            url = response.urljoin(next_button.xpath('@href').extract()[0])
            yield scrapy.Request(url, callback=self.parse_posts)


    def parse_posts(self, response):
        posts = response.xpath('//span[@class="pl"]')
        for post in posts:
            print(post)
            item = CraigslistSampleItem()
            item['title'] = post.xpath('a/span[@id="titletextonly"]/text()').extract()[0]
            link = post.xpath('a/@href').extract()[0]
            item['link'] = response.urljoin(link)
            yield item
