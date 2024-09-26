#mainPage_navigationBar_logo_posCss = ".tsg-img-logo"
mainPage_firstLevelMenu_dashboards_posCss = "#dashboard .level1-title"
mainPage_navigationBar_logo_posCss = mainPage_firstLevelMenu_dashboards_posCss    # 改为引用dashboard路径
mainPage_firstLevelMenu_Objects_posId = "object"  # 一级菜单Global Objects
mainPage_secondLevelMenu_ipAddress_posId = "Objects_ip"  # 二级菜单IP Addresses
mainPage_secondLevelMenu_Ports_posId = "Objects_port"  # 二级菜单Ports
mainPage_secondLevelMenu_FQDNs_posId = "Objects_fqdn"  # 二级菜单FQDNs
mainPage_secondLevelMenu_Subscriber_ids_posId = "Objects_subscriberid"  # 二级菜单Subscriber IDs
mainPage_secondLevelMenu_HTTP_Signatures_posId = "Objects_http_signature"  # 二级菜单HTTP Signatures
mainPage_secondLevelMenu_keywords_posId = "Objects_keywords"  # 二级菜单keywords
mainPage_secondLevelMenu_urls_posId = "Objects_url"  # 二级菜单url
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

mainPage_ObjectSearch_selectLabel_posId = "select-label"  # 查询框id
mainPage_ObjectSearch_buttonSearch_posId = "searchQuery"  # 查询按钮id
mainPage_ObjectSearch_buttonClear_posId = "searchClear"  # 清空查询按钮id
mainPage_ObjectSearch_buttonSearch_Item_posId = "object_ip_search"  # 查询item输入框id
mainPage_ObjectSearch_buttonSearch_Item_first_content_posXpath = "//div[@class='view-row']//span[@class='el-tooltip content-show']"  # item搜索框第一个元素
mainPage_ObjectSearch_buttonSearch_Item_posXpath = "//div/div/div/div[2]/div/div[1]/div/div/div/div[2]/div[1]/div/div[1]/div[1]/div/div/input"  # 查询item输入框Xpath
mainPage_ObjectSearch_buttonAddItem_posXpath = "//div[@id='temporary_form']"  # 添加item_id
mainPage_ObjectSearch_input_Item_posId = "onlyMarvel"  # 输入item_id
main_Group_sub_Object_input_frame_select_one_posXpath = "//div/div[1]/div/div/div/div[2]/div[1]/div/div[2]/div/ul/li[1]/div[2]/span"  # 搜索框第一个元素

mainPage_button_menu_posXCss = ".menu-btn span"
mainPage_currentPage_vsysName_posXpath = "//span[@class='root-title']"
mainPage_vsysTree_vsysName_posXpath = "//div[contains(@class, 'menu-level2')]//article//div[@class='menu-title']/parent::*"    # vsys tree中vsys name定位

#通用元素定位
main_button_audit_button_posXpath = '//*[contains(@class,"icon-a-Adminlogs")]'
url_ObjectDetailPage_auditLogsDrawer_firstRowLog_checkBox_posXpath = '(//div[@class="LocalationDraswer lstsub right-show-edit right-show-edit-other"]//table[@class="el-table__body"]//span[@class="el-checkbox__input"])[1]'  # Audit Logs 侧滑页第一条日志CheckBox Xpath
url_ObjectDetailPage_auditLogsDrawer_compareButton_posXpath = '//div[@class="LocalationDraswer lstsub right-show-edit right-show-edit-other"]//button[contains(@id,"test-compare-_")]'  # Audit Logs 侧滑页Compare 按钮Xpath
url_ObjectDetailPage_auditLogsDrawer_compareDrawer_operationText_posXpath = '//div[contains(text(),"Operation")]/following-sibling::div'  # Audit Logs 侧滑页点击Compare后的 operation text Xpath
ObjectDetailPage_audit_log_compare_version_posXpath = "//div[@class='compare-code-box']//div[text()='Version']/following-sibling::div"
ObjectDetailPage_audit_log_compare_id_posXpath = '//div[contains(text(),"Target ID")]/following-sibling::div'
ObjectDetailPage_audit_log_compare_type_posXpath = '//div[contains(text(),"Target Type")]/following-sibling::div'
ObjectDetailPage_audit_log_compare_ip_posXpath = '//div[contains(text(),"Source IP")]/following-sibling::div'
ObjectDetailPage_audit_log_compare_time_posXpath = "//div[@class='compare-code-box']//div[text()='Time']/following-sibling::div"
ObjectDetailPage_audit_log_compare_user_posXpath = '//div[contains(text(),"User")]/following-sibling::div'
ObjectDetailPage_audit_log_cancel_posXpath = "//div[@class='paper-right-content']//span[normalize-space(text())='Close']"


mainPage_version_posXpath = "//*[@class='header-user-con']/span[1]" #TSG Version按钮
language_button_posXpath = "//input[@id='anonymousComponent_Home_App_anonymousComponent_language']/.."#快捷切换语言按钮

