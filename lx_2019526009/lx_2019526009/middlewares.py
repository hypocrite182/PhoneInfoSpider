from scrapy import signals
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


class JavaScriptMiddleware(object):
    def process_request(self, request, spider):
        if "search.jd.com" in request.url :
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_experimental_option("prefs", {"profile.mamaged_default_content_settings.images": 2})
            self.driver = webdriver.Chrome(chrome_options=chrome_options)
            self.driver.get(request.url)
            html = self.driver.page_source
            self.driver.quit()
            return scrapy.http.HtmlResponse(url=request.url, body=html.encode('utf-8'), encoding='utf-8',request=request)
