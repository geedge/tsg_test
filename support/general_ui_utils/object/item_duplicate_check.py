import sys
import time
from datetime import datetime

from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from support.general_ui_utils.element_position.object_element_position import *
from support.ui_utils.random_name import *


class ItemDuplicateCheck:

    def __init__(self,driver):
        self.driver = driver

    def duplicate_check(self,data):
        try:
            # 侧滑部分校验
            self.driver.find_element(By.XPATH, listPage_object_reprtition_check_postXpath).click()
            self.total_count = self.driver.find_element(By.XPATH,"//div[@class='tab-content floatleft height100 width100']/p").text
            self.count = self.total_count.split("Total:")
            assert self.count[1] == '1'
            # 悬浮框内容校验
            element_to_hover_over = self.driver.find_element(By.XPATH,"//div[@class='TableList floatleft overflow-y-auto width100']//div[@class='reference-box el-popover__reference']/span")
            ActionChains(self.driver).move_to_element(element_to_hover_over).perform()
            tooltip = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@x-placement="right-start"]')))
            # 行符分割为列表
            hover_tooltip = tooltip.text.splitlines()
            # 列表转换为字典
            result_dict = {}
            for i in range(0, len(hover_tooltip), 2):
                if i + 1 < len(hover_tooltip):  # 确保存在下一行
                    key = hover_tooltip[i].strip()  # 去除首尾空格作为键
                    value = hover_tooltip[i + 1].strip()  # 去除首尾空格作为值
                    result_dict[key] = value
            try:
                assert data["object_operation"]['create'][0]['item_value'][0] == result_dict["Item"].split()[0],"校验悬浮框item值"
            except KeyError:
                assert list(data["Create"]["item"].values())[0] == result_dict["Item"].split()[0],"校验悬浮框item值"

            return 200
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}",flush=True)
            return 400