#导入文件
main_button_import_files_button_posXpath = '//button/span[contains(text(),"Import From File")]'  # 导入文件按钮
main_ObjectPage_Input_path_Import_files_posXpath = '//form/div/div/div/div[1]/input[@type="file"]'
main_ObjectPage_Import_Mobile_Identity_files_OK_Button_posXpath = '//div[not(@style="display: none;")]/div/div/div[2]/div[2]/button[1]/span'  # 导入文件OK
main_Import_files_error_format_posXpath = '//ul/li/div[@class="valid-column import-line"]/span'  # 导入文件格式错误提示语


#搜索框元素
listPage_objectSearch_ip_address_select_Id_posXpath = '//li[@id="1-_FilteredSearch_ElRow_Objects_ip_Home_App_anonymousComponent"]'  # 查询ID
listPage_objectSearch_ip_address_select_Name_posXpath = '//li[@id="2-_FilteredSearch_ElRow_Objects_ip_Home_App_anonymousComponent"]'  # 查询Name
listPage_objectSearch_ip_address_select_Details_posXpath = '//li[@id="6-_FilteredSearch_ElRow_Objects_ip_Home_App_anonymousComponent"]'  # 查询Details
listPage_objectSearch_ip_address_select_subType_posXpath = '//li[@id="3-_FilteredSearch_ElRow_Objects_ip_Home_App_anonymousComponent"]'  # 查询SubType
listPage_objectSearch_ip_address_select_Description_posXpath = '//li[@id="4-_FilteredSearch_ElRow_Objects_ip_Home_App_anonymousComponent"]'  # 查询Description
listPage_objectSearch_ip_address_select_CreateBy_posXpath = '//*[@id="5-_FilteredSearch_ElRow_Objects_ip_Home_App_anonymousComponent"]'  # 查询CreateBy
listPage_objectSearch_ip_address_select_IP_posXpath = "//*[@id='100-_FilteredSearch_ElRow_Objects_ip_Home_App_anonymousComponent']"
listPage_objectSearch_geo_select_IP_posXpath = "//li[@id='100-_FilteredSearch_ElRow_Geography_List_Home_App_anonymousComponent']"
listPage_objectSearch_geo_select_GeoNameID_posXpath = "//li[@id='56-_FilteredSearch_ElRow_Geography_List_Home_App_anonymousComponent']"
listPage_objectSearch_geo_select_CountryAbbreviation_posXpath = "//li[@id='156-_FilteredSearch_ElRow_Geography_List_Home_App_anonymousComponent']"
listPage_objectSearch_geo_select_CountryandRegion_posXpath = "//li[@id='58-_FilteredSearch_ElRow_Geography_List_Home_App_anonymousComponent']"
listPage_objectSearch_geo_select_SuperAdministrativeArea_posXpath = "//li[@id='150-_FilteredSearch_ElRow_Geography_List_Home_App_anonymousComponent']"
listPage_objectSearch_geo_select_AdministrativeArea_posXpath = "//li[@id='59-_FilteredSearch_ElRow_Geography_List_Home_App_anonymousComponent']"
listPage_objectSearch_geo_select_SubAdministrativeArea_posXpath = "//li[@id='151-_FilteredSearch_ElRow_Geography_List_Home_App_anonymousComponent']"

