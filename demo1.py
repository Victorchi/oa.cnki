#coding:utf8
#Author:Victor Chi
from selenium import webdriver
import requests
import time
driver = webdriver.Chrome()
driver.get('http://oa.cnki.net/Login.aspx?ReturnUrl=%2f')
driver.maximize_window()
driver.find_element_by_xpath('//*[@id="UserName"]').send_keys('CLF10429')
driver.find_element_by_xpath('//*[@id="PassWord"]').send_keys('CLF937918')
driver.find_element_by_xpath('//*[@id="CheckCode"]').send_keys('6y7f')
driver.find_element_by_xpath('//*[@id="slogin"]/ul/li[1]/a').click()
time.sleep(2)
