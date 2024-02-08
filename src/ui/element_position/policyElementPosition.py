mainPage_navigationBar_logo_posCss = ".tsg-img-logo"
mainPage_policyFirstLevelMenu_posId = "policy"  # 一级菜单Policies
mainPage_policySecondLevelMenu_security_posId = "Objects_ProxyInterception"
mainPage_policySecondLevelMenu_shaping_posId = "policy_trafficShaping"  # 二级菜单Shaping

mainPage_button_menu_posXCss = ".menu-btn span"
mainPage_currentPage_vsysName_posXpath = "//span[@class='root-title']" 
mainPage_vsysTree_vsysName_posXpath = "//div[contains(@class, 'menu-level2')]//article//div[@class='menu-title']"    # vsys tree中vsys name定位

policyRulePage_addSrcIP_posXpath = "//div[@class='MultipleSelect SourceModuleSelect']//i[@class='iconfont icon-Create1 cursor']"
policyRulePage_searchSrcIP_posXpath = "//div[@class='SourceList list-box']//div[contains(@class, 'object-item-seach')]//input"
policyRulePage_selectSrcIP_posXpath = "//div[@class='reference-box el-popover__reference']//div[@class='row-content-cell']"
policyRulePage_closeSrcIP_posXpath = "//div[@class='SourceList list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"

policyRulePage_addApplication_posXpath = "//div[@class='MultipleSelect AppSelect']//i[@class='iconfont icon-Create1 cursor']"
policyRulePage_searchApplication_posXpath = "//div[@class='AppList list-box']//input[@id='object_ip_search']"
policyRulePage_selectApplication_posXpath = "//div[@class='floatleft margin-top20 overflow-y-auto overflow-x-hidden width100']//li[1]//div[@class='reference-box el-popover__reference']"
policyRulePage_closeApplication_posXpath = "//div[@class='ToggleDraw']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"

policyRulePage_addCondition_posXpath = "//div[@class='MultipleSelect ConditionModuleSelect']//span[normalize-space(text())='Add Condition']"
policyRulePage_addCondition_serverFqdn_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Server FQDN']"
policyRulePage_addCondition_url_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='URL']"
policyRulePage_addCondition_close_posXpath = "//div[@class='ToggleDraw']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"

policyRulePage_addServerFqdn_posXpath = "//div[@class='MultipleSelect DestinationsModuleSelect']//li[{replaceValue}]//i[@class='iconfont icon-Create1 cursor']"
policyRulePage_searchServerFqdn_posXpath = "//div[@class='CommonListDetail list-detail']//input[@id='object_ip_search']"
policyRulePage_selectServerFqdn_posXpath = "//ul[@class='row-container tableList']//li[1]//div[@class='row-content-cell']"
policyRulePage_closeServerFqdn_posXpath = "//div[@class='destinations list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"

policyRulePage_addUrl_posXpath = "//div[@class='FilterModuleSelect filter-module-select']//li[{replaceValue}]//div[contains(@class, 'addobject')]"
policyRulePage_searchUrl_posXpath = "//div[@class='CommonListDetail list-detail-not-tabs']//input[@id='object_ip_search']"
policyRulePage_selectUrl_posXpath = "//ul[@class='row-container tableList']//li[1]//div[@class='row-content-cell']"
policyRulePage_closeUrl_posXpath = "//div[@class='FilterList list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"

# security
securityRuleListPage_createButton_posId = "app_create-_OperateBtns_ElRow_Objects_ProxyInterception_Home_App_anonymousComponent"
securityRuleListPage_deleteButton_posId ="appDel-_OperateBtns_ElRow_Objects_ProxyInterception_Home_App_anonymousComponent"
securityRuleListpage_okButton_warningYes_posXpath = "//button[@class='el-button delComponents-ok role-disconnect-btn el-button--default el-button--small']"
securityRuleListpage_okButton_warningNo_posXpath = "//button[@class='el-button delComponents-close el-button--info el-button--small']"
securityRuleListPage_searchLable_posId = "select-label"
securityRuleListPage_searchLable_dropDown_item_posXpath = "//div[contains(@class,'el-scrollbar')]//span[normalize-space(text())='{replaceName}']"   #下拉菜单定位
securityRuleListPage_searchLable_input_itemContent_posXpath = "//div[contains(@class,'ListItem')]//span[normalize-space(text())='{replaceName}']/ancestor::div[contains(@class,'ListItem')]//input"   #输入item的值，replaceName替换实际查询值
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

securityRulePage_addApplication_posXpath = policyRulePage_addApplication_posXpath
securityRulePage_searchApplication_posXpath = policyRulePage_searchApplication_posXpath
securityRulePage_selectApplication_posXpath = policyRulePage_selectApplication_posXpath
securityRulePage_closeApplication_posXpath = policyRulePage_closeApplication_posXpath

securityRulePage_addCondition_posXpath = policyRulePage_addCondition_posXpath
securityRulePage_addCondition_serverFqdn_posXpath = policyRulePage_addCondition_serverFqdn_posXpath
securityRulePage_addCondition_url_posXpath = policyRulePage_addCondition_url_posXpath
securityRulePage_addCondition_close_posXpath = policyRulePage_addCondition_close_posXpath

securityRulePage_addServerFqdn_posXpath = policyRulePage_addServerFqdn_posXpath
securityRulePage_searchServerFqdn_posXpath = policyRulePage_searchServerFqdn_posXpath
securityRulePage_selectServerFqdn_posXpath = policyRulePage_selectServerFqdn_posXpath
securityRulePage_closeServerFqdn_posXpath = policyRulePage_closeServerFqdn_posXpath

