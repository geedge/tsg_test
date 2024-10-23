#login page 登录页面
loginPage_userName_posXpath = "//div[@class='loginTitle']//input[@placeholder='User name']"
loginPage_passwd_posXpath = "//div[@class='loginTitle']//input[@placeholder='Password']"
loginPage_signIn_posXpath = "//div[@class='loginTitle']//button"
loginPage_error_posXpath = "//p[@class='el-message__content']"

#main页面
##上导航栏及语言切换按钮
mainPage_menu_bar_posXpath = "//div[@class='systemMenu']"
#mainPage_navigationBar_logo_posXpath = ".logo"
mainPage_secondLevelMenu_ipAddress_posXpath = "#dashboard .level1-title"
mainPage_navigationBar_logo_posXpath = mainPage_secondLevelMenu_ipAddress_posXpath
mainPage_input_language_posXpath = "//button[@id='header-profile-button']/i"
mainPage_language_change_posXpath = "//button[@id='header-profile-button']/i"
mainPage_language_chinese_posXpath = "//div[@id='fade-menu']//ul[@role='menu']//span[contains(text(), '中文')]"
mainPage_language_russian_posXpath = "//div[@id='fade-menu']//ul[@role='menu']//span[contains(text(), 'Русский')]"
mainPage_language_english_posXpath = "//div[@id='fade-menu']//ul[@role='menu']//span[contains(text(), 'English')]"
mainPage_button_menu_posXpath = "//div[@id='root']//header//div[@class='systemMenu']//button//i"    #menu按钮定位
mainPage_currentPage_vsysName_posXpath = "//div[@class='MuiStack-root mt-[40px] css-1t9fcl0']/div"    # 当前页面中vsys name
mainPage_vsysTree_vsysName_posXpath = "//div[@class='MuiStack-root css-1r1y6jm']//li/div"    # vsys tree中vsys name定位
mainPage_vsysTree_DefaultVsys_posXpath = "//article/div/ul/li[1]/div[2]/ul//div[normalize-space(text())='Vsys1']"
mainPage_vsysTree_Vsys1_posXpath = "//article/div/ul/li[1]/div[2]/ul//div[normalize-space(text())='Vsys10']"
mainPage_vsysTree_Vsys3_posXpath = "//article/div/ul/li[1]/div[2]/ul//div[normalize-space(text())='Vsys3']"
mainPage_vsysTree_Vsys4_posXpath = "//article/div/ul//div[normalize-space(text())='Vsys4']"
mainPage_vsysTree_Vsys5_posXpath = "//article/div/ul//div[normalize-space(text())='Vsys5']"
#菜单栏================================菜单栏===================================菜单栏================================菜单栏==================================菜单栏========================菜单栏
##菜单栏
mainPage_firstLevelMenu_profiles_posName = "Profiles"
mainPage_firstLevelMenu_profiles_posXpath = "//*[normalize-space(text())='Profiles']"  # 一级菜单Profiles
mainPage_leftMenu_posXpath = "//*[normalize-space(text())='{}']" #根据菜单名称文本定位：
mainPage_secondLevelMenu_responsePages_posId = "Proxy_Profiles/Profile_ResponsePages"  # 二级菜单response pages
mainPage_secondLevelMenu_dnsRecords_posId = "Proxy_Profiles/DNS_record_profile"  # 二级菜单dns records
mainPage_secondLevelMenu_trafficMirroringProfiles_posId = '//span[@class="MuiTypography-root MuiTypography-body1 MuiListItemText-primary css-1cxrtde" and text()="Traffic Mirroring Profiles"]'  # 二级菜单traffic mirroring profiles
mainPage_secondLevelMenu_sslDecryptionKeyrings_posId = "Proxy_CertificateManagement/Certificate_Keyrings"  # 二级菜单ssl decryption keyrings
mainPage_secondLevelMenu_sslDecryptionProfiles_posId = "Proxy_Profiles/Profile_DecryptionProfile"  # 二级菜单ssl decryption Profiles
mainPage_secondLevelMenu_trustedCertificateAuthorities_posId = "Proxy_CertificateManagement/Certificate_Authorities"  # 二级菜单 Trusted Certificate Authorities
mainPage_secondLevelMenu_cachedIntermediateCertificates_posId = "Proxy_CertificateManagement/Certificate_Intermediacert"  # 二级菜单 Cached Intermediate Certificates
mainPage_secondLevelMenu_sslFingerprint_posId = "Proxy_CertificateManagement/SSL_Fingerprint"  # 二级菜单SSL Fingerprint
mainPage_secondLevelMenu_tcpProxyProfiles_posId = "Advanced/advanced"  # 二级菜单tcp proxy profiles
mainPage_secondLevelMenu_hijackFiles_posId = "Proxy_Profiles/Profile_HijackFiles"  # 二级菜单hijack files
mainPage_secondLevelMenu_insertScripts_posId = "Proxy_Profiles/Profile_Insert"  # 二级菜单insert scripts
mainPage_secondLevelMenu_tsgProxyScripts_posId = "Proxy_Profiles/runScript"  # 二级菜单tsg proxy scripts
mainPage_secondLevelMenu_vpnAccounts_posId = "Setting_Wannat/VPN_Account"  # 二级菜单vpn accounts
mainPage_secondLevelMenu_wannatTestServers_posId = "Setting_Wannat/Testserver"  # 二级菜单wannat test servers
mainPage_secondLevelMenu_dosDetectionProfiles_posId = "Proxy_Profiles/detectionProfiles"  # 二级菜单dos detection profiles
mainPage_secondLevelMenu_shapingProfiles_posId = "Proxy_Profiles/ShapingProfile"  # 二级菜单shaping profiles
mainPage_secondLevelMenu_serviceFunctionForwarders_posId = "Proxy_Profiles/ServiceFunctionForwarderProfile"  # 二级菜单service functions forwarders
mainPage_secondLevelMenu_serviceFunctions_posId = "Proxy_Profiles/ServiceFunctionProfile"  # 二级菜单service functions
mainPage_secondLevelMenu_statisticsTemplates_posXpath = "//*[normalize-space(text())='Statistics Templates']"  # 二级菜单statistics templates
mainPage_secondLevelMenu_statisticsTemplates_Name = "Statistics Templates"  # 二级菜单statistics templates
mainPage_secondLevelMenu_trafficTemplates_Name = "Traffic Mirroring Profiles"


# Profiles 查询栏===================Profiles 查询栏=====================Profiles 查询栏=================Profiles 查询栏=======================Profiles 查询栏=================Profiles 查询栏
##profiles模块查询栏
mainPage_profileSearch_selectLabel_posId = '//input[@class="MuiAutocomplete-input css-qdyksh"]'  # 查询框id
mainPage_profileSearch_buttonSearch_posId = '//div[@class="flex"]/button' # 查询按钮id
mainPage_profileSearch_selectLabel_posXpath = "//input[contains(@class,'MuiAutocomplete-input')]" #"select-label"  # 查询框id
mainPage_profileSearch_buttonSearch_posXpath = "//*[@class='MuiButtonBase-root MuiButton-root MuiButton-text MuiButton-textPrimary MuiButton-sizeSmall MuiButton-textSizeSmall MuiButton-colorPrimary MuiButton-root MuiButton-text MuiButton-textPrimary MuiButton-sizeSmall MuiButton-textSizeSmall MuiButton-colorPrimary css-1afa66w']"#"searchQuery"  # 查询按钮id
mainPage_profileSearch_buttonClear_posId = "searchClear"  # 清空查询按钮id
# profiles模块列设置
mainPage_profileColumn_columnSetting_posId = "eventfixed"  # 列设置按钮
# profiles模块页面底部all、页面跳转设置
mainPage_profileBottomPage_button_allSelect_posXpath = "//div[@class='flex flex-row flex-wrap justify-start items-center pl-[18px] mt-[20px]']//input[contains(@class,'MuiCheckbox-input')]" #"//div[@class='page-box-containcheck']//label[contains(@class, 'allCheckbox')]/span/span"  # 底部页面设置中ALl选择按钮
# profiles模块引用侧滑
listPage_profileRightReferenceDrawer_referencedItems = "//div[@class='ReachTest']//div[@class='right-menu-content']//div[contains(@class, 'policy-item')]"  # 引用侧滑中被引用对象定位
# profiles编辑对象页面
profilePage_content = "//*[@id='router-view-container']"  # profile对象内容编辑页面
profilePage_alert_topInfo_Xpath = "//*[@role='alert']"  # 顶部提示信息alert框


# 全局Leave this page?确认弹窗
# Leave this page?确认弹窗元素
leave_this_page_elem_Xpath = "//*[normalize-space(text())='Leave this page?']"
# Leave this page?确认弹窗的确认按钮
leave_this_page_ok_elem_Xpath = '//div[@class="el-message-box tsg-message"]//button[contains(@class,"operation-confirm-Leave")]'


# Profiles DNS Records===================Profiles DNS Records====================Profiles DNS Records=================Profiles DNS Records=======================Profiles DNS Records=================Profiles DNS Records
# DNS Records list page  列表页
listPage_profile_dnsRecords_createButton_posId = "app_create-_OperateBtns_ElRow_DNSRecordProfile_Home_App_anonymousComponent"  # create按钮id
listPage_profile_dnsRecords_editButton_posId = "appEdit-_OperateBtns_ElRow_DNSRecordProfile_Home_App_anonymousComponent"  # edit按钮id
listPage_profile_dnsRecords_delButton_posId = "appDel-_OperateBtns_ElRow_DNSRecordProfile_Home_App_anonymousComponent"  # del按钮id
listPage_profile_dnsRecords_linkButton_posId = "btnCopy-_OperateBtns_ElRow_DNSRecordProfile_Home_App_anonymousComponent"  # link按钮id
listPage_profileColumn_dnsRecords_button_columnAll_posXpath = "//div[@class='ly-eventfixed']//span[text()='All']/parent::label"  # 列选择All按钮
listPage_profileColumn_dnsRecords_button_cancel_posId = "dropColcancel-_ElementSet_DNSRecordProfile_Home_App_anonymousComponent"  # cancel按钮
listPage_profileColumn_dnsRecords_button_ok_posId = "dropColOK-_ElementSet_DNSRecordProfile_Home_App_anonymousComponent"  # ok按钮
listPage_profileSearch_dnsRecords_selectLabel_posId = mainPage_profileSearch_selectLabel_posXpath  # 查询框id
listPage_profileSearch_dnsRecords_buttonSearch_posId = mainPage_profileSearch_buttonSearch_posXpath  # 查询按钮id
listPage_profileSearch_dnsRecords_buttonClear_posId = mainPage_profileSearch_buttonClear_posId  # 清空查询按钮id
listPage_profileSearch_dnsRecords_dropDown_item_posXpath = "//div[contains(@class, 'el-select-dropdown el-popper select-popper')]//ul[@class='el-scrollbar__view el-select-dropdown__list']/li/span[normalize-space(text())='{replaceName}']"#"//div[contains(@class,'el-scrollbar')]//span[normalize-space(text())='{replaceName}']"  # 下拉菜单定位
listPage_profileSearch_dnsRecords_input_itemContent_posXpath = "//div[contains(@class,'ListItem')]//span[normalize-space(text())='{replaceName}']/ancestor::div[contains(@class,'ListItem')]//input"  # 输入item的值，replaceName替换实际查询值
listPage_profileSearch_dnsRecords_dropDown_typeItem_posXpath = "//div[contains(@class,'select-popper')]//span[normalize-space(text())='{replaceName}']"  # 查询中type的下拉item定位,replaceName替换实际查询值
listPage_profilTable_dnsRecords_tableTbody_posXpath = "//div[@class='MuiDataGrid-virtualScrollerRenderZone css-1inm7gi']"#//div[contains(@class,'ly-table1')]//tbody"  # 列表tabel body  xpath
listPage_profilTable_dnsRecords_tableHeader_posXpath = "//div[contains(@class,'ly-table1')]//table[@class='el-table__header']//thead//tr"  # 列表table 表头xpath
# listPage->Tips dialog  列表页 tips对话框
listPage_dialogTips_dnsRecords_button_yes_posXpath = 'ogActions-root flex !justify-center items-center MuiDialogActions-spacing css-vplbg4"]/button[1]'  # 删除提示的Tips的yes按钮
listPage_dialogTips_dnsRecords_button_no_posXpath = "//body/*[@class='el-dialog__wrapper']//*[contains(@class, 'delComponents-close')]//span"  # 删除提示的Tips的close按钮
# listPage-> Link提示对话框
listPage_linkTips_dnsRecords_input_clusterSelect_posXpath = "//*[@id='clusterId']/parent::*//span[@class='el-input__suffix']"  # cluster 下拉选择按钮
listPage_linkTips_dnsRecords_dropitem_clusterDrop_posXpath = "//body/div[contains(@class, 'el-select-dropdown')]//li//span[normalize-space(text())='{replaceName}']"  # cluster 下拉列表 选择按钮
listPage_linkTips_dnsRecords_input_vsysSelect_posXpath = "//*[@id='clusterVsysId']/parent::*//span[@class='el-input__suffix']"  # cluster 下拉选择按钮
listPage_linkTips_dnsRecords_dropitem_vsysSelect_posXpath = "//body/div[contains(@class, 'el-select-dropdown')]//li//span[normalize-space(text())='{replaceName}']"  # vsys id 下拉列表 选择按钮
listPage_linkTips_dnsRecords_button_save_posXpath = "//*[@id='clusterSave-_ClusterTable_ElDialog_copyComponents_DNSRecordProfile_Home_App_anonymousComponent']/i"  # 选择cluster后，save行 按钮 xpath
listPage_linkTips_dnsRecords_button_add_posXpath = "//*[@id='temporary_form-_ClusterTable_ElDialog_copyComponents_DNSRecordProfile_Home_App_anonymousComponent']/i"    # 添加 按钮 xpath
listPage_linkTips_dnsRecords_button_OK_posXpath = "//*[@id='copyOk-_copyComponents_DNSRecordProfile_Home_App_anonymousComponent']/span"    # OK 按钮 xpath
# Create DNS Record Profile 和 Edit DNS Record Profile   新增和编辑页
dnsRecordsProfilePage_headerTitle_posXpath = "//div[@class='v-panel-content']//div[@class='panel-header']"   # 页面头部名称 xpath
dnsRecordsProfilePage_input_Name_posId = "DNSRecordPrfileadd_Home_App_anonymousComponent_objectAdd_name"  # name输入框id
dnsRecordsProfilePage_radioButton_typeA_posId = "objectAdd_ip0-_DNSRecordPrfileadd_Home_App_anonymousComponent"  # A单选按钮id,
dnsRecordsProfilePage_radioButton_typeAAAA_posId = "objectAdd_ip1-_DNSRecordPrfileadd_Home_App_anonymousComponent"  # AAAA单选按钮id
dnsRecordsProfilePage_radioButton_typeCNAME_posId = "objectAdd_ip2-_DNSRecordPrfileadd_Home_App_anonymousComponent"  # CNAME单选按钮id
dnsRecordsProfilePage_input_searchFor_posXpath = "//*[@id='object_ip_search']"  # search for 输入框id  Xpath定位
dnsRecordsProfilePage_button_addItem_posId = "temporary_form"  # 添加item按钮id
dnsRecordsProfilePage_input_addItem_posXpath = "//div[contains(@class, 'item-input')]//input[contains(@class, 'el-input__inner')]"
dnsRecordsProfilePage_button_saveItemByIndex_posXpath = "editForm{replaceName}-_DNSRecordPrfileadd_Home_App_anonymousComponent"
dnsRecordsProfilePage_Values_divItem_posXpath = "//div[@class='list-container']/div/div"  # Values列表中每一个item的div容器定位 xpath
dnsRecordsProfilePage_input_inputItemName_posXpath = "//span[normalize-space(text())='replaceName' and contains(@class,'content-show')]/ancestor::div[@class='item-row']//input[@class='el-input__inner']"  # item的输入框xpath, replaceNamew为替换内容
dnsRecordsProfilePage_button_saveItemByName_posXpath = "//span[normalize-space(text())='replaceName' and contains(@class, 'content-show')]/ancestor::div[@class='item-row']//i[contains(@class, 'icon-save')]"  # item的保存xpath, replaceNamew为替换内容
dnsRecordsProfilePage_button_editItemByName_posXpath = "//span[normalize-space(text())='replaceName' and contains(@class,'content-show')]/ancestor::div[@class='item-row']//i[contains(@class, 'icon-Edit')]"  # item的编辑按钮xpath, replaceNamew为替换内容
dnsRecordsProfilePage_button_delItemByName_posXpath = "//span[normalize-space(text())='replaceName' and contains(@class,'content-show')]/ancestor::div[@class='item-row']//i[contains(@class, 'icon-Delete_X')]"  # item的删除按钮， replaceNamew为替换内容
dnsRecordsProfilePage_textArea_Description_posId = "DNSRecordPrfileadd_Home_App_anonymousComponent_objectAdd_description"  # description文本输入区id
dnsRecordsProfilePage_alertContent_posXpath = "//body/div[@role='alert']"  # 页面上不提示信息
dnsRecordsProfilePage_button_warningSaveYes_posCss = ".el-message-box__btns .el-button--primary span"  # 提示保存ok按钮警告框
dnsRecordsProfilePage_button_warningSaveCancel_posCss = ".el-message-box__btns .operation-cancel span"  # 提示保存取消按钮警告框
dnsRecordsProfilePage_button_oK_posCss = "#dnsRecord_ok-_DNSRecordPrfileadd_Home_App_anonymousComponent span"  # OK按钮css
dnsRecordsProfilePage_button_cancel_posCss = "#dnsRecord_cancel-_DNSRecordPrfileadd_Home_App_anonymousComponent span"  # Cancel


