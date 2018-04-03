#coding:utf-8

from urllib.parse import quote
import json
import logging
import scrapy
import random
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings


hello = {}

class baidudistrict(scrapy.Spider):
    name = "baidudistrict"

    def __init__(self, category=None, *args, **kwargs):
        super(baidudistrict, self).__init__(*args, **kwargs)
        self.ak = ["oDdHH5wyAbY8LbivQoABL6K9fzLG8fdn", "BRBlNEMNKB7jwL2kAULKI66G", "SS2ARsiyPDUICwmm1Czco26M", "6UoGKz2uSlnIbRx8Tkf2k6tieSautsNX", "8N4bOwH8uxc5jAkiq4YtvNtF2hxrfOHm", "R7Uqthtlo2qX7hsqHqzl0fHQHt2qTB0K", "KN2gMhxOSEkF0rGdtX8HjPaLCTDd4R3t", "RN3Fh8pdhySe2uWOFkxykBIR3bOsEwLR", "CxVLi8MTtpMBOnfVIZtMUYDoFnqlgDxG", "ozp7CUFmGroNWcADNt0cGQay444Zy2FD", "ixZzi6sf3gBb4WR1BZlEP7qtAmszyXuf", "RPS2WViO94e94LP0rb7l8mktMoWeYYsD", "v93rqudol91IskcI6YSGA9xAxp4n6qDY", "xRe8VrQ3FauXjEocz3ILkXU7WwxYUrwE", "lOIRjcXb9Mnoe7c3CXO3ZXYbTsmL2hc1"]

    def start_requests(self):
        district = ["长沙雍景园", "长沙梦泽园", "长沙新华联家园"]
        request_url = ["http://map.baidu.cn/?newmap=1&reqflag=pcmap&from=webmap&qt=s&wd=", "&from=webmap"]
        for url in district:
            yield scrapy.Request(request_url[0] + quote(url, safe="/:?=") + request_url[1], self.get_district_uid)

    def get_district_uid(self, response):
        # response的content是list,第一个是小区信息,其它是具体的每一栋楼
        req_response = json.loads(response.body_as_unicode())
        district_name = req_response.get("content")[0]["name"]
        district_tag = req_response.get("content")[0]["std_tag"]
        uid = req_response.get("content")[0]["uid"]
        hello[uid] = [district_name, district_tag]
        logging.info("district name : " + district_name + "    district_tag : " + district_tag + "    uid : " + uid )
        # yield scrapy.Request("http://map.baidu.cn/?ugc_type=3&ugc_ver=1&qt=detailConInfo&uid=" + uid, self.get_district_info)
        yield scrapy.Request("http://map.baidu.cn/?newmap=1&qt=ext&uid=" + uid + "&ext_ver=new&l=18", self.get_district_band_geo, meta= {'uid':uid})

    def get_district_info(self, response):
        # response返回三个变量  status, interSource, content,其中content是详细信息,content[0]是总信息，content其它是各栋信息
        content = json.loads(response.body_as_unicode())['content']
        addr = content[0]["addr"]
        area_name = content[0]["addr"]
        name = content[0]["name"]

    def get_district_band_geo(self, response):
        # 返回的json的键 'content', 'current_city', 'err_msg', 'hot_city', 'psrs', 'result', 'suggest_query', 'uii_err'
        uid = response.meta['uid']
        # print(json.loads(response.body_as_unicode()))
        geo = json.loads(response.body_as_unicode())['content']['geo'].split("|")
        geo_format = [geo[0], geo[1].split(";"), geo[2].split("-")[0], geo[2].split("-")[1][:-1].split(",")]
        # hello[uid].append(geo_format)
        hello[uid].append([0] * (len(geo_format[1])))
        hello[uid].append([0]*(int(len(geo_format[3])/2)))
        for each_point in enumerate(zip(geo_format[3][::2], geo_format[3][1::2])):
            each_ak = random.choice(self.ak)
            yield scrapy.Request("http://api.map.baidu.com/geoconv/v1/?coords=" + ",".join(each_point[1]) + "&from=6&to=5&ak=" + each_ak, self.get_baidu_coordinate, meta={'loc': each_point[0], 'uid': uid, 'geo': 1})
        for each_point in enumerate(geo_format[1]):
            each_ak = random.choice(self.ak)
            yield scrapy.Request("http://api.map.baidu.com/geoconv/v1/?coords=" + each_point[1] + "&from=6&to=5&ak=" + each_ak, self.get_baidu_coordinate, meta={'loc': each_point[0], 'uid': uid, 'geo': 0})

    def get_baidu_coordinate(self, response):
        # 返回的json的键 status, result
        uid = response.meta['uid']
        loc = response.meta['loc']
        result = json.loads(response.body_as_unicode())
        geo = response.meta['geo']
        if result['status'] != 0:
            logging.info("get baidu coor error")
        coordinate = ",".join([str(result['result'][0]['x']), str(result['result'][0]['y'])])
        if geo == 1:
            hello[uid][-1][loc] = coordinate
        if geo == 0:
            hello[uid][-2][loc] = coordinate

settings = Settings()
settings.set("USER_AGENT", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)")
settings.set("DOWNLOAD_DELAY", 3)
settings.set("SCHEDULER_DISK_QUEUE", "scrapy.squeues.PickleFifoDiskQueue")
settings.set("SCHEDULER_MEMORY_QUEUE", "scrapy.squeues.FifoMemoryQueue")
settings.set('CONCURRENT_REQUESTS', 2)

process = CrawlerProcess(settings)
process.crawl(baidudistrict)
process.start()
print(hello)
