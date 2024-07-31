import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.log_element_position import *
from support.ui_utils.log.page_jump import PageJump

class SearchLog:
    def __init__(self, driver):
        self.driver = driver
        
    def search(self, sql, log_element_position, vsys_name=""):
        search_element_position = log_element_position["search"]
        page_jump_element_position = log_element_position["page_jump"]
        # 打开该列表
        page_jump = PageJump(self.driver)
        time.sleep(3)
        page_jump.jump_sub_log_page(page_jump_element_position)
        """
        self.driver.find_element(By.ID, logListPage_addFilterButton_posId).click()
        self.driver.find_element(By.XPATH, search_element_position["logListPage_searchField_input_posXpath"]).send_keys("Statistics Rule List")
        self.driver.find_element(By.XPATH, search_element_position["logListPage_searchRuleList_operation_posXpath"]).click()
        self.driver.find_element(By.XPATH, search_element_position["logListPage_searchField_input_posXpath"]).send_keys("906595")
        """
        btn = self.driver.find_element(By.ID, search_element_position["logListPage_enterModelButton_posId"])
        self.driver.execute_script("arguments[0].click()", btn)  # 强制点击
        self.driver.find_element(By.XPATH, search_element_position["logListPage_enterModel_posXpath"]).send_keys(sql)
        self.driver.find_element(By.XPATH, search_element_position["logListPage_search_text_area_posXpath"]).send_keys(Keys.ENTER)
        time.sleep(2)
        total_text = self.driver.find_element(By.XPATH, search_element_position["logListPage_totalText_posXpath"])
        total = total_text.split(": ")[-1]
        if total > 0:
            return 200, total
        else:
            return 400, ""
