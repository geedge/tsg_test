# login page 登录页面
loginPage_userName_posName = "username"
loginPage_passwd_posName = "password"
loginPage_signIn_posId = "login"

# main页面
##上导航栏
mainPage_navigationBar_logo_posCss = ".tsg-img-logo"
mainPage_navigationBar_Menu_posXpath = '//div/div[1]/span/button[@data-desc="Menu"]'
#   定位vsys需要新写，勿改
mainPage_navigationBar_Default_Vsys1_posXpath = '//article/div/ul/li[1]/div[2]/ul/li[1]/div'  # Default Vsys1
mainPage_navigationBar_Tvsys3_posXpath = '//article/div/ul/li[1]/div[2]/ul/li[2]/div/div[2]/div/div[1]'   # Tvsys3
mainPage_navigationBar_Mvsys2_Tvsys4_posXpath = '//article/div/ul/li[1]/div[1]/div[2]/div/div[2]' # Mvsys2_Tvsys4
mainPage_navigationBar_Mvsys3_Tvsys5_posXpath = '//article/div/ul/li[2]/div[1]/div[2]/div/div[2]' # Mvsys3_Tvsys5 super_vsys
mainPage_navigationBar_super_Tvsys1_posXpath = '//article/div/ul/li[2]/div[2]/ul/li[2]/div/div[2]/div/div[1]' # super_Tvsys1
mainPage_navigationBar_super_Tvsys3_posXpath = '//article/div/ul/li[1]/div[2]/ul/li[1]/div/div[2]/div' # super_Tvsys3
# 菜单栏================================菜单栏===================================菜单栏================================菜单栏==================================菜单栏========================菜单栏
##菜单栏
mainPage_firstLevelMenu_Policy_posId = "policy"  # 一级菜单Policies
mainPage_secondLevelMenu_Security_posId = "Objects_ProxyInterception"  # 二级菜单Security
mainPage_secondLevelMenu_Statistics_posId = "policy_statistics"  # 二级菜单Statistics
mainPage_secondLevelMenu_Proxy_intercept_posId = "policy_Intercept"  # 二级菜单Proxy_intercept
mainPage_secondLevelMenu_Proxy_Manipulation_posId = "policy_Manipulation"  # 二级菜单Proxy_Manipulation
mainPage_secondLevelMenu_Shaping_posId = "policy_trafficShaping"  # 二级菜单Shaping
mainPage_secondLevelMenu_ServiceChaining_posId = "policy_ServiceChaining"  # 二级菜单Service Chaining

#Policies 查询栏===================Policies 查询栏=====================Policies 查询栏=================Policies 查询栏=======================Policies 查询栏=================Policies 查询栏
##profiles模块查询栏
listPage_policiesSearch_selectLabel_posId = "select-label"   #查询框id
listPage_policiesSearch_buttonSearch_posId = "searchQuery"    #查询按钮id
listPage_policiesSearch_buttonClear_posId = "searchClear"     #清空查询按钮id
#profiles模块列设置
listPage_policiesColumn_columnSetting_posId = "eventfixed"   #列设置按钮

