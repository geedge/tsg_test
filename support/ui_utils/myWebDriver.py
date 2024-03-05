import time
import traceback
import inspect
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from typing import Optional
from selenium.webdriver.support import expected_conditions as EC

class MyWebDriver(webdriver.Remote):
    def find_element(self, by=By.ID, value: Optional[str] = None, find_before_wait_time=0.3, find_after_wait_time=0.3, wait_timeout=10):
        """
        封装find_element方法：
        :param by:
        :param value:
        :param find_before_wait_time:   开始查找元素前等待时间
        :param find_after_wait_time:    元素查找后等待时间
        :param wait_timeout:        元素等待超时时间
        :return:
        """
        if wait_timeout > 60:
            wait_timeout = 60
        while wait_timeout > 0:
            time.sleep(find_before_wait_time)
            wait_timeout = wait_timeout - (find_before_wait_time if find_before_wait_time > 0 else 2.5)
            try:
                self.element = super().find_element(by, value)
            except:
                caller_info = inspect.stack()[1]
                caller_filename = caller_info.filename
                caller_line_number = caller_info.frame
                caller_code_context = caller_info.code_context
                print(caller_filename, caller_line_number, caller_code_context)
                print(f"查找方法：{by};-->>", f"查找元素：{value}\n")
                throw_assert = 1
                assert_info = traceback.format_exc()
                continue
            else:
                time.sleep(find_after_wait_time)
                throw_assert = 0
                break   #找到则退出循环
        if throw_assert == 1:
            print(assert_info)
            raise
        return self.element

    def find_elements(self, by=By.ID, value: Optional[str] = None, find_before_wait_time=0.3, find_after_wait_time=0.3, wait_timeout=10):
        if wait_timeout > 60:
            wait_timeout = 60
        while wait_timeout > 0:
            time.sleep(find_before_wait_time)
            wait_timeout = wait_timeout - (find_before_wait_time if find_before_wait_time > 0 else 2.5)
            try:
                self.element = super().find_elements(by, value)
            except:
                caller_info = inspect.stack()[1]
                caller_filename = caller_info.filename
                caller_line_number = caller_info.frame
                caller_code_context = caller_info.code_context
                print(caller_filename, caller_line_number, caller_code_context)
                print(f"查找方法：{by};-->>", f"查找元素：{value}\n")
                throw_assert = 1
                assert_info = traceback.format_exc()
                continue
            else:
                time.sleep(find_after_wait_time)
                throw_assert = 0
                break   #找到则退出循环
        if throw_assert == 1:
            print(assert_info)
            raise
        return self.element

    def isElementExist(self,Element, timeout=3):
        try:
            WebDriverWait(super(), timeout).until(EC.presence_of_element_located((By.XPATH, Element)))
            self.Exist = True                # 找到==》True
        except:
            self.Exist = False               # 找不到===》Flase

    def element_isExist(self, by=By.ID, value: Optional[str] = None, timeout=3):
        try:
            WebDriverWait(super(), timeout).until(EC.presence_of_element_located((by, value)))
            isExist = True                # 找到==》True
        except:
            isExist = False               # 找不到===》Flase
        return isExist

if __name__ == '__main__':
    print("test")
