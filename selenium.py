# 导入web驱动
from selenium import webdriver
# 创建chrome驱动
driver = webdriver.Chrome()
# 打开百度
driver.get("https://www.baidu.com")
input=driver.find_element_by_css_selector('#kw')
input.send_keys("照片")
button=driver.find_element_by_css_selector('#su')
button.click()
# ID = "id"
# XPATH = "xpath"
# LINK_TEXT = "link text"
# PARTIAL_LINK_TEXT = "partial link text"
# NAME = "name"
# TAG_NAME = "tag name"
# CLASS_NAME = "class name"
# CSS_SELECTOR = "css selector"