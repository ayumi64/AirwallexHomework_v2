# -*- coding: utf-8 -*-
# @Time    : 2021/10/15 11:53 上午
# @Author  : yuhang
# @Site    :
# @File    : test_api_all.py

import os
import json
import pytest
import allure
from common.common_method import *

url_ = 'https://api-demo.airwallex.com'
filepath = r'./testdata/reg.xls'

class TestDemo():
    @allure.severity("minor")
    @allure.feature("接口测试")
    @allure.story('Test') 
    @pytest.mark.parametrize(
        "test_data",
        commonMethod().read_excle(filepath))

    def test_beneficiary(self, test_data):
        '''Airwallex接口自动化测试----Test''' 
        try:
            excleRow = test_data['rowIndex']  
            # 报告中用来记录测试步骤
            with allure.step('开始发起请求：'+"{0}: {1}".format(str(test_data['method']), test_data['url'])):
                url = url_ + test_data['url']
                Auth = commonMethod().Auth()
                headers = {"Content-Type": "application/json",
                            "Authorization": "Bearer " + Auth
                }

                response = commonMethod().post_invoke(url, test_data['params'].encode('utf-8'), headers)
        
                res_body = response.content.decode()
                res_code = response.status_code
                res = json.loads(res_body)
                commonMethod().write_excle(filepath, excleRow, 7, res_code)
                commonMethod().write_excle(filepath, excleRow, 8, res_body)

                with allure.step('返回消息'+str(res)):
                    allure.attach('返回消息', str(res),
                                    allure.attachment_type.TEXT)
                jsonPathList = test_data['result_key'].split(
                    '.')

                # 根据JsonPath处理Excel期待结果
                for jsonPath in jsonPathList:
                    if isinstance(res, list) and (jsonPath.isdigit() == False):
                        res = res[0]
                    elif jsonPath.isdigit():
                        res = res[int(jsonPath)]
                    else:
                        res = res[jsonPath]
                
                # 断言并将结果写入Excel
                issuccess = 'Failed'
                if res == test_data['except']:
                    issuccess = 'Success'
                commonMethod().write_excle(filepath, excleRow, 9, issuccess)
                assert res == test_data['except'] 
        
        except KeyError as e:
            commonMethod().write_excle(filepath, excleRow, 9, "Exception")
            pytest.fail("测试失败退出！") 
            pytest.xfail(str(e))


if __name__ == '__main__':
    os.system(
        'pytest -s ./test_api_all.py::TestDemo::test_ --alluredir report/result')
    os.system('allure generate report/result -o report/allure_html --clean')
