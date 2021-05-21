# coding=utf-8
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import xlwt

# browser = webdriver.PhantomJS()
# 获取浏览器对象
browser = webdriver.Chrome()
# 显示等待：WebDriverWait(浏览器对象, 最长超时时间)，针对于某个特定的元素设置的等待时间
WAIT = WebDriverWait(browser, 10)
# 设置浏览器显示窗口大小
browser.set_window_size(1400, 900)
# 创建工作簿对象
book = xlwt.Workbook(encoding='utf-8', style_compression=0)
# 在工作簿中创建工作表，cell_overwrite_ok=True写入多次
sheet = book.add_sheet('蔡徐坤篮球', cell_overwrite_ok=True)
# 写入工作表，行数，列数，标签
sheet.write(0, 0, '名称')
sheet.write(0, 1, '地址')
sheet.write(0, 2, '描述')
sheet.write(0, 3, '观看次数')
sheet.write(0, 4, '弹幕数')
sheet.write(0, 5, '发布时间')

n = 1


def search():
    try:
        print('开始访问b站....')
        # 访问哔哩哔哩
        browser.get("https://www.bilibili.com/")

        # 被那个破登录遮住了
        # index = WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#primary_menu > ul > li.home > a")))
        # index.click()

        # 获取到b站首页的输入框和搜索按钮
        # WAIT.until(self,method,message)
        # method：在等待期间，每隔一段时间（__init__中的poll_frequency）调用这个传入的方法，直到返回值不是False
        # message: 如果超时，抛出TimeoutException，将message传入异常
        # WebDriverWait(driver, 超时时长, 调用频率, 忽略异常).until(可执行方法, 超时时返回的信息)

        # EC.presence_of_element_located，页面元素等待处理。显性等待
        # 判断某个元素是否被加到了dom树里，并不代表该元素一定可见，如果定位到就返回WebElement

        # By.CSS_SELECTOR，通过css选择器
        # (#)表示通过  id 属性来定位元素
        # (.)表示通过 class属性来定位元素
        # nav_searchform > input，选择id为nav_searchform的input元素
        input = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#nav_searchform > input")))

        # 判断某个元素中是否可见并且是enable的，代表可点击
        submit = WAIT.until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div[2]/div/div[1]/div[1]/div/div[2]/div/form/div/button')))

        # 输入搜索内容
        input.send_keys('蔡徐坤 篮球')
        submit.click()

        # 跳转到新的窗口
        print('跳转到新窗口')
        # 窗口句柄
        all_h = browser.window_handles
        # 切换到窗口1
        browser.switch_to.window(all_h[1])
        get_source()

        # 获取到总页数
        # 判断某个元素是否被加到了dom树里，并不代表该元素一定可见，如果定位到就返回WebElement
        total = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                           "#all-list > div.flow-loader > div.page-wrap > div > ul > li.page-item.last > button")))
        return int(total.text)
    except TimeoutException:
        return search()


def next_page(page_num):
    try:
        print('获取下一页数据')
        # 判断某个元素中是否可见并且是enable的，代表可点击
        next_btn = WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                          '#all-list > div.flow-loader > div.page-wrap > div > ul > li.page-item.next > button')))
        next_btn.click()
        # 判断指定的元素中是否包含了预期的字符串，返回布尔值
        WAIT.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,
                                                     '#all-list > div.flow-loader > div.page-wrap > div > ul > li.page-item.active > button'),
                                                    str(page_num)))
        get_source()
    except TimeoutException:
        browser.refresh()
        return next_page(page_num)

# 解析爬取
def save_to_excel(soup):
    list = soup.find(class_='video-list clearfix').find_all(class_='video-item matrix')

    for item in list:
        item_title = item.find('a').get('title')
        item_link = item.find('a').get('href')
        item_dec = item.find(class_='des hide').text
        item_view = item.find(class_='so-icon watch-num').text
        item_biubiu = item.find(class_='so-icon hide').text
        item_date = item.find(class_='so-icon time').text

        print('爬取：' + item_title)

        global n

        sheet.write(n, 0, item_title)
        sheet.write(n, 1, item_link)
        sheet.write(n, 2, item_dec)
        sheet.write(n, 3, item_view)
        sheet.write(n, 4, item_biubiu)
        sheet.write(n, 5, item_date)

        n = n + 1


def get_source():
    # 判断某个元素是否被加到了dom树里，并不代表该元素一定可见，如果定位到就返回WebElement
    WAIT.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '#all-list > div.flow-loader > div.filter-wrap')))
    # 获得网页源码
    html = browser.page_source
    # 解析源码
    soup = BeautifulSoup(html, 'html.parser')
    print('到这')

    save_to_excel(soup)


def main():
    try:
        total = search()
        print(total)

        for i in range(2, int(total + 1)):
            next_page(i)

    finally:
        browser.close()


if __name__ == '__main__':
    main()
    book.save('蔡徐坤篮球.xlsx')