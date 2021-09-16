import csv
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Chrome()
WAIT = WebDriverWait(driver, 10)
driver.get("https://www.bilibili.com/video/BV1Sq4y1N7ng")
driver.execute_script("window.scrollTo(0,document.body.scrollHeight/2)")
time.sleep(3)
index = WAIT.until(EC.presence_of_element_located((By.LINK_TEXT, '点击查看')))
index.click()
time.sleep(3)

soup = BeautifulSoup(driver.page_source, 'lxml')

totel = soup.find("span", {"class": "result"}).text
print(totel[1:-1])
page = int(totel[1:-1])
next = driver.find_element_by_xpath("//a[contains(text(),'下一页')]")
f = open('text.csv', 'w', encoding='utf-8')
csv_writer = csv.writer(f)
for i in range(0, page - 1):
    soup = BeautifulSoup(driver.page_source, 'lxml')
    html = soup.find("div", {"class": "list-item reply-wrap is-top"}).findAll("div", {"class": "reply-con"})
    time.sleep(1)
    for item in html:
        name = item.find("a").string
        comm = item.find("span").text
        csv_writer.writerow([name, comm])
        print(name + "--" + comm)
        time.sleep(1)
    driver.execute_script("arguments[0].click();", next)
    time.sleep(2)
    try:
        next = driver.find_element_by_xpath("//a[contains(text(),'下一页')]")
    except:
        break
