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


hello = {}
district_inner = pickle.load(open('district_inner', 'rb'))
district_inner['region_location'] = district_inner['city_name'] + district_inner['region_name']
other_name = ['（铁通）', '(铁通)', 'ZTE小区', '（铁通迁移）',  '周边ZTE小区', 'HW', 'ZX资源村三组补点小区', '及周边ZTE小区', '常德常沅6组片区TT小区', '小区', '铁通', 'ZTE小区', '中兴', '政企宽带专用小区', '华为', '华为','铁通','FTTH片区小区', 'ZX', '安置小区', '(铁通光改)','铁通迁移','对面新房小区', '（铁通光改）', '片区小区', '（FTTH中兴）', '（光交箱移位，暂勿录单）', '行政村', '周边铁通小区', '(长沙中信)', '周边小区', 'FTTB小区',  '散户小区',  '私房及周边小区', '对面（扩容）小区','附近私宅小区',  '无线宽带小区', '1-8片(铁通光改)小区', '(铁通割接)', '(铁通光改)小区', 'ZTE乡', '周边私房小区', '长沙新星小区','2级分光小区', '安置区Q9.1小区', 'TT小区', '九组小区', '（不能发展业务）', 'SGR基站小区', '区域ZTE小区',  '2015光改', '移动小区', '（铁通）', '1、2、3小区', 'T3.4小区', 'AD小区', '（FTTH中兴）', '周边补点小区', 'ZTE小区', 'AB小区', '(无线宽带自建)小区',  '（FTTH烽火）', '扩容2小区', '（待测试）小区', '（光改）', '（无线宽带他建）','(T)小区', '（管道纠纷，需加收50元）', '(他建)', '(EPON改造)小区','（暂勿录单）', 'TZ基站小区','（扩容）小区','（无线覆盖）', '（中兴）', 'E（整治中，暂勿录单）小区','3SGR基站小区', '（铁通光改）', '（FTTB烽火和FTTH中兴）','LX','（无线覆盖）', '散户小区', '无线宽带TZ基站小区','（无线宽带他建）小区', '（千兆）小区', '（FTTH中兴）', 'PON(铁通割接)小区','（自建自营）中兴', '（修梅自建）华为', '（仅由迈思集录单）小区', '（不能发展业务）',  '华为','（LAN）小区', 'YH基站小区', '无线WBS专用小区','补点小区','（散户）小区','（广电移动合作）', '（FTTH）', '(割接)', '（扩容）', '（迁移）','(T)', 'TT', '片区','（）', '（迁移）','()','()','（管道纠纷，需加收100元）' ,'(FB)', '()']
replace_need = sorted(list(set(other_name)), key=len, reverse=True)
district_inner['region_location'] = district_inner['region_location'].replace(to_replace= replace_name, value='', regex=True)

name = ['region_name', 'district_page', 'region_pric', 'district_compare_last_month',
            'district_compare_last_year', 'district_sell_number', 'district_name', 'district_rent_number',
            'district_location', 'district_type', 'city_name', 'cnty_name', 'small_cnty_name',
            'district_build_time', 'district_home_area', 'region_size', 'region_build_cnt',
            'region_home_cnt', 'district_total_family_number',
            'district_green_rate', 'district_volume_rate', 'district_property_management_phone',
            'district_property_management_money', 'region_longitude', 'region_latitude']
data_map = {'region_longitude': float, 'region_latitude': float}
district_web_new = pd.read_csv("SouFanDistrictNow.text", encoding='utf-8', sep='|', names=name)
district_web_new['region_location'] = district_web_new['city_name'] + district_web_new['region_name']
district_web = list(district_web_new.region_location.values)

district_need = district_inner[district_inner['cnty_name'] == '芙蓉']
district_need_web = district_web_new[district_web_new['cnty_name'] == '芙蓉']

district_web = list(district_need_web.region_location.values)
district_web = pd.Series(district_need_web.region_location.values, index=district_need_web.region_name).to_dict()
print(district_web)
district = list(district_need.region_location.values)
district = pd.Series(district_need.region_location.values, index=district_need.region_name).to_dict()

district = {**district_web, **district}
print(district)

# district = district + district_web
# print(district)

