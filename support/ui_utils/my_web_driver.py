import time
import traceback
import inspect
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from typing import Optional
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime 

class MyWebDriver(webdriver.Remote):
    def find_element(self, by=By.ID, value: Optional[str] = None, find_before_wait_time=0.3, find_after_wait_time=0.3, wait_timeout=10):
        """
        封装find_element方法:
        :param by:
        :param value:
        :param find_before_wait_time:   开始查找元素前等待时间
        :param find_after_wait_time:    元素查找后等待时间
        :param wait_timeout:        元素等待超时时间
        :return:
        """
        # 获取当前调用栈
        current_stack = inspect.stack()
        # 调用栈的第一个元素是当前的函数调用（my_function），
        # 第二个元素是调用my_function的地方
        caller_frame_record = current_stack[1]
        # 获取调用者的文件名、行号、函数名等信息
        caller_filename = caller_frame_record.filename
        caller_lineno = caller_frame_record.lineno
        time_1 = time.time()
        if wait_timeout > 60:
            wait_timeout = 60
        while wait_timeout > 0:
            time.sleep(find_before_wait_time)
            wait_timeout = wait_timeout - (find_before_wait_time if find_before_wait_time > 0 else 2.5)
            try:
                self.element = super().find_element(by, value)
            except:
                #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"{caller_filename}. {caller_lineno} line. find element: {value}. find method: {by}.", flush=True)
                throw_assert = 1
                assert_info = traceback.format_exc()
                continue
            else:
                time.sleep(find_after_wait_time)
                throw_assert = 0
                break   #找到则退出循环
        time_2 = time.time()
        search_time = time_2 - time_1
        search_time = round(search_time, 1)
        #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"{caller_filename}. {caller_lineno} line. find element:{value}. find method: {by}. find take time:{search_time} second.", flush=True)
        if throw_assert == 1:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Find Element Error: {caller_filename}. {caller_lineno} line. find element: {value}. find method: {by}.")
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], assert_info, flush=True)
            return 0
        return self.element

    def find_elements(self, by=By.ID, value: Optional[str] = None, find_before_wait_time=0.3, find_after_wait_time=0.3, wait_timeout=10):
        # 获取当前调用栈
        current_stack = inspect.stack()
        # 调用栈的第一个元素是当前的函数调用（my_function），
        # 第二个元素是调用my_function的地方
        caller_frame_record = current_stack[1]
        # 获取调用者的文件名、行号、函数名等信息
        caller_filename = caller_frame_record.filename
        caller_lineno = caller_frame_record.lineno
        if wait_timeout > 60:
            wait_timeout = 60
        while wait_timeout > 0:
            time.sleep(find_before_wait_time)
            wait_timeout = wait_timeout - (find_before_wait_time if find_before_wait_time > 0 else 2.5)
            try:
                self.element = super().find_elements(by, value)
            except:
                #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"{caller_filename}. {caller_lineno} line. find element: {value}. find method: {by}.")
                throw_assert = 1
                assert_info = traceback.format_exc()
                continue
            else:
                time.sleep(find_after_wait_time)
                throw_assert = 0
                break   #找到则退出循环
        if throw_assert == 1:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Find Element Error: {caller_filename}. {caller_lineno} line. find element: {value}. find method: {by}.")
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], assert_info, flush=True)
            return 0
        return self.element

    def is_exist_element(self, Element, timeout=3):
        try:
            WebDriverWait(super(), timeout).until(EC.presence_of_element_located((By.XPATH, Element)))
            self.is_exist = True                # 找到==》True
        except:
            self.is_exist = False               # 找不到===》Flase
        return self.is_exist

    def is_exist_element_by_value(self, by=By.ID, value: Optional[str] = None, timeout=3):
        try:
            WebDriverWait(super(), timeout).until(EC.presence_of_element_located((by, value)))
            is_exist = True                # 找到==》True
        except:
            is_exist = False               # 找不到===》Flase
        return is_exist

if __name__ == '__main__':
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")
