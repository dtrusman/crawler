import scrapy;
from scrapy.shell import inspect_response

BASE_URL = "https://lojaeaglemossbrasil.com.br"

class DCSpider(scrapy.Spider):
    name = "eaglemoss"
    urls = list();
    for i in range(1, 10):
        urls.append(BASE_URL + "/eaglemoss/vitrines/colecao-miniaturas-dc-comics-super-herois.aspx?pg=" + str(i))

    start_urls = urls

    def parse(self, response):
        SET_SELECTOR = '.product'
        for figures in response.css(SET_SELECTOR):
            # inspect_response(response, self)
            IMAGE_SELECTOR = 'img::attr(src)'
            NAME_SELECTOR = '.little-desc a::text'
            PRICE_SELECTOR = '.price ::text'
            yield {
                'image': figures.css(IMAGE_SELECTOR).extract_first().strip(),
                'name': figures.css(NAME_SELECTOR).extract_first().strip(),
                'price': figures.css(PRICE_SELECTOR).extract_first().strip(),
            }

        NEXT_PAGE_SELECTOR = ".pagingFirstLast ::attr(href)"
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            # print(BASE_URL + next_page)
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )