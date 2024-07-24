mainPage_navigationBar_logo_posCss = ".tsg-img-logo"
mainPage_policyFirstLevelMenu_posId = "policy"  # 一级菜单Policies
mainPage_policySecondLevelMenu_security_posId = "Objects_ProxyInterception"
mainPage_policySecondLevelMenu_intercept_posId = "policy_Intercept"  # 二级菜单intercept
mainPage_policySecondLevelMenu_manipulation_posId = "policy_Manipulation"  # 二级菜单manipulatjion
mainPage_policySecondLevelMenu_shaping_posId = "policy_trafficShaping"  # 二级菜单Shaping
mainPage_policySecondLevelMenu_statistics_posId = "policy_statistics"  # 二级菜单Statistics

mainPage_button_menu_posXCss = ".menu-btn span"
mainPage_currentPage_vsysName_posXpath = "//span[@class='root-title']" 
mainPage_vsysTree_vsysName_posXpath = "//div[contains(@class, 'menu-level2')]//div[@class='VsysTree']/ul//li"    # vsys tree中vsys name定位
mainPage_version_posXpath = "//*[@class='header-user-con']/span[1]" #TSG Version按钮
language_button_posXpath = "//input[@id='anonymousComponent_Home_App_anonymousComponent_language']/.."#快捷切换语言按钮
policyRulePage_addSrcIP_posXpath = "//div[@class='MultipleSelect SourceModuleSelect']//i[@class='iconfont icon-Create1 cursor']"
policyRulePage_searchSrcIP_posXpath = "//div[@class='SourceList list-box']//div[contains(@class, 'object-item-seach')]//input"
policyRulePage_selectSrcIP_posXpath = "//div[@class='SourceList list-box']//span[normalize-space(text())='{replaceValue}']"
policyRulePage_closeSrcIP_posXpath = "//div[@class='SourceList list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"

policyRulePage_addDstIP_posXpath = "//div[@class='MultipleSelect DestinationsModuleSelect']//i[@class='iconfont icon-Create1 cursor']"
policyRulePage_searchDstIP_posXpath = "//div[@class='destinations list-box']//input[contains(@id, 'object_ip_search')]"
policyRulePage_selectDstIP_posXpath = "//div[@class='CommonListDetail list-detail']//span[normalize-space(text())='{replaceValue}']"
policyRulePage_closeDstIP_posXpath = "//div[@class='destinations list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"

policyRulePage_addSrcPort_posXpath = "//div[@zs-label='Source']//p[normalize-space(text())='Port']/ancestor::div[@zs-label='SourceItem']//i[@class='iconfont icon-Create1 cursor']"
policyRulePage_searchSrcPort_posXpath = "//div[@class='SourceList list-box']//input[@id='object_ip_search']"
policyRulePage_selectSrcPort_posXpath = "//div[@class='reference-box el-popover__reference']//span[normalize-space(text())='{replaceValue}']"
policyRulePage_closeSrcPort_posXpath = "//div[@class='SourceList list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"

policyRulePage_addApplication_posXpath = "//div[@class='MultipleSelect AppSelect']//i[@class='iconfont icon-Create1 cursor']"
policyRulePage_searchApplication_posXpath = "//div[@class='AppList list-box']//input[@id='object_ip_search']"
policyRulePage_selectApplication_posXpath = '//div[@class="LocalationDraswer lstsub policy-right-show-edit v-draswer"]//li[1]//div[@class="row-content-cell"]'
policyRulePage_closeApplication_posXpath = "//div[@class='ToggleDraw']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"
policyRulePage_selectApplicationLabel_posXpath = "//div[@class='el-tabs__nav is-top']//div[normalize-space(text())='Application']"
policyRulePage_selectApplicationGroupLabel_posXpath = "//div[normalize-space(text())='Group']"
policyRulePage_little_button_addApplication_posId = "policy_app_create-_AppSelect_ElFormItem_ElForm_VPanel_VEditPanel_policy_monitor_write_Home_App_anonymousComponent"

policyRulePage_addInternalIP_posXpath = "//div[@zs-label='Internal']//div[@class='MultipleSelect InternalsSelect']//i[@class='iconfont icon-Create1 cursor']"
policyRulePage_searchInternalIP_posXpath = "//div[@class='CommonListDetail list-detail']//input[@id='object_ip_search']"
policyRulePage_selectInternalIP_posXpath = "//div[@class='InternalsList list-box']//span[normalize-space(text())='{replaceValue}']"
policyRulePage_closeInternalIP_posXpath = "//div[@class='InternalsList list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"

policyRulePage_addInternalPort_posXpath = "//div[@zs-label='Internal']//div[@class='MultipleSelect InternalsSelect']//i[@class='iconfont icon-Create1 cursor']"
policyRulePage_searchInternalPort_posXpath = "//div[@class='CommonListDetail list-detail-not-tabs']//input[@id='object_ip_search']"
policyRulePage_selectInternalPort_posXpath = "//div[@class='reference-box el-popover__reference']//span[normalize-space(text())='{replaceValue}']"
policyRulePage_closeInternalPort_posXpath = "//div[@class='InternalsList list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"

policyRulePage_addDstPort_posXpath = "//div[@zs-label='Destination']//p[normalize-space(text())='Port']/ancestor::div[@zs-label='SourceItem']//i[@class='iconfont icon-Create1 cursor']"
policyRulePage_searchDstPort_posXpath = "//div[@class='CommonListDetail list-detail-not-tabs']//input[@id='object_ip_search']"
policyRulePage_selectDstPort_posXpath = "//div[@class='reference-box el-popover__reference']//span[normalize-space(text())='{replaceValue}']"
policyRulePage_closeDstPort_posXpath = "//div[@class='destinations list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"

policyRulePage_addExternalIP_posXpath = "//div[@zs-label='External']//div[@class='MultipleSelect ExternalsSelect']//i[@class='iconfont icon-Create1 cursor']"
policyRulePage_searchExternalIP_posXpath = "//div[@class='ExternalsList list-box']//input[@id='object_ip_search']"
policyRulePage_selectExternalIP_posXpath = "//div[@class='ExternalsList list-box']//span[normalize-space(text())='{replaceValue}']"
policyRulePage_closeExternalIP_posXpath = "//div[@class='ExternalsList list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"

policyRulePage_addExternalPort_posXpath = "//div[@zs-label='External']//p[normalize-space(text())='Port']/ancestor::div[@zs-label='SourceItem']//i[@class='iconfont icon-Create1 cursor']"
policyRulePage_searchExternalPort_posXpath = "//div[@class='ExternalsList list-box']//input[@id='object_ip_search']"
policyRulePage_selectExternalPort_posXpath = "//div[@class='ExternalsList list-box']//span[normalize-space(text())='{replaceValue}']"
policyRulePage_closeExternalPort_posXpath = "//div[@class='ExternalsList list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"

policyRulePage_addImsi_posXpath = "//div[@zs-label='Source']//p[normalize-space(text())='Device']/ancestor::div[@zs-label='SourceItem']//i[@class='iconfont icon-Create1 cursor']"
policyRulePage_searchImsi_posXpath = "//div[@class='SourceList list-box']//input[@id='object_ip_search']"
policyRulePage_selectImsi_posXpath = "//ul[@class='row-container tableList']//li[1]//div[@class='row-content-cell']"
policyRulePage_closeImsi_posXpath = "//div[@class='SourceList list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"

# phone number
policyRulePage_choosePhoneNumber_posXpath = "//*[@id='tab-phone_number' and contains(concat(' ', @class, ' '), ' el-tabs__item is-top ') and contains(text(), 'Phone Number')]"

# imei
policyRulePage_chooseImei_posXpath = "//*[@id='tab-imei' and contains(concat(' ', @class, ' '), ' el-tabs__item is-top ') and contains(text(), 'IMEI')]"

policyRulePage_addCondition_posXpath = "//div[@class='MultipleSelect ConditionModuleSelect']//span[normalize-space(text())='Add Condition']"
policyRulePage_addConditionImsi_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Device']"
policyRulePage_addCondition_serverFqdn_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Server FQDN']"
policyRulePage_addCondition_dstPort_posXpath = "//div[@class='SourceList list-box']//li[4]//div[normalize-space(text())='Port']"
policyRulePage_addCondition_url_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='URL']"
policyRulePage_addCondition_uri_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Protocol Field']/parent::*//div[normalize-space(text())='URI']"
policyRulePage_addCondition_requestHeader_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Request Header']"
policyRulePage_addCondition_responseHeader_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Response Header']"
policyRulePage_addCondition_requestBody_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Request Body']"
policyRulePage_addCondition_responseBody_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Response Body']"
policyRulePage_addCondition_close_posXpath = "//div[@class='ToggleDraw']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"
policyRulePage_addCondition_srcPort_posXpath = "//div[@class='SourceList list-box']//li[3]//div[normalize-space(text())='Port']"
policyRulePage_addCondition_internalIP_posXpath = "//div[@class='SourceList list-box']//li[5]//div[normalize-space(text())='IP Address']"
policyRulePage_addCondition_externalIP_posXpath = "//div[@class='SourceList list-box']//li[6]//div[normalize-space(text())='IP Address']"
policyRulePage_addCondition_internalPort_posXpath = "//div[@class='SourceList list-box']//li[5]//div[normalize-space(text())='Port']"
policyRulePage_addCondition_externalPort_posXpath = "//div[@class='SourceList list-box']//li[6]//div[normalize-space(text())='Port']"
policyRulePage_addCondition_IpProtocol_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='IP Protocol']"
policyRulePage_addCondition_Boolean_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='{replaceValue}']"
policyRulePage_addCondition_requestHeader_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Request Header']"
policyRulePage_addCondition_ftpAccount_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Account']"
policyRulePage_addCondition_ftpContent_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Content']"
policyRulePage_addCondition_cn_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='CN']"
policyRulePage_addCondition_san_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='SAN']"
policyRulePage_addCondition_qname_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='QNAME']"
policyRulePage_addCondition_mailSubject_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Subject']"
policyRulePage_addCondition_mailContent_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Content']"
policyRulePage_addCondition_mailFrom_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='From']"
policyRulePage_addCondition_mailTo_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='To']"
policyRulePage_addCondition_mailAccount_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Account']"


policyRulePage_addBoolean_posXpath = "//div[@class='FilterModuleSelect filter-module-select']//li[{replaceValue}]//div[contains(@class, 'addobject')]"
policyRulePage_searchBoolean_posXpath = "//div[@class='CommonListDetail list-detail-not-tabs']//input[@id='object_ip_search']"
policyRulePage_selectBoolean_posXpath = "//ul[@class='row-container tableList']//li[1]//div[@class='row-content-cell']"
policyRulePage_closeBoolean_posXpath = "//div[@class='FilterList list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"
policyRulePage_little_button_addBoolean_posXpath='//p[normalize-space(text())="{replaceValue}"]//ancestor::div[@class="FilterItem"]//i[@class="operate-icon row-edit iconfont icon-Create1"]'

policyRulePage_addIpProtocol_posXpath = "//div[@zs-label='Protocol']//p[normalize-space(text())='IP Protocol']/ancestor::div[@zs-label='Protocol']//i[@class='iconfont icon-Create1 cursor']"
policyRulePage_searchIpProtocol_posXpath = "//div[@class='ProtocolList list-box']//input[@id='object_ip_search']"
policyRulePage_selectIpProtocol_posXpath = "//div[@class='ProtocolList list-box']//span[normalize-space(text())='{replaceValue}']"
policyRulePage_closeIpProtocol_posXpath = "//div[@class='ProtocolList list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"
policyRulePage_little_button_addIpProtocol_posXpath='//div[@zs-label="Protocol"]//*[@class="operate-icon row-edit iconfont icon-Create1"]'

policyRulePage_addServerFqdn_posXpath = "//div[@class='MultipleSelect DestinationsModuleSelect']//li[{replaceValue}]//i[@class='iconfont icon-Create1 cursor']"
policyRulePage_searchServerFqdn_posXpath = "//div[@class='CommonListDetail list-detail']//input[@id='object_ip_search']"
policyRulePage_selectServerFqdn_posXpath = "//ul[@class='row-container tableList']//li[1]//div[@class='row-content-cell']"
policyRulePage_closeServerFqdn_posXpath = "//div[@class='destinations list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"

# cn
policyRulePage_addCn_posXpath = "//div[@zs-label='FilterItem']//p[normalize-space(text())='CN']/ancestor::div[@zs-label='FilterItem']//i[@class='iconfont icon-Create1 cursor']"
policyRulePage_searchCn_posXpath = "//div[@class='FilterList list-box']//input[@id='object_ip_search']"
policyRulePage_selectCn_posXpath = "//ul[@class='row-container tableList']//li[1]//div[@class='row-content-cell']"
policyRulePage_closeCn_posXpath = "//div[@class='FilterList list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"
# san
policyRulePage_addSan_posXpath = "//div[@zs-label='FilterItem']//p[normalize-space(text())='SAN']/ancestor::div[@zs-label='FilterItem']//i[@class='iconfont icon-Create1 cursor']"
policyRulePage_searchSan_posXpath = "//div[@class='FilterList list-box']//input[@id='object_ip_search']"
policyRulePage_selectSan_posXpath = "//ul[@class='row-container tableList']//li[1]//div[@class='row-content-cell']"
policyRulePage_closeSan_posXpath = "//div[@class='FilterList list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"
# qname
policyRulePage_addQname_posXpath = "//div[@zs-label='FilterItem']//p[normalize-space(text())='QNAME']/ancestor::div[@zs-label='FilterItem']//i[@class='iconfont icon-Create1 cursor']"
policyRulePage_searchQname_posXpath = "//div[@class='FilterList list-box']//input[@id='object_ip_search']"
policyRulePage_selectQname_posXpath = "//ul[@class='row-container tableList']//li[1]//div[@class='row-content-cell']"
policyRulePage_closeQname_posXpath = "//div[@class='FilterList list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"

policyRulePage_addUrl_posXpath = "//div[@class='FilterModuleSelect filter-module-select']//li[{replaceValue}]//div[contains(@class, 'addobject')]"
policyRulePage_searchUrl_posXpath = "//div[@class='CommonListDetail list-detail-not-tabs']//input[@id='object_ip_search']"
policyRulePage_selectUrl_posXpath = "//ul[@class='row-container tableList']//li[1]//div[@class='row-content-cell']"
policyRulePage_closeUrl_posXpath = "//div[@class='FilterList list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"


policyRulePage_addRequestHeader_posXpath = "//div[@class='FilterModuleSelect filter-module-select']//li[{replaceValue}]//div[contains(@class, 'addobject')]"
policyRulePage_searchRequestHeader_posXpath = "//div[@class='CommonListDetail list-detail-not-tabs']//input[@id='object_ip_search']"
policyRulePage_selectRequestHeader_posXpath = "//ul[@class='row-container tableList']//li[1]//div[@class='row-content-cell']"
policyRulePage_closeRequestHeader_posXpath = "//div[@class='FilterList list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"

#ftp account
policyRulePage_addFtpAccount_posXpath = "//div[@zs-label='FilterItem']//p[normalize-space(text())='Account']/ancestor::div[@zs-label='FilterItem']//i[@class='iconfont icon-Create1 cursor']"
policyRulePage_searchFtpAccount_posXpath = "//div[@class='CommonListDetail list-detail-not-tabs']//input[@id='object_ip_search']"
policyRulePage_selectFtpAccount_posXpath = "//ul[@class='row-container tableList']//li[1]//div[@class='row-content-cell']"
policyRulePage_closeFtpAccount_posXpath = "//div[@class='FilterList list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"

# ftp content
policyRulePage_addFtpContent_posXpath = "//div[@zs-label='FilterItem']//p[normalize-space(text())='Content']/ancestor::div[@zs-label='FilterItem']//i[@class='iconfont icon-Create1 cursor']"
policyRulePage_searchFtpContent_posXpath = "//div[@class='CommonListDetail list-detail-not-tabs']//input[@id='object_ip_search']"
policyRulePage_selectFtpContent_posXpath = "//ul[@class='row-container tableList']//li[1]//div[@class='row-content-cell']"
policyRulePage_closeFtpContent_posXpath = "//div[@class='FilterList list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"

#mail from
policyRulePage_addMailFrom_posXpath = "//div[@zs-label='FilterItem']//p[normalize-space(text())='From']/ancestor::div[@zs-label='FilterItem']//i[@class='iconfont icon-Create1 cursor']"
policyRulePage_searchMailFrom_posXpath = "//div[@class='CommonListDetail list-detail-not-tabs']//input[@id='object_ip_search']"
policyRulePage_selectMailFrom_posXpath = "//ul[@class='row-container tableList']//li[1]//div[@class='row-content-cell']"
policyRulePage_closeMailFrom_posXpath = "//div[@class='FilterList list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"
#mail to
policyRulePage_addMailTo_posXpath = "//div[@zs-label='FilterItem']//p[normalize-space(text())='To']/ancestor::div[@zs-label='FilterItem']//i[@class='iconfont icon-Create1 cursor']"
policyRulePage_searchMailTo_posXpath = "//div[@class='CommonListDetail list-detail-not-tabs']//input[@id='object_ip_search']"
policyRulePage_selectMailTo_posXpath = "//ul[@class='row-container tableList']//li[1]//div[@class='row-content-cell']"
policyRulePage_closeMailTo_posXpath = "//div[@class='FilterList list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"
#mail account
policyRulePage_addMailAccount_posXpath = "//div[@zs-label='FilterItem']//p[normalize-space(text())='Account']/ancestor::div[@zs-label='FilterItem']//i[@class='iconfont icon-Create1 cursor']"
policyRulePage_searchMailAccount_posXpath = "//div[@class='CommonListDetail list-detail-not-tabs']//input[@id='object_ip_search']"
policyRulePage_selectMailAccount_posXpath = "//ul[@class='row-container tableList']//li[1]//div[@class='row-content-cell']"
policyRulePage_closeMailAccount_posXpath = "//div[@class='FilterList list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"
#mail subject
policyRulePage_addMailSubject_posXpath = "//div[@zs-label='FilterItem']//p[normalize-space(text())='Subject']/ancestor::div[@zs-label='FilterItem']//i[@class='iconfont icon-Create1 cursor']"
policyRulePage_searchMailSubject_posXpath = "//div[@class='CommonListDetail list-detail-not-tabs']//input[@id='object_ip_search']"
policyRulePage_selectMailSubject_posXpath = "//ul[@class='row-container tableList']//li[1]//div[@class='row-content-cell']"
policyRulePage_closeMailSubject_posXpath = "//div[@class='FilterList list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"

# security
securityRuleListPage_createButton_posId = "app_create-_OperateBtns_ElRow_Objects_ProxyInterception_Home_App_anonymousComponent"
securityRuleListPage_deleteButton_posId ="appDel-_OperateBtns_ElRow_Objects_ProxyInterception_Home_App_anonymousComponent"
securityRuleListpage_okButton_warningYes_posXpath = "//button[@class='el-button delComponents-ok role-disconnect-btn el-button--default el-button--small']"
securityRuleListpage_okButton_warningNo_posXpath = "//button[@class='el-button delComponents-close el-button--info el-button--small']"
securityRuleListPage_searchLable_posId = "select-label"
securityRuleListPage_searchLable_dropDown_item_posXpath = "//div[contains(@class,'el-scrollbar')]//span[normalize-space(text())='{replaceValue}']"   #下拉菜单定位
securityRuleListPage_searchLable_input_itemContent_posXpath = "//div[contains(@class,'ListItem')]//span[normalize-space(text())='{replaceValue}']/ancestor::div[contains(@class,'ListItem')]//input"   #输入item的值，replaceValue替换实际查询值
securityRuleListPage_searchLable_searchButton_posId = "searchQuery"
securityRuleListPage_tableTbody_posXpath = "//div[contains(@class,'ly-table1')]//tbody" 
securityRulelistPage_allSelect_posXpath = "//div[@class='page-box-containcheck']//label[contains(@class, 'allCheckbox')]/span/span"

securityRulePage_inputName_posXpath = "//*[@class='biFangName']//input"
securityRulePage_selectShunt_posId = "shuntshunt"
securityRulePage_selectAllow_posId = "allowallow"
securityRulePage_selectDeny_posId = "denydeny"

securityRulePage_addSrcIP_posXpath = policyRulePage_addSrcIP_posXpath
securityRulePage_searchSrcIP_posXpath = policyRulePage_searchSrcIP_posXpath
securityRulePage_selectSrcIP_posXpath = policyRulePage_selectSrcIP_posXpath
securityRulePage_closeSrcIP_posXpath = policyRulePage_closeSrcIP_posXpath

securityRulePage_addSrcPort_posXpath = policyRulePage_addSrcPort_posXpath
securityRulePage_searchSrcPort_posXpath = policyRulePage_searchSrcPort_posXpath
securityRulePage_selectSrcPort_posXpath = policyRulePage_selectSrcPort_posXpath
securityRulePage_closeSrcPort_posXpath = policyRulePage_closeSrcPort_posXpath

securityRulePage_addInternalIP_posXpath = policyRulePage_addInternalIP_posXpath
securityRulePage_searchInternalIP_posXpath = policyRulePage_searchInternalIP_posXpath
securityRulePage_selectInternalIP_posXpath = policyRulePage_selectInternalIP_posXpath
securityRulePage_closeInternalIP_posXpath = policyRulePage_closeInternalIP_posXpath