class baidudistrict(scrapy.Spider):
    name = "baidudistrict"

    def __init__(self, category=None, *args, **kwargs):
        super(baidudistrict, self).__init__(*args, **kwargs)
        self.ak = ["oDdHH5wyAbY8LbivQoABL6K9fzLG8fdn", "BRBlNEMNKB7jwL2kAULKI66G", "SS2ARsiyPDUICwmm1Czco26M", "6UoGKz2uSlnIbRx8Tkf2k6tieSautsNX", "8N4bOwH8uxc5jAkiq4YtvNtF2hxrfOHm", "R7Uqthtlo2qX7hsqHqzl0fHQHt2qTB0K", "KN2gMhxOSEkF0rGdtX8HjPaLCTDd4R3t", "RN3Fh8pdhySe2uWOFkxykBIR3bOsEwLR", "CxVLi8MTtpMBOnfVIZtMUYDoFnqlgDxG", "ozp7CUFmGroNWcADNt0cGQay444Zy2FD", "ixZzi6sf3gBb4WR1BZlEP7qtAmszyXuf", "RPS2WViO94e94LP0rb7l8mktMoWeYYsD", "v93rqudol91IskcI6YSGA9xAxp4n6qDY", "xRe8VrQ3FauXjEocz3ILkXU7WwxYUrwE", "lOIRjcXb9Mnoe7c3CXO3ZXYbTsmL2hc1"]

    def start_requests(self):
        # district = district
        # district = ["长沙雍景园", "长沙梦泽园", "长沙新华联家园"]
        request_url = ["http://map.baidu.cn/?newmap=1&reqflag=pcmap&from=webmap&qt=s&wd=", "&from=webmap"]
        for url in district:
            yield scrapy.Request(request_url[0] + quote(district[url], safe="/:?=") + request_url[1], self.get_district_uid, meta={'inner_district_name': url})

    def get_district_uid(self, response):
        try:
            # response的content是list,第一个是小区信息,其它是具体的每一栋楼
            inner_district_name = response.meta['inner_district_name']
            req_response = json.loads(response.body_as_unicode())
            district_name = req_response.get("content")[0]["name"]
            district_tag = req_response.get("content")[0]["std_tag"]
            uid = req_response.get("content")[0]["uid"]
            hello[uid] = [inner_district_name, district_name, district_tag]
            logging.info("district name : " + district_name + "    district_tag : " + district_tag + "    uid : " + uid)
            yield scrapy.Request("http://map.baidu.cn/?newmap=1&qt=ext&uid=" + uid + "&ext_ver=new&l=18", self.get_district_band_geo, meta= {'uid':uid})
        except Exception as e:
            print(e)


    def get_district_info(self, response):
        # response返回三个变量  status, interSource, content,其中content是详细信息,content[0]是总信息，content其它是各栋信息
        content = json.loads(response.body_as_unicode())['content']
        addr = content[0]["addr"]
        area_name = content[0]["addr"]
        name = content[0]["name"]

    def get_district_band_geo(self, response):
        try:
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
        except Exception as e:
            print(e)

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
settings.set('CONCURRENT_REQUESTS', 5)

process = CrawlerProcess(settings)
process.crawl(baidudistrict)
process.start()
print(hello)
pickle.dump(hello,open('furong','wb'))

# import pickle
# import pandas as pd
# hello = pickle.load(open('hello','rb'))
# hi = {}
# for i in hello:
#     try:
#         if len(hello[i]) > 3:
#             min_loc = hello[i][2][0]
#             max_loc = hello[i][2][1]
#             if type(hello[i][3][-1]) == int:
#                 loc = hello[i][3][:-1]
#             else:
#                 loc = hello[i][3]
#             hi[i] = [hello[i][0], hello[i][1], min_loc.split(',')[0], min_loc.split(',')[1], max_loc.split(',')[0] , max_loc.split(',')[1], '|'.join(loc)]
#     except:
#         print(hello[i])
# district = pd.DataFrame(hi).transpose()
# district.rename(columns = {0:'region_name',1:'region_tag', 2:'region_minlng', 3:'region_minlat',4:'region_maxlng', 5:'region_maxlat',6:'region_outline'},inplace=True)
# e = create_engine("db2+ibm_db://ericsson:4qaz$WSX@10.154.147.218:50002/showdb", pool_size=5, max_overflow=0, echo=True)
# sql = "select * from TA_RP_BROADBAND_POTEN_USER_M FETCH FIRST 1 ROWS ONLY with ur"
# potential_init = pd.read_sql(sql, e)
# region_type = {'statis_month': VARCHAR(6), 'city_name': VARCHAR(50), 'cnty_name': VARCHAR(50),  'region_name': VARCHAR(256),
#                       'region_minlng': VARCHAR(20), 'region_minlat': VARCHAR(20), 'region_maxlng': VARCHAR(20), 'region_maxlat': VARCHAR(20),
#                       'region_outline': VARCHAR(3500)  }
# district['cnty_name'] = '芙蓉'
# district['city_name'] = '长沙'
# district[['city_name','cnty_name','region_name','region_minlng','region_minlat','region_maxlng', 'region_maxlat','region_outline']].to_sql('TA_DT_BROADBAND_REGION_GRIDS_M',e, dtype=region_type, if_exists='append', index=False, chunksize=10000)
#
