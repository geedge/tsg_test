
from selenium.webdriver.common.by import By
from support.general_ui_utils.element_position.dashboard_element_position import *
from datetime import datetime

class DeleteDashboard:

    def __init__(self,driver):
        self.driver = driver

    def delete(self):
        try:
            edit_btn = self.driver.find_element(By.XPATH, mainPage_edit_dashboard_button_posXpath)
            self.driver.execute_script("arguments[0].click()", edit_btn)  # 强制点击
            self.driver.find_element(By.XPATH, mainPage_delete_dashboard_posXpath).click()
            self.driver.find_element(By.XPATH, mainPage_delete_Delete_button_posXpath).click()
            return 200
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}",flush=True)
            return 400

    def delete_dashboard(self):
        self.driver.refresh()
        edit_btn = self.driver.find_element(By.XPATH, mainPage_edit_dashboard_button_posXpath)
        self.driver.execute_script("arguments[0].click()", edit_btn)  # 强制点击
        self.driver.find_element(By.XPATH, mainPage_delete_dashboard_posXpath).click()
        self.driver.find_element(By.XPATH, mainPage_delete_Delete_button_posXpath).click()
