import sys
import time
from datetime import datetime
from support.general_ui_utils.object.page_jump import PageJump
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from support.general_ui_utils.element_position.object_element_position import *


class ViewStatisticsPage:
    def __init__(self,driver):
        self.driver = driver

    def view_statistics_check(self,statistics_type,object_element_position,first_row_checkbox_element):
        try:
            edit_element_position = object_element_position["edit"]
            page_jump_element_position = object_element_position["page_jump"]

            # 打开该列表
            page_jump = PageJump(self.driver)
            time.sleep(0.5)
            if statistics_type == "elaborate" or statistics_type == "brief":
                # 主界面View验证
                self.driver.find_element(By.XPATH, main_listPage_object_statistics_view_postXpath).click()
                self.isElementExist(Element="(//div[@class='ObjectStatisticSlider'])[1]")
                assert self.Exist, "Statistics界面未打开"
                self.driver.find_element(By.XPATH, "(//div[@class='ObjectStatisticSlider']//span[text()='Cancel'])[2]").click()
                # 详情界面Statistics验证
                first_row_checkbox_element.click()
                edit_button_position = edit_element_position["objectListPage_editButton_posId"]
                self.driver.find_element(By.ID, edit_button_position).click()
                self.driver.find_element(By.XPATH, ObjectDetailPage_statistics_button_posXpath).click()
                self.isElementExist(Element="(//div[@class='ObjectStatisticSlider'])[1]")
                assert self.Exist, "Statistics界面未打开"
            elif statistics_type == "none":
                view_list_class_text = self.driver.find_element(By.XPATH, main_listPage_object_statistics_view_postXpath).get_attribute("class")
                assert "statistics-option-disabled" in view_list_class_text, "该元素应不可点击"
                first_row_checkbox_element.click()
                edit_button_position = edit_element_position["objectListPage_editButton_posId"]
                self.driver.find_element(By.ID, edit_button_position).click()
                statistics_details_class_text = self.driver.find_element(By.XPATH, ObjectDetailPage_statistics_button_posXpath).get_attribute("class")
                assert "statistics-option-disabled" in statistics_details_class_text, "该元素应不可点击"
            page_jump.jump_sub_object_page(page_jump_element_position)
            time.sleep(0.5)
            return 200
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}",file=sys.stderr, flush=True)
            return 400



    def isElementExist(self, Element, timeout=3):
        try:
            WebDriverWait(self.driver,timeout).until(EC.presence_of_element_located((By.XPATH, Element)))
            self.Exist = True  # 找到==》True
        except:
            self.Exist = False  # 找不到===》Flase
        return self.Exist