securityRulePage_addInternalPort_posXpath = policyRulePage_addInternalPort_posXpath
securityRulePage_searchInternalPort_posXpath = policyRulePage_searchInternalPort_posXpath
securityRulePage_selectInternalPort_posXpath = policyRulePage_selectInternalPort_posXpath
securityRulePage_closeInternalPort_posXpath = policyRulePage_closeInternalPort_posXpath



securityRulePage_addDstPort_posXpath = policyRulePage_addDstPort_posXpath
securityRulePage_searchDstPort_posXpath = policyRulePage_searchDstPort_posXpath
securityRulePage_selectDstPort_posXpath = policyRulePage_selectDstPort_posXpath
securityRulePage_closeDstPort_posXpath = policyRulePage_closeDstPort_posXpath

securityRulePage_addExternalPort_posXpath = policyRulePage_addExternalPort_posXpath
securityRulePage_searchExternalPort_posXpath = policyRulePage_searchExternalPort_posXpath
securityRulePage_selectExternalPort_posXpath = policyRulePage_selectExternalPort_posXpath
securityRulePage_closeExternalPort_posXpath = policyRulePage_closeExternalPort_posXpath

securityRulePage_addExternalIP_posXpath = policyRulePage_addExternalIP_posXpath
securityRulePage_searchExternalIP_posXpath = policyRulePage_searchExternalIP_posXpath
securityRulePage_selectExternalIP_posXpath = policyRulePage_selectExternalIP_posXpath
securityRulePage_closeExternalIP_posXpath = policyRulePage_closeExternalIP_posXpath

securityRulePage_addApplication_posXpath = policyRulePage_addApplication_posXpath
securityRulePage_searchApplication_posXpath = policyRulePage_searchApplication_posXpath
securityRulePage_selectApplication_posXpath = policyRulePage_selectApplication_posXpath
securityRulePage_closeApplication_posXpath = policyRulePage_closeApplication_posXpath
securityRulePage_selectApplicationLabel_posXpath = policyRulePage_selectApplicationLabel_posXpath
securityRulePage_selectApplicationGroupLabel_posXpath = policyRulePage_selectApplicationGroupLabel_posXpath

securityRulePage_addCondition_posXpath = policyRulePage_addCondition_posXpath
securityRulePage_addCondition_serverFqdn_posXpath = policyRulePage_addCondition_serverFqdn_posXpath

securityRulePage_addCondition_imsi_posXpath = policyRulePage_addConditionImsi_posXpath
securityRulePage_addCondition_url_posXpath = policyRulePage_addCondition_url_posXpath
securityRulePage_addCondition_uri_posXpath = policyRulePage_addCondition_uri_posXpath
securityRulePage_addCondition_requestHeader_posXpath = policyRulePage_addCondition_requestHeader_posXpath
securityRulePage_addCondition_requestBody_posXpath = policyRulePage_addCondition_requestBody_posXpath
securityRulePage_addCondition_responseBody_posXpath = policyRulePage_addCondition_responseBody_posXpath
securityRulePage_addCondition_responseHeader_posXpath = policyRulePage_addCondition_responseHeader_posXpath
securityRulePage_addCondition_srcPort_posXpath = policyRulePage_addCondition_srcPort_posXpath
securityRulePage_addCondition_dstPort_posXpath = policyRulePage_addCondition_dstPort_posXpath
securityRulePage_addCondition_externalPort_posXpath = policyRulePage_addCondition_externalPort_posXpath
securityRulePage_addCondition_internalIP_posXpath = policyRulePage_addCondition_internalIP_posXpath
securityRulePage_addCondition_externalIP_posXpath = policyRulePage_addCondition_externalIP_posXpath
securityRulePage_addCondition_internalPort_posXpath = policyRulePage_addCondition_internalPort_posXpath
securityRulePage_addCondition_ftpAccount_posXpath = policyRulePage_addCondition_ftpAccount_posXpath
securityRulePage_addCondition_ftpContent_posXpath = policyRulePage_addCondition_ftpContent_posXpath
securityRulePage_addCondition_cn_posXpath = policyRulePage_addCondition_cn_posXpath
securityRulePage_addCondition_san_posXpath = policyRulePage_addCondition_san_posXpath
securityRulePage_addCondition_qname_posXpath = policyRulePage_addCondition_qname_posXpath
securityRulePage_addCondition_close_posXpath = policyRulePage_addCondition_close_posXpath
 

securityRulePage_addServerFqdn_posXpath = policyRulePage_addServerFqdn_posXpath
securityRulePage_searchServerFqdn_posXpath = policyRulePage_searchServerFqdn_posXpath
securityRulePage_selectServerFqdn_posXpath = policyRulePage_selectServerFqdn_posXpath
securityRulePage_closeServerFqdn_posXpath = policyRulePage_closeServerFqdn_posXpath

securityRulePage_addCn_posXpath = policyRulePage_addCn_posXpath
securityRulePage_searchCn_posXpath = policyRulePage_searchCn_posXpath
securityRulePage_selectCn_posXpath = policyRulePage_selectCn_posXpath
securityRulePage_closeCn_posXpath = policyRulePage_closeCn_posXpath

securityRulePage_addSan_posXpath = policyRulePage_addSan_posXpath
securityRulePage_searchSan_posXpath = policyRulePage_searchSan_posXpath
securityRulePage_selectSan_posXpath = policyRulePage_selectSan_posXpath
securityRulePage_closeSan_posXpath = policyRulePage_closeSan_posXpath

securityRulePage_addQname_posXpath = policyRulePage_addQname_posXpath
securityRulePage_searchQname_posXpath = policyRulePage_searchQname_posXpath
securityRulePage_selectQname_posXpath = policyRulePage_selectQname_posXpath
securityRulePage_closeQname_posXpath = policyRulePage_closeQname_posXpath

securityRulePage_addUrl_posXpath = policyRulePage_addUrl_posXpath
securityRulePage_searchUrl_posXpath = policyRulePage_searchUrl_posXpath
securityRulePage_selectUrl_posXpath = policyRulePage_selectUrl_posXpath
securityRulePage_closeUrl_posXpath = policyRulePage_closeUrl_posXpath

securityRulePage_addRequestHeader_posXpath = policyRulePage_addRequestHeader_posXpath
securityRulePage_searchRequestHeader_posXpath = policyRulePage_searchRequestHeader_posXpath
securityRulePage_selectRequestHeader_posXpath = policyRulePage_selectRequestHeader_posXpath
securityRulePage_closeRequestHeader_posXpath = policyRulePage_closeRequestHeader_posXpath

securityRulePage_addImsi_posXpath = policyRulePage_addImsi_posXpath
securityRulePage_searchImsi_posXpath = policyRulePage_searchImsi_posXpath
securityRulePage_selectImsi_posXpath = policyRulePage_selectImsi_posXpath
securityRulePage_closeImsi_posXpath = policyRulePage_closeImsi_posXpath
# ftp account
securityRulePage_addftpAccount_posXpath = policyRulePage_addFtpAccount_posXpath 
securityRulePage_searchftpAccount_posXpath = policyRulePage_searchFtpAccount_posXpath 
securityRulePage_selectftpAccount_posXpath = policyRulePage_selectFtpAccount_posXpath 
securityRulePage_closeftpAccount_posXpath = policyRulePage_closeFtpAccount_posXpath
# ftp content
securityRulePage_addftpContent_posXpath = policyRulePage_addFtpContent_posXpath 
securityRulePage_searchftpContent_posXpath = policyRulePage_searchFtpContent_posXpath 
securityRulePage_selectftpContent_posXpath = policyRulePage_selectFtpContent_posXpath 
securityRulePage_closeftpContent_posXpath = policyRulePage_closeFtpContent_posXpath


#phone number 
securityRulePage_choosePhoneNumber_posXpath = policyRulePage_choosePhoneNumber_posXpath

#phone number 
securityRulePage_chooseImei_posXpath = policyRulePage_chooseImei_posXpath

securityRulePage_enable_posXpath = "//div[@zs-label='Enabled']//span[@class='el-switch__core']"
securityRulePage_okButton_yes_posId = "OK-_SecurityAdd_Home_App_anonymousComponent"
securityRulePage_okButton_warningYes_posXpath = "//button[@class='el-button el-button--default el-button--small el-button--primary operation-confirm']"

securityRulePage_subAction_override_posXpath = "//label[@zs-label='Override Application Deny Action']//span[@class='el-checkbox__inner']"
securityRulePage_subAction_drop_posXpath = "//div[@zs-label='Sub Action']//span[normalize-space(text())='Drop']"
securityRulePage_subAction_drop_dropPkt_posXpath = "//div[@zs-label='Drop packet after N packet']//input[@class='el-input__inner']"
securityRulePage_subAction_drop_sendTcpRst_posXpath = "//label[contains(@class, 'checkbox-value-label')]//span[normalize-space(text())='Send TCP reset']"
securityRulePage_subAction_drop_sendIcmp_posXpath = "//label[contains(@class, 'checkbox-value-label')]//span[normalize-space(text())='Send ICMP unreachable']"
securityRulePage_subAction_rateLimit_posXpath = "//div[@zs-label='Sub Action']//span[normalize-space(text())='Rate Limit']"
securityRulePage_subAction_rateLimit_rate_posXpath = "//div[@class='margin-right5 el-input el-input--small']//input"
securityRulePage_subAction_tamper_posXpath = "//div[@zs-label='Sub Action']//span[normalize-space(text())='Tamper']"
securityRulePage_subAction_block_posXpath = "//div[@zs-label='Sub Action']//span[normalize-space(text())='Block']"
securityRulePage_subAction_block_responseCode_posXpath = "//div[contains(@zs-label, '应答码')]//input[@class='el-input__inner']"
securityRulePage_subAction_block_responseCode_change_posXpath = "//div[contains(@class,'el-scrollbar')]//span[normalize-space(text())='{replaceValue}']"
securityRulePage_subAction_block_responseContent_posXpath = "//div[@class='margin-bottom6 box-sizing']//input[@class='el-input__inner']"
securityRulePage_subAction_block_responseContent_change_posXpath = "//div[contains(@class,'el-scrollbar')]//span[normalize-space(text())='{replaceValue}']"
securityRulePage_subAction_block_responseContent_text_posId = "myEditor1"
securityRulePage_subAction_block_responseContent_clickProfile_posXpath = "//div[@class='box-sizing']//input[@class='el-input__inner']"
securityRulePage_subAction_block_responseContent_searchProfile_posXpath = "//input[@class='width85']"
securityRulePage_subAction_block_responseContent_selectProfile_posId = "filelist_select0"
securityRulePage_subAction_redirect_posXpath = "//div[@zs-label='Sub Action']//span[normalize-space(text())='Redirect']"
securityRulePage_subAction_redirect_input_posXpath = "myEditor1"
securityRulePage_subAction_alert_posXpath = "//div[@zs-label='Sub Action']//span[normalize-space(text())='Alert']"
securityRulePage_subAction_alert_responseCode_posXpath = "//div[contains(@zs-label, '应答码')]//input[@class='el-input__inner']"
securityRulePage_subAction_alert_responseCode_change_posXpath = "//div[contains(@class,'el-scrollbar')]//span[normalize-space(text())='{replaceValue}']"
securityRulePage_subAction_alert_responseContent_posXpath = "//div[@class='margin-bottom6 box-sizing']//input[@class='el-input__inner']"
securityRulePage_subAction_alert_responseContent_change_posXpath = "//div[contains(@class,'el-scrollbar')]//span[normalize-space(text())='{replaceValue}']"
securityRulePage_subAction_alert_responseContent_text_posId = "myEditor1"
securityRulePage_subAction_alert_responseContent_clickProfile_posXpath = "//div[@class='box-sizing']//input[@class='el-input__inner']"
securityRulePage_subAction_alert_responseContent_searchProfile_posXpath = "//input[@class='width85']"
securityRulePage_subAction_alert_responseContent_selectProfile_posId = "filelist_select0"

