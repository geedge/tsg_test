import os
import sys
import time
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.profile_element_position import *
from datetime import datetime 


class CreateMonitorProfile:
    def __init__(self, driver):
        self.driver = driver

    def create_traffic_mirroring_profile(self, data):
        profile_name = data["name"]
        self.driver.find_element(By.ID, trafficMirroringProfiles_input_Name_posId).send_keys(profile_name)

        #解析输入的vlan id数据
        vlan_ids = data["vlan_id"]
        vlan_ids_create = []   #创建的vlan id
        for i in vlan_ids:
            if i.strip().split("->")[0] != "":
                vlan_ids_create.append(i.strip().split("->")[0])
        #循环输入vlan id
        for j in range(len(vlan_ids_create)):
            #输入ipnut
            elements_vlan_ids_input = self.driver.find_elements(By.XPATH, trafficMirroringProfiles_input_vlanIdsInput_posXpath)
            for element_vlan_id in elements_vlan_ids_input:
                if element_vlan_id.get_attribute("value") == "":    #创建时，只是往input.value=none中键入数据
                    element_pos_by_id = element_vlan_id.get_attribute("id")
                    self.driver.find_element(By.ID, element_pos_by_id).send_keys(vlan_ids_create[j])    #输入vlan id的值
                    self.driver.find_element(By.XPATH, "//label[text()='VLAN ID']").click()
                    break
            if (len(vlan_ids_create) - 1) - j > 0:    #最后一个数据，不用点击+
                self.driver.find_element(By.CSS_SELECTOR, trafficMirroringProfiles_button_vlanIdAdd_posCss).click()   #点击add添加
        #点击OK
        self.driver.find_element(By.CSS_SELECTOR, trafficMirroringProfiles_button_oK_posCss).click()
        if self.driver.find_element(By.CSS_SELECTOR, trafficMirroringProfiles_button_warningSaveYes_posCss, find_before_wait_time=1).is_displayed():
            self.driver.find_element(By.CSS_SELECTOR, trafficMirroringProfiles_button_warningSaveYes_posCss).click()

