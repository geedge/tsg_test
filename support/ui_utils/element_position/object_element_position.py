mainPage_navigationBar_logo_posCss = ".tsg-img-logo"
mainPage_button_menu_posXCss = ".menu-btn span"    #menu按钮定位
mainPage_objectSearch_buttonSearch_posId = "searchQuery"  # 查询按钮id
mainPage_currentPage_vsysName_posXpath = "//span[@class='root-title']"    # 当前页面中vsys name
mainPage_vsysTree_vsysName_posXpath = "//div[contains(@class, 'menu-level2')]//article//div[@class='menu-title']/parent::*"    # vsys tree中vsys name定位
mainPage_firstLevelMenu_Objects_posId = "object"  # 一级菜单Global Objects
mainPage_secondLevelMenu_ipAddress_posId = "Objects_ip"  # 二级菜单IP Addresses
mainPage_secondLevelMenu_port_posId = "Objects_port"
mainPage_secondLevelMenu_httpSignature_posId = "Objects_http_signature"
mainPage_secondLevelMenu_keywords_posId = "Objects_keywords"
mainPage_secondLevelMenu_url_posId = "Objects_url"
mainPage_secondLevelMenu_mobileIdentify_posId = "Objects_mobile_identity"
mainPage_secondLevelMenu_fqdn_posId = "Objects_fqdn"  # 二级菜单IP Addresses
mainPage_secondLevelMenu_appliactionGroup_posId = "Application_appGroups"  # 二级菜单App Group

#Object Group公共定位
ObjectListPage_searchLabel_posId = "select-label"  # 查询框id
ObjectListPage_deleteButton_warningYes_posXpath = "//button[@class='el-button delComponents-ok role-disconnect-btn el-button--default el-button--small']"
ObjectListPage_deleteButton_warningNo_posCss = "body>.el-dialog__wrapper .delComponents-close span"
ObjectListPage_allSelect_posXpath = "//div[@class='page-box-containcheck']//label[contains(@class, 'allCheckbox')]/span/span"
ObjectListPage_tableTbody_posXpath = "//div[contains(@class,'ly-table1')]//tbody"
ObjectPage_statistics_select_posId = "statistics_select"
ObjectPage_statistics_select_option_posXpath = "//div[@class='statistics-title'][normalize-space(text())='{}']/.."#"//div[@class='el-select-dropdown__wrap el-scrollbar__wrap']/ul/li/div[@class='statistics-title'][normalize-space(text())='Elaborate']/.."
groupObjectPage_inputName_posXpath="//*[@class='biFangName']//input"#input_name
groupObjectPage_addSubordinate_posXpath="//div[@data-desc='subObject']//div[@class='addobject width300px addobject-long-list obj-content-null cursorPointer borderColor']"#add sub……+
groupObjectPage_searchSubordinate_posXpath="//div[@class='CommonListDetail list-detail']//input[@id='object_ip_search']" #search_sub 输入框替换值name
groupObjectPage_selectSubordinate_posXpath="//div[@class='reference-box el-popover__reference']//span[normalize-space(text())='{replaceValue}']"#select_sub 替换值name
groupObjectPage_closeSubordinate_posXpath='//div[contains(@class,"list-box")]' #close_sub  替换值type
groupObjectPage_addSubordinateObject_posId="temporary_form" #再次add sub的按钮
groupObjectPage_enableExclude_posXpath="//span[@class='el-switch__core']"#enable exclude
groupObjectPage_addExclude_posXpath="//div[@data-desc='exclude subObject']//div[@class='addobject width300px addobject-long-list obj-content-null cursorPointer borderColor']"#addexclude
groupObjectPage_searchExclude_posXpath="//div[@class='CommonListDetail list-detail']//input[@id='object_ip_search']"    #search_sub 输入框替换值name
groupObjectPage_selectExclude_posXpath="//div[@class='reference-box el-popover__reference']//span[normalize-space(text())='{replaceValue}']"   #select_sub 替换值name
groupObjectPage_closeExclude_posXpath=groupObjectPage_closeSubordinate_posXpath  #close_sub  替换值type
groupObjectPage_addExcludeObject_posId=groupObjectPage_addSubordinateObject_posId #再次add sub的按钮

