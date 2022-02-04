# to run 
# scrapy crawl imdb_spider -o movies.csv

import scrapy
import re

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    
    start_urls = ['https://www.imdb.com/title/tt10872600/']

    def parse(self, response):
        # navigate to the Cast & Crew page
        url = response.urljoin("fullcredits")
        yield scrapy.Request(url, callback = self.parse_full_credits)

    def parse_full_credits(self, response):
        for actor_link in [a.attrib["href"] for a in response.css("td.primary_photo a")]:
            yield scrapy.Request(response.urljoin(actor_link), callback = self.parse_actor_page)

    def parse_actor_page(self, response):
        # get the name of the actor
        actor_name = response.css("span.itemprop ::text").get()
        # get all the titles of movies and TV shows which id that is actor only.
        titles_actor_only = response.css('div.filmo-row[id^=actor] b a ::text').getall()

        for title in titles_actor_only:
            yield {
                "actor" : actor_name,
                "movie_or_TV_name" : title
            }