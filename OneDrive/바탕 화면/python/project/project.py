# selenium은 webdriver api를 통해 브라우저를 제어한다.
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import calendar
import time

outfile = open("information.txt", "w")
driver = webdriver.Chrome('c:\project\chromedriver')
driver.implicitly_wait(3)

crawl_url = 'http://fly.interpark.com'
dep = input("출발지를 입력하세요")
arr = input("도착지를 입력하세요")

#출발, 도착 div id값
dep_name = 'dep_name'
arr_name = 'arr_name'

# 사이트 접속
driver.get(crawl_url)

def setting_crawl(name, location, number):
    #편도 클릭
    driver.find_element_by_class_name('oneWay-trip').click()

    #출발, 도착지 입력
    driver.find_element_by_id(name).clear()
    driver.find_element_by_id(name).send_keys(location)
    driver.find_element_by_id(name).click()
    driver.find_element_by_id(name).send_keys(Keys.ENTER)

    if(number == 1):
        #날짜 선택
        driver.find_element_by_xpath('//*[@id="searchForm"]/div[3]/button').click()
        driver.find_element_by_xpath('//*[@id="dd06_0"]/a').click()
        driver.find_element_by_xpath('//*[@id="cal"]/div/div[2]/a[1]').click()

def output(data):
    s_data = data.splitlines()
    html = str(datetime.today().month) + '/' + str(currentday)
    for c in s_data:
            if c !="":
                html = html+" "+c
    print(html)
    outfile.write(html+'\n')
                
def search_crawl(currntday, count):
    if(count == 0):
        #첫 번째 검색
        driver.find_element_by_xpath('//*[@id="searchButton"]/span').click()
        time.sleep(3)
    
        #오름차순 정렬
        driver.find_element_by_xpath('//*[@id="lowPriceCol"]').click()
        data = driver.find_element_by_xpath('//*[@id="schedule0List"]/li[1]').text

        return data

    if(count == 1):
        #날짜 다시 설정
        driver.find_element_by_xpath('//*[@id="dBodyContent"]/div[1]/div[1]/div/table/tbody/tr/td/div[2]/button').click()
        driver.find_element_by_xpath('//*[@id="dBodyContent"]/div[1]/div[3]/div/div[2]/div/div[3]/button').click()
        if(currentday < 10):
            driver.find_element_by_xpath('//*[@id="dd0'+str(currentday)+'_0"]/a').click()
        elif(currentday >= 10 and currentday <= final_day):
            driver.find_element_by_xpath('//*[@id="dd'+str(currentday)+'_0"]/a').click()

        driver.find_element_by_xpath('//*[@id="cal"]/div/div[2]/a[1]').click()
        # 재검색
        driver.find_element_by_xpath('//*[@id="dBodyContent"]/div[1]/div[3]/div/div[2]/div/div[7]/button/span').click()
        time.sleep(3)
        
        #오름차순 정렬
        driver.find_element_by_xpath('//*[@id="lowPriceCol"]').click()
        data = driver.find_element_by_xpath('//*[@id="schedule0List"]/li[1]').text

        return data
    
flag = 0
first = 0
after = 1
today = datetime.today().day
final_day = 8
final_day = calendar.monthrange(datetime.today().year, datetime.today().month)[1]
currentday = today + 1

while(1):
    if(flag == 0):
        setting_crawl(dep_name, dep, 0)
        setting_crawl(arr_name, arr, 1)
        output(search_crawl(currentday, first))
        flag += 1
        currentday += 1
        
    elif(flag == 1 and currentday <= final_day):
        output(search_crawl(currentday, after))
        currentday += 1
    else:
        driver.close()
        break
                
outfile.close()