#app group
applicationGroupobjectListPage_createButton_posId="app_create-_OperateBtns_ElCol_ElRow_Application_appGroups_Home_App_anonymousComponent"#create_button
applicationGroupObjectPage_okButton_posId = "OK-_AppGroupDetail_Home_App_anonymousComponent" # OK按钮
appllicationGroupObjectPage_okButton_warningYes_posXpath = "//div[@class='el-message-box__wrapper']//button[contains(@class, 'el-button--primary operation-confirm')]//span"
applicationGroupObjectListPage_deleteButton_posId = id="appDel-_OperateBtns_ElCol_ElRow_Application_appGroups_Home_App_anonymousComponent"

# ip object
ipObjectListPage_createButton_posId = "objectCreate-_OperateBtns_ElRow_Objects_ip_Home_App_anonymousComponent"  # create按钮id
ipObjectListPage_dropDown_createButton_posId = 'object0-_OperateBtns_ElRow_Objects_ip_Home_App_anonymousComponent'  # 从下拉菜单中选择Address
ipObjectListPage_dropDown_createGroupButton_posId = "object1-_OperateBtns_ElRow_Objects_ip_Home_App_anonymousComponent"
ipObjectListPage_searchLabel_posId = "select-label"  # 查询框id
ipObjectListPage_searchLabel_selectName_posXpath = '//li[@id="2-_FilteredSearch_ElRow_Objects_ip_Home_App_anonymousComponent"]'  # 查询Name
ipObjectListPage_deleteButton_posId = "appDel-_OperateBtns_ElRow_Objects_ip_Home_App_anonymousComponent"
ipObjectListPage_deleteButton_warningYes_posXpath = "//button[@class='el-button delComponents-ok role-disconnect-btn el-button--default el-button--small']"
ipObjectListPage_deleteButton_warningNo_posCss = "body>.el-dialog__wrapper .delComponents-close span"
ipObjectListPage_allSelect_posXpath = "//div[@class='page-box-containcheck']//label[contains(@class, 'allCheckbox')]/span/span"
ipObjectListPage_tableTbody_posXpath = "//div[contains(@class,'ly-table1')]//tbody" 
ipObjectPage_inputName_posXpath = "//*[@class='biFangName']//input" # name输入框Xpath
ipObjectPage_ipType_posId = "IPip"
ipObjectPage_geographyType_posId = "Geographygeo_location"
ipObjectPage_ipLearningType_posId = "IP Learningip_learning"
ipObjectPage_addItem_posId = "temporary_form"  # 添加item_id
ipObjectPage_inputItem_posXpath = '//div[@class="el-input el-input--small"]//input'
ipObjectPage_button_saveItem_posXpath = '//div/i[@class="operate-icon iconfont icon-save check"]'  # 保存item按钮
# ipObjectPage_okButton_posXpath = '//button[@id="OK-_IpDetail_Home_App_anonymousComponent"]/span'  # OK按钮
ipObjectPage_okButton_posId = "OK-_IpDetail_Home_App_anonymousComponent"  # OK按钮
ipObjectPage_okButton_warningYes_posXpath = "//div[@class='el-message-box__wrapper']//button[contains(@class, 'el-button--primary operation-confirm')]//span"
ipGroupObjectPage_selectTypeIP_posId = "IPip"
ipGroupObjectPage_selectTypeGeography_posId = "Geographygeo_location"
ipGroupObjectPage_addSubordinate_posXpath = "//div[@data-desc='subObject']//div[@class='addobject width300px addobject-long-list obj-content-null cursorPointer borderColor']"
ipGroupObjectPage_searchSubordinateIP_posXpath = "//div[@class='CommonListDetail list-detail']//input[@id='object_ip_search']"
ipGroupObjectPage_selectSubordinateIP_posXpath = "//div[@class='reference-box el-popover__reference']//span[normalize-space(text())='{replaceValue}']"
ipGroupObjectPage_closeSubordinateIP_posXpath = "//div[@class='KeywordsList list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"
ipGroupObjectPage_addSubordinateObject_posId = "temporary_form"
ipGroupObjectPage_enableExclude_posXpath = "//span[@class='el-switch__core']"
ipGroupObjectPage_addExclude_posXpath = "//div[@data-desc='exclude subObject']//div[@class='addobject width300px addobject-long-list obj-content-null cursorPointer borderColor']"
ipGroupObjectPage_searchExcludeIP_posXpath = "//div[@class='CommonListDetail list-detail']//input[@id='object_ip_search']"
ipGroupObjectPage_selectExcludeIP_posXpath = "//div[@class='reference-box el-popover__reference']//span[normalize-space(text())='{replaceValue}']"
ipGroupObjectPage_closeExcludeIP_posXpath = "//div[@class='KeywordsList list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"
ipGroupObjectPage_addExcludeObject_posId = "temporary_form"

