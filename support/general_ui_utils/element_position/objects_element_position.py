# login page 登录页面
loginPage_userName_posName = "username"
loginPage_passwd_posName = "password"
loginPage_signIn_posId = "login"

# main页面
##上导航栏
mainPage_navigationBar_logo_posCss = ".tsg-img-logo"
mainPage_navigationBar_Menu_posXpath = '//div[@class="header"]//button[@data-desc="Menu"]'
mainPage_navigationBar_Menu_adminArea_posXpath = '//div[contains(text(),"Admin Area")]'  # Admin Area
mainPage_navigationBar_Default_Vsys3_posXpath = '//article/div/ul/li[2]/div[2]/ul/li[1]/div/div[2]/div'  # Default TVsys3

# mainPage_navigationBar_Tvsys10_posXpath = '//article/div/ul/li[2]/div[2]/ul/li[2]/div/div[2]'  # Tvsys10
mainPage_navigationBar_Tvsys3_posXpath = '//*[@class="el-row"]//*[contains(text(),"Vsys3")]'  # Tvsys3
mainPage_navigationBar_Tvsys10_posXpath = '//*[@class="el-row"]//*[contains(text(),"Vsys10")]'  # Tvsys10
mainPage_navigationBar_Mvsys2_Tvsys4_posXpath = '//article/div/ul/li[2]/div[1]/div[2]/div'  # Mvsys2_Tvsys4
# mainPage_navigationBar_Mvsys3_Tvsys5_posXpath = '//article/div/ul/li[1]/div[1]/div[2]'  # Mvsys3_Tvsys5 super_vsys
mainPage_navigationBar_Mvsys3_Tvsys5_posXpath = '//article/div[@class="VsysTree"]//div[not(@class="VsysTree")]//div[@class="menu-desc" and normalize-space(text())="Vsys5"]'  # Mvsys3_Tvsys5 super_vsys
mainPage_navigationBar_super_Tvsys1_posXpath = '//article/div/ul/li[1]/div[2]/ul/li[1]/div/div[2]/div'  # super_Tvsys3
mainPage_navigationBar_super_Tvsys10_posXpath = '//article/div/ul/li[1]/div[2]/ul/li[2]/div/div[2]'  # super_Tvsys10
# test area!!!!======================#test area!!!!======================#test area!!!!======================
# test_mainPage_navigationBar_Tvsys3_posXpath = '//article/div/ul/li[2]/div[2]/ul/li[1]/div/div[2]/div'  # Tvsys3
test_mainPage_navigationBar_Tvsys3_posXpath = '//*[@class="el-row"]//*[contains(text(),"Vsys3")]'  # Tvsys3
test_mainPage_navigationBar_Mvsys2_Tvsys4_posXpath = '//article/div[@class="VsysTree"]//div[not(@class="VsysTree")]//div[@class="menu-desc" and normalize-space(text())="Vsys4"]'  # Mvsys4
test_mainPage_navigationBar_Mvsys3_Tvsys5_posXpath = '//article/div[@class="VsysTree"]//div[not(@class="VsysTree")]//div[@class="menu-desc" and normalize-space(text())="Vsys5"]'  # Mvsys5
# Mvsys2_Tvsys1

# Mvsys4_Tvsys1


# Admin Area菜单栏================================Admin Area菜单栏===================================Admin Area菜单栏================================Admin Area菜单栏==================================Admin Area菜单栏========================Admin Area菜单栏
adminArea_mainPage_firstLevelMenu_globalObjects_posId = "Global_Objects"  # 一级菜单Object
adminArea_mainPage_secondLevelMenu_globalObjects_categories_posId = "Objects_fqdn_category"  # 二级菜单Categories
# 菜单栏================================菜单栏===================================菜单栏================================菜单栏==================================菜单栏========================菜单栏
##菜单栏
mainPage_firstLevelMenu_Objects_posId = "object"  # 一级菜单Global Objects
mainPage_secondLevelMenu_ipAddress_posId = "Objects_ip"  # 二级菜单IP Addresses
mainPage_secondLevelMenu_Ports_posId = "Objects_port"  # 二级菜单Ports
mainPage_secondLevelMenu_FQDNs_posId = "Objects_fqdn"  # 二级菜单FQDNs
mainPage_secondLevelMenu_Subscriber_ids_posId = "Objects_subscriberid"  # 二级菜单Subscriber IDs
mainPage_secondLevelMenu_HTTP_Signatures_posId = "Objects_http_signature"  # 二级菜单HTTP Signatures
mainPage_secondLevelMenu_keywords_posId = "Objects_keywords"  # 二级菜单keywords
mainPage_secondLevelMenu_urls_posId = "Objects_url"  # 二级菜单url
mainPage_secondLevelMenu_Categories_posId = "Objects_fqdn_category"  # 二级菜单Categories
mainPage_secondLevelMenu_Account_posId = "Objects_account"  # 二级菜单Account
mainPage_secondLevelMenu_Mobile_Identities_posId = "Objects_mobile_identity"  # 二级菜单Mobile Identities
mainPage_secondLevelMenu_APNs_posId = "Objects_apn"  # 二级菜单APNs
mainPage_secondLevelMenu_Application_posId = "Application_applications"  # 二级菜单Application_applications
mainPage_secondLevelMenu_Application_appSelectors_posId = "Application_appSelectors"  # 二级菜单Application_appSelectors
mainPage_secondLevelMenu_Application_appGroups_posId = "Application_appGroups"  # 二级菜单Application_appGroups
mainPage_secondLevelMenu_Application_appSignatures_posId = "Application_appSignatures"  # 二级菜单Application_appSignatures
mainPage_secondLevelMenu_Application_customizedAttr_posId = "Application_customizedAttr"  # 二级菜单Application_customizedAttr
mainPage_secondLevelMenu_Tunnel_posId = "Objects_tunnel"  # 二级菜单Tunnel
mainPage_secondLevelMenu_Flags_posId = "Objects_flag"  # 二级菜单Flag
mainPage_secondLevelMenu_Intervals_posId = "Objects_interval"  # 二级菜单Intervals
mainPage_secondLevelMenu_Geolocation_posId = "Advanced/IP_Libraries"  # 二级菜单Geolocation
mainPage_secondLevelMenu_Asns_posId = 'Objects_asn'  # 二级菜单ASNs

# Object 查询栏===================Object 查询栏=====================Object 查询栏=================Object 查询栏=======================Object 查询栏=================Object 查询栏
##Object模块查询栏

mainPage_ObjectSearch_selectLabel_posId = "select-label"  # 查询框id
mainPage_ObjectSearch_buttonSearch_posId = "searchQuery"  # 查询按钮id
mainPage_ObjectSearch_buttonClear_posId = "searchClear"  # 清空查询按钮id
mainPage_ObjectSearch_buttonSearch_Item_posId = "object_ip_search"  # 查询item输入框id
mainPage_ObjectSearch_buttonSearch_Item_first_content_posXpath = "//div[@class='view-row']//span[@class='el-tooltip content-show']"  # item搜索框第一个元素
mainPage_ObjectSearch_buttonSearch_Item_posXpath = "//div/div/div/div[2]/div/div[1]/div/div/div/div[2]/div[1]/div/div[1]/div[1]/div/div/input"  # 查询item输入框Xpath
mainPage_ObjectSearch_buttonAddItem_posId = "temporary_form"  # 添加item_id
mainPage_ObjectSearch_input_Item_posId = "onlyMarvel"  # 输入item_id
# Group 策划框
main_Group_sub_Object_input_frame_posXpath = '//div/div[1]/div/div/div/div[2]/div[1]/div/div[1]/div[1]/div/div/input'  # 新建subObject搜索框
main_Group_sub_Object_input_frame_select_one_posXpath = "//div/div[1]/div/div/div/div[2]/div[1]/div/div[2]/div/ul/li[1]/div[2]/span"  # 搜索框第一个元素
# 列表页
main_listPage_object_reference_count_posXpath = "//table/tbody/tr[2]/td[7]/div/div/div/div"  # 提取reference的数量《断言》
main_listPage_object_statistics_view_postXpath = "(//div[@id='ly-table1-listcontent']//span[text()='View'])[1]"

# object导入文件Xpath路径
main_ObjectPage_Input_path_Import_files_posXpath = '//form/div/div/div/div[1]/input[@type="file"]'

# 列表中元素
main_listPage_object_select_Second_object_posXpath = '//table/tbody/tr[2]/td[1]/div/div/div[1]/div/label/span[1]/span'  # 选择列表中第二个对象
##Object模块列设置
mainPage_ObjectSearch_Column_settings_posXpath = '//span[@id="eventfixed"]/i'
mainPage_ObjectSearch_Column_settings_select_allCheckBox_posXpath = '(//div[@class="ly-eventfixed"]//span[@class="el-checkbox__inner"])[last()]'  # ALL选择框----------------
mainPage_ObjectSearch_Column_settings_click_Cancel_Button_posXpath = '//div[@class="choose-button"][1]//span[text()="Cancel"]'  # 点击Cancel
mainPage_ObjectSearch_Column_settings_click_OK_Button_posXpath = '//div[@class="choose-button"][1]//span[text()="OK"]'  # 点击OK
##Object模块列设置
listPage_object_mobileIdentities_Description_Button_posXpath = '//div[@class="ly-eventfixed"]/ul/li[6]/label/span[2]'  # 列设置 Description
# Object table栏===================Object table栏=====================Object table栏=================Object table栏=======================Object table栏=================Object table栏
##Object模块查询栏
list_first_row_first_column_posXpath = '//div[@id="ly-table1-listcontent"]//span[text()="ID"]'  # 第一行、第一列--ID
list_second_row_first_column_posXpath = '//div[@id="ly-table1-listcontent"]//div[@class="table-status-item-id"]/span'  # 第二行、第一列--Object对应ID号

list_first_row_second_column_posXpath = '//div[@id="ly-table1-listcontent"]//span[text()="Vsys ID"]'  # 第一行、第二列
list_second_row_second_column_posXpath = '//table/tbody/tr[1]/td[2]/div//span'  # 第二行、第二列

list_first_row_third_column_posXpath = '//table/thead/tr/th[3]/div/div/span'  # 第一行、第三列
list_second_row_third_column_posXpath = '//table/tbody/tr[1]/td[3]/div/div/div/span'  # 第二行、第三列
list_second_row_third_column_posXpath_IMSI = '//table/tbody/tr[1]/td[4]/div/div/div/div/div/div[1]/span'  # IMSI
list_second_row_third_column_posXpath_IMSI_Group = '//table/tbody/tr/td[4]/div/div/div/div/div/div/div/span/div/div/div'  # IMSI Group
list_second_row_third_column_posXpath_Phone_Number_IMEI_Group = '//table/tbody/tr/td[4]/div/div/div/div/div/div/div/span/div/div/div'  # Phone Number/IMEI Group
list_second_row_third_column_posXpath_Phone_Number_IMEI = '//table/tbody/tr/td[4]/div/div/div/div/div/div/span'  # Phone Number/IMEI

list_first_row_fourth_column_posXpath = '//table/thead/tr/th[4]/div/div/span'  # 第一行、第四列
list_second_row_fourth_column_posXpath = '//table/tbody/tr[1]/td[4]/div/div/div/div/div/div/div/span'  # 第二行、第四列

list_first_row_fifth_column_posXpath = '//table/thead/tr/th[5]/div/div/span'  # 第一行、第五列
list_second_row_fifth_column_posXpath = '//table/tbody/tr[1]/td[5]/div/div/div'  # 第二行、第五列

list_first_row_sixth_column_posXpath = '//table/thead/tr/th[6]/div/div/span'  # 第一行、第六列
list_second_row_sixth_column_posXpath = '//table/tbody/tr[1]/td[6]/div//p'  # 第二行、第六列

# 列表页翻页元素
listPage_object_pages_maxPageNumber_posXpath = '(//div[@class="page-box-containcheck"]//li[contains(@class,"number")])[last()]'  # 列表页最大页码
listPage_object_pages_currentPageNumber_posXpath = '//div[@class="page-box-containcheck"]//li[@class="number active"]'  # 列表页当前页码元素Xpath
listPage_object_pages_currentPageAreaMinNumber_posXpath = '//li[@class="el-icon more btn-quickprev el-icon-more"]/following-sibling::li[1]'  # 列表页当前页码所属区域最小页码元素Xpath
listPage_object_pages_currentPageAreaMaxNumber_posXpath = '(//li[@class="el-icon more btn-quicknext el-icon-more"]/preceding-sibling::li)[last()]'  # 列表页当前页码所属区域最大页码元素Xpath
listPage_object_pages_currentPageArea_MaxNumber_posXpath = '(//li[@class="number"])[last()]'
listPage_object_pages_previousPage_button_poxXpath = '//div[@class="page-box-containcheck"]//button[@class="btn-prev"]/i'  # 前翻页按钮Xpath
listPage_object_pages_nextPage_button_poxXpath = '//div[@class="page-box-containcheck"]//button[@class="btn-next"]'  # 后翻页按钮Xpath
listPage_object_pages_next_2_Page_button_poxXpath = '//div[1]/ul/li[text()="2"]'  # 翻页至第二页
listPage_object_pages_goTo_input_poxXpath = '//div[@class="page-box-containcheck"]//input[@class="el-input__inner"]'  # 页码Go to输入框Xpath
listPage_object_pages_quickPreviousPage_button_poxXpath = '//li[contains(@class,"el-icon more btn-quickprev")]'  # 快速前翻页按钮Xpath
listPage_object_pages_quickNextPage_button_poxXpath = '//li[contains(@class,"el-icon more btn-quicknext")]'  # 快速后翻页按钮Xpath

# Object Group添加object侧滑页下翻页元素
DrawerlistPage_object_pages_maxPageNumber_posXpath = '//div[@class="ToggleDraw"]//li[contains(@class,"number")][last()]'  # 列表页最大页码
DrawerlistPage_object_pages_currentPageNumber_posXpath = '//div[@class="ToggleDraw"]//li[@class="number active"]'  # 列表页当前页码元素Xpath
DrawerlistPage_object_pages_previousPage_button_poxXpath = '//div[@class="ToggleDraw"]//button[@class="btn-prev"]/i'  # 前翻页按钮Xpath
DrawerlistPage_object_pages_nextPage_button_poxXpath = '//div[@class="ToggleDraw"]//button[@class="btn-next"]'  # 后翻页按钮Xpath
DrawerlistPage_object_pages_currentPageAreaMinNumber_posXpath = listPage_object_pages_currentPageAreaMinNumber_posXpath  # 列表页当前页码所属区域最小页码元素Xpath
DrawerlistPage_object_pages_currentPageAreaMaxNumber_posXpath = listPage_object_pages_currentPageAreaMaxNumber_posXpath  # 列表页当前页码所属区域最大页码元素Xpath
DrawerlistPage_object_pages_currentPageArea_MaxNumber_posXpath = listPage_object_pages_currentPageArea_MaxNumber_posXpath
DrawerlistPage_object_pages_goTo_input_poxXpath = '//div[@class="ToggleDraw"]//*[@class="el-pagination__jump"]//input[@class="el-input__inner"]'  # 页码Go to输入框Xpath
DrawerlistPage_object_pages_quickPreviousPage_button_poxXpath = listPage_object_pages_quickPreviousPage_button_poxXpath  # 快速前翻页按钮Xpath
DrawerlistPage_object_pages_quickNextPage_button_poxXpath = listPage_object_pages_quickNextPage_button_poxXpath  # 快速后翻页按钮Xpath

# 列表页其他通用元素
listPage_object_pages_clearCounter_button_poxXpath = '//div[@class="page-box-containcheck"]//*[normalize-space(text())="Clear Counter"]'  # 列表页中的Clear Counter 按钮
listPage_object_pages_first_quoted_object_elem_posXpath = '(//div[contains(@class,"cursorPointer textCenter") and number(text()>=1)])[1]/ancestor::tr//*[@class="el-checkbox__inner"]'#列表页中Reference Count大于等于1的第一个Object的CheckBox

# Object Mobile Identities===================Object Mobile Identities====================Object Mobile Identities=================Object Mobile Identities=======================Object Mobile Identities=================Object Mobile Identities
# Mobile_Identities list page 列表页
listPage_object_mobileIdentities_allButton_posId = '//*[@id="router-view-container"]/div/div[1]/div[4]/label/span[2]'  # all按钮
listPage_object_mobileIdentities_createButton_posId = "objectCreate-_OperateBtns_ElRow_Objects_mobile_identity_Home_App_anonymousComponent"  # create按钮id
listPage_object_mobileIdentities_editButton_posId = "appEdit-_OperateBtns_ElRow_Objects_mobile_identity_Home_App_anonymousComponent"  # edit按钮id
listPage_object_mobileIdentities_editButton_content_posXpath = '//button[@id="appEdit-_OperateBtns_ElRow_Objects_mobile_identity_Home_App_anonymousComponent"]/span/div/div[2]/p[1]'
listPage_object_mobileIdentities_delButton_posId = "appDel-_OperateBtns_ElRow_Objects_mobile_identity_Home_App_anonymousComponent"  # del按钮id
listPage_object_mobileIdentities_del_yes_Button_posXpath = '//div[@class="el-dialog__wrapper"]/div/div[3]/span/button[1]/span'  # del_yes按钮
listPage_objectSearch_mobileIdentities_selectLabel_posId = mainPage_ObjectSearch_selectLabel_posId  # 查询框id
listPage_objectSearch_mobileIdentities_add_watch_posXpath = '//div[@id="router-view-container"]/div/div[1]/div/div[4]/span/span[text() = "Watch"]'  # 添加watch列表页
listPage_objectSearch_mobileIdentities_right_list_watch_posXpath = '//div[@id="fixed-right"]/ul/div/div[1]/li/div/i'  # 右侧watch列表
listPage_objectSearch_mobileIdentities_right_list_watch_select_all_posXpath = '//div[1]/div/div/div[3]/label/span[1]/span'  # 右侧watch列表选择all
listPage_objectSearch_mobileIdentities_right_list_watch_select_clear_posXpath = '//span[@id="watchClean"]'  # 右侧watch列表选择clear
listPage_objectSearch_mobileIdentities_right_list_watch_object_posXpath = '//div[4]/div[1]/div[1]/div/div[1]/div[1]/div/ul/li[2]'  # 选择清空object
listPage_object_mobileIdentities_delButton_is_to_be_click_posXpath = '//button[@class="el-button topicCol-btn el-button--default el-button--small"][@id="appDel-_OperateBtns_ElRow_Objects_mobile_identity_Home_App_anonymousComponent"]'  # 断言<delete按钮是否存在>
listPage_object_keywords_delButton_is_to_be_click_posXpath = '//button[@id="appDel-_OperateBtns_ElRow_Objects_keywords_Home_App_anonymousComponent"][@disabled="disabled"]'
listPage_object_mobileIdentities_reference_count_posXpath = main_listPage_object_reference_count_posXpath
listPage_object_clear_count_posXpath = "//*[@id='objectResetBtn-_anonymousComponent_ElForm_anonymousComponent_VPanel_VEditPanel_FqdnDetail_Home_App_anonymousComponent']"  # clear counter 按钮
listPage_object_clear_count_Yes_posXpath = "//div[@class='el-message-box__btns']//span[normalize-space(text())='Yes']"  # clear counter点击后Yes按钮

listPage_object_mobileIdentities_reference_posXpath = '//div[@id="router-view-container"]/div/div[2]/div[1]/div/div/div[2]/div[2]/div[1]/div/div[3]/div'  # 侧滑引用界面
listPage_object_mobileIdentities_reference_close_posXpath = "//button[@id='interceptionadd_allcancelobject1']"  # 侧滑关闭按钮
listPage_object_reprtition_check_postXpath = "//i[@class='operate-icon iconfont icon-jinggao1']"
# '//table/tbody/tr[1]/td[4]/div/div/div/div/div/div[1]/span'  # IMSI提取Details


# Object Mobile Identities===================Object Mobile Identities====================Object Mobile Identities=================Object Mobile Identities=======================Object Mobile Identities=================Object Mobile Identities
# 导入导出文件设置
main_ObjectPage_Input_Import_files_button_posXpath = '//div/button[contains(@class,"Export")]/i'  # main导出文件按钮
mobileIdentitiesObjectPage_Button_Import_Mobile_Identity_files_posXpath = "//button[@class='el-button btn-style el-button--default el-button--small']"  # Create Import Mobile Identity Button
mobileIdentitiesObjectPage_Input_path_Import_Mobile_Identity_files_posXpath = main_ObjectPage_Input_path_Import_files_posXpath  # Create Import Mobile Identity path
main_ObjectPage_Import_Mobile_Identity_files_OK_Button_posXpath = '//div[not(@style="display: none;")]/div/div/div[2]/div[2]/button[1]/span'  # 导入文件OK
mobileIdentitiesObjectPage_Import_Mobile_Identity_files_OK_Button_posXpath = main_ObjectPage_Import_Mobile_Identity_files_OK_Button_posXpath  # 导入文件OK
mobileIdentitiesObjectPage_Import_Mobile_Identity_files_Cancel_Button_posXpath = "//div[5]/div/div[1]/div/div/div[2]/div[2]/button[2]/span"  # 导入文件Cancel
mobileIdentitiesObjectPage_Import_Mobile_Identity_files_IMSI_Group_Cancel_Button_posXpath = '//div[2]/div/div[1]/div/div/div[2]/div[2]/button[2]/span'
main_item_error_format_posXpath = '//div/span[contains(text(),"Format error")]'  # 错误格式提示语
main_Import_files_error_format_posXpath = '//ul/li/div[@class="valid-column import-line"]/span'  # 导入文件格式错误提示语
main_Item_length_error_posXpath = '//div[@class="object-item-error"]/span'  # item 长度校验错误
mobileIdentitiesObjectPage_Import_Mobile_Identity_files_error_format_posXpath = main_Import_files_error_format_posXpath  # mobile identities 导入文件格式错误提示语
main_Import_Mobile_Identity_files_error_type_posXpath = '//div[@class="el-message el-message--error"]/p'  # 错误类型提示语
main_Import_Mobile_Identity_files_item_error_posXpath = '//div/div/div[1]/div[2]/form/div[3]/div/div/div[2]/span'  # 错误item提示语
mobileIdentitiesObjectPage_Import_Mobile_Identity_files_error_type_posXpath = main_Import_Mobile_Identity_files_error_type_posXpath  # mobile identities 错误弹出提示语
main_ObjectPage_import_files_error_type_posXpath = mobileIdentitiesObjectPage_Import_Mobile_Identity_files_error_type_posXpath  # 错误弹出提示语
main_ObjectPage_import_files_error_format_posXpath = mobileIdentitiesObjectPage_Import_Mobile_Identity_files_error_format_posXpath  # 导入文件格式错误提示语
# 置灰按钮
mobileIdentitiesObjectPage_Export_Mobile_Identity_Button_posXpath = '//button[@id="objectExport-_importAndExport_ElRow_Objects_mobile_identity_Home_App_anonymousComponent"][@disabled="disabled"]/i'  # 导出按钮置灰
mobileIdentitiesObjectPage_Edit_Mobile_Identity_Button_posXpath = '//button[@id="appEdit-_OperateBtns_ElRow_Objects_mobile_identity_Home_App_anonymousComponent"][@disabled="disabled"]'  # 编辑按钮置灰
# 删除按钮置灰
main_Delete_Mobile_Identity_Button_posXpath = '//div/div/div[1]/div/div[1]/div/div[3]/button[@disabled="disabled"]'  # 删除按钮置灰
mobileIdentitiesObjectPage_Delete_Mobile_Identity_Button_posXpath = main_Delete_Mobile_Identity_Button_posXpath  # 删除按钮置灰
mobileIdentitiesObjectPage_selete_Mobile_Identity_Button_posXpath = '//table/tbody/tr[1]/td[1]/div/div/div[1]/div/label[@class="el-checkbox"]/span[@class="el-checkbox__input"]'  # 不勾选Object置灰

mobileIdentitiesObjectPage_import_files_Mobile_Identity_Button_posXpath = '//button[@class="el-button el-button--primary el-button--small is-disabled"][@disabled="disabled"]'  # 导入文件按钮置灰
mobileIdentitiesObjectPage_Exclude_Objects_close_Mobile_Identity_Button_posXpath = '//div[@role="switch"][@class="el-switch"]'  # 关闭的Exclude_Objects_close
mobileIdentitiesObjectPage_Exclude_Objects_operation_Mobile_Identity_Button_posXpath = '//div/div/div[1]/div[2]/form/div[4]/div[2]/div/div/span'  # Exclude_Objects开关按钮
mobileIdentitiesObjectPage_Exclude_Objects_open_Mobile_Identity_Button_posXpath = '//div[@role="switch"][@class="el-switch is-checked"]'  # 打开的Exclude_Objects_open
#  置灰按钮
mobileIdentitiesObjectPage_Export_Mobile_Identity_files_OK_Button_posXpath = '//div/button[contains(@class,"Export")]/i'  # 导出文件按钮
mobileIdentitiesObjectPage_Export_Mobile_type_imsi_posXpath = '//label[@id="objectAdd_ip0"]/span'  # imsi展示
mobileIdentitiesObjectPage_Export_Mobile_type_phone_number_posXpath = '//label[@id="objectAdd_ip1"]/span'  # phone_number展示
mobileIdentitiesObjectPage_Export_Mobile_type_imei_posXpath = '//label[@id="objectAdd_ip2"]/span'  # imsi展示
# Object Mobile Identities===================Object Mobile Identities====================Object Mobile Identities=================Object Mobile Identities=======================Object Mobile Identities=================Object Mobile Identities
mobileIdentitiesObjectPage_Import_Mobile_Identity_Group_files_OK_Button_posXpath = "(//div[@class='edit-height'])[4]//span[normalize-space(text())='OK']"  # Group 导入文件OK
# Object Mobile Identities===================Object Mobile Identities====================Object Mobile Identities=================Object Mobile Identities=======================Object Mobile Identities=================Object Mobile Identities
# 查询框输入并选择
listPage_objectSearch_mobileIdentities_select_Id_posXpath = '//li[@id="1-_FilteredSearch_ElRow_Objects_mobile_identity_Home_App_anonymousComponent"]'
listPage_objectSearch_mobileIdentities_select_Name_posXpath = '//li[@id="2-_FilteredSearch_ElRow_Objects_mobile_identity_Home_App_anonymousComponent"]'
listPage_objectSearch_mobileIdentities_select_Details_posXpath = '//li[@id="6-_FilteredSearch_ElRow_Objects_mobile_identity_Home_App_anonymousComponent"]'
listPage_objectSearch_mobileIdentities_select_subType_posXpath = '//li[@id="3-_FilteredSearch_ElRow_Objects_mobile_identity_Home_App_anonymousComponent"]'
listPage_objectSearch_mobileIdentities_select_Description_posXpath = '//li[@id="4-_FilteredSearch_ElRow_Objects_mobile_identity_Home_App_anonymousComponent"]'
listPage_objectSearch_mobileIdentities_select_CreateBy_posXpath = '//*[@id="5-_FilteredSearch_ElRow_Objects_mobile_identity_Home_App_anonymousComponent"]'