# Security================================Security===================================Security================================Security==================================Security========================Security
# Create element
security_policy_add_condition_button_by_xpath='//span[contains(text(),"Add Condition")]' #Add Condition按钮
security_policy_add_device_button_by_xpath='//div[(normalize-space(text())="Device")]' #选择Device
security_policy_add_button_by_xpath='(//*[@class="MultipleSelect SourceSelect"])[2]'#添加Device
#security_policy_add_apn_by_xpath='//div[(normalize-space(text())="APN")]'#选择apn
security_create_Button_posXpath = '//button[@id="app_create-_OperateBtns_ElRow_Objects_ProxyInterception_Home_App_anonymousComponent"]/span' # 安全创建按钮
security_create_Name_input_frame_PosXpath = '//div/div/div[1]/div[2]/form/div[1]/div/div[1]/div[1]/input'   # 创建输入Name框
security_create_add_source_button_click_PosXpath =  '//div/div/div/div[1]/div[2]/form/div[4]/div/div/div/i' # 创建添加source按钮
security_create_add_tunnel_button_click_PosXpath='(//div[(normalize-space(text())="Tunnel")])[2]' #选择tunnel按钮
security_add_tunnel_button='(//*[@class="iconfont icon-Create1 cursor"])[1]'
security_search_tunnel_frame_click_PosXpath='(//*[@id="object_ip_search"])[2]' #tunnel搜索框
security_first_tunnel_inlist_click_PosXpath='(//*[@class="ellipsis list-popover-click"])[1]'#tunnel列表页的第一个元素
security_first_add_App_Group_right_top_click_PosXpath='//*[@id="tab-group"]'#"+"App,列表页选择App Group
security_first_app_group_inlist_click_PosXpath ='//div/div/div/div[3]/div[1]/div/div[2]/ul/li[1]/div[2]/span/div[2]/div/span'#App Group列表页的第一个元素
security_create_add_source_button_right_click_PosXpath = '//div[2]/div/div[1]/div/div/div/div[2]/div/div/div[1]/div/span[2]/i' # 右划选择框
security_create_add_source_button_select_IMSI_PosXpath = '//div[@id="tab-imsi"]'   # 选择imsi
security_create_add_source_button_select_APN_PosXpath='//*[@id="tab-apn"]'#选择apn
security_create_add_source_button_select_Phone_Number_PosXpath = '//div[@id="tab-phone_number"]' # 选择phone_number
security_create_add_source_button_select_IMEI_PosXpath = '//div[@id="tab-imei"]' # 选择imei
security_create_add_source_button_IMSI_search_frame_PosXpath = '(//*[@id="object_ip_search"])[2]' # IMSI搜索框
security_create_add_source_button_Phone_Number_search_frame_PosXpath = '//div/div/div/div[2]/div/div[1]/div/div/div/div[3]/div[1]/div/div[1]/div[1]/div/div/input' # Phone_number 搜索框
security_create_add_source_button_IMEI_search_frame_PosXpath = '//div/div/div/div[2]/div/div[1]/div/div/div/div[3]/div[1]/div/div[1]/div[1]/div/div/input' # IMEI搜索框
security_create_add_source_button_select_first_object_PosXpath ='//*[@class="ellipsis list-popover-click"]' # 选择第一个元素
security_create_ok_click_posXpath = '//button[@id="OK-_SecurityAdd_Home_App_anonymousComponent"]/span' # 点击OK
security_create_Warn_ok_click_posXpath = '//div[@role="dialog"]/div/div[3]/button[2]/span' # Warn OK
# List element
list_security_select_frame_click_posXpath = '//input[@id="select-label"]' # 点击搜索框
list_security_select_frame_Name_click_posXpath = '//li[@id="2-_FilteredSearch_ElRow_Objects_ProxyInterception_Home_App_anonymousComponent"]/span' # 搜索框选择Name
list_security_select_frame_Name_input_posXpath = '//div[@id="profileName"]/div[3]/div/input'  # 输入Name
list_security_select_frame_click_search_posXpath = '//i[@id="searchQuery"]'  # 输入框点击Search
list_security_select_first_element_posXpath = '//table/tbody/tr[1]/td[1]/div/div/div/div[1]/div/label/span[1]/span'  # 选择第一个输入框
# delete element
delete_security_delete_button_posXpath = '//button[@id="appDel-_OperateBtns_ElRow_Objects_ProxyInterception_Home_App_anonymousComponent"]/span/div/div[2]/p[1]' # 点击delete按钮
delete_security_delete_confirm_button_posXpath = '//div/div[3]/span/button[1]/span' # 确认删除按钮
# Security list page 列表页
listPage_security_create_button_posId = "app_create-_OperateBtns_ElRow_Objects_ProxyInterception_Home_App_anonymousComponent"  # Security创建按钮
listPage_security_delete_button_posId = "appDel-_OperateBtns_ElRow_Objects_ProxyInterception_Home_App_anonymousComponent"  # Security删除按钮
listPage_securitySearch_selectLabel_posId = listPage_policiesSearch_selectLabel_posId  # 查询框id
listPage_securitySearch_buttonSearch_posId = listPage_policiesSearch_buttonSearch_posId  # 查询按钮id
listPage_securitySearch_dropDown_item_posXpath = "//div[contains(@class,'el-scrollbar')]//span[normalize-space(text())='{replaceName}']"   #下拉菜单定位
listPage_securitySearch_input_itemContent_posXpath = "//div[contains(@class,'ListItem')]//span[normalize-space(text())='{replaceName}']/ancestor::div[contains(@class,'ListItem')]//input"   #输入item的值，replaceName替换实际查询值
listPage_securitySearch_dropDown_typeItem_posXpath = "//div[contains(@class,'select-popper')]//span[normalize-space(text())='{replaceName}']"     #查询中type的下拉item定位,replaceName替换实际查询值
listPage_securityTable_tableTbody_posXpath = "//*[@id='ly-table1-listcontent']/div/div[3]/table/tbody"   #列表tabel body  xpath
listPage_securityTable_tableHeader_posXpath = "//div[contains(@class,'ly-table1')]//table[@class='el-table__header']//thead"    #列表table 表头xpath
#listPage->Tips dialog  列表页 tips对话框
listPage_dialogTips_security_button_yes_posCss = "body>.el-dialog__wrapper .delComponents-ok span"   #删除提示的Tips的yes按钮
listPage_dialogTips_security_button_no_posCss = "body>.el-dialog__wrapper .delComponents-close span"   #删除提示的Tips的close按钮
# create security 和edit security 新增和编辑页
security_create_action_shunt_label_posId = "shuntshunt"
security_create_action_allow_label_posId = "allowallow"
security_create_action_deny_label_posId = "denydeny"
security_create_add_source_IPAddress_button_click_posXpath = "//div[@class='MultipleSelect SourceModuleSelect']//i[@class='iconfont icon-Create1 cursor']"  #添加Source IPAddress按钮
security_create_add_application_button_click_posXpath = "//div[@class='MultipleSelect AppSelect']"  #添加Application按钮
security_create_add_application_select_input_posXpath = "//div[@class='AppList list-box']//div[@class='CommonListDetail list-detail']//input[@id='object_ip_search']"  #Application搜索框
security_button_warningSaveYes_posCss = ".el-message-box__btns .el-button--primary span"    #提示保存按钮警告框OK按钮
security_button_warningSaveCancel_posCss = ".el-message-box__btns .operation-cancel span"     #提示保存警告框Cancel按钮
security_button_oK_posId = "OK-_SecurityAdd_Home_App_anonymousComponent"     #OK按钮
security_button_cancel_posId = "Cancle-_SecurityAdd_Home_App_anonymousComponent"      #Cancel按钮
# Action Parameters
security_deny_overrride_label_posXpath = "//span[text()='Override Application Deny Action']" #Override Application Deny Action复选框
security_deny_subAction_drop_posXpath = "//span[contains(text(),'Drop')]"   #Sub Action-Drop
security_deny_subAction_redirect_posXpath = "//span[contains(text(),'Redirect')]"   #Sub Action-Redirect
security_deny_subAction_rateLimit_posXpath = "//span[contains(text(),'Rate Limit')]"   #Sub Action-Rate Limit
security_deny_subAction_tamper_posXpath = "//span[contains(text(),'Tamper')]"   #Sub Action-Tamper
security_deny_redirect_queryType_A_posId = "dns_qtype_radio00"  #Query Type -A
security_deny_redirect_queryType_AAAA_posId = "dns_qtype_radio01"   #Query Type -AAAA
security_deny_redirect_answerType_dropDown_posXpath = "//label[text()='Answer Type']/parent::div//span[@class='el-input__suffix']"  #Answer Type下拉按钮
security_deny_redirect_answerType_CNAME_posXpath = "//ul[@class='el-scrollbar__view el-select-dropdown__list']//span[text()='CNAME']" # Answer Type -CNAME
security_deny_redirect_answerType_A_posXpath = "//ul[@class='el-scrollbar__view el-select-dropdown__list']//span[text()='A']" # Answer Type -A
security_deny_redirect_answerType_AAAA_posXpath = "//ul[@class='el-scrollbar__view el-select-dropdown__list']//span[text()='AAAA']" # Answer Type -AAAA
security_deny_redirect_answer_dropDown_posXpath = "//input[@id='blockselect00']/parent::div//span[@class='el-input__suffix']"  #Answer下拉按钮
security_deny_redirect_answer_TEXT_posXpath = "//ul[@class='el-scrollbar__view el-select-dropdown__list']//span[text()='TEXT']"  #Answer -TEXT
security_deny_redirect_answer_Profile_posXpath = "//ul[@class='el-scrollbar__view el-select-dropdown__list']//span[text()='Profile']"  #Answer  -Profile
security_deny_redirect_answer_Profile_dropDown_posXpath = "//input[@id='html_profile']/parent::div//span[@class='el-input__suffix']"  #Answer  -Profile 文件选择下拉按钮
security_deny_redirect_answer_Profile_search_posId = "filedata_profileName"   #Answer  -Profile 文件搜索框
security_deny_redirect_TTL_input_posId = "ttl00"  # TTL

