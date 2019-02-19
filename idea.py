# -*- coding: utf-8 -*-
import scrapy
import csv
from bs4 import BeautifulSoup

class IdeaSpider(scrapy.Spider):
    name = 'idea'
    allowed_domains = ['ideafit.com']
    start_urls = ['https://www.ideafit.com/fitnessconnect']

    with open("AllData.csv","a") as f:
        writer = csv.writer(f)
        writer.writerow(['name','profile_pic','address','zipcode','profile_url','facebook_link','twitter_link','description','gender','website'])

    def parse(self, response):
        links = response.xpath('.//*[@class="block-grid-xs-1 block-grid-sm-2 block-grid-md-2 type-links"]/div/a/@href[contains(.,"find-")]').extract()
        for link in links:
            yield scrapy.Request(response.urljoin(link),callback=self.getcities)

    def getcities(self,response):
        states = response.xpath('.//div[contains(.,"Select a State")]/div/div/a/@href').extract()
        for state in states:
            yield scrapy.Request(response.urljoin(state),callback=self.getstates)

    def getstates(self,response):
        links = response.xpath('.//div[@class="col-xs-12 col-sm-6 col-md-3"]/a/@href[contains(.,"find-")]').extract()
        for link in links:
            yield scrapy.Request(response.urljoin(link),callback=self.getlinks)

    def getlinks(self,response):
        links = response.xpath('.//*[@class="thin no-margin-top"]/a/@href').extract()
        for link in links:
            yield scrapy.Request(response.urljoin(link),callback=self.getdata)

        nextlink = response.xpath('.//a[contains(.,"»")]/@href').extract_first()
        if nextlink:
            yield scrapy.Request(response.urljoin(nextlink),callback=self.getlinks)

    def getdata(self,response):
        links = response.xpath('.//*[@class="block-grid-item text-center"]/a/@href[contains(.,"profile")]').extract()
        if links:
            for link in links:
                yield scrapy.Request(response.urljoin(link),callback=self.getdata)
        else:
            name = response.xpath('.//h1/text()').extract_first()
            try:
                profile_pic = response.xpath('.//*[@class="profile-picture"]/img/@src').extract_first()
                if 'http' not in profile_pic:
                    profile_pic = 'https:'+str(profile_pic)
            except:
                profile_pic = ''
            address = response.xpath('.//h1/following-sibling::p/text()').extract_first()
            try:
                zipcode = ','.join([i for i in response.xpath('.//h1/following-sibling::p/text()').extract_first().split() if i.isdigit()])
            except:
                zipcode = ''
            profile_url = response.url
            facebook_link = response.xpath('.//*[@class="btn btn-block btn-facebook btn-sm"]/@href').extract_first()
            twitter_link = response.xpath('.//*[@class="btn btn-block btn-twitter btn-sm"]/@href').extract_first()
            try:
                description = BeautifulSoup(response.xpath('.//*[@class="about with-show"]').extract_first(),'lxml').get_text()
            except:
                description = ''
            gender = response.xpath('.//div[contains(.,"Gender")]/following-sibling::div/text()').extract_first()
            website = response.xpath('.//div[contains(.,"Website")]/following-sibling::div/a/text()').extract_first()

            with open("AllData.csv","a") as f:
                writer = csv.writer(f)
                writer.writerow([name,profile_pic,address,zipcode,profile_url,facebook_link,twitter_link,description,gender,website])
                print([name,profile_pic,address,zipcode,profile_url,facebook_link,twitter_link,description,gender,website])

