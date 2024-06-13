mainPage_navigationBar_logo_posCss = ".tsg-img-logo"
mainPage_policyFirstLevelMenu_posId = "policy"  # 一级菜单Policies
mainPage_policySecondLevelMenu_security_posId = "Objects_ProxyInterception"
mainPage_policySecondLevelMenu_manipulation_posId = "policy_Manipulation"  # 二级菜单manipulatjion
mainPage_policySecondLevelMenu_shaping_posId = "policy_trafficShaping"  # 二级菜单Shaping

mainPage_button_menu_posXCss = ".menu-btn span"
mainPage_currentPage_vsysName_posXpath = "//span[@class='root-title']" 
mainPage_vsysTree_vsysName_posXpath = "//div[contains(@class, 'menu-level2')]//article//div[@class='menu-title']"    # vsys tree中vsys name定位

policyRulePage_addSrcIP_posXpath = "//div[@class='MultipleSelect SourceModuleSelect']//i[@class='iconfont icon-Create1 cursor']"
policyRulePage_searchSrcIP_posXpath = "//div[@class='SourceList list-box']//div[contains(@class, 'object-item-seach')]//input"
policyRulePage_selectSrcIP_posXpath = "//div[@class='SourceList list-box']//span[normalize-space(text())='{replaceValue}']"
policyRulePage_closeSrcIP_posXpath = "//div[@class='SourceList list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"

policyRulePage_addSrcPort_posXpath = "//div[@class='MultipleSelect SourceModuleSelect']//i[@class='iconfont icon-Create1 cursor']"
policyRulePage_searchSrcPort_posXpath = "//div[@class='SourceList list-box']//input[@id='object_ip_search']"
policyRulePage_selectSrcPort_posXpath = "//div[@class='reference-box el-popover__reference']//span[normalize-space(text())='{replaceValue}']"
policyRulePage_closeSrcPort_posXpath = "//div[@class='SourceList list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"

policyRulePage_addApplication_posXpath = "//div[@class='MultipleSelect AppSelect']//i[@class='iconfont icon-Create1 cursor']"
policyRulePage_searchApplication_posXpath = "//div[@class='AppList list-box']//input[@id='object_ip_search']"
policyRulePage_selectApplication_posXpath = "//div[@class='floatleft margin-top20 overflow-y-auto overflow-x-hidden width100']//li[1]//div[@class='reference-box el-popover__reference']"
policyRulePage_closeApplication_posXpath = "//div[@class='ToggleDraw']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"
policyRulePage_selectApplicationLabel_posXpath = "//div[@class='el-tabs__nav is-top']//div[normalize-space(text())='Application']"
policyRulePage_selectApplicationGroupLabel_posXpath = "//div[normalize-space(text())='Group']"

policyRulePage_addInternalIP_posXpath = "//div[@zs-label='Internal']//div[@class='MultipleSelect InternalsSelect']//i[@class='iconfont icon-Create1 cursor']"
policyRulePage_searchInternalIP_posXpath = "//div[@class='CommonListDetail list-detail']//input[@id='object_ip_search']"
policyRulePage_selectInternalIP_posXpath = "//div[@class='InternalsList list-box']//span[normalize-space(text())='{replaceValue}']"
policyRulePage_closeInternalIP_posXpath = "//div[@class='InternalsList list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"

policyRulePage_addInternalPort_posXpath = "//div[@zs-label='Internal']//div[@class='MultipleSelect InternalsSelect']//i[@class='iconfont icon-Create1 cursor']"
policyRulePage_searchInternalPort_posXpath = "//div[@class='CommonListDetail list-detail-not-tabs']//input[@id='object_ip_search']"
policyRulePage_selectInternalPort_posXpath = "//div[@class='reference-box el-popover__reference']//span[normalize-space(text())='{replaceValue}']"
policyRulePage_closeInternalPort_posXpath = "//div[@class='InternalsList list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"

policyRulePage_addConditionDstPort_posXpath = "//div[@zs-label='Destination']//p[normalize-space(text())='Port]/ancestor::div[@zs-label='SourceItem']//i[@class='iconfont icon-Create1 cursor']"
policyRulePage_searchDstPort_posXpath = "//div[@class='CommonListDetail list-detail-not-tabs']//input[@id='object_ip_search']"
policyRulePage_selectDstPort_posXpath = "//div[@class='reference-box el-popover__reference']//span[normalize-space(text())='{replaceValue}']"
policyRulePage_closeDstPort_posXpath = "//div[@class='destinations list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"