listPage_objectSearch_mobileIdentities_buttonSearch_posId = mainPage_ObjectSearch_buttonSearch_posId  # 查询按钮id
listPage_objectSearch_mobileIdentities_buttonClear_posId = mainPage_ObjectSearch_buttonClear_posId  # 清空查询按钮id
listPage_object_mobileIdentities_create_Mobile_Identity_Button_posId = "object0-_OperateBtns_ElRow_Objects_mobile_identity_Home_App_anonymousComponent"  # 创建Mobile Identity
listPage_object_mobileIdentities_create_Mobile_Identity_Group_Button_posId = "object1-_OperateBtns_ElRow_Objects_mobile_identity_Home_App_anonymousComponent"  # 创建Mobile Identity_Group

listPage_profileSearch_mobileIdentities_dropDown_item_posXpath = ""  # 下拉菜单定位
listPage_profileSearch_mobileIdentities_input_itemContent_posXpath = ""  # 输入item的值，replaceName替换实际查询值
listPage_profileSearch_mobileIdentities_dropDown_typeItem_posXpath = ""  # 查询中type的下拉item定位,replaceName替换实际查询值
listPage_profilTable_mobileIdentities_tableTbody_posXpath = ""  # 列表tabel body  xpath
listPage_profilTable_mobileIdentities_tableHeader_posXpath = ""  # 列表table 表头xpath

# listPage->Tips dialog  列表页 tips对话框
listPage_dialogTips_mobileIdentities_button_yes_posCss = ".delComponents-ok span"  # 删除提示的Tips的yes按钮
listPage_dialogTips_mobileIdentities_button_no_posCss = ".delComponents-close span"  # 删除提示的Tips的close按钮
listPage_dialogTips_mobileIdentities_Tips_len_Name_posXpath = '//div/div[1]/div[1]/div/div/div/div[1]/div[2]/form/div[1]/div/div[2]'
listPage_dialogTips_main_Tips_len_Name_posXpath = listPage_dialogTips_mobileIdentities_Tips_len_Name_posXpath
# Mobile_Identities list page 列表页提取元素--列表页
listPage_object_mobileIdentities_new_ID_extract_posXpath = '//table/tbody/tr[1]/td[1]/div/div/div[4]/span'  # 提取ID
listPage_object_mobileIdentities_new_Name_extract_posXpath = '//table/tbody/tr[1]/td[3]/div/div/div/span'  # 提取Name
listPage_object_mobileIdentities_new_Description_extract_posXpath = '//table/tbody/tr[1]/td[6]/div/div/p'  # 提取Description
listPage_object_mobileIdentities_new_Details_extract_posXpath = '//table/tbody/tr[1]/td[4]/div/div/div/div/div/div/span'  # 提取Detail
listPage_object_mobileIdentities_del_after_ele_posXpath = '//div[@id="ly-table1-listcontent"]/div/div[3]/div/span'  # 删除后提示"No Data"
# Mobile_Identities list page 列表页操作
listPage_object_mobileIdentities_select_First_object_posXpath = '//table/tbody/tr[1]/td[1]/div/div/div[1]/div/label/span[1]/span'  # 选择列表中第一个对象

listPage_object_mobileIdentities_select_Second_object_posXpath = main_listPage_object_reference_count_posXpath  # 选择列表中第二个对象

# Create mobile Identities Object 和 Edit mobile Identities Object   新增和编辑页
mobileIdentitiesObjectPage_input_Name_posXpath = "//form/div[1]/div/div[1]/div[1]/input"  # name输入框Xpath
mobileIdentitiesObjectPage_radioButton_IMSI_posId = "IMSIimsi"  # IMSI单选按钮id
mobileIdentitiesObjectPage_input_searchFor_posId = mainPage_ObjectSearch_buttonSearch_Item_posId  # search for item搜索输入框id
mobileIdentitiesObjectPage_button_addItem_posId = mainPage_ObjectSearch_buttonAddItem_posId  # 添加item按钮id
mobileIdentitiesObjectPage_button_inputItem_posId = mainPage_ObjectSearch_input_Item_posId  # 输入item内容

mobileIdentitiesObjectPage_content_inputItem1_posId = '//div[1]/div/div/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div/div/div[1]/span/span'  # 第一行输入item的内容
mobileIdentitiesObjectPage_IMSI_button_Save_Item_posXpath = "//i[@class='operate-icon iconfont icon-save save-color']"  # 创建保存item按钮

mobileIdentitiesObjectPage_IMSI_button_Edit_Save_Item_posXpath = '//div[@class="item-box"]//i[contains(@class,"icon-save")]'  # 编辑保存item按钮
mobileIdentitiesObjectPage_IMSI_button_Edit_assert_first_Item_content_posXpath = "//div[@class='object-item-box']//div[@class='item-box']/div/div[1]/span/span"  ## <断言>第一个item的内容
mobileIdentitiesObjectPage_IMSI_button_Edit_assert_first_Item_count_posXpath = "//div[@class='item-container']//div[@class='total']"  ## <断言>新增item的个数

mobileIdentitiesObjectPage_sub_Phone_Number_button_Edit_assert_first_Item_count_posXpath = "//div[@class='CommonSubObjects']/div[2]/div[2]"  # sub Phone_Number<断言>新增item的个数

mobileIdentitiesObjectPage_radioButton_phone_number_posId = "Phone Numberphone_number"  # Phone Number单选按钮id
mobileIdentitiesObjectPage_Phone_Number_button_Save_phone_number_Item_posXpath = "//i[@class='operate-icon iconfont icon-save save-color']"  # 保存item按钮
mobileIdentitiesObjectPage_Phone_Number_button_inputItem_posXpath = "//div[@class='expr-box']//input[@class='el-input__inner']"  # 输入Phone_item内容
mobileIdentitiesObjectPage_Phone_Number_button_input_more_Item_posXpath = "(//div[@class='TextExpr expr-item']//input[@class='el-input__inner'])['replace']"  # 输入Phone_item内容 多次输入

mobileIdentitiesObjectPage_Phone_Number_button_add_Item_input_posXpath = '//div[@class="addobject width300px addobject-long-list obj-content-null cursorPointer borderColor add-btn"]'

mobileIdentitiesObjectPage_radioButton_IMEI_posId = "IMEIimei"  # IMEI单选按钮id
mobileIdentitiesObjectPage_IMEI_button_inputItem_posID = mainPage_ObjectSearch_input_Item_posId
mobileIdentitiesObjectPage_IMEI_button_Save_Item_posXpath = '//div[@class="item-box"]//i[contains(@class,"icon-save")]'  # 保存item按钮

mobileIdentitiesObjectPage_textArea_Description_posXpath = "//div[@class='objectAdd_description el-textarea el-input--small']/textarea"  # description文本输入区Xpath
mobileIdentitiesObjectPage_button_SaveYes_posXpath = "//button[@id='OK-_mobileIdDetail_Home_App_anonymousComponent']/span"  # OK按钮
mobileIdentitiesObjectPage_button_warningSaveYes_posXpath = "//div[@class='el-message-box__wrapper']/div/div[3]/button[2]/span"  # 提示保存ok按钮警告框
mobileIdentitiesObjectPage_button_warningSaveCancel_posCss = '//div[@class="el-message-box__wrapper"]/div/div[3]/button[1]/span'  # 提示保存取消按钮警告框
mobileIdentitiesObjectPage_button_cancel_posXpath = "//button[@id='Cancle-_mobileIdDetail_Home_App_anonymousComponent']/span"  # Cancel按钮
# Audit ele
mobileIdentitiesObjectPage_button_audit_button_posXpath = '//div[@class="paper-grid-right"]//span[normalize-space(text())="Audit Logs"][1]'  # create audit button
mobileIdentitiesObjectPage_button_audit_first_object_posXpath = '//table/tbody/tr'  ## create audit first ele
mobileIdentitiesObjectPage_button_audit_second_posXpath = '//table/tbody/tr[2]/td[3]/div'  ## create audit second ele
## Audit ele
# Create mobile Identities Group Object 和 Edit Create mobile Identities Group   新增和编辑页
mobile_Identities_Group_sub_Object_addButton_posXpath = "//div[@class='CommonSubObjects']//i[@class='iconfont icon-Create1 cursor']"  # mobile_Identities_Group添加sub Object按钮

mobile_Identities_Group_sub_Object_input_frame_posXpath = main_Group_sub_Object_input_frame_posXpath  # sub Object 搜索输入框

mobile_Identities_Group_sub_Object_input_frame_select_one_posXpath = main_Group_sub_Object_input_frame_select_one_posXpath  # 搜索框第一个元素
mobile_Identities_Group_confirm_leave_posXpath = '//div/div[3]/button[2]/span[contains(text(),"OK")]'  # 确认离开
mobile_Identities_Group_sub_Object_Edit_Button_posXpath = "//div[@class='object-item-box']//div[@class='OperateBtn']/i"  # mobile_Identities_Group编辑sub Object按钮
mobile_Identities_Group_sub_Object_add_new_Button_posXpath = "//div/div/div[2]/div/div[1]/div/div/div/div[2]/div[1]/div/div[1]/div[2]/div/div/button/i"  # 新建sub_mobile_Identities按钮
mobile_Identities_Group_sub_Object_add_new_Select_one_Button_posXpath = "//ul[@x-placement='bottom-start']/li[1]"  # 新建选择mobile_Identities按钮
mobile_Identities_Group_sub_Object_add_new_Select_Group_Button_posXpath = "//ul[@x-placement='bottom-start']/li[2]"  # 新建选择mobile_Identities_Group按钮
mobile_Identities_Group_sub_Object_add_new_one_inputName_posXpath = '//div/div/div[1]/div/div/div[1]/div[1]/div/div/div/div[1]/div[2]/form/div[1]/div/div[1]/div[1]/input'  # new mobile_Identities input Name
mobile_Identities_Group_sub_Object_add_new_add_item_Button_posXpath = "(//div[@class='object-item-add'])[2]/div"  # new mobile_Identities add items
mobile_Identities_Group_sub_Object_add_new_addIMSI_item_inputName_posXpath = "//input[@id='onlyMarvel']"  # new IMSI inputItemName
mobile_Identities_Group_sub_Object_add_new_addphoneNumber_item_inputName_posXpath = "//div[@class='expr-box']//input[@class='el-input__inner']"  # new PhoneNumber inputItemName
mobile_Identities_Group_sub_Object_add_new_addIMEI_item_inputName_posXpath = '//input[@id="onlyMarvel"]'  # new IMEI inputItemName
mobile_Identities_Group_sub_Object_add_new_add_itemIMSI_Save_Button_posXpath = "//i[@class='operate-icon iconfont icon-save save-color']"  # 保存item按钮
mobile_Identities_Group_sub_Object_add_new_add_item_phoneNumber_Save_Button_posXpath = "//i[@class='operate-icon iconfont icon-save save-color']"
mobile_Identities_Group_sub_Object_add_new_add_item_IMEI_Save_Button_posXpath = "//i[@class='operate-icon iconfont icon-save save-color']"

mobile_Identities_Group_sub_Object_add_new_one_OK1_Button_posXpath = '//div/div/div[2]/div/div/div[1]/div/div/div[1]/div[3]/button[1]/span'  # new mobile_Identities CreateOK1
mobile_Identities_Group_sub_Object_add_new_one_OK1_Warning_Yes_Button_posXpath = '//div[@class="el-message-box__wrapper"]/div/div[3]/button[2]/span'  # 再次确认创建new mobile_Identities
mobile_Identities_Group_sub_Object_add_new_one_OK1_Warning_Cancel_Button_posXpath = '//div[@class="el-message-box__wrapper"]/div/div[3]/button[1]/span'  # 再次确认取消new mobile_Identities
mobile_Identities_Group_sub_Object_add_new_one_Cancel2_Button_posXpath = '//div/div/div[2]/div/div/div[1]/div/div/div[1]/div[3]/button[2]/span'  # new mobile_Identities CreateCancel2
mobile_Identities_Group_sub_Object_add_first_posXpath = '//div/div[2]/div/div[1]/div/div/div/div[2]/div[1]/div/div[2]/div/ul/li[1]/div[2]'  # 添加subObject索引框第一个元素
# Mobile_Identities
# Object Mobile Identities===================Object Mobile Identities====================Object Mobile Identities=================Object Mobile Identities=======================Object Mobile Identities=================Object Mobile Identities


# Object URLs elements area top===================Object URLs elements area top===================Object URLs elements area top===================Object URLs elements area top===================Object URLs elements area top===================Object URLs elements area top
# Object URLs elements area top===================Object URLs elements area top===================Object URLs elements area top===================Object URLs elements area top===================Object URLs elements area top===================Object URLs elements area top
# 全局页面
mainPage_rightTopTips_closeButton_posXpath = '(//i[@class="iconfont icon-Delete_X"])[last()]'  # 全局右上提示窗关闭按钮（最新的一个）
##URLs列表页
listPage_object_urls_createButton_posId = 'objectCreate-_OperateBtns_ElRow_Objects_url_Home_App_anonymousComponent'  # Create按钮id
listPage_object_urls_createButton_url_posId = 'object0-_OperateBtns_ElRow_Objects_url_Home_App_anonymousComponent'  # Create下的URL选项id
listPage_object_urls_createButton_urlGroup_posId = 'object1-_OperateBtns_ElRow_Objects_url_Home_App_anonymousComponent'  # Create下的URL Group选项id
listPage_object_urls_editButton_posId = 'appEdit-_OperateBtns_ElRow_Objects_url_Home_App_anonymousComponent'  # Edit 按钮id
listPage_object_urls_delButton_posId = 'appDel-_OperateBtns_ElRow_Objects_url_Home_App_anonymousComponent'  # Delete 按钮id
url_listPage_deleteButton_posId = 'appDel-_OperateBtns_ElRow_Objects_url_Home_App_anonymousComponent'  # Delete 按钮id
url_listPage_first_row_checkBox_posXpath = '(//td[@rowspan="1"and @colspan="1"]//span[@class="el-checkbox__inner"])[1]'  # 列表页第一行对象多选框Xpath
# listPage_object_urls_columnSetting_descriptionOption_posXpath = '//ul[@class="col-choose open"]//span[text()="Description"]'  # 列设置中的description选项元素Xpath
listPage_object_urls_columnSetting_descriptionOption_posXpath = '//li[contains(@id,"dropColRes-_ElementSet")]//span[normalize-space(text())="Description"]'  # 列设置中的description选项元素Xpath
listPage_object_urls_tableDetails_posXpath = '//div[@class="el-table__header-wrapper"]//span[contains(text(),"Details")]'  # list表头 Details列Xpath
# listPage_object_urls_tableDetails_selected_detailsRow_posXpaths = '//span[@class="el-checkbox__input is-checked"]/ancestor::tr//div[@class="itemDetails cursor"]/span'  # list页被选中的对象details 值Xpath
# listPage_object_urls_tableDetails_selected_detailsRow_posXpaths = '//span[@class="el-checkbox__input is-checked"]/ancestor::tr//div[@class="itemDetails cursor"]/..'  # list页被选中的对象details 值Xpath
listPage_object_urls_tableDetails_selected_detailsRow_posXpaths = '//span[@class="el-checkbox__input is-checked"]/ancestor::tr//div[@class="itemDetails cursor"]'  # list页被选中的对象details 值Xpath
listPage_object_urls_tableDetails_detailsRow_firstDetailValue_posXpaths = '//div[@class="itemDetails cursor"][1]/span'  # 列表页某行第一个details值 Xpath
listPage_object_urls_tableDetails_selected_checkBox_posXpaths = '//div[@class="ly-table1"]//span[@class="el-checkbox__input is-checked"]'  # list页被选中的对象 CheckBox Xpath
listPage_object_urls_tableDetails_firstRowValues_span_posXpaths = '//li[@class="row el-dropdown-menu__item"]//span[@class="ellipsis list-popover"]'  # list页点击Details后展示的数据Xpaths_span
listPage_object_urls_tableDetails_firstRowValues_div_posXpaths = '//li[@class="row el-dropdown-menu__item"]//div[@class="row-content-cell"]'  # list页点击Details后展示的数据Xpaths_div
listPage_object_urls_importButton_posXpath = '//div[@class="ly-tablecontrol-1 el-row"]//div[@class="functional"]//i[@class="iconfont icon-Import"]'  # 导入文件按钮 Xpath
listPage_object_urls_exportButton_posXpath = '//button[contains(@class,"importAndExport")]'  # 导出文件按钮 Xpath
listPage_object_urls_exportPopYes_posXpath = '//div[@class="el-dialog__wrapper"]/div[@aria-label="Export"]//span[contains(text(),"Yes")]'  # 导出数据选择确认弹窗 yes Xpath
listPage_object_urls_exportPopNo_posXpath = '//div[@class="el-dialog__wrapper"]/div[@aria-label="Export"]//span[contains(text(),"No")]'  # 导出数据选择确认弹窗 no Xpath
listPage_object_urls_exportPopSelectAll_posXpath = '//div[@class="el-table__header-wrapper"]//span[@class="el-checkbox__inner"]'  # 导出数据选择确认弹窗全选CheckBox Xpath
listPage_object_urls_exportPopCheckbox_posXpaths = '//div[@class="el-dialog__body"]//div[@class="el-table__body-wrapper is-scrolling-none"]//span[@class="el-checkbox__inner"]'  # 导出数据选择确认弹窗CheckBox(多个)
listPage_object_urls_clearCounterPopYes_posXpath = '//*[contains(text(),"Confirm to Clear Counter")]/../..//span[contains(text(),"Yes")]'  # Clear Counter 选择确认弹窗中的Yes确认按钮
# listPage_object_urls_tableCheckbox_posXpaths = '//table[@class="el-table__body"]//span[@class="el-checkbox__inner"]'  # 列表页CheckBox（50）
listPage_object_urls_tableCheckbox_posXpaths = '//table[@class="el-table__body"]//span[@class="el-checkbox__input"]'  # 列表页CheckBox（50）
# listPage_object_urls_tableCheckbox_singleObject_posXpaths = '//span[contains(@class,"name-fontFamily")]/preceding-sibling::i[not(contains(@class,"icon-URLgroup"))]/ancestor::tr//span[@class="el-checkbox__inner"]'  # 列表页CheckBox（50）
# listPage_object_urls_tableCheckbox_singleObject_posXpaths = '//span[contains(@class,"name-fontFamily")]/preceding-sibling::i[not(contains(@class,"group"))]/ancestor::tr//span[@class="el-checkbox__inner"]'  # 列表页CheckBox（50），不包含Object Group和锁定对象
# listPage_object_urls_tableCheckbox_objectGroup_posXpaths = '//i[contains(@class,"icon-URLgroup")]/ancestor::tr//span[@class="el-checkbox__inner"]'  # 列表页对象组的CheckBox（多个）
# listPage_object_urls_tableCheckbox_objectGroup_posXpaths = '//i[contains(@class,"group")]/ancestor::tr//span[@class="el-checkbox__inner"]'  # 列表页对象组的CheckBox（多个）
listPage_object_urls_tableCheckbox_objectGroup_posXpaths = \
    '(//*[contains(@class,"table-status-item-id")]/preceding-sibling::div[2][not(*)]/ancestor::tr//*[contains(@class,"name-fontFamily")]/preceding-sibling::i[(contains(@class,"group"))]/ancestor::tr//span[@class="el-checkbox__inner"])'  # 列表页Object Group 的CheckBoxs(不包含single Object和锁定对象)
listPage_object_urls_tableCheckbox_notLocalVsys_objectOrGroup_posXpaths = '//div[@class="table-status-box"]/div[2]//*[contains(@class,"icon-lock")]/ancestor::tr//span[@class="el-checkbox__inner"]'  # 列表页中不是本Vsys的对象或对象组的CheckBox
listPage_object_urls_tableDetails_singleObject_posXpaths = '//span[contains(@class,"name-fontFamily")]/preceding-sibling::i[not(contains(@class,"icon-URLgroup"))]/ancestor::tr//div[@class="itemDetails cursor"]/..'  # 列表页中所有对象（不包含对象组）的DetailsXpath
# listPage_object_urls_tableDetails_firstSingleObject_posXpath = '(//span[contains(@class,"name-fontFamily")]/preceding-sibling::i[not(contains(@class,"group"))]/ancestor::tr//span[@class="el-checkbox__inner"])[1]'  # 列表页中第一个Object 的CheckBox
listPage_object_urls_tableCheckbox_singleObject_posXpaths = \
    '(//*[contains(@class,"table-status-item-id")]/preceding-sibling::div[2][not(*)]/ancestor::tr//*[contains(@class,"name-fontFamily")]/preceding-sibling::i[not(contains(@class,"group"))]/ancestor::tr//span[@class="el-checkbox__inner"])'  # 列表页中Object 的CheckBoxs(不包含Group和锁定对象)
listPage_object_urls_tableDetails_firstSingleObject_posXpath = \
    '(//*[contains(@class,"table-status-item-id")]/preceding-sibling::div[2][not(*)]/ancestor::tr//*[contains(@class,"name-fontFamily")]/preceding-sibling::i[not(contains(@class,"group"))]/ancestor::tr//span[@class="el-checkbox__inner"])[1]'  # 列表页中第一个Object 的CheckBox(不包含Group和锁定对象)

# listPage_object_urls_tableDetails_firstObjectGroup_posXpath = '(//i[contains(@class,"group")]/ancestor::tr//span[@class="el-checkbox__inner"][1])'  # 列表页中第一个Object Group 的CheckBox
listPage_object_urls_tableDetails_firstObjectGroup_posXpath = \
    '(//*[contains(@class,"table-status-item-id")]/preceding-sibling::div[2][not(*)]/ancestor::tr//*[contains(@class,"name-fontFamily")]/preceding-sibling::i[(contains(@class,"group"))]/ancestor::tr//span[@class="el-checkbox__inner"])[1]'  # 列表页中第一个Object Group 的CheckBox(不包含single Object和锁定对象)
listPage_object_urls_tableCheckbox_firstNotLocalVsys_objectOrGroup_posXpath = '(//div[@class="table-status-box"]/div[2]//*[contains(@class,"icon-lock")]/ancestor::tr//span[@class="el-checkbox__inner"])[1]'  # 列表页中第一个不是本Vsys的对象或对象组的CheckBox

listPage_object_urls_tableCheckbox_localVsys_objectOrGroup_posXpaths = '//*[contains(@class,"table-status-item-id")]/preceding-sibling::div[2][not(*)]/ancestor::tr//span[@class="el-checkbox__inner"]'# 列表页中本Vsys的Object 或Group（不包含其他Vsys）
listPage_object_urls_tableCheckbox_localVsys_firstObjectOrGroup_posXpath = '(//*[contains(@class,"table-status-item-id")]/preceding-sibling::div[2][not(*)]/ancestor::tr//span[@class="el-checkbox__inner"])[1]'# 列表页中第一个本Vsys的Object 或Group（不包含其他Vsys）
url_listPage_usage_policies_elems_posXpaths = "//div[contains(@class,'LocalationDraswer ')]//div[contains(@class,'el-dropdown-menu')]"  # 点击Reference count后展开的侧滑页面，其中的引用条数

url_listPage_noDataText_posXpath = '//div[@class="ly-table1"]//span[@class="el-table__empty-text"]'  # 列表页无数据时的no data文本 Xpath
# listPage->Tips dialog  列表页 tips对话框
listPage_object_urls_button_yes_posCss = 'body>.el-dialog__wrapper .delComponents-ok span'  # 删除提示的Tips的yes按钮Xpath
url_listPage_object_delete_yesButton_posCss ='body>.el-dialog__wrapper .delComponents-ok span'  # 删除提示的Tips的yes按钮Xpath
url_listPage_object_urls_delete_noButton_posCss = 'body>.el-dialog__wrapper .delComponents-close span'  # 删除提示的Tips的No按钮Xpath
listPage_object_urls_button_no_posCss = 'body>.el-dialog__wrapper .delComponents-close span'  # 删除提示的Tips的No按钮Xpath

# 列表页搜索选项
listPage_object_urls_fuzzySearch_posXpath = '//div[@class="el-scrollbar"]//li[@class="el-select-dropdown__item flex" and not(@id)]'  # 模糊搜索
listPage_object_urls_searchId_posId = '1-_FilteredSearch_ElRow_Objects_url_Home_App_anonymousComponent'  # ID 搜索
listPage_object_urls_searchName_posId = '2-_FilteredSearch_ElRow_Objects_url_Home_App_anonymousComponent'  # name 搜索
listPage_object_urls_searchDetails_posId = '6-_FilteredSearch_ElRow_Objects_url_Home_App_anonymousComponent'  # details搜索
listPage_object_urls_searchDescription_posId = '4-_FilteredSearch_ElRow_Objects_url_Home_App_anonymousComponent'  # Description 搜索
listPage_object_urls_searchCreatedBy_posId = '5-_FilteredSearch_ElRow_Objects_url_Home_App_anonymousComponent'  # created by 搜索