securityRulePage_packetCapture_posXpath = "//form[@class='el-form policy_edit el-form--label-left']//div[17]//span"
securityRulePage_packetCapture_depth_posXpath = "//div[@class='el-form-item labelStyle padding-left20 el-form-item--small']//input[@class='el-input__inner']"

 
# intercept
interceptRuleListPage_createButton_posId = "app_create-_OperateBtns_ElRow_policy_Intercept_Home_App_anonymousComponent"
interceptRuleListPage_deleteButton_posId ="appDel-_OperateBtns_ElRow_policy_Intercept_Home_App_anonymousComponent"

interceptRulePage_inputName_posXpath = "//*[@class='biFangName']//input"
interceptRulePage_selectDeny_posId = "interceptintercept"

interceptRulePage_enable_posXpath = "//div[@zs-label='Enabled']//span[@class='el-switch__core']"
interceptRulePage_okButton_yes_posId = "OK-_policy_Intercept_edit_Home_App_anonymousComponent"
interceptRulePage_okButton_warningYes_posXpath = "//button[@class='el-button el-button--default el-button--small el-button--primary operation-confirm']"



#### manipulation
manipulationRuleListPage_createButton_posId = "app_create-_OperateBtns_ElRow_policy_Manipulation_Home_App_anonymousComponent"
manipulationRuleListPage_deleteButton_posId ="appDel-_OperateBtns_ElRow_policy_Manipulation_Home_App_anonymousComponent"
manipulationRuleListpage_okButton_warningYes_posXpath = securityRuleListpage_okButton_warningYes_posXpath
# 名字输入定位
manipulationRulePage_inputName_posXpath = securityRulePage_inputName_posXpath
# 动作action定位
manipulationRulePage_selectAllow_posId = "allowallow"
manipulationRulePage_selectDeny_posId = "denydeny"
manipulationRulePage_selectMonitor_posId = "monitormonitor"
manipulationRulePage_selectRedirect_posId = "redirectredirect"
manipulationRulePage_selectReplace_posId = "replacereplace"
manipulationRulePage_selectHijack_posId = "hijackhijack"
manipulationRulePage_selectInsert_posId = "insertinsert"
manipulationRulePage_selectEditElement_posId = "edit_elementedit_element"
manipulationRulePage_selectRunScript_posId = "run_scriptrun_script"
# rule 页面中Add Condition按钮定位
manipulationRulePage_addCondition_posXpath = "//*[@id='policy_condition-_ConditionModuleSelect_ElFormItem_ElForm_VPanel_VEditPanel_Edit_Home_App_anonymousComponent']"
manipulationRulePage_addCondition_close_posXpath = policyRulePage_addCondition_close_posXpath
# rule 中添加condition侧滑中选择行定位
manipulationRulePage_addCondition_srcIP_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Source']/parent::*//div[normalize-space(text())='IP Address']"
manipulationRulePage_addCondition_srcGeography_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Source']/parent::*//div[normalize-space(text())='Geography']"
manipulationRulePage_addCondition_dstcIP_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Destination']/parent::*//div[normalize-space(text())='IP Address']"
manipulationRulePage_addCondition_dstcGeography_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Destination']/parent::*//div[normalize-space(text())='Geography']"
manipulationRulePage_addCondition_serverFqdn_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Destination']/parent::*//div[normalize-space(text())='Server FQDN']"
manipulationRulePage_addCondition_serverPort_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Destination']/parent::*//div[normalize-space(text())='Port']"
manipulationRulePage_addCondition_internalIP_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Internal']/parent::*//div[normalize-space(text())='IP Address']"
manipulationRulePage_addCondition_srcPort_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Source']/parent::*//div[normalize-space(text())='Port']"
manipulationRulePage_addCondition_internalPort_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Internal']/parent::*//div[normalize-space(text())='Port']"
manipulationRulePage_addCondition_destinationPort_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Destination']/parent::*//div[normalize-space(text())='Port']"
manipulationRulePage_addCondition_externalPort_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='External']/parent::*//div[normalize-space(text())='Port']"
manipulationRulePage_addCondition_externalIP_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='External']/parent::*//div[normalize-space(text())='IP Address']"
manipulationRulePage_addCondition_Protocol_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Protocol']"
manipulationRulePage_addCondition_url_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Protocol Field']/parent::*//div[normalize-space(text())='URL']"
manipulationRulePage_addCondition_requestHeader_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Protocol Field']/parent::*//div[normalize-space(text())='Request Header']"
manipulationRulePage_addCondition_responseHeader_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Protocol Field']/parent::*//div[normalize-space(text())='Response Header']"
manipulationRulePage_addCondition_requestBody_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Protocol Field']/parent::*//div[normalize-space(text())='Request Body']"
manipulationRulePage_addCondition_responseBody_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Protocol Field']/parent::*//div[normalize-space(text())='Response Body']"
# rule 页面中不同condition的添加+符号定位操作
## Sorce IP Address的添加、查询、选中、关闭操作
manipulationRulePage_addSrcIP_posXpath = "//div[@zs-label='Source']//div[normalize-space(text())='IP Address']/ancestor::div[@zs-label='SourceItem']//i[contains(@class, 'icon-Create1')]"
manipulationRulePage_searchSrcIP_posXpath = "//div[@class='CommonListDetail list-detail']//input[@id='object_ip_search']"
manipulationRulePage_selectSrcIP_posXpath ="//div[@class='SourceList list-box']//span[normalize-space(text())='{replaceValue}']"
manipulationRulePage_closeSrcIP_posXpath = "//div[@class='SourceList list-box']//div[@class='rigth-menu-button-info']//button"
## Internal IP的添加、查询、选中、关闭操作
manipulationRulePage_addInternalIP_posXpath = policyRulePage_addInternalIP_posXpath
manipulationRulePage_searchInternalIP_posXpath = policyRulePage_searchInternalIP_posXpath
manipulationRulePage_selectInternalIP_posXpath = policyRulePage_selectInternalIP_posXpath
manipulationRulePage_closeInternalIP_posXpath = policyRulePage_closeInternalIP_posXpath
# source Port的添加、查询、选中、关闭操作
manipulationPage_addSrcPort_posXpath = policyRulePage_addSrcPort_posXpath
manipulationRulePage_searchSrcPort_posXpath = policyRulePage_searchSrcPort_posXpath
manipulationRulePage_selectSrcPort_posXpath = policyRulePage_selectSrcPort_posXpath
manipulationRulePage_closeSrcPort_posXpath = policyRulePage_closeSrcPort_posXpath
# Internal Port的添加、查询、选中、关闭操作
manipulationRulePage_addInternalPort_posXpath = policyRulePage_addInternalPort_posXpath
manipulationRulePage_searchInternalPort_posXpath = policyRulePage_searchInternalPort_posXpath
manipulationRulePage_selectInternalPort_posXpath = policyRulePage_selectInternalPort_posXpath
manipulationRulePage_closeInternalPort_posXpath = policyRulePage_closeInternalPort_posXpath
# destination port 的添加、查询、选中、关闭操作
manipulationRulePage_addDstPort_posXpath = policyRulePage_addDstPort_posXpath
manipulationRulePage_searchDstPort_posXpath = policyRulePage_searchDstPort_posXpath
manipulationRulePage_selectDstPort_posXpath = policyRulePage_selectDstPort_posXpath
manipulationRulePage_closeDstPort_posXpath = policyRulePage_closeDstPort_posXpath
# external port 的添加、查询、选中、关闭操作
manipulationRulePage_addExternalPort_posXpath = policyRulePage_addExternalPort_posXpath
manipulationRulePage_searchExternalPort_posXpath = policyRulePage_searchExternalPort_posXpath
manipulationRulePage_selectExternalPort_posXpath = policyRulePage_selectExternalPort_posXpath
manipulationRulePage_closeExternalPort_posXpath = policyRulePage_closeExternalPort_posXpath
# External IP的添加、查询、选中、关闭操作
manipulationRulePage_addExternalIP_posXpath = policyRulePage_addExternalIP_posXpath
manipulationRulePage_searchExternalIP_posXpath = policyRulePage_searchExternalIP_posXpath
manipulationRulePage_selectExternalIP_posXpath = policyRulePage_selectExternalIP_posXpath
manipulationRulePage_closeExternalIP_posXpath = policyRulePage_closeExternalIP_posXpath
# Application的添加、查询、选中、关闭操作
manipulationRulePage_addApplication_posXpath = policyRulePage_addApplication_posXpath
manipulationRulePage_searchApplication_posXpath = policyRulePage_searchApplication_posXpath
manipulationRulePage_selectApplication_posXpath = policyRulePage_selectApplication_posXpath
manipulationRulePage_closeApplication_posXpath = policyRulePage_closeApplication_posXpath
manipulationRulePage_selectApplicationLabel_posXpath = policyRulePage_selectApplicationLabel_posXpath
manipulationRulePage_selectApplicationGroupLabel_posXpath = policyRulePage_selectApplicationGroupLabel_posXpath
# Server FQDN的添加、查询、选中、关闭操作
manipulationRulePage_addServerFqdn_posXpath = policyRulePage_addServerFqdn_posXpath
manipulationRulePage_searchServerFqdn_posXpath = "//div[@class='rm-content']//input[@id='object_ip_search']"
manipulationRulePage_selectServerFqdn_posXpath = policyRulePage_selectServerFqdn_posXpath
manipulationRulePage_closeServerFqdn_posXpath = policyRulePage_closeServerFqdn_posXpath
# url的添加、查询、选中、关闭操作
manipulationRulePage_addUrl_posXpath = policyRulePage_addUrl_posXpath
manipulationRulePage_searchUrl_posXpath = policyRulePage_searchUrl_posXpath
manipulationRulePage_selectUrl_posXpath = policyRulePage_selectUrl_posXpath
manipulationRulePage_closeUrl_posXpath = policyRulePage_closeUrl_posXpath
# request header的添加、查询、选中、关闭操作
manipulationRulePage_addRequestHeader_posXpath = "//p[normalize-space(text())='Request Header']/ancestor::div[@class='FilterItem']//i[contains(@class, 'icon-Create1')]"
manipulationRulePage_searchRequestHeader_posXpath = policyRulePage_searchRequestHeader_posXpath
manipulationRulePage_selectRequestHeader_posXpath = policyRulePage_selectRequestHeader_posXpath
manipulationRulePage_closeRequestHeader_posXpath = policyRulePage_closeRequestHeader_posXpath
# response header的添加、查询、选中、关闭操作
manipulationRulePage_addResponseHeader_posXpath = "//p[normalize-space(text())='Response Header']/ancestor::div[@class='FilterItem']//i[contains(@class, 'icon-Create1')]"
manipulationRulePage_searchResponseHeader_posXpath = policyRulePage_searchRequestHeader_posXpath
manipulationRulePage_selectResponseHeader_posXpath = policyRulePage_selectRequestHeader_posXpath
manipulationRulePage_closeResponseHeader_posXpath = policyRulePage_closeRequestHeader_posXpath
# request body 的添加、查询、选中、关闭操作
manipulationRulePage_addRequestBody_posXpath = "//p[normalize-space(text())='Request Body']/ancestor::div[@class='FilterItem']//i[contains(@class, 'icon-Create1')]"
manipulationRulePage_searchRequestBody_posXpath = policyRulePage_searchRequestHeader_posXpath
manipulationRulePage_selectRequestBody_posXpath = policyRulePage_selectRequestHeader_posXpath
manipulationRulePage_closeRequestBody_posXpath = policyRulePage_closeRequestHeader_posXpath
# response body 的添加、查询、选中、关闭操作
manipulationRulePage_addResponseBody_posXpath = "//p[normalize-space(text())='Response Body']/ancestor::div[@class='FilterItem']//i[contains(@class, 'icon-Create1')]"
manipulationRulePage_searchResponseBody_posXpath = policyRulePage_searchRequestHeader_posXpath
manipulationRulePage_selectResponseBody_posXpath = policyRulePage_selectRequestHeader_posXpath
manipulationRulePage_closeResponseBody_posXpath = policyRulePage_closeRequestHeader_posXpath
# action parameter deny
manipulationRulePage_deny_addResponseCodeSelectBox_posXpath = "//div[@class='panel-content']//label[normalize-space(text())='Response Code']/parent::*//i"   # resposne code 选择框
manipulationRulePage_deny_addResponseCodeSelectDropItem_posXpath = "//body/div[contains(@class, 'el-select-dropdown')]//li//span[normalize-space(text())='{replace_code}']"   # reposne code 下拉列表定位
manipulationRulePage_deny_addResponseContentSelectBox_posXpath = "//div[@class='panel-content']//label[normalize-space(text())='Response Content']/parent::*//i"   # resposne content 选择框
manipulationRulePage_deny_addResponseContentSelectDropItem_posXpath = "//body/div[contains(@class, 'el-select-dropdown')]//li//span[normalize-space(text())='{replace_type}']"   # reposne content 下拉列表定位
manipulationRulePage_deny_addResponseContentTextInput_posXpath = "//div[@id='myEditor1']"   # resposnse content text输入框  定位
manipulationRulePage_deny_addResponseContentProfileSelectBox_posXpath = "//div[@class='box-sizing']//i"   # resposne content profile  选择框  定位
manipulationRulePage_deny_searchResponseProfile_posXpath = "//div[@class='el-scrollbar']//input[@placeholder='Search']"   # resposne content search profile 对话框查询输入框
manipulationRulePage_deny_searchResponseProfileDorpItem_posXpath = "//div[@class='el-scrollbar']//div[contains(@class, 'margin-top')]/li[1]"   # resposne content search profile 对话框查询下拉列表第一个元素
# action parameter redirect http
manipulationRulePage_redirectHttp_addResponseCodeSelectBox_posXpath = manipulationRulePage_deny_addResponseCodeSelectBox_posXpath   # resposne code 选择框
manipulationRulePage_redirectHttp_addResponseCodeSelectDropItem_posXpath = manipulationRulePage_deny_addResponseCodeSelectDropItem_posXpath   # reposne code 下拉列表定位
manipulationRulePage_redirectHttp_addRedirectUrlInput_posXpath = "//input[@id='undefined1']"   # redirect url 输入框 定位
# action parameter replace
manipulationRulePage_replace_addRegex_posXpath = "//ul[@class='replacelist']//div[@zs-label='regexEnable']//div[contains(@class, 'el-switch')]"   # regex 开关定位
manipulationRulePage_replace_addSearchInSelectBox_posXpath = "//ul[@class='replacelist']//div[@zs-label='搜索区域']//i"   # search in 选择框 定位
manipulationRulePage_replace_addSearchInSelectDropItem_posXpath = "//body/div[contains(@class, 'el-select-dropdown')]//li[normalize-space(text())='{replace_type}']"   # search in 下拉框item 定位
manipulationRulePage_replace_addFindInput_posXpath = "//ul[@class='replacelist']//div[@zs-label='Fined']//input"   # find 输入框 定位
manipulationRulePage_replace_addReplaceWithInput_posXpath = "//ul[@class='replacelist']//div[@zs-label='Replace']//input"   # replace with 输入框 定位
# action parameter hijack
manipulationRulePage_hijack_addHijackProfileSelectBox_posXpath = "//div[@zs-label='劫持文件']//i"   # hijack profile  选择框  定位
manipulationRulePage_hijack_searchHijackProfile_posXpath = "//body/div/div[@class='el-scrollbar']//input[@placeholder='Search for']"   # hijack search profile 对话框查询输入框
manipulationRulePage_hijack_searchHijackProfileDorpItem_posXpath = "//body/div/div[@class='el-scrollbar']//div[contains(@class, 'select-search-option')]/li[1]"   # hijack search profile 对话框查询下拉列表第一个元素
# action parameter insert
manipulationRulePage_insert_addInsertProfileSelectBox_posXpath = "//div[@zs-label='劫持文件']//span[@class='el-input__suffix-inner']//i"   # insert script  选择框  定位
manipulationRulePage_insert_searchInsertProfile_posXpath = manipulationRulePage_hijack_searchHijackProfile_posXpath   # insert script search profile 对话框查询输入框
manipulationRulePage_insert_searchInsertProfileDorpItem_posXpath = manipulationRulePage_hijack_searchHijackProfileDorpItem_posXpath   # insert script search profile 对话框查询下拉列表第一个元素
# action parameter edit element
manipulationRulePage_editElement_addSearchScopeWholeFileRadio_posXpath = "//div[@role='radiogroup']//span[normalize-space(text())='whole file']"
manipulationRulePage_editElement_addSearchScopeInsideElementRadio_posXpath = "//div[@role='radiogroup']//span[normalize-space(text())='inside element']"
manipulationRulePage_editElement_addStartIndicatorInput_posXpath = "//label[normalize-space(text())='Start Indicator']/parent::*//input[@id='undefined1']"
manipulationRulePage_editElement_addContainedKeywordInput_posXpath = "//label[normalize-space(text())='Contained Keyword']/parent::*//input[@id='undefined1']"
manipulationRulePage_editElement_addSDistanceFromAnchorInput_posXpath = "//label[normalize-space(text())='Distance from Anchor']/parent::*//input[@class='el-input__inner']"
manipulationRulePage_editElement_addMarkRadio_posXpath = "//label[normalize-space(text())='Treatment']/parent::*//span[normalize-space(text())='Mark']"
manipulationRulePage_editElement_addRemoveRadio_posXpath = "//label[normalize-space(text())='Treatment']/parent::*//span[normalize-space(text())='Remove']"
# action parameter run script profile
manipulationRulePage_insert_addrunScriptProfileSelectBox_posXpath = manipulationRulePage_insert_addInsertProfileSelectBox_posXpath   # run script  选择框  定位
manipulationRulePage_insert_searchrunScriptProfile_posXpath = manipulationRulePage_hijack_searchHijackProfile_posXpath   # insert script search profile 对话框查询输入框
manipulationRulePage_insert_searchrunScriptProfileDorpItem_posXpath = manipulationRulePage_hijack_searchHijackProfileDorpItem_posXpath   # insert script search profile 对话框查询下拉列表第一个元素

