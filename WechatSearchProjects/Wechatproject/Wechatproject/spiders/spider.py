#coding: utf-8
import scrapy
from scrapy.selector import Selector
from Wechatproject.items import WechatprojectItem
from bs4 import BeautifulSoup
from scrapy.http import Request


class WechatSpider(scrapy.Spider):
    #############################################################################################
    '''微信搜索程序'''
    name = 'spider'

    start_urls = ['http://weixin.sogou.com/weixin?type=2&query=goodboy&page=7']
    querystring = 'goodboy'
    type = 2 # 2-文章，1-微信号
    # for i in range(1, 50, 1):
    #     start_urls.append('http://weixin.sogou.com/weixin?type=%d&query=%s&page=%d' % (type, querystring, i))
    # print start_urls

    # def start_requests(self):
    #     print('shuai start request')
    #     hostname = 'http://weixin.sogou.com'
    #     yield Request(url=hostname, meta={'cookiejar':1}, callback=self.getcookie, dont_filter=True)
    #     pass
    #
    # def getcookie(self, response):
    #     yield Request(url=self.start_urls[0], meta={'cookiejar':response.meta['cookiejar']}, callback=self.parse, dont_filter=True)
    #     pass

    #############################################################################################
    ## 递归抓取

    ## 使用xpath()方法，注意item中键对值为string类型，extract()方法返回list
    def parse(self, response):
        print('shuai: start parse00 is: ' + response.url)
        # print response.body
        sel = Selector(response)
        sites = sel.xpath('//div[@class="txt-box"]/h3/a')
        # for site in sites:
        #     item = WechatprojectItem()
        #     item['title'] = site.xpath("text()").extract() # 其中在item.py中定义了title = Field()
        #     item["link"] = site.xpath("@href").extract() # 其中在item.py中定义了link = Field()
        #     #############################################################################################
        #     # yield item ## 只抓取当前页数据
        #     next_url = item["link"][0]
        #     print('start open wechat title' + item['title'][0])
        #     print('start open wechat link' + item['link'][0])
        #     # yield Request(url=next_url, callback=self.parse2) ## 只抓取二级页面数据
        #     yield Request(url=next_url, meta={"item":item, 'cookiejar':response.meta['cookiejar']}, callback=self.parse2, dont_filter=True) ## 抓取当前页数和二级页面数据

        item = WechatprojectItem()
        item['title'] = sites[7].xpath("descendant::text()").extract()  # 其中在item.py中定义了title = Field()
        item["link"] = sites[7].xpath("@href").extract()  # 其中在item.py中定义了link = Field()
    #############################################################################################
    # yield item ## 只抓取当前页数据
        item["link"] = item["link"][0]
        item['title'] = "".join(item['title'])
        print('start open wechat title is: ' + item['title'])
        print('start open wechat link is: ' + item['link'])
    # yield Request(url=next_url, callback=self.parse2) ## 只抓取二级页面数据
        yield Request(url=item["link"], meta={"item": item}, callback=self.parse2,dont_filter=True)  ## 抓取当前页数和二级页面数据

    # ## 使用BeautifulSoup方法，注意item中键对值为string类型
    # def parse(self, response):
    #     # print response.body
    #     soup = BeautifulSoup(response.body, 'lxml')
    #     tags = soup.findAll("h4")
    #     for tag in tags:
    #         item = WechatprojectItem()
    #         item['title'] = tag.text # 其中在item.py中定义了title = Field()
    #         item['link'] = tag.find("a").get("href") # 其中在item.py中定义了link = Field()
    #         #############################################################################################
    #         # yield item ## 只抓取当前页数据
    #         next_url = item["link"]
    #         # yield Request(url=next_url, callback=self.parse2) ## 只抓取二级页面数据
    #         yield Request(url=next_url, meta={"item":item}, callback=self.parse2, dont_filter=True) ## 抓取当前页数和二级页面数据

    def parse2(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        tag = soup.find("div", attrs={"class":"rich_media_content", "id":"js_content"}) # 提取第一个标签
        content_list = [tag_i.text for tag_i in tag.findAll("p")]
        content = "".join(content_list)
        print('wechat content is: ' + content)
        # item = WechatprojectItem() ## 只抓取二级页面数据
        item = response.meta['item'] ## 抓取当前页数和二级页面数据
        item['content'] = content
        return item