# Profiles Response-Pages===================Profiles Response-Pages====================Profiles Response-Pages=================Profiles Response-Pages=======================Profiles Response-Pages=================Profiles Response-Pages
# Response Pages list page  列表页
listPage_profile_responsePages_createButton_posId = "app_create-_OperateBtns_ElRow_Profile_ResponsePages_Home_App_anonymousComponent"  # create按钮id
listPage_profile_responsePages_editButton_posId = "appEdit-_OperateBtns_ElRow_Profile_ResponsePages_Home_App_anonymousComponent"  # edit按钮id
listPage_profile_responsePages_delButton_posId = "appDel-_OperateBtns_ElRow_Profile_ResponsePages_Home_App_anonymousComponent"  # del按钮id
listPage_profile_responsePages_linkButton_posId = "btnCopy-_OperateBtns_ElRow_Profile_ResponsePages_Home_App_anonymousComponent"  # link按钮id
listPage_profileColumn_responsePages_button_columnAll_posXpath = "//div[@class='ly-eventfixed']//span[text()='All']/parent::label"  # 列选择All按钮
listPage_profileColumn_responsePages_button_cancel_posId = "dropColcancel-_ElementSet_Profile_ResponsePages_Home_App_anonymousComponent"  # cancel按钮
listPage_profileColumn_responsePages_button_ok_posId = "dropColOK-_ElementSet_Profile_ResponsePages_Home_App_anonymousComponent"  # ok按钮
listPage_profileSearch_responsePages_selectLabel_posId = mainPage_profileSearch_selectLabel_posXpath  # 查询框id    定位形式一样
listPage_profileSearch_responsePages_buttonSearch_posId = mainPage_profileSearch_buttonSearch_posXpath  # 查询按钮id       定位形式一样
listPage_profileSearch_responsePages_buttonClear_posId = mainPage_profileSearch_buttonClear_posId  # 清空查询按钮id    定位形式一样
listPage_profileSearch_responsePages_dropDown_item_posXpath = listPage_profileSearch_dnsRecords_dropDown_item_posXpath  # 下拉菜单定位   定位形式一样
listPage_profileSearch_responsePages_input_itemContent_posXpath = listPage_profileSearch_dnsRecords_input_itemContent_posXpath  # 输入item的值，replaceName替换实际查询值    定位形式一样
listPage_profilTable_responsePages_tableTbody_posXpath = listPage_profilTable_dnsRecords_tableTbody_posXpath  # 列表tabel body  xpath   定位形式一样
listPage_profilTable_responsePages_tableHeader_posXpath = listPage_profilTable_dnsRecords_tableHeader_posXpath  # 列表table 表头xpath   定位形式一样
# listPage->Tips dialog  列表页 tips对话框
listPage_dialogTips_responsePages_button_yes_posXpath = listPage_dialogTips_dnsRecords_button_yes_posXpath  # 删除提示的Tips的yes按钮
listPage_dialogTips_responsePages_button_no_posXpath = listPage_dialogTips_dnsRecords_button_no_posXpath  # 删除提示的Tips的close按钮
# listPage-> Link提示对话框
listPage_linkTips_responsePages_button_save_posXpath = "//*[@id='clusterSave-_ClusterTable_ElDialog_copyComponents_Profile_ResponsePages_Home_App_anonymousComponent']/i"  # 选择cluster后，save行 按钮 xpath
listPage_linkTips_responsePages_button_add_posXpath = "//*[@id='temporary_form-_ClusterTable_ElDialog_copyComponents_Profile_ResponsePages_Home_App_anonymousComponent']/i"    # 添加 按钮 xpath
listPage_linkTips_responsePages_button_OK_posXpath = "//*[@id='copyOk-_copyComponents_Profile_ResponsePages_Home_App_anonymousComponent']/span"    # OK 按钮 xpath
# Create Response Page 和 Edit Response Page   新增和编辑页
responsePage_headerTitle_posXpath = dnsRecordsProfilePage_headerTitle_posXpath   # 页面头部名称 xpath
responsePage_input_Name_posId = "responsepages_profileName"  # name输入框id
responsePage_input_file_posXpath = "//*[@id='responseAddUpload']/parent::*//input"  # File上次输入按钮
responsePage_button_warningSaveYes_posCss = dnsRecordsProfilePage_button_warningSaveYes_posCss  # 提示保存按钮警告框OK按钮
responsePage_button_warningSaveCancel_posCss = dnsRecordsProfilePage_button_warningSaveCancel_posCss  # 提示保存警告框Cancel按钮
responsePage_button_oK_posCss = "#responseAddOk1-_interceptionadd_Home_App_anonymousComponent span"  # OK按钮css
responsePage_button_cancel_posCss = "#responseAddCancel1-_interceptionadd_Home_App_anonymousComponent span"  # Cancel按钮


# Profiles traffic mirroring profiles===================Profiles traffic mirroring profiles====================Profiles traffic mirroring profiles=================Profiles traffic mirroring profiles=======================Profiles traffic mirroring profiles=================Profiles traffic mirroring profiles
# listPage->traffic mirroring profiles list page  列表页
listPage_profile_trafficMirroringProfiles_createButton_posXpath = "app_create-_OperateBtns_ElRow_Profile_TrafficMirrorProfiles_Home_App_anonymousComponent"  # create按钮id
listPage_profile_trafficMirroringProfiles_editButton_posId = "appEdit-_OperateBtns_ElRow_Profile_TrafficMirrorProfiles_Home_App_anonymousComponent"  # edit按钮id
listPage_profile_trafficMirroringProfiles_delButton_posId = "appDel-_OperateBtns_ElRow_Profile_TrafficMirrorProfiles_Home_App_anonymousComponent"  # del按钮id
listPage_profile_trafficMirroringProfiles_linkButton_posId = "btnCopy-_OperateBtns_ElRow_Profile_TrafficMirrorProfiles_Home_App_anonymousComponent"  # link按钮id
listPage_profileColumn_trafficMirroringProfiles_button_columnAll_posXpath = '//div[@class="MuiDataGrid-columnsManagementFooter css-1l93brk"]//input'  # 列选择All按钮
listPage_profileColumn_trafficMirroringProfiles_button_cancel_posId = "dropColcancel-_ElementSet_Profile_TrafficMirrorProfiles_Home_App_anonymousComponent"  # cancel按钮
listPage_profileColumn_trafficMirroringProfiles_button_ok_posId = "dropColOK-_ElementSet_Profile_TrafficMirrorProfiles_Home_App_anonymousComponent"  # ok按钮
listPage_profileSearch_trafficMirroringProfiles_selectLabel_posId = mainPage_profileSearch_selectLabel_posXpath  # 查询框id    定位形式一样
listPage_profileSearch_trafficMirroringProfiles_buttonSearch_posId = mainPage_profileSearch_buttonSearch_posXpath  # 查询按钮id       定位形式一样
listPage_profileSearch_trafficMirroringProfiles_buttonClear_posId = mainPage_profileSearch_buttonClear_posId  # 清空查询按钮id    定位形式一样
listPage_profileSearch_trafficMirroringProfiles_dropDown_item_posXpath = listPage_profileSearch_dnsRecords_dropDown_item_posXpath  # 下拉菜单定位   定位形式一样
listPage_profileSearch_trafficMirroringProfiles_input_itemContent_posXpath = listPage_profileSearch_dnsRecords_input_itemContent_posXpath  # 输入item的值，replaceName替换实际查询值    定位形式一样
listPage_profilTable_trafficMirroringProfiles_tableTbody_posXpath = listPage_profilTable_dnsRecords_tableTbody_posXpath  # 列表tabel body  xpath   定位形式一样
listPage_profilTable_trafficMirroringProfiles_tableHeader_posXpath = listPage_profilTable_dnsRecords_tableHeader_posXpath  # 列表table 表头xpath   定位形式一样
# listPage->Tips dialog  列表页 tips对话框
listPage_dialogTips_trafficMirroringProfiles_button_yes_posXpath = listPage_dialogTips_dnsRecords_button_yes_posXpath  # 删除提示的Tips的yes按钮
listPage_dialogTips_trafficMirroringProfiles_button_no_posXpath = listPage_dialogTips_dnsRecords_button_no_posXpath  # 删除提示的Tips的close按钮
# listPage-> Link提示对话框
listPage_linkTips_trafficMirroringProfiles_button_save_posXpath = "//*[@id='clusterSave-_ClusterTable_ElDialog_copyComponents_Profile_TrafficMirrorProfiles_Home_App_anonymousComponent']/i"  # 选择cluster后，save行 按钮 xpath
listPage_linkTips_trafficMirroringProfiles_button_add_posXpath = "//*[@id='temporary_form-_ClusterTable_ElDialog_copyComponents_Profile_TrafficMirrorProfiles_Home_App_anonymousComponent']/i"    # 添加 按钮 xpath
listPage_linkTips_trafficMirroringProfiles_button_OK_posXpath = "//*[@id='copyOk-_copyComponents_Profile_TrafficMirrorProfiles_Home_App_anonymousComponent']/span"    # OK 按钮 xpath
# Create traffic mirroring profile page 和 Edit traffic mirroring profile page   新增和编辑页
trafficMirroringProfiles_headerTitle_posXpath = dnsRecordsProfilePage_headerTitle_posXpath   # 页面头部名称 xpath
trafficMirroringProfiles_input_Name_posXpath = "trafficmirror_profileName"  # name输入框id
trafficMirroringProfiles_button_vlanIdAdd_posXpath = "#addrTypeAdd i"  # vlan id 添加按钮css
trafficMirroringProfiles_input_vlanIdsInput_posXpath = "//form//div[contains(@class, 'addel-form')]//input"  # 所有显示的vlan id的所有input定位，需要通过value二次处理，css
trafficMirroringProfiles_button_warningSaveYes_posCss = dnsRecordsProfilePage_button_warningSaveYes_posCss  # 提示保存按钮警告框OK按钮
trafficMirroringProfiles_button_warningSaveCancel_posCss = dnsRecordsProfilePage_button_warningSaveCancel_posCss  # 提示保存警告框Cancel按钮
trafficMirroringProfiles_button_oK_posXpath = "#trafficMirrorProfile_ok span"  # OK按钮css
trafficMirroringProfiles_button_cancel_posCss = "#trafficMirrorProfile_cancel span"  # Cancel按钮

# Profiles ssl decryption keyrings===================Profiles ssl decryption keyrings====================Profiles ssl decryption keyrings=================Profiles ssl decryption keyrings=======================Profiles ssl decryption keyrings
# listPage->ssl decryption keyrings list page  列表页
listPage_profile_sslDecryptionKeyrings_createButton_posId = "app_create-_OperateBtns_ElRow_Certificate_Keyrings_Home_App_anonymousComponent"  # create按钮id
listPage_profile_sslDecryptionKeyrings_editButton_posId = "appEdit-_OperateBtns_ElRow_Certificate_Keyrings_Home_App_anonymousComponent"  # edit按钮id
listPage_profile_sslDecryptionKeyrings_delButton_posId = "appDel-_OperateBtns_ElRow_Certificate_Keyrings_Home_App_anonymousComponent"  # del按钮id
listPage_profile_sslDecryptionKeyrings_linkButton_posId = "btnCopy-_OperateBtns_ElRow_Certificate_Keyrings_Home_App_anonymousComponent"  # link按钮id
listPage_profileColumn_sslDecryptionKeyrings_button_columnAll_posXpath = "//div[@class='ly-eventfixed']//span[text()='All']/parent::label"  # 列选择All按钮
listPage_profileColumn_sslDecryptionKeyrings_button_cancel_posId = "dropColcancel-_ElementSet_Certificate_Keyrings_Home_App_anonymousComponent"  # cancel按钮
listPage_profileColumn_sslDecryptionKeyrings_button_ok_posId = "dropColOK-_ElementSet_Certificate_Keyrings_Home_App_anonymousComponent"  # ok按钮
listPage_profileSearch_sslDecryptionKeyrings_selectLabel_posId = mainPage_profileSearch_selectLabel_posXpath  # 查询框id    定位形式一样
listPage_profileSearch_sslDecryptionKeyrings_buttonSearch_posId = mainPage_profileSearch_buttonSearch_posXpath  # 查询按钮id       定位形式一样
listPage_profileSearch_sslDecryptionKeyrings_buttonClear_posId = mainPage_profileSearch_buttonClear_posId  # 清空查询按钮id    定位形式一样
listPage_profileSearch_sslDecryptionKeyrings_dropDown_item_posXpath = listPage_profileSearch_dnsRecords_dropDown_item_posXpath  # 下拉菜单定位   定位形式一样
listPage_profileSearch_sslDecryptionKeyrings_input_itemContent_posXpath = listPage_profileSearch_dnsRecords_input_itemContent_posXpath  # 输入item的值，replaceName替换实际查询值    定位形式一样
listPage_profilTable_sslDecryptionKeyrings_tableTbody_posXpath = listPage_profilTable_dnsRecords_tableTbody_posXpath  # 列表tabel body  xpath   定位形式一样
listPage_profilTable_sslDecryptionKeyrings_tableHeader_posXpath = listPage_profilTable_dnsRecords_tableHeader_posXpath  # 列表table 表头xpath   定位形式一样
# listPage->Tips dialog  列表页 tips对话框
listPage_dialogTips_sslDecryptionKeyrings_button_yes_posXpath = listPage_dialogTips_dnsRecords_button_yes_posXpath  # 删除提示的Tips的yes按钮
listPage_dialogTips_sslDecryptionKeyrings_button_no_posXpath = listPage_dialogTips_dnsRecords_button_no_posXpath  # 删除提示的Tips的close按钮
# listPage-> Link提示对话框
listPage_linkTips_sslDecryptionKeyrings_button_save_posXpath = "//*[@id='clusterSave-_ClusterTable_ElDialog_copyComponents_Certificate_Keyrings_Home_App_anonymousComponent']/i"  # 选择cluster后，save行 按钮 xpath
listPage_linkTips_sslDecryptionKeyrings_button_add_posXpath = "//*[@id='temporary_form-_ClusterTable_ElDialog_copyComponents_Certificate_Keyrings_Home_App_anonymousComponent']/i"    # 添加 按钮 xpath
listPage_linkTips_sslDecryptionKeyrings_button_OK_posXpath = "//*[@id='copyOk-_copyComponents_Certificate_Keyrings_Home_App_anonymousComponent']/span"    # OK 按钮 xpath
# Create ssl decryption keyrings page 和 Edit ssl decryption keyrings page   新增和编辑页
sslDecryptionKeyrings_headerTitle_posXpath = dnsRecordsProfilePage_headerTitle_posXpath   # 页面头部名称 xpath
sslDecryptionKeyrings_input_Name_posId = "keyringsadd_name"  # name输入框id
sslDecryptionKeyrings_input_certificateFile_posXpath = "//*[@id='keyringsadd_file']/parent::*//input"  # 证书上传按钮xpath
sslDecryptionKeyrings_radio_privateKeyFile_posId = "private_file"  # 私钥单选按钮
sslDecryptionKeyrings_radio_hsm_posId = "privateHSM"  # 私钥单选按钮
sslDecryptionKeyrings_input_privateKeyFile_posXpath = "//*[@id='keyringsadd_file1']/parent::*//input"  # 证书上传按钮xpath
sslDecryptionKeyrings_input_slotIdHSM_posId = "keyringsadd_slotid"  # slot id输入框定位id
sslDecryptionKeyrings_radio_mirrorServerCertificate_poId = "keyringsadd_default"  # 默认服务端证书时间单选按钮id
sslDecryptionKeyrings_radio_customized_poId = "keyringsadd_customized"  # 自定义时间单选按钮id
sslDecryptionKeyrings_input_customized_poId = "reissueExpiryDate"  # 自定义输入框id
sslDecryptionKeyrings_input_certificateType_poId = "certificateType_input"  # 证书类型选择输入框id
sslDecryptionKeyrings_dropdown_certificateTypeSelect_poId = "certificateType_select{replaceIndex}"  # 证书类型下拉列表item选择，replaceIndex为替换索引
sslDecryptionKeyrings_input_publickKeyAlgorithm_poId = "keyringsadd_publicKeyAlgo"  # 公钥算法选择输入框id
sslDecryptionKeyrings_dropdown_publickKeyAlgorithmSelect_poId = "keyringsadd_publicKeyAlgoSelet{replaceIndex}"  # 公钥算术下拉列表item选择，replaceIndex为替换索引
sslDecryptionKeyrings_input_certificateRevocationList_poId = "keyringsadd_crl"  # Certificate Revocation List输入框id
sslDecryptionKeyrings_input_includeRoot_poXpath = "//*[@id='keyringsadd_includeRoot']/parent::*/span"  # 包含根证书输入框开关选择xpath
sslDecryptionKeyrings_button_warningSaveYes_posCss = dnsRecordsProfilePage_button_warningSaveYes_posCss  # 提示保存按钮警告框OK按钮
sslDecryptionKeyrings_button_warningSaveCancel_posCss = dnsRecordsProfilePage_button_warningSaveCancel_posCss  # 提示保存警告框Cancel按钮
sslDecryptionKeyrings_button_oK_posCss = "#keyringsadd_sub span"  # OK按钮css
sslDecryptionKeyrings_button_cancel_posCss = "#keyringsadd_info span"  # Cancel按钮

