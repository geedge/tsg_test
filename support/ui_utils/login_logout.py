import time
import configparser
from support.ui_utils.my_web_driver import MyWebDriver
from selenium.webdriver.common.by import By
from support.ui_utils.workpath import *
from support.ui_utils.element_position.profile_element_position import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import sys
import subprocess
import platform
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from datetime import datetime 

class LogInOut:
    def __init__(self, driver: MyWebDriver):
        self.driver = driver
        self.loginout_parse = configparser.ConfigParser()
        loginout_parse_dir = os.path.join(workdir, "configuration_file.ini")
        self.loginout_parse.read(loginout_parse_dir, encoding="utf-8")
        self.tsglogin_url = self.loginout_parse.get("tsg_url", "login_url")

    def login(self, vsys_name=""):
        self.driver.get(self.tsglogin_url)
        # 需要判断，遇到https不安全时，点击高级-继续登录才可以访问https-tsg
        if "https" in self.tsglogin_url:
            is_existence = self.driver.is_element_exist("//*[@id='details-button']", timeout=1.5)
            if is_existence == True:
                if "高级" in self.driver.find_element(By.XPATH, "//*[@id='details-button']").text.strip():
                    self.driver.find_element(By.XPATH, "//*[@id='details-button']").click()
                    self.driver.find_element(By.XPATH, "//*[@id='proceed-link']").click()
        # 输入账户和密码
        self.driver.find_element(By.XPATH, loginPage_userName_posXpath).send_keys(self.loginout_parse.get("account", "username"))
        self.driver.find_element(By.XPATH, loginPage_passwd_posXpath).send_keys(self.loginout_parse.get("account", "password"))
        self.driver.find_element(By.XPATH, loginPage_signIn_posXpath).click()
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Login to TSG successfully.", flush=True)
        # 消除右上角弹框
        self.dismiss_right_top_tips()
        # 切换至默认ui_vsys
        self._change_vsys(vsys_name=vsys_name)
        # 默认更改为英语
        self._default_language()
        # 如果是centos虚拟机，要调整分辨率，不然会导致元素定位失败
        # os_name = platform.system()
        # if os_name == "Linux":
        #     command = f"xrandr --output eDP-1 --mode {1920}x{1200}"
        #     subprocess.check_call(command, shell=True)

    def _default_language(self):
        # 获取当前默认语言，并设置为英语
        current_language_element_i_class = self.driver.find_element(By.XPATH, mainPage_input_language_posXpath).get_attribute("class").strip()
        if "icon-Lang_enSelect".lower() not in current_language_element_i_class.lower():
            self.driver.find_element(By.XPATH, mainPage_language_change_posXpath).click()
            self.driver.find_element(By.XPATH, mainPage_language_english_posXpath).click()
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "Change language to English successfully.", flush=True)

    def _change_vsys(self, vsys_name=""):
        current_path = os.path.dirname(__file__)  # 当前文件目录
        temp_path = os.path.dirname(os.path.dirname(current_path))
        conf_path = os.path.join(temp_path, "configuration_file.ini")
        # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], conf_path)
        conf = configparser.ConfigParser()
        conf.read(conf_path, encoding="utf-8")
        id_for_ui = conf.get("vsys", "for_traffic_verification")
        id_vsys_format = "vsys{}".format(id_for_ui)  # 使用配置变量值
        if id_vsys_format == "vsys1":   # 临时调整
            id_vsys_format = "Default Vsys"
        elif id_vsys_format == "vsys2":
            id_vsys_format = "UIAutoTestVsys"
        elif id_vsys_format == "vsys3":
            id_vsys_format = "PerformanceTestVsys"
        elif id_vsys_format == "vsys5":
            id_vsys_format = "UIwithTrafficTestVsys"
        # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], id_vsys_format)
        # 传入vsys_name值区分
        if vsys_name == "":  # 空，vsys值来自配置文件
            change_vsys_name = id_vsys_format
        else:  # 切换到指定vsys
            change_vsys_name = vsys_name
        self.driver.find_element(By.XPATH, mainPage_button_menu_posXpath).click()  # 点击vsys menu
        vsys_tree_name_list = self.driver.find_elements(By.XPATH, mainPage_vsysTree_vsysName_posXpath, find_before_wait_time=0.5, find_after_wait_time=0.1)
        time.sleep(0.5)
        flag_num = 0
        for el_vsys_item in vsys_tree_name_list:
            vsys_item_name = el_vsys_item.text.strip().lower()
            vsys_item_name_list = vsys_item_name.split("\n")
            # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], vsys_item_name_list)
            if change_vsys_name.lower() in vsys_item_name_list:
                flag_num = 1
                el_vsys_item.find_element(By.XPATH, ".//span[@class='vsysItem']").click()
                break
        if flag_num == 0:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"no vsys: {change_vsys_name}", flush=True)
        
    def dismiss_right_top_tips(self):
        # 消除弹框
        """
        :param close_button_elem_Xpath:
        :return:
        """
        close_button_elem_Xpath ='(//i[@class="iconfont icon-Delete_X"])[last()]'  # 全局右上提示窗关闭按钮（最新的一个）
        self.driver.is_element_exist(close_button_elem_Xpath, timeout=0.5)
        loop_count = 2
        while loop_count > 0:
            try:
                self.driver.is_element_exist(close_button_elem_Xpath, timeout=0.5)
                if self.driver.is_existence:
                    self.driver.find_element(By.XPATH, close_button_elem_Xpath).click()
                loop_count -= 1
            except:
                loop_count -= 1
                pass
            
    def login_by_user_pwd_mode(self, user_name, passowrd, login_mode=1, ldap_server=""):
        """
        指定用户名、密码、登录
        :param user_name:
        :param passowrd:
        :param login_mode: 1:local 2:LDAP 3:
        :param ldap_server: LDAP模式登录时对应的LDAP Server
        :return:
        """
        self.driver.get(self.tsglogin_url)
        # 输入账户和密码
        self.driver.find_element(By.Xpath, loginPage_userName_posXpath).send_keys(user_name)
        self.driver.find_element(By.Xpath, loginPage_passwd_posXpath).send_keys(passowrd)
        self.driver.find_element(By.Xpath, loginPage_signIn_posXpath).click()

    def logout(self):
        user_btn = self.driver.find_element(By.XPATH, "//*[@id='user_avator']//i")    # 点击账户按钮
        self.driver.execute_script("arguments[0].click()", user_btn)
        signout_btn = self.driver.find_element(By.XPATH, "//*[@id='SignOut']")    # 点击退出登录
        self.driver.execute_script("arguments[0].click()", signout_btn)

    def login_error(self, elment_position=loginPage_error_posXpath, elment_text="", is_existence=True):
        """
        判断错误信息：
        :param elment_position: 错误信息定位
        :param is_existence: 错误内容是否存在
        :return:
         driver是webdriver对象
         10是最长等待时间
         0.5是每0.5秒去查询对应的元素
         until后面跟的等待具体条件
         EC是判断条件，检查元素是否存在于页面的 DOM 上
        """
        try:
           error_text = self.driver.find_element(By.XPATH, loginPage_error_posXpath).text.strip()
           if is_existence == True and error_text == elment_text:
               return True
           else:
               return False
        except:
            if is_existence == False:
                return True
            else:
                return False

    def get_login_error(self,elment_position=loginPage_error_posXpath):
        """
        判断错误信息：
        :param elment_position: 错误信息定位
        :param is_existence: 错误内容是否存在
        :return:
         driver是webdriver对象
         10是最长等待时间
         0.5是每0.5秒去查询对应的元素
         until后面跟的等待具体条件
         EC是判断条件，检查元素是否存在于页面的 DOM 上
        """
        try:
           error_text = self.driver.find_element(By.XPATH, loginPage_error_posXpath).text.strip()
           return error_text
        except:
            return ""