# 保存策略时，ok cancel warnging定位
manipulationRulePage_enable_posXpath = securityRulePage_enable_posXpath
manipulationRulePage_okButton_yes_posId = "OK-_Edit_Home_App_anonymousComponent"
manipulationRulePage_okButton_warningYes_posXpath = "//div[@class='el-message-box__btns']//button[contains(@class, 'el-button--primary')]"

#service chaining
mainPage_policySecondLevelMenu_servicechaining_posId = "policy_ServiceChaining"

serviceChainingRuleListPage_createButton_posId = "app_create-_OperateBtns_ElRow_policy_ServiceChaining_Home_App_anonymousComponent"
serviceChainingRuleListPage_deleteButton_posId = "appDel-_OperateBtns_ElRow_policy_ServiceChaining_Home_App_anonymousComponent"
serviceChainingRuleListPage_searchLable_posId = "select-label"
serviceChainingRuleListPage_searchLable_dropDown_item_posXpath = "//div[contains(@class,'el-scrollbar')]//span[normalize-space(text())='{replaceValue}']"   #下拉菜单定位
serviceChainingRuleListPage_searchLable_input_itemContent_posXpath = "//div[contains(@class,'ListItem')]//span[normalize-space(text())='{replaceValue}']/ancestor::div[contains(@class,'ListItem')]//input"   #输入item的值，replaceValue替换实际查询值
serviceChainingRuleListPage_searchLable_searchButton_posId = "searchQuery"
serviceChainingRuleListPage_selectRule_posXpath = "//div[contains(@class,'ly-table1')]//tbody//sapn[@class='el-checkbox__inner']"
serviceChainingRuleListPage_tableTbody_posXpath = "//div[contains(@class,'ly-table1')]//tbody"

serviceChainingRulePage_inputName_posXpath = "//*[@class='biFangName']//input" 
serviceChainingRulePage_rawTrafficButton_posXpath = "//div[@id='TargetedTraffic-group-_policy_service_chaining_write_Home_App_anonymousComponent']//label[@class='el-radio-button el-radio-button--small is-active']" 
serviceChainingRulePage_decryptedTrafficButton_posXpath = "//div[@id='TargetedTraffic-group-_policy_service_chaining_write_Home_App_anonymousComponent']//label[@class='el-radio-button el-radio-button--small']" 
serviceChainingRulePage_addSrcIP_posXpath = policyRulePage_addSrcIP_posXpath
serviceChainingRulePage_searchSrcIP_posXpath = policyRulePage_searchSrcIP_posXpath
serviceChainingRulePage_selectSrcIP_posXpath = policyRulePage_selectSrcIP_posXpath
serviceChainingRulePage_closeSrcIP_posXpath = policyRulePage_closeSrcIP_posXpath