# Profiles ssl decryption profiles===================Profiles ssl decryption profiles====================Profiles ssl decryption profiles=================Profiles ssl decryption profiles=======================Profiles ssl decryption profiles
# listPage->ssl decryption profiles list page  列表页
listPage_profile_sslDecryptionProfiles_createButton_posId = "app_create-_OperateBtns_ElRow_Profile_Decryption_Profile_Home_App_anonymousComponent"  # create按钮id
listPage_profile_sslDecryptionProfiles_editButton_posId = "appEdit-_OperateBtns_ElRow_Profile_Decryption_Profile_Home_App_anonymousComponent"  # edit按钮id
listPage_profile_sslDecryptionProfiles_delButton_posId = "appDel-_OperateBtns_ElRow_Profile_Decryption_Profile_Home_App_anonymousComponent"  # del按钮id
listPage_profile_sslDecryptionProfiles_linkButton_posId = "btnCopy-_OperateBtns_ElRow_Profile_Decryption_Profile_Home_App_anonymousComponent"  # link按钮id
listPage_profileColumn_sslDecryptionProfiles_button_columnAll_posXpath = "//div[@class='ly-eventfixed']//span[text()='All']/parent::label"  # 列选择All按钮
listPage_profileColumn_sslDecryptionProfiles_button_cancel_posId = "dropColcancel-_ElementSet_Profile_Decryption_Profile_Home_App_anonymousComponent"  # cancel按钮
listPage_profileColumn_sslDecryptionProfiles_button_ok_posId = "dropColOK-_ElementSet_Profile_Decryption_Profile_Home_App_anonymousComponent"  # ok按钮
listPage_profileSearch_sslDecryptionProfiles_selectLabel_posId = mainPage_profileSearch_selectLabel_posXpath  # 查询框id    定位形式一样
listPage_profileSearch_sslDecryptionProfiles_buttonSearch_posId = mainPage_profileSearch_buttonSearch_posXpath  # 查询按钮id       定位形式一样
listPage_profileSearch_sslDecryptionProfiles_buttonClear_posId = mainPage_profileSearch_buttonClear_posId  # 清空查询按钮id    定位形式一样
listPage_profileSearch_sslDecryptionProfiles_dropDown_item_posXpath = listPage_profileSearch_dnsRecords_dropDown_item_posXpath  # 下拉菜单定位   定位形式一样
listPage_profileSearch_sslDecryptionProfiles_input_itemContent_posXpath = listPage_profileSearch_dnsRecords_input_itemContent_posXpath  # 输入item的值，replaceName替换实际查询值    定位形式一样
listPage_profilTable_sslDecryptionProfiles_tableTbody_posXpath = listPage_profilTable_dnsRecords_tableTbody_posXpath  # 列表tabel body  xpath   定位形式一样
listPage_profilTable_sslDecryptionProfiles_tableHeader_posXpath = listPage_profilTable_dnsRecords_tableHeader_posXpath  # 列表table 表头xpath   定位形式一样
# listPage->Tips dialog  列表页 tips对话框
listPage_dialogTips_sslDecryptionProfiles_button_yes_posXpath = listPage_dialogTips_dnsRecords_button_yes_posXpath  # 删除提示的Tips的yes按钮
listPage_dialogTips_sslDecryptionProfiles_button_no_posXpath = listPage_dialogTips_dnsRecords_button_no_posXpath  # 删除提示的Tips的close按钮
# listPage-> Link提示对话框
listPage_linkTips_sslDecryptionProfiles_button_save_posXpath = "//*[@id='clusterSave-_ClusterTable_ElDialog_copyComponents_Profile_Decryption_Profile_Home_App_anonymousComponent']/i"  # 选择cluster后，save行 按钮 xpath
listPage_linkTips_sslDecryptionProfiles_button_add_posXpath = "//*[@id='temporary_form-_ClusterTable_ElDialog_copyComponents_Profile_Decryption_Profile_Home_App_anonymousComponent']/i"    # 添加 按钮 xpath
listPage_linkTips_sslDecryptionProfiles_button_OK_posXpath = "//*[@id='copyOk-_copyComponents_Profile_Decryption_Profile_Home_App_anonymousComponent']/span"    # OK 按钮 xpath
# Create ssl decryption profiles page 和 Edit ssl decryption profiles page   新增和编辑页
sslDecryptionProfiles_headerTitle_posXpath = dnsRecordsProfilePage_headerTitle_posXpath   # 页面头部名称 xpath
sslDecryptionProfiles_input_Name_posId = "decrytion_profileName"  # name输入框id
sslDecryptionProfiles_switch_commonName_posXpath = "//*[@id='decryption-commenName']/parent::*"  # common name 开关xpath
sslDecryptionProfiles_switch_issuer_posXpath = "//*[@id='decryption-issuer']/parent::*"  # issuer 开关xpath
sslDecryptionProfiles_switch_selfSigned_posXpath = "//*[@id='decryption-signed']/parent::*"  # decryption-signed 开关xpath
sslDecryptionProfiles_switch_expiryDate_posXpath = "//*[@id='decryption-expiration']/parent::*"  # ddecryption-expiration 开关xpath
sslDecryptionProfiles_radio_failClose_posXpath = "//*[@id='decryptionfail-close']"  # decryptionfail-close 点选按钮 Fail-close xpath
sslDecryptionProfiles_radio_passThrough_posXpath = "//*[@id='decryptionpass-through']"  # decryptionpass-through 点选按钮 Pass-through xpath
sslDecryptionProfiles_switch_evCert_posXpath = "//*[@id='decryption-ev_cert']/parent::*"  # ddecryption-expiration 开关xpath
sslDecryptionProfiles_switch_certificateTransparency_posXpath = "//*[@id='decryption-cert_transparency']/parent::*"  # Certificate Transparency 开关xpath
sslDecryptionProfiles_switch_mutualAuthentication_posXpath = "//*[@id='decryption-client_cert_req']/parent::*"  # Mutual Authentication 开关xpath
sslDecryptionProfiles_switch_onProtocolErrors_posXpath = "//*[@id='decryption-protocol_errors']/parent::*"  # On Protocol Errors 开关xpath
sslDecryptionProfiles_switch_certificatePinning_posXpath = "//*[@id='decryption-pinning']/parent::*"  # Certificate Pinning 开关xpath
sslDecryptionProfiles_switch_certificateNotInstalled_posXpath = "//*[@id='decryption-Certificate_Not_Installed']/parent::*"  # Certificate Not Installed 开关xpath
sslDecryptionProfiles_switch_mirrorClientVersions_posXpath = "//*[@id='decryption-radio']/parent::*"  # Mirror Client Versions 开关xpath
sslDecryptionProfiles_input_minVersion_posXpath = "//*[@id='decryption-radio']/ancestor::div[@class='decryption_from']/div[2]//i"  # Min Version 下拉菜单xpath
sslDecryptionProfiles_dropDown_minVersion_posXpath = "//*[@id='pro_min{replaceIndex}']"  # MMin Version 下拉列表中item选项定位 xpath。replaceIndex需要二次处理，替换为实际的索引。
sslDecryptionProfiles_dropDown_maxVersion_posXpath = "//*[@id='pro_max{replaceIndex}']"  # MMin Version 下拉列表中item选项定位 xpath。replaceIndex需要二次处理，替换为实际的索引。
sslDecryptionProfiles_input_maxVersion_posXpath = "//*[@id='decryption-radio']/ancestor::div[@class='decryption_from']/div[3]//i"  # Max Version 下拉菜单xpath
sslDecryptionProfiles_switch_allowHTTP2_posXpath = "//*[@id='decryption-allow_http2']/parent::*"  # Allow HTTP2 开关xpath
sslDecryptionProfiles_button_warningSaveYes_posCss = dnsRecordsProfilePage_button_warningSaveYes_posCss  # 提示保存按钮警告框OK按钮
slDecryptionProfiles_button_warningSaveCancel_posCss = dnsRecordsProfilePage_button_warningSaveCancel_posCss  # 提示保存警告框Cancel按钮
sslDecryptionProfiles_button_oK_posCss = "#decryption-ok span"  # OK按钮css
sslDecryptionProfiles_button_cancel_posCss = "#decryption-cancel span"  # Cancel按钮

# Profiles trusted certificate authorities===================Profiles trusted certificate authorities====================Profiles trusted certificate authorities=================Profiles trusted certificate authorities
# listPage->trusted certificate authorities list page  列表页
listPage_profile_trustedCertificateAuthorities_createButton_posId = "app_create-_OperateBtns_ElRow_Certificate_Authorities_Home_App_anonymousComponent"  # create按钮id
listPage_profile_trustedCertificateAuthorities_editButton_posId = "appEdit-_OperateBtns_ElRow_Certificate_Authorities_Home_App_anonymousComponent"  # edit按钮id
listPage_profile_trustedCertificateAuthorities_delButton_posId = "appDel-_OperateBtns_ElRow_Certificate_Authorities_Home_App_anonymousComponent"  # del按钮id
listPage_profile_trustedCertificateAuthorities_linkButton_posId = "btnCopy-_OperateBtns_ElRow_Certificate_Authorities_Home_App_anonymousComponent"  # link按钮id
listPage_profileColumn_trustedCertificateAuthorities_button_columnAll_posXpath = "//div[@class='ly-eventfixed']//span[text()='All']/parent::label"  # 列选择All按钮
listPage_profileColumn_trustedCertificateAuthorities_button_cancel_posId = "dropColcancel-_ElementSet_Certificate_Authorities_Home_App_anonymousComponent"  # cancel按钮
listPage_profileColumn_trustedCertificateAuthorities_button_ok_posId = "dropColOK-_ElementSet_Certificate_Authorities_Home_App_anonymousComponent"  # ok按钮
listPage_profile_trustedCertificateAuthorities_allButton_posId = "authorities_built0"  # All按钮id
listPage_profile_trustedCertificateAuthorities_builtinButton_posId = "authorities_built1"  # Built-in按钮id
listPage_profile_trustedCertificateAuthorities_importedButton_posId = "authorities_built2"  # Imported按钮id
listPage_profile_trustedCertificateAuthorities_button_allSelect_posXpath = mainPage_profileBottomPage_button_allSelect_posXpath  # 页面底部all选择按钮
listPage_profileSearch_trustedCertificateAuthorities_selectLabel_posId = mainPage_profileSearch_selectLabel_posXpath  # 查询框id    定位形式一样
listPage_profileSearch_trustedCertificateAuthorities_buttonSearch_posId = mainPage_profileSearch_buttonSearch_posXpath  # 查询按钮id       定位形式一样
listPage_profileSearch_trustedCertificateAuthorities_buttonClear_posId = mainPage_profileSearch_buttonClear_posId  # 清空查询按钮id    定位形式一样
listPage_profileSearch_trustedCertificateAuthorities_dropDown_item_posXpath = listPage_profileSearch_dnsRecords_dropDown_item_posXpath  # 下拉菜单定位   定位形式一样
listPage_profileSearch_trustedCertificateAuthorities_input_itemContent_posXpath = listPage_profileSearch_dnsRecords_input_itemContent_posXpath  # 输入item的值，replaceName替换实际查询值    定位形式一样
listPage_profilTable_trustedCertificateAuthorities_tableTbody_posXpath = listPage_profilTable_dnsRecords_tableTbody_posXpath  # 列表tabel body  xpath   定位形式一样
listPage_profilTable_trustedCertificateAuthorities_tableHeader_posXpath = listPage_profilTable_dnsRecords_tableHeader_posXpath  # 列表table 表头xpath   定位形式一样
# listPage->Tips dialog  列表页 tips对话框
listPage_dialogTips_trustedCertificateAuthorities_button_yes_posCss = listPage_dialogTips_dnsRecords_button_yes_posXpath  # 删除提示的Tips的yes按钮
listPage_dialogTips_trustedCertificateAuthorities_button_no_posCss = listPage_dialogTips_dnsRecords_button_no_posXpath  # 删除提示的Tips的close按钮
# listPage-> Link提示对话框
listPage_linkTips_trustedCertificateAuthorities_button_save_posXpath = "//*[@id='clusterSave-_ClusterTable_ElDialog_copyComponents_Certificate_Authorities_Home_App_anonymousComponent']/i"  # 选择cluster后，save行 按钮 xpath
listPage_linkTips_trustedCertificateAuthorities_button_add_posXpath = "//*[@id='temporary_form-_ClusterTable_ElDialog_copyComponents_Certificate_Authorities_Home_App_anonymousComponent']/i"    # 添加 按钮 xpath
listPage_linkTips_trustedCertificateAuthorities_button_OK_posXpath = "//*[@id='copyOk-_copyComponents_Certificate_Authorities_Home_App_anonymousComponent']/span"    # OK 按钮 xpath
# Create trusted certificate authorities page 和 Edit trusted certificate authorities page   新增和编辑页
trustedCertificateAuthorities_headerTitle_posXpath = dnsRecordsProfilePage_headerTitle_posXpath   # 页面头部名称 xpath
trustedCertificateAuthorities_input_Name_posId = "authoritiesAdd_name"  # name输入框id
trustedCertificateAuthorities_input_certificateFile_posXpath = "//*[@id='authoritiesAdd_file']/parent::*//input"  # 证书上传按钮xpath
trustedCertificateAuthorities_button_warningSaveYes_posCss = dnsRecordsProfilePage_button_warningSaveYes_posCss  # 提示保存按钮警告框OK按钮
trustedCertificateAuthorities_button_warningSaveCancel_posCss = dnsRecordsProfilePage_button_warningSaveCancel_posCss  # 提示保存警告框Cancel按钮
trustedCertificateAuthorities_button_oK_posCss = "#authoritiesAdd_sub span"  # OK按钮css
trustedCertificateAuthorities_button_cancel_posCss = "#authoritiesAdd_cancel span"  # Cancel按钮css

# Profiles cached intermediate certificates===================Profiles cached intermediate certificates====================Profiles cached intermediate certificates=================Profiles cached intermediate certificates
# listPage->cached intermediate certificates list page  列表页
listPage_profileColumn_cachedIntermediateCertificates_button_columnAll_posXpath = "//div[@class='ly-eventfixed']//span[text()='All']/parent::label"  # 列选择All按钮
listPage_profileColumn_cachedIntermediateCertificates_button_cancel_posId = "dropColcancel-_ElementSet_Certificate_Intermediacert_Home_App_anonymousComponent"  # cancel按钮
listPage_profileColumn_cachedIntermediateCertificates_button_ok_posId = "dropColOK-_ElementSet_Certificate_Intermediacert_Home_App_anonymousComponent"  # ok按钮
listPage_profileSearch_cachedIntermediateCertificates_selectLabel_posId = mainPage_profileSearch_selectLabel_posXpath  # 查询框id    定位形式一样
listPage_profileSearch_cachedIntermediateCertificates_buttonSearch_posId = mainPage_profileSearch_buttonSearch_posXpath  # 查询按钮id       定位形式一样
listPage_profileSearch_cachedIntermediateCertificates_buttonClear_posId = mainPage_profileSearch_buttonClear_posId  # 清空查询按钮id    定位形式一样
listPage_profileSearch_cachedIntermediateCertificates_dropDown_item_posXpath = listPage_profileSearch_dnsRecords_dropDown_item_posXpath  # 下拉菜单定位   定位形式一样
listPage_profileSearch_cachedIntermediateCertificates_input_itemContent_posXpath = listPage_profileSearch_dnsRecords_input_itemContent_posXpath  # 输入item的值，replaceName替换实际查询值    定位形式一样
listPage_profilTable_cachedIntermediateCertificates_tableTbody_posXpath = listPage_profilTable_dnsRecords_tableTbody_posXpath  # 列表tabel body  xpath   定位形式一样
listPage_profilTable_cachedIntermediateCertificates_tableHeader_posXpath = listPage_profilTable_dnsRecords_tableHeader_posXpath  # 列表table 表头xpath   定位形式一样


