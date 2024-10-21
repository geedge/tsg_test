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
                rows = self.driver.find_element(By.XPATH, ipObjectListPage_tableTbody_posXpath).find_elements(By.XPATH, "./tr")
                self.select_lock_and_referenceCount(rows)
            else:
                first_row_checkbox_element.click()
                self.driver.find_element(By.XPATH, delete_element_position["objectListPage_deleteButton_posId"]).click()
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
        try:
            referenceCount = (referenceCount)
            return_code = 1
            for row_item in rows:  # 每一行操作
                el_td_1 = row_item.find_element(By.XPATH, "./td[1]")
                # 获取第一列元素下所有的属性
                child_class_list = []
                el_child_list = el_td_1.find_elements(By.XPATH, ".//*")
                for el_child_item in el_child_list:
                    # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], el_child_item.get_attribute("class"))
                    child_class_list.append(el_child_item.get_attribute("class"))
                # 如果没有 icon-lock 属性，则需要点击选择框
                child_class_list = list(set(child_class_list))  # 去重
                lock_flag = 0   # 没有锁
                refer_count = 0  # 引用为0
                click_flag = 0   # 0不点击、1点击
                for _ in child_class_list:  # 校验所有的class 中是否有 该属性
                    if "icon-lock" in _:
                        lock_flag = 1  # 有锁 则变成1
                        break
                        # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], child_class_list)
                # 再次查找元素是引用是否不为0
                el_td_list = row_item.find_elements(By.XPATH, "./td")  # 每一列操作
                # 判断一下，是否存在 Reference Count 列，如果存在，则需要进一步操作
                for el_td_item in el_td_list:
                    td_item_id_list = []  # 每一列存放id的属性
                    td_item_childs = el_td_item.find_elements(By.XPATH, ".//*")
                    for td_child in td_item_childs:
                        td_item_id_list.append(td_child.get_attribute("id"))
                    td_item_id_list = list(set(td_item_id_list))  # 去重
                    #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], td_item_id_list)
                    refer_except = "objectReferenceData"  # objectReferenceData3738465-_Objects_ip_Home_App_anonymousComponent  id中存在预期值即可
                    for td_id_item in td_item_id_list:
                        if refer_except in td_id_item:  # 存在这个部分id属性即可
                            refer_counter_actual = el_td_item.find_element(By.XPATH, f".//*[@id='{td_id_item}']").text.strip()
                            #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], td_id_item, ">>>", refer_counter_actual)
                            if refer_counter_actual != "0":    #
                                refer_count = 1  # 引用数不为 0

                # lock=False, referenceCount=0  # 传入参数和实际判断参数对比，确认是否点击
                if islock == False:   # 选择没有锁的
                    if referenceCount == 0:   # 选择引用为0的
                        if lock_flag == 0 and refer_count == 0:
                            click_flag = 1
                    else:    # 选择引用不为0的
                        if lock_flag == 0 and refer_count == 1:
                            click_flag = 1
                else:    # 选择有锁的
                    if referenceCount == 0:  # 选择引用为0的
                        if lock_flag == 1 and refer_count == 0:
                            click_flag = 1
                    else:  # 选择引用不为0的
                        if lock_flag == 1 and refer_count == 1:
                            click_flag = 1

                if click_flag == 1:  # 没有 icon-lock  引用为0，， 需要点击
                    el_td_1.find_element(By.XPATH, ".//*[@class='el-checkbox__input']").click()
                    return_code = 0
                    time.sleep(0.1)
            return return_code
        except Exception as e:
            raise