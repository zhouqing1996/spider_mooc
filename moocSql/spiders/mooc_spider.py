import scrapy
from moocSql.items import MoocsqlItem


class MoocSpiderSpider(scrapy.Spider):
    name = 'mooc_spider'
    allowed_domains = ['mooc.cn']
    start_urls = ['https://www.mooc.cn/course']

    num = 0
    def parse(self, response):
        courseList = response.xpath("//*[@id='newscontent']/div[@class='course-list']")
        # //*[@id='newscontent']/div[@class="course-list"]
        for course in courseList:
            courseName = course.xpath(".//div[2]/div[1]/h1/a/text()").get()
            if len(course.xpath(".//div[2]/div[2]/div[1]/span[1]/text()")):
                courseName_english = "中文课程没有英文名"
                schoolName = course.xpath(".//div[2]/div[2]/div[1]/span[1]/text()").get()
                language = course.xpath(".//div[2]/div[2]/div[2]//text()").getall()
                language = "".join(language).strip()
            else:
                courseName_english = course.xpath(".//div[2]/div[2]/text()").get()
                schoolName = course.xpath(".//div[2]/div[3]/div[1]/span[1]/text()").get()
                language = course.xpath(".//div[2]/div[3]/div[2]//text()").getall()
                language = "".join(language).strip()
            # 将数据给pipeline进行数据保存
            item = MoocsqlItem( courseName=courseName, courseName_English=courseName_english,
                               schoolName=schoolName, language=language)
            yield item
        next_url = response.xpath("//*[@id='newscontent']/div[last()]/nav/div/a[last()]/@href").get()
        # 下一页的链接
        print(next_url)
        if not next_url:
            return
        else:
            yield scrapy.Request(next_url, callback=self.parse)
