import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider


class WikiSpyder(CrawlSpider):
    name = "wiki"
    custom_settings = {
      'CLOSESPIDER_ITEMCOUNT': 1000,
   }
    allowed_domains = ['en.wikipedia.org']
    start_urls= ['https://en.wikipedia.org/wiki/Category:Articles_using_Infobox_video_game_using_locally_defined_parameters']
    rules = {
          Rule(LinkExtractor(allow = (), restrict_xpaths = ('//*[@id="toctitle"]/a'))),
          Rule(LinkExtractor(allow=(), restrict_xpaths = ('//*[@class="mw-category-group"]/ul//li//a')),
            callback = 'parse_games', follow = False)
    }



    def parse_games(self, response):
        dicgame ={}
        game_name = response.xpath('//*[@class="fn"]//text()').extract()
        dicgame['name'] = game_name
        for u in response.xpath('//*[@class="infobox hproduct"]/tbody/tr')[2:]:
            item = [s.strip('\n') for s in u.xpath(u'.//td//text()').extract()]
            item_name = u.xpath(u'.//th//text()').extract_first()
            dicgame[item_name] = item
        return dicgame
