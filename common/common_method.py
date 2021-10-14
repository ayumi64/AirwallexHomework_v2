# -*- coding: utf-8 -*-
# @Time    : 2021/10/15 11:53 上午
# @Author  : yuhang
# @Site    :
# @File    : common_method.py

import ssl
import xlrd, json
from xlutils.copy import copy
import requests

# 证书问题 # 禁用安全请求警告
ssl._create_default_https_context = ssl._create_unverified_context

url_ = 'https://api-demo.airwallex.com'

class commonMethod():

    # 获取Auth

    def Auth(self):
        url = url_ + '/api/v1/authentication/login'
        headers = {'Content-Type': 'application/json',
                    'x-api-key': '2308e2dd300f6b959b7f4e0a52ba9181186fc92f075f7e64ee9fa0b6b1ada094c39c9a9f39f06693d06b17067f78d4e7',
                    'x-client-id': 'KJbr_Xs5TLmhY03JWSi3NQ'
                    }
        json_ = '{}'      
        res = self.post_invoke(url=url, headers=headers, data=json_)
        res = json.loads(res.content.decode())
        return res['token']

    def post_invoke(self, url, data, headers=None):
        res = None
        if headers == None:
            res = requests.post(url=url, data=data)
        else:
            res = requests.post(url=url, data=data, headers=headers)
        return res

    def get_invoke(self, url, data, headers=None):
        res = None
        if headers == None:
            res = requests.get(url=url, data=data)
        else:
            res = requests.get(url=url, data=data, headers=headers)
        return res


    # 读取excle文件转换成json列表
    def read_excle(self, path):
        final_list = []
        rb = xlrd.open_workbook(path)  # 打开文件
        # print(wb.sheet_names())#获取所有表格名字
        sheet1 = rb.sheet_by_index(0)  # 通过索引获取表格 tab
        wb = copy(rb)
        wbsheet1 = wb.get_sheet(0)
        ncols = sheet1.ncols  #列
        nrows = sheet1.nrows  #行
        #把excle转换成json列表
        for i in range(1, nrows):
            object_json = {'rowIndex':i}
            for a in range(ncols):
                object_json[sheet1.row_values(0)[a]] = sheet1.row_values(i)[a]
            final_list.append(object_json)
        return final_list

    # 写excle##
    def write_excle(self, path, row, col, meassage):
        rb = xlrd.open_workbook(path)  # 打开文件
        wb = copy(rb)
        wbsheet1 = wb.get_sheet(0)
        wbsheet1.write(row, col, meassage)
        wb.save(path)

if __name__ == '__main__':
    print(commonMethod().Auth2())

