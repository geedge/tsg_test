mainPage_navigationBar_logo_posCss = ".tsg-img-logo"
mainPage_button_menu_posXCss = ".menu-btn span"    #menu按钮定位
mainPage_objectSearch_buttonSearch_posId = "searchQuery"  # 查询按钮id
mainPage_currentPage_vsysName_posXpath = "//span[@class='root-title']"    # 当前页面中vsys name
mainPage_vsysTree_vsysName_posXpath = "//div[contains(@class, 'menu-level2')]//article//div[@class='menu-title']"    # vsys tree中vsys name定位
mainPage_firstLevelMenu_Objects_posId = "object"  # 一级菜单Global Objects
mainPage_secondLevelMenu_ipAddress_posId = "Objects_ip"  # 二级菜单IP Addresses

# ip object
listPage_object_ip_address_createButton_posId = "objectCreate-_OperateBtns_ElRow_Objects_ip_Home_App_anonymousComponent"  # create按钮id
listPage_object_ip_address_create_ip_address_Button_posId = 'object0-_OperateBtns_ElRow_Objects_ip_Home_App_anonymousComponent'  # 从下拉菜单中选择Address
listPage_objectSearch_ip_address_selectLabel_posId = "select-label"  # 查询框id
listPage_objectSearch_ip_address_select_Name_posXpath = '//li[@id="2-_FilteredSearch_ElRow_Objects_ip_Home_App_anonymousComponent"]'  # 查询Name
listPage_object_delButton_posId = "appDel-_OperateBtns_ElRow_Objects_ip_Home_App_anonymousComponent"
listPage_dialogTips_delButton_yes_posCss = "//span[@class='dialog-footer']//button[@class='el-button delComponents-ok role-disconnect-btn el-button--default el-button--small']/span"
listPage_dialogTips_delButton_no_posCss = "body>.el-dialog__wrapper .delComponents-close span"
listPage_objectBottomPage_ip_object_button_allSelect_posXpath = "//div[@class='page-box-containcheck']//label[contains(@class, 'allCheckbox')]/span/span"
listPage_objectTable_ip_tableTbody_posXpath = "//div[contains(@class,'ly-table1')]//tbody" 
ip_addressObjectPage_input_name_posXpath = "//*[@class='biFangName']//input" # name输入框Xpath
ip_addressObjectPage_button_addItem_posId = "temporary_form"  # 添加item_id
ip_addressObjectPage_button_inputItem_posXpath = '//div[@class="ip-input el-input el-input--small"]//input'
ip_addressObjectPage_button_saveItem_posXpath = '//div/i[@class="operate-icon iconfont icon-save check"]'  # 保存item按钮
ip_addressObjectPage_button_saveYes_posXpath = '//button[@id="OK-_IpDetail_Home_App_anonymousComponent"]/span'  # OK按钮
ip_addressObjectPage_button_warningSaveYes_posXpath = "//div[@class='el-message-box__wrapper']//button[contains(@class, 'el-button--primary operation-confirm')]/span"

# 其他