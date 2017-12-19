# coding:utf8
# Author:Victor Chi
import PIL
from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFilter
import sys
from selenium import webdriver
import requests
import time
from lxml import etree
import lxml.html as html
import pytesseract

url = 'http://oa.cnki.net/Login.aspx?ReturnUrl=%2f'


def getimg(url):
    response = requests.get(url)
    with open('pic.jpg', 'wb') as f:
        f.write(response.content)
    # text = image_to_string(pic.jpg)

# a = pytesseract.image_to_string(Image.open('./pic.jpg'))
# print(a)
driver = webdriver.Chrome()
driver.get(url)
driver.maximize_window()
driver.find_element_by_xpath('//*[@id="UserName"]').send_keys('CLF10429')
driver.find_element_by_xpath('//*[@id="PassWord"]').send_keys('CLF937918')
for link in driver.find_elements_by_xpath('//*[@id="FormShield1"]'):
    url = link.get_attribute('src')
    getimg(url)
a = pytesseract.image_to_string(Image.open('./pic.jpg'))
print(a)
# driver.find_element_by_xpath('//*[@id="CheckCode"]').send_keys('6y7f')
# driver.find_element_by_xpath('//*[@id="slogin"]/ul/li[1]/a').click()
time.sleep(2)
