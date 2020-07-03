# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import JsonLinesItemExporter
import pymysql


class MoocsqlPipeline:
    def __init__(self):
        # 存储在本地文件中
        self.fp = open("moocsql.json", 'wb')
        self.exporter = JsonLinesItemExporter(self.fp, ensure_ascii=False, encoding='utf-8')
        # # 存储在数据库中
        # # 连接数据库
        # self.connect = pymysql.connect(host='120.78.150.89', user='root', password='zhouqing', db='mooc')
        # self.cursor = self.connect.cursor()
        # print("连接数据库成功！")

    def open_spider(self, spider):
        print("开始爬虫")
        pass
        # 打开爬虫

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.fp.close()
        print("爬虫结束")
        pass
        # 关闭爬虫


class MoocPipeline(object):
    def __init__(self):
        # 存储在数据库中
        # 连接数据库
        self.connect = None
        self.cursor = None
        self.num = 0

    def open_spider(self, spider):
        print("开始爬虫")
        self.connect = pymysql.connect(host='120.78.150.89', port=3306, user='root', password='zhouqing', db='mooc',
                                       charset='utf8')
        print("连接数据库成功！")
        pass
        # 打开爬虫

    def process_item(self, item, spider):
        courseName = item['courseName']
        courseName_English = item['courseName_English']
        schoolName = item['schoolName']
        language = item['language']
        self.cursor = self.connect.cursor()
        self.cursor.execute('select count(*) from `courseList`')
        count = self.cursor.fetchone()
        try:
            insertValues = """"insert into courseList(id,courseName,courseName_English,schoolName,language) VALUES (
            %s,%s,%s,%s, %s) """
            self.cursor.execute('insert into `courseList` values (%s,%s,%s,%s,%s)', (count, courseName, courseName_English, schoolName, language))
            self.connect.commit()
        except Exception as e:
            print(e)
            self.connect.rollback()
        return item

    def close_spider(self, spider):
        print("爬虫结束")
        self.cursor.close()
        self.connect.close()
        pass
        # 关闭爬虫