serviceChainingRulePage_addDstIP_posXpath = "//div[@class='MultipleSelect DestinationsModuleSelect']//i[@class='iconfont icon-Create1 cursor']"
serviceChainingRulePage_searchDstIP_posXpath =  "//div[@class='destinations list-box']//div[contains(@class, 'object-item-seach')]//input"
serviceChainingRulePage_selectDstIP_posXpath = "//div[@class='destinations list-box']//span[normalize-space(text())='{replaceValue}']"
serviceChainingRulePage_closeDstIP_posXpath = "//div[@class='destinations list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"

serviceChainingRulePage_addApplication_posXpath = policyRulePage_addApplication_posXpath
serviceChainingRulePage_searchApplication_posXpath = policyRulePage_searchApplication_posXpath
serviceChainingRulePage_selectApplication_posXpath = policyRulePage_selectApplication_posXpath
serviceChainingRulePage_closeApplication_posXpath = policyRulePage_closeApplication_posXpath
serviceChainingRulePage_selectApplicationLabel_posXpath = policyRulePage_selectApplicationLabel_posXpath
serviceChainingRulePage_selectApplicationGroupLabel_posXpath = policyRulePage_selectApplicationGroupLabel_posXpath

serviceChainingRulePage_addCondition_posXpath = policyRulePage_addCondition_posXpath
serviceChainingRulePage_addCondition_serverFqdn_posXpath = policyRulePage_addCondition_serverFqdn_posXpath
serviceChainingRulePage_addCondition_close_posXpath = policyRulePage_addCondition_close_posXpath
serviceChainingRulePage_addServerFqdn_posXpath = policyRulePage_addServerFqdn_posXpath
serviceChainingRulePage_searchServerFqdn_posXpath = policyRulePage_searchServerFqdn_posXpath
serviceChainingRulePage_selectServerFqdn_posXpath = policyRulePage_selectServerFqdn_posXpath
serviceChainingRulePage_closeServerFqdn_posXpath = policyRulePage_closeServerFqdn_posXpath

serviceChainingRulePage_addSFFProfile_posId = "policy_sff_add-_SFFSelect_ElFormItem_ElForm_VPanel_VEditPanel_policy_service_chaining_write_Home_App_anonymousComponent"
serviceChainingRulePage_searchSFFProfile_posXpath = "//div[@class='SFFList list-box']//input"
serviceChainingRulePage_selectSFFProfile_posXpath = "//div[@class='SFFList list-box']//span[@class='ellipsis list-popover-click' and text()='{replaceValue}']"
serviceChainingRulePage_closeSFFProfile_posXpath = "//div[@class='SFFList list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"
serviceChainingRulePage_enable_posXpath = "//div[@zs-label='Enabled']//span[@class='el-switch__core']"
serviceChainingRulePage_okButton_posId = "OK-_policy_service_chaining_write_Home_App_anonymousComponent"
serviceChainingRulePage_warningYes_posXpath = "//button[@class='el-button el-button--default el-button--small el-button--primary operation-confirm']"
serviceChainingRuleListPage_warningYes_posXpath = "//button[@class='el-button delComponents-ok role-disconnect-btn el-button--default el-button--small']"


# shaping
shapingRuleListPage_createButton_posId = "app_create-_OperateBtns_ElRow_policy_trafficShaping_Home_App_anonymousComponent"
shapingRuleListpage_deleteButton_posId = "appDel-_OperateBtns_ElRow_policy_trafficShaping_Home_App_anonymousComponent"
shapingRuleListpage_okButton_warningYes_posXpath = "//button[@class='el-button delComponents-ok role-disconnect-btn el-button--default el-button--small']"
shapingRuleListpage_okButton_warningNo_posXpath = "//button[@class='el-button delComponents-close el-button--info el-button--small']"
shapingRuleListPage_searchLable_posId = "select-label"
shapingRuleListPage_searchLable_dropDown_item_posXpath = "//div[contains(@class,'el-scrollbar')]//span[normalize-space(text())='{replaceValue}']"   #下拉菜单定位
shapingRuleListPage_searchLable_input_itemContent_posXpath = "//div[contains(@class,'ListItem')]//span[normalize-space(text())='{replaceValue}']/ancestor::div[contains(@class,'ListItem')]//input"   #输入item的值，replaceValue替换实际查询值
shapingRuleListPage_searchLable_searchButton_posId = "searchQuery"
shapingRuleListPage_tableTbody_posXpath = "//div[contains(@class,'ly-table1')]//tbody" 
shapingRuleListpage_allButton_posXpath = "//div[@class='checkAction']//span[@class='el-checkbox__label']"

shapingRulePage_inputName_posXpath = "//*[@class='biFangName']//input" # name输入框Xpath

shapingRulePage_addSrcIP_posXpath = policyRulePage_addSrcIP_posXpath
shapingRulePage_searchSrcIP_posXpath = policyRulePage_searchSrcIP_posXpath
shapingRulePage_selectSrcIP_posXpath = policyRulePage_selectSrcIP_posXpath
shapingRulePage_closeSrcIP_posXpath = policyRulePage_closeSrcIP_posXpath

shapingRulePage_priority_posId = "//input[@id='userRegionPriority']"
shapingRulePage_fairFactor_posId = "//input[@id='userRegionfairfactor']"
shapingRulePage_addProfile_posXpath = "//div[@class='MultipleSelect FlagSelect']//div[contains(@class, 'addobject')]"
shapingRulePage_searchProfile_posXpath = "//div[@class='SFFList list-box']//div[contains(@class, 'object-item-seach')]//input"
shapingRulePage_selectProfile_posXpath = "//div[@class='row-content-cell cursorPointer']//div[@class='UaPopover ObjectPopover popover']"
shapingRulePage_closeProfile_posXpath = "//div[@class='SFFList list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"
shapingRulePage_addProfile_plus_posXpath = "//div[@class='MultipleSelect FlagSelect']//i[@class='operate-icon row-edit iconfont icon-Create1']"

shapingRulePage_enable_posXpath = "//span[@class='el-switch__core']"
shapingRulePage_okButton_yes_posId = "OK-_policy_shaping_write_Home_App_anonymousComponent"
shapingRulePage_okButton_warningYes_posXpath = "//button[@class='el-button el-button--default el-button--small el-button--primary operation-confirm']"