# Profiles SSL fingerprints===================Profiles SSL fingerprints====================Profiles SSL fingerprints=================Profiles SSL fingerprints=======================Profiles SSL fingerprints
# listPage->SSL fingerprints list page  列表页
listPage_profile_sslFingerprints_createButton_posId = "app_create-_OperateBtns_ElRow_Fingerprint_Home_App_anonymousComponent"  # create按钮id
listPage_profile_sslFingerprints_editButton_posId = "appEdit-_OperateBtns_ElRow_Fingerprint_Home_App_anonymousComponent"  # edit按钮id
listPage_profile_sslFingerprints_delButton_posId = "appDel-_OperateBtns_ElRow_Fingerprint_Home_App_anonymousComponent"  # del按钮id
listPage_profile_sslFingerprints_linkButton_posId = "btnCopy-_OperateBtns_ElRow_Fingerprint_Home_App_anonymousComponent"  # link按钮id
listPage_profileColumn_sslFingerprints_button_columnAll_posXpath = "//div[@class='ly-eventfixed']//span[text()='All']/parent::label"  # 列选择All按钮
listPage_profileColumn_sslFingerprints_button_cancel_posId = "dropColcancel-_ElementSet_Fingerprint_Home_App_anonymousComponent"  # cancel按钮
listPage_profileColumn_sslFingerprints_button_ok_posId = "dropColOK-_ElementSet_Fingerprint_Home_App_anonymousComponent"  # ok按钮
listPage_profile_sslFingerprints_allButton_posId = "Fingerprint_built0"  # All按钮id
listPage_profile_sslFingerprints_pinnedButton_posId = "Fingerprint_built1"  # pinned按钮id
listPage_profile_sslFingerprints_notPinnedButton_posId = "Fingerprint_built2"  # not pinned按钮id
listPage_profile_sslFingerprints_importUAB_utton_posXpath = "//button//*[contains(@class, 'icon-SSL')]"      # 导入 user-agent 按钮定位 xpath
listPage_profile_sslFingerprints_import_Button_posXpath = "//*[@id='objectImport-_importAndExport_ElRow_Fingerprint_Home_App_anonymousComponent']"      # 导入按钮定位 xpath
listPage_profile_sslFingerprints_export_Button_posXpath = "//*[@id='objectExport-_importAndExport_ElRow_Fingerprint_Home_App_anonymousComponent']"      # 导出按钮定位 xpath
listPage_profile_sslFingerprints_importUpload_Button_posXpath = "//*[@id='SSLFingerprintUploaded']/parent::*//input"      # 上传文件 按钮定位 xpath
listPage_profile_sslFingerprints_importUploadUA_Button_posXpath = "//*[@enctype='multipart/form-data']//input"      # 上传文件 按钮定位 xpath
listPage_profile_sslFingerprints_importUploadOk_Button_posXpath = "//button[contains(@class, 'upload-button')]//span"      # 上传文件 OK 钮定位 xpath
listPage_profile_sslFingerprints_importUploadUserAgentOk_Button_posXpath = "//*[@id='Import_ua_Ok']//span"      # 上传User Agent文件 OK 钮定位 xpath
listPage_profileSearch_sslFingerprints_selectLabel_posId = mainPage_profileSearch_selectLabel_posXpath # 查询框id    定位形式一样
listPage_profileSearch_sslFingerprints_buttonSearch_posId = mainPage_profileSearch_buttonSearch_posXpath  # 查询按钮id       定位形式一样
listPage_profileSearch_sslFingerprints_buttonClear_posId = mainPage_profileSearch_buttonClear_posId  # 清空查询按钮id    定位形式一样
listPage_profileSearch_sslFingerprints_dropDown_item_posXpath = listPage_profileSearch_dnsRecords_dropDown_item_posXpath  # 下拉菜单定位   定位形式一样
listPage_profileSearch_sslFingerprints_input_itemContent_posXpath = listPage_profileSearch_dnsRecords_input_itemContent_posXpath  # 输入item的值，replaceName替换实际查询值    定位形式一样
listPage_profilTable_sslFingerprints_tableTbody_posXpath = listPage_profilTable_dnsRecords_tableTbody_posXpath  # 列表tabel body  xpath   定位形式一样
listPage_profilTable_sslFingerprints_tableHeader_posXpath = listPage_profilTable_dnsRecords_tableHeader_posXpath  # 列表table 表头xpath   定位形式一样
# listPage->Tips dialog  列表页 tips对话框
listPage_dialogTips_sslFingerprints_button_yes_posCss = listPage_dialogTips_dnsRecords_button_yes_posXpath  # 删除提示的Tips的yes按钮
listPage_dialogTips_sslFingerprints_button_no_posCss = listPage_dialogTips_dnsRecords_button_no_posXpath  # 删除提示的Tips的close按钮
# listPage-> Link提示对话框
listPage_linkTips_sslFingerprints_button_save_posXpath = "//*[@id='clusterSave-_ClusterTable_ElDialog_copyComponents_Fingerprint_Home_App_anonymousComponent']/i"  # 选择cluster后，save行 按钮 xpath
listPage_linkTips_sslFingerprints_button_add_posXpath = "//*[@id='temporary_form-_ClusterTable_ElDialog_copyComponents_Fingerprint_Home_App_anonymousComponent']/i"    # 添加 按钮 xpath
listPage_linkTips_sslFingerprints_button_OK_posXpath = "//*[@id='copyOk-_copyComponents_Fingerprint_Home_App_anonymousComponent']/span"    # OK 按钮 xpath
# Create SSL fingerprints page 和 Edit hijack files page   新增和编辑页
sslFingerprints_headerTitle_posXpath = "//div[@id='router-view-container']//div[contains(@class, 'prox-fixed-header')]"   # 页面头部名称 xpath
sslFingerprints_input_ja3Hash_posXpath = "//*[@id='authoritiesAdd_name1']"  # ja3 hash 输入框 xpath
sslFingerprints_button_siPinningYes_posXpath = "//*[@id='pinningStateYes']"  # is pinning yes 按钮 xpath
sslFingerprints_button_siPinningNo_posXpath = "//*[@id='pinningStateNo']"  # is pinning no 按钮 xpath
sslFingerprints_input_description_posXpath =  "//*[@id='labels_describe']"  # description 输入框 xpath
sslFingerprints_button_warningSaveYes_posCss = dnsRecordsProfilePage_button_warningSaveYes_posCss  # 提示保存按钮警告框OK按钮
sslFingerprints_button_warningSaveCancel_posCss = dnsRecordsProfilePage_button_warningSaveCancel_posCss  # 提示保存警告框Cancel按钮
sslFingerprints_button_oK_posCss = "#authoritiesAdd_sub span"  # OK按钮css
sslFingerprints_button_cancel_posCss = "#authoritiesAdd_cancel span"  # Cancel按钮


# Profiles tcp proxy profiles===================Profiles tcp proxy profiles====================Profiles tcp proxy profiles=================Profiles tcp proxy profiles=======================Profiles tcp proxy profiles
# listPage->tcp proxy profiles list page  列表页
listPage_profile_tcpProxyProfiles_createButton_posId = "app_create-_OperateBtns_ElRow_advanced_Home_App_anonymousComponent"  # create按钮id
listPage_profile_tcpProxyProfiles_editButton_posId = "appEdit-_OperateBtns_ElRow_advanced_Home_App_anonymousComponent"  # edit按钮id
listPage_profile_tcpProxyProfiles_delButton_posId = "appDel-_OperateBtns_ElRow_advanced_Home_App_anonymousComponent"  # del按钮id
listPage_profile_tcpProxyProfiles_linkButton_posId = "btnCopy-_OperateBtns_ElRow_advanced_Home_App_anonymousComponent"  # link按钮id
listPage_profileColumn_tcpProxyProfiles_button_columnAll_posXpath = "//div[@class='ly-eventfixed']//span[text()='All']/parent::label"  # 列选择All按钮
listPage_profileColumn_tcpProxyProfiles_button_cancel_posId = "dropColcancel-_ElementSet_advanced_Home_App_anonymousComponent"  # cancel按钮
listPage_profileColumn_tcpProxyProfiles_button_ok_posId = "dropColOK-_ElementSet_advanced_Home_App_anonymousComponent"  # ok按钮
listPage_profileSearch_tcpProxyProfiles_selectLabel_posId = mainPage_profileSearch_selectLabel_posXpath  # 查询框id    定位形式一样
listPage_profileSearch_tcpProxyProfiles_buttonSearch_posId = mainPage_profileSearch_buttonSearch_posXpath  # 查询按钮id       定位形式一样
listPage_profileSearch_tcpProxyProfiles_buttonClear_posId = mainPage_profileSearch_buttonClear_posId  # 清空查询按钮id    定位形式一样
listPage_profileSearch_tcpProxyProfiles_dropDown_item_posXpath = listPage_profileSearch_dnsRecords_dropDown_item_posXpath  # 下拉菜单定位   定位形式一样
listPage_profileSearch_tcpProxyProfiles_input_itemContent_posXpath = listPage_profileSearch_dnsRecords_input_itemContent_posXpath  # 输入item的值，replaceName替换实际查询值    定位形式一样
listPage_profilTable_tcpProxyProfiles_tableTbody_posXpath = listPage_profilTable_dnsRecords_tableTbody_posXpath  # 列表tabel body  xpath   定位形式一样
listPage_profilTable_tcpProxyProfiles_tableHeader_posXpath = listPage_profilTable_dnsRecords_tableHeader_posXpath  # 列表table 表头xpath   定位形式一样
# listPage->Tips dialog  列表页 tips对话框
listPage_dialogTips_tcpProxyProfiles_button_yes_posXpath = listPage_dialogTips_dnsRecords_button_yes_posXpath  # 删除提示的Tips的yes按钮
listPage_dialogTips_tcpProxyProfiles_button_no_posXpath = listPage_dialogTips_dnsRecords_button_no_posXpath  # 删除提示的Tips的close按钮
# listPage-> Link提示对话框
listPage_linkTips_tcpProxyProfiles_button_save_posXpath = "//*[@id='clusterSave-_ClusterTable_ElDialog_copyComponents_advanced_Home_App_anonymousComponent']/i"  # 选择cluster后，save行 按钮 xpath
listPage_linkTips_tcpProxyProfiles_button_add_posXpath = "//*[@id='temporary_form-_ClusterTable_ElDialog_copyComponents_advanced_Home_App_anonymousComponent']/i"    # 添加 按钮 xpath
listPage_linkTips_tcpProxyProfiles_button_OK_posXpath = "//*[@id='copyOk-_copyComponents_advanced_Home_App_anonymousComponent']/span"    # OK 按钮 xpath
# Create tcp proxy profiles page 和 Edit tcp proxy profiles page   新增和编辑页
tcpProxyProfiles_headerTitle_posXpath = "//div[@id='router-view-container']//div[contains(@class, 'policy-form-header')]/span"   # 页面头部名称 xpath
tcpProxyProfiles_input_Name_posId = "advancedAdd_policyName"  # name输入框id
tcpProxyProfiles_switch_enableTCPPassthrough_posXpath = "//*[@id='proxytcpThrough1']/parent::*"  # Enable TCP Passthrough状态开关 xpath
tcpProxyProfiles_switch_clientOverrideMSS_posXpath = "(//*[@id='anonymousComponent_ElForm_advancedAdd_Home_App_anonymousComponent_proxytcpParameter_tcp_maxseg'])[1]/parent::*"  # Client-side Override MSS状态开关  xpath，点击操作其子元素改变状态
tcpProxyProfiles_input_clientOverrideMSS_posXpath = "//div[@id='policy_paper_left']/div[2]/form/div[6]/form/div[2]/div/div/input"  # Client-side Override MSS输入框 xpath
tcpProxyProfiles_switch_clientNoDelay_posXpath = "(//*[@id='proxytcpParameters_nodelay_anonymousComponent_ElForm_advancedAdd_Home_App_anonymousComponent'])[1]/parent::*"  # Client-side No Delay状态开关  xpath，点击操作其子元素改变状态
tcpProxyProfiles_input_clientTTL_posXpath = "(//*[@id='proxytcpParameters_ttl_anonymousComponent_ElForm_advancedAdd_Home_App_anonymousComponent'])[1]"  # Client-side TTL输入框 xpath
tcpProxyProfiles_switch_clientKeepalive_posXpath = "(//*[@id='anonymousComponent_ElForm_advancedAdd_Home_App_anonymousComponent_proxytcpParameters_keepalive'])[1]/parent::*"  # Client-side Keepalive状态开关  xpath，点击操作其子元素改变状态
tcpProxyProfiles_input_clientProbeNumber_posXpath = "(//*[@id='proxytcpParameters_keepcnt'])[1]"  # Client-side Probe Number输入框 xpath
tcpProxyProfiles_input_clientIdleTime_posXpath = "(//*[@id='proxytcpParameters_ldeleTime'])[1]"  # Client-side Idle Time输入框 xpath
tcpProxyProfiles_input_clientInterval_posXpath = "(//*[@id='proxytcpParameters_interval'])[1]"  # Client-side Interval输入框 xpath
tcpProxyProfiles_switch_clientUserTimeout_posXpath = "(//*[@id='anonymousComponent_ElForm_advancedAdd_Home_App_anonymousComponent_proxytcpParameters_keepalive'])[2]/parent::*"  # Client-side User Timeout状态开关  xpath，点击操作其子元素改变状态
tcpProxyProfiles_input_clientUserTimeout_posXpath = "(//*[@id='proxytcpParameters_userTimeout_anonymousComponent_ElForm_advancedAdd_Home_App_anonymousComponent'])[1]"  # Client-side User Timeout输入框 xpath
tcpProxyProfiles_switch_serverOverrideMSS_posXpath = "(//*[@id='anonymousComponent_ElForm_advancedAdd_Home_App_anonymousComponent_proxytcpParameter_tcp_maxseg'])[2]/parent::*"  # Server-side Override MSS状态开关  xpath，点击操作其子元素改变状态
tcpProxyProfiles_input_serverOverrideMSS_posXpath = "//div[@id='policy_paper_left']/div[2]/form/div[7]/form/div[2]/div/div/input"  # Server-side Override MSS输入框 xpath
tcpProxyProfiles_switch_serverNoDelay_posXpath = "(//*[@id='proxytcpParameters_nodelay_anonymousComponent_ElForm_advancedAdd_Home_App_anonymousComponent'])[2]/parent::*"  # Server-side No Delay状态开关  xpath，点击操作其子元素改变状态
tcpProxyProfiles_input_serverTTL_posXpath = "(//*[@id='proxytcpParameters_ttl_anonymousComponent_ElForm_advancedAdd_Home_App_anonymousComponent'])[2]"  # Server-side TTL输入框 xpath
tcpProxyProfiles_switch_serverKeepalive_posXpath = "(//*[@id='anonymousComponent_ElForm_advancedAdd_Home_App_anonymousComponent_proxytcpParameters_keepalive'])[3]/parent::*"  # Server-side Keepalive状态开关  xpath，点击操作其子元素改变状态
tcpProxyProfiles_input_serverProbeNumber_posXpath = "(//*[@id='proxytcpParameters_keepcnt'])[2]"  # Server-side Probe Number输入框 xpath
tcpProxyProfiles_input_serverIdleTime_posXpath = "(//*[@id='proxytcpParameters_ldeleTime'])[2]"  # Server-side Idle Time输入框 xpath
tcpProxyProfiles_input_serverInterval_posXpath = "(//*[@id='proxytcpParameters_interval'])[2]"  # Server-side Interval输入框 xpath
tcpProxyProfiles_switch_serverUserTimeout_posXpath = "(//*[@id='anonymousComponent_ElForm_advancedAdd_Home_App_anonymousComponent_proxytcpParameters_keepalive'])[4]/parent::*"  # Server-side User Timeout状态开关  xpath，点击操作其子元素改变状态
tcpProxyProfiles_input_serverUserTimeout_posXpath = "(//*[@id='proxytcpParameters_userTimeout_anonymousComponent_ElForm_advancedAdd_Home_App_anonymousComponent'])[2]"  # Client-side User Timeout输入框 xpath
tcpProxyProfiles_button_warningSaveYes_posCss = dnsRecordsProfilePage_button_warningSaveYes_posCss  # 提示保存按钮警告框OK按钮
tcpProxyProfiles_button_warningSaveCancel_posCss = dnsRecordsProfilePage_button_warningSaveCancel_posCss  # 提示保存警告框Cancel按钮
tcpProxyProfiles_button_oK_posCss = "#proxyTCPSuccess span"  # OK按钮css
tcpProxyProfiles_button_cancel_posCss = "#proxyTCPCancel span"  # Cancel按钮css

# Profiles hijack files===================Profiles hijack files====================Profiles hijack files=================Profiles hijack files=======================Profiles hijack files
# listPage->hijack files list page  列表页
listPage_profile_hijackFiles_createButton_posId = "app_create-_OperateBtns_ElRow_Profile_HijackFiles_Home_App_anonymousComponent"  # create按钮id
listPage_profile_hijackFiles_editButton_posId = "appEdit-_OperateBtns_ElRow_Profile_HijackFiles_Home_App_anonymousComponent"  # edit按钮id
listPage_profile_hijackFiles_delButton_posId = "appDel-_OperateBtns_ElRow_Profile_HijackFiles_Home_App_anonymousComponent"  # del按钮id
listPage_profile_hijackFiles_linkButton_posId = "btnCopy-_OperateBtns_ElRow_Profile_HijackFiles_Home_App_anonymousComponent"  # link按钮id
listPage_profileColumn_hijackFiles_button_columnAll_posXpath = "//div[@class='ly-eventfixed']//span[text()='All']/parent::label"  # 列选择All按钮
listPage_profileColumn_hijackFiles_button_cancel_posId = "dropColcancel-_ElementSet_Profile_HijackFiles_Home_App_anonymousComponent"  # cancel按钮
listPage_profileColumn_hijackFiles_button_ok_posId = "dropColOK-_ElementSet_Profile_HijackFiles_Home_App_anonymousComponent"  # ok按钮
listPage_profileSearch_hijackFiles_selectLabel_posId = mainPage_profileSearch_selectLabel_posXpath  # 查询框id    定位形式一样
listPage_profileSearch_hijackFiles_buttonSearch_posId = mainPage_profileSearch_buttonSearch_posXpath  # 查询按钮id       定位形式一样
listPage_profileSearch_hijackFiles_buttonClear_posId = mainPage_profileSearch_buttonClear_posId  # 清空查询按钮id    定位形式一样
listPage_profileSearch_hijackFiles_dropDown_item_posXpath = listPage_profileSearch_dnsRecords_dropDown_item_posXpath  # 下拉菜单定位   定位形式一样
listPage_profileSearch_hijackFiles_input_itemContent_posXpath = listPage_profileSearch_dnsRecords_input_itemContent_posXpath  # 输入item的值，replaceName替换实际查询值    定位形式一样
listPage_profilTable_hijackFiles_tableTbody_posXpath = listPage_profilTable_dnsRecords_tableTbody_posXpath  # 列表tabel body  xpath   定位形式一样
listPage_profilTable_hijackFiles_tableHeader_posXpath = listPage_profilTable_dnsRecords_tableHeader_posXpath  # 列表table 表头xpath   定位形式一样
# listPage->Tips dialog  列表页 tips对话框
listPage_dialogTips_hijackFiles_button_yes_posXpath = listPage_dialogTips_dnsRecords_button_yes_posXpath  # 删除提示的Tips的yes按钮
listPage_dialogTips_hijackFiles_button_no_posXpath = listPage_dialogTips_dnsRecords_button_no_posXpath  # 删除提示的Tips的close按钮
# listPage-> Link提示对话框
listPage_linkTips_hijackFiles_button_save_posXpath = "//*[@id='clusterSave-_ClusterTable_ElDialog_copyComponents_Profile_HijackFiles_Home_App_anonymousComponent']/i"  # 选择cluster后，save行 按钮 xpath
listPage_linkTips_hijackFiles_button_add_posXpath = "//*[@id='temporary_form-_ClusterTable_ElDialog_copyComponents_Profile_HijackFiles_Home_App_anonymousComponent']/i"    # 添加 按钮 xpath
listPage_linkTips_hijackFiles_button_OK_posXpath = "//*[@id='copyOk-_copyComponents_Profile_HijackFiles_Home_App_anonymousComponent']/span"    # OK 按钮 xpath
# Create hijack files page 和 Edit hijack files page   新增和编辑页
hijackFiles_headerTitle_posXpath = dnsRecordsProfilePage_headerTitle_posXpath   # 页面头部名称 xpath
hijackFiles_input_Name_posId = "hijack_name"  # name输入框id
hijackFiles_input_fileUpLoad_posXpath = "//*[@id='uploadFile']/parent::*//input"  # input 上传文件xpath
hijackFiles_switch_downLoadName_posXpath = "//*[@id='contentNameChoose']/parent::*"  # download name状态开关  xpath，点击操作其子元素改变状态
hijackFiles_input_downLoadName_posXpath = "//*[@id='hijack_contentName']"  # 下载文件名称输入框 xpath
hijackFiles_button_fileType_posXpath = "//*[normalize-space(text())='File Type']/parent::*//input"  # 添加文件类型按钮 xpath
hijackFiles_tablist_fileType_posXpath = "//*[@class='el-scrollbar']//span[normalize-space(text())='{replaceName}']"  # 右侧滑中type元素定位 xpath。需要二次处理，replaceName替换为类型名称
hijackFiles_button_warningSaveYes_posCss = dnsRecordsProfilePage_button_warningSaveYes_posCss  # 提示保存按钮警告框OK按钮
hijackFiles_button_warningSaveCancel_posCss = dnsRecordsProfilePage_button_warningSaveCancel_posCss  # 提示保存警告框Cancel按钮
hijackFiles_button_oK_posCss = "#hijackAddOk1 span"  # OK按钮css
hijackFiles_button_cancel_posCss = "#hijackAddCancel1 span"  # Cancel按钮