#ip object元素
ipObjectPage_ipType_posId = "IPip"
main_ObjectPage_tips_Name_input_Xpath = '//form/div[1]/div/div[@class="el-form-item__error"]'
main_Import_Mobile_Identity_files_error_type_posXpath = '//div[@class="el-message el-message--error"]/p'  # 错误类型提示语
ip_addressObjectPage_input_Name_posXpath = "//div[@class='biFangName']//input"  # name输入框Xpath
listPage_object_ip_address_createButton_posId = "objectCreate-_OperateBtns_ElRow_Objects_ip_Home_App_anonymousComponent"  # create按钮id
listPage_object_ip_address_editButton_posId = "appEdit-_OperateBtns_ElRow_Objects_ip_Home_App_anonymousComponent"  # edit按钮id
listPage_object_ip_address_delButton_disable_posXpath = '//button[@id="appDel-_OperateBtns_ElRow_Objects_ip_Home_App_anonymousComponent"][@disabled="disabled"]'  # del按钮Xpath置灰
listPage_object_ip_address_delButton_posId = "appDel-_OperateBtns_ElRow_Objects_ip_Home_App_anonymousComponent"  # del按钮id
listPage_object_ip_address_del_yes_Button_posXpath = '//div/div[@aria-label="Tips"]/div[3]/span/button[1]/span'  # del_yes按钮
listPage_object_ip_address_create_ip_address_Button_posId = 'object0-_OperateBtns_ElRow_Objects_ip_Home_App_anonymousComponent'  # 创建IP Address
listPage_object_ip_address_create_ip_address_Group_Button_posId = "object1-_OperateBtns_ElRow_Objects_ip_Home_App_anonymousComponent"  # 创建IP Address_Group
listPage_objectSearch_ip_address_selectLabel_posId = mainPage_ObjectSearch_selectLabel_posId  # 查询框id
ip_address_listPage_first_row_checkBox_posXpath = '(//td[@rowspan="1"and @colspan="1"]//span[@class="el-checkbox__inner"])[1]'
listPage_object_ip_address_viewButton_posXpath = "//button[@id='appEdit-_OperateBtns_ElRow_Objects_ip_Home_App_anonymousComponent']//p[normalize-space(text()) = 'View']"
ip_addressObjectPage_button_addItem_posXpath = mainPage_ObjectSearch_buttonAddItem_posXpath  # 添加item按钮id
ip_addressObjectPage_addItem_error_tips_posXpath = "//div[@class='object-item-error']/span"  # IP error_format 错误提示
ip_addressObjectPage_button_inputItem_posXpath = '//div[@class="list-container"]//div[@class="IpExpr expr-item"]//div/input'  # 输入item内容
ip_addressObjectPage_radioButton_IP_learning_posId = "IP Learningip_learning"  # IP Learning单选按钮id
ip_addressObjectPage_button_editItem_posXpath = "//i[@class='operate-icon iconfont icon-Edit']"  # object item编辑按钮
ip_addressObjectPage_button_editgroup_posXpath = "//i[@class='row-edit iconfont icon-Edit cursor fontsize18']"  # object group组 item编辑按钮
ip_addressObjectPage_button_ip_text_posXpath = "//div[@class='object-item-box']//div[@class='item-box']//div[@class='el-input el-input--small']/input"  # ip object item文本编辑框
ip_addressObjectPage_button_ip_learing_text_posXpath = "//div[@class='object-item-box']//div[@class='item-box']//div[@class='fqdn-input el-input el-input--small']/input"  # ip_learing object item文本编辑框
ip_addressObjectPage_button_add_itemIP_Save_posXpath = "//i[@class='operate-icon iconfont icon-save check']"  # 保存item按钮
ip_addressObjectPage_button_addItem_first_item_posXpath = "//div[@class='item-box']//span[@class='ip-txt']"  # item 搜索框第一个元素
ip_addressObjectPage_IP_learning_inputItem_posXpath = "//div[@class='IpLearningItemList']//div[@class='edit-row']//input[@class='el-input__inner']"  # IP Learning中Item输入
ip_addressObjectPage_button_Save_Item_posXpath = '//div/i[@class="operate-icon iconfont icon-save check"]'  # 保存item按钮
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
ip_addressObjectPage_button_cancel_posCss = "//button[@id='Cancel-_IpDetail_Home_App_anonymousComponent']/span"  # Cancel按钮
ip_address_Group_sub_Object_addButton_posXpath = "//div[@class='CommonSubObjects']//i[@class='iconfont icon-Create1 cursor']"  # ip_address_Group添加sub Object按钮
ip_address_Group_sub_Object_add_new_Button_posXpath = "//i[@class='iconfont icon-Create1']"  # 新建sub_ip_address按钮
ip_address_Group_sub_Object_add_new_Select_one_Button_posXpath = "//ul[@x-placement='bottom-start']/li[1]"  # 新建选择ip_address按钮
ip_address_Group_sub_Object_edit_subObject_Button_posXpath = "//i[@class='row-edit iconfont icon-Edit cursor fontsize18']"  # 编辑group 下的object 按钮
ip_address_Group_sub_Object_add_new_Select_Group_Button_posXpath = "//ul[@x-placement='bottom-start']/li[2]"  # 新建选择ip_address_Group按钮
ip_address_Group_sub_Object_add_new_one_inputName_posXpath = "(//div[@class='biFangName']//input)[2]"  # new ip_address input Name
ip_address_Group_sub_Object_add_new_add_item_Button_posXpath = "//div[@class='CommonItems']//div[@class='object-item-add']//i[@class='operate-icon iconfont icon-Create1']"  # new ip_address add items
ip_address_Group_sub_Object_add_new_addIP_item_inputName_posXpath = '//div[@class="list-container"]//input'  # new IP Item input
ip_address_ObjectDetailPage_okButton_yes_posXpath = '//div[@class="el-message-box__btns"]//button[contains(@class,"operation-confirm")]'  # 确认弹窗的“Yes”按钮
ip_address_Group_sub_Object_add_new_one_OK1_Button_posXpath = "//button[@id='OK-_IpDetail_VDraswer_EditDraw_IpDetail_Home_App_anonymousComponent']"  # new ip_address CreateOK1
ip_address_Group_sub_Object_add_new_one_OK1_Warning_Yes_Button_posXpath = "//div[@class='el-message-box__btns']//span[normalize-space(text())='Yes']"  # 再次确认创建new ip_address
ip_address_Group_sub_Object_add_new_one_OK1_Warning_Cancel_Button_posXpath = "//div[@class='el-message-box__btns']//span[normalize-space(text())='Cancel']"  # 再次确认取消new ip_address