# URLs对象详情页
url_ObjectDetailPage_nameInput_posXpath = '//div[@class="rel-input el-input el-input--mini"]/input'  # Name输入框Xpath
url_ObjectDetailPage_nameLenthNumber_posXpath = '//*[@class="VEditPanel"]//*[@class="biFangNameLength-length"]'  # Name输入框中字符长度数值Xpath
url_ObjectDetailPage_addButton_posId = 'temporary_form'  # “+”按钮id
url_ObjectDetailPage_item_subAddButton_poXpath = '//*[@class="item-box"]//*[contains(@class,"add-btn")]'  # 单个Item中新增多条数据的"+"按钮
# url_ObjectDetailPage_itemValue_posXpath = '//*[@id="router-view-container"]/div/div[1]/div[1]/div/div/div/div[1]/div[2]/form/div[3]/div/div/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div/input'  # Item value输入框Xpath
url_ObjectDetailPage_itemValue_posXpath = '//*[@class="CommonItems"]//*[@class="edit-row"]//*[@class="el-input__inner"]'  # Item value输入框Xpath
# url_ObjectDetailPage_itemSaveButton_posXpath = '//div[@class="row-header"]/div[2]'  # 保存按钮Xpath
url_ObjectDetailPage_itemSaveButton_posXpath = '//div[@class="item-box"]//i[contains(@class,"icon-save")]'  # item 下value保存按钮Xpath
url_ObjectDetailPage_subObjectAddButton_posXpath = '//div[@class="AddButton"]/div/i'  # Subordinate Objects + 按钮Xpath
url_ObjectDetailPage_subObjectAddButtonWhenHadData_posXpath = '//*[@data-desc="subObject"]//*[@class="operate-icon iconfont icon-Create1"]'  # 有数据时Subordinate Objects + 按钮Xpath
url_ObjectDetailPage_firstUrlObject = '//ul[@class="row-container tableList"]/li[1]/div[2]/span'  # URL Object中第一个url Xpath
url_ObjectDetailPage_secondUrlObject = '//ul[@class="row-container tableList"]/li[2]/div[2]/span'  # URL Object中第二个url Xpath
url_ObjectDetailPage_description_posXpath = '//textarea[@class="el-textarea__inner"]'  # Description textarea Xpath
url_ObjectDetailPage_object_ip_search_posId = 'object_ip_search'  # url item 搜索框id
url_ObjectDetailPage_urlDelCross_posXpath = '//i[@class="operate-icon iconfont icon-Delete_X del"]'  # url item "X"按钮Xpath
url_ObjectDetailPage_auditLogs_posXpath = '//div[@class="audit_log"]/span'  # Audit Logs Xpath
url_ObjectDetailPage_auditLogsDrawer_firstRowLog_checkBox_posXpath = '(//div[@class="LocalationDraswer lstsub right-show-edit right-show-edit-other"]//table[@class="el-table__body"]//span[@class="el-checkbox__input"])[1]'  # Audit Logs 侧滑页第一条日志CheckBox Xpath
url_ObjectDetailPage_auditLogsDrawer_compareButton_posXpath = '//div[@class="LocalationDraswer lstsub right-show-edit right-show-edit-other"]//button[contains(@id,"test-compare-_")]'  # Audit Logs 侧滑页Compare 按钮Xpath
url_ObjectDetailPage_auditLogsDrawer_compareDrawer_operationText_posXpath = '//div[contains(text(),"Operation")]/following-sibling::div'  # Audit Logs 侧滑页点击Compare后的 operation text Xpath
url_ObjectDetailPage_itemsTotal_posXpath = '//div[@class="panel-content"]//div[@class="total"]'  # Items Total Xpath
url_ObjectDetailPage_importFromFile_posXpath = '//span[contains(text(),"Import From File")]'  # Import From File 按钮Xpath
url_ObjectDetailPage_importFromFile_button_posXpath = '//span[contains(text(),"Import From File")]/..'  # Import From File 按钮Xpath
# url_ObjectDetailPage_pleaseUpload_posXpath = '//span[contains(text(),"Please Upload")]/../../input'  # Please Upload input标签Xpath
url_ObjectDetailPage_pleaseUpload_posXpath = '//span[contains(text(),"Please Upload")]/ancestor::div[@class="el-upload el-upload--text"]//input'  # Please Upload input标签Xpath
url_ObjectDetailPage_importUrlOk_posXpath = '//button[contains(@class,"import-ok")]'  # Import URL 下的OK按钮Xpath

url_ObjectDetailPage_importedFile_posXpath = '//ul[@class="el-upload-list el-upload-list--text"]/li'  # 导入文件元素位置（Import From File 按钮旁）
url_ObjectDetailPage_importedFile_delete_posXpath = '//i[@class="el-icon-close fontsize18"]'  # 文件删除按钮
url_ObjectDetailPage_importedFile_download_posXpath = '//i[@class="iconfont icon-DownNormal fontsize16"]'  # 文件下载按钮

# Create URL Group对象详情页
urlGroup_ObjectDetailPage_addButton_posId = 'temporary_form'  # Subordinate Objects下 “+”按钮id
urlGroup_ObjectDetailPage_description_posXpath = '(//div[@class="objectAdd_description el-textarea el-input--small"])[1]'  # Description textarea Xpath
urlGroup_ObjectDetailPage_subAddButton_posXpath = '//div[@class="CreateBtn rm-search-button"]/div/button'  # Subordinate Objects下点击 “+”按钮后，新建url项目中的“+”元素Xpath
url_ObjectGroupDetailPage_subObjects_addButton_newAdd_posXpath = '//div[@data-desc="subObject"]//div[@class="AddButton"]'  # Subordinate Objects 下无数据新增时"+"按钮Xpath
urlGroup_ObjectDetailPage_subUrl_posXpath = "(//ul[starts-with(@id ,'dropdown-menu')]//li[1])[last()]"  # 子+下的Url选项
urlGroup_ObjectDetailPage_subNameInput_posXpath = '(//div[@class="rel-input el-input el-input--mini"]/input)[last()]'  # 子Name输入框Xpath
urlGroup_ObjectDetailPage_subSubAddButton_posXpath = '(//div[@id="temporary_form"])[last()]'  # 子“+”按钮Xpath
urlGroup_ObjectDetailPage_subItemSearch_posXpath = '//div[@class="right-menu-content"]//input[@id="object_ip_search"]'  # 侧滑Item栏搜索框Xpath
# urlGroup_ObjectDetailPage_subItemSearch_posXpath = '//div[@class="EditDraw"]//input[@id="object_ip_search"][1]' # 侧滑Item栏搜索框Xpath
urlGroup_ObjectDetailPage_subTotalField_posXpath = '//div[@class="ToggleDraw"]//p[contains(text(),"Total")]'  # 侧滑Total:xx 元素Xpath
# urlGroup_ObjectDetailPage_subTotalField_posXpath = '//*[@class="EditDraw"]//div[@class="drawer-box"]//div[@class="panel-content"]//*[contains(text(),"Total")]' # 侧滑Total:xx 元素Xpath
urlGroup_ObjectDetailPage_subItemValue_posXpath = '//div[@class="item-box"]//input'  # 子Item value输入框Xpath
urlGroup_ObjectDetailPage_subItemSaveButton_posXpath = '//div[@class="row-header"]/div[2]'  # 子保存按钮Xpath
urlGroup_ObjectDetailPage_subDescription_posXpath = '(//textarea[@class="el-textarea__inner"])[last()]'  # 子Description textarea Xpath
urlGroup_ObjectDetailPage_subOkButton_posId = 'OK-_URLDetail_VDraswer_EditDraw_URLDetail_Home_App_anonymousComponent'  # 子“OK”按钮id
urlGroup_ObjectDetailPage_subOkButton_yes_posXpath = ''  # 子确认弹窗的“Yes”按钮
url_ObjectDetailPage_subImportUrlOk_posXpath = '(//button[contains(@class,"import-ok")])[last()]'  # 子Import URL 下的OK按钮Xpath
urlGroup_ObjectDetailPage_subObjectEdit_posXpath = '//div[@class="infinite-list-wrapper"]//div[@class="OperateBtn"]'  # 编辑object group 中编辑object的编辑按钮Xpath
urlGroup_ObjectDetailPage_excludeObjectsSwitch_posXpath = '//div[@data-desc="exclude subObject"]//div[@role="switch"]'  # Exclude Objects Switch Xpath
urlGroup_ObjectDetailPage_excludeObjectsSwitch_newAdd_posXpath = '//div[@data-desc="exclude subObject"]//i[@class="iconfont icon-Create1 cursor"]'  # Exclude Objects无数据时新增按钮Xpath
urlGroup_ObjectDetailPage_excludeObjectsSwitch_normalAdd_posXpath = '//div[@data-desc="exclude subObject"]//div[@id="temporary_form"]'  # Exclude Objects有数据时新增按钮Xpath
urlGroup_ObjectDetailPage_excludeObjects_itemsArea_posXpath = '//div[@data-desc="exclude subObject"]//div[@class="CommonSubObjects"]'  # Exclude Objects下的item区域div Xpath
url_ObjectGroupDetailPage_subObjects_toggleDraw_closeButton_posXpath = '//div[contains(@class,"list-box")]//button[contains(@class,"right-menu-button-close")]'  # url侧滑窗口的Close按钮
url_ObjectDetailPage_clearCounter_posXpath = '//button[contains(@id,"objectResetBtn-_anonymousComponent_ElForm_anonymousComponent_VPanel_VEditPanel_")]'  # Clear Counter按钮

url_ObjectDetailPage_okButton_posId = 'OK-_URLDetail_Home_App_anonymousComponent'  # “OK”按钮id
url_ObjectDetailPage_cancelButton_posId = 'Cancle-_URLDetail_Home_App_anonymousComponent'  # “Cancel”按钮id
url_ObjectDetailPage_okButton_yes_posXpath = '//div[@class="el-message-box__btns"]//button[contains(@class,"operation-confirm")]'  # 确认弹窗的“Yes”按钮
url_ObjectDetailPage_okButton_cancel_posXpath = '//div[@class="el-message-box__btns"]//button[contains(@class,"operation-cancel")]'  # 确认弹窗的“Cancel”按钮
# Object URLs elements area bottom===================Object URLs elements area bottom===================Object URLs elements area bottom===================Object URLs elements area bottom===================Object URLs elements area bottom
# Object URLs elements area bottom===================Object URLs elements area bottom===================Object URLs elements area bottom===================Object URLs elements area bottom===================Object URLs elements area bottom
# Object IP address===================Object IP address====================Object IP address=================Object IP address=======================Object IP address=================Object IP address
# Mobile_Identities list page 列表页
listPage_object_ip_address_createButton_posId = "objectCreate-_OperateBtns_ElRow_Objects_ip_Home_App_anonymousComponent"  # create按钮id
listPage_object_ip_address_editButton_posId = "appEdit-_OperateBtns_ElRow_Objects_ip_Home_App_anonymousComponent"  # edit按钮id
listPage_object_ip_address_delButton_disable_posXpath = '//button[@id="appDel-_OperateBtns_ElRow_Objects_ip_Home_App_anonymousComponent"][@disabled="disabled"]'  # del按钮Xpath置灰
listPage_object_ip_address_delButton_posId = "appDel-_OperateBtns_ElRow_Objects_ip_Home_App_anonymousComponent"  # del按钮id
listPage_object_ip_address_del_yes_Button_posXpath = '//div/div[@aria-label="Tips"]/div[3]/span/button[1]/span'  # del_yes按钮
listPage_objectSearch_ip_address_selectLabel_posId = mainPage_ObjectSearch_selectLabel_posId  # 查询框id
# 查询框输入并选择
listPage_objectSearch_ip_address_select_Id_posXpath = '//li[@id="1-_FilteredSearch_ElRow_Objects_ip_Home_App_anonymousComponent"]'  # 查询ID
listPage_objectSearch_ip_address_select_Name_posXpath = '//li[@id="2-_FilteredSearch_ElRow_Objects_ip_Home_App_anonymousComponent"]'  # 查询Name
listPage_objectSearch_ip_address_select_Details_posXpath = '//li[@id="6-_FilteredSearch_ElRow_Objects_ip_Home_App_anonymousComponent"]'  # 查询Details
listPage_objectSearch_ip_address_select_subType_posXpath = '//li[@id="3-_FilteredSearch_ElRow_Objects_ip_Home_App_anonymousComponent"]'  # 查询SubType
listPage_objectSearch_ip_address_select_Description_posXpath = '//li[@id="4-_FilteredSearch_ElRow_Objects_ip_Home_App_anonymousComponent"]'  # 查询Description
listPage_objectSearch_ip_address_select_CreateBy_posXpath = '//*[@id="5-_FilteredSearch_ElRow_Objects_ip_Home_App_anonymousComponent"]'  # 查询CreateBy
listPage_objectSearch_geo_select_IP_posXpath = "//li[@id='100-_FilteredSearch_ElRow_Geography_List_Home_App_anonymousComponent']"
listPage_objectSearch_geo_select_GeoNameID_posXpath = "//li[@id='56-_FilteredSearch_ElRow_Geography_List_Home_App_anonymousComponent']"
listPage_objectSearch_geo_select_CountryAbbreviation_posXpath = "//li[@id='156-_FilteredSearch_ElRow_Geography_List_Home_App_anonymousComponent']"
listPage_objectSearch_geo_select_CountryandRegion_posXpath = "//li[@id='58-_FilteredSearch_ElRow_Geography_List_Home_App_anonymousComponent']"
listPage_objectSearch_geo_select_SuperAdministrativeArea_posXpath = "//li[@id='150-_FilteredSearch_ElRow_Geography_List_Home_App_anonymousComponent']"
listPage_objectSearch_geo_select_AdministrativeArea_posXpath = "//li[@id='59-_FilteredSearch_ElRow_Geography_List_Home_App_anonymousComponent']"
listPage_objectSearch_geo_select_SubAdministrativeArea_posXpath = "//li[@id='151-_FilteredSearch_ElRow_Geography_List_Home_App_anonymousComponent']"





listPage_objectSearch_ip_address_buttonSearch_posId = mainPage_ObjectSearch_buttonSearch_posId  # 查询按钮id
# main_Export_ObjectPage_Button_posXpath = '//div/button[contains(@class,"Export")]/i' # 导出按钮
main_Export_ObjectPage_Button_posXpath = '//button[contains(@class,"Export")]'  # 导出按钮
listPage_objectSearch_ip_address_buttonClear_posId = mainPage_ObjectSearch_buttonClear_posId  # 清空查询按钮id
listPage_object_ip_address_create_ip_address_Button_posId = 'object0-_OperateBtns_ElRow_Objects_ip_Home_App_anonymousComponent'  # 创建IP Address
listPage_object_ip_address_create_ip_address_Group_Button_posId = "object1-_OperateBtns_ElRow_Objects_ip_Home_App_anonymousComponent"  # 创建IP Address_Group

listPage_profileSearch_ip_address_dropDown_item_posXpath = ""  # 下拉菜单定位
listPage_profileSearch_ip_address_input_itemContent_posXpath = ""  # 输入item的值，replaceName替换实际查询值
listPage_profileSearch_ip_address_dropDown_typeItem_posXpath = ""  # 查询中type的下拉item定位,replaceName替换实际查询值
listPage_profilTable_ip_address_tableTbody_posXpath = ""  # 列表tabel body  xpath
listPage_profilTable_ip_address_tableHeader_posXpath = ""  # 列表table 表头xpath

# ip_address list page 列表页提取元素--列表页
listPage_object_ip_address_new_ID_extract_posXpath = '//table/tbody/tr[1]/td[1]/div/div/div[4]/span'  # 提取ID
listPage_object_ip_address_new_Name_extract_posXpath = '//table/tbody/tr[1]/td[3]/div/div/div/span'  # 提取Name
listPage_object_ip_address_new_Description_extract_posXpath = '//table/tbody/tr[1]/td[6]/div/div/p'  # 提取Description
listPage_object_ip_address_new_Details_extract_posXpath = '//table/tbody/tr[1]/td[4]/div/div/div/div/div/div/span'  # 提取Detail
listPage_object_ip_address_del_after_ele_posXpath = '//div[@id="ly-table1-listcontent"]/div/div[3]/div/span'  # 删除后提示"No Data"
# ip_address list page 列表页操作
listPage_object_ip_address_select_First_object_posXpath = '//table/tbody/tr/td[1]/div/div/div[1]/div/label/span[1]/span'  # 选择列表中第一个对象

# Create IP Address Object 和 Edit IP Address Object   新增和编辑页
ip_addressObjectPage_input_Name_posXpath = "//form/div[1]/div/div[1]/div[1]/input"  # name输入框Xpath
ip_addressObjectPage_radioButton_IP_posId = "IPendpoint"  # IP单选按钮id
ip_addressObjectPage_input_searchFor_posId = mainPage_ObjectSearch_buttonSearch_Item_posId  # search for item搜索输入框id
ip_addressObjectPage_button_addItem_posId = mainPage_ObjectSearch_buttonAddItem_posId  # 添加item按钮id
ip_addressObjectPage_button_addItem_first_item_posXpath = "//div[@class='item-box']/div/div/span[1]"  # item 搜索框第一个元素
ip_addressObjectPage_Group_button_addItem_posXpath = '//form/div[4]/div/div/div/div[1]/div/div[1]/div[3]/div/i'  # 添加item按钮Xpath
ip_addressObjectPage_addItem_error_tips_posXpath = "//div[@class='object-item-error']/span"  # IP error_format 错误提示
ip_addressObjectPage_button_inputItem_posXpath = '//div[@class="list-container"]//div[@class="IpExpr expr-item"]//div/input'  # 输入item内容
ip_addressObjectPage_button_editItem_posXpath = "//i[@class='operate-icon iconfont icon-Edit']"  # object item编辑按钮
ip_addressObjectPage_button_editgroup_posXpath = "//i[@class='row-edit iconfont icon-Edit cursor fontsize18']"  # object group组 item编辑按钮
ip_addressObjectPage_button_ip_text_posXpath = "//div[@class='object-item-box']//div[@class='item-box']//div[@class='el-input el-input--small']/input"  # ip object item文本编辑框
ip_addressObjectPage_button_ip_learing_text_posXpath = "//div[@class='object-item-box']//div[@class='item-box']//div[@class='fqdn-input el-input el-input--small']/input"  # ip_learing object item文本编辑框

ip_addressObjectPage_radioButton_Geography_posId = "Geographygeo_location"  # Geography单选按钮id
ip_addressObjectPage_radioButton_Geography_Select_Asia = '//div[4]/div//div[3]/div/div/span[text()="Europa"]'  # countryRegion选择1亚洲
ip_addressObjectPage_radioButton_Geography_Select_replace = '//div[4]/div//div[2]/div/div/span[text()="replace"]'  # countryRegion选择1亚洲
ip_addressObjectPage_radioButton_Geography_Select_Asia_China = '//div[4]/div/div//div[3]/div[2]/div[8]/div/label/span/span'  # countryRegion选择2中国

ip_addressObjectPage_radioButton_IP_learning_posId = "IP Learningip_learning"  # IP Learning单选按钮id
ip_addressObjectPage_IP_learning_inputItem_posXpath = "//div[@class='IpLearningItemList']//div[@class='edit-row']//input[@class='el-input__inner']"  # IP Learning中Item输入
ip_addressObjectPage_button_Save_Item_posXpath = '//div/i[@class="operate-icon iconfont icon-save check"]'  # 保存item按钮
ip_address_Geography_list_first_ele_posXpath = '//div[@role="group"][@aria-expanded="true"]/div[1]/div/label/span'  # Geography所选列表下第一个元素
ip_addressObjectPage_button_IP_learn_from_protocols_posXpath = "//input[@placeholder='Protocols']"  # Learn From Protocols选择框
ip_addressObjectPage_button_IP_learn_from_protocols_up_posXpath = '//i[@class="el-select__caret el-input__icon el-icon-arrow-up is-reverse"]'  # Learn From Protocols_up选择框
ip_addressObjectPage_button_IP_learn_from_protocols_Select_HTTP_posXpath = '//li/span[text()="HTTP"]'  # Learn From Protocols选择HTTP
ip_addressObjectPage_button_IP_learn_from_protocols_Select_SSL_posXpath = '//li/span[text()="SSL"]'  # Learn From Protocols选择SSL
ip_addressObjectPage_button_Input_Aging_Times_posXpath = "//input[@placeholder='Aging Times']"  # Aging Times输入框
ip_addressObjectPage_button_Input_Vote_Clients_Number_posXpath = "//input[@placeholder='Vote Clients Number']"  # Vote Clients Number输入框
ip_addressObjectPage_button_Input_Learned_IP_Limits_posXpath = "//input[@placeholder='Learned IP Limits']"  # Learned IP Limits 输入框

ip_addressObjectPage_textArea_Description_posXpath = "//div[@class='objectAdd_description el-textarea el-input--small']/textarea"  # description文本输入区Xpath
ip_addressObjectPage_button_OK_posXpath = '//button[@id="OK-_IpDetail_Home_App_anonymousComponent"]/span'  # Group保存主页面OK按钮
ip_addressObjectPage_button_SaveYes_posXpath = '//button[@id="OK-_IpDetail_VDraswer_EditDraw_IpDetail_Home_App_anonymousComponent"]/span'  # Group引用创建OK按钮
ip_addressObjectPage_button_warningSaveYes_posXpath = "//div[@class='el-message-box__wrapper']/div/div[3]/button[2]/span"  # 提示保存ok按钮警告框
ip_addressObjectPage_button_warningSaveCancel_posCss = '//div[@class="el-message-box__wrapper"]/div/div[3]/button[1]/span'  # 提示保存取消按钮警告框
ip_addressObjectPage_button_cancel_posCss = "//button[@id='Cancle-_IpDetail_Home_App_anonymousComponent']/span"  # Cancel按钮

# Create IP Address Group Object 和 Edit Create IP Address Group   新增和编辑页
ip_address_Group_sub_Object_addButton_posXpath = "//div[@class='CommonSubObjects']//i[@class='iconfont icon-Create1 cursor']"  # ip_address_Group添加sub Object按钮
ip_address_Group_sub_Object_add_new_Button_posXpath = "//div/div/div[2]/div/div[1]/div/div/div/div[2]/div[1]/div/div[1]/div[2]/div/div/button/i"  # 新建sub_ip_address按钮
ip_address_Group_sub_Object_add_new_Select_one_Button_posXpath = "//ul[@x-placement='bottom-start']/li[1]"  # 新建选择ip_address按钮
ip_address_Group_sub_Object_edit_subObject_Button_posXpath = "//i[@class='row-edit iconfont icon-Edit cursor fontsize18']"  # 编辑group 下的object 按钮
ip_address_Group_sub_Object_add_new_Select_Group_Button_posXpath = "//ul[@x-placement='bottom-start']/li[2]"  # 新建选择ip_address_Group按钮
ip_address_Group_sub_Object_add_new_one_inputName_posXpath = '//div/div/div[1]/div/div/div[1]/div[1]/div/div/div/div[1]/div[2]/form/div[1]/div/div[1]/div[1]/input'  # new ip_address input Name
ip_address_Group_sub_Object_add_new_add_item_Button_posXpath = "(//div[@class='object-item-add'])[2]/div"  # new ip_address add items
ip_address_Group_sub_Object_add_new_addIP_item_inputName_posXpath = '//div[@class="list-container"]//input'  # new IP Item input
# ================= Geography =============== Geography================= Geography =============== Geography================= Geography =============== Geography================= Geography =============== Geography
ip_address_Group_sub_Object_add_new_addphoneNumber_item_inputName_posXpath = '//form/div[4]/div[1]/div/div/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div/input'  # new PhoneNumber inputItemName
ip_address_Group_sub_Object_add_new_addIMEI_item_inputName_posXpath = '//input[@id="onlyMarvel"]'  # new IMEI inputItemName
ip_address_Group_sub_Object_add_new_add_itemIP_Save_Button_posXpath = "//i[@class='operate-icon iconfont icon-save check']"  # 保存item按钮
ip_address_Group_sub_Object_add_new_one_OK1_Button_posXpath = '//div/div/div[2]/div/div/div[1]/div/div/div[1]/div[3]/button[1]/span'  # new ip_address CreateOK1
ip_address_Group_sub_Object_add_new_one_OK1_Warning_Yes_Button_posXpath = '//div[@class="el-message-box__wrapper"]/div/div[3]/button[2]/span'  # 再次确认创建new ip_address
ip_address_Group_sub_Object_add_new_one_OK1_Warning_Cancel_Button_posXpath = '//div[@class="el-message-box__wrapper"]/div/div[3]/button[1]/span'  # 再次确认取消new ip_address
ip_address_Group_sub_Object_add_new_one_Cancel2_Button_posXpath = '//div/div/div[2]/div/div/div[1]/div/div/div[1]/div[3]/button[2]/span'  # new ip_address CreateCancel2



# Object FQDNs===================Object FQDNs====================Object FQDNs=================Object FQDNs=======================Object FQDNs=================Object FQDNs
### Object-FQDNs
# Object FQDNs===================Object FQDNs====================Object FQDNs=================Object FQDNs=======================Object FQDNs=================Object FQDNs
# FQDNs list page 列表页
listPage_object_FQDNs_createButton_posId = "objectCreate-_OperateBtns_ElRow_Objects_fqdn_Home_App_anonymousComponent"  # create按钮id
listPage_object_FQDNs_editButton_posId = "appEdit-_OperateBtns_ElRow_Objects_fqdn_Home_App_anonymousComponent"  # edit按钮id
listPage_object_FQDNs_delButton_posId = "appDel-_OperateBtns_ElRow_Objects_fqdn_Home_App_anonymousComponent"  # del按钮id
listPage_object_FQDNs_del_disabled_Button_posXpath = '//button[@class="el-button topicCol-btn el-button--default el-button--small is-disabled"][@disabled="disabled"]'  # FQDN删除按钮置灰
listPage_object_FQDNs_del_yes_Button_posXpath = '//div/div[@aria-label="Tips"]/div[3]/span/button[1]/span'  # del_yes按钮
listPage_objectSearch_FQDNs_selectLabel_posId = mainPage_ObjectSearch_selectLabel_posId  # 查询框id
# 查询框输入并选择
listPage_objectSearch_FQDNs_select_Id_posXpath = '//li[@id="1-_FilteredSearch_ElRow_Objects_fqdn_Home_App_anonymousComponent"]'  # 查询ID
listPage_objectSearch_FQDNs_select_Name_posXpath = '//li[@id="2-_FilteredSearch_ElRow_Objects_fqdn_Home_App_anonymousComponent"]'  # 查询Name
listPage_objectSearch_FQDNs_select_Details_posXpath = '//li[@id="6-_FilteredSearch_ElRow_Objects_fqdn_Home_App_anonymousComponent"]'  # 查询Details
listPage_objectSearch_FQDNs_select_Description_posXpath = '//li[id="4-_FilteredSearch_ElRow_Objects_fqdn_Home_App_anonymousComponent"]'  # 查询Description
listPage_objectSearch_FQDNs_select_CreateBy_posXpath = '//*[@id="5-_FilteredSearch_ElRow_Objects_fqdn_Home_App_anonymousComponent"]'  # 查询CreateBy