# Profiles insert scripts===================Profiles insert scripts====================Profiles insert scripts=================Profiles insert scripts=======================Profiles insert scripts
# listPage->insert scripts list page  列表页
listPage_profile_insertScripts_createButton_posId = "app_create-_OperateBtns_ElRow_Profile_Insert_Home_App_anonymousComponent"  # create按钮id
listPage_profile_insertScripts_editButton_posId = "appEdit-_OperateBtns_ElRow_Profile_Insert_Home_App_anonymousComponent"  # edit按钮id
listPage_profile_insertScripts_delButton_posId = "appDel-_OperateBtns_ElRow_Profile_Insert_Home_App_anonymousComponent"  # del按钮id
listPage_profile_insertScripts_linkButton_posId = "btnCopy-_OperateBtns_ElRow_Profile_Insert_Home_App_anonymousComponent"  # link按钮id
listPage_profileColumn_insertScripts_button_columnAll_posXpath = "//div[@class='ly-eventfixed']//span[text()='All']/parent::label"  # 列选择All按钮
listPage_profileColumn_insertScripts_button_cancel_posId = "dropColcancel-_ElementSet_Profile_Insert_Home_App_anonymousComponent"  # cancel按钮
listPage_profileColumn_insertScripts_button_ok_posId = "dropColOK-_ElementSet_Profile_Insert_Home_App_anonymousComponent"  # ok按钮
listPage_profileSearch_insertScripts_selectLabel_posId = mainPage_profileSearch_selectLabel_posXpath  # 查询框id    定位形式一样
listPage_profileSearch_insertScripts_buttonSearch_posId = mainPage_profileSearch_buttonSearch_posXpath  # 查询按钮id       定位形式一样
listPage_profileSearch_insertScripts_buttonClear_posId = mainPage_profileSearch_buttonClear_posId  # 清空查询按钮id    定位形式一样
listPage_profileSearch_insertScripts_dropDown_item_posXpath = listPage_profileSearch_dnsRecords_dropDown_item_posXpath  # 下拉菜单定位   定位形式一样
listPage_profileSearch_insertScripts_input_itemContent_posXpath = listPage_profileSearch_dnsRecords_input_itemContent_posXpath  # 输入item的值，replaceName替换实际查询值    定位形式一样
listPage_profilTable_insertScripts_tableTbody_posXpath = listPage_profilTable_dnsRecords_tableTbody_posXpath  # 列表tabel body  xpath   定位形式一样
listPage_profilTable_insertScripts_tableHeader_posXpath = listPage_profilTable_dnsRecords_tableHeader_posXpath  # 列表table 表头xpath   定位形式一样
# listPage->Tips dialog  列表页 tips对话框
listPage_dialogTips_insertScripts_button_yes_posXpath = listPage_dialogTips_dnsRecords_button_yes_posXpath  # 删除提示的Tips的yes按钮
listPage_dialogTips_insertScripts_button_no_posXpath = listPage_dialogTips_dnsRecords_button_no_posXpath  # 删除提示的Tips的close按钮
# listPage-> Link提示对话框
listPage_linkTips_insertScripts_button_save_posXpath = "//*[@id='clusterSave-_ClusterTable_ElDialog_copyComponents_Profile_Insert_Home_App_anonymousComponent']/i"  # 选择cluster后，save行 按钮 xpath
listPage_linkTips_insertScripts_button_add_posXpath = "//*[@id='temporary_form-_ClusterTable_ElDialog_copyComponents_Profile_Insert_Home_App_anonymousComponent']/i"    # 添加 按钮 xpath
listPage_linkTips_insertScripts_button_OK_posXpath = "//*[@id='copyOk-_copyComponents_Profile_Insert_Home_App_anonymousComponent']/span"    # OK 按钮 xpath
# Create insert scripts page 和 Edit inserts script page   新增和编辑页
insertScripts_headerTitle_posXpath = dnsRecordsProfilePage_headerTitle_posXpath   # 页面头部名称 xpath
insertScripts_input_Name_posId = "insert_profileName"  # name输入框id
insertScripts_input_scriptUpLoad_posXpath = "//*[@id='insertAddUpload']//input"  # input 上传文件xpath
insertScripts_input_scriptType_posXpath = "//*[@id='insert_select_format']"  # input 文件类型选择xpath
insertScripts_dropdown_jsItem_posXpath = "//*[@id='insert_select_formatjs']"  # 下拉菜单 js选项 xpath
insertScripts_dropdown_cssItem_posXpath = "//*[@id='insert_select_formatcss']"  # 下拉菜单 js选项 xpath
insertScripts_input_insertPosition_posXpath = "//*[@id='insert_select_insertOn']"  # input insert position xpath
insertScripts_dropdown_beforePageLoadItem_posXpath = "//*[@x-placement='bottom-start']//li[1]"  # 下拉菜单 before page load xpath
insertScripts_dropdown_afterPageLoadItem_posXpath = "//*[@x-placement='bottom-start']//li[2]"  # 下拉菜单 after page load xpath
insertScripts_alert_topInfo_Xpath = profilePage_alert_topInfo_Xpath  # 页面顶部alert信息
insertScripts_button_warningSaveYes_posCss = dnsRecordsProfilePage_button_warningSaveYes_posCss  # 提示保存按钮警告框OK按钮
insertScripts_button_warningSaveCancel_posCss = dnsRecordsProfilePage_button_warningSaveCancel_posCss  # 提示保存警告框Cancel按钮
insertScripts_button_oK_posCss = "#insertAddOk1 span"  # OK按钮css
insertScripts_button_cancel_posCss = "#insertAddCancel1 span"  # Cancel按钮

# Profiles tsg proxy scripts===================Profiles tsg proxy scripts====================Profiles tsg proxy scripts=================Profiles tsg proxy scripts=======================Profiles tsg proxy scripts
# listPage->tsg proxy scripts list page  列表页
listPage_profile_tsgProxyScripts_createButton_posId = "app_create-_OperateBtns_ElRow_Profile_RunScript_Home_App_anonymousComponent"  # create按钮id
listPage_profile_tsgProxyScripts_editButton_posId = "appEdit-_OperateBtns_ElRow_Profile_RunScript_Home_App_anonymousComponent"  # edit按钮id
listPage_profile_tsgProxyScripts_delButton_posId = "appDel-_OperateBtns_ElRow_Profile_RunScript_Home_App_anonymousComponent"  # del按钮id
listPage_profileColumn_tsgProxyScripts_button_columnAll_posXpath = "//div[@class='ly-eventfixed']//span[text()='All']/parent::label"  # 列选择All按钮
listPage_profileColumn_tsgProxyScripts_button_cancel_posId = "dropColcancel-_ElementSet_Profile_RunScript_Home_App_anonymousComponent"  # cancel按钮
listPage_profileColumn_tsgProxyScripts_button_ok_posId = "dropColOK-_ElementSet_Profile_RunScript_Home_App_anonymousComponent"  # ok按钮
listPage_profileSearch_tsgProxyScripts_selectLabel_posId = mainPage_profileSearch_selectLabel_posXpath  # 查询框id    定位形式一样
listPage_profileSearch_tsgProxyScripts_buttonSearch_posId = mainPage_profileSearch_buttonSearch_posXpath  # 查询按钮id       定位形式一样
listPage_profileSearch_tsgProxyScripts_buttonClear_posId = mainPage_profileSearch_buttonClear_posId  # 清空查询按钮id    定位形式一样
listPage_profileSearch_tsgProxyScripts_dropDown_item_posXpath = listPage_profileSearch_dnsRecords_dropDown_item_posXpath  # 下拉菜单定位   定位形式一样
listPage_profileSearch_tsgProxyScripts_input_itemContent_posXpath = listPage_profileSearch_dnsRecords_input_itemContent_posXpath  # 输入item的值，replaceName替换实际查询值    定位形式一样
listPage_profilTable_tsgProxyScripts_tableTbody_posXpath = listPage_profilTable_dnsRecords_tableTbody_posXpath  # 列表tabel body  xpath   定位形式一样
listPage_profilTable_tsgProxyScripts_tableHeader_posXpath = listPage_profilTable_dnsRecords_tableHeader_posXpath  # 列表table 表头xpath   定位形式一样
# listPage->Tips dialog  列表页 tips对话框
listPage_dialogTips_tsgProxyScripts_button_yes_posXpath = listPage_dialogTips_dnsRecords_button_yes_posXpath  # 删除提示的Tips的yes按钮
listPage_dialogTips_tsgProxyScripts_button_no_posXpath = listPage_dialogTips_dnsRecords_button_no_posXpath  # 删除提示的Tips的close按钮
# Create tsg proxy scripts page 和 Edit tsg proxy scripts page   新增和编辑页
tsgProxyScripts_headerTitle_posXpath = dnsRecordsProfilePage_headerTitle_posXpath   # 页面头部名称 xpath
tsgProxyScripts_input_Name_posXpath = "//*[@class='biFangName']//input"  # name输入框xpath
tsgProxyScripts_input_runScripts_posXpath = "//*[@id='uloadFile']/parent::*//input"  # input 上传文件xpath
tsgProxyScripts_input_maximumExecutionTime_posXpath = "//*[@id='insert_select_format']"  # input Maximum Execution Time xpath
tsgProxyScripts_alert_topInfo_Xpath = profilePage_alert_topInfo_Xpath  # 顶部提示信息alert框
tsgProxyScripts_button_warningSaveYes_posCss = dnsRecordsProfilePage_button_warningSaveYes_posCss  # 提示保存按钮警告框OK按钮
tsgProxyScripts_button_warningSaveCancel_posCss = dnsRecordsProfilePage_button_warningSaveCancel_posCss  # 提示保存警告框Cancel按钮
tsgProxyScripts_button_oK_posCss = "#runScriptOk1 span"  # OK按钮css
tsgProxyScripts_button_cancel_posCss = "#runScriptCancel1 span"  # Cancel按钮

# Profiles vpn accounts===================Profiles vpn accounts====================Profiles vpn accounts=================Profiles vpn accounts=======================Profiles vpn accounts
# listPage->tsg vpn accounts list page  列表页
listPage_profile_vpnAccounts_createButton_posId = "app_create-_OperateBtns_ElCol_ElRow_Setting_Wannat_Home_App_anonymousComponent"  # create按钮id
listPage_profile_vpnAccounts_editButton_posId = "appEdit-_OperateBtns_ElCol_ElRow_Setting_Wannat_Home_App_anonymousComponent"  # edit按钮id
listPage_profile_vpnAccounts_delButton_posId = "appDel-_OperateBtns_ElCol_ElRow_Setting_Wannat_Home_App_anonymousComponent"  # del按钮id
listPage_profileSearch_vpnAccounts_selectLabel_posId = mainPage_profileSearch_selectLabel_posXpath  # 查询框id    定位形式一样
listPage_profileSearch_vpnAccounts_buttonSearch_posId = mainPage_profileSearch_buttonSearch_posXpath  # 查询按钮id       定位形式一样
listPage_profileSearch_vpnAccounts_buttonClear_posId = mainPage_profileSearch_buttonClear_posId  # 清空查询按钮id    定位形式一样
listPage_profileSearch_vpnAccounts_dropDown_item_posXpath = listPage_profileSearch_dnsRecords_dropDown_item_posXpath  # 下拉菜单定位   定位形式一样
listPage_profileSearch_vpnAccounts_input_itemContent_posXpath = listPage_profileSearch_dnsRecords_input_itemContent_posXpath  # 输入item的值，replaceName替换实际查询值    定位形式一样
listPage_profilTable_vpnAccounts_tableTbody_posXpath = listPage_profilTable_dnsRecords_tableTbody_posXpath  # 列表tabel body  xpath   定位形式一样
listPage_profilTable_vpnAccounts_tableHeader_posXpath = listPage_profilTable_dnsRecords_tableHeader_posXpath  # 列表table 表头xpath   定位形式一样
# listPage->Tips dialog  列表页 tips对话框
listPage_dialogTips_vpnAccounts_button_yes_posCss = listPage_dialogTips_dnsRecords_button_yes_posXpath  # 删除提示的Tips的yes按钮
listPage_dialogTips_vpnAccounts_button_no_posCss = listPage_dialogTips_dnsRecords_button_no_posXpath  # 删除提示的Tips的close按钮
# Create vpn accounts page 和 Edit vpn accounts page   新增和编辑页
vpnAccounts_input_vpnName_posXpath = "//*[@id='wannat_vpn_username']"  # vpn name输入框xpath
vpnAccounts_input_vpnpassword_posXpath = "//*[@id='Account_VPanel_VEditPanel_Setting_WannatDetail_Home_App_anonymousComponent_formPassword']"  # input vpn password xpath
vpnAccounts_button_warningSaveYes_posCss = dnsRecordsProfilePage_button_warningSaveYes_posCss  # 提示保存按钮警告框OK按钮
vpnAccounts_button_warningSaveCancel_posCss = dnsRecordsProfilePage_button_warningSaveCancel_posCss  # 提示保存警告框Cancel按钮
vpnAccounts_button_oK_posCss = "#wanAdd_ok-_Setting_WannatDetail_Home_App_anonymousComponent span"  # OK按钮css
vpnAccounts_button_cancel_posCss = "#wanAdd_cancel-_Setting_WannatDetail_Home_App_anonymousComponent span"  # Cancel按钮

# Profiles wannat test servers===================Profiles wannat test servers====================Profiles wannat test servers=================Profiles wannat test servers=======================Profiles wannat test servers
# listPage->tsg wannat test servers list page  列表页
listPage_profile_wannatTestServers_createButton_posId = "app_create-_OperateBtns_ElCol_ElRow_Setting_Wannat_Home_App_anonymousComponent"  # create按钮id
listPage_profile_wannatTestServers_editButton_posId = "appEdit-_OperateBtns_ElCol_ElRow_Setting_Wannat_Home_App_anonymousComponent"  # edit按钮id
listPage_profile_wannatTestServers_delButton_posId = "appDel-_OperateBtns_ElCol_ElRow_Setting_Wannat_Home_App_anonymousComponent"  # del按钮id
listPage_profileSearch_wannatTestServers_selectLabel_posId = mainPage_profileSearch_selectLabel_posXpath  # 查询框id    定位形式一样
listPage_profileSearch_wannatTestServers_buttonSearch_posId = mainPage_profileSearch_buttonSearch_posXpath  # 查询按钮id       定位形式一样
listPage_profileSearch_wannatTestServers_buttonClear_posId = mainPage_profileSearch_buttonClear_posId  # 清空查询按钮id    定位形式一样
listPage_profileSearch_wannatTestServers_dropDown_item_posXpath = listPage_profileSearch_dnsRecords_dropDown_item_posXpath  # 下拉菜单定位   定位形式一样
listPage_profileSearch_wannatTestServers_input_itemContent_posXpath = listPage_profileSearch_dnsRecords_input_itemContent_posXpath  # 输入item的值，replaceName替换实际查询值    定位形式一样
listPage_profilTable_wannatTestServers_tableTbody_posXpath = listPage_profilTable_dnsRecords_tableTbody_posXpath  # 列表tabel body  xpath   定位形式一样
listPage_profilTable_wannatTestServers_tableHeader_posXpath = listPage_profilTable_dnsRecords_tableHeader_posXpath  # 列表table 表头xpath   定位形式一样
# listPage->Tips dialog  列表页 tips对话框
listPage_dialogTips_wannatTestServers_button_yes_posCss = listPage_dialogTips_dnsRecords_button_yes_posXpath  # 删除提示的Tips的yes按钮
listPage_dialogTips_wannatTestServers_button_no_posCss = listPage_dialogTips_dnsRecords_button_no_posXpath  # 删除提示的Tips的close按钮
# Create  wannat test servers page 和 Edit wannat test servers page   新增和编辑页
wannatTestServers_input_Name_posId = "profileName"  # name输入框id
wannatTestServers_input_serverType_posXpath = "//*[@id='type']"  # server type 下拉选择框定位Xpath
wannatTestServers_dropdown_serverTypeDnsItem_posXpath = "//*[@id='DNS']"  # server type 下拉列表DNS项选择定位 Xpath
wannatTestServers_input_ip_posXpath = "//*[@id='formIp']"  # i输入框定位 Xpath
wannatTestServers_input_serverRelativeLocation_posXpath = "//*[@id='relativeLocation']"  # Server Relative Location下拉选择框定位 Xpath
wannatTestServers_dropdown_serverRelativeLocationInternalItem_posXpath = "//*[@id='Internal']"  # Server Relative Location下拉列表Internal选项 Xpath
wannatTestServers_dropdown_serverRelativeLocationExternalItem_posXpath = "//*[@id='External']"  # Server Relative Location下拉列表External选项 Xpath
wannatTestServers_input_serverLocation_posXpath = "//*[@id='formGeoLocation']"  # Server Location输入框 Xpath
wannatTestServers_input_description_posXpath = "//*[@id='formProfileDesc']"  # Description输入框 Xpath
wannatTestServers_switch_isValid_posXpath = "//*[@id='wannat_testserver_isValid']/parent::*"  # 开关IsValid Xpath
wannatTestServers_button_warningSaveYes_posCss = dnsRecordsProfilePage_button_warningSaveYes_posCss  # 提示保存按钮警告框OK按钮
wannatTestServers_button_warningSaveCancel_posCss = dnsRecordsProfilePage_button_warningSaveCancel_posCss  # 提示保存警告框Cancel按钮
wannatTestServers_button_oK_posCss = "#wanAdd_ok-_Setting_WannatDetail_Home_App_anonymousComponent span"  # OK按钮css
wannatTestServers_button_cancel_posCss = "#wanAdd_cancel-_Setting_WannatDetail_Home_App_anonymousComponent span"  # Cancel按钮