policyRulePage_addExternalIP_posXpath = "//div[@zs-label='External']//div[@class='MultipleSelect ExternalsSelect']//i[@class='iconfont icon-Create1 cursor']"
policyRulePage_searchExternalIP_posXpath = "//div[@class='ExternalsList list-box']//input[@id='object_ip_search']"
policyRulePage_selectExternalIP_posXpath = "//div[@class='ExternalsList list-box']//span[normalize-space(text())='{replaceValue}']"
policyRulePage_closeExternalIP_posXpath = "//div[@class='ExternalsList list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"

policyRulePage_addCondition_posXpath = "//div[@class='MultipleSelect ConditionModuleSelect']//span[normalize-space(text())='Add Condition']"
policyRulePage_addCondition_serverFqdn_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Server FQDN']"
policyRulePage_addCondition_url_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='URL']"
policyRulePage_addCondition_requestHeader_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Request Header']"
policyRulePage_addCondition_close_posXpath = "//div[@class='ToggleDraw']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"
policyRulePage_addCondition_srcPort_posXpath = "//div[@class='SourceList list-box']//li[3]//div[normalize-space(text())='Port']"
policyRulePage_addCondition_internalIP_posXpath = "//div[@class='SourceList list-box']//li[5]//div[normalize-space(text())='IP Address']"
policyRulePage_addCondition_externalIP_posXpath = "//div[@class='SourceList list-box']//li[6]//div[normalize-space(text())='IP Address']"
policyRulePage_addCondition_internalPort_posXpath = "//div[@class='SourceList list-box']//li[5]//div[normalize-space(text())='Port']"

policyRulePage_addServerFqdn_posXpath = "//div[@class='MultipleSelect DestinationsModuleSelect']//li[{replaceValue}]//i[@class='iconfont icon-Create1 cursor']"
policyRulePage_searchServerFqdn_posXpath = "//div[@class='CommonListDetail list-detail']//input[@id='object_ip_search']"
policyRulePage_selectServerFqdn_posXpath = "//ul[@class='row-container tableList']//li[1]//div[@class='row-content-cell']"
policyRulePage_closeServerFqdn_posXpath = "//div[@class='destinations list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"

policyRulePage_addUrl_posXpath = "//div[@class='FilterModuleSelect filter-module-select']//li[{replaceValue}]//div[contains(@class, 'addobject')]"
policyRulePage_searchUrl_posXpath = "//div[@class='CommonListDetail list-detail-not-tabs']//input[@id='object_ip_search']"
policyRulePage_selectUrl_posXpath = "//ul[@class='row-container tableList']//li[1]//div[@class='row-content-cell']"
policyRulePage_closeUrl_posXpath = "//div[@class='FilterList list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"

policyRulePage_addRequestHeader_posXpath = "//div[@class='FilterModuleSelect filter-module-select']//li[{replaceValue}]//div[contains(@class, 'addobject')]"
policyRulePage_searchRequestHeader_posXpath = "//div[@class='CommonListDetail list-detail-not-tabs']//input[@id='object_ip_search']"
policyRulePage_selectRequestHeader_posXpath = "//ul[@class='row-container tableList']//li[1]//div[@class='row-content-cell']"
policyRulePage_closeRequestHeader_posXpath = "//div[@class='FilterList list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"

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

securityRulePage_addDstPort_posXpath = policyRulePage_addConditionDstPort_posXpath
securityRulePage_searchDstPort_posXpath = policyRulePage_searchDstPort_posXpath
securityRulePage_selectDstPort_posXpath = policyRulePage_selectDstPort_posXpath
securityRulePage_closeDstPort_posXpath = policyRulePage_closeDstPort_posXpath

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
securityRulePage_addCondition_url_posXpath = policyRulePage_addCondition_url_posXpath
securityRulePage_addCondition_requestHeader_posXpath = policyRulePage_addCondition_requestHeader_posXpath
securityRulePage_addCondition_srcPort_posXpath = policyRulePage_addCondition_srcPort_posXpath
securityRulePage_addCondition_internalIP_posXpath = policyRulePage_addCondition_internalIP_posXpath
securityRulePage_addCondition_externalIP_posXpath = policyRulePage_addCondition_externalIP_posXpath
securityRulePage_addCondition_internalPort_posXpath = policyRulePage_addCondition_internalPort_posXpath
securityRulePage_addCondition_close_posXpath = policyRulePage_addCondition_close_posXpath

securityRulePage_addServerFqdn_posXpath = policyRulePage_addServerFqdn_posXpath
securityRulePage_searchServerFqdn_posXpath = policyRulePage_searchServerFqdn_posXpath
securityRulePage_selectServerFqdn_posXpath = policyRulePage_selectServerFqdn_posXpath
securityRulePage_closeServerFqdn_posXpath = policyRulePage_closeServerFqdn_posXpath

