import time
import configparser
from myWebDriver import MyWebDriver
from selenium.webdriver.common.by import By
from workpath import *
from element_position.profileElementPosition import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from ui_utils.profile.profilePublicFunc import ProfilePublicFunc

class LogInOut:
    def __init__(self, driver: MyWebDriver):
        self.driver = driver
        self.loginout_parse = configparser.ConfigParser()
        loginout_parse_dir = os.path.join(workdir, "ui_utils", "loginout.ini")
        self.loginout_parse.read(loginout_parse_dir, encoding="utf-8")
        self.tsglogin_url = self.loginout_parse.get("tsg_url", "login_url")

    def login(self):
        self.driver.get(self.tsglogin_url)
        # 输入账户和密码
        self.driver.find_element(By.NAME, loginPage_userName_posName).send_keys(self.loginout_parse.get("ui_account_1", "username"))
        self.driver.find_element(By.NAME, loginPage_passwd_posName).send_keys(self.loginout_parse.get("ui_account_1", "passwd"))
        self.driver.find_element(By.ID, loginPage_signIn_posId).click()
        # 消除右上角弹框
        self.dismiss_rightTopTips()
        # 切换至默认ui_vsys
        # self._check_ui_vsys()
        # 默认更改为英语
        self._default_language()

    def _default_language(self):
        # 获取当前默认语言，并设置为英语
        current_language = self.driver.find_element(By.XPATH, mainPage_input_language_posXpath).get_attribute("value").strip()
        if "english" != current_language.lower():
            self.driver.find_element(By.XPATH, mainPage_language_change_posXpath).click()
            self.driver.find_element(By.XPATH, mainPage_language_english_posXpath).click()

    def _check_ui_vsys(self):
        # 切换UI自动化使用vsys
        vsys_name = "UIAutoTestVsys"     # 登录后vsys切换为UIAutoTestVsys
        profile_pub = ProfilePublicFunc(self.driver)
        profile_pub.change_vsys(vsys_name=vsys_name)
        
    def dismiss_rightTopTips(self):
        # 消除弹框
        """
        :param close_button_elem_Xpath:
        :return:
        """
        close_button_elem_Xpath ='(//i[@class="iconfont icon-Delete_X"])[last()]'  # 全局右上提示窗关闭按钮（最新的一个）
        self.driver.isElementExist(close_button_elem_Xpath)
        loop_count = 2
        while loop_count > 0:
            try:
                self.driver.isElementExist(close_button_elem_Xpath)
                if self.driver.Exist:
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
        self.driver.find_element(By.NAME, loginPage_userName_posName).send_keys(user_name)
        self.driver.find_element(By.NAME, loginPage_passwd_posName).send_keys(passowrd)
        self.driver.find_element(By.ID, loginPage_signIn_posId).click()

    def logout(self):
        user_btn = self.driver.find_element(By.XPATH, "//*[@id='user_avator']//i")    # 点击账户按钮
        self.driver.execute_script("arguments[0].click()", user_btn)
        signout_btn = self.driver.find_element(By.XPATH, "//*[@id='SignOut']")    # 点击退出登录
        self.driver.execute_script("arguments[0].click()", signout_btn)

    def login_error(self, elment_position=loginPage_error_posXpath, elment_text="", is_exist=True):
        """
        判断错误信息：
        :param elment_position: 错误信息定位
        :param is_exist: 错误内容是否存在
        :return:
         driver是webdriver对象
         10是最长等待时间
         0.5是每0.5秒去查询对应的元素
         until后面跟的等待具体条件
         EC是判断条件，检查元素是否存在于页面的 DOM 上
        """
        try:
           error_text = self.driver.find_element(By.XPATH, loginPage_error_posXpath).text.strip()
           if is_exist == True and error_text == elment_text:
               return True
           else:
               return False
        except:
            if is_exist == False:
                return True
            else:
                return False

    def get_login_error(self,elment_position=loginPage_error_posXpath):
        """
        判断错误信息：
        :param elment_position: 错误信息定位
        :param is_exist: 错误内容是否存在
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