# Profiles dos detection profiles===================Profiles dos detection profiles====================Profiles dos detection profiles=================Profiles dos detection profiles=======================Profiles dos detection profiles
# listPage->tsg dos detection profiles list page  列表页
listPage_profile_dosDetectionProfiles_createButton_posId = "app_create-_OperateBtns_ElRow_detectionProfiles_Home_App_anonymousComponent"  # create按钮id
listPage_profile_dosDetectionProfiles_editButton_posId = "appEdit-_OperateBtns_ElRow_detectionProfiles_Home_App_anonymousComponent"  # edit按钮id
listPage_profile_dosDetectionProfiles_delButton_posId = "appDel-_OperateBtns_ElRow_detectionProfiles_Home_App_anonymousComponent"  # del按钮id
listPage_profile_dosDetectionProfiles_viewButton_posId = "appEdit-_OperateBtns_ElRow_detectionProfiles_Home_App_anonymousComponent"  # view按钮id
listPage_profileColumn_dosDetectionProfiles_button_columnAll_posXpath = "//div[@class='all-btn']//label"  # 列选择All按钮
listPage_profileColumn_dosDetectionProfiles_button_columnCancel_posId = "dropColALlFalse-_ElementSet_detectionProfiles_Home_App_anonymousComponent"  # 列选择Cancel按钮
listPage_profileColumn_dosDetectionProfiles_button_cancel_posId = "dropColcancel-_ElementSet_detectionProfiles_Home_App_anonymousComponent"  # cancel按钮
listPage_profileColumn_dosDetectionProfiles_button_ok_posId = "dropColOK-_ElementSet_detectionProfiles_Home_App_anonymousComponent"  # ok按钮
listPage_profileSearch_dosDetectionProfiles_selectLabel_posId = mainPage_profileSearch_selectLabel_posXpath  # 查询框id    定位形式一样
listPage_profileSearch_dosDetectionProfiles_buttonSearch_posId = mainPage_profileSearch_buttonSearch_posXpath  # 查询按钮id       定位形式一样
listPage_profileSearch_dosDetectionProfiles_buttonClear_posId = mainPage_profileSearch_buttonClear_posId  # 清空查询按钮id    定位形式一样
listPage_profileSearch_dosDetectionProfiles_dropDown_item_posXpath = listPage_profileSearch_dnsRecords_dropDown_item_posXpath  # 下拉菜单定位   定位形式一样
listPage_profileSearch_dosDetectionProfiles_input_itemContent_posXpath = listPage_profileSearch_dnsRecords_input_itemContent_posXpath  # 输入item的值，replaceName替换实际查询值    定位形式一样
listPage_profilTable_dosDetectionProfiles_tableTbody_posXpath = listPage_profilTable_dnsRecords_tableTbody_posXpath  # 列表tabel body  xpath   定位形式一样
listPage_profilTable_dosDetectionProfiles_tableHeader_posXpath = listPage_profilTable_dnsRecords_tableHeader_posXpath  # 列表table 表头xpath   定位形式一样
listPage_profileBottomPageNum_dosDetectionProfiles_posXpath = "//*[@id='pagination-_pagination_detectionProfiles_Home_App_anonymousComponent']"  # 页面底部翻页 定位
# listPage->Tips dialog  列表页 tips对话框
listPage_dialogTips_dosDetectionProfiles_button_yes_posCss = listPage_dialogTips_dnsRecords_button_yes_posXpath  # 删除提示的Tips的yes按钮
listPage_dialogTips_dosDetectionProfiles_button_no_posCss = listPage_dialogTips_dnsRecords_button_no_posXpath  # 删除提示的Tips的close按钮
# Create tdos detection profiles page 和 Edit dos detection profiles page   新增和编辑页
dosDetectionProfiles_pageContent_posXpath = profilePage_content  # profile创建、编辑页面查看
dosDetectionProfiles_input_Name_posId = "name"  # name输入框id
dosDetectionProfiles_radio_attackType_posXpath = "//*[@id='{rplaceName}']"  # attack type单选按钮，replaceName需要二次处理替换内容
dosDetectionProfiles_button_ipAdd_posXpath = "//*[@id='temporary_form']"  # ip添加按钮 xpath
dosDetectionProfiles_input_ipItems_posXpath = "//*[@class='list-container']//div[@class='item-row']"  # ip items定位 input xpath，可能包含多个定位，需要处理
dosDetectionProfiles_input_packetsSecond_posXpath = "//*[@id='packets_per_sec']"  # packets/second input xpath
dosDetectionProfiles_input_bitsSecond_posXpath = "//*[@id='bits_per_sec']"  # packets/second input xpath
dosDetectionProfiles_input_sessionsSecond_posXpath = "//*[@id='sessions_per_sec']"  # packets/second input xpath
dosDetectionProfiles_div_rightDetails_posXpath = "//div[@class='paper-grid-right']//form/div"  # 右侧详情div容器 xpath
dosDetectionProfiles_alert_topInfo_Xpath = profilePage_alert_topInfo_Xpath  # 页面顶部alert信息
dosDetectionProfiles_button_warningSaveYes_posCss = dnsRecordsProfilePage_button_warningSaveYes_posCss  # 提示保存按钮警告框OK按钮
dosDetectionProfiles_button_warningSaveCancel_posCss = dnsRecordsProfilePage_button_warningSaveCancel_posCss  # 提示保存警告框Cancel按钮
dosDetectionProfiles_button_oK_posCss = "#hijackAddOk1-_detectionProfilesAdd_Home_App_anonymousComponent span"  # OK按钮css
dosDetectionProfiles_button_cancel_posCss = "#hijackAddCancel1-_detectionProfilesAdd_Home_App_anonymousComponent span"  # Cancel按钮
# create_edit_page->侧滑中Audit Logs页面
profilePage_auditLogsPage_firstRowItemSelect_posXpath = "//div[@class='paper-grid-right']//div[@class='right-menu-content']//tbody/tr[1]/td[1]//span/span"  # Audit logs中第一行变更记录的勾选框
dosDetectionProfiles_auditLogsPage_firstRowItemSelect_posXpath = profilePage_auditLogsPage_firstRowItemSelect_posXpath  # Audit logs中第一行变更记录的勾选框
dosDetectionProfiles_auditLogsPage_button_compare_posXpath = "//*[@id='test-compare-_AuditLogs_InfoRightProfile_tsg-html-fixed_detectionProfilesAdd_Home_App_anonymousComponent']"  # compare 按钮
dosDetectionProfiles_auditLogsPage_button_close_posXpath = "//*[@id='interceptionadd_allcancelobject10-_AuditLogs_InfoRightProfile_tsg-html-fixed_detectionProfilesAdd_Home_App_anonymousComponent']"  # compare 按钮
# create_edit_page->侧滑中Audit Logs页面->modification history页面
profilePage_auditLogsPage_modificationPage_tbody_posXpath = "//div[@class='compare-code-box']//tbody"  # modification history页面中内容定位 xpath
dosDetectionProfiles_auditLogsPage_modificationPage_tbody_posXpath = profilePage_auditLogsPage_modificationPage_tbody_posXpath  # modification history页面中内容定位 xpath
dosDetectionProfiles_auditLogsPage_modificationPage_button_close_posXpath = "//*[@id='interceptionadd_allcancelobject10-_AuditLogs_InfoRightProfile_tsg-html-fixed_detectionProfilesAdd_Home_App_anonymousComponent']"  # modification history页面中内容定位 xpath

# Profiles Shaping profiles=============Profiles Shaping profiles===================Profiles Shaping profiles====================Profiles Shaping profiles==================Profiles Shaping profiles
# Shaping Profiles list page  列表页
listPage_profile_shapingProfiles_createButton_posId = "app_create-_OperateBtns_ElRow_Profile_ShapingProfile_Home_App_anonymousComponent"  # create按钮id
listPage_profile_shapingProfiles_editButton_posId = "appEdit-_OperateBtns_ElRow_Profile_ShapingProfile_Home_App_anonymousComponent"  # edit按钮id
listPage_profile_shapingProfiles_delButton_posId = "appDel-_OperateBtns_ElRow_Profile_ShapingProfile_Home_App_anonymousComponent"  # del按钮id
listPage_profile_shapingProfiles_viewButton_posId = "appEdit-_OperateBtns_ElRow_Profile_ShapingProfile_Home_App_anonymousComponent"  # del按钮id
listPage_profile_shapingProfiles_linkButton_posId = "btnCopy-_OperateBtns_ElRow_Profile_ShapingProfile_Home_App_anonymousComponent"  # link按钮id
listPage_profileColumn_shapingProfiles_button_columnAll_posXpath = "//div[@class='all-btn']//label"  # 列选择All按钮
listPage_profileColumn_shapingProfiles_button_columnCancel_posId = "dropColALlFalse-_ElementSet_Profile_ShapingProfile_Home_App_anonymousComponent"  # 列选择Cancel按钮
listPage_profileColumn_shapingProfiles_button_cancel_posId = "dropColcancel-_ElementSet_Profile_ShapingProfile_Home_App_anonymousComponent"  # cancel按钮
listPage_profileColumn_shapingProfiles_button_ok_posId = "dropColOK-_ElementSet_Profile_ShapingProfile_Home_App_anonymousComponent"  # ok按钮
listPage_profileSearch_shapingProfiles_selectLabel_posId = mainPage_profileSearch_selectLabel_posXpath  # 查询框id    定位形式一样
listPage_profileSearch_shapingProfiles_buttonSearch_posId = mainPage_profileSearch_buttonSearch_posXpath  # 查询按钮id       定位形式一样
listPage_profileSearch_shapingProfiles_buttonClear_posId = mainPage_profileSearch_buttonClear_posId  # 清空查询按钮id    定位形式一样
listPage_profileSearch_shapingProfiles_dropDown_item_posXpath = listPage_profileSearch_dnsRecords_dropDown_item_posXpath  # 下拉菜单定位   定位形式一样
listPage_profileSearch_shapingProfiles_input_itemContent_posXpath = listPage_profileSearch_dnsRecords_input_itemContent_posXpath  # 输入item的值，replaceName替换实际查询值    定位形式一样
listPage_profilTable_shapingProfiles_tableTbody_posXpath = listPage_profilTable_dnsRecords_tableTbody_posXpath  # 列表tabel body  xpath   定位形式一样
listPage_profilTable_shapingProfiles_tableHeader_posXpath = listPage_profilTable_dnsRecords_tableHeader_posXpath  # 列表table 表头xpath   定位形式一样
listPage_profilTable_shapingProfiles_EnabledButton_posXpath = "//*[@id='Function-adminStatus']"    # Enabled 列可点击按钮定位 xpath
listPage_profilTable_shapingProfiles_tableHeaderDrops_posXpath = "{}//th//span[text()='Drops']/parent::*//i".format(
    listPage_profilTable_dnsRecords_tableHeader_posXpath)  # 列表table-Drops 表头xpath   定位形式一样
listPage_profilTable_shapingProfiles_tableHeaderAvgMax_posXpath = "{}//th//span[text()='Avg Q/Max Q']/parent::*//i".format(
    listPage_profilTable_dnsRecords_tableHeader_posXpath)  # 列表table-Avg Q/Max Q 表头xpath   定位形式一样
listPage_profileBottomPage_shapingProfiles_button_allSelect_posXpath = mainPage_profileBottomPage_button_allSelect_posXpath  # 底部页面all选择按钮
listPage_profileBottomPageNum_shapingProfiles_posXpath = "//*[@id='pagination-_pagination_Profile_ShapingProfile_Home_App_anonymousComponent']"  # 页面底部翻页 定位
# listPage->Tips dialog  列表页 tips对话框
listPage_dialogTips_shapingProfiles_button_yes_posCss = "body>.el-dialog__wrapper .delComponents-ok span"  # 删除提示的Tips的yes按钮
listPage_dialogTips_shapingProfiles_button_no_posCss = "body>.el-dialog__wrapper .delComponents-close span"  # 删除提示的Tips的close按钮
# listPage-> Link提示对话框
listPage_linkTips_shapingProfiles_button_save_posXpath = "//*[@id='clusterSave-_ClusterTable_ElDialog_copyComponents_Profile_ShapingProfile_Home_App_anonymousComponent']/i"  # 选择cluster后，save行 按钮 xpath
listPage_linkTips_shapingProfiles_button_add_posXpath = "//*[@id='temporary_form-_ClusterTable_ElDialog_copyComponents_Profile_ShapingProfile_Home_App_anonymousComponent']/i"    # 添加 按钮 xpath
listPage_linkTips_shapingProfiles_button_OK_posXpath = "//*[@id='copyOk-_copyComponents_Profile_ShapingProfile_Home_App_anonymousComponent']/span"    # OK 按钮 xpath
# listpage->right-menu-content   列表页 引用计数侧滑box
listPage_rightReferenceDrawer_shapingProfiles_referencedItems = listPage_profileRightReferenceDrawer_referencedItems  # 引用侧滑中被引用对象的选项div容器
# Create Shaping Profile 和 Edit Shaping Profile   新增和编辑页
shapingProfilePage_headerTitle_posXpath = dnsRecordsProfilePage_headerTitle_posXpath   # 页面头部名称 xpath
shapingProfilePage_input_Name_posId = "ShapingProfile_profileName"  # name输入框id
shapingProfilePage_radioButton_generic_posXpath = "//div[@id='shaping_Splitby-_ShapingProfile_write_Home_App_anonymousComponent']//span[normalize-space(text())='Generic']"  # Generic单选按钮Xpath
shapingProfilePage_radioButton_fairShare_posXpath = "//div[@id='shaping_Splitby-_ShapingProfile_write_Home_App_anonymousComponent']//span[normalize-space(text())='Fair Share']"  # Fair Share单选按钮iXpath
shapingProfilePage_radioButton_splitBy_posXpath = "//div[@id='shaping_Splitby-_ShapingProfile_write_Home_App_anonymousComponent']//span[normalize-space(text())='Split By']"  # Split By单选按钮Xpath
shapingProfilePage_radioButton_maxMinHostFairness_posXpath = "//div[@id='shaping_Splitby-_ShapingProfile_write_Home_App_anonymousComponent']//span[normalize-space(text())='Max Min Host Fairness']"  # Max Min Host Fairness单选按钮Xpath
shapingProfilePage_radioButton_localHost_posXpath = "//div[@id='shaping_Splitby-_ShapingProfile_write_Home_App_anonymousComponent']//span[normalize-space(text())='Local Host']"  # Host Fairness单选按钮Xpath
shapingProfilePage_inputSelect_unit_posId = "ShapingProfile-directionValue"  # unit单位输入选择框id
shapingProfilePage_radioButton_unidirectional_posXpath = "//*[@id='vsys0-_ShapingProfile_write_Home_App_anonymousComponent']//span[normalize-space(text())='Unidirectional']"  # Unidirectional单选按钮
shapingProfilePage_radioButton_bidirectional_posXpath = "//*[@id='vsys1-_ShapingProfile_write_Home_App_anonymousComponent']//span[normalize-space(text())='Bidirectional']"  # Bidirectional单选按钮
shapingProfilePage_drowDown_unitItem_posXpath = "//div[contains(@class, 'el-select-dropdown')]//li//span[normalize-space(text())='{replaceName}']"  # unit的下拉item定位,replaceName替换实际查询值
shapingProfilePage_input_incoming_posId = "ShapingProfile-Incoming"  # incoming输入框 id
shapingProfilePage_input_outgoing_posId = "ShapingProfile-Outgoing"  # outgoing输入框 id
shapingProfilePage_input_bidirectional_posId = "ShapingProfile-bidirectional"  # bidirectional输入框 id
shapingProfilePage_button_aqm_posXpath = "//*[@id='ShapingProfile-algorithmValue']/parent::*//span"  # aqm打开关闭定位
shapingProfilePage_inputSelect_aqm_posXpath = "//*[@id='ShapingProfile-algorithm']/parent::*//span"  # Algorith选择框定位
shapingProfilePage_drowDown_aqmItem_posXpath = "//body/div[contains(@class, 'el-select-dropdown')]//*[@class='el-scrollbar']//span[normalize-space(text())='{replaceName}']"  # 下拉菜单选项定位选择框定位
shapingProfilePage_div_rightDetails_posXpath = "//div[@class='paper-right-content']//div[@class='ShapingProfile-box-right']//div[text()='ID']/parent::*/parent::*/div"  # 右侧详情div容器 xpath
shapingProfilePage_div_rightDetails_clearCounter_posXpath = "//*[@id='porfileResetBtn-_anonymousComponent_anonymousComponent_VPanel_VEditPanel_ShapingProfile_write_Home_App_anonymousComponent']/span/span"  # 右侧详情---clear counter元素定位 xpath
shapingProfilePage_clickClearCounter_tipsYes_posXpath = "//body/div[@role='dialog']//*[contains(@class, 'operation-confirm')]"  # 右侧详情---点击 clear counter元素定位后弹出的 tip--yes定位 xpath
shapingProfilePage_hoverClearCounter_tooltip_name_xpath = "//body/div[@role='tooltip']//div[@class='spright-text-name']"        # 右侧详情---悬停 clear counter元素定位后弹出的 --toottip--name定位 xpath
shapingProfilePage_hoverClearCounter_tooltip_value_xpath = "//body/div[@role='tooltip']//div[@class='spright-text-value']"      # 右侧详情---悬停 clear counter元素定位后弹出的 --toottip--value定位 xpath
shapingProfilePage_button_warningSaveYes_posCss = dnsRecordsProfilePage_button_warningSaveYes_posCss  # 提示保存警告框
shapingProfilePage_button_oK_posCss = "#runScriptOk1 span"  # OK按钮css
shapingProfilePage_button_cancel_posCss = "#runScriptCancel1 span"  # Cancel
# create_edit_page->侧滑中Audit Logs页面
shapingProfilePage_auditLogsPage_firstRowItemSelect_posXpath = profilePage_auditLogsPage_firstRowItemSelect_posXpath  # Audit logs中第一行变更记录的勾选框
shapingProfilePage_auditLogsPage_button_compare_posXpath = "//*[@id='test-compare-_AuditLogs_anonymousComponent_VPanel_VEditPanel_ShapingProfile_write_Home_App_anonymousComponent']"  # compare 按钮
shapingProfilePage_auditLogsPage_button_close_posXpath = "//*[@id='interceptionadd_allcancelobject10-_AuditLogs_anonymousComponent_VPanel_VEditPanel_ShapingProfile_write_Home_App_anonymousComponent']"  # compare 按钮
# create_edit_page->侧滑中Audit Logs页面->modification history页面
shapingProfilePage_auditLogsPage_modificationPage_tbody_posXpath = profilePage_auditLogsPage_modificationPage_tbody_posXpath  # modification history页面中内容定位 xpath
shapingProfilePage_auditLogsPage_modificationPage_button_close_posXpath = "//*[@id='interceptionadd_allcancelobject10-_AuditLogs_anonymousComponent_VPanel_VEditPanel_ShapingProfile_write_Home_App_anonymousComponent']"  # modification history页面中内容定位 xpath


