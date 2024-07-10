import time
from support.ui_utils.my_web_driver import MyWebDriver
from selenium.webdriver.common.by import By
import configparser
from support.general_ui_utils.workpath import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from support.general_ui_utils.profile.profiles_public_operations import ProfilesPublicOperations
from support.general_ui_utils.element_position.profiles_element_position import *


class LogInOut:
    def __init__(self, driver: MyWebDriver):
        self.driver = driver
        #初始化，负载远程用户登录
        self.loginout_parse = configparser.ConfigParser()
        loginout_parse_dir = os.path.join(workdir, "config", "loginout.ini")
        self.loginout_parse.read(loginout_parse_dir, encoding="utf-8")
        self.tsglogin_url = self.loginout_parse.get("tsg_url", "login_url")

    def login(self):
        self.driver.get(self.tsglogin_url)
        # 需要判断，遇到https不安全时，点击高级-继续登录才可以访问https-tsg
        if "https" in self.tsglogin_url:
            self.driver.is_exist_element("//*[@id='details-button']")
            if self.driver.Exist:
                if "高级" in self.driver.find_element(By.XPATH, "//*[@id='details-button']").text.strip():
                    self.driver.find_element(By.XPATH, "//*[@id='details-button']").click()
                    self.driver.find_element(By.XPATH, "//*[@id='proceed-link']").click()
        #输入账户和密码
        self.driver.find_element(By.NAME, loginPage_userName_posName).send_keys(self.loginout_parse.get("ui_account_1", "username"))
        self.driver.find_element(By.NAME, loginPage_passwd_posName).send_keys(self.loginout_parse.get("ui_account_1", "passwd"))
        self.driver.find_element(By.ID, loginPage_signIn_posId).click()
        # 消除右上角弹框
        self.dismiss_rightTopTips()
        # 切换至默认ui_vsys
        self._check_ui_vsys()
        # 默认更改为英语
        self._default_language()

    def login_other(self, url="", username="", passwd=""):
        """可以登录给定地址的tsg系统"""
        self.driver.get(url)
        # 需要判断，遇到https不安全时，点击高级-继续登录才可以访问https-tsg
        if "https" in url:
            self.driver.is_exist_element("//*[@id='details-button']")
            if self.driver.Exist:
                if "高级" in self.driver.find_element(By.XPATH, "//*[@id='details-button']").text.strip():
                    self.driver.find_element(By.XPATH, "//*[@id='details-button']").click()
                    self.driver.find_element(By.XPATH, "//*[@id='proceed-link']").click()
        #输入账户和密码
        self.driver.find_element(By.NAME, loginPage_userName_posName).send_keys(username)
        self.driver.find_element(By.NAME, loginPage_passwd_posName).send_keys(passwd)
        self.driver.find_element(By.ID, loginPage_signIn_posId).click()
        # 消除右上角弹框
        self.dismiss_rightTopTips()
        # 切换至默认ui_vsys
        #self._check_ui_vsys()
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
        vsys_name = self.loginout_parse.get("vsys", "vsys_name")   # 登录后vsys切换为UIAutoTestVsys
        print(vsys_name)
        profile_pub = ProfilesPublicOperations(self.driver)
        profile_pub.change_vsys(vsys_name=vsys_name)
        # 提取当前vsys信息
        # current_vsys = self.driver.find_element(By.XPATH,'//span[@class="root-title"]').text.strip()
        # if current_vsys == "UIAutoTestVsys":
        #     pass
        # else:
        #     self.driver.find_element(By.XPATH,'//span/button/span[contains(text(),"Menu")]').click() # 打开Menu
        #     self.driver.find_element(By.XPATH,'//li[@class="infinite-list-item"]/div[2]/ul/li[2]/div/div[2]/div/div[contains(text(),"UIAutoTestVsys")]').click() # 默认切换至UIAutoTestVsys

    def dismiss_rightTopTips(self):
        # 消除弹框
        """
        :param close_button_elem_Xpath:
        :return:
        """
        # try:
        #     self.driver.is_exist_element(Element="//div/div[1]/div[2]/div/div[2]/div[3]/i", timeout=0.5)
        #     if self.driver.Exist:
        #         self.driver.find_element(By.XPATH,'//div/div[1]/div[2]/div/div[2]/div[3]/i').click()
        # except:
        #     pass
        # try:
        #     self.driver.is_exist_element(Element="//div/div[1]/div[2]/div/div/div[3]/i", timeout=0.5)
        #     if self.driver.Exist:
        #         self.driver.find_element(By.XPATH,'//div/div[1]/div[2]/div/div/div[3]/i').click()
        # except:
        #     pass

        # time.sleep(3)
        close_button_elem_Xpath ='(//i[@class="iconfont icon-Delete_X"])[last()]'  # 全局右上提示窗关闭按钮（最新的一个）
        self.driver.is_exist_element(close_button_elem_Xpath)
        loop_count = 2
        while loop_count > 0:
            try:
                self.driver.is_exist_element(close_button_elem_Xpath)
                if self.driver.Exist:
                    self.driver.find_element(By.XPATH, close_button_elem_Xpath).click()
                loop_count -= 1
            except:
                loop_count -= 1
                pass
    def login_by_user_pwd_mode(self,user_name,passowrd,login_mode=1,ldap_server=""):
        """
        指定用户名、密码、登录
        :param user_name:
        :param passowrd:
        :param login_mode: 1:local 2:LDAP 3:
        :param ldap_server: LDAP模式登录时对应的LDAP Server
        :return:
        """
        self.driver.get(self.tsglogin_url)
        #输入账户和密码
        self.driver.find_element(By.NAME, loginPage_userName_posName).send_keys(user_name)
        self.driver.find_element(By.NAME, loginPage_passwd_posName).send_keys(passowrd)
        self.driver.find_element(By.ID, loginPage_signIn_posId).click()

    def logout(self):
        user_btn = self.driver.find_element(By.XPATH, "//*[@id='user_avator']//i")    # 点击账户按钮
        self.driver.execute_script("arguments[0].click()", user_btn)
        signout_btn = self.driver.find_element(By.XPATH, "//*[@id='SignOut']")    # 点击退出登录
        self.driver.execute_script("arguments[0].click()", signout_btn)

    def login_error(self,elment_position=loginPage_error_posXpath,elment_text="",is_exist=True):
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
           #element = WebDriverWait(self.driver, 3, 0.1).until(EC.visibility_of_element_located((By.XPATH, loginPage_error_posXpath)))
           #error_text= element.text.strip()
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
           #element = WebDriverWait(self.driver, 3, 0.1).until(EC.visibility_of_element_located((By.XPATH, loginPage_error_posXpath)))
           #error_text= element.text.strip()
           error_text = self.driver.find_element(By.XPATH, loginPage_error_posXpath).text.strip()
           return error_text
        except:
            return ""





