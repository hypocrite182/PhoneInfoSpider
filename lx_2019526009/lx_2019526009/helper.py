from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
import random
import json

class JustMark:
    file=open("record.txt",mode="r",encoding="utf-8")
    try:
        records=int(file.readline())
    except:
        records=0
    file.close()


def get_phone_list():
    count=0
    info=[['xxx','pppp'],["xxxx","ppp"]]
    #两个账号，如果被淘宝抓到了轮流上
    while True:
        index=count%2
        browser=register(info[index][0],info[index][1])
        #这部分是模拟人操作的部分，从tmall网站开始搜索一步步得到所有手机的列表
        result=list()
        browser.get('https://www.tmall.com/')
        search = browser.find_element(By.ID, 'mq')
        button = browser.find_element_by_xpath(".//div//button")
        search.send_keys("手机")
        time.sleep(1*random.random())
        button.click()
        sort=browser.find_element_by_xpath(".//a[@class='fSort'][3]")
        sort.click()

        try:
         data=get_phone_data(browser,result)
         return data
        except:
            browser.close()
            count+=1
            file = open("record.txt", mode="w", encoding="utf-8")
            file.write(str(JustMark.records))
            file.close()
            for each in result:
                dict_item = each   
                json_str = json.dumps(dict_item, ensure_ascii=False) + "\n"   
                file.write(json_str)   
            file.close()
            continue


def register(username,paw): 
    i=260
    #滑块拖动距离
    while True:
        browser = webdriver.ChromeOptions()
        browser.add_experimental_option('excludeSwitches', ['enable-automation'])
        #设置chromedriver开发人员选项，避免被检测大
        browser.add_argument("--start-maximized")
        #最大化窗口，不最大化拖滑块会出问题
        browser = webdriver.Chrome(chrome_options=browser)
        browser.get('https://login.taobao.com/member/login.jhtml')
        input = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'forget-pwd.J_Quick2Static')))  
        input.click()
        user = browser.find_element(By.ID, 'TPL_username_1') 
        password = browser.find_element(By.ID, 'TPL_password_1') 
        user.send_keys(username)  
        time.sleep(random.random() * 1)
        password.send_keys(paw) 
        time.sleep(random.random() * 1)
        #以上是填入用户名和密码
        browser.execute_script("Object.defineProperties(navigator,{webdriver:{get:() => false}})")
        action = ActionChains(browser)
        time.sleep(random.random() * 1)
        butt = browser.find_element(By.ID, 'nc_1_n1z')
        browser.switch_to.frame(browser.find_element(By.ID, '_oid_ifr_'))
        browser.switch_to.default_content()
        action.click_and_hold(butt).perform()
        action.reset_actions()
        action.move_by_offset(i, 0).perform() 
        action.release()
        #以上是滑块拖动部分
        button = browser.find_element(By.ID, 'J_SubmitStatic') 
        time.sleep(random.random() * 2)
        button.click()
        #提交登录
        cookie = browser.get_cookies()
        #获得cookie，据网上所说，如果登录成功，获取的cookie会大于10个
        list = {} 
        for cookiez in cookie:
            name = cookiez['name']
            value = cookiez['value']
            list[name] = value
        if len(list) > 10:
            break
        else:
            browser.close()
    return browser


def get_phone_data(browser,result):
    #这个方法是已经到了相关商品的所有商家销售信息，直接开始爬
    hrefs=list()
    names=list()
    for each in browser.find_elements_by_xpath(".//a[@class='productShop-num']"):
        hrefs.append(each.get_attribute("href"))
    #获取各种手机的所有商家销售信息链接
    for each in browser.find_elements_by_xpath("//div[@class='productTitle productTitle-spu']/a[1]"):
        names.append(each.get_attribute("text"))
    #获取各种手机型号名
    i=JustMark.records
    #读取断点，看上次爬到哪儿了
    while i < len(hrefs):
        browser.get(hrefs[i])
        time.sleep(1*random.random())
        sort = browser.find_element_by_xpath(".//a[@class='fSort'][2]")
        sort.click()
        for page in range(5):
        #每种商品所有商家销售按销量排序后爬5页即可了，到后面基本上没人买
            try:
                for each in browser.find_elements_by_xpath(".//div[@class='product ']|//div[@class='product  productFirst ']"):
                    result.append({"name":names[i],"gross":each.find_element_by_xpath(".//div[@class='productComment']//em").text,"price":each.find_element_by_xpath(".//p[@class='proSell-price']").text,"seller":each.find_element_by_xpath(".//p[@class='proInfo-seller']/a").text})
                next_page=browser.find_element_by_xpath(".//a[@class='ui-page-next']")
                next_page.click()
            except Exception as e:
                #如果下一页不存在，就直接跳出当前循环从下一种手机开始
                break
            time.sleep(4*random.random())
        time.sleep(10*random.random())
        JustMark.records+=1
        i+=1
        if i%3==0:
            time.sleep(15)
        #每爬了3种商品后，等待15秒，玄学检测
    return result