# intercept================================intercept===================================intercept================================intercept==================================intercept========================intercept
# Create element
intercept_create_Button_posXpath = '//button[@id="app_create-_OperateBtns_ElRow_policy_Intercept_Home_App_anonymousComponent"]/span/div/div[2]/p[1]' # 代理拦截创建按钮
intercept_create_Name_input_frame_PosXpath = '//div/div/div[1]/div[2]/form/div[1]/div/div[1]/div[1]/input'   # 创建输入Name框
intercept_create_add_source_button_click_PosXpath =  '//div/div/div/div[1]/div[2]/form/div[3]/div/div/div/i' # 创建添加source按钮
intercept_create_add_source_button_right_click_PosXpath = '//div[2]/div/div[1]/div/div/div/div[2]/div/div/div[1]/div/span[2]/i' # 右划选择框
intercept_create_add_source_button_select_IMSI_PosXpath = '//div[@id="tab-imsi"]'   # 选择imsi
intercept_create_add_source_button_select_Phone_Number_PosXpath = '//div[@id="tab-phone_number"]' # 选择phone_number
intercept_create_add_source_button_select_IMEI_PosXpath = '//div[@id="tab-imei"]' # 选择imei
intercept_create_add_source_button_IMSI_search_frame_PosXpath = '//div/div/div/div[2]/div/div[1]/div/div/div/div[3]/div[1]/div/div[1]/div[1]/div/div/input' # IMSI搜索框
intercept_create_add_source_button_Phone_Number_search_frame_PosXpath = '//div/div/div/div[2]/div/div[1]/div/div/div/div[3]/div[1]/div/div[1]/div[1]/div/div/input' # Phone_number 搜索框
intercept_create_add_source_button_IMEI_search_frame_PosXpath = '//div/div/div/div[2]/div/div[1]/div/div/div/div[3]/div[1]/div/div[1]/div[1]/div/div/input' # IMEI搜索框
intercept_create_add_source_button_select_first_object_PosXpath ="//div/div[1]/div/div/div/div[3]/div[1]/div/div[2]/div/ul/li[1]/div[2]/span/div/div/span"  # 选择第一个元素
intercept_create_ok_click_posXpath = '//button[@id="OK-_policy_Intercept_edit_Home_App_anonymousComponent"]/span' # 点击OK
intercept_create_add_application__posXpath = '//div/div/div/div[1]/div[2]/form/div[5]/div/div/div/i' # 选择添加application
intercept_create_application_select_first_http_posXpath = '//div/div/div[2]/div[1]/div/div/div/ul/li[1]/div[2]/span/div/div/span' # application 选择第一个http
intercept_create_Warn_ok_click_posXpath = '//div[@role="dialog"]/div/div[3]/button[2]/span' # Warn OK
# List element
list_intercept_assert_nodata_posXpath = '//div[@id="intercept_table"]/div[3]/div/span' # 删除断言No data
list_intercept_select_frame_click_posXpath = '//input[@id="select-label"]' # 点击搜索框
list_intercept_select_frame_Name_click_posXpath = '//li[@id="2-_FilteredSearch_ElRow_policy_Intercept_Home_App_anonymousComponent"]/span' # 搜索框选择Name
list_intercept_select_frame_Name_input_posXpath = '//div[@id="profileName"]/div[3]/div/input'  # 输入Name
list_intercept_select_frame_click_search_posXpath = '//i[@id="searchQuery"]'  # 输入框点击Search
list_intercept_select_first_element_posXpath = '//table/tbody/tr[1]/td[1]/div/div/div/div[1]/div/label/span[1]/span'  # 选择第一个输入框
# delete element
delete_intercept_delete_button_posXpath = '//button[@id="appDel-_OperateBtns_ElRow_policy_Intercept_Home_App_anonymousComponent"]/span/div/div[2]/p[1]' # 点击delete按钮
delete_intercept_delete_confirm_button_posXpath = '//div/div[3]/span/button[1]/span' # 确认删除按钮
# intercept list page 列表页
listPage_intercept_create_button_posId = "app_create-_OperateBtns_ElRow_policy_Intercept_Home_App_anonymousComponent"  # intercept创建按钮
listPage_intercept_delete_button_posId = "appDel-_OperateBtns_ElRow_policy_Intercept_Home_App_anonymousComponent"  # intercept删除按钮
listPage_interceptSearch_selectLabel_posId = listPage_policiesSearch_selectLabel_posId  # 查询框id
listPage_interceptSearch_buttonSearch_posId = listPage_policiesSearch_buttonSearch_posId  # 查询按钮id
listPage_interceptSearch_dropDown_item_posXpath = "//div[contains(@class,'el-scrollbar')]//span[normalize-space(text())='{replaceName}']"   #下拉菜单定位
listPage_interceptSearch_input_itemContent_posXpath = "//div[contains(@class,'ListItem')]//span[normalize-space(text())='{replaceName}']/ancestor::div[contains(@class,'ListItem')]//input"   #输入item的值，replaceName替换实际查询值
listPage_interceptSearch_dropDown_typeItem_posXpath = "//div[contains(@class,'select-popper')]//span[normalize-space(text())='{replaceName}']"     #查询中type的下拉item定位,replaceName替换实际查询值
listPage_interceptTable_tableTbody_posXpath = "//*[@id='ly-table1-listcontent']/div/div[3]/table/tbody"   #列表tabel body  xpath
listPage_interceptTable_tableHeader_posXpath = "//div[contains(@class,'ly-table1')]//table[@class='el-table__header']//thead"    #列表table 表头xpath
#listPage->Tips dialog  列表页 tips对话框
listPage_dialogTips_intercept_button_yes_posCss = "body>.el-dialog__wrapper .delComponents-ok span"   #删除提示的Tips的yes按钮
listPage_dialogTips_intercept_button_no_posCss = "body>.el-dialog__wrapper .delComponents-close span"   #删除提示的Tips的close按钮
# create intercept 和edit intercept 新增和编辑页
intercept_create_action_intercept_label_posId = "interceptintercept"
intercept_create_action_nointercept_label_posId = "no_interceptno_intercept"
intercept_create_add_IPAddress_button_click_posXpath= "//div[@class='MultipleSelect SourceModuleSelect']//i[@class='iconfont icon-Create1 cursor']"   # 添加Source IPAddress按钮
intercept_create_add_application_button_click_posXpath = "//div[@class='MultipleSelect AppSelect']"  #添加Application按钮
intercept_create_add_application_select_input_posXpath = "//div[@class='AppList list-box']//div[@class='CommonListDetail list-detail']//input[@id='object_ip_search']"  #Application搜索框
intercept_button_warningSaveYes_posCss = ".el-message-box__btns .el-button--primary span"    #提示保存按钮警告框OK按钮
intercept_button_warningSaveCancel_posCss = ".el-message-box__btns .operation-cancel span"     #提示保存警告框Cancel按钮
intercept_button_oK_posId = "OK-_policy_Intercept_edit_Home_App_anonymousComponent"     #OK按钮
intercept_button_cancel_posId = "Cancle-_policy_Intercept_edit_Home_App_anonymousComponent"      #Cancel按钮
# Action Parameters
intercept_ssl_trustedKeyring_dropDown_posXpath = "//label[text()='For trusted servers']/parent::div//span[@class='el-input__suffix']"   #For trusted servers下拉按钮
intercept_ssl_trustedKeyring_search_posXpath = "(//input[@id='object_ip_search'])[6]"   #For trusted servers搜索框
intercept_ssl_untrustedKeyring_dropDown_posXpath = "//label[text()='For untrusted servers']/parent::div//span[@class='el-input__suffix']"   #For untrusted servers下拉按钮
intercept_ssl_untrustedKeyring_search_posXpath = "(//input[@id='object_ip_search'])[6]"  #For untrusted servers搜素框
intercept_ssl_mirrorDecryption_button_posXpath = "//label[text()='Mirror Decrypted Traffic']/parent::div//div[contains(@class,'el-switch')]"  #Mirror Decrypted Traffic开关按钮
intercept_ssl_addVLANID_button_posXpath = "//label[text()='Add VLAN ID']/parent::div//div[contains(@class,'el-switch')]"  #Add VLAN ID开关按钮
intercept_ssl_trafficMirror_dropDown_posXpath = "//label[text()='Traffic Mirror Profile']/parent::div//span[@class='el-input__suffix']"  #Traffic Mirror Profile下拉按钮
intercept_ssl_trafficMirror_search_posXpath = "(//input[@id='object_ip_search'])[6]"  #Traffic Mirror Profile搜素框
intercept_ssl_decryptionProfile_dropDown_posXpath = "//label[text()='Decryption Profile']/parent::div//span[@class='el-input__suffix']"  #Decryption Profile下拉按钮
intercept_ssl_decryptionProfile_search_posXpath = "(//input[@id='object_ip_search'])[6]"  #Decryption Profile搜素框
intercept_ssl_tcpProxyProfile_dropDown_posXpath = "//label[text()='TCP Proxy Profile']/parent::div//span[@class='el-input__suffix']"  #TCP Proxy Profile下拉按钮
intercept_ssl_tcpProxyProfile_search_posXpath = "(//input[@id='object_ip_search'])[6]"  #TCP Proxy Profile搜素框

