import scrapy


class QuotesSpider(scrapy.Spider):
    name = "remodd"
    start_urls = ['https://www.cs.colostate.edu/remodd/v1/repository?page={}'.format(x) for x in range(4)]

    def start_request(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse_data, dont_filter=True)

    def parse(self, response):
        #page = response.url.split("=")[-1]
        filename = 'assets.txt'
        #with open(filename, 'w') as f:
        for x in response.xpath('//tbody').css('tr'):
            url = response.urljoin(x.css('td.views-field-title a::attr(href)').get())
            yield scrapy.Request(url, callback=self.parse_asset_page)
            
            
    def parse_asset_page(self, response):
        content = response.css('div.content')
        yield{
            'title': response.css('h1.page-title::text').get(),
            'authors': content.css('div.field-name-field-submittersname div.field-item::text').get(),
            'organization': content.css('div.field-name-field-organization div.field-item::text').get(),
            'req-tools': content.css('div.field-name-field-reqtools div.field-item::text').get(),
            'languages': content.css('div.field-name-field-languages div.field-item::text').get(),
            'description': content.css('div.field-name-field-submissiondescription div.field-item p::text').getall(),
            'artifacts-link': content.css('div.field-type-link-field div.field-item a::attr(href)').getall(),
            'artifacts-types': content.css('div.field-name-taxonomy-vocabulary-8 div.field-items a::text').getall(),
            'artifacts-dev-context': content.css('div.field-name-taxonomy-vocabulary-3 div.field-items a::text').getall(),
            'software-domains': content.css('div.field-name-taxonomy-vocabulary-2 div.field-items a::text').getall(),
            'lifecycle-phases': content.css('div.field-name-taxonomy-vocabulary-7 div.field-items a::text').getall(),
            'modelinglanguages-notations': content.css('div.field-name-taxonomy-vocabulary-6 div.field-items a::text').getall(),
            'keyword': content.css('div.field-name-taxonomy-vocabulary-9 div.field-items a::text').getall(),
            'git-url': content.css('div.field-name-field-git-url div.field-item::text').get()
        }