#Profiles Service Function Forwarders===================Profiles Service Function Forwarders====================Profiles Service Function Forwarders=================Profiles Service Function Forwarders=======================Profiles Service Function Forwarders
#listPage->Service Function Forwarders list page  列表页
mainPage_secondLevelMenu_serviceFunctionForwarders_posName = "Service Function Forwarders"
mainPage_secondLevelMenu_serviceFunctionForwarders_posXpath = "//div[@class='MuiListItem-root MuiListItem-gutters menu-service-chaining css-1l56wwh']//span[text()='Service Function Forwarders']"
listPage_profile_serviceFunctionForwarders_createButton_posXpath = "//div[@class='flex justify-start items-center mr-[20px]']//span[text()='Create']"     #create按钮
listPage_profile_serviceFunctionForwarders_editButton_posId = "appEdit-_OperateBtns_ElRow_Profile_Forwarders_Home_App_anonymousComponent"          #edit按钮id
listPage_profile_serviceFunctionForwarders_delButton_posXpath = "//div[@class='flex justify-start items-center mr-[20px]']//span[text()='Delete']"          #del按钮id
listPage_profile_serviceFunctionForwarders_viewButton_posId = "appEdit-_OperateBtns_ElRow_Profile_Forwarders_Home_App_anonymousComponent"          #view按钮id
listPage_profileColumn_serviceFunctionForwarders_button_columnAll_posId = "dropColAll-_ElementSet_Profile_Forwarders_Home_App_anonymousComponent"  #列选择All按钮
listPage_profileColumn_serviceFunctionForwarders_button_columnCancel_posId = "dropColALlFalse-_ElementSet_Profile_Forwarders_Home_App_anonymousComponent"  #列选择Cancel按钮
listPage_profileColumn_serviceFunctionForwarders_button_cancel_posId = "dropColcancel-_ElementSet_Profile_Forwarders_Home_App_anonymousComponent"  #cancel按钮
listPage_profileColumn_serviceFunctionForwarders_button_ok_posId = "dropColOK-_ElementSet_Profile_Forwarders_Home_App_anonymousComponent"  #ok按钮
listPage_profileSearch_serviceFunctionForwarders_selectLabel_posXpath = "//div[@class='MuiPaper-root MuiPaper-elevation MuiPaper-rounded MuiPaper-elevation1 dune-ui-page relative service-function-forwarder-page dune-container-table css-1823oea']//input"
listPage_profileSearch_serviceFunctionForwarders_buttonSearch_posId = mainPage_profileSearch_buttonSearch_posXpath    #查询按钮id       定位形式一样
listPage_profileSearch_serviceFunctionForwarders_buttonClear_posId = mainPage_profileSearch_buttonClear_posId       #清空查询按钮id    定位形式一样
listPage_profileSearch_serviceFunctionForwarders_searchName_posId = "2-_FilteredSearch_ElRow_Profile_Forwarders_Home_App_anonymousComponent"
listPage_profileSearch_serviceFunctionForwarders_dropDown_item_posXpath = "//ul[@class='base-Popper-root MuiAutocomplete-listbox css-18r31z0']//span"
listPage_profileSearch_serviceFunctionForwarders_input_itemContent_posXpath = "//div[@class='base-Popper-root']//input"   #输入item的值，replaceName替换实际查询值    定位形式一样
listPage_profilTable_serviceFunctionForwarders_tableTbody_posXpath = listPage_profilTable_dnsRecords_tableTbody_posXpath   #列表tabel body  xpath   定位形式一样
listPage_profilTable_serviceFunctionForwarders_tableHeader_posXpath = listPage_profilTable_dnsRecords_tableHeader_posXpath    #列表table 表头xpath   定位形式一样
listPage_profileBottomPage_serviceFunctionForwarders_button_allSelect_posXpath = mainPage_profileBottomPage_button_allSelect_posXpath     # 底部页面all选择按钮
listPage_profileBottomPageNum_serviceFunctionForwarders_posXpath = "//*[@id='pagination-_pagination_Profile_Forwarders_Home_App_anonymousComponent']"    # 页面底部翻页 定位
#listPage->Tips dialog  列表页 tips对话框
listPage_dialogTips_serviceFunctionForwarders_button_yes_posCss = "//button[@class='el-button delComponents-ok role-disconnect-btn el-button--default el-button--small']"   #删除提示的Tips的yes按钮
listPage_dialogTips_serviceFunctionForwarders_button_no_posCss = listPage_dialogTips_dnsRecords_button_no_posXpath   #删除提示的Tips的close按钮
#listpage->right-menu-content   列表页 引用计数侧滑box
listPage_rightReferenceDrawer_serviceFunctionForwarders_referencedItems = listPage_profileRightReferenceDrawer_referencedItems      # 引用侧滑中被引用对象的选项div容器
#Create Service Function Forwarders page 和 Edit Service Function Forwarders   新增和编辑页
serviceFunctionForwarders_input_Name_posXpath = "//label[text()='Name']/parent::div[@class='MuiFormControl-root MuiFormControl-horizontal MuiFormControl-sizeMd css-90yvhw']//input"    # name输入框
#//*[@class='content-box']//*[normalize-space(text())='Failure Action']/parent::*//span[normalize-space(text())='Re-dispatch']
serviceFunctionForwarders_radio_labelAndRadioName_posXpath = "//label[text()='{replaceLabel}']/ancestor::div[@class='MuiFormControl-root MuiFormControl-horizontal MuiFormControl-sizeMd css-90yvhw']//button[text()='{replaceRadioName}']"         # 单选按钮 xpath  二次处理  replaceLabel=标签名称  replaceRadioName=按钮名称
serviceFunctionForwarders_radio_unavailabilityAction_posXpath = serviceFunctionForwarders_radio_labelAndRadioName_posXpath        # 单选按钮 xpath  二次处理  replaceLabel=标签名称  replaceRadioName=按钮名称
serviceFunctionForwarders_input_minHealthServiceFunctions_posXpath = "//label[text()='Minimum Health Service Functions']/parent::div[@class='MuiFormControl-root MuiFormControl-horizontal MuiFormControl-sizeMd css-90yvhw']//input"         # Minimum Health Service Functions 输入框 xpath
serviceFunctionForwarders_button_serviceFunctionsAdd_posXpath = "//label[text()='Service Functions']/parent::div[@class='MuiFormControl-root MuiFormControl-horizontal MuiFormControl-sizeMd css-90yvhw']//i"         #  Service Functions 添加 xpath
serviceFunctionForwarders_rightDrawer_input_sfDrawerSearch_posXpath = "//div[@class='px-[12px] py-[4px] flex']//input"         #  sf侧滑 搜索框 xpath
serviceFunctionForwarders_rightDrawer_li_sfDrawerFirerRowItem_posXpath = "//div[@class='px-[12px]  pb-[40px] overflow-hidden']//div[text()='{replaceName}']"         #  sf搜索框第一条数据 xpath
serviceFunctionForwarders_rightDrawer_button_sfDrawerClose_posXpath = "//div[@class='absolute bottom-0 h-[40px] w-[100%] overflow-hidden text-[16px] truncate bg-[--color-background-secondary] flex  justify-center items-center pl-[12px] pr-[38px]']//button"         #  sf侧滑 close按钮 xpath
serviceFunctionForwarders_div_rightDetails_posXpath = "//div[@class='paper-right-content']//div[@class='ShapingProfile-box-right']/div[1]/div"            # enable 开关 xpath
serviceFunctionForwarders_button_warningSaveYes_posCss = dnsRecordsProfilePage_button_warningSaveYes_posCss    #提示保存按钮警告框OK按钮
serviceFunctionForwarders_button_warningSaveCancel_posCss = dnsRecordsProfilePage_button_warningSaveCancel_posCss    #提示保存警告框Cancel按钮
serviceFunctionForwarders_alert_topInfo_Xpath = profilePage_alert_topInfo_Xpath      # 顶部提示信息alert框
serviceFunctionForwarders_button_oK_posXpath = "//div[@class='form-action bg-[--color-background] flex justify-center py-[12px] absolute bottom-0 w-full']//button[text()='OK']"     #OK按钮
serviceFunctionForwarders_button_cancel_posCss = "#runScriptCancel1 span"      #Cancel按钮
serviceFunctionForwarders_button_leaveOK_posXpath = "//div[@role='dialog']//button[contains(@class, 'operation-confirm-Leave')]"      #Cancel按钮

# Profiles Service Functions===================Profiles Service Functions====================Profiles Service Functions=================Profiles Service Functions=======================Profiles Service Functions
mainPage_secondLevelMenu_serviceFunctions_posName = "Service Functions"
mainPage_secondLevelMenu_serviceFunctions_posXpath = "//div[@class='MuiListItem-root MuiListItem-gutters menu-service-chaining css-1l56wwh']//span[text()='Service Functions']"
listPage_profileBottomPage_serviceFunctions_button_allSelect_posXpath = "//div[@class='flex flex-row flex-wrap justify-start items-center pl-[18px] mt-[20px]']//span[@class='MuiCheckbox-action css-kit57i']"
listPage_profile_serviceFunctions_createButton_posXpath = "//div[@class='flex justify-start items-center mr-[20px]']//span[text()='Create']"  
listPage_profile_serviceFunctions_editButton_posXpath = "//div[@class='flex justify-start items-center mr-[20px]']//span[text()='Edit']"
listPage_profile_serviceFunctions_delButton_posXpath = "//div[@class='flex justify-start items-center mr-[20px]']//span[text()='Delete']"  # del按钮id
listPage_profile_serviceFunctions_linkButton_posId = "btnCopy-_OperateBtns_ElRow_Profile_Functions_Home_App_anonymousComponent"  # link按钮id
listPage_profileColumn_serviceFunctions_button_columnAll_posXpath = "//div[@class='MuiDataGrid-columnsManagementFooter css-1l93brk']//span[@class='MuiCheckbox-checkbox MuiCheckbox-indeterminate css-28xynh']"  # 列选择Xpath按钮   列选择all按钮
listPage_profileColumn_serviceFunctions_button_columnCancel_posXpath = listPage_profileColumn_serviceFunctions_button_columnAll_posXpath
listPage_profileColumn_serviceFunctions_button_cancel_posId = "dropColcancel-_ElementSet_Profile_Functions_Home_App_anonymousComponent"  # cancel按钮
listPage_profileColumn_serviceFunctions_button_ok_posId = "dropColOK-_ElementSet_Profile_Functions_Home_App_anonymousComponent"  # ok按钮
listPage_profileSearch_serviceFunctions_selectLabel_posXpath = "//span[@class='action-search inline-flex mr-[8px] flex-1']//input"
listPage_profileSearch_serviceFunctions_buttonSearch_posXpath = "//button[@class='MuiButtonBase-root MuiButton-root MuiButton-text MuiButton-textPrimary MuiButton-sizeSmall MuiButton-textSizeSmall MuiButton-colorPrimary MuiButton-root MuiButton-text MuiButton-textPrimary MuiButton-sizeSmall MuiButton-textSizeSmall MuiButton-colorPrimary css-1afa66w']"
listPage_profileSearch_serviceFunctions_buttonClear_posId = mainPage_profileSearch_buttonClear_posId  # 清空查询按钮id    定位形式一样
listPage_profileSearch_serviceFunctions_dropDown_item_posXpath = listPage_profileSearch_serviceFunctionForwarders_dropDown_item_posXpath
listPage_profileSearch_serviceFunctions_input_itemContent_posXpath = listPage_profileSearch_serviceFunctionForwarders_input_itemContent_posXpath  # 输入item的值，replaceName替换实际查询值    定位形式一样
listPage_profilTable_serviceFunctions_tableTbody_posXpath = listPage_profilTable_dnsRecords_tableTbody_posXpath  # 列表tabel body  xpath   定位形式一样
listPage_profilTable_serviceFunctions_tableHeader_posXpath = listPage_profilTable_dnsRecords_tableHeader_posXpath  # 列表table 表头xpath   定位形式一样
# listPage->Tips dialog  列表页 tips对话框
listPage_dialogTips_serviceFunctions_button_yes_posCss = listPage_dialogTips_dnsRecords_button_yes_posXpath  # 删除提示的Tips的yes按钮
listPage_dialogTips_serviceFunctions_button_no_posCss = listPage_dialogTips_dnsRecords_button_no_posXpath  # 删除提示的Tips的close按钮
# listPage-> Link提示对话框
listPage_linkTips_serviceFunctions_button_save_posXpath = "//*[@id='clusterSave-_ClusterTable_ElDialog_copyComponents_Profile_Functions_Home_App_anonymousComponent']/i"  # 选择cluster后，save行 按钮 xpath
listPage_linkTips_serviceFunctions_button_add_posXpath = "//*[@id='temporary_form-_ClusterTable_ElDialog_copyComponents_Profile_Functions_Home_App_anonymousComponent']/i"    # 添加 按钮 xpath
listPage_linkTips_serviceFunctions_button_OK_posXpath = "//*[@id='copyOk-_copyComponents_Profile_Functions_Home_App_anonymousComponent']/span"    # OK 按钮 xpath
# listpage->right-menu-content   列表页 引用计数侧滑box
listPage_rightReferenceDrawer_serviceFunctions_referencedItems = listPage_profileRightReferenceDrawer_referencedItems  # 引用侧滑中被引用对象的选项div容器
# Create Service Functions page 和 Edit Service Functions   新增和编辑页
serviceFunctions_headerTitle_posXpath = dnsRecordsProfilePage_headerTitle_posXpath   # 页面头部名称 xpath
serviceFunctions_input_Name_posXpath = "//div[@class='service-function-name']//input"  
serviceFunctions_button_deviceGroupAdd_posXpath = "//label[text()='Device Tag']/ancestor::div[@class='MuiFormControl-root MuiFormControl-horizontal MuiFormControl-sizeMd css-90yvhw']//i"  # device group 添加按钮 xpath
# //*[contains(@class, 'drawer-box')]//*[@class='title' and contains(normalize-space(text()), 'Select Device Group')]/parent::*//span[normalize-space(text())='City A']/parent::*//input//parent::*
serviceFunctions_radio_selectDeviceType_posXpath = "//div[@class='bg-default mb-[4px]']//button[text()='{deviceType}']"  #deviceType替换为Group/Center
serviceFunctions_searchDevice_input_Name_posXpath = "//div[@class='px-[12px] py-[4px] flex']//input"
serviceFunctions_radio_selectDevice_posXpath = "//div[@class='px-[12px]  pb-[40px] overflow-hidden']//li[1]//i"
serviceFunctions_button_closeSidePage_Cancel_posXpath = "//div[@class='absolute bottom-0 h-[40px] w-[100%] overflow-hidden text-[16px] truncate bg-[--color-background-secondary] flex  justify-center items-center pl-[12px] pr-[38px]']//button[text()='Cancel']"  # effective devices 侧滑中Cancel按钮 xpath
serviceFunctions_radio_connectivityLayer2Switch_posXpath = "//label[text()='Type']/ancestor::div[@class='MuiFormControl-root MuiFormControl-horizontal MuiFormControl-sizeMd css-90yvhw']//button[text()='Layer 2 Switch']"  # Layer 2 Switch 单选按钮 xpath
serviceFunctions_radio_connectivityXvlan_posXpath = "//label[text()='Type']/ancestor::div[@class='MuiFormControl-root MuiFormControl-horizontal MuiFormControl-sizeMd css-90yvhw']//button[text()='VXLAN-G']"  # Function-internal 单选按钮 xpath
serviceFunctions_input_internalVlan_posXpath = "//label[text()='Internal VLAN Tag']/ancestor::div[@class='MuiFormControl-root MuiFormControl-horizontal MuiFormControl-sizeMd css-90yvhw']//input"  # Internal VLAN Tag 输入框 xpath
serviceFunctions_input_externalVlan_posXpath = "//label[text()='External VLAN Tag']/ancestor::div[@class='MuiFormControl-root MuiFormControl-horizontal MuiFormControl-sizeMd css-90yvhw']//input"  # external VLAN Tag 输入框 xpath
serviceFunctions_input_destinationIpAddress_posXpath = "//label[text()='Destination IP Address']/ancestor::div[@class='MuiFormControl-root MuiFormControl-horizontal MuiFormControl-sizeMd css-90yvhw']//input"  # destination Ip Address 输入框 xpath
serviceFunctions_radio_healthCheck_posXpath = "//div[@class='service-function-checkMethod']//button[text()='{type}']"  # health Check 单选按钮 xpath   replaceIndex需要二次处理
serviceFunctions_input_interval_posXpath = "//label[text()='Internal VLAN Tag']/ancestor::div[@class='MuiFormControl-root MuiFormControl-horizontal MuiFormControl-sizeMd css-90yvhw']//input"  # interval 输入框 xpath
serviceFunctions_input_retries_posXpath = "//label[text()='External VLAN Tag']/ancestor::div[@class='MuiFormControl-root MuiFormControl-horizontal MuiFormControl-sizeMd css-90yvhw']//input"  # retires 输入框 xpath
serviceFunctions_switch_enalbe_posXpath = "//label[text()='Enable']/ancestor::div[@class='MuiFormControl-root MuiFormControl-horizontal MuiFormControl-sizeMd css-90yvhw']//span"  # enable 开关 xpath
serviceFunctions_div_rightDetails_posXpath = "//div[@class='paper-right-content']//div[@class='Function-box-right']/div"    
serviceFunctions_div_rightDetails_clearCounter_posXpath = "//*[@id='porfileResetBtn-_anonymousComponent_anonymousComponent_VPanel_VEditPanel_Profile_Functions_edit_Home_App_anonymousComponent']/span/span"  # 右侧详情---clear counter元素定位 xpath
serviceFunctions_button_warningSaveYes_posCss = dnsRecordsProfilePage_button_warningSaveYes_posCss  # 提示保存按钮警告框OK按钮
serviceFunctions_button_warningSaveCancel_posCss = dnsRecordsProfilePage_button_warningSaveCancel_posCss  # 提示保存警告框Cancel按钮
serviceFunctions_alert_topInfo_Xpath = profilePage_alert_topInfo_Xpath  # 顶部提示信息alert框
serviceFunctions_button_oK_posXpath = "//div[@class='form-action bg-[--color-background] flex justify-center py-[12px] absolute bottom-0 w-full']//button[text()='OK']"  # OK按钮
serviceFunctions_button_cancel_posXpath = "//div[@class='form-action bg-[--color-background] flex justify-center py-[12px] absolute bottom-0 w-full']//button[text()='Cancel']"  # Cancel按钮
# create_edit_page->侧滑中Audit Logs页面
serviceFunctions_auditLogsPage_firstRowItemSelect_posXpath = profilePage_auditLogsPage_firstRowItemSelect_posXpath  # Audit logs中第一行变更记录的勾选框
serviceFunctions_auditLogsPage_button_compare_posXpath = "//*[@id='test-compare-_AuditLogs_anonymousComponent_VPanel_VEditPanel_Profile_Functions_edit_Home_App_anonymousComponent']"  # compare 按钮
# create_edit_page->侧滑中Audit Logs页面->modification history页面
serviceFunctions_auditLogsPage_modificationPage_tbody_posXpath = profilePage_auditLogsPage_modificationPage_tbody_posXpath  # modification history页面中内容定位 xpath
serviceFunctions_auditLogsPage_modificationPage_button_close_posXpath = "//*[@id='interceptionadd_allcancelobject10-_AuditLogs_anonymousComponent_VPanel_VEditPanel_Profile_Functions_edit_Home_App_anonymousComponent']"  # modification history页面中内容定位 xpath