# Proxy Manipulation================================Proxy Manipulation===================================Proxy Manipulation================================Proxy Manipulation==================================Proxy Manipulation========================Proxy Manipulation
#Proxy Manipulation list page  列表页
listPage_manipulation_create_button_posId = "app_create-_OperateBtns_ElRow_policy_Manipulation_Home_App_anonymousComponent"  # Manipulation创建按钮
listPage_manipulation_delete_button_posId = "appDel-_OperateBtns_ElRow_policy_Manipulation_Home_App_anonymousComponent"   # Manipulation删除按钮
listPage_manipulationSearch_selectLabel_posId = listPage_policiesSearch_selectLabel_posId  # 查询框id
listPage_manipulationSearch_buttonSearch_posId = listPage_policiesSearch_buttonSearch_posId  # 查询按钮id
listPage_manipulationSearch_dropDown_item_posXpath = "//div[contains(@class,'el-scrollbar')]//span[normalize-space(text())='{replaceName}']"   #下拉菜单定位
listPage_manipulationSearch_input_itemContent_posXpath = "//div[contains(@class,'ListItem')]//span[normalize-space(text())='{replaceName}']/ancestor::div[contains(@class,'ListItem')]//input"   #输入item的值，replaceName替换实际查询值
listPage_manipulationSearch_dropDown_typeItem_posXpath = "//div[contains(@class,'select-popper')]//span[normalize-space(text())='{replaceName}']"     #查询中type的下拉item定位,replaceName替换实际查询值
listPage_manipulationTable_tableTbody_posXpath = "//*[@id='ly-table1-listcontent']/div/div[3]/table/tbody"   #列表tabel body  xpath
listPage_manipulationTable_tableHeader_posXpath = "//div[contains(@class,'ly-table1')]//table[@class='el-table__header']//thead"    #列表table 表头xpath
#listPage->Tips dialog  列表页 tips对话框
listPage_dialogTips_manipulation_button_yes_posCss = "body>.el-dialog__wrapper .delComponents-ok span"   #删除提示的Tips的yes按钮
listPage_dialogTips_manipulation_button_no_posCss = "body>.el-dialog__wrapper .delComponents-close span"   #删除提示的Tips的close按钮
#Create Proxy Manipulation 和 Edit Proxy Manipulation   新增和编辑页
manipulation_input_Name_posXpath = "//div[@class='biFangName']//input"   # 创建输入Name框
manipulation_action_label_Allow_posId = "allowallow"
manipulation_action_label_Deny_posId = "denydeny"
manipulation_action_label_Monitor_posId = "monitormonitor"
manipulation_action_label_Redirect_posId = "redirectredirect"
manipulation_action_label_Replace_posId = "replacereplace"
manipulation_action_label_Hijack_posId = "hijackhijack"
manipulation_action_label_Insert_posId = "insertinsert"
manipulation_action_label_EditElement_posId = "edit_elementedit_element"
manipulation_action_label_RunScript_posId = "run_scriptrun_script"
manipulation_source_add_posXpath = "//div[@class='MultipleSelect SourceSelect']//i[contains(@class, 'icon-Create1')]"  # 添加source按钮
manipulation_button_warningSaveYes_posCss = ".el-message-box__btns .el-button--primary span"    #提示保存按钮警告框OK按钮
manipulation_button_warningSaveCancel_posCss = ".el-message-box__btns .operation-cancel span"     #提示保存警告框Cancel按钮
manipulation_button_oK_posId = "OK-_Edit_Home_App_anonymousComponent"     #OK按钮
manipulation_button_cancel_posId = "Cancle-_Edit_Home_App_anonymousComponent"      #Cancel按钮
#Filter
manipulation_add_condition_button_posXpath = "//div[@class='MultipleSelect ConditionModuleSelect']/button"    #Add Condition添加按钮
manipulation_http_filter_URL_select_posXpath = "//li/div/div[contains(text(),'URL')]"
manipulation_http_filter_Host_select_posXpath = "//li/div/div[contains(text(),'Host')]"
manipulation_http_filter_RequestHeader_select_posXpath = "//li/div/div[contains(text(),'Request Header')]"
manipulation_http_filter_ResponseHeader_select_posXpath = "//li/div/div[contains(text(),'Response Header')]"
manipulation_http_filter_URL_add_posXpath = "//p[contains(text(),'URL')]/ancestor::label/parent::div//i[contains(@class,'icon-Create1')]"
#Action Parameters
deny_responseCode_dropDown_item_posCss = ".el-form-item__content > .el-select .el-select__caret"  # Response Code下拉按钮
deny_responseCode_403_posXpath = "//span[text()='403']"
deny_responseCode_404_posXpath = "//span[text()='404']"
deny_responseCode_451_posXpath = "//span[text()='451']"
deny_responseContent_dropDown_item_posCss = ".margin-bottom6 .el-select__caret"  # Response Content下拉按钮
deny_responseContent_TEXT_posXpath = "//span[text()='TEXT']"  # Response Content text类型
deny_responseContent_Profile_posXpath = "//span[text()='Profile']"  # Response Content Profile类型
deny_responseContent_profile_dropDown_item_posXpath = "//div[@class='box-sizing']"  # Response Content-Profile下拉按钮
deny_responseContent_profile_search_posXpath = "//ul/div/div/input"  # Response Content-Profile搜索框
hijack_file_dropDown_item_posCss = ".el-form-item__content > .el-select .el-select__caret"   # hijack file 下拉按钮
hijack_file_profile_search_posXpath = "//ul/div/div/input"  # hijack file 搜索框
insert_file_dropDown_item_posCss = ".el-form-item__content > .el-select .el-select__caret"   # hijack file 下拉按钮
insert_file_profile_search_posXpath = "//ul/div/div/input"  # hijack file 搜索框
