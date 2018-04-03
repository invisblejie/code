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


def add_name(cnty_id, id_dict):
    return id_dict.get(cnty_id)

def get_district_url(df):
    hello = ["oDdHH5wyAbY8LbivQoABL6K9fzLG8fdn", "BRBlNEMNKB7jwL2kAULKI66G", "SS2ARsiyPDUICwmm1Czco26M",
     "6UoGKz2uSlnIbRx8Tkf2k6tieSautsNX", "8N4bOwH8uxc5jAkiq4YtvNtF2hxrfOHm", "R7Uqthtlo2qX7hsqHqzl0fHQHt2qTB0K",
     "KN2gMhxOSEkF0rGdtX8HjPaLCTDd4R3t", "RN3Fh8pdhySe2uWOFkxykBIR3bOsEwLR", "CxVLi8MTtpMBOnfVIZtMUYDoFnqlgDxG",
     "ozp7CUFmGroNWcADNt0cGQay444Zy2FD", "ixZzi6sf3gBb4WR1BZlEP7qtAmszyXuf", "RPS2WViO94e94LP0rb7l8mktMoWeYYsD",
     "v93rqudol91IskcI6YSGA9xAxp4n6qDY", "xRe8VrQ3FauXjEocz3ILkXU7WwxYUrwE", "lOIRjcXb9Mnoe7c3CXO3ZXYbTsmL2hc1"]
    return "http://api.map.baidu.com/geocoder/v2/?address=" + quote(str(df['region_location']), safe="/:?=") + "&city=" + quote(str(df['city']), safe="/:?=") +"&output=json&ak=" + random.choice(hello)

lng = {}
lat = {}
district_inner = pd.read_excel('attack_district.xls')
district_inner['city'] = district_inner['地市'].str[2:]
print(district_inner['city'])
other_name = ['（他建）', 'ZTE小区', '（百兆）', '（华为增补）', '2016', '2017年', '2017', '扩容小区', '小区','（铁通）', '(铁通)', 'ZTE小区', '（铁通迁移）',  '周边ZTE小区', 'HW', 'ZX资源村三组补点小区', '及周边ZTE小区', '常德常沅6组片区TT小区', '小区', '铁通', 'ZTE小区', '中兴', '政企宽带专用小区', '华为', '华为','铁通','FTTH片区小区', 'ZX', '安置小区', '(铁通光改)','铁通迁移','对面新房小区', '（铁通光改）', '片区小区', '（FTTH中兴）', '（光交箱移位，暂勿录单）', '行政村', '周边铁通小区', '(长沙中信)', '周边小区', 'FTTB小区',  '散户小区',  '私房及周边小区', '对面（扩容）小区','附近私宅小区',  '无线宽带小区', '1-8片(铁通光改)小区', '(铁通割接)', '(铁通光改)小区', 'ZTE乡', '周边私房小区', '长沙新星小区','2级分光小区', '安置区Q9.1小区', 'TT小区', '九组小区', '（不能发展业务）', 'SGR基站小区', '区域ZTE小区',  '2015光改', '移动小区', '（铁通）', '1、2、3小区', 'T3.4小区', 'AD小区', '（FTTH中兴）', '周边补点小区', 'ZTE小区', 'AB小区', '(无线宽带自建)小区',  '（FTTH烽火）', '扩容2小区', '（待测试）小区', '（光改）', '（无线宽带他建）','(T)小区', '（管道纠纷，需加收50元）', '(他建)', '(EPON改造)小区','（暂勿录单）', 'TZ基站小区','（扩容）小区','（无线覆盖）', '（中兴）', 'E（整治中，暂勿录单）小区','3SGR基站小区', '（铁通光改）', '（FTTB烽火和FTTH中兴）','LX','（无线覆盖）', '散户小区', '无线宽带TZ基站小区','（无线宽带他建）小区', '（千兆）小区', '（FTTH中兴）', 'PON(铁通割接)小区','（自建自营）中兴', '（修梅自建）华为', '（仅由迈思集录单）小区', '（不能发展业务）',  '华为','（LAN）小区', 'YH基站小区', '无线WBS专用小区','补点小区','（散户）小区','（广电移动合作）', '（FTTH）', '(割接)', '（扩容）', '（迁移）','(T)', 'TT', '片区','（）', '（迁移）','()','()','（管道纠纷，需加收100元）' ,'(FB)', '()']
replace_need = sorted(list(set(other_name)), key=len, reverse=True)
district_inner['region_location'] = district_inner['小区名称'].replace(to_replace=replace_need, value='', regex=True)
district_inner['district_name'] = district_inner['小区名称']
district_inner['region_url'] = district_inner.apply(get_district_url, axis=1)
district_inner['region_id'] = district_inner['小区编码']
district = pd.Series(district_inner.region_url.values, index=district_inner.district_name).to_dict()
print(district)

