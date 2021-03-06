#coding:utf-8

import pandas
import pandas as pd
import numpy as np
import datetime
import calendar
import logging
import time
from datetime import date
from dateutil.relativedelta import relativedelta
from sqlalchemy import select, create_engine
from sqlalchemy.types import VARCHAR, String, TIME, Date, Numeric, FLOAT, Integer, BIGINT
from sqlalchemy.dialects.mysql import DOUBLE

from urllib.parse import quote
import json
import logging
import scrapy
import random
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
import pickle


hello = []
hunanschool = {}


class baidudistrict(scrapy.Spider):
    name = "baidudistrict"
    district_lng_and_lat = hello
    school = hunanschool

    def __init__(self, category=None, *args, **kwargs):
        super(baidudistrict, self).__init__(*args, **kwargs)
        self.ak = ["oDdHH5wyAbY8LbivQoABL6K9fzLG8fdn", "BRBlNEMNKB7jwL2kAULKI66G", "SS2ARsiyPDUICwmm1Czco26M", "6UoGKz2uSlnIbRx8Tkf2k6tieSautsNX", "8N4bOwH8uxc5jAkiq4YtvNtF2hxrfOHm", "R7Uqthtlo2qX7hsqHqzl0fHQHt2qTB0K", "KN2gMhxOSEkF0rGdtX8HjPaLCTDd4R3t", "RN3Fh8pdhySe2uWOFkxykBIR3bOsEwLR", "CxVLi8MTtpMBOnfVIZtMUYDoFnqlgDxG", "ozp7CUFmGroNWcADNt0cGQay444Zy2FD", "ixZzi6sf3gBb4WR1BZlEP7qtAmszyXuf", "RPS2WViO94e94LP0rb7l8mktMoWeYYsD", "v93rqudol91IskcI6YSGA9xAxp4n6qDY", "xRe8VrQ3FauXjEocz3ILkXU7WwxYUrwE", "lOIRjcXb9Mnoe7c3CXO3ZXYbTsmL2hc1"]

    def start_requests(self):
        district = ["http://map.baidu.com/?newmap=1&reqflag=pcmap&from=webmap&da_par=direct&pcevaname=pc4.1&qt=ext&l=10&uid=3959e82b0c19ca50a2d230e6"]
        for url in district:
            yield scrapy.Request(url, self.get_district_range)

    def get_district_range(self, response):
        req_response = json.loads(response.body_as_unicode())
        district_point = req_response.get("content")["geo"][:-1].split("|")
        district_range_point = district_point[2].split(";")[0].split(",")
        district_min_lng = float(district_point[1].split(";")[0].split(",")[0])
        district_min_lat = float(district_point[1].split(";")[0].split(",")[1])
        district_max_lng = float(district_point[1].split(";")[1].split(",")[0])
        district_max_lat = float(district_point[1].split(";")[1].split(",")[1])
        district_polygon = [(float(district_range_point[i]), float(district_range_point[i + 1])) for i in range(0, len(district_range_point), 2)]

        district_need_lng = (district_max_lng - district_min_lng) / 400
        district_need_lat = (district_max_lat - district_min_lat) / 400
        # print(district_need_lng, district_need_lat)
        # print(district_polygon)
        for i in range(400):
            for j in range(400):
                district_lng = district_min_lng + district_need_lng * i
                district_lat = district_min_lat + district_need_lat * j
                point = ','.join([str(district_min_lat + district_need_lat * j), str(district_min_lng + district_need_lng * i)])
                if self.check_point_in_polygon([district_lng, district_lat], district_polygon):
                    # print("in district range, the point is ", [district_lng, district_lat])
                    yield scrapy.Request("http://api.map.baidu.com/place/v2/search?query=行政村&location={}&radius=40000&output=json&scope=2&filter=distance&coord_type=4&ret_coordtype=gcj02ll&page_size=20&ak=".format(point) + random.choice(self.ak), self.get_district_need_save)
                else:
                    pass
                    # print("Not in district range, the point is ", [district_lng, district_lat])

    def get_district_need_save(self, response):
        content = json.loads(response.body_as_unicode())
        print('hello', content)
        try:
            if content['status'] == 0:
                if len(content['results']) > 0:
                    print(content)
                    for h in content['results']:
                        school_name = h['name']
                        school_location_lat = h['location']['lat']
                        school_location_lng = h['location']['lng']
                        school_address = h['address']
                        school_uid = h['uid']
                        school_detail_url = h['detail_info']['detail_url']
                        print([school_name, school_location_lat, school_location_lng, school_address, school_detail_url])
                        self.school[school_uid] = [school_name, school_location_lat, school_location_lng,school_address, school_detail_url]
            else:
                yield scrapy.Request(response.url[:response.url.index('&ak=') + 4] + random.choice(self.ak),  self.get_district_need_save)
        except:
            print("Detect error.", content)

    def get_district_band_geo(self, polygen_need_change, polygen_change):
        try:
            polygen_change += [[0,0]] * len(polygen_need_change)
            for each_point in enumerate(polygen_need_change):
                polygen_change.append([0, 0])
                each_ak = random.choice(self.ak)
                yield scrapy.Request("http://api.map.baidu.com/geoconv/v1/?coords=" + ",".join(each_point[1]) + "&from=6&to=5&ak=" + each_ak, self.get_baidu_coordinate, meta={'loc': each_point[0], 'after_change': polygen_change})
            print(polygen_change)
        except Exception as e:
            print(e)

    def get_baidu_coordinate(self, response):
        # 返回的json的键 status, result
        polygen_change = response.meta['after_change']
        loc = response.meta['loc']
        result = json.loads(response.body_as_unicode())
        if result['status'] == 0:
            polygen_change[loc][0] = result['result'][0]['x']
            polygen_change[loc][1] = result['result'][0]['y']
        else:
            yield scrapy.Request(response.url[:response.url.index('&ak=') + 4] + random.choice(self.ak), self.get_baidu_coordinate, meta={'loc': loc, 'after_change': polygen_change})


    def check_point_in_polygon(self, point, polygon):
        """point is the point which format is (x, y)"""
        """polygen is the tuple or list which contains point that form polygon , format is [(x1, y1), (x2, y2)....]"""
        status = False
        len_polygon = len(polygon)
        for i in range(len_polygon):
            j = (i + 1) % len_polygon
            if ((polygon[i][1] > point[1]) != (polygon[j][1] > point[1])) and ( point[0] < (polygon[j][0] - polygon[i][0]) * (point[1] - polygon[i][1]) / (polygon[j][1] - polygon[i][1]) + polygon[i][0]):
                status = not status
        return status

settings = Settings()
settings.set("USER_AGENT", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)")
# settings.set("DOWNLOAD_DELAY", 3)
settings.set("SCHEDULER_DISK_QUEUE", "scrapy.squeues.PickleFifoDiskQueue")
settings.set("SCHEDULER_MEMORY_QUEUE", "scrapy.squeues.FifoMemoryQueue")
settings.set('CONCURRENT_REQUESTS', 100)

process = CrawlerProcess(settings)
process.crawl(baidudistrict)
process.start()
pickle.dump(hello, open("school_object", "wb"))
pickle.dump(hunanschool, open("hospital", "wb"))