#monitor
#monitor列表页按钮
mainPage_policySecondLevelMenu_monitor_posId = "policy_monitor"
monitorRuleListPage_createButton_posId = "app_create-_OperateBtns_ElRow_policy_monitor_Home_App_anonymousComponent"
monitorRuleListPage_deleteButton_posId = "appDel-_OperateBtns_ElRow_policy_monitor_Home_App_anonymousComponent"
monitorRuleListPage_searchLable_posId = "select-label"
monitorRuleListPage_searchLable_dropDown_item_posXpath = "//div[contains(@class,'el-scrollbar')]//span[normalize-space(text())='{replaceValue}']"   #下拉菜单定位
monitorRuleListPage_searchLable_input_itemContent_posXpath = "//div[contains(@class,'ListItem')]//span[normalize-space(text())='{replaceValue}']/ancestor::div[contains(@class,'ListItem')]//input"   #输入item的值，replaceValue替换实际查询值
monitorRuleListPage_searchLable_searchButton_posId = "searchQuery"
monitorRuleListPage_tableTbody_posXpath = "//div[contains(@class,'ly-table1')]//tbody"
monitorRulelistPage_allSelect_posXpath = "//div[@class='page-box-containcheck']//label[contains(@class, 'allCheckbox')]/span/span"
monitorRuleListpage_okButton_warningYes_posXpath= "//button[@class='el-button delComponents-ok role-disconnect-btn el-button--default el-button--small']"
monitorRuleListpage_okButton_warningNo_posXpath= "//button[@class='el-button delComponents-close el-button--info el-button--small']"
#monitor新建页/编辑页面按钮
monitorRulePage_inputName_posXpath = "//*[@class='biFangName']//input"
monitorRulePage_mirrorTrafficButton_posXpath ='//*[text()="Mirror Traffic"]/ancestor::div[@class="el-form-item el-form-item--small"]//*[@class="el-switch__core"]'
monitorRulePage_packetCaptureButton_posXpath = '//*[text()="Packet Capture"]/ancestor::div[@class="el-form-item el-form-item--small"]//span[@class="el-switch__core"]'
monitorRulePage_addSrcIP_posXpath = policyRulePage_addSrcIP_posXpath
monitorRulePage_searchSrcIP_posXpath = policyRulePage_searchSrcIP_posXpath
monitorRulePage_selectSrcIP_posXpath = policyRulePage_selectSrcIP_posXpath
monitorRulePage_closeSrcIP_posXpath = policyRulePage_closeSrcIP_posXpath
monitorRulePage_addApplication_posXpath = policyRulePage_addApplication_posXpath
monitorRulePage_searchApplication_posXpath = policyRulePage_searchApplication_posXpath
monitorRulePage_selectApplication_posXpath = policyRulePage_selectApplication_posXpath
monitorRulePage_closeApplication_posXpath = policyRulePage_closeApplication_posXpath
monitorRulePage_selectApplicationLabel_posXpath = policyRulePage_selectApplicationLabel_posXpath
monitorRulePage_selectApplicationGroupLabel_posXpath = policyRulePage_selectApplicationGroupLabel_posXpath
monitorRulePage_addCondition_posXpath = policyRulePage_addCondition_posXpath
monitorRulePage_packetCapture_posXpath = "//form[@class='el-form policy_edit el-form--label-left']//div[17]//span"
monitorRulePage_packetCapture_depth_posXpath = "//div[@class='el-form-item labelStyle padding-left20 el-form-item--small']//input[@class='el-input__inner']"
monitorRulePage_okButton_warningYes_posXpath = "//button[@class='el-button el-button--default el-button--small el-button--primary operation-confirm']"
##monitor 添加profile的按钮
monitorRulePage_addVLANIDButton_posXpath = '//*[text()="Add VLAN ID"]/ancestor::div[@class="el-form-item padding-left20 Capture_Depth el-form-item--small"]//div[@class="el-switch"]'
monitorRulePage_firstSelectMirrorProfile_posXpath='//*[@class="el-form-item padding-left20 Capture_Depth el-form-item--small"]//input[@class="el-input__inner"]'
monitorRulePage_searchMirrorProfile_posXpath = '//input[@type="search"]'
monitorRulePage_selectMirrorProfile_posXpath = "//li[@class='el-select-dropdown__item' and contains(text(),'{replaceValue}')]"
monitorRulePage_addProfile_plusButton_posXpath= '(//i[@class="iconfont icon-Create1"])[last()]'
monitorRulePage_addProfile_inputName_posXpath='//*[@id="trafficmirror_profileName"]'
monitorRulePage_addProfile_inputVLANID_posXpath='//*[@id="trafficmirror_addrArray0"]'
monitorRulePage_addProfile_addVLANID_plusButton_posXpath='//*[@id="addrTypeAdd"]/i'
monitorRulePage_saveProile_ok_posXpath='//*[@id="trafficMirrorProfile_ok"]'
monitorRulePage_saveProile_warningYes_posXpath='//button[@class="el-button el-button--default el-button--small el-button--primary operation-confirm"]'
#monitor新建页/编辑页按钮
monitorRulePage_enable_posXpath = "//div[@zs-label='Enabled']//span[@class='el-switch__core']"
monitorRulePage_okButton_posId = "OK-_policy_monitor_write_Home_App_anonymousComponent"
monitorRulePage_warningYes_posXpath =shapingRulePage_okButton_warningYes_posXpath
monitorRuleListPage_warningYes_posXpath = "//button[@class='el-button delComponents-ok role-disconnect-btn el-button--default el-button--small']"
#monitor add response header
monitorRulePage_addResponseHeader_posXpath = manipulationRulePage_addResponseHeader_posXpath
monitorRulePage_searchResponseHeader_posXpath = manipulationRulePage_searchResponseHeader_posXpath
monitorRulePage_selectResponseHeader_posXpath = manipulationRulePage_selectResponseHeader_posXpath
monitorRulePage_closeResponseHeader_posXpath = manipulationRulePage_closeResponseHeader_posXpath
#monitor add src port
monitorRulePage_addSrcPort_posXpath = policyRulePage_addSrcPort_posXpath
monitorRulePage_searchSrcPort_posXpath = policyRulePage_searchSrcPort_posXpath
monitorRulePage_selectSrcPort_posXpath = policyRulePage_selectSrcPort_posXpath
monitorRulePage_closeSrcPort_posXpath = policyRulePage_closeSrcPort_posXpath
#monitor add internal ip
monitorRulePage_addInternalIP_posXpath = policyRulePage_addInternalIP_posXpath
monitorRulePage_searchInternalIP_posXpath = policyRulePage_searchInternalIP_posXpath
monitorRulePage_selectInternalIP_posXpath = policyRulePage_selectInternalIP_posXpath
monitorRulePage_closeInternalIP_posXpath = policyRulePage_closeInternalIP_posXpath
#monitor add internal port
monitorRulePage_addInternalPort_posXpath = policyRulePage_addInternalPort_posXpath
monitorRulePage_searchInternalPort_posXpath = policyRulePage_searchInternalPort_posXpath
monitorRulePage_selectInternalPort_posXpath = policyRulePage_selectInternalPort_posXpath
monitorRulePage_closeInternalPort_posXpath = policyRulePage_closeInternalPort_posXpath
#monitor add dst port
monitorRulePage_addDstPort_posXpath = policyRulePage_addDstPort_posXpath
monitorRulePage_searchDstPort_posXpath = policyRulePage_searchDstPort_posXpath
monitorRulePage_selectDstPort_posXpath = policyRulePage_selectDstPort_posXpath
monitorRulePage_closeDstPort_posXpath = policyRulePage_closeDstPort_posXpath
#monitor add external port
monitorRulePage_addExternalPort_posXpath = policyRulePage_addExternalPort_posXpath
monitorRulePage_searchExternalPort_posXpath = policyRulePage_searchExternalPort_posXpath
monitorRulePage_selectExternalPort_posXpath = policyRulePage_selectExternalPort_posXpath
monitorRulePage_closeExternalPort_posXpath = policyRulePage_closeExternalPort_posXpath
#monitor add external ip
monitorRulePage_addExternalIP_posXpath = policyRulePage_addExternalIP_posXpath
monitorRulePage_searchExternalIP_posXpath = policyRulePage_searchExternalIP_posXpath
monitorRulePage_selectExternalIP_posXpath = policyRulePage_selectExternalIP_posXpath
monitorRulePage_closeExternalIP_posXpath = policyRulePage_closeExternalIP_posXpath
#monitor add server fqdn
monitorRulePage_addCondition_serverFqdn_posXpath = policyRulePage_addCondition_serverFqdn_posXpath
#monitor add ....
monitorRulePage_addCondition_imsi_posXpath = policyRulePage_addConditionImsi_posXpath
monitorRulePage_addCondition_url_posXpath = policyRulePage_addCondition_url_posXpath
monitorRulePage_addCondition_uri_posXpath = policyRulePage_addCondition_uri_posXpath
monitorRulePage_addCondition_requestHeader_posXpath = policyRulePage_addCondition_requestHeader_posXpath
monitorRulePage_addCondition_requestBody_posXpath = policyRulePage_addCondition_requestBody_posXpath
monitorRulePage_addCondition_responseBody_posXpath = policyRulePage_addCondition_responseBody_posXpath
monitorRulePage_addCondition_responseHeader_posXpath = policyRulePage_addCondition_responseHeader_posXpath
monitorRulePage_addCondition_srcPort_posXpath = policyRulePage_addCondition_srcPort_posXpath
monitorRulePage_addCondition_dstPort_posXpath = policyRulePage_addCondition_dstPort_posXpath
monitorRulePage_addCondition_externalPort_posXpath = policyRulePage_addCondition_externalPort_posXpath
monitorRulePage_addCondition_internalIP_posXpath = policyRulePage_addCondition_internalIP_posXpath
monitorRulePage_addCondition_externalIP_posXpath = policyRulePage_addCondition_externalIP_posXpath
monitorRulePage_addCondition_internalPort_posXpath = policyRulePage_addCondition_internalPort_posXpath
monitorRulePage_addCondition_ftpAccount_posXpath = policyRulePage_addCondition_ftpAccount_posXpath
monitorRulePage_addCondition_ftpContent_posXpath = policyRulePage_addCondition_ftpContent_posXpath
monitorRulePage_addCondition_cn_posXpath = policyRulePage_addCondition_cn_posXpath
monitorRulePage_addCondition_san_posXpath = policyRulePage_addCondition_san_posXpath
monitorRulePage_addCondition_qname_posXpath = policyRulePage_addCondition_qname_posXpath
monitorRulePage_addCondition_close_posXpath = policyRulePage_addCondition_close_posXpath
#monitor_add server fqdn
monitorRulePage_addServerFqdn_posXpath = policyRulePage_addServerFqdn_posXpath
monitorRulePage_searchServerFqdn_posXpath = policyRulePage_searchServerFqdn_posXpath
monitorRulePage_selectServerFqdn_posXpath = policyRulePage_selectServerFqdn_posXpath
monitorRulePage_closeServerFqdn_posXpath = policyRulePage_closeServerFqdn_posXpath
#monitor add url
monitorRulePage_addUrl_posXpath = "//p[normalize-space(text())='URL']/ancestor::div[@class='FilterItem']//i[contains(@class, 'icon-Create1')]"
monitorRulePage_searchUrl_posXpath = policyRulePage_searchUrl_posXpath
monitorRulePage_selectUrl_posXpath = policyRulePage_selectUrl_posXpath
monitorRulePage_closeUrl_posXpath = policyRulePage_closeUrl_posXpath
#monitor add requset header
monitorRulePage_addRequestHeader_posXpath =  "//p[normalize-space(text())='Request Header']/ancestor::div[@class='FilterItem']//i[contains(@class, 'icon-Create1')]"
monitorRulePage_searchRequestHeader_posXpath = policyRulePage_searchRequestHeader_posXpath
monitorRulePage_selectRequestHeader_posXpath = policyRulePage_selectRequestHeader_posXpath
monitorRulePage_closeRequestHeader_posXpath = policyRulePage_closeRequestHeader_posXpath
#monitor add imsi
monitorRulePage_addImsi_posXpath = policyRulePage_addImsi_posXpath
monitorRulePage_searchImsi_posXpath = policyRulePage_searchImsi_posXpath
monitorRulePage_selectImsi_posXpath = policyRulePage_selectImsi_posXpath
monitorRulePage_closeImsi_posXpath = policyRulePage_closeImsi_posXpath
#monitor add ftp account
monitorRulePage_addftpAccount_posXpath = policyRulePage_addFtpAccount_posXpath
monitorRulePage_searchftpAccount_posXpath = policyRulePage_searchFtpAccount_posXpath
monitorRulePage_selectftpAccount_posXpath = policyRulePage_selectFtpAccount_posXpath
monitorRulePage_closeftpAccount_posXpath = policyRulePage_closeFtpAccount_posXpath
#monitor add  ftp content
monitorRulePage_addftpContent_posXpath = policyRulePage_addFtpContent_posXpath
monitorRulePage_searchftpContent_posXpath = policyRulePage_searchFtpContent_posXpath
monitorRulePage_selectftpContent_posXpath = policyRulePage_selectFtpContent_posXpath
monitorRulePage_closeftpContent_posXpath = policyRulePage_closeFtpContent_posXpath
#monitor add  phone number
monitorRulePage_choosePhoneNumber_posXpath = policyRulePage_choosePhoneNumber_posXpath
#monitor add mail account
monitorRulePage_addmailAccount_posXpath = policyRulePage_addMailAccount_posXpath
monitorRulePage_searchmailAccount_posXpath = policyRulePage_searchMailAccount_posXpath
monitorRulePage_selectmailAccount_posXpath = policyRulePage_selectMailAccount_posXpath
monitorRulePage_closemailAccount_posXpath = policyRulePage_closeMailAccount_posXpath
#monitor add mail from
monitorRulePage_addmailFrom_posXpath = policyRulePage_addMailFrom_posXpath
monitorRulePage_searchmailFrom_posXpath = policyRulePage_searchMailFrom_posXpath
monitorRulePage_selectmailFrom_posXpath = policyRulePage_selectMailFrom_posXpath
monitorRulePage_closemailFrom_posXpath = policyRulePage_closeMailFrom_posXpath
#monitor add mail to
monitorRulePage_addmailTo_posXpath = policyRulePage_addMailTo_posXpath
monitorRulePage_searchmailTo_posXpath = policyRulePage_searchMailTo_posXpath
monitorRulePage_selectmailTo_posXpath = policyRulePage_selectMailTo_posXpath
monitorRulePage_closemailTo_posXpath = policyRulePage_closeMailTo_posXpath
#monitor add mail subject
monitorRulePage_addmailSubject_posXpath = policyRulePage_addMailSubject_posXpath
monitorRulePage_searchmailSubject_posXpath = policyRulePage_searchMailSubject_posXpath
monitorRulePage_selectmailSubject_posXpath = policyRulePage_selectMailSubject_posXpath
monitorRulePage_closemailSubject_posXpath = policyRulePage_closeMailSubject_posXpath
#monit add cn
monitorRulePage_addCn_posXpath = policyRulePage_addCn_posXpath
monitorRulePage_searchCn_posXpath = policyRulePage_searchCn_posXpath
monitorRulePage_selectCn_posXpath = policyRulePage_selectCn_posXpath
monitorRulePage_closeCn_posXpath = policyRulePage_closeCn_posXpath
#monit add san
monitorRulePage_addSan_posXpath = policyRulePage_addSan_posXpath
monitorRulePage_searchSan_posXpath = policyRulePage_searchSan_posXpath
monitorRulePage_selectSan_posXpath = policyRulePage_selectSan_posXpath
monitorRulePage_closeSan_posXpath = policyRulePage_closeSan_posXpath
#monit add qname
monitorRulePage_addQname_posXpath = policyRulePage_addQname_posXpath
monitorRulePage_searchQname_posXpath = policyRulePage_searchQname_posXpath
monitorRulePage_selectQname_posXpath = policyRulePage_selectQname_posXpath
monitorRulePage_closeQname_posXpath = policyRulePage_closeQname_posXpath

