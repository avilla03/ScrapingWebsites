import scrapy
from datetime import datetime

class QuotecrawlerSpider(scrapy.Spider):
    name = "quoteCrawler"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]
    
    # Lets extract the quote itself, the speaker, the tags,
    # when they were born (parsed as 8 numbers), country, and description
    def parse_about_page(self, response):
        country = response.xpath('//span[@class="author-born-location"]/text()').get()
        country_arr = country.split(',')
        country = country_arr[-1][1:]
        description = response.xpath('//div[@class="author-description"]/text()').get()
        quote_data = response.meta['quote_data']
        combined_data = {
            **quote_data,
            'birth_country': country,
            'description': description
        }
        yield combined_data
    def parse(self, response):
        quote_info = response.css('div.quote')
        for block in quote_info:
            quote_data = {
                'quote': block.css('span.text::text').get(),
                'tags': block.css('div.tags a::text').getall(),
                'author': block.css('span small.author::text').get()
            }
            about_page = block.css('span a::attr(href)').get()
            if about_page:
                yield response.follow(about_page, callback=self.parse_about_page, meta={'quote_data': quote_data}, dont_filter=True)
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse, dont_filter=True)