listPage_objectSearch_FQDNs_buttonSearch_posId = mainPage_ObjectSearch_buttonSearch_posId  # 查询按钮id
listPage_objectSearch_FQDNs_buttonClear_posId = mainPage_ObjectSearch_buttonClear_posId  # 清空查询按钮id
listPage_object_FQDNs_create_FQDNs_Button_posId = 'object0-_OperateBtns_ElRow_Objects_fqdn_Home_App_anonymousComponent'  # 创建FQDNs
listPage_object_FQDNs_create_FQDNs_Group_Button_posId = "object1-_OperateBtns_ElRow_Objects_fqdn_Home_App_anonymousComponent"  # 创建FQDNs Group

listPage_profileSearch_FQDNs_dropDown_item_posXpath = ""  # 下拉菜单定位
listPage_profileSearch_FQDNs_input_itemContent_posXpath = ""  # 输入item的值，replaceName替换实际查询值
listPage_profileSearch_FQDNs_dropDown_typeItem_posXpath = ""  # 查询中type的下拉item定位,replaceName替换实际查询值
listPage_profilTable_FQDNs_tableTbody_posXpath = ""  # 列表tabel body  xpath
listPage_profilTable_FQDNs_tableHeader_posXpath = ""  # 列表table 表头xpath

# FQDNs list page 列表页提取元素--列表页
listPage_object_FQDNs_new_ID_extract_posXpath = '//table/tbody/tr[1]/td[1]/div/div/div[4]/span'  # 提取ID
listPage_object_FQDNs_new_Name_extract_posXpath = '//table/tbody/tr[1]/td[3]/div/div/div/span'  # 提取Name
listPage_object_FQDNs_new_Description_extract_posXpath = '//table/tbody/tr[1]/td[6]/div/div/p'  # 提取Description
listPage_object_FQDNs_new_Details_extract_posXpath = '//table/tbody/tr[1]/td[4]/div/div/div/div/div/div/span'  # 提取Detail
listPage_object_FQDNs_del_after_ele_posXpath = '//div[@id="ly-table1-listcontent"]/div/div[3]/div/span'  # 删除后提示"No Data"
# FQDNs list page 列表页操作
listPage_object_FQDNs_select_First_object_posXpath = '//table/tbody/tr/td[1]/div/div/div[1]/div/label/span[1]/span'  # 选择列表中第一个对象

# Create FQDNs Object 和 Edit FQDNs Object   新增和编辑页
FQDNsObjectPage_input_Name_posXpath = "//form/div[1]/div/div[1]/div[1]/input"  # name输入框Xpath

FQDNsObjectPage_input_searchFor_posId = mainPage_ObjectSearch_buttonSearch_Item_posId  # search for item搜索输入框id
FQDNsObjectPage_button_addItem_posId = mainPage_ObjectSearch_buttonAddItem_posId  # 添加item按钮id
FQDNsObjectPage_button_inputItem_posXpath = "//div[@class='object-item-box']//div[@class='item-box']//div[@class='rel-input el-input el-input--small']/input"  # 输入item内容
FQDNsObjectPage_button_Save_Item_posXpath = "//div[@class='object-item-box']//div[@class='item-box']//div[@class='IconBtn']/i"  # 保存item按钮

FQDNsObjectPage_textArea_Description_posXpath = "//div[@class='objectAdd_description el-textarea el-input--small']/textarea" # description文本输入区Xpath
FQDNsObjectPage_button_SaveYes_posXpath = '//button[@id="OK-_FqdnDetail_Home_App_anonymousComponent"]/span'  # OK按钮
FQDNsObjectPage_button_warningSaveYes_posXpath = "//div[@class='el-message-box__wrapper']/div/div[3]/button[2]/span"  # 提示保存ok按钮警告框
FQDNsObjectPage_button_warningSaveCancel_posCss = '//div[@class="el-message-box__wrapper"]/div/div[3]/button[1]/span'  # 提示保存取消按钮警告框
FQDNsObjectPage_button_cancel_posCss = "//button[@id='Cancle-_FqdnDetail_Home_App_anonymousComponent']/span"  # Cancel按钮

# Create FQDNs Group Object 和 Edit CreateFQDNs Group   新增和编辑页
FQDNs_Group_sub_Object_addButton_posXpath = "//div[@class='CommonSubObjects']//i[@class='iconfont icon-Create1 cursor']"  # FQDNs_Group添加sub Object按钮
FQDNs_Group_sub_Object_add_new_Button_posXpath = "//div/div/div[2]/div/div[1]/div/div/div/div[2]/div[1]/div/div[1]/div[2]/div/div/button/i"  # 新建sub_FQDNs按钮
FQDNs_Group_sub_Object_add_new_Select_one_Button_posXpath = "//ul[@x-placement='bottom-start']/li[1]"  # 新建选择FQDNs按钮
FQDNs_Group_sub_Object_add_new_Select_Group_Button_posXpath = "//ul[@x-placement='bottom-start']/li[2]"  # 新建选择FQDNs_Group按钮
FQDNs_Group_sub_Object_add_new_one_inputName_posXpath = '//div/div/div[1]/div/div/div[1]/div[1]/div/div/div/div[1]/div[2]/form/div[1]/div/div[1]/div[1]/input'  # new FQDNs input Name
FQDNs_Group_sub_Object_add_new_add_item_Button_posXpath = "(//div[@class='object-item-add'])[2]/div"  # new FQDNs add items Button
FQDNs_Group_sub_Object_add_new_addIP_item_inputName_posXpath = '//div[@class="list-container"]//input'  # new FQDNs Item input
FQDNs_Group_sub_Object_add_new_add_itemIP_Save_Button_posXpath = "//i[@class='operate-icon iconfont icon-save save-color']"  # new FQDNs 保存item按钮
FQDNs_Group_sub_Object_add_new_one_OK1_Button_posXpath = '//div/div/div[2]/div/div/div[1]/div/div/div[1]/div[3]/button[1]/span'  # new FQDNs CreateOK1
FQDNs_Group_sub_Object_add_new_one_OK1_Warning_Yes_Button_posXpath = '//div[@class="el-message-box__wrapper"]/div/div[3]/button[2]/span'  # 再次确认创建new FQDNs
FQDNs_Group_sub_Object_add_new_one_OK1_Warning_Cancel_Button_posXpath = '//div[@class="el-message-box__wrapper"]/div/div[3]/button[1]/span'  # 再次确认取消new FQDNs
FQDNs_Group_sub_Object_add_new_one_Cancel2_Button_posXpath = '//div/div/div[2]/div/div/div[1]/div/div/div[1]/div[3]/button[2]/span'  # new FQDNs CreateCancel2
# Object FQDNs===================Object FQDNs====================Object FQDNs=================Object FQDNs=======================Object FQDNs=================Object FQDNs
### Object-FQDNs
# Object FQDNs===================Object FQDNs====================Object FQDNs=================Object FQDNs=======================Object FQDNs=================Object FQDNs


# Object Subscriber_IDs===================Object Subscriber_IDs====================Object Subscriber_IDs=================Object Subscriber_IDs=======================Object Subscriber_IDs=================Object Subscriber_IDs
### Object-Subscriber_IDs
# Object Subscriber_IDs===================Object Subscriber_IDs====================Object Subscriber_IDs=================Object Subscriber_IDs=======================Object Subscriber_IDs=================Object Subscriber_IDs
# Subscriber_IDs list page 列表页
listPage_object_Subscriber_IDs_createButton_posId = "objectCreate-_OperateBtns_ElRow_Objects_subscriberid_Home_App_anonymousComponent"  # create按钮id
listPage_object_Subscriber_IDs_editButton_posId = "appEdit-_OperateBtns_ElRow_Objects_subscriberid_Home_App_anonymousComponent"  # edit按钮id
listPage_object_Subscriber_IDs_delButton_posId = "appDel-_OperateBtns_ElRow_Objects_subscriberid_Home_App_anonymousComponent"  # del按钮id
listPage_object_Subscriber_IDs_delButton_disable_posXpath = '//button[@id="appDel-_OperateBtns_ElRow_Objects_subscriberid_Home_App_anonymousComponent"][@disabled="disabled"]'  # del按钮置灰
listPage_object_Subscriber_IDs_reference_count_posXpath = '//table/tbody/tr[2]/td[7]/div/div/div/div'  # 引用计数
listPage_object_main_reference_count_posXpath = listPage_object_Subscriber_IDs_reference_count_posXpath
listPage_object_Subscriber_IDs_first_reference_list_posXpath = '//div/div/div[2]/div[2]/div[1]/div/div[3]/div[1]'  # 侧滑引用列表第一列
listPage_object_Subscriber_IDs_second_reference_list_posXpath = '//div/div/div[2]/div[2]/div[1]/div/div[3]/div[2]'  # 侧滑引用列表第二列
listPage_profilTable_FQDNs_reference_first_row_posXpath = listPage_object_Subscriber_IDs_first_reference_list_posXpath
listPage_profilTable_FQDNs_reference_Second_row_posXpath = listPage_object_Subscriber_IDs_second_reference_list_posXpath
listPage_object_Subscriber_IDs_del_yes_Button_posXpath = '//div[@aria-label="Tips"]/div[3]/span/button[1]/span'  # del_yes按钮
listPage_objectSearch_Subscriber_IDs_selectLabel_posId = mainPage_ObjectSearch_selectLabel_posId  # 查询框id
# 查询框输入并选择
listPage_objectSearch_Subscriber_IDs_select_Id_posXpath = '//li[@id="1-_FilteredSearch_ElRow_Objects_subscriberid_Home_App_anonymousComponent"]'  # 查询ID
listPage_objectSearch_Subscriber_IDs_select_Name_posXpath = '//li[@id="2-_FilteredSearch_ElRow_Objects_subscriberid_Home_App_anonymousComponent"]'  # 查询Name
listPage_objectSearch_Subscriber_IDs_select_Details_posXpath = '//li[@id="6-_FilteredSearch_ElRow_Objects_subscriberid_Home_App_anonymousComponent"]'  # 查询Details
listPage_objectSearch_Subscriber_IDs_select_Description_posXpath = '//li[id="4-_FilteredSearch_ElRow_Objects_subscriberid_Home_App_anonymousComponent"]'  # 查询Description
listPage_objectSearch_Subscriber_IDs_select_CreateBy_posXpath = '//*[@id="5-_FilteredSearch_ElRow_Objects_subscriberid_Home_App_anonymousComponent"]'  # 查询CreateBy

listPage_objectSearch_Subscriber_IDs_buttonSearch_posId = mainPage_ObjectSearch_buttonSearch_posId  # 查询按钮id
listPage_objectSearch_Subscriber_IDs_buttonClear_posId = mainPage_ObjectSearch_buttonClear_posId  # 清空查询按钮id
listPage_object_Subscriber_IDs_create_Subscriber_IDs_Button_posId = 'object0-_OperateBtns_ElRow_Objects_subscriberid_Home_App_anonymousComponent'  # 创建Subscriber_IDs
listPage_object_Subscriber_IDs_create_Subscriber_IDs_Group_Button_posId = "object1-_OperateBtns_ElRow_Objects_subscriberid_Home_App_anonymousComponent"  # 创建Subscriber_IDs Group

listPage_profileSearch_Subscriber_IDs_dropDown_item_posXpath = ""  # 下拉菜单定位
listPage_profileSearch_Subscriber_IDs_input_itemContent_posXpath = ""  # 输入item的值，replaceName替换实际查询值
listPage_profileSearch_Subscriber_IDs_dropDown_typeItem_posXpath = ""  # 查询中type的下拉item定位,replaceName替换实际查询值
listPage_profilTable_Subscriber_IDs_tableTbody_posXpath = ""  # 列表tabel body  xpath
listPage_profilTable_Subscriber_IDs_tableHeader_posXpath = ""  # 列表table 表头xpath

# Subscriber_IDs list page 列表页提取元素--列表页
listPage_object_Subscriber_IDs_new_ID_extract_posXpath = '//table/tbody/tr[1]/td[1]/div/div/div[4]/span'  # 提取ID
listPage_object_Subscriber_IDs_new_Name_extract_posXpath = '//table/tbody/tr[1]/td[3]/div/div/div/span'  # 提取Name
listPage_object_Subscriber_IDs_new_Description_extract_posXpath = '//table/tbody/tr[1]/td[6]/div/div/p'  # 提取Description
listPage_object_Subscriber_IDs_new_Details_extract_posXpath = '//table/tbody/tr[1]/td[4]/div/div/div/div/div/div/div/span/div/span'  # 提取Detail
listPage_object_Subscriber_IDs_del_after_ele_posXpath = '//div[@id="ly-table1-listcontent"]/div/div[3]/div/span'  # 删除后提示"No Data"
# Subscriber_IDs list page 列表页操作
listPage_object_Subscriber_IDs_select_First_object_posXpath = '//table/tbody/tr/td[1]/div/div/div[1]/div/label/span[1]/span'  # 选择列表中第一个对象

# Create Subscriber_IDs Object 和 Edit Subscriber_IDs Object   新增和编辑页
Subscriber_IDsObjectPage_input_Name_posXpath = "//form/div[1]/div/div[1]/div[1]/input"  # name输入框Xpath

Subscriber_IDsObjectPage_input_searchFor_posId = mainPage_ObjectSearch_buttonSearch_Item_posId  # search for item搜索输入框id
Subscriber_IDsObjectPage_button_addItem_posId = mainPage_ObjectSearch_buttonAddItem_posId  # 添加item按钮id
Subscriber_IDsObjectPage_button_inputItem_posXpath = "//input[@id='onlyMarvel']"  # 输入item内容
Subscriber_IDsObjectPage_button_Save_Item_posXpath = "//i[@class='operate-icon iconfont icon-save save-color']"  # 保存item按钮

Subscriber_IDsObjectPage_textArea_Description_posXpath = '//div[@class="objectAdd_description el-textarea el-input--small"]/textarea'  # Subscriber IDs_description文本输入区Xpath
Subscriber_IDs_GroupObjectPage_textArea_Description_posXpath = "//div[@class='objectAdd_description el-textarea el-input--small']/textarea"  # Subscriber IDs Group_description文本输入区Xpath
Subscriber_IDsObjectPage_button_SaveYes_posXpath = '//button[@id="OK-_SubscriberidDetail_Home_App_anonymousComponent"]/span'  # OK按钮
Subscriber_IDsObjectPage_button_warningSaveYes_posXpath = "//div[@class='el-message-box__wrapper']/div/div[3]/button[2]/span"  # 提示保存ok按钮警告框
Subscriber_IDsObjectPage_button_warningSaveCancel_posCss = '//div[@class="el-message-box__wrapper"]/div/div[3]/button[1]/span'  # 提示保存取消按钮警告框
Subscriber_IDsObjectPage_button_cancel_posCss = "//button[@id='Cancle-_SubscriberidDetail_Home_App_anonymousComponent']/span"  # Cancel按钮

# Create Subscriber_IDs Group Object 和 Edit CreateSubscriber_IDs Group   新增和编辑页
Subscriber_IDs_Group_sub_Object_addButton_posXpath = "//div[@class='CommonSubObjects']//i[@class='iconfont icon-Create1 cursor']"  # Subscriber_IDs_Group添加sub Object按钮
Subscriber_IDs_Group_sub_Object_add_new_Button_posXpath = "//div/div/div[2]/div/div[1]/div/div/div/div[2]/div[1]/div/div[1]/div[2]/div/div/button/i"  # 新建sub_Subscriber_IDs按钮
Subscriber_IDs_Group_sub_Object_add_new_Select_one_Button_posXpath = "//ul[@x-placement='bottom-start']/li[1]"  # 新建选择Subscriber_IDs按钮
Subscriber_IDs_Group_sub_Object_add_new_Select_Group_Button_posXpath = "//ul[@x-placement='bottom-start']/li[2]"  # 新建选择Subscriber_IDs_Group按钮
Subscriber_IDs_Group_sub_Object_export_files_Button_posXpath = '//div[@class="el-tooltip object-export"]/button'  # 导出文件按钮
Subscriber_IDs_Group_sub_Object_import_files_Button_posXpath = '//div[@class="ImportBtn import-btn"]/button/span'  # object导入文件按钮
Subscriber_IDs_Group_sub_Object_import_files_Path_posXpath = '//form/div/div/div/div[1]/input[@type="file"]'  # 导入文件路径
Subscriber_IDs_Group_sub_Object_import_files_OK_posXpath = '//div/div/div[2]/div[2]/button[1]/span[contains(text(),"OK")]'  # 导入文件OK
Subscriber_IDs_Group_sub_Object_export_files_yes_Button_posXpath = '//span/button[@class="el-button delComponents-ok el-button--primary el-button--small"]/span[contains(text(),"Yes")]'  # 导出文件Yes按钮
list_PageObject_Export_files_yes_button_posXpath = Subscriber_IDs_Group_sub_Object_export_files_yes_Button_posXpath  # 导出文件Yes按钮
main_sub_Object_edit_sub_object_Button_posXpath = "//i[@class='row-edit iconfont icon-Edit cursor fontsize18']"
Subscriber_IDs_Group_sub_Object_edit_sub_object_Button_posXpath = main_sub_Object_edit_sub_object_Button_posXpath  # Subscriber_IDs_Group编辑subObject按钮
Subscriber_IDs_Group_sub_Object_add_new_one_inputName_posXpath = '//div/div/div[1]/div/div/div[1]/div[1]/div/div/div/div[1]/div[2]/form/div[1]/div/div[1]/div[1]/input'  # new Subscriber_IDs input Name
Subscriber_IDs_Group_sub_Object_add_new_add_item_Button_posXpath = "(//div[@class='object-item-add'])[2]/div"  # new Subscriber_IDs add items Button
Subscriber_IDs_Group_sub_Object_add_new_addIP_item_inputName_posXpath = '//div[@class="list-container"]//input'  # new Subscriber_IDs Item input
Subscriber_IDs_Group_sub_Object_add_new_add_itemIP_Save_Button_posXpath = "//i[@class='operate-icon iconfont icon-save save-color']"  # new Subscriber_IDs 保存item按钮
Subscriber_IDs_Group_sub_Object_add_new_one_OK1_Button_posXpath = '//div/div/div[1]/div/div/div[1]/div[3]/button[1]/span[contains(text(),"OK")]'  # new Subscriber_IDs CreateOK1
Subscriber_IDs_Group_sub_Object_add_new_one_OK1_Warning_Yes_Button_posXpath = '//div[@class="el-message-box__wrapper"]/div/div[3]/button[2]/span'  # 再次确认创建new Subscriber_IDs
Subscriber_IDs_Group_sub_Object_add_new_one_OK1_Warning_Cancel_Button_posXpath = '//div[@class="el-message-box__wrapper"]/div/div[3]/button[1]/span'  # 再次确认取消new Subscriber_IDs
Subscriber_IDs_Group_sub_Object_add_new_one_Cancel2_Button_posXpath = '//div/div/div[2]/div/div/div[1]/div/div/div[1]/div[3]/button[2]/span'  # new Subscriber_IDs CreateCancel2
# Object Subscriber_IDs===================Object Subscriber_IDs====================Object Subscriber_IDs=================Object Subscriber_IDs=======================Object Subscriber_IDs=================Object Subscriber_IDs
### Object-Subscriber_IDs
# Object Subscriber_IDs===================Object Subscriber_IDs====================Object Subscriber_IDs=================Object Subscriber_IDs=======================Object Subscriber_IDs=================Object Subscriber_IDs


# Object HTTP_Signatures===================Object HTTP_Signatures====================Object HTTP_Signatures=================Object HTTP_Signatures=======================Object HTTP_Signatures=================Object HTTP_Signatures
### Object-HTTP_Signatures
# Object HTTP_Signatures===================Object HTTP_Signatures====================Object HTTP_Signatures=================Object HTTP_Signatures=======================Object HTTP_Signatures=================Object HTTP_Signatures
# HTTP_Signatures list page 列表页
listPage_object_HTTP_Signatures_createButton_posId = "objectCreate-_OperateBtns_ElRow_Objects_http_signature_Home_App_anonymousComponent"  # create按钮id
listPage_object_HTTP_Signatures_editButton_posId = "appEdit-_OperateBtns_ElRow_Objects_http_signature_Home_App_anonymousComponent"  # edit按钮id
listPage_object_HTTP_Signatures_delButton_posId = "appDel-_OperateBtns_ElRow_Objects_http_signature_Home_App_anonymousComponent"  # del按钮id
listPage_object_HTTP_Signatures_delButton_display_posXpath = '//button[@id="appDel-_OperateBtns_ElRow_Objects_http_signature_Home_App_anonymousComponent"][@disabled="disabled"]'  # del按钮置灰状态
list_quote_content_object_HTTP_Signatures_posXpath = '//table/tbody/tr[2]/td[7]/div/div/div/div'  # quote计数
list_Column_settings_HTTP_Signatures_Description_posXpath = '//div[@class="ly-eventfixed"]/ul/li[6]/label/span[2]'  # 列设置选择Description
list_HTTP_Signatures_Export_files_button_posXpath = '//div/button[contains(@class,"Export")]/i'  # 导出文件按钮
list_HTTP_Signatures_Export_files_yes_button_posXpath = '//div/div[3]/span/button[1]/span[contains(text(),"Yes")]'  # 导出文件Yes按钮
list_quote_first_row_object_HTTP_Signatures_posXpath = '//div/div/div[2]/div[2]/div[1]/div/div[3]/div'  # quote侧滑第一行
list_quote_second_row_object_HTTP_Signatures_posXpath = '//div/div[2]/div[2]/div[1]/div/div[3]/div[2]'  # quote侧滑第二行
Create_item_second_row_object_HTTP_Signatures_posXpath = "(//div[@class='infinite-list-wrapper']//div[@class='view-row'])[2]//div[@class='keywords-txt']/span"  # item第二行
listPage_object_HTTP_Signatures_del_yes_Button_posXpath = '//div[@class="el-dialog__wrapper"]/div/div[3]/span/button[1]/span'  # del_yes按钮
listPage_objectSearch_HTTP_Signatures_selectLabel_posId = mainPage_ObjectSearch_selectLabel_posId  # 查询框id
# 查询框输入并选择
listPage_objectSearch_HTTP_Signatures_select_Id_posXpath = '//li[@id="1-_FilteredSearch_ElRow_Objects_http_signature_Home_App_anonymousComponent"]'  # 查询ID
listPage_objectSearch_HTTP_Signatures_select_Name_posXpath = '//li[@id="2-_FilteredSearch_ElRow_Objects_http_signature_Home_App_anonymousComponent"]'  # 查询Name
listPage_objectSearch_HTTP_Signatures_select_Details_posXpath = '//li[@id="6-_FilteredSearch_ElRow_Objects_http_signature_Home_App_anonymousComponent"]'  # 查询Details
listPage_objectSearch_HTTP_Signatures_select_Description_posXpath = '//li[id="4-_FilteredSearch_ElRow_Objects_http_signature_Home_App_anonymousComponent"]'  # 查询Description
listPage_objectSearch_HTTP_Signatures_select_CreateBy_posXpath = '//*[@id="5-_FilteredSearch_ElRow_Objects_http_signature_Home_App_anonymousComponent"]'  # 查询CreateBy

listPage_objectSearch_HTTP_Signatures_buttonSearch_posId = mainPage_ObjectSearch_buttonSearch_posId  # 查询按钮id
listPage_objectSearch_HTTP_Signatures_buttonClear_posId = mainPage_ObjectSearch_buttonClear_posId  # 清空查询按钮id
listPage_object_HTTP_Signatures_create_HTTP_Signatures_Button_posId = 'object0-_OperateBtns_ElRow_Objects_http_signature_Home_App_anonymousComponent'  # 创建HTTP_Signatures
listPage_object_HTTP_Signatures_create_HTTP_Signatures_Group_Button_posId = "object1-_OperateBtns_ElRow_Objects_http_signature_Home_App_anonymousComponent"  # 创建HTTP_Signatures Group

listPage_profileSearch_HTTP_Signatures_dropDown_item_posXpath = ""  # 下拉菜单定位
listPage_profileSearch_HTTP_Signatures_input_itemContent_posXpath = ""  # 输入item的值，replaceName替换实际查询值
listPage_profileSearch_HTTP_Signatures_dropDown_typeItem_posXpath = ""  # 查询中type的下拉item定位,replaceName替换实际查询值
listPage_profilTable_HTTP_Signatures_tableTbody_posXpath = ""  # 列表tabel body  xpath
listPage_profilTable_HTTP_Signatures_tableHeader_posXpath = ""  # 列表table 表头xpath