securityRulePage_addUrl_posXpath = policyRulePage_addUrl_posXpath
securityRulePage_searchUrl_posXpath = policyRulePage_searchUrl_posXpath
securityRulePage_selectUrl_posXpath = policyRulePage_selectUrl_posXpath
securityRulePage_closeUrl_posXpath = policyRulePage_closeUrl_posXpath

securityRulePage_addRequestHeader_posXpath = policyRulePage_addRequestHeader_posXpath
securityRulePage_searchRequestHeader_posXpath = policyRulePage_searchRequestHeader_posXpath
securityRulePage_selectRequestHeader_posXpath = policyRulePage_selectRequestHeader_posXpath
securityRulePage_closeRequestHeader_posXpath = policyRulePage_closeRequestHeader_posXpath

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
manipulationRulePage_addCondition_posXpath = policyRulePage_addCondition_internalIP_posXpath
manipulationRulePage_addCondition_close_posXpath = policyRulePage_addCondition_close_posXpath
# rule 中添加condition侧滑中选择行定位
manipulationRulePage_addCondition_srcIP_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Source']/parent::*//div[normalize-space(text())='IP Address']"
manipulationRulePage_addCondition_srcGeography_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Source']/parent::*//div[normalize-space(text())='Geography']"
manipulationRulePage_addCondition_srcPort_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Source']/parent::*//div[normalize-space(text())='Port']"
manipulationRulePage_addCondition_dstcIP_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Destination']/parent::*//div[normalize-space(text())='IP Address']"
manipulationRulePage_addCondition_dstcGeography_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Destination']/parent::*//div[normalize-space(text())='Geography']"
manipulationRulePage_addCondition_serverFqdn_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Destination']/parent::*//div[normalize-space(text())='Server FQDN']"
manipulationRulePage_addCondition_serverPort_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Destination']/parent::*//div[normalize-space(text())='Port']"
manipulationRulePage_addCondition_internalIP_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Internal']/parent::*//div[normalize-space(text())='IP Address']"
manipulationRulePage_addCondition_internalPort_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Internal']/parent::*//div[normalize-space(text())='Port']"
manipulationRulePage_addCondition_externalIP_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='External']/parent::*//div[normalize-space(text())='IP Address']"
manipulationRulePage_addCondition_externalPort_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='External']/parent::*//div[normalize-space(text())='Port']"
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
# Internal Port的添加、查询、选中、关闭操作
manipulationRulePage_addInternalPort_posXpath = policyRulePage_addInternalPort_posXpath
manipulationRulePage_searchInternalPort_posXpath = policyRulePage_searchInternalPort_posXpath
manipulationRulePage_selectInternalPort_posXpath = policyRulePage_selectInternalPort_posXpath
manipulationRulePage_closeInternalPort_posXpath = policyRulePage_closeInternalPort_posXpath
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
manipulationRulePage_searchServerFqdn_posXpath = policyRulePage_searchServerFqdn_posXpath
manipulationRulePage_selectServerFqdn_posXpath = policyRulePage_selectServerFqdn_posXpath
manipulationRulePage_closeServerFqdn_posXpath = policyRulePage_closeServerFqdn_posXpath
# url的添加、查询、选中、关闭操作
manipulationRulePage_addUrl_posXpath = policyRulePage_addUrl_posXpath
manipulationRulePage_searchUrl_posXpath = policyRulePage_searchUrl_posXpath
manipulationRulePage_selectUrl_posXpath = policyRulePage_selectUrl_posXpath
manipulationRulePage_closeUrl_posXpath = policyRulePage_closeUrl_posXpath
# request header的添加、查询、选中、关闭操作
manipulationRulePage_addRequestHeader_posXpath = policyRulePage_addRequestHeader_posXpath
manipulationRulePage_searchRequestHeader_posXpath = policyRulePage_searchRequestHeader_posXpath
manipulationRulePage_selectRequestHeader_posXpath = policyRulePage_selectRequestHeader_posXpath
manipulationRulePage_closeRequestHeader_posXpath = policyRulePage_closeRequestHeader_posXpath
# action parameter deny
manipulationRulePage_deny_addResponseCodeSelectBox_posXpath ="//div[@class='panel-content']//label[normalize-space(text())='Response Code']/parent::*//i"   # resposne code 选择框
manipulationRulePage_deny_addResponseCodeSelectDropItem_posXpath ="//body/div[contains(@class, 'el-select-dropdown')]//li//span[normalize-space(text())='{replace_code}']"   # reposne code 下拉列表定位
manipulationRulePage_deny_addResponseContentSelectBox_posXpath ="//div[@class='panel-content']//label[normalize-space(text())='Response Content']/parent::*//i"   # resposne content 选择框
manipulationRulePage_deny_addResponseContentSelectDropItem_posXpath ="//body/div[contains(@class, 'el-select-dropdown')]//li//span[normalize-space(text())='{replace_type}']"   # reposne content 下拉列表定位
manipulationRulePage_deny_addResponseContentTextInput_posXpath ="//div[@id='myEditor1']"   # resposnse content text输入框  定位
manipulationRulePage_deny_addResponseContentProfileSelectBox_posXpath ="//div[@class='box-sizing']//i"   # resposne content profile  选择框  定位
manipulationRulePage_deny_searchResponseProfile_posXpath ="//div[@class='el-scrollbar']//input[@placeholder='Search']"   # resposne content search profile 对话框查询输入框
manipulationRulePage_deny_searchResponseProfileDorpItem_posXpath ="//div[@class='el-scrollbar']//div[contains(@class, 'margin-top')]/li[1]"   # resposne content search profile 对话框查询下拉列表第一个元素