# imsi object
mobile_identitiesObjectListPage_createButton_posId = "objectCreate-_OperateBtns_ElRow_Objects_mobile_identity_Home_App_anonymousComponent"  # create按钮id
mobile_identitiesObjectListPage_dropDown_createButton_posId = 'object0-_OperateBtns_ElRow_Objects_mobile_identity_Home_App_anonymousComponent'  # 从下拉菜单中选择Mobile Identity
ipObjectListPage_dropDown_createGroupButton_posId = "object1-_OperateBtns_ElRow_Objects_mobile_identity_Home_App_anonymousComponent"
imsiObjectListPage_searchLabel_posId = ipObjectListPage_searchLabel_posId = "select-label"  # 查询框id
imsiObjectListPage_searchLabel_selectName_posXpath = '//li[@id="2-_FilteredSearch_ElRow_Objects_mobile_identity_Home_App_anonymousComponent"]'  # 查询Name
imsiObjectListPage_deleteButton_posId = "appDel-_OperateBtns_ElRow_Objects_mobile_identity_Home_App_anonymousComponent"
imsiObjectListPage_deleteButton_warningYes_posXpath = ipObjectListPage_deleteButton_warningYes_posXpath 
ipObjectListPage_deleteButton_warningNo_posCss = "body>.el-dialog__wrapper .delComponents-close span"
imsiObjectListPage_allSelect_posXpath = ipObjectListPage_allSelect_posXpath
imsiObjectListPage_tableTbody_posXpath = ipObjectListPage_tableTbody_posXpath
mobile_identitiesObjectPage_inputName_posXpath = ipObjectPage_inputName_posXpath # name输入框Xpath
imsiObjectPage_imsiType_posId = "IMSIimsi"
imsiObjectPage_addItem_posId = ipObjectPage_addItem_posId  # 添加item_id
imsiObjectPage_inputItem_posXpath = '//div[@class="rel-input el-input el-input--small"]//input'
imsiObjectPage_button_saveItem_posXpath = '//div/i[@class="operate-icon iconfont icon-save save-color"]'  # 保存item按钮
imsiObjectPage_okButton_posId = "OK-_mobileIdDetail_Home_App_anonymousComponent"  # OK按钮
imsiObjectPage_okButton_warningYes_posXpath = ipObjectPage_okButton_warningYes_posXpath


# port
portObjectListPage_createButton_posId = "objectCreate-_OperateBtns_ElRow_Objects_port_Home_App_anonymousComponent"
portObjectListPage_deleteButton_posId = "appDel-_OperateBtns_ElRow_Objects_port_Home_App_anonymousComponent"
portObjectListPage_deleteButton_warningYes_posXpath = "//button[@class='el-button delComponents-ok role-disconnect-btn el-button--default el-button--small']"
portObjectListPage_deleteButton_warningNo_posCss = "//button[@class='el-button delComponents-ok role-disconnect-btn el-button--default el-button--small']"
portObjectListPage_dropDown_createButton_posId = "object0-_OperateBtns_ElRow_Objects_port_Home_App_anonymousComponent"
portObjectListPage_searchLabel_posId = "select-label"
portObjectListPage_searchLabel_selectName_posXpath = "//li[@id='2-_FilteredSearch_ElRow_Objects_port_Home_App_anonymousComponent']"
portObjectListPage_allSelect_posXpath = "//div[@class='page-box-containcheck']//label[contains(@class, 'allCheckbox')]/span/span"
portObjectListPage_tableTbody_posXpath = "//div[contains(@class,'ly-table1')]//tbody"
portObjectPage_inputName_posXpath = "//*[@class='biFangName']//input"
portObjectPage_addItem_posId = "temporary_form"
portObjectPage_inputItem_posXpath = "//div[@class='port-input el-input el-input--small']//input"
portObjectPage_button_saveItem_posXpath = "//div/i[@class='operate-icon iconfont icon-save check']"
portObjectPage_okButton_posId= "OK-_PortDetail_Home_App_anonymousComponent"
portObjectPage_okButton_warningYes_posXpath = "//button[@class='el-button el-button--default el-button--small el-button--primary operation-confirm']//span"