#### statistics
statisticsRuleListPage_createButton_posId = "app_create-_OperateBtns_ElRow_policy_statistics_Home_App_anonymousComponent"
statisticsRuleListPage_deleteButton_posId ="appDel-_OperateBtns_ElRow_policy_statistics_Home_App_anonymousComponent"
statisticsRuleListpage_okButton_warningYes_posXpath = securityRuleListpage_okButton_warningYes_posXpath
# 名字输入定位
statisticsRulePage_inputName_posXpath = securityRulePage_inputName_posXpath
# rule 页面中Add Condition按钮定位
statisticsRulePage_addCondition_posXpath = policyRulePage_addCondition_posXpath
statisticsRulePage_addCondition_close_posXpath = policyRulePage_addCondition_close_posXpath
# rule 中添加condition侧滑中选择行定位
statisticsRulePage_addCondition_srcIP_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Source']/parent::*//div[normalize-space(text())='IP Address']"
statisticsRulePage_addCondition_srcGeography_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Source']/parent::*//div[normalize-space(text())='Geography']"
statisticsRulePage_addCondition_srcPort_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Source']/parent::*//div[normalize-space(text())='Port']"
statisticsRulePage_addCondition_dstcIP_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Destination']/parent::*//div[normalize-space(text())='IP Address']"
statisticsRulePage_addCondition_dstcGeography_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Destination']/parent::*//div[normalize-space(text())='Geography']"
statisticsRulePage_addCondition_serverFqdn_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Destination']/parent::*//div[normalize-space(text())='Server FQDN']"
statisticsRulePage_addCondition_serverPort_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Destination']/parent::*//div[normalize-space(text())='Port']"
statisticsRulePage_addCondition_internalIP_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Internal']/parent::*//div[normalize-space(text())='IP Address']"
statisticsRulePage_addCondition_internalPort_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Internal']/parent::*//div[normalize-space(text())='Port']"
statisticsRulePage_addCondition_externalIP_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='External']/parent::*//div[normalize-space(text())='IP Address']"
statisticsRulePage_addCondition_externalPort_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='External']/parent::*//div[normalize-space(text())='Port']"
statisticsRulePage_addCondition_Protocol_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Protocol']"
statisticsRulePage_addCondition_url_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Protocol Field']/parent::*//div[normalize-space(text())='URL']"
statisticsRulePage_addCondition_requestHeader_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Protocol Field']/parent::*//div[normalize-space(text())='Request Header']"
statisticsRulePage_addCondition_responseHeader_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Protocol Field']/parent::*//div[normalize-space(text())='Response Header']"
statisticsRulePage_addCondition_requestBody_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Protocol Field']/parent::*//div[normalize-space(text())='Request Body']"
statisticsRulePage_addCondition_responseBody_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Protocol Field']/parent::*//div[normalize-space(text())='Response Body']"
# rule 页面中不同condition的添加+符号定位操作
## Sorce IP Address的添加、查询、选中、关闭操作
statisticsRulePage_addSrcIP_posXpath = "//div[@zs-label='Source']//div[normalize-space(text())='IP Address']/ancestor::div[@zs-label='SourceItem']//i[contains(@class, 'icon-Create1')]"
statisticsRulePage_searchSrcIP_posXpath = "//div[@class='SourceList list-box']//div[@class='CommonListDetail list-detail']//input[@id='object_ip_search']"
statisticsRulePage_selectSrcIP_posXpath ="//div[@class='SourceList list-box']//span[normalize-space(text())='{replaceValue}']"
statisticsRulePage_closeSrcIP_posXpath = "//div[@class='SourceList list-box']//div[@class='rigth-menu-button-info']//button"
## Destination IP Address的添加、查询、选中、关闭操作
statisticsRulePage_addDstIP_posXpath = "//div[@zs-label='Destination']//div[normalize-space(text())='IP Address']/ancestor::div[@zs-label='SourceItem']//i[contains(@class, 'icon-Create1')]"
statisticsRulePage_searchDstIP_posXpath = "//div[@class='destinations list-box']//div[@class='CommonListDetail list-detail']//input[@id='object_ip_search']"
statisticsRulePage_selectDstIP_posXpath ="//div[@class='destinations list-box']//span[normalize-space(text())='{replaceValue}']"
statisticsRulePage_closeDstIP_posXpath = "//div[@class='destinations list-box']//div[@class='rigth-menu-button-info']//button"
## Internal IP的添加、查询、选中、关闭操作
statisticsRulePage_addInternalIP_posXpath = policyRulePage_addInternalIP_posXpath
statisticsRulePage_searchInternalIP_posXpath = policyRulePage_searchInternalIP_posXpath
statisticsRulePage_selectInternalIP_posXpath = policyRulePage_selectInternalIP_posXpath
statisticsRulePage_closeInternalIP_posXpath = policyRulePage_closeInternalIP_posXpath
# Internal Port的添加、查询、选中、关闭操作
statisticsRulePage_addInternalPort_posXpath = policyRulePage_addInternalPort_posXpath
statisticsRulePage_searchInternalPort_posXpath = policyRulePage_searchInternalPort_posXpath
statisticsRulePage_selectInternalPort_posXpath = policyRulePage_selectInternalPort_posXpath
statisticsRulePage_closeInternalPort_posXpath = policyRulePage_closeInternalPort_posXpath
# External IP的添加、查询、选中、关闭操作
statisticsRulePage_addExternalIP_posXpath = policyRulePage_addExternalIP_posXpath
statisticsRulePage_searchExternalIP_posXpath = policyRulePage_searchExternalIP_posXpath
statisticsRulePage_selectExternalIP_posXpath = policyRulePage_selectExternalIP_posXpath
statisticsRulePage_closeExternalIP_posXpath = policyRulePage_closeExternalIP_posXpath
# Application的添加、查询、选中、关闭操作
statisticsRulePage_addApplication_posXpath = policyRulePage_addApplication_posXpath
statisticsRulePage_searchApplication_posXpath = policyRulePage_searchApplication_posXpath
statisticsRulePage_selectApplication_posXpath = policyRulePage_selectApplication_posXpath
statisticsRulePage_closeApplication_posXpath = policyRulePage_closeApplication_posXpath
statisticsRulePage_selectApplicationLabel_posXpath = policyRulePage_selectApplicationLabel_posXpath
statisticsRulePage_selectApplicationGroupLabel_posXpath = policyRulePage_selectApplicationGroupLabel_posXpath
# Server FQDN的添加、查询、选中、关闭操作
statisticsRulePage_addServerFqdn_posXpath = policyRulePage_addServerFqdn_posXpath
statisticsRulePage_searchServerFqdn_posXpath = policyRulePage_searchServerFqdn_posXpath
statisticsRulePage_selectServerFqdn_posXpath = policyRulePage_selectServerFqdn_posXpath
statisticsRulePage_closeServerFqdn_posXpath = policyRulePage_closeServerFqdn_posXpath
# url的添加、查询、选中、关闭操作
statisticsRulePage_addUrl_posXpath = policyRulePage_addUrl_posXpath
statisticsRulePage_searchUrl_posXpath = policyRulePage_searchUrl_posXpath
statisticsRulePage_selectUrl_posXpath = policyRulePage_selectUrl_posXpath
statisticsRulePage_closeUrl_posXpath = policyRulePage_closeUrl_posXpath
# request header的添加、查询、选中、关闭操作
statisticsRulePage_addRequestHeader_posXpath = policyRulePage_addRequestHeader_posXpath
statisticsRulePage_searchRequestHeader_posXpath = policyRulePage_searchRequestHeader_posXpath
statisticsRulePage_selectRequestHeader_posXpath = policyRulePage_selectRequestHeader_posXpath
statisticsRulePage_closeRequestHeader_posXpath = policyRulePage_closeRequestHeader_posXpath
# Template添加按钮定位
statisticsRulePage_add_template_posXpath = "//div[@class='el-form-item__content']/div[@class='addobject width300px addobject-long-list obj-content-null cursorPointer borderColor']"   # resposne code 选择框
statisticsRulePage_search_template_posXpath = "//div[@class='CommonListDetail list-detail']//div[contains(@class, 'object-item-seach')]//input"
statisticsRulePage_select_template_posXpath = "//div[@class='CommonListDetail list-detail']//div[@class='UaPopover TemplatePopover popover']"
statisticsRulePage_close_template_posXpath = "//div[@class='FlagList list-box']//div[@class='rigth-menu-button-info']"
# 保存策略时，ok cancel warnging定位
statisticsRulePage_enable_posXpath = securityRulePage_enable_posXpath
statisticsRulePage_okButton_yes_posId = "OK-_policy_statistics_edit_Home_App_anonymousComponent"
statisticsRulePage_okButton_warningYes_posXpath = "//button[@class='el-button el-button--default el-button--small el-button--primary operation-confirm']"
statisticsRulePage_okButton_warningNo_posXpath = "//button[@class='el-button el-button--default el-button--small el-button--primary operation-confirm']"
statisticsRulePage_delete_tip_button_warningYes_posXpath = "//button[@class='el-button delComponents-ok role-disconnect-btn el-button--default el-button--small']"
statisticsRulePage_delete_tip_button_warningNo_posXpath = "//button[@class='el-button delComponents-close el-button--info el-button--small']"

# 策略编辑界面右侧信息
statisticsRulePage_rightInfo_lastHitTime_posXpath = "//form[@class='el-form paper-grid-right el-form--label-top']//table//tr[1]//td[2]"
statisticsRulePage_rightInfo_firstHitTime_posXpath = "//form[@class='el-form paper-grid-right el-form--label-top']//table//tr[2]//td[2]"
statisticsRulePage_rightInfo_throughput_posXpath = "//form[@class='el-form paper-grid-right el-form--label-top']//table//tr[3]//td[2]"
statisticsRulePage_rightInfo_hitCount_posXpath = "//form[@class='el-form paper-grid-right el-form--label-top']//table//tr[4]//td[2]"
statisticsRulePage_rightInfo_72hoursHitCount_posXpath = "//form[@class='el-form paper-grid-right el-form--label-top']//table//tr[5]//td[2]"
