mainPage_navigationBar_logo_posCss = ".tsg-img-logo"

# shaping
mainPage_firstLevelMenu_policy_posId = "policy"  # 一级菜单Policies
mainPage_secondLevelMenu_shaping_posId = "policy_trafficShaping"  # 二级菜单Shaping

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
shapingRulePage_addCondition_srcIP_posXpath = "//div[@class='MultipleSelect SourceModuleSelect']//i[@class='iconfont icon-Create1 cursor']"
shapingRulePage_searchSrcIP_posXpath = "//div[@class='SourceList list-box']//div[contains(@class, 'object-item-seach')]//input"
shapingRulePage_selectSrcIP_posXpath = "//div[@class='reference-box el-popover__reference']//div[@class='row-content-cell']"
shapingRulePage_addProfile_posXpath = "//div[@class='MultipleSelect FlagSelect']//div[contains(@class, 'addobject')]"
shapingRulePage_searchProfile_posXpath = "//div[@class='SFFList list-box']//div[contains(@class, 'object-item-seach')]//input"
shapingRulePage_selectProfile_posXpath = "//div[@class='row-content-cell cursorPointer']//div[@class='UaPopover ObjectPopover popover']"
shapingRulePage_enable_posXpath = "//span[@class='el-switch__core']"
shapingRulePage_okButton_yes_posId = "OK-_policy_shaping_write_Home_App_anonymousComponent"
shapingRulePage_okButton_warningYes_posXpath = "//button[@class='el-button el-button--default el-button--small el-button--primary operation-confirm']"