# fqdn
fqdnObjectListPage_createButton_posId = "objectCreate-_OperateBtns_ElRow_Objects_fqdn_Home_App_anonymousComponent"  # create按钮id
fqdnObjectListPage_dropDown_createButton_posId = 'object0-_OperateBtns_ElRow_Objects_fqdn_Home_App_anonymousComponent'  # 从下拉菜单中选择FQDN
fqdnObjectListPage_dropDown_createGroupButton_posId = "object1-_OperateBtns_ElRow_Objects_fqdn_Home_App_anonymousComponent"
fqdnObjectListPage_searchLabel_posId = "select-label"  # 查询框id
fqdnObjectListPage_searchLabel_selectName_posXpath = '//li[@id="2-_FilteredSearch_ElRow_Objects_fqdn_Home_App_anonymousComponent"]'  # 查询Name
fqdnObjectListPage_tableTbody_posXpath = "//div[contains(@class,'ly-table1')]//tbody" 
fqdnObjectListPage_deleteButton_posId = "appDel-_OperateBtns_ElRow_Objects_fqdn_Home_App_anonymousComponent"
fqdnObjectListPage_deleteButton_warningYes_posXpath = "//button[@class='el-button delComponents-ok role-disconnect-btn el-button--default el-button--small']"
fqdnObjectListPage_deleteButton_warningNo_posCss = "body>.el-dialog__wrapper .delComponents-close span"
fqdnObjectListPage_allSelect_posXpath = "//div[@class='page-box-containcheck']//label[contains(@class, 'allCheckbox')]/span/span"
fqdnObjectListPage_tableTbody_posXpath = "//div[contains(@class,'ly-table1')]//tbody" 
fqdnObjectPage_inputName_posXpath = "//*[@class='biFangName']//input" # name输入框Xpath
fqdnObjectPage_addItem_posId = "temporary_form"  # 添加item_id
fqdnObjectPage_inputItem_posXpath = '//div[@class="rel-input el-input el-input--small"]//input'
fqdnObjectPage_button_saveItem_posXpath = '//div/i[@class="operate-icon iconfont icon-save save-color"]'  # 保存item按钮
fqdnObjectPage_okButton_posId = "OK-_FqdnDetail_Home_App_anonymousComponent"  # OK按钮
fqdnObjectPage_okButton_warningYes_posXpath = "//div[@class='el-message-box__wrapper']//button[contains(@class, 'el-button--primary operation-confirm')]//span"

# http signature
httpSignatureObjectListPage_createButton_posId = "objectCreate-_OperateBtns_ElRow_Objects_http_signature_Home_App_anonymousComponent"
httpSignatureObjectListPage_deleteButton_posId = "appDel-_OperateBtns_ElRow_Objects_http_signature_Home_App_anonymousComponent"
httpSignatureObjectListPage_deleteButton_warningYes_posXpath = "//button[@class='el-button delComponents-ok role-disconnect-btn el-button--default el-button--small']"
# httpSignatureObjectListPage_deleteButton_warningNo_posCss
httpSignatureObjectListPage_dropDown_createButton_posId = "object0-_OperateBtns_ElRow_Objects_http_signature_Home_App_anonymousComponent"
httpSignatureObjectListPage_searchLabel_posId = "select-label"
httpSignatureObjectListPage_searchLabel_selectName_posXpath = "//li[@id='2-_FilteredSearch_ElRow_Objects_http_signature_Home_App_anonymousComponent']"
httpSignatureObjectListPage_allSelect_posXpath = "//div[@class='page-box-containcheck']//label[contains(@class, 'allCheckbox')]/span/span"
httpSignatureObjectListPage_tableTbody_posXpath = "//div[contains(@class,'ly-table1')]//tbody"
httpSignatureObjectPage_inputName_posXpath = "//*[@class='biFangName']//input"
httpSignatureObjectPage_addItem_posId = "temporary_form"
httpSignatureObjectPage_item_key_dropDown_posXpath = "//div[@class='SelectInput district-select']//div[@class='el-select inline-input el-select--small']//input"
httpSignatureObjectPage_item_key_dropDown_select_posXpath = "//span[normalize-space(text())='{replaceValue}']"
httpSignatureObjectPage_item_value_select_posXpath  = "//span[normalize-space(text())='{replaceValue}']"
httpSignatureObjectPage_inputItem_posXpath = "//div[@class='expr-collection Expressions']//div[{replaceValue}]//input"
httpSignatureObjectPage_item_value_plus_posXpath = "//i[@class='iconfont icon-Create1 cursor']"
httpSignatureObjectPage_button_saveItem_posXpath = "//div/i[@class='operate-icon iconfont icon-save check']"
httpSignatureObjectPage_okButton_posId = "OK-_HttpSigDetail_Home_App_anonymousComponent"
httpSignatureObjectPage_okButton_warningYes_posXpath = "//button[@class='el-button el-button--default el-button--small el-button--primary operation-confirm']//span"