# HTTP_Signatures list page 列表页提取元素--列表页
listPage_object_HTTP_Signatures_new_ID_extract_posXpath = '//table/tbody/tr[1]/td[1]/div/div/div[4]/span'  # 提取ID
listPage_object_HTTP_Signatures_new_Name_extract_posXpath = '//table/tbody/tr[1]/td[3]/div/div/div/span'  # 提取Name
listPage_object_HTTP_Signatures_new_Description_extract_posXpath = '//table/tbody/tr[1]/td[6]/div/div/p'  # 提取Description
listPage_object_HTTP_Signatures_new_Details_extract_posXpath = '//table/tbody/tr[1]/td[4]/div/div/div/div/div/div/span'  # 提取Detail
listPage_object_HTTP_Signatures_del_after_ele_posXpath = '//div[@id="ly-table1-listcontent"]/div/div[3]/div/span'  # 删除后提示"No Data"
# HTTP_Signatures list page 列表页操作
listPage_object_HTTP_Signatures_select_First_object_posXpath = '//table/tbody/tr/td[1]/div/div/div[1]/div/label/span[1]/span'  # 选择列表中第一个对象

# Create HTTP_Signatures Object 和 Edit HTTP_Signatures Object   新增和编辑页
HTTP_SignaturesObjectPage_input_Name_posXpath = "//div[@class='biFangName']/div[1]/input"  # name输入框Xpath

HTTP_SignaturesObjectPage_input_searchFor_posId = mainPage_ObjectSearch_buttonSearch_Item_posId  # search for item搜索输入框id
HTTP_SignaturesObjectPage_button_addItem_posId = mainPage_ObjectSearch_buttonAddItem_posId  # 添加item按钮id
HTTP_SignaturesObjectPage_button_inputItem_posXpath = "//div[@class='row-value-content']//div[@class='content-input el-input el-input--small']/input"  # 输入item内容
HTTP_SignaturesObjectPage_sub_inputItem_posXpath = '//div/div/div[2]/div[2]/div[2]/div/div/div[1]/div[1]/div/input'
HTTP_SignaturesObjectPage_button_input_Item_posXpath = "//div[1]/div[1]/div/div/div[2]/div[2]/div[2]/div/div/div['replace']/div[1]/div/input"  # 输入& 所需要元素
HTTP_SignaturesObjectPage_button_select_HEX_posXpath = "//div[@class='expr-type-list']/span[text()='HEX']"  # 选择HEX
HTTP_SignaturesObjectPage_button_Save_Item_posXpath = "//i[@class='operate-icon iconfont icon-save check']"  # 保存item按钮
HTTP_SignaturesObjectPage_button_sub_add_Item_posXpath = "//div[@class='ItemRow infinite-list-item']//i[@class='iconfont icon-Create1 cursor']"  # &添加按钮
HTTP_SignaturesObjectPage_textArea_Description_posXpath = "//div[@class='objectAdd_description el-textarea el-input--small']/textarea"  # HTTP_Signatures_description文本输入区Xpath
HTTP_Signatures_GroupObjectPage_textArea_Description_posXpath = "//div[@class='objectAdd_description el-textarea el-input--small']/textarea"  # HTTP_Signatures Group_description文本输入区Xpath
HTTP_SignaturesObjectPage_button_SaveYes_posXpath = '//button[@id="OK-_HttpSigDetail_Home_App_anonymousComponent"]/span'  # OK按钮
HTTP_SignaturesObjectPage_button_warningSaveYes_posXpath = "//div[@class='el-message-box__wrapper']/div/div[3]/button[2]/span"  # 提示保存ok按钮警告框
HTTP_SignaturesObjectPage_button_warningSaveCancel_posCss = '//div[@class="el-message-box__wrapper"]/div/div[3]/button[1]/span'  # 提示保存取消按钮警告框
HTTP_SignaturesObjectPage_button_cancel_posCss = "//button[@id='Cancle-_HttpSigDetail_Home_App_anonymousComponent']/span"  # Cancel按钮

# Create HTTP_Signatures Group Object 和 Edit CreateHTTP_Signatures Group   新增和编辑页
HTTP_Signatures_Group_sub_Object_addButton_posXpath = "//div[@class='CommonSubObjects']//i[@class='iconfont icon-Create1 cursor']"  # HTTP_Signatures_Group添加sub Object按钮
main_button_audit_button_posXpath = '//div/div/form/div[8]/div/div[1]/span'
HTTP_SignaturesObjectPage_button_audit_button_posXpath = main_button_audit_button_posXpath  # Audit Logs 按钮
main_button_import_files_button_posXpath = '//button/span[contains(text(),"Import From File")]'  # 导入文件按钮
HTTP_SignaturesObjectPage_button_import_files_button_posXpath = main_button_import_files_button_posXpath  # 导入文件按钮
HTTP_SignaturesObjectPage_button_import_files_path_button_posXpath = '//form/div/div/div/div[1]/input[@type="file"]'  # 导入文件路径
HTTP_SignaturesObjectPage_button_import_error_files_tips_posXpath = '//div/div[2]/div[2]/ul/li/div[3]/span'  # 导入错误文件提示
HTTP_SignaturesObjectPage_first_item_content_button_posXpath = '//form/div[3]/div/div/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div/div/div[1]/div/span'  # 第一个item的内容
HTTP_Signatures_Group_sub_Object_add_new_Button_posXpath = "//div/div/div[2]/div/div[1]/div/div/div/div[2]/div[1]/div/div[1]/div[2]/div/div/button/i"  # 新建sub_HTTP_Signatures按钮
HTTP_Signatures_Group_sub_Object_add_new_Select_one_Button_posXpath = "//ul[@x-placement='bottom-start']/li[1]"  # 新建选择HTTP_Signatures按钮
HTTP_Signatures_Group_sub_Object_add_new_Select_Group_Button_posXpath = "//ul[@x-placement='bottom-start']/li[2]"  # 新建选择HTTP_Signatures_Group按钮
HTTP_Signatures_Group_sub_Object_add_new_one_inputName_posXpath = '//div/div/div[1]/div/div/div[1]/div[1]/div/div/div/div[1]/div[2]/form/div[1]/div/div[1]/div[1]/input'  # new HTTP_Signatures input Name
HTTP_Signatures_Group_sub_Object_add_new_add_item_Button_posXpath = "(//div[@class='object-item-add'])[2]/div"  # new HTTP_Signatures add items Button
HTTP_Signatures_Group_sub_Object_edit_posXpath = "//i[@class='row-edit iconfont icon-Edit cursor fontsize18']"  # 修改HTTP_Signatures下的sub object
HTTP_Signatures_Select_Key_Button_posXpath = "//div[@class='type-icon-box']//input[@placeholder='Select']"  # new HTTP_Signatures select Key
HTTP_Signatures_Select_Key_Select_Set_Cookie_Button_posXpath = '//li/span[text()="Set-Cookie"]'  # Key选择Set-Cookie
HTTP_Signatures_Select_Key_Select_Content_Type_Button_posXpath = '//li/span[text()="Content-Type"]'  # Key选择Content-Type
HTTP_Signatures_Select_Key_Select_User_Agent_Button_posXpath = '//li/span[text()="User-Agent"]'  # Key选择User-Agent
HTTP_Signatures_Select_Key_Select_Cookie_Button_posXpath = '//li/span[text()="Cookie"]'  # Key选择Cookie
HTTP_Signatures_Group_sub_Object_add_new_add_item_inputName_posXpath = '//div/div[2]/div[2]/div[2]/div/div/div[1]/div[1]/div/input'  # new HTTP_Signatures Item input
HTTP_Signatures_Group_sub_Object_add_new_add_item_Save_Button_posXpath = '//form/div[3]/div/div/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div/div/div[1]/div[2]/i'  # new HTTP_Signatures 保存item按钮
HTTP_Signatures_Group_sub_Object_add_new_one_OK1_Button_posXpath = '//div/div/div[2]/div/div/div[1]/div/div/div[1]/div[3]/button[1]/span'  # new HTTP_Signatures CreateOK1
HTTP_Signatures_Group_sub_Object_add_new_one_OK1_Warning_Yes_Button_posXpath = '//div[@class="el-message-box__wrapper"]/div/div[3]/button[2]/span'  # 再次确认创建new HTTP_Signatures
HTTP_Signatures_Group_sub_Object_add_new_one_OK1_Warning_Cancel_Button_posXpath = '//div[@class="el-message-box__wrapper"]/div/div[3]/button[1]/span'  # 再次确认取消new HTTP_Signatures
HTTP_Signatures_Group_sub_Object_add_new_one_Cancel2_Button_posXpath = '//div/div/div[2]/div/div/div[1]/div/div/div[1]/div[3]/button[2]/span'  # new HTTP_Signatures CreateCancel2
# Object HTTP_Signatures===================Object HTTP_Signatures====================Object HTTP_Signatures=================Object HTTP_Signatures=======================Object HTTP_Signatures=================Object HTTP_Signatures
### Object-HTTP_Signatures
# Object HTTP_Signatures===================Object HTTP_Signatures====================Object HTTP_Signatures=================Object HTTP_Signatures=======================Object HTTP_Signatures=================Object HTTP_Signatures


# Object Keywords===================Object Keywords====================Object Keywords=================Object Keywords=======================Object Keywords=================Object Keywords
### Object-Keywords
# Object Keywords===================Object Keywords====================Object Keywords=================Object Keywords=======================Object Keywords=================Object Keywords
# Keywords list page 列表页
listPage_object_Keywords_createButton_posId = "objectCreate-_OperateBtns_ElRow_Objects_keywords_Home_App_anonymousComponent"  # create按钮id
listPage_object_Keywords_editButton_posId = "appEdit-_OperateBtns_ElRow_Objects_keywords_Home_App_anonymousComponent"  # edit按钮id
listPage_object_Keywords_editButton_posXpath = '//button[@id="appEdit-_OperateBtns_ElRow_Objects_keywords_Home_App_anonymousComponent"][@disabled="disabled"]'  # edit按钮xpath
listPage_object_Keywords_delButton_posId = "appDel-_OperateBtns_ElRow_Objects_keywords_Home_App_anonymousComponent"  # del按钮id
listPage_object_Keywords_del_yes_Button_posXpath = '//div[@class="el-dialog__wrapper"]/div/div[3]/span/button[1]/span'  # del_yes按钮
listPage_objectSearch_Keywords_selectLabel_posId = mainPage_ObjectSearch_selectLabel_posId  # 查询框id
# 查询框输入并选择
listPage_objectSearch_Keywords_select_Id_posXpath = '//li[@id="1-_FilteredSearch_ElRow_Objects_keywords_Home_App_anonymousComponent"]'  # 查询ID
listPage_objectSearch_Keywords_select_Name_posXpath = '//li[@id="2-_FilteredSearch_ElRow_Objects_keywords_Home_App_anonymousComponent"]'  # 查询Name
listPage_objectSearch_Keywords_select_Details_posXpath = '//li[@id="6-_FilteredSearch_ElRow_Objects_keywords_Home_App_anonymousComponent"]'  # 查询Details
listPage_objectSearch_Keywords_select_Description_posXpath = '//li[id="4-_FilteredSearch_ElRow_Objects_keywords_Home_App_anonymousComponent"]'  # 查询Description
listPage_objectSearch_Keywords_select_CreateBy_posXpath = '//*[@id="5-_FilteredSearch_ElRow_Objects_keywords_Home_App_anonymousComponent"]'  # 查询CreateBy

listPage_objectSearch_Keywords_buttonSearch_posId = mainPage_ObjectSearch_buttonSearch_posId  # 查询按钮id
listPage_objectSearch_Keywords_buttonClear_posId = mainPage_ObjectSearch_buttonClear_posId  # 清空查询按钮id
listPage_object_Keywords_create_Keywords_Button_posId = 'object0-_OperateBtns_ElRow_Objects_keywords_Home_App_anonymousComponent'  # 创建Keywords
Create_page_import_from_file_button_xpath = "//button[@class='el-button btn-style el-button--default el-button--small']"  # 创建Keywords import button
listPage_object_Keywords_create_Keywords_Group_Button_posId = "object1-_OperateBtns_ElRow_Objects_keywords_Home_App_anonymousComponent"  # 创建Keywords Group

listPage_profileSearch_Keywords_dropDown_item_posXpath = ""  # 下拉菜单定位
listPage_profileSearch_Keywords_input_itemContent_posXpath = ""  # 输入item的值，replaceName替换实际查询值
listPage_profileSearch_Keywords_dropDown_typeItem_posXpath = ""  # 查询中type的下拉item定位,replaceName替换实际查询值
listPage_profilTable_Keywords_tableTbody_posXpath = ""  # 列表tabel body  xpath
listPage_profilTable_Keywords_tableHeader_posXpath = ""  # 列表table 表头xpath

# Keywords list page 列表页提取元素--列表页
listPage_object_Keywords_new_ID_extract_posXpath = '//table/tbody/tr[1]/td[1]/div/div/div[4]/span'  # 提取ID
listPage_object_Keywords_new_Name_extract_posXpath = '//table/tbody/tr[1]/td[3]/div/div/div/span'  # 提取Name
listPage_object_Keywords_new_Description_extract_posXpath = '//table/tbody/tr[1]/td[6]/div/div/p'  # 提取Description
listPage_object_Keywords_new_Details_extract_posXpath = '//table/tbody/tr[1]/td[4]/div/div/div/div/div/div/span'  # 提取Detail
listPage_object_Keywords_del_after_ele_posXpath = '//div[@id="ly-table1-listcontent"]/div/div[3]/div/span'  # 删除后提示"No Data"
# Keywords list page 列表页操作
listPage_object_Keywords_select_First_object_posXpath = '//table/tbody/tr/td[1]/div/div/div[1]/div/label/span[1]/span'  # 选择列表中第一个对象

# Create Keywords Object 和 Edit Keywords Object   新增和编辑页

KeywordsObjectPage_input_Name_posXpath = "//form/div[1]/div/div[1]/div[1]/input"  # name输入框Xpath

KeywordsObjectPage_input_searchFor_posId = mainPage_ObjectSearch_buttonSearch_Item_posId  # search for item搜索输入框id
KeywordsObjectPage_button_addItem_posId = mainPage_ObjectSearch_buttonAddItem_posId  # 添加item按钮id
KeywordsObjectPage_first_Item_content_posXpath = "(//div[@class='list-container']//div[@class='v-fill-available row-info']/span)[1]"  # 第一个item的内容
main_first_Item_count_posXpath = '//div[1]/div[2]/div[@class="total"]'
KeywordsObjectPage_first_Item_count_posXpath = main_first_Item_count_posXpath  ## 断言新增item的个数
KeywordsObjectPage_Audit_Logs_Button_posXpath = '//div/div/div[3]/div/div/form/div[8]/div/div[1]/span'  # Audit Logs编辑框
KeywordsObjectPage_Audit_Logs_First_create_posXpath = '//table/tbody/tr/td[3]/div'  # Audit Logs第一条编辑记录
KeywordsObjectPage_Audit_Logs_First_edit_posXpath = '//div/div/div/div/div[2]/div[2]/div/div[2]/div[3]/table/tbody/tr[2]'  # Audit Logs第二条编辑记录
KeywordsObjectPage_button_item_select_HEX_posXpath = "//div[@class='v-fill-available']//span[text()='HEX']"  # HEX按钮
KeywordsObjectPage_button_inputItem_posXpath = "//div[@class='ItemRow infinite-list-item']//div[@class='content-input el-input el-input--small']/input"  # 输入item内容

KeywordsObjectPage_button_Save_Item_posXpath = "//i[@class='operate-icon iconfont icon-save check']"  # 保存item按钮
KeywordsObjectPage_import_files_ok1_posXpath = '//div/div/div[2]/div[2]/button[1]/span'  # 导入文件确定ok
KeywordsObjectPage_textArea_Description_posXpath = "//div[@class='objectAdd_description el-textarea el-input--small']/textarea"  # Keywords_description文本输入区Xpath
Keywords_GroupObjectPage_textArea_Description_posXpath = "//div[@class='objectAdd_description el-textarea el-input--small']/textarea"  # Keywords Group_description文本输入区Xpath
KeywordsObjectPage_button_SaveYes_posXpath = '//button[@id="OK-_keywordsDetail_Home_App_anonymousComponent"]/span'  # OK按钮
KeywordsObjectPage_button_warningSaveYes_posXpath = "//div[@class='el-message-box__wrapper']/div/div[3]/button[2]/span"  # 提示保存ok按钮警告框
KeywordsObjectPage_button_warningSaveCancel_posCss = '//div[@class="el-message-box__wrapper"]/div/div[3]/button[1]/span'  # 提示保存取消按钮警告框
KeywordsObjectPage_button_cancel_posCss = "//button[@id='Cancle-_keywordsDetail_Home_App_anonymousComponent']/span"  # Cancel按钮

# Create Keywords Group Object 和 Edit CreateKeywords Group   新增和编辑页
main_ObjectPage_tips_Name_input_Xpath = '//form/div[1]/div/div[@class="el-form-item__error"]'
KeywordsObjectPage_tips_Name_input_Xpath = main_ObjectPage_tips_Name_input_Xpath  # 删除失败，Name提示框
Keywords_list_reference_content_first_raw = '//div[1]/div/div/div[2]/div[2]/div[1]/div/div[3]/div'  # 列表页引用第一行
Keywords_list_reference_content_second_raw = '//div/div/div[2]/div[2]/div[1]/div/div[2]/div/div[2]'  # 列表引用第二行
Keywords_ObjectPage_content_inputItem1_posXpath = '//div/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div/div/div[1]/span'  # 第一行输入item的内容
Keywords_Group_sub_Object_addButton_posXpath = "//div[@class='CommonSubObjects']//i[@class='iconfont icon-Create1 cursor']"  # Keywords_Group添加sub Object按钮
KeywordsObjectPage_Keywords_button_input_more_Item_posXpath = "(//div[@class='TextExpr expr-item']//input[@class='el-input__inner'])['replace']"  # 输入keywords_item内容
Keywords_Group_sub_Object_add_new_Button_posXpath = "//div/div/div[2]/div/div[1]/div/div/div/div[2]/div[1]/div/div[1]/div[2]/div/div/button/i"  # 新建sub_Keywords按钮
Keywords_Group_sub_Object_edit_posXpath = "//div[@class='list-container']//i[@class='row-edit iconfont icon-Edit cursor fontsize18']"  # 修改Keyword下的sub object
Keywords_Group_sub_Object_add_new_Select_one_Button_posXpath = "//ul[@x-placement='bottom-start']/li[1]"  # 新建选择Keywords按钮
Keywords_Group_sub_Object_add_new_Select_Group_Button_posXpath = "//ul[@x-placement='bottom-start']/li[2]"  # 新建选择Keywords_Group按钮
Keywords_Group_sub_Object_add_new_one_inputName_posXpath = '//div/div/div[1]/div/div/div[1]/div[1]/div/div/div/div[1]/div[2]/form/div[1]/div/div[1]/div[1]/input'  # new Keywords input Name
Keywords_Group_sub_Object_add_new_add_item_Button_posXpath = "//div[@class='CommonItems']//div[@class='object-item-add']//i[@class='operate-icon iconfont icon-Create1']"  # new Keywords add items Button
Keywords_Group_sub_Object_add_new_addIP_item_inputName_posXpath = "//div[@class='ItemRow infinite-list-item']//div[@class='content-input el-input el-input--small']/input"  # new Keywords Item input
Keywords_Group_sub_Object_add_new_add_itemIP_Save_Button_posXpath = "//i[@class='operate-icon iconfont icon-save check']"  # new Keywords 保存item按钮
Keywords_Group_sub_Object_add_new_one_OK1_Button_posXpath = '//div/div/div[2]/div/div/div[1]/div/div/div[1]/div[3]/button[1]/span'  # new Keywords CreateOK1
Keywords_Group_sub_Object_add_new_one_OK1_Warning_Yes_Button_posXpath = '//div[@class="el-message-box__wrapper"]/div/div[3]/button[2]/span'  # 再次确认创建new Keywords
Keywords_Group_sub_Object_add_new_one_OK1_Warning_Cancel_Button_posXpath = '//div[@class="el-message-box__wrapper"]/div/div[3]/button[1]/span'  # 再次确认取消new Keywords
Keywords_Group_sub_Object_add_new_one_Cancel2_Button_posXpath = '//div/div/div[2]/div/div/div[1]/div/div/div[1]/div[3]/button[2]/span'  # new Keywords CreateCancel2
# Object Keywords===================Object Keywords====================Object Keywords=================Object Keywords=======================Object Keywords=================Object Keywords
### Object-Keywords
# Object Keywords===================Object Keywords====================Object Keywords=================Object Keywords=======================Object Keywords=================Object Keywords


# Object Categories elements area top===================Object Categories elements area top===================Object Categories elements area top===================Object Categories elements area top===================Object Categories elements area top===================
# Object Categories elements area top===================Object Categories elements area top===================Object Categories elements area top===================Object Categories elements area top===================Object Categories elements area top===================
global_loading_elem_whenNotDisplaied_xpath = '//*[@class="el-loading-mask" and @style="display: none;"]'  # Loading不展示时的Xpath

admin_listPage_object_categories_createButton_posId = 'objectCreate-_OperateBtns_ElRow_Objects_fqdn_category_Home_App_anonymousComponent'  # create按钮id
admin_listPage_object_categories_createButton_category_posId = 'object0-_OperateBtns_ElRow_Objects_fqdn_category_Home_App_anonymousComponent'  # create按钮下category选项id
admin_listPage_object_categories_editButton_posId = "appEdit-_OperateBtns_ElRow_Objects_fqdn_category_Home_App_anonymousComponent"  # edit按钮id
admin_listPage_object_categories_delButton_posId = "appDel-_OperateBtns_ElRow_Objects_fqdn_category_Home_App_anonymousComponent"  # del按钮id
# admin_listPage_second_row_fourth_column_posXpath = '//table/tbody/tr[1]/td[4]//p'  # 第二行,第四列（description）
# admin_listPage_second_row_fifth_column_posXpath = '//table/tbody/tr[1]/td[5]/div/div/div/div'  # 第二行、第五列（Reference Count）
admin_listPage_first_row_checkBox_posXpath = url_listPage_first_row_checkBox_posXpath  # 列表页第一行对象多选框Xpath
listPage_object_cate_tableDetails_firstRowValues_div_posXpaths = listPage_object_urls_tableDetails_firstRowValues_div_posXpaths  # list页点击Details后展示的数据Xpaths_div
# listPage->Tips dialog  列表页 tips对话框
admin_listPage_object_cate_button_yes_posCss = listPage_object_urls_button_yes_posCss  # 删除提示的Tips的yes按钮Xpath
admin_listPage_object_cate_button_no_posCss = listPage_object_urls_button_no_posCss  # 删除提示的Tips的No按钮Xpath
# object Categories列表页
# cate_listPage_object_exportButton_posXpath = '//button[contains(@id,"objectExport-_importAndExport_ElRow_Objects_fqdn_category_Home_App_anonymousComponent")]'  # 导出文件按钮 Xpath
# cate_listPage_object_exportButton_posXpath = '//button[contains(@class,"importAndExport")]'  # 导出文件按钮 Xpath
cate_listPage_object_importButton_posXpath = listPage_object_urls_importButton_posXpath  # 导入文件按钮 Xpath
cate_listPage_object_exportButton_posXpath = listPage_object_urls_exportButton_posXpath  # 导出文件按钮 Xpath
cate_listPage_object_exportPopYes_posXpath = listPage_object_urls_exportPopYes_posXpath  # 导出数据选择确认弹窗 yes Xpath
cate_listPage_first_row_checkBox_posXpath = url_listPage_first_row_checkBox_posXpath  # 列表页第一行对象多选框Xpath
cate_listPage_object_exportPopNo_posXpath = listPage_object_urls_exportPopNo_posXpath  # 导出数据选择确认弹窗 no Xpath
cate_listPage_object_exportPopSelectAll_posXpath = listPage_object_urls_exportPopSelectAll_posXpath  # 导出数据选择确认弹窗全选CheckBox Xpathcat
cate_listPage_object_exportPopCheckbox_posXpaths = listPage_object_urls_exportPopCheckbox_posXpaths  # 导出数据选择确认弹窗CheckBox(多个)
cate_listPage_object_clearCounterPopYes_posXpath = listPage_object_urls_clearCounterPopYes_posXpath  # Clear Counter 选择确认弹窗中的Yes确认按钮
cate_object_columnSetting_descriptionOption_posXpath = listPage_object_urls_columnSetting_descriptionOption_posXpath  # 列设置中的description选项元素Xpath
cate_listPage_usage_policies_elems_posXpaths = url_listPage_usage_policies_elems_posXpaths  # 点击Reference count后展开的侧滑页面，其中的引用条数
cate_listPage_common_reference_count_elem_posXpath = '(//div[contains(@id,"-_Objects_fqdn_category_Home_App_anonymousComponent") and text()={}])[1]'  # reference_count通用模板
cate_listPage_object_tableCheckbox_firstSingleObject_posXpath = listPage_object_urls_tableDetails_firstSingleObject_posXpath  # 列表页中第一个列表页中第一个Single Object 的CheckBox
# cate_object_urls_tableDetails_singleObject_posXpaths = listPage_object_urls_tableDetails_singleObject_posXpaths  # 列表页中所有对象（不包含对象组）的DetailsXpath
cate_listPage_object_tableCheckbox_singleObject_posXpaths = listPage_object_urls_tableCheckbox_singleObject_posXpaths# 列表页中Object 的CheckBoxs(不包含Group和锁定对象)
cate_listPage_object_tableCheckbox_notLocalVsys_objectOrGroup_posXpaths = listPage_object_urls_tableCheckbox_notLocalVsys_objectOrGroup_posXpaths  # 列表页中不是本Vsys的对象或对象组的CheckBox
cate_listPage_object_tableCheckbox_firstSingleObject_posXpaths = listPage_object_urls_tableDetails_firstSingleObject_posXpath# 列表页中第一个Object 的CheckBox(不包含Group和锁定对象)
cate_listPage_object_tableCheckbox_firstNotLocalVsys_objectOrGroup_posXpath = listPage_object_urls_tableCheckbox_firstNotLocalVsys_objectOrGroup_posXpath  # 列表页中第一个不是本Vsys的对象或对象组的CheckBox
cate_listPage_object_tableCheckbox_firstObjectGroup_posXpath = listPage_object_urls_tableDetails_firstObjectGroup_posXpath## 列表页中第一个Object Group 的CheckBox(不包含single Object和锁定对象)
cate_listPage_object_tableCheckbox_objectGroup_posXpaths = listPage_object_urls_tableCheckbox_objectGroup_posXpaths ## 列表页Object Group 的CheckBoxs(不包含single Object和锁定对象)
cate_ObjectDetailPage_clearCounter_posXpath = url_ObjectDetailPage_clearCounter_posXpath  # Clear Counter 按钮

