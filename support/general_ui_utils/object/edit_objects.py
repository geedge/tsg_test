import time
from datetime import datetime

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from support.general_ui_utils.object.page_jump import PageJump
from support.ui_utils.element_position.object_element_position import *
from support.ui_utils.read_data import ReadData
from support.general_ui_utils.element_position.object_element_position import *

class EditObjects:

    def __init__(self,driver):
        self.driver = driver
        self.driver.implicitly_wait(5)
        self.my_files = ReadData()
        self.is_import = False
        self.is_group = False

    def edit(self,data,object_element_position,first_row_checkbox_element):
        try:
            edit_element_position = object_element_position["edit"]
            create_element_position = object_element_position["create"]
            # page_jump_element_position = object_element_position["page_jump"]
            # 打开该列表
            # page_jump = PageJump(self.driver)
            # page_jump.jump_sub_object_page(page_jump_element_position)
            # #搜索该object并进入编辑页面
            # self.driver.find_element(By.ID, edit_element_position["objectListPage_searchLabel_posId"]).send_keys(name)
            # self.driver.find_element(By.XPATH, edit_element_position["objectListPage_searchLabel_selectName_posXpath"]).click()
            # self.driver.find_element(By.ID, mainPage_objectSearch_buttonSearch_posId).click()
            # time.sleep(10)
            # all_button_position = "//div[@class='page-box-containcheck']//label[contains(@class, 'allCheckbox')]/span/span"
            # self.driver.find_element(By.XPATH, all_button_position).click()
            first_row_checkbox_element.click()
            edit_button_position = edit_element_position["objectListPage_editButton_posId"]
            self.driver.find_element(By.ID, edit_button_position).click()
            if "objectPage_Group_edit_subObject_Button_posXpath" in edit_element_position.keys():
                self.is_group = True
                self.driver.find_element(By.XPATH, edit_element_position["objectPage_Group_edit_subObject_Button_posXpath"]).click()
            for i in range(len(data["object_operation"]['edit'])):
                if data["object_operation"]['edit'][i]['item_operation'] == 'add':
                    self.driver.find_element(By.XPATH, create_element_position["objectPage_addItem_posXpath"]).click()
                    self.driver.find_element(By.XPATH, create_element_position["objectPage_inputItem_posXpath"]).send_keys(data["object_operation"]['edit'][i]['item_value'][0])
                    self.driver.find_element(By.XPATH, create_element_position["objectPage_button_saveItem_posXpath"]).click()
                elif data["object_operation"]['edit'][i]['item_operation'] == 'modify':
                    modify_item = data["object_operation"]['edit'][i]['item_value'][0].split('->')
                    self.driver.find_element(By.ID, mainPage_ObjectSearch_buttonSearch_Item_posId).send_keys(modify_item[0] + Keys.ENTER) #查找需要修改的item
                    self.item_check_content = self.driver.find_element(By.XPATH,edit_element_position["objectPage_addItem_first_item_posXpath"]).text
                    assert self.item_check_content == modify_item[0], "断言检查item文本正确"
                    self.driver.find_element(By.XPATH, edit_element_position["objectPage_editItem_Button_posXpath"]).click()
                    description_elem = self.driver.find_element(By.XPATH, edit_element_position["objectPage_Item_text_posXpath"])
                    description_elem.clear()
                    description_elem.send_keys(modify_item[1])
                    self.driver.find_element(By.XPATH, edit_element_position["objectPage_editItem_Save_Button_posXpath"]).click()
                elif data["object_operation"]['edit'][i]['item_operation'] == "import":
                    self.is_import = True
                    self.driver.find_element(By.XPATH,create_element_position["objectPage_importItem_posXpath"]).click()
                    self.driver.find_element(By.XPATH,create_element_position["importPage_uploadFile_posXpath"]).send_keys(self.my_files._obj_files_path(file_name=data["object_operation"]['edit'][i]['item_value']))
                    time.sleep(5)
            # 确认创建
            if self.is_import == True:
                self.driver.find_element(By.XPATH, create_element_position["objectPage_import_ok_button_posXpath"]).click()
            if self.is_group == True:
                self.driver.find_element(By.XPATH, create_element_position["groupObjectPage_subObject_OK_button_posXpath"]).click()
                self.driver.find_element(By.XPATH, create_element_position["groupObjectPage_subObject_OK_Warning_Yes_posXpath"]).click()
                self.driver.find_element(By.XPATH, create_element_position["objectPage_okButton_posXpath"]).click()
            else:
                self.driver.find_element(By.XPATH, create_element_position["objectPage_okButton_posXpath"]).click()
                self.driver.find_element(By.XPATH, create_element_position["objectPage_okButton_warningYes_posXpath"]).click()

            time.sleep(0.5)
            return 200
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], f"Exception: {e}", flush=True)
            return 400


