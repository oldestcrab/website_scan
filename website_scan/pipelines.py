# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from website_scan.settings import *
import re
from warnings import filterwarnings
filterwarnings("error",category=pymysql.Warning)
import time

class WebsiteScanPipeline(object):
    def process_item(self, item, spider):
        return item

class GenecopoeiaaScanPipeline(object):
    def __init__(self):
        """
        初始化
        """
        # 链接数据库
        self.db = pymysql.connect(host=MYSQL_HOST,port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASSWORD, db=MYSQL_DB)
        # 获取句柄
        self.cursor = self.db.cursor()
        # 获取时间
        self.update_time = time.strftime('%Y-%m-%d',time.localtime())
        # 获取表名
        self.table = MYSQL_TABLE
    
    def process_item(self, item, spider):
        """
        添加url
        """
            # 判断url是否需要忽略
        count = 0
        for i in IGNORE_URL:
            pattern = re.compile(i, re.I)
            if pattern.search(item['url']):
                count += 1
        if not count:
                # real_url = re.sub(r'\/$', '', real_url)
            if not re.search(r'com\/\d+\/\d+', item['url']):

                data = {
                        'url':item['url'],
                        'code': item['code'],
                        'response_url': item['url'],
                        'update_time':self.update_time
                    }
                keys = ','.join(data.keys())
                values = ','.join(['%s']*len(data))
                sql = 'INSERT ignore INTO {table}({keys}) VALUES ({values}) ;'.format(table=self.table, keys=keys, values=values)

                # print(sql)
                try:
                    # 执行语句
                    if self.cursor.execute(sql,tuple(data.values())):
                        # 提交
                        self.db.commit()
                except pymysql.Warning as e:
                    # 错误则回滚
                    self.db.rollback()
                    print("add mysql failed", e.args)

        return item

    def close_spider(self, spider):
        """
        关闭链接
        """
        # 关闭句柄
        self.cursor.close()
        # 关闭链接
        self.db.close()