# 列表页搜索选项
cate_listPage_object_searchId_posId = '1-_FilteredSearch_ElRow_Objects_fqdn_category_Home_App_anonymousComponent'  # ID 搜索
cate_listPage_object_ssearchName_posId = '2-_FilteredSearch_ElRow_Objects_fqdn_category_Home_App_anonymousComponent'  # name 搜索
cate_listPage_object_searchDetails_posId = '6-_FilteredSearch_ElRow_Objects_fqdn_category_Home_App_anonymousComponent'  # details搜索
cate_listPage_object_searchDescription_posId = '4-_FilteredSearch_ElRow_Objects_fqdn_category_Home_App_anonymousComponent'  # Description 搜索
cate_listPage_object_searchCreatedBy_posId = '5-_FilteredSearch_ElRow_Objects_fqdn_category_Home_App_anonymousComponent'  # created by 搜索
cate_listPage_object_tableDetails_detailsRow_firstDetailValue_posXpaths = listPage_object_urls_tableDetails_detailsRow_firstDetailValue_posXpaths  # 列表页某行第一个details值 Xpath
# cate_list_objectPage_second_row_third_column_posXpath = '(//table[@class="el-table__body"]/tbody//td)[3]//span'  # 第二行、第三列(Name)
# cate_list_objectPage_second_row_fifth_column_posXpath = '//table/tbody/tr[1]/td[5]//p'  # 第二行、第五列
# cate_list_objectPage_second_row_sixth_column_posXpath = '(//table/tbody/tr[1]/td[6]/div/div//div)[last()]'  # 第二行、第六列
cate_listPage_noDataText_posXpath = url_listPage_noDataText_posXpath  # 列表页无数据时的no data文本 Xpath
# Categories详情页
cate_ObjectDetailPage_nameInput_posXpath = '//div[@data-label="Name"]//input'  # 对象详情页Name输入框Xpath
cate_ObjectDetailPage_nameLenthNumber_posXpath = url_ObjectDetailPage_nameLenthNumber_posXpath  # Name输入框中字符长度数值Xpath
cate_ObjectDetailPage_item_search_posId = url_ObjectDetailPage_object_ip_search_posId  # 对象详情页对象搜索框 ID
cate_ObjectDetailPage_item_addButton_posId = url_ObjectDetailPage_addButton_posId  # item下"+"按钮
cate_ObjectDetailPage_itemValueInput_posId = 'onlyMarvel'  # item 下value输入框Xpath
cate_ObjectDetailPage_item_subAddButton_poId = url_ObjectDetailPage_item_subAddButton_poXpath  # 单个Item中新增多条数据的"+"按钮
# cate_ObjectDetailPage_itemSaveButton_poXpath = '//div[@class="el-form-item margin-bottom6 el-form-item--small"]//i[@class="operate-icon iconfont icon-save save-color"]'  # item 下value保存按钮Xpath
cate_ObjectDetailPage_itemSaveButton_poXpath = url_ObjectDetailPage_itemSaveButton_posXpath  # item 下value保存按钮Xpath
cate_ObjectDetailPage_descriptionInput_posXpath = url_ObjectDetailPage_description_posXpath  # Create Category 页面下Description input Xpath
cate_ObjectDetailPage_auditLogs_posXpath = url_ObjectDetailPage_auditLogs_posXpath  # Audit Logs Xpath
cate_ObjectDetailPage_auditLogsDrawer_firstRowLog_checkBox_posXpath = url_ObjectDetailPage_auditLogsDrawer_firstRowLog_checkBox_posXpath  # Audit Logs 侧滑页第一条日志CheckBox Xpath
cate_ObjectDetailPage_auditLogsDrawer_compareButton_posXpath = url_ObjectDetailPage_auditLogsDrawer_compareButton_posXpath  # Audit Logs 侧滑页Compare 按钮Xpath
cate_ObjectDetailPage_auditLogsDrawer_compareDrawer_operationText_posXpath = url_ObjectDetailPage_auditLogsDrawer_compareDrawer_operationText_posXpath  # Audit Logs 侧滑页点击Compare后的 operation text Xpath
cate_ObjectDetailPage_itemsTotal_posXpath = url_ObjectDetailPage_itemsTotal_posXpath  # Items Total Xpath
cate_ObjectDetailPage_importFromFile_posXpath = url_ObjectDetailPage_importFromFile_posXpath  # Import From File 按钮Xpath
cate_ObjectDetailPage_pleaseUpload_posXpath = url_ObjectDetailPage_pleaseUpload_posXpath  # Please Upload input标签Xpath
cate_ObjectDetailPage_importUrlOk_posXpath = url_ObjectDetailPage_importUrlOk_posXpath  # Import URL 下的OK按钮Xpath

cate_ObjectDetailPage_mainOkButton_poId = 'OK-_fqdnCategorieDetail_Home_App_anonymousComponent'  # OK按钮ID
cate_ObjectDetailPage_okButton_yes_posXpath = url_ObjectDetailPage_okButton_yes_posXpath  # 确认弹窗的“Yes”按钮
# Object Categories elements area bottom===================Object Categories elements area bottom===================Object Categories elements area bottom===================Object Categories elements area bottom===================Object Categories elements area bottom===================
# Object Categories elements area bottom===================Object Categories elements area bottom===================Object Categories elements area bottom===================Object Categories elements area bottom===================Object Categories elements area bottom===================

# Object Accounts elements area top===================Object Accounts elements area top===================Object Accounts elements area top===================Object Accounts elements area top===================Object Accounts elements area top===================
# Object Accounts elements area top===================Object Accounts elements area top===================Object Accounts elements area top===================Object Accounts elements area top===================Object Accounts elements area top===================
# 列表页
acc_listPage_createButton_posId = 'objectCreate-_OperateBtns_ElRow_Objects_account_Home_App_anonymousComponent'  # 列表页create 按钮ID
acc_listPage_createButton_account_posId = 'object0-_OperateBtns_ElRow_Objects_account_Home_App_anonymousComponent'  # 列表页create下account ID
acc_listPage_createButton_accountGroup_posId = 'object1-_OperateBtns_ElRow_Objects_account_Home_App_anonymousComponent'  # 列表页create下account group ID
acc_listPage_editButton_posId = 'appEdit-_OperateBtns_ElRow_Objects_account_Home_App_anonymousComponent'  # 列表页 Edit 按钮ID
acc_listPage_deleteButton_posId = 'appDel-_OperateBtns_ElRow_Objects_account_Home_App_anonymousComponent'  # 列表页 Delete 按钮ID
acc_object_columnSetting_descriptionOption_posXpath = listPage_object_urls_columnSetting_descriptionOption_posXpath  # 列设置中的description选项元素Xpath
acc_listPage_first_row_checkBox_posXpath = '(//td[@rowspan="1"and @colspan="1"]//span[@class="el-checkbox__inner"])[1]'  # 列表页第一行对象多选框Xpath
acc_listPage_noDataText_posXpath = url_listPage_noDataText_posXpath  # 列表页无数据时的no data文本 Xpath
acc_listPage_object_importButton_posXpath = listPage_object_urls_importButton_posXpath  # 导入文件按钮 Xpath
acc_listPage_object_exportButton_posXpath = listPage_object_urls_exportButton_posXpath  # 导出文件按钮 Xpath
acc_listPage_object_exportPopYes_posXpath = listPage_object_urls_exportPopYes_posXpath  # 导出数据选择确认弹窗 yes Xpath
acc_listPage_object_clearCounterPopYes_posXpath = listPage_object_urls_clearCounterPopYes_posXpath  # Clear Counter 选择确认弹窗中的Yes确认按钮
acc_listPage_object_exportPopNo_posXpath = listPage_object_urls_exportPopNo_posXpath  # 导出数据选择确认弹窗 no Xpath
acc_listPage_object_exportPopSelectAll_posXpath = listPage_object_urls_exportPopSelectAll_posXpath  # 导出数据选择确认弹窗全选CheckBox Xpathcat
acc_listPage_object_exportPopCheckbox_posXpaths = listPage_object_urls_exportPopCheckbox_posXpaths  # 导出数据选择确认弹窗CheckBox(多个)
acc_listPage_object_tableDetails_firstRowValues_div_posXpaths = listPage_object_urls_tableDetails_firstRowValues_div_posXpaths  # list页点击Details后展示的数据Xpaths_div
acc_listPage_object_tableDetails_selected_detailsRow_posXpaths = listPage_object_urls_tableDetails_selected_detailsRow_posXpaths  # list页被选中的对象details 值Xpath
acc_listPage_object_tableCheckbox_posXpaths = listPage_object_urls_tableCheckbox_posXpaths  # 列表页CheckBox（50）
acc_listPage_object_tableCheckbox_singleObject_posXpaths = listPage_object_urls_tableCheckbox_singleObject_posXpaths   # 列表页中Object 的CheckBoxs(不包含Group和锁定对象)
acc_listPage_object_tableCheckbox_firstSingleObject_posXpath = listPage_object_urls_tableDetails_firstSingleObject_posXpath  # 列表页中第一个Object 的CheckBox(不包含Group和锁定对象)
acc_listPage_object_tableCheckbox_objectGroup_posXpaths = listPage_object_urls_tableCheckbox_objectGroup_posXpaths  # 列表页对象组的CheckBox（多个）
acc_listPage_object_tableCheckbox_firstObjectGroup_posXpath = listPage_object_urls_tableDetails_firstObjectGroup_posXpath  # 列表页中第一个Object Group 的CheckBox
acc_listPage_object_tableCheckbox_notLocalVsys_objectOrGroup_posXpaths = listPage_object_urls_tableCheckbox_notLocalVsys_objectOrGroup_posXpaths  # 列表页中不是本Vsys的对象或对象组的CheckBox
acc_listPage_object_tableCheckbox_firstNotLocalVsys_objectOrGroup_posXpath = listPage_object_urls_tableCheckbox_firstNotLocalVsys_objectOrGroup_posXpath  # 列表页中第一个不是本Vsys的对象或对象组的CheckBox
acc_listPage_object_tableDetails_singleObject_posXpaths = listPage_object_urls_tableDetails_singleObject_posXpaths  # 列表页中所有对象（不包含对象组）的DetailsXpath
acc_listPage_object_tableCheckbox_selectedCheckBox_posXpaths = listPage_object_urls_tableDetails_selected_checkBox_posXpaths  # list页被选中的对象 CheckBox Xpath
## listPage->Tips dialog  列表页 tips对话框
acc_listPage_object_delete_yesButton_posCss = 'body>.el-dialog__wrapper .delComponents-ok span'  # 删除提示的Tips的yes按钮Xpath
acc_listPage_object_urls_delete_noButton_posCss = 'body>.el-dialog__wrapper .delComponents-close span'  # 删除提示的Tips的No按钮Xpath

# 列表页搜索选项
acc_listPage_object_fuzzySearch_posXpath = listPage_object_urls_fuzzySearch_posXpath  # 模糊搜索选项x
acc_listPage_object_searchId_posId = '1-_FilteredSearch_ElRow_Objects_account_Home_App_anonymousComponent'  # ID 搜索
acc_listPage_object_searchName_posId = '2-_FilteredSearch_ElRow_Objects_account_Home_App_anonymousComponent'  # name 搜索
acc_listPage_object_searchDetails_posId = '6-_FilteredSearch_ElRow_Objects_account_Home_App_anonymousComponent'  # details搜索
acc_listPage_object_searchDescription_posId = '4-_FilteredSearch_ElRow_Objects_account_Home_App_anonymousComponent'  # Description 搜索
acc_listPage_object_searchCreatedBy_posId = '5-_FilteredSearch_ElRow_Objects_account_Home_App_anonymousComponent'  # created by 搜索
acc_listPage_object_tableDetails_detailsRow_firstDetailValue_posXpaths = listPage_object_urls_tableDetails_detailsRow_firstDetailValue_posXpaths  # 列表页某行第一个details值 Xpath

# 对象详情页
acc_ObjectDetailPage_nameInput_posXpath = url_ObjectDetailPage_nameInput_posXpath  # Name输入框Xpath
acc_ObjectDetailPage_nameLenthNumber_posXpath = url_ObjectDetailPage_nameLenthNumber_posXpath  # Name输入框中字符长度数值Xpath
acc_ObjectDetailPage_item_addButton_poId = url_ObjectDetailPage_addButton_posId  # item下"+"按钮
acc_ObjectDetailPage_item_subAddButton_poId = url_ObjectDetailPage_item_subAddButton_poXpath  # 单个Item中新增多条数据的"+"按钮
# acc_ObjectDetailPage_item_subAddButton_poId = '//*[@class="item-box"]//*[contains(@class,"addobject")]'  # 单个Item中新增多条数据的"+"按钮
acc_ObjectDetailPage_itemValueInput_poXpath = '//div[@class="expr-box"]//input'  # item 下value输入框Xpath
acc_ObjectDetailPage_itemSaveButton_poXpath = url_ObjectDetailPage_itemSaveButton_posXpath  # item 下value保存按钮Xpath
acc_ObjectDetailPage_item_search_posId = url_ObjectDetailPage_object_ip_search_posId  # item 下搜索框id
acc_ObjectDetailPage_description_posXpath = url_ObjectDetailPage_description_posXpath  # 对象详情页面下Description input Xpath
acc_ObjectDetailPage_auditLogs_posXpath = url_ObjectDetailPage_auditLogs_posXpath  # Audit Logs Xpath
acc_ObjectDetailPage_auditLogsDrawer_firstRowLog_checkBox_posXpath = url_ObjectDetailPage_auditLogsDrawer_firstRowLog_checkBox_posXpath  # Audit Logs 侧滑页第一条日志CheckBox Xpath
acc_ObjectDetailPage_auditLogsDrawer_compareButton_posXpath = url_ObjectDetailPage_auditLogsDrawer_compareButton_posXpath  # Audit Logs 侧滑页Compare 按钮Xpath
acc_ObjectDetailPage_auditLogsDrawer_compareDrawer_operationText_posXpath = url_ObjectDetailPage_auditLogsDrawer_compareDrawer_operationText_posXpath  # Audit Logs 侧滑页点击Compare后的 operation text Xpath
acc_ObjectDetailPage_itemsTotal_posXpath = url_ObjectDetailPage_itemsTotal_posXpath  # Items Total Xpath
acc_ObjectDetailPage_importFromFile_posXpath = url_ObjectDetailPage_importFromFile_posXpath  # Import From File 按钮Xpath
acc_ObjectDetailPage_importFromFile_button_posXpath = url_ObjectDetailPage_importFromFile_button_posXpath  # Import From File 按钮Xpath
acc_ObjectDetailPage_pleaseUpload_posXpath = url_ObjectDetailPage_pleaseUpload_posXpath  # Please Upload input标签Xpath
acc_ObjectDetailPage_importUrlOk_posXpath = url_ObjectDetailPage_importUrlOk_posXpath  # Import 页面 下的OK按钮Xpath
acc_ObjectDetailPage_clearCounter_posXpath = url_ObjectDetailPage_clearCounter_posXpath  # Clear Counter 按钮
acc_ObjectDetailPage_objectStatistics_elaborate_posXpath = '//div[@class="object-Statistics"]//span[text()="Elaborate"]'#object_statistics下的Elaborate选项
acc_ObjectDetailPage_objectStatistics_brief_posXpath = '//div[@class="object-Statistics"]//span[text()="Brief"]'#object_statistics下的 Brief 选项
acc_ObjectDetailPage_objectStatistics_none_posXpath = '//div[@class="object-Statistics"]//span[text()="None"]'#object_statistics下的 None 选项
acc_ObjectDetailPage_dupAlert_posXpath = '//div[@title="Duplicate data exists"]'  # item重复提示
acc_ObjectDetailPage_dupAlert_duplicateListTotal_posXpath = '//div[@class="DuplicateList list-box"]//p[contains(@class,"total")]'  # duplicateList中的“Total：xx”
acc_ObjectDetailPage_importedFile_posXpath = url_ObjectDetailPage_importedFile_posXpath  # 导入文件元素位置（Import From File 按钮旁）
acc_ObjectDetailPage_importedFile_delete_posXpath = url_ObjectDetailPage_importedFile_delete_posXpath  # 文件删除按钮
acc_ObjectDetailPage_importedFile_download_posXpath = url_ObjectDetailPage_importedFile_download_posXpath  # 文件下载按钮

# 对象组详情页
acc_ObjectGroupDetailPage_subObjects_addButton_normalAdd_posXpath = '//div[@data-desc="subObject"]//i[@class="operate-icon iconfont icon-Create1"]'  # Subordinate Objects 下有数据新增时"+"按钮Xpath
acc_ObjectGroupDetailPage_subObjects_addButton_newAdd_posXpath = '//div[@data-desc="subObject"]//div[@class="AddButton"]'  # Subordinate Objects 下无数据新增时"+"按钮Xpath
acc_ObjectDetailPage_firstAccObject = url_ObjectDetailPage_firstUrlObject  ## 侧滑Objects列表中第一个acc object Xpath
acc_ObjectGroupDetailPage_subObjects_search_posId = url_ObjectDetailPage_object_ip_search_posId  # Subordinate Objects 下搜索框id
acc_ObjectGroupDetailPage_subObjects_toggleDraw_addButton_posXpath = '//div[@class="ToggleDraw"]//div[contains(@class,"search-box")]//button'  # Accounts侧滑窗口的"+"按钮
acc_ObjectGroupDetailPage_subObjects_toggleDraw_closeButton_posXpath = url_ObjectGroupDetailPage_subObjects_toggleDraw_closeButton_posXpath  # Accounts侧滑窗口的Close按钮
acc_ObjectGroupDetailPage_subObjects_toggleDraw_addButton_account_posXpath = '(//ul[@class="el-dropdown-menu el-popper el-dropdown-menu--small"]/li[not(contains(text(),"Group"))])[last()]'  # Accounts侧滑窗口的"+"按钮下的Account
acc_ObjectGroupDetailPage_subObjects_subCreateAccountDrawer_nameInput_posXpath = '//div[@class="drawer-box"]//div[@data-label="Name"]//input'  # 侧滑子Create Account页面Name input Xpath
acc_ObjectGroupDetailPage_subObjects_subCreateAccountDrawer_itemsAddButton_posXpath = '//div[@class="drawer-box"]//div[@class="CommonItems"]//div[@class="object-item-add"]/div[@class="IconBtn"]'  # 侧滑子Create Account页面中Items下的"+"按钮 Xpath
acc_ObjectGroupDetailPage_subObjects_subCreateAccountDrawer_itemsValueInput_posXpath = '//div[@class="drawer-box"]//div[@class="CommonItems"]//div[@class="expr-box"]//input'  # 侧滑子Create Account页面中Items下的item value输入框 Xpath
acc_ObjectGroupDetailPage_subObjects_subCreateAccountDrawer_itemsValueSaveButton_posXpath = '//div[@class="drawer-box"]//div[@class="CommonItems"]//i[contains(@class,"icon-save")]'  # 侧滑子Create Account页面中Items下的保存按钮 Xpath
acc_ObjectGroupDetailPage_subObjects_subCreateAccountDrawer_descriptionTextarea_posXpath = '//div[@class="drawer-box"]//label[text()="Description"]/..//textarea'  # 侧滑子Create Account页面中的Description textarea Xpath
acc_ObjectGroupDetailPage_subObjects_subCreateAccountDrawer_okButton_posXpath = '//div[@class="drawer-box"]//div[@class="prox-fixed-footer policy-foot-color"]/button[contains(@id,"OK-_")]'  # 侧滑子Create Account页面中OK按钮
acc_ObjectGroupDetailPage_subObjects_subCreateAccountDrawer_okButton_yes_posXpath = url_ObjectDetailPage_okButton_yes_posXpath  # 侧滑子Create Account页面确认弹窗的“Yes”按钮
acc_ObjectGroupDetailPage_subObjects_subCreateAccountDrawer_okButton_cancel_posXpath = url_ObjectDetailPage_okButton_cancel_posXpath  # 侧滑子Create Account页面确认弹窗的“Cancel”按钮
accGroup_ObjectDetailPage_excludeObjectsSwitch_posXpath = urlGroup_ObjectDetailPage_excludeObjectsSwitch_posXpath  # Exclude Objects Switch Xpath
accGroup_ObjectDetailPage_excludeObjectsSwitch_newAdd_posXpath = urlGroup_ObjectDetailPage_excludeObjectsSwitch_newAdd_posXpath  # Exclude Objects无数据时新增按钮Xpath
accGroup_ObjectDetailPage_excludeObjectsSwitch_normalAdd_posXpath = urlGroup_ObjectDetailPage_excludeObjectsSwitch_normalAdd_posXpath  # Exclude Objects有数据时新增按钮Xpath
accGroup_ObjectDetailPage_excludeObjects_itemsArea_posXpath = urlGroup_ObjectDetailPage_excludeObjects_itemsArea_posXpath  # Exclude Objects下的item区域div Xpath
acc_ObjectDetailPage_firstObject = url_ObjectDetailPage_firstUrlObject  # 侧滑acc Object中第一个url Xpath
acc_ObjectDetailPage_secondObject = url_ObjectDetailPage_secondUrlObject  # 侧滑acc Object中第二个url Xpath

# 详情页通用元素
acc_ObjectDetailPage_mainOkButton_poId = 'OK-_accountsDetail_Home_App_anonymousComponent'  # OK按钮ID
acc_ObjectDetailPage_okButton_yes_posXpath = url_ObjectDetailPage_okButton_yes_posXpath  # 确认弹窗的“Yes”按钮

# Object Accounts elements area bottom===================Object Accounts elements area bottom===================Object Accounts elements area bottom===================Object Accounts elements area bottom===================Object Accounts elements area bottom===================
# Object Accounts elements area bottom===================Object Accounts elements area bottom===================Object Accounts elements area bottom===================Object Accounts elements area bottom===================Object Accounts elements area bottom===================

# Object Intervals elements area top===================Object Intervals elements area top===================Object Intervals elements area top===================Object Intervals elements area top===================Object Intervals elements area top===================
# Object Intervals elements area top===================Object Intervals elements area top===================Object Intervals elements area top===================Object Intervals elements area top===================Object Intervals elements area top===================
# 列表页
int_listPage_createButton_posId = 'objectCreate-_OperateBtns_ElRow_Objects_interval_Home_App_anonymousComponent'  # 列表页create 按钮ID
int_listPage_createButton_account_posId = "object0-_OperateBtns_ElRow_Objects_interval_Home_App_anonymousComponent"  # 列表页create下account ID
int_listPage_createButton_accountGroup_posId = "object1-_OperateBtns_ElRow_Objects_interval_Home_App_anonymousComponent"  # 列表页create下account group ID
int_listPage_editButton_posId = 'appEdit-_OperateBtns_ElRow_Objects_interval_Home_App_anonymousComponent'  # 列表页 Edit 按钮ID
int_listPage_deleteButton_posId = 'appDel-_OperateBtns_ElRow_Objects_interval_Home_App_anonymousComponent'  # 列表页 Delete 按钮ID
int_listPage_first_row_checkBox_posXpath = acc_listPage_first_row_checkBox_posXpath  # 列表页第一行对象多选框Xpath
int_listPage_noDataText_posXpath = '//div[@class="ly-table1"]//span[@class="el-table__empty-text"]'  # 列表页无数据时的no data文本 Xpath
int_ObjectDetailPage_auditLogs_posXpath = '//div[@class="audit_log"]/span'
int_listPage_object_searchName_posId = '2-_FilteredSearch_ElRow_Objects_interval_Home_App_anonymousComponent'
int_listPage_object_searchId_posId = '1-_FilteredSearch_ElRow_Objects_interval_Home_App_anonymousComponent'
int_listPage_object_searchDescription_posId = '4-_FilteredSearch_ElRow_Objects_interval_Home_App_anonymousComponent'
int_listpage_linkButton_posId = 'btnCopy-_OperateBtns_ElRow_Objects_interval_Home_App_anonymousComponent'

## listPage->Tips dialog  列表页 tips对话框
int_listPage_object_delete_yesButton_posCss = acc_listPage_object_delete_yesButton_posCss  # 删除提示的Tips的yes按钮Xpath
int_listPage_object_urls_delete_noButton_posCss = acc_listPage_object_urls_delete_noButton_posCss  # 删除提示的Tips的No按钮Xpath

# 对象详情页a
int_ObjectDetailPage_nameInput_posXpath = url_ObjectDetailPage_nameInput_posXpath  # Name输入框Xpath
int_ObjectDetailPage_nameLenthNumber_posXpath = url_ObjectDetailPage_nameLenthNumber_posXpath  # Name输入框中字符长度数值Xpath
int_ObjectDetailPage_item_addButton_poId = url_ObjectDetailPage_addButton_posId  # item下"+"按钮
int_ObjectDetailPage_itemValueInput_lowBoundary_poXpath = '(//div[@class="v-panel-content"]//div[@class="CommonItems"]//div[@class="list-container"]//input)[1]'  # item 下low_boundary value输入框Xpath
int_ObjectDetailPage_itemValueInput_upBoundary_poXpath = '(//div[@class="v-panel-content"]//div[@class="CommonItems"]//div[@class="list-container"]//input)[last()]'  # item 下 up_boundary value输入框Xpath
int_ObjectDetailPage_itemSaveButton_poXpath = url_ObjectDetailPage_itemSaveButton_posXpath  # item 下value保存按钮Xpath
int_ObjectDetailPage_item_search_posId = url_ObjectDetailPage_object_ip_search_posId  # item 下搜索框id
int_ObjectDetailPage_description_posXpath = url_ObjectDetailPage_description_posXpath  # 对象详情页面下Description input Xpath

