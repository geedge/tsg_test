import configparser
import os
import sys
import time
from datetime import datetime
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from support.general_ui_utils.element_position.object_element_position import *
from support.general_ui_utils.object.search_objects import SearchObjects
from support.general_ui_utils.object.page_jump import PageJump
from selenium.webdriver.support import expected_conditions as EC
from support.ui_utils.random_name import *




class DifferentVsysObjectCheck():

    def __init__(self,driver):
        self.driver = driver
        self.vsys_zero_object ={}
        self.vsys_two_object = {}

    def different_vsys_object_check(self,first_object_info,second_object_info,test_data,object_element_position):
        try:
            self.vsys_zero_object = second_object_info
            self.vsys_two_object = first_object_info
            search_object = SearchObjects(self.driver)
            page_jump = PageJump(self.driver)
            search_object.search(first_object_info, test_data,object_element_position)
            self.view_check("vsys0")
            page_jump.change_vsys(vsys_name="PerformanceTestVsys")
            search_object.search(first_object_info, test_data, object_element_position)
            self.view_check("PerformanceTestVsys")
            page_jump.change_vsys(vsys_name="UIAutoTestVsys")
            search_object.search(first_object_info, test_data, object_element_position)
            self.view_check("UIAutoTestVsys")
            page_jump.change_vsys(vsys_name="vsys0")
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}",file=sys.stderr, flush=True)
            return 400


    def view_check(self,vsys_name):
        time.sleep(1)
        total = self.driver.find_element(By.XPATH,"//div[@class='page-box-containcheck']//span[contains(text(),'Total')]").text
        count = total.split("Total:")
        if vsys_name == "PerformanceTestVsys":
            assert int(count[1]) == 1
            assert self.driver.find_element(By.XPATH,listPage_First_object_ID_posXpath).text == self.vsys_zero_object["id"]
        elif vsys_name =="vsys0":
            assert int(count[1]) == 2
            assert self.driver.find_element(By.XPATH,listPage_First_object_ID_posXpath).text == self.vsys_zero_object["id"]
            assert self.driver.find_element(By.XPATH,listPage_Second_object_ID_posXpath).text == self.vsys_two_object["id"]
            self.driver.find_element(By.XPATH,listPage_object_ip_address_select_Second_object_posXpath).click()
            self.driver.find_element(By.XPATH, listPage_object_ip_address_viewButton_posXpath).click()
            assert len(self.driver.find_elements(By.XPATH, '//div[@class="IconBtn disabled-btn"]')) >= 3
            # self.isElementExist(ip_addressObjectPage_button_OK_posXpath)
            # assert  self.Exist == False
            self.driver.find_element(By.XPATH,ip_addressObjectPage_button_cancel_posCss).click()
        elif vsys_name == "UIAutoTestVsys":
            assert int(count[1]) == 2
            assert self.driver.find_element(By.XPATH,listPage_First_object_ID_posXpath).text == self.vsys_zero_object["id"]
            assert self.driver.find_element(By.XPATH,listPage_Second_object_ID_posXpath).text == self.vsys_two_object["id"]
            self.driver.find_element(By.XPATH,listPage_object_ip_address_select_First_object_posXpath).click()
            self.driver.find_element(By.XPATH, listPage_object_ip_address_viewButton_posXpath).click()
            # add_item_disable = self.isElementExist("//div[@class='object-item-add']/div[@class='IconBtn disabled-btn']")
            # edit_item_disable = self.isElementExist("//div[@class='list-container']//div[@class='IconBtn disabled-btn'][1]")
            # del_item_disable = self.isElementExist("//div[@class='list-container']//div[@class='IconBtn disabled-btn'][2]")
            # assert add_item_disable == edit_item_disable == del_item_disable == True
            # self.isElementExist(ip_addressObjectPage_button_OK_posXpath)
            # assert self.Exist == False
            self.driver.find_element(By.XPATH, ip_addressObjectPage_button_cancel_posCss).click()
            # self.driver.find_element(By.XPATH,listPage_object_ip_address_select_Second_object_posXpath).click()
            # self.driver.find_element(By.ID, listPage_object_ip_address_delButton_posId).click()
            # self.driver.find_element(By.XPATH, listPage_object_ip_address_del_yes_Button_posXpath).click()

    def isElementExist(self, Element, timeout=1):
        try:
            WebDriverWait(self.driver,timeout).until(EC.presence_of_element_located((By.XPATH, Element)))
            self.Exist = True  # 找到==》True
        except:
            self.Exist = False  # 找不到===》Flase
        return self.Exist