class baidudistrict(scrapy.Spider):
    name = "baidudistrict"

    def __init__(self, category=None, *args, **kwargs):
        super(baidudistrict, self).__init__(*args, **kwargs)
        self.ak = ["oDdHH5wyAbY8LbivQoABL6K9fzLG8fdn", "BRBlNEMNKB7jwL2kAULKI66G", "SS2ARsiyPDUICwmm1Czco26M", "6UoGKz2uSlnIbRx8Tkf2k6tieSautsNX", "8N4bOwH8uxc5jAkiq4YtvNtF2hxrfOHm", "R7Uqthtlo2qX7hsqHqzl0fHQHt2qTB0K", "KN2gMhxOSEkF0rGdtX8HjPaLCTDd4R3t", "RN3Fh8pdhySe2uWOFkxykBIR3bOsEwLR", "CxVLi8MTtpMBOnfVIZtMUYDoFnqlgDxG", "ozp7CUFmGroNWcADNt0cGQay444Zy2FD", "ixZzi6sf3gBb4WR1BZlEP7qtAmszyXuf", "RPS2WViO94e94LP0rb7l8mktMoWeYYsD", "v93rqudol91IskcI6YSGA9xAxp4n6qDY", "xRe8VrQ3FauXjEocz3ILkXU7WwxYUrwE", "lOIRjcXb9Mnoe7c3CXO3ZXYbTsmL2hc1"]

    def start_requests(self):
        for url in district:
            yield scrapy.Request(district[url], self.get_district_uid, meta={'inner_district_id': url})

    def get_district_uid(self, response):
        try:
            # response的content是list,第一个是小区信息,其它是具体的每一栋楼
            region_id = response.meta['inner_district_id']
            result = json.loads(response.body_as_unicode())
            if result["status"] == 0:
                lng[region_id] = result["result"]["location"]['lng']
                lat[region_id] = result["result"]["location"]['lat']
                # return result["result"]["location"]['lng'], result["result"]["location"]['lat']
            else:
                lng[region_id] = None
                lat[region_id] = None
        except:
            lng[region_id] = None
            lat[region_id] = None


settings = Settings()
settings.set("USER_AGENT", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)")
# settings.set("DOWNLOAD_DELAY", 3)
settings.set("SCHEDULER_DISK_QUEUE", "scrapy.squeues.PickleFifoDiskQueue")
settings.set("SCHEDULER_MEMORY_QUEUE", "scrapy.squeues.FifoMemoryQueue")
settings.set('CONCURRENT_REQUESTS', 100)

process = CrawlerProcess(settings)
process.crawl(baidudistrict)
process.start()

pickle.dump(lng, open('lng', 'wb'))
pickle.dump(lat, open('lat', 'wb'))
district_inner['lng'] = district_inner['district_name'].apply(add_name, args=(lng,))
district_inner['lat'] = district_inner['district_name'].apply(add_name, args=(lat,))
district_inner.to_csv('district1.out', sep='|')
# writer = pd.ExcelWriter('output.xlsx')
# district_inner.to_excel(writer,'Sheet1')
# print(hello)
# pickle.dump(hello,open('furong','wb'))

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