# 对象组详情页
int_ObjectGroupDetailPage_subObjects_addButton_normalAdd_posXpath = acc_ObjectGroupDetailPage_subObjects_addButton_normalAdd_posXpath  # Subordinate Objects 下有数据新增时"+"按钮Xpath
int_ObjectGroupDetailPage_subObjects_addButton_newAdd_posXpath = acc_ObjectGroupDetailPage_subObjects_addButton_newAdd_posXpath  # Subordinate Objects 下无数据新增时"+"按钮Xpath
int_ObjectGroupDetailPage_subObjects_toggleDraw_addButton_posXpath = acc_ObjectGroupDetailPage_subObjects_toggleDraw_addButton_posXpath  # Object侧滑窗口的"+"按钮
int_ObjectGroupDetailPage_subObjects_toggleDraw_addButton_account_posXpath = acc_ObjectGroupDetailPage_subObjects_toggleDraw_addButton_account_posXpath  # Object侧滑窗口的"+"按钮下的single object
int_ObjectGroupDetailPage_subObjects_subCreateObjectDrawer_nameInput_posXpath = '//div[@class="drawer-box"]//div[@data-label="Name"]//input'  # 侧滑子Create Object页面Name input Xpath
int_ObjectGroupDetailPage_subObjects_subCreateObjectDrawer_itemsAddButton_posXpath = acc_ObjectGroupDetailPage_subObjects_subCreateAccountDrawer_itemsAddButton_posXpath  # 侧滑子Create Object页面中Items下的"+"按钮 Xpath
int_ObjectGroupDetailPage_subObjects_subCreateObjectDrawer_itemsValueInput_lowBoundary_posXpath = '(//div[@class="drawer-box"]//div[@class="CommonItems"]//div[@class="list-container"]//input)[1]'  # 侧滑子Create Interval页面中Items下的low_boundary输入框 Xpath
int_ObjectGroupDetailPage_subObjects_subCreateObjectDrawer_itemsValueInput_upBoundary_posXpath = '(//div[@class="drawer-box"]//div[@class="CommonItems"]//div[@class="list-container"]//input)[last()]'  # 侧滑子Create Interval页面中Items下的upBoundary输入框 Xpath\
int_ObjectGroupDetailPage_subObjects_subCreateObjectDrawer_itemsValueSaveButton_posXpath = acc_ObjectGroupDetailPage_subObjects_subCreateAccountDrawer_itemsValueSaveButton_posXpath  # 侧滑子Create Objects页面中Items下的保存按钮 Xpath
int_ObjectGroupDetailPage_subObjects_subCreateAccountDrawer_descriptionTextarea_posXpath = acc_ObjectGroupDetailPage_subObjects_subCreateAccountDrawer_descriptionTextarea_posXpath  # 侧滑子Create Objects页面中的Description textarea Xpath
int_ObjectGroupDetailPage_subObjects_subCreateAccountDrawer_okButton_posXpath = '//div[@class="drawer-box"]//div[@class="prox-fixed-footer policy-foot-color"]/button[@id="OK-_IntervalsDetail_VDraswer_EditDraw_IntervalsDetail_Home_App_anonymousComponent"]'  # 侧滑子Create Objects页面中OK按钮
int_ObjectGroupDetailPage_subObjects_subCreateAccountDrawer_okButton_yes_posXpath = url_ObjectDetailPage_okButton_yes_posXpath  # 侧滑子Create Account页面确认弹窗的“Yes”按钮
int_ObjectGroupDetailPage_subObjects_subCreateAccountDrawer_okButton_cancel_posXpath = url_ObjectDetailPage_okButton_cancel_posXpath  # 侧滑子Create Account页面确认弹窗的“Cancel”按钮
# 详情页通用元素
int_ObjectDetailPage_mainOkButton_poId = 'OK-_IntervalsDetail_Home_App_anonymousComponent'  # OK按钮ID
int_ObjectDetailPage_okButton_yes_posXpath = url_ObjectDetailPage_okButton_yes_posXpath  # 确认弹窗的“Yes”按钮
# Object Intervals elements area bottom===================Object Intervals elements area bottom===================Object Intervals elements area bottom===================Object Intervals elements area bottom===================Object Intervals elements area bottom===================
# Object Intervals elements area bottom===================Object Intervals elements area bottom===================Object Intervals elements area bottom===================Object Intervals elements area bottom===================Object Intervals elements area bottom===================


# Object Flags elements area top===================Object Flags elements area top===================Object Flags elements area top===================Object Flags elements area top===================Object Flags elements area top===================Object Flags elements area top===================
# Object Flags elements area top===================Object Flags elements area top===================Object Flags elements area top===================Object Flags elements area top===================Object Flags elements area top===================Object Flags elements area top===================

# 列表页
flag_listPage_createButton_posId = 'objectCreate-_OperateBtns_ElRow_Objects_flag_Home_App_anonymousComponent'  # 列表页create 按钮ID
flag_listPage_createButton_flag_posId = 'object0-_OperateBtns_ElRow_Objects_flag_Home_App_anonymousComponent'  # 列表页create下account ID
flag_listPage_createButton_flagountGroup_posId = 'object1-_OperateBtns_ElRow_Objects_flag_Home_App_anonymousComponent'  # 列表页create下account group ID
flag_listPage_editButton_posId = 'appEdit-_OperateBtns_ElRow_Objects_flag_Home_App_anonymousComponent'  # 列表页 Edit 按钮ID
flag_listPage_deleteButton_posId = 'appDel-_OperateBtns_ElRow_Objects_flag_Home_App_anonymousComponent'  # 列表页 Delete 按钮ID
flag_listPage_first_row_checkBox_posXpath = acc_listPage_first_row_checkBox_posXpath  # 列表页第一行对象多选框Xpath
flag_listPage_noDataText_posXpath = url_listPage_noDataText_posXpath  # 列表页无数据时的no data文本 Xpath
flag_listPage_object_exportButton_posXpath = listPage_object_urls_exportButton_posXpath  # 导出文件按钮 Xpath
flag_listPage_object_exportPopCheckbox_posXpaths = listPage_object_urls_exportPopCheckbox_posXpaths  # 导出数据选择确认弹窗CheckBox(多个)
flag_listPage_object_exportPopSelectAll_posXpath = listPage_object_urls_exportPopSelectAll_posXpath  # 导出数据选择确认弹窗全选CheckBox Xpath
flag_listPage_object_exportPopYes_posXpath = listPage_object_urls_exportPopYes_posXpath  # 导出数据选择确认弹窗 yes Xpath
flag_listPage_object_exportPopNo_posXpath = listPage_object_urls_exportPopNo_posXpath  # 导出数据选择确认弹窗 no Xpath
flag_listPage_object_tableDetails_singleObject_posXpaths = listPage_object_urls_tableDetails_singleObject_posXpaths  # 列表页中所有对象（不包含对象组）的DetailsXpath
flag_listPage_object_tableCheckbox_objectGroup_posXpaths = listPage_object_urls_tableCheckbox_objectGroup_posXpaths  # 列表页对象组的CheckBox（多个）
# flag_listPage_object_tableCheckbox_singleObject_posXpaths = listPage_object_urls_tableCheckbox_singleObject_posXpaths  # 列表页CheckBox（50）
flag_listPage_object_tableCheckbox_posXpaths = listPage_object_urls_tableCheckbox_posXpaths  # 列表页CheckBox（50）
flag_listPage_object_tableCheckbox_singleObject_posXpaths = listPage_object_urls_tableCheckbox_singleObject_posXpaths  # 列表页CheckBox（50），不包含Object Group
flag_listPage_object_tableCheckbox_selectedCheckBox_posXpaths = listPage_object_urls_tableDetails_selected_checkBox_posXpaths  # list页被选中的对象 CheckBox Xpath
flag_listPage_object_tableDetails_selected_detailsRow_posXpaths = listPage_object_urls_tableDetails_selected_detailsRow_posXpaths  # list页被选中的对象details 值Xpath
flag_listPage_object_tableDetails_firstRowValues_div_posXpaths = listPage_object_urls_tableDetails_firstRowValues_div_posXpaths  # list页点击Details后展示的数据Xpaths_div
# flag_listPage_usage_policies_elems_posXpaths = "//div[contains(@class,'LocalationDraswer ')]//div[contains(@class,'el-dropdown-menu')]"  # 点击Reference count后展开的侧滑页面，其中的引用条数
flag_listPage_usage_policies_elems_posXpaths = url_listPage_usage_policies_elems_posXpaths  # 点击Reference count后展开的侧滑页面，其中的引用条数
flag_listpage_linkButton_posId = 'btnCopy-_OperateBtns_ElRow_Objects_flag_Home_App_anonymousComponent'

# 列表页搜索选项
# 列表页搜索选项
flag_listPage_object_fuzzySearch_posXpath = listPage_object_urls_fuzzySearch_posXpath  # 模糊搜索选项
flag_listPage_object_searchId_posId = '1-_FilteredSearch_ElRow_Objects_flag_Home_App_anonymousComponent'  # ID 搜索
flag_listPage_object_searchName_posId = '2-_FilteredSearch_ElRow_Objects_flag_Home_App_anonymousComponent'  # name 搜索
flag_listPage_object_searchDetails_posId = '6-_FilteredSearch_ElRow_Objects_flag_Home_App_anonymousComponent'  # details搜索
flag_listPage_object_searchDescription_posId = '4-_FilteredSearch_ElRow_Objects_flag_Home_App_anonymousComponent'  # Description 搜索
flag_listPage_object_searchCreatedBy_posId = '5-_FilteredSearch_ElRow_Objects_flag_Home_App_anonymousComponent'  # created by 搜索
# flag_listPage_object_searchFqdn_posId = "7-_FilteredSearch_ElRow_Objects_flag_Home_App_anonymousComponent"  # fqdn 搜索
flag_listPage_object_tableDetails_detailsRow_firstDetailValue_posXpaths = listPage_object_urls_tableDetails_detailsRow_firstDetailValue_posXpaths  # 列表页某行第一个details值 Xpath

## listPage->Tips dialog  列表页 tips对话框
flag_listPage_object_delete_yesButton_posCss = acc_listPage_object_delete_yesButton_posCss  # 删除提示的Tips的yes按钮Xpath
flag_listPage_object_urls_delete_noButton_posCss = acc_listPage_object_urls_delete_noButton_posCss  # 删除提示的Tips的No按钮Xpath

# 对象详情页
flag_ObjectDetailPage_nameInput_posXpath = url_ObjectDetailPage_nameInput_posXpath  # Name输入框Xpath
flag_ObjectDetailPage_nameLenthNumber_posXpath = url_ObjectDetailPage_nameLenthNumber_posXpath  # Name输入框中字符长度数值Xpath
flag_ObjectDetailPage_item_addButton_poId = url_ObjectDetailPage_addButton_posId  # item下"+"按钮
flag_ObjectDetailPage_itemSaveButton_poXpath = url_ObjectDetailPage_itemSaveButton_posXpath  # item 下value保存按钮Xpath
flag_ObjectDetailPage_item_search_posId = url_ObjectDetailPage_object_ip_search_posId  # item 下搜索框id
flag_ObjectDetailPage_description_posXpath = url_ObjectDetailPage_description_posXpath  # 对象详情页面下Description input Xpath
flag_ObjectDetailPage_auditLogs_posXpath = url_ObjectDetailPage_auditLogs_posXpath  # Audit Logs Xpath
flag_ObjectDetailPage_auditLogsDrawer_firstRowLog_checkBox_posXpath = url_ObjectDetailPage_auditLogsDrawer_firstRowLog_checkBox_posXpath  # Audit Logs 侧滑页第一条日志CheckBox Xpath
flag_ObjectDetailPage_auditLogsDrawer_compareButton_posXpath = url_ObjectDetailPage_auditLogsDrawer_compareButton_posXpath  # Audit Logs 侧滑页Compare 按钮Xpath
flag_ObjectDetailPage_auditLogsDrawer_compareDrawer_operationText_posXpath = url_ObjectDetailPage_auditLogsDrawer_compareDrawer_operationText_posXpath  # Audit Logs 侧滑页点击Compare后的 operation text Xpath

# 详情页通用元素
flag_ObjectDetailPage_mainOkButton_poId = 'OK-_FlagsDetail_Home_App_anonymousComponent'  # OK按钮ID
flag_ObjectDetailPage_okButton_yes_posXpath = url_ObjectDetailPage_okButton_yes_posXpath  # 确认弹窗的“Yes”按钮

# 对象组详情页
flag_ObjectGroupDetailPage_subObjects_addButton_normalAdd_posXpath = acc_ObjectGroupDetailPage_subObjects_addButton_normalAdd_posXpath  # Subordinate Objects 下有数据新增时"+"按钮Xpath
flag_ObjectGroupDetailPage_subObjects_addButton_newAdd_posXpath = acc_ObjectGroupDetailPage_subObjects_addButton_newAdd_posXpath  # Subordinate Objects 下无数据新增时"+"按钮Xpath
flag_ObjectDetailPage_firstObject = url_ObjectDetailPage_firstUrlObject  ## 侧滑Objects列表中第一个flag object Xpath
flag_ObjectGroupDetailPage_subObjects_toggleDraw_addButton_posXpath = acc_ObjectGroupDetailPage_subObjects_toggleDraw_addButton_posXpath  # Flag侧滑窗口的"+"按钮
flag_ObjectGroupDetailPage_subObjects_toggleDraw_closeButton_posXpath = url_ObjectGroupDetailPage_subObjects_toggleDraw_closeButton_posXpath  # Flag侧滑窗口的Close按钮
flag_ObjectGroupDetailPage_subObjects_toggleDraw_addButton_flag_posXpath = acc_ObjectGroupDetailPage_subObjects_toggleDraw_addButton_account_posXpath  # Flag侧滑窗口的"+"按钮下的Flag
flag_ObjectGroupDetailPage_subObjects_subCreateFlagDrawer_nameInput_posXpath = acc_ObjectGroupDetailPage_subObjects_subCreateAccountDrawer_nameInput_posXpath  # 侧滑子Create Flag页面Name input Xpath
flag_ObjectGroupDetailPage_subObjects_subCreateFlagDrawer_itemsAddButton_posXpath = acc_ObjectGroupDetailPage_subObjects_subCreateAccountDrawer_itemsAddButton_posXpath  # 侧滑子Create Flag页面中Items下的"+"按钮 Xpath
flag_ObjectGroupDetailPage_subObjects_subCreateFlagDrawer_descriptionTextarea_posXpath = acc_ObjectGroupDetailPage_subObjects_subCreateAccountDrawer_descriptionTextarea_posXpath  # 侧滑子Create Flag 页面中的Description textarea Xpath
flag_ObjectGroupDetailPage_subObjects_subCreateFlagDrawer_itemsValueSaveButton_posXpath = acc_ObjectGroupDetailPage_subObjects_subCreateAccountDrawer_itemsValueSaveButton_posXpath  # 侧滑子Create Flag页面中Items下的保存按钮 Xpath
flag_ObjectGroupDetailPage_subObjects_subCreateFlagDrawer_okButton_posXpath = acc_ObjectGroupDetailPage_subObjects_subCreateAccountDrawer_okButton_posXpath  # 侧滑子Create Flag 页面中OK按钮
flag_ObjectGroupDetailPage_subObjects_subCreateFlagDrawer_okButton_yes_posXpath = url_ObjectDetailPage_okButton_yes_posXpath  # 侧滑子Create Flag 页面确认弹窗的“Yes”按钮
flag_ObjectGroupDetailPage_subObjects_subCreateFlagDrawer_okButton_cancel_posXpath = url_ObjectDetailPage_okButton_cancel_posXpath  # 侧滑子Create Flag页面确认弹窗的“Cancel”按钮
flagGroup_ObjectDetailPage_excludeObjectsSwitch_normalAdd_posXpath = urlGroup_ObjectDetailPage_excludeObjectsSwitch_normalAdd_posXpath  # Exclude Objects有数据时新增按钮Xpath
flagGroup_ObjectDetailPage_excludeObjectsSwitch_newAdd_posXpath = urlGroup_ObjectDetailPage_excludeObjectsSwitch_newAdd_posXpath  # Exclude Objects无数据时新增按钮Xpath
flag_ObjectDetailPage_secondObject = url_ObjectDetailPage_secondUrlObject  # 侧滑 Object中第二个url Xpath
flagGroup_ObjectDetailPage_excludeObjects_itemsArea_posXpath = urlGroup_ObjectDetailPage_excludeObjects_itemsArea_posXpath  # Exclude Objects下的item区域div Xpath
# flag_ObjectDetailPage_firstObject =url_ObjectDetailPage_firstUrlObject # 侧滑 Object中第一个url Xpath
flagGroup_ObjectDetailPage_excludeObjectsSwitch_posXpath = urlGroup_ObjectDetailPage_excludeObjectsSwitch_posXpath  # Exclude Objects Switch Xpath

# Object Flags elements area bottom===================Object Flags elements area bottom===================Object Flags elements area bottom===================Object Flags elements area bottom===================Object Flags elements area bottom===================Object Flags elements area bottom===================
# Object Flags elements area bottom===================Object Flags elements area bottom===================Object Flags elements area bottom===================Object Flags elements area bottom===================Object Flags elements area bottom===================Object Flags elements area bottom===================
# Object Geolocation elements area bottom===================Object Geolocation elements area bottom===================Object Geolocation elements area bottom===================Object Geolocation elements area bottom===================
# 对象详情页
port_ObjectDetailPage_nameInput_posXpath = acc_ObjectDetailPage_nameInput_posXpath  # Name输入框Xpath
port_ObjectDetailPage_item_addButton_poId = acc_ObjectDetailPage_item_addButton_poId  # item下"+"按钮
port_ObjectDetailPage_itemValueInput_poXpath = '//div[@class="item-box"]//input'  # item 下value输入框Xpath
port_ObjectDetailPage_itemSaveButton_poXpath = acc_ObjectDetailPage_itemSaveButton_poXpath  # item 下value保存按钮Xpath
port_ObjectDetailPage_item_search_posId = acc_ObjectDetailPage_item_search_posId  # item 下搜索框id
port_ObjectDetailPage_importFromFile_posXpath = acc_ObjectDetailPage_importFromFile_posXpath  # Import From File 按钮Xpath
port_ObjectDetailPage_pleaseUpload_posXpath = acc_ObjectDetailPage_pleaseUpload_posXpath  # Please Upload input标签Xpath
port_ObjectDetailPage_importUrlOk_posXpath = acc_ObjectDetailPage_importUrlOk_posXpath  # Import 页面 下的OK按钮Xpath
port_ObjectDetailPage_description_posXpath = acc_ObjectDetailPage_description_posXpath  # 对象详情页面下Description input Xpath
port_ObjectDetailPage_auditLogs_posXpath = acc_ObjectDetailPage_auditLogs_posXpath  # Audit Logs Xpath
port_ObjectDetailPage_auditLogsDrawer_firstRowLog_checkBox_posXpath = acc_ObjectDetailPage_auditLogsDrawer_firstRowLog_checkBox_posXpath  # Audit Logs 侧滑页第一条日志CheckBox Xpath
port_ObjectDetailPage_auditLogsDrawer_compareButton_posXpath = acc_ObjectDetailPage_auditLogsDrawer_compareButton_posXpath  # Audit Logs 侧滑页Compare 按钮Xpath
port_ObjectDetailPage_auditLogsDrawer_compareDrawer_operationText_posXpath = acc_ObjectDetailPage_auditLogsDrawer_compareDrawer_operationText_posXpath  # Audit Logs 侧滑页点击Compare后的 operation text Xpath
port_ObjectDetailPage_itemsTotal_posXpath = acc_ObjectDetailPage_itemsTotal_posXpath  # Items Total Xpath
port_ObjectDetailPage_nameLenthNumber_posXpath = acc_ObjectDetailPage_nameLenthNumber_posXpath  # Name输入框中字符长度数值Xpath
port_ObjectDetailPage_importFromFile_button_posXpath = acc_ObjectDetailPage_importFromFile_button_posXpath  # Import From File 按钮Xpath
port_ObjectDetailPage_importedFile_posXpath = acc_ObjectDetailPage_importedFile_posXpath  # 导入文件元素位置（Import From File 按钮旁）
port_ObjectDetailPage_importedFile_delete_posXpath = acc_ObjectDetailPage_importedFile_delete_posXpath  # 文件删除按钮
port_ObjectDetailPage_importedFile_download_posXpath = acc_ObjectDetailPage_importedFile_download_posXpath  # 文件下载按钮
port_ObjectDetailPage_leaveThisPage_yesButton_posXpath = '//button[contains(@class,"operation-confirm-Leave")]'
port_ObjectDetailPage_clearCounter_posXpath = acc_ObjectDetailPage_clearCounter_posXpath  # Clear Counter 按钮
port_ObjectDetailPage_dupAlert_posXpath = '//div[@title="Duplicate data exists"]'  # item重复提示
port_ObjectDetailPage_dupAlert_duplicateListTotal_posXpath = '//div[@class="DuplicateList list-box"]//p[contains(@class,"total")]'  # duplicateList中的“Total：xx”

# 列表页
port_listPage_createButton_posId = 'objectCreate-_OperateBtns_ElRow_Objects_port_Home_App_anonymousComponent'  # 列表页create 按钮ID
port_listPage_createButton_port_posId = 'object0-_OperateBtns_ElRow_Objects_port_Home_App_anonymousComponent'  # 列表页create下account ID
port_listPage_createButton_portGroup_posId = 'object1-_OperateBtns_ElRow_Objects_port_Home_App_anonymousComponent'  # 列表页create下account group ID
port_listPage_editButton_posId = 'appEdit-_OperateBtns_ElRow_Objects_port_Home_App_anonymousComponent'  # 列表页 Edit 按钮ID
port_listPage_noDataText_posXpath = url_listPage_noDataText_posXpath  # 列表页无数据时的no data文本 Xpath
port_listPage_first_row_checkBox_posXpath = '(//td[@rowspan="1"and @colspan="1"]//span[@class="el-checkbox__inner"])[1]'  # 列表页第一行对象多选框Xpath
port_listPage_deleteButton_posId = 'appDel-_OperateBtns_ElRow_Objects_port_Home_App_anonymousComponent'  # 列表页 Delete 按钮ID
port_object_columnSetting_descriptionOption_posXpath = listPage_object_urls_columnSetting_descriptionOption_posXpath  # 列设置中的description选项元素Xpath
port_listPage_object_exportButton_posXpath = listPage_object_urls_exportButton_posXpath  # 导出文件按钮 Xpath
port_listPage_object_exportPopYes_posXpath = listPage_object_urls_exportPopYes_posXpath  # 导出数据选择确认弹窗 yes Xpath
port_listPage_object_tableCheckbox_singleObject_posXpaths = listPage_object_urls_tableCheckbox_singleObject_posXpaths  # 列表页CheckBox（50）
port_listPage_object_tableCheckbox_objectGroup_posXpaths = listPage_object_urls_tableCheckbox_objectGroup_posXpaths  # 列表页对象组的CheckBox（多个）
port_listPage_object_tableCheckbox_posXpaths = listPage_object_urls_tableCheckbox_posXpaths  # 列表页CheckBox（50）
port_listPage_object_tableDetails_singleObject_posXpaths = listPage_object_urls_tableDetails_singleObject_posXpaths  # 列表页中所有对象（不包含对象组）的DetailsXpath
port_listPage_object_tableDetails_selected_detailsRow_posXpaths = listPage_object_urls_tableDetails_selected_detailsRow_posXpaths  # list页被选中的对象details 值Xpath
port_listPage_object_tableDetails_firstRowValues_div_posXpaths = listPage_object_urls_tableDetails_firstRowValues_div_posXpaths  # list页点击Details后展示的数据Xpaths_div
port_listPage_object_exportPopSelectAll_posXpath = listPage_object_urls_exportPopSelectAll_posXpath  # 导出数据选择确认弹窗全选CheckBox Xpath
port_listPage_object_exportPopCheckbox_posXpaths = listPage_object_urls_exportPopCheckbox_posXpaths  # 导出数据选择确认弹窗CheckBox(多个)
port_listPage_object_exportPopNo_posXpath = listPage_object_urls_exportPopNo_posXpath  # 导出数据选择确认弹窗 no Xpath
port_listPage_object_tableCheckbox_selectedCheckBox_posXpaths = listPage_object_urls_tableDetails_selected_checkBox_posXpaths  # list页被选中的对象 CheckBox Xpath
port_listPage_object_tableCheckbox_firstObjectGroup_posXpath = listPage_object_urls_tableDetails_firstObjectGroup_posXpath  # 列表页中第一个Object Group 的CheckBox
port_listPage_object_tableCheckbox_firstSingleObject_posXpath = listPage_object_urls_tableDetails_firstSingleObject_posXpath  # 列表页中第一个列表页中第一个Single Object 的CheckBox
port_listPage_object_tableCheckbox_firstNotLocalVsys_objectOrGroup_posXpath = listPage_object_urls_tableCheckbox_firstNotLocalVsys_objectOrGroup_posXpath  # 列表页中第一个不是本Vsys的对象或对象组的CheckBox
port_listPage_object_tableCheckbox_notLocalVsys_objectOrGroup_posXpaths = listPage_object_urls_tableCheckbox_notLocalVsys_objectOrGroup_posXpaths  # 列表页中不是本Vsys的对象或对象组的CheckBox
port_listPage_object_clearCounterPopYes_posXpath = listPage_object_urls_clearCounterPopYes_posXpath  # Clear Counter 选择确认弹窗中的Yes确认按钮
port_listpage_linkButton_posId = '@id="btnCopy-_OperateBtns_ElRow_Objects_port_Home_App_anonymousComponent'

# 详情页通用元素
port_ObjectDetailPage_mainOkButton_poId = 'OK-_PortDetail_Home_App_anonymousComponent'  # OK按钮ID
port_ObjectDetailPage_okButton_yes_posXpath = acc_ObjectDetailPage_okButton_yes_posXpath  # 确认弹窗的“Yes”按钮

