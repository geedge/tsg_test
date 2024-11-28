import random
import time
import traceback
from support.ui_utils.element_position.profile_element_position import *
from selenium.webdriver.common.by import By
from datetime import datetime 

class DeleteProfiles:
    def __init__(self, driver):
        self.driver = driver
        
    def delete_profiles(self, profiles_tuple):
        profile_element_position = {}
        first_row_checkbox_element = {}
        is_del_all = False
        delete_element_position = profile_element_position["delete"]
        try:
            if is_del_all == True:
                element = self.driver.find_element(By.XPATH, mainPage_profileBottomPage_button_allSelect_posXpath).click()
                #self.driver.find_element(By.XPATH, delete_element_position["profileListPage_allSelect_posXpath"]).click()   #遇到无reference count在优化
                rows = self.driver.find_element(By.XPATH, listPage_profilTable_dnsRecords_tableTbody_posXpath).find_elements(By.XPATH, "./tr")
                self.select_lock_and_referenceCount(rows)

            else:
                first_row_checkbox_element.click()
            self.driver.find_element(By.XPATH, delete_element_position["profileListPage_deleteButton_posXpath"]).click()
            time.sleep(0.5)
            self.driver.find_element(By.XPATH, delete_element_position["profileListPage_deleteButton_warningYes_posXpath"]).click()
            time.sleep(2)
            return 200
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}", flush=True)
            #self.driver.find_element(By.XPATH, delete_element_position["profileListPage_deleteButton_warningYes_posXpath"]).click()
            time.sleep(0.5)
            raise
            #return 200

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
                # 查找元素是引用是否不为0,因为已经全选，不为0的点击取消选择//div[@class='MuiDataGrid-virtualScrollerRenderZone css-1inm7gi']/div/div[@data-field='referenced_by']/button/parent::*/parent::*
                el_td_list = row_item.find_elements(By.XPATH, "./div[@data-field='referenced_by']//button")
                for el_td_item in el_td_list:
                    test = el_td_item.text
                    if test != '0':
                        el_td_item.find_elements(By.XPATH, "./parent::*/parent::*").click()
                        break

            return return_code
        except Exception as e:
            raise