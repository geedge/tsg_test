mainPage_navigationBar_logo_posCss = ".tsg-img-logo"
mainPage_button_menu_posXCss = ".menu-btn span"    #menu按钮定位
mainPage_objectSearch_buttonSearch_posId = "searchQuery"  # 查询按钮id
mainPage_currentPage_vsysName_posXpath = "//span[@class='root-title']"    # 当前页面中vsys name
mainPage_vsysTree_vsysName_posXpath = "//div[contains(@class, 'menu-level2')]//article//div[@class='menu-title']"    # vsys tree中vsys name定位
mainPage_firstLevelMenu_Objects_posId = "object"  # 一级菜单Global Objects
mainPage_secondLevelMenu_ipAddress_posId = "Objects_ip"  # 二级菜单IP Addresses
mainPage_secondLevelMenu_port_posId = "Objects_port"
mainPage_secondLevelMenu_httpSignature_posId = "Objects_http_signature"
mainPage_secondLevelMenu_url_posId = "Objects_url"
mainPage_secondLevelMenu_fqdn_posId = "Objects_fqdn"  # 二级菜单IP Addresses

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