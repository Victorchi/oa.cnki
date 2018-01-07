# coding:utf8
# Author:Victor Chi
import smtplib
import time
from email.header import Header
from email.mime.text import MIMEText

import pytesseract
import requests
from PIL import Image
from selenium import webdriver
# tessdata 训练集的位置
tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'


def getimg(url):
    # 获取图片
    response = requests.get(url)
    with open('pic.jpg', 'wb') as f:
        f.write(response.content)
#
def OpenChrome(user,pwd,mail):
    url = 'http://oa.cnki.net/Login.aspx?ReturnUrl=%2f'
    driver = webdriver.Chrome()

    driver.get(url)
    driver.maximize_window()
    driver.find_element_by_xpath('//*[@id="UserName"]').send_keys(user) # 填写用户名
    driver.find_element_by_xpath('//*[@id="PassWord"]').send_keys(pwd) # 填写密码
    for link in driver.find_elements_by_xpath('//*[@id="FormShield1"]'):
        url = link.get_attribute('src')
        getimg(url)
    time.sleep(1)
    # 识别验证码
    verify = pytesseract.image_to_string(Image.open('./pic.jpg'),config=tessdata_dir_config)
    driver.find_element_by_xpath('//*[@id="CheckCode"]').send_keys(verify)
    time.sleep(4)
    driver.find_element_by_xpath('//*[@id="slogin"]/ul/li[1]/a').click()# 登陆
    time.sleep(1)
    try:
        # 获取考勤的状态,时间
        driver.get('http://oa.cnki.net/TTKN/PersonManage/KQMessageList.aspx')
        status = driver.find_elements_by_xpath('//*[@id="repeaterData_ctl01_Label7"]')[0].text
        _date = driver.find_elements_by_xpath('//*[@id="TableData"]/tbody/tr[2]/td[6]')[0].text
        if status == '全勤':
            text = '{}你忘记打卡啦,\nOA显示{},\n赶快提交忘打卡记录吧'.format(_date,status)
            send_email(text,mail)

    except Exception as e:
        print(e)
        driver.close()
        return False


    # for kaoqin in driver.find_elements_by_xpath('//*[@id="TreeView1_item_148_cell"]/nobr'):
    #     kaoqin = kaoqin.get_property('nobr')
    #     print(kaoqin)
    # return 1
    return True
def run(user,pwd,mail):

    if OpenChrome(user,pwd,mail) == False:
        run(user,pwd,mail)
    else:
        return '1'

def send_email(text,mail):

    # 第三方 SMTP 服务
    mail_host = "smtp.163.com"  # 设置服务器
    mail_user = "xxx"  # 用户名
    mail_pass = "xxx"  # 口令

    sender = 'xxx'
    receivers = [mail]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEText(text, 'plain', 'utf-8')
    message['From'] = Header(mail, 'utf-8')
    message['To'] = Header(mail, 'utf-8')

    subject = 'OA平台忘打卡提醒'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")

    except Exception as e:
        print(e)
        print ("Error: 无法发送邮件")


if __name__ == '__main__':
    user = [{'user':'xxx','pwd':'xxx','mail':'xxx'}]
    for i in user:
       run(i.get('user'),i.get('pwd'),i.get('mail'))

    # run(user)
    pass





