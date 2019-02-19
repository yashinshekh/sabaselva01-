# -*- coding: utf-8 -*-
import scrapy
import csv
import time
import pandas
import os

class FacebookSpider(scrapy.Spider):
    name = 'facebook'
    allowed_domains = ['facebook.com']
    start_urls = []

    filename = 'chinchinale'

    if filename+'.csv' not in os.listdir(os.getcwd()):
        with open(filename+".csv","a") as f:
            writer = csv.writer(f)
            writer.writerow(['url','name','streetaddress','country','number','cuisine','parking','specialties','services','email','website','about','attire','general_manager'])

    with open('links.csv','r') as r:
        reader = csv.reader(r)
        for line in reader:
            start_urls.append(line[0])

    try:
        alreadylinks = pandas.read_csv(filename+'.csv').url.tolist()
    except:
        alreadylinks = []
        pass

    def start_requests(self):
        for url in self.start_urls:
            if '/pages/' not in url and url not in self.alreadylinks:
                yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        aboutlink = response.xpath('.//a[contains(.,"About")]/@href').extract_first()
        if aboutlink:
            yield scrapy.Request(response.urljoin(aboutlink),callback=self.scrapedata,meta={'url':response.url})

    def scrapedata(self,response):
        # time.sleep(1)
        try:
            name = response.xpath('.//title/text()').extract_first().split('-')[0]
        except:
            name = ''
        try:
            streetaddress = response.xpath('.//*[@class="_2iem"]/text()').extract_first()
        except:
            streetaddress = ''
        try:
            country = response.xpath('.//*[@class="_2iem"]/text()').extract()[1]
        except:
            country = ''
        try:
            number = response.xpath('.//div[contains(.,"Call")]/text()').extract_first().replace('Call ','')
        except:
            number = ''
        try:
            cuisine = response.xpath('.//div[contains(.,"Cuisine")]/following-sibling::div/span/text()').extract_first()
        except:
            cuisine = ''
        try:
            parking = response.xpath('.//div[contains(.,"Parking")]/following-sibling::div/span/text()').extract_first()
        except:
            parking = ''
        try:
            specialties =  response.xpath('.//div[contains(.,"Specialties")]/following-sibling::div/span/text()').extract_first()
        except:
            specialties = ''
        try:
            services = ', '.join(response.xpath('.//div[contains(.,"Services")]/following-sibling::div/span/text()').extract())
        except:
            services = ''
        try:
            email = response.xpath('.//a/@href[contains(.,"mailto")]/../div/text()').extract_first()
        except:
            email = ''
        try:
            website = response.xpath('.//div[@class="_4bl9"]/a/div/div/div/text()').extract_first()
        except:
            website = ''
        try:
            about = response.xpath('.//div[contains(.,"About")]/following-sibling::div/text()').extract_first()
        except:
            about = ''
        try:
            attire = response.xpath('.//div[contains(.,"Attire")]/following-sibling::div/text()').extract_first()
        except:
            attire = ''
        try:
            general_manager = response.xpath('.//div[contains(.,"General Manager")]/following-sibling::div/text()').extract_first()
        except:
            general_manager = ''

        with open(self.filename+".csv","a") as f:
            writer = csv.writer(f)
            writer.writerow([response.meta.get('url'),name,streetaddress,country,number,cuisine,parking,specialties,services,email,website,about,attire,general_manager])
            print([response.meta.get('url'),name,streetaddress,country,number,cuisine,parking,specialties,services,email,website,about,attire,general_manager])

