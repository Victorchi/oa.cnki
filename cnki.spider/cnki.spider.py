# -*- coding: utf-8 -*-
# auhtor by:Victor chi

import xlrd
import xlwt
import requests
import lxml.html as html
import datetime
import re


def read_excel(path):
    _list = []
    xlrd.Book.encoding = "utf8"  # 设置编码
    data = xlrd.open_workbook(path)
    table = data.sheet_by_index(0)  # 取第一张工作簿
    rows_count = table.nrows  # 取总行数
    for row in range(rows_count):
        url = table.cell(row, 0).value  # 取第1行第1列的值
        _list.append(url)
    return _list


def get_year(url):
    print(datetime.datetime.now())
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
    }
    response = requests.get(url, headers=header).text
    print(datetime.datetime.now())
    doc = html.fromstring(response)
    years1 = doc.xpath('//a[@target="issue"]')
    years2 = doc.xpath('//*[@id="yearIssueInfo"]/ul/li/a')
    years3 = doc.xpath('//*[@id="yearIssueInfo"]/ul/li/a')
    # years3 = doc.xpath('//*[@id="drpYear"]/option')
    _year = []
    for years in [years1, years2,years3]:
        if years:
            print(url)
            for year in years:
                year = year.xpath('text()')[0]
                year = re.sub('[^\d]', '', year)
                _year.append(year)
            break
    _year.remove('')
    print(_year)
    try:
        year_max = max(_year)
    except:
        year_max = ''
    try:
        year_min = min(_year)
    except Exception as e:
        print(e)
        year_min = ''
    if year_min == '' and year_max == '':
        return ''
    result = year_max + '-' + year_min
    print(result)
    return url, result


def write_excel(path):
    urls = read_excel(path)
    for url in urls:
        a = get_year(url)
        url = a[0]
        year = a[1]
        result = url + '    ' + year
        # 参数对应 行, 列, 值
        with open('cnki.txt', 'a+') as f:
            f.write(result)


# def write_excel(path):
#     workbook = xlwt.Workbook(encoding='utf-8')
#     worksheet = workbook.add_sheet('My Worksheet')
#     urls = read_excel(path)
#     n = 0
#     for url in urls:
#         a = get_year(url)
#         url =a[0]
#         year = a[1]
#         # 参数对应 行, 列, 值
#         worksheet.write(n, 0, label=url)
#         worksheet.write(n, 1, label=year)
#         n +=1
#     # workbook.save('Excel_test.xls')
if __name__ == '__main__':
    path = r'C:\Users\Administrator\Desktop\CNKI-A.xlsx'
    # write_excel(path)
    url = 'http://oversea.cnki.net/kns55/oldnavi/n_CNKIPub.aspx?naviid=69&Flg=local&BaseID=AQHJ&NaviLink=Initial+Pinyin+of+Title%3aA-%2fkns55%2foldnavi%2fn_list.aspx%3fNaviID%3d48%26Field%3dpy_203%26Flg%3dlocal%26Value%3dA%7cJournal+of+Safety+and+Environment'
    a = get_year(url)
    print(a)