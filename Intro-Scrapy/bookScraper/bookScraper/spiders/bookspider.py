import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books = response.css('article.product_pod')
        for book in books:
            book_link = book.css('h3 a').attrib['href']
            if 'catalogue' not in book_link:
                book_link = 'https://books.toscrape.com/catalogue/' + book_link
            else:
                book_link = 'https://books.toscrape.com/' + book_link
            yield response.follow(book_link, callback = self.parse_book_link)
            
            
        next_page = response.css('ul.pager li.next a').attrib['href']
        if next_page:
            # some may have '/catalogue/*', while others dont
            if 'catalogue' not in next_page:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/' + next_page
            yield response.follow(next_page_url, callback = self.parse)
    def parse_book_link(self, response):
        yield {
            'book_description' : response.xpath('//div[@id="product_description"]/following-sibling::p/text()').get(),
            'book_category' : response.xpath('//ul[@class="breadcrumb"]/li[3]/a/text()').get(),
            'book_name' : response.css('div.col-sm-6.product_main h1::text').get(),
            'book_price' : response.css('div.col-sm-6.product_main p.price_color::text').get(),
            'book_rating' : response.css('div.col-sm-6.product_main p.star-rating::attr(class)').get(),
            'book_tax' : response.xpath('//table/tr[5]/td/text()').get(),
            'prod_type' : response.xpath('//table/tr[2]/td/text()').get()
        }