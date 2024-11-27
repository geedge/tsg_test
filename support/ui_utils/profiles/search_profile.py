import time
from selenium.webdriver.common.by import By
from support.ui_utils.element_position.profile_element_position import *
from support.ui_utils.profiles.page_jump import PageJump
from selenium.webdriver.common.keys import Keys

class SearchProfile:
    def __init__(self, driver):
        self.driver = driver

    def search(self, name, profile_element_position, vsys_name=""):
        search_element_position = profile_element_position["search"]
        page_jump_element_position = profile_element_position["page_jump"]
        # 打开该列表
        page_jump = PageJump(self.driver)
        page_jump.jump_sub_profile_page(page_jump_element_position)
        btn = self.driver.find_element(By.XPATH, search_element_position["profileListPage_searchLabel_posXpath"])
        self.driver.execute_script("arguments[0].click()", btn)
        # 通过name 查询时
        # 先输入Name，下拉列表显示Name contains profilename后选择对应选项
        self.driver.find_element(By.XPATH, search_element_position["profileListPage_searchLabel_posXpath"]).send_keys(Keys.CONTROL + "a")
        self.driver.find_element(By.XPATH, search_element_position["profileListPage_searchLabel_posXpath"]).send_keys(name)
        # 下拉列表显示Name contains profilename后选择对应选项
        btn = self.driver.find_element(By.XPATH, search_element_position["profileListPage_searchLabel_selectName_posXpath"].format(replaceValue="Name"))
        self.driver.execute_script("arguments[0].click()", btn) # 点击查询下拉菜单中item

        #input_item_posXpath = search_element_position["profileListPage_searchLabel_inputContent_posXpath"].format( replaceName="Name")
        #self.driver.find_element(By.XPATH, input_item_posXpath).send_keys(name)  # 输入查询值
        #self.driver.find_element(By.XPATH, input_item_posXpath).send_keys(Keys.ENTER)  # 模拟回车按键
        # 点击查询按钮
        element_search = self.driver.find_element(By.XPATH, mainPage_profileSearch_buttonSearch_posXpath)
        self.driver.execute_script("arguments[0].click()", element_search)  # 强制点击
        time.sleep(0.5)
        element_tr = self.driver.find_element(By.XPATH, search_element_position["profileListPage_tableTbody_posXpath"])
        row = element_tr.find_elements(By.XPATH, "div")
        if len(row) != 0 :
            first_row = row[0]
            first_row_checkBox_element = first_row.find_element(By.XPATH, "//span[@class='MuiCheckbox-action css-kit57i']")
            return 200, first_row_checkBox_element
        else:
            return 400, ""