# 对象组详情页
port_ObjectGroupDetailPage_subObjects_addButton_normalAdd_posXpath = '//div[@data-desc="subObject"]//i[@class="operate-icon iconfont icon-Create1"]'  # Subordinate Objects 下有数据新增时"+"按钮Xpath
port_ObjectGroupDetailPage_subObjects_addButton_newAdd_posXpath = '//div[@data-desc="subObject"]//div[@class="AddButton"]'  # Subordinate Objects 下无数据新增时"+"按钮Xpath
port_ObjectGroupDetailPage_subObjects_toggleDraw_addButton_posXpath = '//div[@class="ToggleDraw"]//div[contains(@class,"search-box")]//button'  # Ports侧滑窗口的"+"按钮
port_ObjectGroupDetailPage_subObjects_toggleDraw_addButton_port_posXpath = '(//ul[@class="el-dropdown-menu el-popper el-dropdown-menu--small"]/li[not(contains(text(),"Group"))])[last()]'  # Ports侧滑窗口的"+"按钮下的Port
port_ObjectGroupDetailPage_subObjects_subCreatePortDrawer_nameInput_posXpath = '//*[@id="router-view-container"]//div[@class="drawer-box"]//div[@data-label="Name"]//input'  # 侧滑子Create Ports页面Name input Xpath
port_ObjectGroupDetailPage_subObjects_subCreatePortDrawer_itemsAddButton_posXpath = '//div[@class="drawer-box"]//div[@class="CommonItems"]//div[@class="object-item-add"]/div[@class="IconBtn"]'  # 侧滑子Create Ports页面中Items下的"+"按钮 Xpath
port_ObjectGroupDetailPage_subObjects_subCreatePortDrawer_itemsValueInput_posXpath = '//*[@id="router-view-container"]//div[@class="item-box"]//input'  # 侧滑子Create Ports页面中Items下的item value输入框 Xpath
port_ObjectGroupDetailPage_subObjects_subCreatePortDrawer_itemsValueSaveButton_posXpath = '//div[@class="drawer-box"]//div[@class="CommonItems"]//i[contains(@class,"icon-save")]'  # 侧滑子Create Ports页面中Items下的保存按钮 Xpath
port_ObjectGroupDetailPage_subObjects_subCreatePortDrawer_descriptionTextarea_posXpath = '//div[@class="drawer-box"]//label[text()="Description"]/..//textarea'  # 侧滑子Create Ports页面中的Description textarea Xpath
port_ObjectGroupDetailPage_subObjects_subCreatePortDrawer_okButton_posXpath = '//*[@id="OK-_PortDetail_VDraswer_EditDraw_PortDetail_Home_App_anonymousComponent"]'  # 侧滑子Create Account页面中OK按钮
port_ObjectGroupDetailPage_subObjects_subCreatePortDrawer_okButton_yes_posXpath = acc_ObjectGroupDetailPage_subObjects_subCreateAccountDrawer_okButton_yes_posXpath  # 侧滑子Create Account页面确认弹窗的“Yes”按钮
port_ObjectDetailPage_firstPortObject = acc_ObjectDetailPage_firstAccObject  ## 侧滑Objects列表中第一个acc object Xpath
portGroup_ObjectDetailPage_excludeObjectsSwitch_posXpath = accGroup_ObjectDetailPage_excludeObjectsSwitch_posXpath  # Exclude Objects Switch Xpath
portGroup_ObjectDetailPage_excludeObjects_itemsArea_posXpath = accGroup_ObjectDetailPage_excludeObjects_itemsArea_posXpath  # Exclude Objects下的item区域div Xpath
portGroup_ObjectDetailPage_excludeObjectsSwitch_newAdd_posXpath = accGroup_ObjectDetailPage_excludeObjectsSwitch_newAdd_posXpath  # Exclude Objects无数据时新增按钮Xpath
port_ObjectDetailPage_firstObject = acc_ObjectDetailPage_firstObject  # 侧滑acc Object中第一个url Xpath
port_ObjectGroupDetailPage_subObjects_toggleDraw_closeButton_posXpath = acc_ObjectGroupDetailPage_subObjects_toggleDraw_closeButton_posXpath  # Accounts侧滑窗口的Close按钮
portGroup_ObjectDetailPage_excludeObjectsSwitch_normalAdd_posXpath = accGroup_ObjectDetailPage_excludeObjectsSwitch_normalAdd_posXpath  # Exclude Objects有数据时新增按钮Xpath
port_ObjectDetailPage_secondObject = acc_ObjectDetailPage_secondObject  # 侧滑acc Object中第二个url Xpath

## listPage->Tips dialog  列表页 tips对话框
port_listPage_object_delete_yesButton_posCss = 'body>.el-dialog__wrapper .delComponents-ok span'  # 删除提示的Tips的yes按钮Xpath
port_listPage_object_urls_delete_noButton_posCss = 'body>.el-dialog__wrapper .delComponents-close span'  # 删除提示的Tips的No按钮Xpath

# 列表页搜索选项
port_listPage_object_fuzzySearch_posXpath = listPage_object_urls_fuzzySearch_posXpath  # 模糊搜索选项
port_listPage_object_searchId_posId = '1-_FilteredSearch_ElRow_Objects_port_Home_App_anonymousComponent'  # ID 搜索
port_listPage_object_searchName_posId = '2-_FilteredSearch_ElRow_Objects_port_Home_App_anonymousComponent'  # name 搜索
port_listPage_object_searchDescription_posId = '4-_FilteredSearch_ElRow_Objects_port_Home_App_anonymousComponent'  # Description 搜索
port_listPage_object_tableDetails_detailsRow_firstDetailValue_posXpaths = listPage_object_urls_tableDetails_detailsRow_firstDetailValue_posXpaths  # 列表页某行第一个details值 Xpath
#Object Geolocation elements area bottom===================Object Geolocation elements area bottom===================Object Geolocation elements area bottom===================Object Geolocation elements area bottom===================
listPage_object_geolocation_createButton_posId = "app_create-_OperateBtns_ElRow_Geography_List_Home_App_anonymousComponent" #Geolocation页面Create按钮
listPage_object_geolocation_delButton_posId = "appDel-_OperateBtns_ElRow_Geography_List_Home_App_anonymousComponent" #Geolocation页面del按钮
listPage_object_geolocation_editButton_posId = "appEdit-_OperateBtns_ElRow_Geography_List_Home_App_anonymousComponent" #Geolocation页面edit按钮
listPage_object_geolocation_delYesButton_posXpath = "//div[@class='el-message-box el-message-box--center']//span[normalize-space(text())='Delete']"#删除后确认删除按钮
geo_ObjectCreate_Continent_select_button_posID = "ip_geography_continent"       #创建页面添加Continet按钮
geo_ObjectCreate_type_city_posXpath = "//div[@id='ip_geography_type']//span[normalize-space(text())='City']"
geo_Geographic_add_continent_button_posXpath = "//div[@class='add_custom']//span[text()='Add Continent']"  # 点击添加按钮后侧滑页 Add Continet按钮
geo_Geographic_add_continent_text_input_posXpath = "//div[@class='add_input']/div/input"  # Add Continet文本输入框
geo_Geographic_add_continent_save_button_posID = "saveGeoCountry"
geo_Geographic_add_continent_cancel_button_posID = "interceptionadd_allcancelobject9"
geo_ObjectCreate_geo_name_id_posID = "ip_geography_name"
geo_ObjectCreate_Country_Abbreviation_posID = "ip_geography_countryAbbr"
geo_ObjectCreate_Country_Region_posID = "ip_geography_Country1"
geo_ObjectCreate_Longitude_posXPATH = "//input[@id='ip_geography_longitude']"
geo_ObjectCreate_Latitude_posXPATH = "//input[@id='ip_geography_latitude']"
geo_ObjectCreate_add_super_administrative_area_button_posXpath = "//div[@id='add_ip_geography_location']/i"
geo_ObjectCreate_super_administrative_area_posID = "ip_geography_Country"
geo_ObjectCreate_add_super_administrative_area_text_posXpath = "//div[@class='add_input']/input"
geo_Geographic_add_custom_button_posXpath = "//div[@id='addContentTree']//span[text()='Add Custom']"
geo_Geographic_add_super_administrative_area_save_button_posID = "addLocation"
geo_ObjectCreate_ip_add_button_posID = "ip_geography_IPRange"
geo_ObjectCreate_ip_item_add_button_posID = "addIPList"
geo_ObjectCreate_ip_item_type_posID = "geoAddrType"
geo_ObjectCreate_ip_item_type_ipv6_posXpath = "//div[@class='el-select-dropdown el-popper']//span[text()='IPv6']"
geo_ObjectCreate_ip_item_text_save_button_posXpath = "//div[@class='IconBtn iconfont icon-save check margin-right7 fontsize18 IPIcon']"
geo_ObjectCreate_button_OK_posXpath = "//button[@id='IP_library_add']/span"
geo_ObjectCreate_button_Cancel_posXpath = "//button[@id='IP_library_cancel']/span"
geo_ObjectCreate_button_warningSaveYes_posXpath = ip_addressObjectPage_button_warningSaveYes_posXpath
geoObjectPage_button_editItem_text_Save_posXpath = "//ul[@class='list']//div[@class='IconBtn iconfont icon-save check margin-right7 fontsize18 IPIcon']"
geoObjectPage_item_error_posXpath = "//*[@id='router-view-container']//div[@class='object-item-error']/span"
geo_ObjectCreate_contry_error_posXpath = "(//div[@class='el-form-item el-form-item--small']//div[@class='el-form-item__error'])[1]"
geo_ObjectCreate_geo_name_error_posXpath = "//div[@class='el-form-item biFangName is-error el-form-item--small']//div[@class='el-form-item__error']"
geo_ObjectCreate_city_ip_range_error_posXpath = "(//div[@class='el-form-item__content']/div[@class='el-form-item__error'])[2]"
geo_ObjectCreate_Longitude_error_posXpath = "(//div[@class='el-form-item is-error el-form-item--small']//div[@class='el-form-item__error'])[1]"
geo_ObjectCreate_Latitude_error_posXpath = "(//div[@class='el-form-item is-error el-form-item--small']//div[@class='el-form-item__error'])[2]"
geo_ObjectCreate_country_abbr_error_posXpath = "//div[@class='el-form-item is-error el-form-item--small']//div[@class='el-form-item__error']"
geo_ObjectCreate_country_region_error_posXpath = "//*[@class='el-form-item biFangName is-error el-form-item--small']//div[@class='el-form-item__error']"
geo_Geographic_add_continent_search_button_posID = "objectName_seach-_Geographyadd_Home_App_anonymousComponent"
geo_Geographic_super_admin_search_button_posID = "objectName_seach-_locationComponents_Geographyadd_Home_App_anonymousComponent"
geo_ObjectCreate_sideslip_fist_data_posXpath = "//*[@id='selectContentTree']"
geo_ObjectCreate_sideslip_no_data_posXpath = "//div[@class='conditions-right right-show-edit sideslipStyle']//div[normalize-space(text())='No Data']"


#alter提示
main_listPage_object_error_alter_postXpath = "//div[@role='alert'][1]"

# Object ASNs elements area top===================# Object ASNs elements area top===================# Object ASNs elements area top===================# Object ASNs elements area top===================# Object ASNs elements area top===================# Object ASNs elements area top===================
# Object ASNs elements area top===================# Object ASNs elements area top===================# Object ASNs elements area top===================# Object ASNs elements area top===================# Object ASNs elements area top===================# Object ASNs elements area top===================
# 列表页
asn_listPage_createButton_posId = 'app_create-_OperateBtns_ElRow_Objects_asn_Home_App_anonymousComponent'  # 列表页create 按钮ID
# asn_listPage_createButton_singleObject_posId = 'object0-_OperateBtns_ElRow_Objects_account_Home_App_anonymousComponent'  # 列表页create下account ID
asn_listPage_editButton_posId = 'appEdit-_OperateBtns_ElRow_Objects_asn_Home_App_anonymousComponent'  # 列表页 Edit 按钮ID
asn_listPage_deleteButton_posId = 'appDel-_OperateBtns_ElRow_Objects_asn_Home_App_anonymousComponent'  # 列表页 Delete 按钮ID

asn_object_columnSetting_descriptionOption_posXpath = listPage_object_urls_columnSetting_descriptionOption_posXpath  # 列设置中的description选项元素Xpath
asn_listPage_first_row_checkBox_posXpath = acc_listPage_first_row_checkBox_posXpath  # 列表页第一行对象多选框Xpath
asn_listPage_noDataText_posXpath = url_listPage_noDataText_posXpath  # 列表页无数据时的no data文本 Xpath
asn_listPage_object_importButton_posXpath = listPage_object_urls_importButton_posXpath  # 导入文件按钮 Xpath
asn_listPage_object_exportButton_posXpath = listPage_object_urls_exportButton_posXpath  # 导出文件按钮 Xpath
asn_listPage_object_exportPopYes_posXpath = listPage_object_urls_exportPopYes_posXpath  # 导出数据选择确认弹窗 yes Xpath
asn_listPage_object_clearCounterPopYes_posXpath = listPage_object_urls_clearCounterPopYes_posXpath  # Clear Counter 选择确认弹窗中的Yes确认按钮
asn_listPage_object_exportPopNo_posXpath = listPage_object_urls_exportPopNo_posXpath  # 导出数据选择确认弹窗 no Xpath
asn_listPage_object_exportPopSelectAll_posXpath = listPage_object_urls_exportPopSelectAll_posXpath  # 导出数据选择确认弹窗全选CheckBox Xpathcat
asn_listPage_object_exportPopCheckbox_posXpaths = listPage_object_urls_exportPopCheckbox_posXpaths  # 导出数据选择确认弹窗CheckBox(多个)
asn_listPage_object_tableDetails_firstRowValues_div_posXpaths = listPage_object_urls_tableDetails_firstRowValues_div_posXpaths  # list页点击Details后展示的数据Xpaths_div
asn_listPage_object_tableDetails_selected_detailsRow_posXpaths = listPage_object_urls_tableDetails_selected_detailsRow_posXpaths  # list页被选中的对象details 值Xpath
asn_listPage_object_tableCheckbox_posXpaths = listPage_object_urls_tableCheckbox_posXpaths  # 列表页CheckBox（50）
asn_listPage_object_tableCheckbox_singleObject_posXpaths = listPage_object_urls_tableCheckbox_singleObject_posXpaths  # 列表页single Object CheckBox（多个）
asn_listPage_object_tableCheckbox_firstSingleObject_posXpath = listPage_object_urls_tableDetails_firstSingleObject_posXpath  # 列表页中第一个列表页中第一个Single Object 的CheckBox
asn_listPage_object_tableCheckbox_objectGroup_posXpaths = listPage_object_urls_tableCheckbox_objectGroup_posXpaths  # 列表页对象组的CheckBox（多个）
asn_listPage_object_tableCheckbox_firstObjectGroup_posXpath = listPage_object_urls_tableDetails_firstObjectGroup_posXpath  # 列表页中第一个Object Group 的CheckBox
asn_listPage_object_tableCheckbox_notLocalVsys_objectOrGroup_posXpaths = listPage_object_urls_tableCheckbox_notLocalVsys_objectOrGroup_posXpaths  # 列表页中不是本Vsys的对象或对象组的CheckBox
asn_listPage_object_tableCheckbox_firstNotLocalVsys_objectOrGroup_posXpath = listPage_object_urls_tableCheckbox_firstNotLocalVsys_objectOrGroup_posXpath  # 列表页中第一个不是本Vsys的对象或对象组的CheckBox
asn_listPage_object_tableDetails_singleObject_posXpaths = listPage_object_urls_tableDetails_singleObject_posXpaths  # 列表页中所有对象（不包含对象组）的DetailsXpath
asn_listPage_object_tableCheckbox_selectedCheckBox_posXpaths = listPage_object_urls_tableDetails_selected_checkBox_posXpaths  # list页被选中的对象 CheckBox Xpath
asn_listPage_object_tableCheckbox_localVsys_objectOrGroup_posXpaths = listPage_object_urls_tableCheckbox_localVsys_objectOrGroup_posXpaths  # 列表页中本Vsys的Object 或Group（不包含其他Vsys）
asn_listPage_object_tableCheckbox_localVsys_firstObjectOrGroup_posXpaths = listPage_object_urls_tableCheckbox_localVsys_firstObjectOrGroup_posXpath  # 列表页中第一个本Vsys的Object 或Group（不包含其他Vsys）

asn_listPage_object_tableDetails_firstASNValue_posXpaths = '(//span[contains(text(),"AS ")])[1]'#列表页第一行的ASN 数值
## listPage->Tips dialog  列表页 tips对话框
asn_listPage_object_delete_yesButton_posCss = acc_listPage_object_delete_yesButton_posCss  # 删除提示的Tips的yes按钮Xpath
asn_listPage_object_urls_delete_noButton_posCss = acc_listPage_object_urls_delete_noButton_posCss  # 删除提示的Tips的No按钮Xpath

# 列表页搜索选项
asn_listPage_object_fuzzySearch_posXpath = listPage_object_urls_fuzzySearch_posXpath  # 模糊搜索选项x
asn_listPage_object_searchId_posId = '1-_FilteredSearch_ElRow_Objects_asn_Home_App_anonymousComponent'  # ID 搜索
asn_listPage_object_searchName_posId = '2-_FilteredSearch_ElRow_Objects_asn_Home_App_anonymousComponent'  # name 搜索
asn_listPage_object_searchDetails_posId = '6-_FilteredSearch_ElRow_Objects_asn_Home_App_anonymousComponent'  # details搜索
asn_listPage_object_searchDescription_posId = '4-_FilteredSearch_ElRow_Objects_asn_Home_App_anonymousComponent'  # Description 搜索
asn_listPage_object_searchASN_posId = '44-_FilteredSearch_ElRow_Objects_asn_Home_App_anonymousComponent'#asn 搜索
asn_listPage_object_searchCreatedBy_posId = '5-_FilteredSearch_ElRow_Objects_asn_Home_App_anonymousComponent'  # created by 搜索
asn_listPage_object_tableDetails_detailsRow_firstDetailValue_posXpaths = listPage_object_urls_tableDetails_detailsRow_firstDetailValue_posXpaths  # 列表页某行第一个details值 Xpath

# 详情页
asn_ObjectDetailPage_asnInput_posXpath = '//div[@class="ASN-input el-input el-input--small"]//input'  # 详情页ASN输入框
asn_ObjectDetailPage_asnInputError_posXpath = '//div[@data-label="ASN"]//div[@class="el-form-item__error"]'#详情页ASN输入框下的字段错误提示
asn_ObjectDetailPage_nameInputError_posXpath = '//div[@data-label="Name"]//div[@class="el-form-item__error"]'#详情页ASN输入框下的字段错误提示
asn_ObjectDetailPage_nameInput_posXpath = url_ObjectDetailPage_nameInput_posXpath  # Name输入框Xpath
asn_ObjectDetailPage_nameLenthNumber_posXpath = url_ObjectDetailPage_nameLenthNumber_posXpath  # Name输入框中字符长度数值Xpath
asn_ObjectDetailPage_item_addButton_poId = url_ObjectDetailPage_addButton_posId  # item下"+"按钮
asn_ObjectDetailPage_item_subAddButton_poXpath = url_ObjectDetailPage_item_subAddButton_poXpath  # 单个Item中新增多条数据的"+"按钮
# acc_ObjectDetailPage_item_subAddButton_poId = '//*[@class="item-box"]//*[contains(@class,"addobject")]'  # 单个Item中新增多条数据的"+"按钮
asn_ObjectDetailPage_itemValueInput_poXpath = '//div[@class="item-box"]//div[contains(@class,"content-input")]//input'  # item 下value输入框Xpath
# acc_ObjectDetailPage_itemValueInput_poXpath = '//div[@class="expr-box"]//input'  # item 下value输入框Xpath
asn_ObjectDetailPage_itemSaveButton_poXpath = url_ObjectDetailPage_itemSaveButton_posXpath  # item 下value保存按钮Xpath
asn_ObjectDetailPage_item_search_posId = url_ObjectDetailPage_object_ip_search_posId  # item 下搜索框id
asn_ObjectDetailPage_description_posXpath = url_ObjectDetailPage_description_posXpath  # 对象详情页面下Description input Xpath
asn_ObjectDetailPage_auditLogs_posXpath = url_ObjectDetailPage_auditLogs_posXpath  # Audit Logs Xpath
asn_ObjectDetailPage_auditLogsDrawer_firstRowLog_checkBox_posXpath = url_ObjectDetailPage_auditLogsDrawer_firstRowLog_checkBox_posXpath  # Audit Logs 侧滑页第一条日志CheckBox Xpath
asn_ObjectDetailPage_auditLogsDrawer_compareButton_posXpath = url_ObjectDetailPage_auditLogsDrawer_compareButton_posXpath  # Audit Logs 侧滑页Compare 按钮Xpath
asn_ObjectDetailPage_auditLogsDrawer_compareDrawer_operationText_posXpath = url_ObjectDetailPage_auditLogsDrawer_compareDrawer_operationText_posXpath  # Audit Logs 侧滑页点击Compare后的 operation text Xpath
asn_ObjectDetailPage_itemsTotal_posXpath = url_ObjectDetailPage_itemsTotal_posXpath  # Items Total Xpath
asn_ObjectDetailPage_importFromFile_posXpath = url_ObjectDetailPage_importFromFile_posXpath  # Import From File 按钮Xpath
asn_ObjectDetailPage_importFromFile_button_posXpath = url_ObjectDetailPage_importFromFile_button_posXpath  # Import From File 按钮Xpath
asn_ObjectDetailPage_pleaseUpload_posXpath = url_ObjectDetailPage_pleaseUpload_posXpath  # Please Upload input标签Xpath
asn_ObjectDetailPage_importUrlOk_posXpath = url_ObjectDetailPage_importUrlOk_posXpath  # Import 页面 下的OK按钮Xpath
asn_ObjectDetailPage_clearCounter_posXpath = url_ObjectDetailPage_clearCounter_posXpath  # Clear Counter 按钮

asn_ObjectDetailPage_dupAlert_posXpath = acc_ObjectDetailPage_dupAlert_posXpath  # item重复提示
asn_ObjectDetailPage_dupAlert_duplicateListTotal_posXpath = acc_ObjectDetailPage_dupAlert_duplicateListTotal_posXpath # duplicateList中的“Total：xx”
asn_ObjectDetailPage_importedFile_posXpath = url_ObjectDetailPage_importedFile_posXpath  # 导入文件元素位置（Import From File 按钮旁）
asn_ObjectDetailPage_importedFile_delete_posXpath = url_ObjectDetailPage_importedFile_delete_posXpath  # 文件删除按钮
asn_ObjectDetailPage_importedFile_download_posXpath = url_ObjectDetailPage_importedFile_download_posXpath  # 文件下载按钮

asn_ObjectDetailPage_leaveThisPage_yesButton_posXpath = '//button[contains(@class,"operation-confirm-Leave")]'#is_leave_this_page_exist 弹窗中的确认按钮

# 详情页通用元素
asn_ObjectDetailPage_mainOkButton_poId = 'OK-_ASNDetail_Home_App_anonymousComponent'  # OK按钮ID
asn_ObjectDetailPage_okButton_yes_posXpath = url_ObjectDetailPage_okButton_yes_posXpath  # 确认弹窗的“Yes”按钮
# Object ASNs elements area bottom===================# Object ASNs elements area bottom===================# Object ASNs elements area bottom===================# Object ASNs elements area bottom===================# Object ASNs elements area bottom===================# Object ASNs elements area bottom===================
# Object ASNs elements area bottom===================# Object ASNs elements area bottom===================# Object ASNs elements area bottom===================# Object ASNs elements area bottom===================# Object ASNs elements area bottom===================# Object ASNs elements area bottom===================

mainPage_GeolocationSearch_buttonSearch_Item_posId = "IPseach"
geoObjectPage_button_addItem_first_item_posXpath = "//*[@class='object-item-sub-ip table-hide']"
geoObjectPage_button_editItem_posXpath = "//div[@class='IconBtn iconfont icon-Edit fontsize18 IPIcon']"
geoObjectPage_button_editItem_text_posXpath = "//div[@class='object-item-box']//ul[@class='list']//div[@class='object-item-sub-ip el-input el-input--small']/input"

# Main Dashboard elements area bottom===================# Main Dashboard elements area bottom===================# Main Dashboard elements area bottom===================# Main Dashboard elements area bottom===================# Main Dashboard elements area bottom===================# Main Dashboard elements area bottom===================
mainPage_main_dashboard_posXpath = "//div[@class='VDropdown']//span[@title='Main Dashboard']"
mainPage_create_button_dashboard_posXpath ="//div[@class='VDropdown']//i[@class='el-icon-plus']"
mainPage_create_chart_button_posXpath ="//div[@class='CustomDashboard']//div[@class='el-card__body']"
dashboard_chart_name_text_posXpath = "//div[@class='el-form-item el-form-item--small']//div[@class='width280px el-input el-input--small']//input[@class='el-input__inner']"
dashboard_chart_visualization_type_table_posXpath = "(//div[@class='el-radio-group visualization-type-radio']//span[@class='el-radio__label'])[1]"
dashboard_chart_visualization_type_line_posXpath = "(//div[@class='el-radio-group visualization-type-radio']//span[@class='el-radio__label'])[2]"
dashboard_chart_visualization_type_bar_posXpath = "(//div[@class='el-radio-group visualization-type-radio']//span[@class='el-radio__label'])[3]"
dashboard_chart_visualization_type_area_posXpath = "(//div[@class='el-radio-group visualization-type-radio']//span[@class='el-radio__label'])[4]"
dashboard_chart_visualization_type_pie_posXpath = "(//div[@class='el-radio-group visualization-type-radio']//span[@class='el-radio__label'])[5]"
dashboard_chart_metric_add_button_posXpath = "//div[@class='Metrics']//i[@class='iconfont icon-Create1 fontsize14']"
dashboard_chart_metric_field_select_button_posXpath = "(//div[@class='Metrics']//i[@class='el-select__caret el-input__icon el-icon-arrow-up'])[1]"
dashboard_chart_metric_aggregate_select_button_posXpath = "(//div[@class='Metrics']//i[@class='el-select__caret el-input__icon el-icon-arrow-up'])[2]"