# 保存策略时，ok cancel warnging定位
manipulationRulePage_enable_posXpath = securityRulePage_enable_posXpath
manipulationRulePage_okButton_yes_posId = "OK-_Edit_Home_App_anonymousComponent"
manipulationRulePage_okButton_warningYes_posXpath = "//div[@class='el-message-box__btns']//button[contains(@class, 'el-button--primary')]"




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
mainPage_policySecondLevelMenu_monitor_posId = "policy_monitor"

monitorRuleListPage_createButton_posId = "app_create-_OperateBtns_ElRow_policy_monitor_Home_App_anonymousComponent"
monitorRuleListPage_deleteButton_posId = "appDel-_OperateBtns_ElRow_policy_monitor_Home_App_anonymousComponent"
monitorRuleListPage_searchLable_posId = shapingRuleListPage_searchLable_posId
monitorRuleListPage_searchLable_dropDown_item_posXpath = "//div[contains(@class,'el-scrollbar')]//span[normalize-space(text())='{replaceValue}']"   #下拉菜单定位
monitorRuleListPage_searchLable_input_itemContent_posXpath = "//div[contains(@class,'ListItem')]//span[normalize-space(text())='{replaceValue}']/ancestor::div[contains(@class,'ListItem')]//input"   #输入item的值，replaceValue替换实际查询值
monitorRuleListPage_searchLable_searchButton_posId = "searchQuery"
monitorRuleListPage_selectRule_posXpath = "//div[contains(@class,'ly-table1')]//tbody//sapn[@class='el-checkbox__inner']"
monitorRuleListPage_tableTbody_posXpath = "//div[contains(@class,'ly-table1')]//tbody"

monitorRulePage_inputName_posXpath = "//*[@class='biFangName']//input"
monitorRulePage_mirrorTrafficButton_posXpath ='//*[text()="Mirror Traffic"]/ancestor::div[@class="el-form-item el-form-item--small"]//*[@class="el-switch is-checked"]'
monitorRulePage_packetCaptureButton_posXpath = '//*[text()="Packet Capture"]/ancestor::div[@class="el-form-item el-form-item--small"]//span[@class="el-switch__core"]'
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

monitorRulePage_addVLANIDButton_posXpath = '//*[text()="Add VLAN ID"]/ancestor::div[@class="el-form-item padding-left20 Capture_Depth el-form-item--small"]//div[@class="el-switch is-checked"]'
monitorRulePage_firstSelectMirrorProfile_posXpath='//*[@class="el-form-item padding-left20 Capture_Depth el-form-item--small"]//input[@class="el-input__inner"]'
monitorRulePage_searchMirrorProfile_posXpath = '//input[@type="search"]'
monitorRulePage_selectMirrorProfile_posXpath = "//li[@class='el-select-dropdown__item' and contains(text(),'{replaceValue}')]"
monitorRulePage_enable_posXpath = shapingRulePage_enable_posXpath
monitorRulePage_okButton_posId = "OK-_policy_monitor_write_Home_App_anonymousComponent"
monitorRulePage_warningYes_posXpath =shapingRulePage_okButton_warningYes_posXpath
monitorRuleListPage_warningYes_posXpath = "//button[@class='el-button delComponents-ok role-disconnect-btn el-button--default el-button--small']"