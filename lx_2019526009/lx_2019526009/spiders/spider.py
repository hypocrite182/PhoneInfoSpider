import scrapy
from lx_2019526009.items import Phone
from urllib import parse
import json
from lx_2019526009.helper import register,get_phone_list,JustMark


class JDStartSpider(scrapy.spiders.Spider):
    name="jdStart"
    allowed_domains = ["jd.com"]
    start_urls = []
    for i in range(1):
        start_urls.append("https://list.jd.com/list.html?cat=9987,653,655&page={0}&sort=sort_commentcount_desc&trans=1&JL=4_5_0#J_main".format(i))

    def parse(self, response):
        if "list.jd.com/list.html" in response.url:
        #第一部分：先爬到所有手机，这儿由于效率不高，排序后爬取前60种手机
            for each in response.xpath("//div[@id='plist']//li[@class='gl-item']"):
                str = each.xpath(".//div[@class='p-name']//a/@href").extract_first()
                yield scrapy.Request("http:" + str, callback=self.parse, dont_filter=True)

        if "item.jd.com" in response.url:
        #第二部分：进入每种手机的详情页，得到这种手机的准确型号
            each = response.xpath("//div[@class='item ellipsis']")
            str = each.xpath("./text()").extract_first()
            if str:
                yield scrapy.Request(f"http://search.jd.com/Search?keyword={str}&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&bs=1&wq={str}&psort=4&click=0", callback=self.parse, dont_filter=True)

        if "search.jd.com" in response.url:
        #第三部分：通过搜索手机的准确型号，得到出售这种手机的所有商家销售信息
            for each in response.xpath("//div[@id='J_goodsList']//li[@class='gl-item']"):
                item=Phone()
                item['name']=response.url.split("keyword=")[1].split("&")[0]
                item['name']=parse.unquote(item['name'])
                item['price']=each.xpath(".//div[@class='p-price']//i/text()").extract_first()
                item['gross']=each.xpath(".//div[@class='p-commit']//strong//a/text()").extract_first()
                item['seller']=each.xpath(".//div[@class='p-shop']//a/text()").extract_first()
                if item['name']:
                    yield (item)



class TbStartSpider(scrapy.spiders.Spider):
    name="tbStart"
    allowed_domains = ["tmall.com"]
    start_urls = ["https://www.tmall.com/"]

    def start_requests(self):
    #天猫的核心爬虫部分实现不在这儿，这儿主要是控制开始爬取，然后爬完之后对数据的保存
        result=get_phone_list()
        file=open("record.txt",mode="w",encoding="utf-8")
        file.write(str(JustMark.records))
        file.close()
        for each in result:
            item=Phone()
            item['name']=each['name']
            item['gross']=each['gross']
            item['seller']=each['seller']
            item['price']=each['price']
            file=open('tb.json', "a+", encoding="utf-8")
            dict_item = dict(item)    
            json_str = json.dumps(dict_item, ensure_ascii=False) + "\n"    
            file.write(json_str)    
        file.close()