# Profiles statistics templates===================Profiles statistics templates====================Profiles statistics templates=================Profiles statistics templates=======================Profiles statistics templates
# listPage->tsg dos detection profiles list page  列表页
listPage_profileHandleButton_posXpath = "//i[@class='iconfont icon-{replaceName}']/parent::*/parent::*" #"//span[@class='text-[14px] inline-block max-w-[50px] normal-case'][normalize-space(text())='{replaceName}']"
listPage_profile_statisticsTemplates_createButton_name = "Create" #"app_create-_OperateBtns_ElRow_Statistic_Template_Home_App_anonymousComponent"     #create按钮id
listPage_profile_statisticsTemplates_editButton_name = "Editinpage" #"appEdit-_OperateBtns_ElRow_Statistic_Template_Home_App_anonymousComponent"          #edit按钮id
listPage_profile_statisticsTemplates_delButton_name = "Delete" #"appDel-_OperateBtns_ElRow_Statistic_Template_Home_App_anonymousComponent"          #del按钮id
listPage_profileSearch_statisticsTemplates_selectLabel_posXpath = mainPage_profileSearch_selectLabel_posXpath     #查询框id    定位形式一样
listPage_profileSearch_statisticsTemplates_buttonSearch_posId = mainPage_profileSearch_buttonSearch_posXpath    #查询按钮id       定位形式一样
listPage_profileSearch_statisticsTemplates_buttonClear_posId = mainPage_profileSearch_buttonClear_posId       #清空查询按钮id    定位形式一样
listPage_profileSearch_statisticsTemplates_dropDown_item_posXpath = "//ul[@role='listbox']//li//div//span[normalize-space(text())='{replaceValue}']/.."   #下拉菜单定位   定位形式一样
listPage_profileSearch_statisticsTemplates_input_itemContent_posXpath = listPage_profileSearch_dnsRecords_input_itemContent_posXpath   #输入item的值，replaceName替换实际查询值    定位形式一样
listPage_profilTable_statisticsTemplates_tableTbody_posXpath = "//*[@class='MuiDataGrid-virtualScrollerRenderZone css-1inm7gi']"   #列表tabel body  xpath   定位形式一样
listPage_profilTable_statisticsTemplates_tableHeader_posXpath = listPage_profilTable_dnsRecords_tableHeader_posXpath    #列表table 表头xpath   定位形式一样
#listPage->Tips dialog  列表页 tips对话框
listPage_profile_delete_dialogTips_button_yes_posXpath = "//div[@class='MuiDialogActions-root flex !justify-center items-center MuiDialogActions-spacing css-vplbg4']//button[@type='danger']" #profile列表删除提示的Tips的yes按钮
listPage_profile_delete_dialogTips_button_no_posXpath = "//div[@class='MuiDialogActions-root flex !justify-center items-center MuiDialogActions-spacing css-vplbg4']//button[@type='button']" #profile列表删除提示的Tips的yes按钮
listPage_dialogTips_statisticsTemplates_button_yes_posXpath = listPage_profile_delete_dialogTips_button_yes_posXpath   #删除提示的Tips的yes按钮
listPage_dialogTips_statisticsTemplates_button_no_posXpath = listPage_profile_delete_dialogTips_button_no_posXpath   #删除提示的Tips的close按钮
#Create statistics templates page 和 Edit statistics templates page   新增和编辑页
statisticsTemplates_input_Name_posId = "advancedAdd_policyName"    # name输入框id
statisticsTemplates_input_Name_posXpath = "//input[@class='MuiInput-input css-fqt4w4']" # name输入框xpath
#Metrics 选择列表：//ul[@class='base-Popper-root MuiAutocomplate-listbox css-1m20s0g'][contains(@style,'position: absolute')]
# metrics field行：//form[1]//div[@class='timeDimension MuiBox-root css-0']//div[@class='MuiStack-root css-fhxiwe']
# Metrics field行的每个Input：//div[contains(@class,'MuiBox-root css-1ozlgi5')]
# metrics field行对应的删除按钮：/button
# metrics Funcation input：
# # metrics Funcation选择列表：//ul[@class='base-Popper-root MuiSelect-listbox Mui-expanded css-1bxrsif'][contains(@style,'position: absolute')]/li[contains(@class, 'MuiOption-root')]
# Dimensions，每行：//form[1]//div[@class='DimentionList MuiBox-root css-0']//div[@class='MuiStack-root css-fhxiwe']
# Dimensions，每行的每个input：//div[contains(@class,'MuiBox-root css-1ozlgi5')]
# Dimensions field选择列表、Order By选择列表：//ul[@class='base-Popper-root MuiSelect-listbox Mui-expanded css-1bxrsif'][contains(@style,'position: absolute')]/li[contains(@class, 'MuiOption-root')]
# Order By、Row Limit/Series Limit Input://form[1]//label[normalize-space(text())='Series Limit']/parent::*//input
#Minimum Coming/Outgoing size Input ://form[2]//div[normalize-space(text())='Minimum Incoming size']/parent::*//input
# Chart OK/Cancel按钮：//form[2]//div[@class='text-center MuiBox-root css-0']/button[1/2]
statisticsTemplates_input_metricsAndDimensionsSelect_posXpath = "//form[{replaceChart}]//div[@class='{repalceLabel}List MuiBox-root css-0']//div[@class='MuiStack-root css-fhxiwe']"#MetricList/DimentionList MuiBox-root css-0#"//form[{replaceChart}]//div[@class='timeDimension {repalceLabel}MuiBox-root css-0']//div[@class='MuiStack-root css-fhxiwe']"#timeDimension
#"//form[contains(@class, 'ly-addform1')]/div[contains(@class, 'template-edit-chart')][{replaceChart}]//label[normalize-space(text())='{repalceLabel}']/parent::*//div[contains(@class,'margin-top-2')]/div[@class='el-row']"  # Metrics输入框的定位，可能包含多个。replaceChart repalceLabel需要二次处理
# statisticsTemplates_button_metricsAndDimensionsAdd_posXpath = "//form[contains(@class, 'ly-addform1')]/div[contains(@class, 'template-edit-chart')][{replaceChart}]//label[normalize-space(text())='{repalceLabel}']/parent::*//div[contains(@class, 'addCondition')]"    # Metrics的add添加按钮。replaceChart repalceLabel 需要二次处理
statisticsTemplates_button_metricsAndDimensionsAdd_posXpath = "//form[{replaceChart}]//div[contains(@class,'MuiBox-root css-0')]/div/label[normalize-space(text())='{repalceLabel}']/parent::*/button"
#"//form[contains(@class, 'ly-addform1')]/div[contains(@class, 'template-edit-chart')][{replaceChart}]//label[normalize-space(text())='{repalceLabel}']/parent::*//div[contains(@class, 'addCondition')]"  # Metrics的add添加按钮。replaceChart repalceLabel 需要二次处理
statisticsTemplates_radio_visualizationType_posXpath = "//form[{replaceChart}]//label[normalize-space(text())='{repalceLabel}']/parent::*//span[@class='MuiBox-root css-10rvbm3'][normalize-space(text())='{replaceType}']/parent::*/parent::*/parent::*"
#"//form[contains(@class, 'ly-addform1')]/div[contains(@class, 'template-edit-chart')][{replaceChart}]//label[normalize-space(text())='{repalceLabel}']/parent::*//span[normalize-space(text())='{replaceType}']/parent::*/span[contains(@class, 'el-radio__input')]"  # Visualization Type 单选按钮按钮。replaceChart repalceLabel replaceType 需要二次处理
#tatisticsTemplates_radio_visualizationType_posXpath = "//label[normalize-space(text())='{replaceChart}']/parent::*//label[normalize-space(text())='{repalceLabel}']/parent::*//span[normalize-space(text())='{replaceType}']/parent::*/span[contains(@class, 'el-radio__input')]"    # Visualization Type 单选按钮按钮。replaceChart repalceLabel replaceType 需要二次处理
statisticsTemplates_radio_sampling_posXpath = "//form[contains(@class, 'ly-addform1')]/div[contains(@class, 'template-edit-chart')][{replaceChart}]//label[normalize-space(text())='{repalceLabel}']/parent::*//span[normalize-space(text())='{replaceSampling}']"  # sampling 单选按钮按钮。replaceName需要二次处理
statisticsTemplates_input_other_posXpath = "//form[{replaceChart}]//label[normalize-space(text())='{repalceLabel}']/parent::*//input"
statisticsTemplates_input_thresholds_posXpath = "//form[{replaceChart}]//div[normalize-space(text())='{repalceLabel}']/parent::*//input[@name='{replaceName}']"
#//form[1]//label[normalize-space(text())='Thresholds']/parent::*//input[@name='threshold.in_bytes']
statisticsTemplates_button_other_posXpath = "//form[{replaceChart}]//label[normalize-space(text())='{repalceLabel}']/parent::*//button"
#"//form[contains(@class, 'ly-addform1')]/div[contains(@class, 'template-edit-chart')][{replaceChart}]//span[normalize-space(text())='{repalceLabel}']/parent::*//input"  # 其它的输入框和下拉输入框 。replaceName需要二次处理
statisticsTemplates_input_posXpath = "//form[contains(@class, 'ly-addform1')]/div[contains(@class, 'template-edit-chart')][{replaceChart}]//label[normalize-space(text())='{repalceLabel}']/parent::*//input"  # 其它的输入框和下拉输入框 。replaceName需要二次处理
statisticsTemplates_LabelName_posXpath = "//form[contains(@class, 'ly-addform1')]/div[contains(@class, 'template-edit-chart')]//*[normalize-space(text())='{repalceLabel}']"
statisticsTemplates_dropdownMetrics_posXpath = "//ul[contains(@class,'base-Popper-root MuiAutocomplete-listbox')]//li[contains(@class,'MuiAutocomplete-option')][normalize-space(text())='{replaceDropdownIterm}']"#//li[contains(@class,'MuiAutocomplete-option')][normalize-space(text())='{replaceDropdownIterm}']
statisticsTemplates_dropdown_posXpath = "//ul[contains(@class,'base-Popper-root MuiSelect-listbox')][contains(@style,'position: absolute')]//li[normalize-space(text())='{replaceDropdownIterm}']"
#"//form[contains(@class, 'ly-addform1')]/div[contains(@class, 'template-edit-chart')][{replaceChart}]//label[normalize-space(text())='{repalceLabel}']/parent::*//div[contains(@class, 'el-popper')]//span[normalize-space(text())='{replaceDropdownIterm}']"  # 所有的下拉列表中内容定位 。replaceDropdownIterm 二次处理
statisticsTemplates_button_chartAdd_posXpath = "//div[@class='ChartList MuiBox-root css-0']"#"//*[contains(@class, 'add_widget')]"  # 添加图标按钮 xpath
statisticsTemplates_button_chartEdit_posXpath = "//form[contains(@class, 'ly-addform1')]/div[contains(@class, 'template-edit-chart')][{replaceChart}]//div[@class='operateIcon']//i[contains(@class, 'icon-Edit')]"  # 编辑图标按钮 xpath
statisticsTemplates_metrics_dropdown_item_posXpath = "//ul[contains(@class, 'base-Popper-root MuiAutocomplate-listbox')]"#[contains(@style,'position: absolute;')]//li[normalize-space(text())='{replaceMetricsField}']"
    #"//div[@class='el-select-dropdown el-popper is-multiple'][contains(@style,'position: absolute;')]//li/span[normalize-space(text())='{}']" #24.08版本，Metrics item定位#[not(contains(@style,'display: none;'))]
statisticsTemplates_metrics_function_dropdown_item_posXpath = "//ul[contains(@class, 'base-Popper-root MuiSelect-listbox')][contains(@style,'position: absolute;')]//*[normalize-space(text())='{}']"
statisticsTemplates_dimensions_dropdown_item_posXpath = "//ul[contains(@class, 'base-Popper-root MuiSelect-listbox')][contains(@style,'position: absolute')]//li[normalize-space(text())='{}']"
#"//div[@class='Dimension margin-top-2']//div[@class='el-select-dropdown el-popper'][contains(@style,'position: absolute;')]//li/span[normalize-space(text())='{}']" #24.08版本，Dimensions item定位
statisticsTemplates_div_paperGrid_posXpath = "//div[@class=' statistics-template-page MuiBox-root css-o7xelj']"#"//*[@id='proxyTCP']/div[contains(@class, 'paper-grid')]"    # div的包含滚动条的长页面 xpath
statisticsTemplates_div_rightDetails_posXpath = "//div[@id='router-view-container']//div[@class='paper-grid-right']//form/div"  # 右侧详情div容器 xpath
statisticsTemplates_button_warningSaveYes_posCss = dnsRecordsProfilePage_button_warningSaveYes_posCss    #提示保存按钮警告框OK按钮
statisticsTemplates_button_warningSaveCancel_posCss = dnsRecordsProfilePage_button_warningSaveCancel_posCss    #提示保存警告框Cancel按钮
statisticsTemplates_button_chartSubmit_posXpath = "//form[{replaceChart}]//div[@class='text-center MuiBox-root css-0']/button[1]"  # 保存chart的OK按钮 xpath定位
statisticsTemplates_button_chartCancel_posXpath = "//form[{replaceChart}]//div[@class='text-center MuiBox-root css-0']/button[2]"  # 保存chart的OK按钮 xpath定位
statisticsTemplates_button_oK_posXpath = "//div[@class='form-action bg-[--color-background] flex justify-center py-[12px] absolute bottom-0 w-full']//button[1]"     #OK按钮css
statisticsTemplates_button_cancel_posXpath = "//div[@class='form-action bg-[--color-background] flex justify-center py-[12px] absolute bottom-0 w-full']//button[2]"      #Cancel按钮
statisticsTemplates_charts_posXpath = "//div[@class='el-form-item template-edit-chart el-form-item--small']"#"//form[@class='el-form el-form--label-top']" # 编辑页码获取所有Chart Name所在Chart
statisticsTemplates_label_chart_name_posXpath = ".//label[@for='name']/..//div[normalize-space(text())='{repalceLabel}']" # 编辑页码Chart Name定位Chart
statisticsTemplates_button_chart_edit_posXpath = ".//div[@class='operateIcon']/i[contains(@class,'icon-Edit')]" # chart编辑按钮
statisticsTemplates_button_chart_delete_posXpath = ".//div[@class='operateIcon']/i[contains(@class,'icon-Delete')]" # chart删除按钮
statisticsTemplates_alert_unSaveChart_posXpath = "//div[@class='MuiAlert-message css-1xsto0d']" # Chart未保存提示