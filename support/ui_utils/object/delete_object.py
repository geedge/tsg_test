import random
import time
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.object_element_position import *
from datetime import datetime 

class DeleteObject:
    def __init__(self, driver):
        self.driver = driver
        
    def delete(self, object_element_position, first_row_checkbox_element, is_del_all):
        delete_element_position = object_element_position["delete"]
        try:
            time.sleep(0.5)
            if is_del_all == True:
                self.driver.find_element(By.XPATH, delete_element_position["objectListPage_allSelect_posXpath"]).click()
                rows = self.driver.find_element(By.XPATH, objectListPage_tableTbody_posXpath).find_elements(By.XPATH, "./div")
                self.select_lock_and_referenceCount(rows)
            else:
                first_row_checkbox_element.click()
            self.driver.find_element(By.XPATH, delete_element_position["objectListPage_deleteButton_posXpath"]).click()
            self.driver.find_element(By.XPATH, delete_element_position["objectListPage_deleteButton_warningYes_posXpath"]).click()
            time.sleep(3)
            return 200
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}", flush=True)
            raise
            #return 400

    def select_lock_and_referenceCount(self, rows, islock=False, referenceCount=0):
        """
        筛选点击是 否有锁、引用数是否为0的数据，默认选择列表列中无锁且引用为0的数据。
        :param rows:   查询的所有行数据， 例如：self.driver.find_element(By.XPATH, listPage_profilTable_dnsRecords_tableTbody_posXpath).find_elements(By.XPATH, "./tr")
        :param lock: False True
        :param referenceCount: 0， 1
        :return:  0 表示有删除对象， 1表示没有删除对象
        """
        return_code = 1
        try:
            for row_item in rows:
                # 查找元素是引用是否不为0,因为已经全选，不为0的点击取消选择//*[@class='MuiDataGrid-virtualScrollerRenderZone css-1inm7gi']/div/div[@data-field='reference_count']
                el_td_list = row_item.find_elements(By.XPATH, "./div[@data-field='reference_count']//button")
                for el_td_item in el_td_list:
                    test = el_td_item.text
                    if test != '0':
                        el_td_item.find_element(By.XPATH, "./parent::*/parent::*").click()
                        break

            return return_code
        except Exception as e:
            raise