securityRulePage_addUrl_posXpath = policyRulePage_addUrl_posXpath
securityRulePage_searchUrl_posXpath = policyRulePage_searchUrl_posXpath
securityRulePage_selectUrl_posXpath = policyRulePage_selectUrl_posXpath
securityRulePage_closeUrl_posXpath = policyRulePage_closeUrl_posXpath

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
securityRulePage_subAction_block_responseCode_change_posXpath = "//div[contains(@class,'el-scrollbar')]//span[normalize-space(text())='{replaceName}']"
securityRulePage_subAction_block_responseContent_posXpath = "//div[@class='margin-bottom6 box-sizing']//input[@class='el-input__inner']"
securityRulePage_subAction_block_responseContent_change_posXpath = "//div[contains(@class,'el-scrollbar')]//span[normalize-space(text())='{replaceName}']"
securityRulePage_subAction_block_responseContent_text_posId = "myEditor1"
securityRulePage_subAction_block_responseContent_clickProfile_posXpath = "//div[@class='box-sizing']//input[@class='el-input__inner']"
securityRulePage_subAction_block_responseContent_searchProfile_posXpath = "//input[@class='width85']"
securityRulePage_subAction_block_responseContent_selectProfile_posId = "filelist_select0"
securityRulePage_subAction_redirect_posXpath = "//div[@zs-label='Sub Action']//span[normalize-space(text())='Redirect']"
securityRulePage_subAction_alert_posXpath = "//div[@zs-label='Sub Action']//span[normalize-space(text())='Alert']"
securityRulePage_subAction_alert_responseCode_posXpath = "//div[contains(@zs-label, '应答码')]//input[@class='el-input__inner']"
securityRulePage_subAction_alert_responseCode_change_posXpath = "//div[contains(@class,'el-scrollbar')]//span[normalize-space(text())='{replaceName}']"
securityRulePage_subAction_alert_responseContent_posXpath = "//div[@class='margin-bottom6 box-sizing']//input[@class='el-input__inner']"
securityRulePage_subAction_alert_responseContent_change_posXpath = "//div[contains(@class,'el-scrollbar')]//span[normalize-space(text())='{replaceName}']"
securityRulePage_subAction_alert_responseContent_text_posId = "myEditor1"
securityRulePage_subAction_alert_responseContent_clickProfile_posXpath = "//div[@class='box-sizing']//input[@class='el-input__inner']"
securityRulePage_subAction_alert_responseContent_searchProfile_posXpath = "//input[@class='width85']"
securityRulePage_subAction_alert_responseContent_selectProfile_posId = "filelist_select0"

securityRulePage_packetCapture_posXpath = "//form[@class='el-form policy_edit el-form--label-left']//div[17]//span"
securityRulePage_packetCapture_depth_posXpath = "//div[@class='el-form-item labelStyle padding-left20 el-form-item--small']//input[@class='el-input__inner']"

# shaping
shapingRuleListPage_createButton_posId = "app_create-_OperateBtns_ElRow_policy_trafficShaping_Home_App_anonymousComponent"
shapingRuleListpage_deleteButton_posId = "appDel-_OperateBtns_ElRow_policy_trafficShaping_Home_App_anonymousComponent"
shapingRuleListpage_okButton_warningYes_posXpath = "//button[@class='el-button delComponents-ok role-disconnect-btn el-button--default el-button--small']"
shapingRuleListpage_okButton_warningNo_posXpath = "//button[@class='el-button delComponents-close el-button--info el-button--small']"
shapingRuleListPage_searchLable_posId = "select-label"
shapingRuleListPage_searchLable_dropDown_item_posXpath = "//div[contains(@class,'el-scrollbar')]//span[normalize-space(text())='{replaceName}']"   #下拉菜单定位
shapingRuleListPage_searchLable_input_itemContent_posXpath = "//div[contains(@class,'ListItem')]//span[normalize-space(text())='{replaceName}']/ancestor::div[contains(@class,'ListItem')]//input"   #输入item的值，replaceName替换实际查询值
shapingRuleListPage_searchLable_searchButton_posId = "searchQuery"
shapingRuleListPage_tableTbody_posXpath = "//div[contains(@class,'ly-table1')]//tbody" 
shapingRuleListpage_allButton_posXpath = "//div[@class='checkAction']//span[@class='el-checkbox__label']"

shapingRulePage_inputName_posXpath = "//*[@class='biFangName']//input" # name输入框Xpath

shapingRulePage_addCondition_srcIP_posXpath = policyRulePage_addSrcIP_posXpath
shapingRulePage_searchSrcIP_posXpath = policyRulePage_searchSrcIP_posXpath
shapingRulePage_selectSrcIP_posXpath = policyRulePage_selectSrcIP_posXpath
shapingRulePage_closeSrcIP_posXpath = policyRulePage_closeSrcIP_posXpath

shapingRulePage_priority_posId = "//input[@id='userRegionPriority']"
shapingRulePage_fairFactor_posId = "//input[@id='userRegionfairfactor']"
shapingRulePage_addProfile_posXpath = "//div[@class='MultipleSelect FlagSelect']//div[contains(@class, 'addobject')]"
shapingRulePage_searchProfile_posXpath = "//div[@class='SFFList list-box']//div[contains(@class, 'object-item-seach')]//input"
shapingRulePage_selectProfile_posXpath = "//div[@class='row-content-cell cursorPointer']//div[@class='UaPopover ObjectPopover popover']"

shapingRulePage_enable_posXpath = "//span[@class='el-switch__core']"
shapingRulePage_okButton_yes_posId = "OK-_policy_shaping_write_Home_App_anonymousComponent"
shapingRulePage_okButton_warningYes_posXpath = "//button[@class='el-button el-button--default el-button--small el-button--primary operation-confirm']"