# url
urlObjectListPage_createButton_posId = "objectCreate-_OperateBtns_ElRow_Objects_url_Home_App_anonymousComponent"
urlObjectListPage_deleteButton_posId = "appDel-_OperateBtns_ElRow_Objects_url_Home_App_anonymousComponent"
urlObjectListPage_dropDown_createButton_posId = "object0-_OperateBtns_ElRow_Objects_url_Home_App_anonymousComponent"
urlObjectPage_inputName_posXpath = ipObjectPage_inputName_posXpath
urlObjectPage_addItem_posId = ipObjectPage_addItem_posId
urlObjectPage_inputItem_posXpath = "//div[@class='item-box']//input"     # input 输入框，简单的第一个定位，后期优化
urlObjectPage_saveItem_posXpath = "//div[@class='item-box']//i[contains(@class, 'save-color')]"     # input item保存，简单的第一个定位，后期优化
urlObjectPage_okButton_posId = "OK-_URLDetail_Home_App_anonymousComponent"
urlObjectPage_okButton_warningYes_posXpath = httpSignatureObjectPage_okButton_warningYes_posXpath
# 查询
urlObjectPage_searchLabel_posId = httpSignatureObjectListPage_searchLabel_posId
urlObjectListPage_searchLabel_selectName_posXpath = "//*[@id='2-_FilteredSearch_ElRow_Objects_url_Home_App_anonymousComponent']"
urlObjectPage_tableTbody_posXpath = httpSignatureObjectListPage_tableTbody_posXpath
urlObjectPage_allSelect_posXpath = httpSignatureObjectListPage_allSelect_posXpath
urlObjectListPage_deleteButton_warningYes_posXpath = httpSignatureObjectListPage_deleteButton_warningYes_posXpath


# keywords
keywordsObjectListPage_createButton_posId = "objectCreate-_OperateBtns_ElRow_Objects_keywords_Home_App_anonymousComponent"
keywordsObjectListPage_deleteButton_posId = "appDel-_OperateBtns_ElRow_Objects_keywords_Home_App_anonymousComponent"
keywordsObjectListPage_deleteButton_warningYes_posXpath = httpSignatureObjectListPage_deleteButton_warningYes_posXpath
# httpSignatureObjectListPage_deleteButton_warningNo_posCss
keywordsObjectListPage_dropDown_createButton_posId = "object0-_OperateBtns_ElRow_Objects_keywords_Home_App_anonymousComponent"
keywordsObjectListPage_searchLabel_posId = httpSignatureObjectListPage_searchLabel_posId
keywordsObjectListPage_searchLabel_selectName_posXpath = "//li[@id='2-_FilteredSearch_ElRow_Objects_keywords_Home_App_anonymousComponent']"
keywordsObjectListPage_allSelect_posXpath = httpSignatureObjectListPage_allSelect_posXpath
keywordsObjectListPage_tableTbody_posXpath = httpSignatureObjectListPage_tableTbody_posXpath
keywordsObjectPage_inputName_posXpath = httpSignatureObjectPage_inputName_posXpath
keywordsObjectPage_addItem_posId = httpSignatureObjectPage_addItem_posId
httpSignatureObjectPage_item_key_dropDown_posXpath = "//div[@class='SelectInput district-select']//div[@class='el-select inline-input el-select--small']//input"
httpSignatureObjectPage_item_key_dropDown_select_posXpath = "//span[normalize-space(text())='{replaceValue}']"
keywordsObjectPage_item_value_select_posXpath  = "//span[normalize-space(text())='{replaceValue}']"
keywordsObjectPage_inputItem_posXpath = "//div[@class='expr-collection Expressions']//div[{replaceValue}]//input"
keywordsObjectPage_item_value_plus_posXpath = "//i[@class='iconfont icon-Create1 cursor']"
keywordsObjectPage_button_saveItem_posXpath = "//div/i[@class='operate-icon iconfont icon-save check']"
keywordsObjectPage_okButton_posId = "OK-_keywordsDetail_Home_App_anonymousComponent"
keywordsObjectPage_okButton_warningYes_posXpath = "//button[@class='el-button el-button--default el-button--small el-button--primary operation-confirm']//span"






