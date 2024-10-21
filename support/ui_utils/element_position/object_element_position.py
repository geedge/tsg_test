#mainPage_navigationBar_logo_posXpath = ".tsg-img-logo"
mainPage_secondLevelMenu_ipAddress_posXpath = "#dashboard .level1-title"
mainPage_navigationBar_logo_posXpath = mainPage_secondLevelMenu_ipAddress_posXpath    # 改为引用dashboard路径
mainPage_button_menu_posXCss = ".menu-btn span"    #menu按钮定位
mainPage_objectSearch_buttonSearch_posXpath = '//*[@class="MuiButtonBase-root MuiButton-root MuiButton-text MuiButton-textPrimary MuiButton-sizeSmall MuiButton-textSizeSmall MuiButton-colorPrimary MuiButton-root MuiButton-text MuiButton-textPrimary MuiButton-sizeSmall MuiButton-textSizeSmall MuiButton-colorPrimary css-1afa66w"]'  # 查询按钮id
mainPage_currentPage_vsysName_posXpath = "//span[@class='root-title']"    # 当前页面中vsys name
mainPage_vsysTree_vsysName_posXpath = "//div[contains(@class, 'menu-level2')]//article//div[@class='menu-title']/parent::*"    # vsys tree中vsys name定位
mainPage_firstLevelMenu_Objects_posXpath = "//*[normalize-space(text())='Objects']" # 一级菜单Global Objects
mainPage_secondLevelMenu_ipAddress_posXpath = '//*[@class="MuiListItemText-root css-1wojmrk"]//span[normalize-space(text())="IP Addresses"]' # 二级菜单IP Addresses
# mainPage_secondLevelMenu_port_posId = "Objects_port"
mainPage_secondLevelMenu_port_posXpath = '//*[@class="MuiListItemText-root css-1wojmrk"]//span[normalize-space(text())="Ports"]' # 二级菜单Ports
mainPage_secondLevelMenu_httpSignature_posId = "Objects_http_signature"
mainPage_secondLevelMenu_keywords_posId = "Objects_keywords"
mainPage_secondLevelMenu_url_posId = "Objects_url"
mainPage_secondLevelMenu_mobileIdentify_posId = "Objects_mobile_identity"
mainPage_secondLevelMenu_fqdn_posId = "Objects_fqdn"  # 二级菜单 fqdn
mainPage_secondLevelMenu_subid_posId = "Objects_subscriberid"  # 二级菜单sub id
mainPage_secondLevelMenu_apn_posId = "Objects_apn"  # 二级菜单apn
mainPage_secondLevelMenu_appliactionGroup_posId = "Application_appGroups"  # 二级菜单App Group
mainPage_secondLevelMenu_account_posId = "Objects_account"

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
ipObjectListPage_createButton_posXpath= '//span[@class="action-create inline-flex mr-[8px] "]/button' # create按钮id
ipObjectListPage_dropDown_createButton_posXpath = '//li[@class="MuiMenuItem-root MuiMenuItem-colorNeutral MuiMenuItem-variantPlain ip-item css-1rt9hnn"]'  # 从下拉菜单中选择Address
ipObjectListPage_dropDown_createGroupButton_posId = "object1-_OperateBtns_ElRow_Objects_ip_Home_App_anonymousComponent"
ipObjectListPage_searchLabel_posXpath =  '//*[@class="MuiAutocomplete-wrapper MuiAutocomplete-multiple css-1h1ala5"]/input' # 查询框id
ipObjectListPage_searchLabel_selectName_posXpath = '//*[@class="MuiInput-input css-1u0jcuo"]'  # 查询Name
ipObjectListPage_deleteButton_posXpath = '//*[@class="action-delete inline-flex mr-[8px] "]'
ipObjectListPage_deleteButton_warningYes_posXpath = '//button[normalize-space(text())="Yes"]'
ipObjectListPage_deleteButton_warningNo_posCss = "body>.el-dialog__wrapper .delComponents-close span"
ipObjectListPage_allSelect_posXpath = '(//*[@class="MuiCheckbox-action css-kit57i"]/parent::span)[last()]//input'
ipObjectListPage_tableTbody_posXpath = '//*[@class="MuiDataGrid-virtualScrollerRenderZone css-1inm7gi"]'
ipObjectPage_inputName_posXpath = '//input[@class="MuiInput-input css-fqt4w4"]' # name输入框Xpath
ipObjectPage_ipType_posXpath = "//*[normalize-space(text())='IP']"
ipObjectPage_geographyType_posId = "Geographygeo_location"
ipObjectPage_ipLearningType_posId = "IP Learningip_learning"
ipObjectPage_addItem_posXpath = '//*[@class="iconfont icon-Create1 font-[700]"]'  # 添加item_id
ipObjectPage_inputItem_posXpath = '//*[@class="MuiAutocomplete-input css-1lv7pyi"]'
ipObjectPage_button_saveItem_posXpath = '//i[@class="operate-icon iconfont icon-save"]'  # 保存item按钮
ipObjectPage_searchLable_dropDown_item_posXpath = '//span[normalize-space(text())="Name"]/../..'
# ipObjectPage_okButton_posXpath = '//button[@id="OK-_IpDetail_Home_App_anonymousComponent"]/span'  # OK按钮
ipObjectPage_okButton_posXpath = '//div[@class="form-action bg-[--color-background] flex justify-center py-[12px] absolute bottom-0 w-full"]//button[normalize-space(text())="OK"]'# OK按钮
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
imsiObjectPage_imsiType_posId = "IMSIimsi"
imsiobjectPage_addItem_posXpath = ipObjectPage_addItem_posXpath  # 添加item_id
#imsiObjectPage_inputItem_posXpath = '//div[@class="rel-input el-input el-input--small"]//input'
imsiObjectPage_inputItem_posXpath = '//div[@class="item-box"]//div[contains(@class, "el-input el-input--small")]//input'
imsiObjectPage_button_saveItem_posXpath = '//div/i[@class="operate-icon iconfont icon-save save-color"]'  # 保存item按钮
imsiObjectPage_okButton_posId = "OK-_mobileIdDetail_Home_App_anonymousComponent"  # OK按钮
imsiObjectPage_okButton_warningYes_posXpath = ipObjectPage_okButton_warningYes_posXpath
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


# phone number
phoneNumberObjectPage_phoneNumberType_posId = "Phone Numberphone_number"
phoneNumberobjectPage_addItem_posXpath = ipObjectPage_addItem_posXpath  # 添加item_id
phoneNumberObjectPage_inputItem_posXpath = ipObjectPage_addItem_posXpath
phoneNumberObjectPage_button_saveItem_posXpath = '//div/i[@class="operate-icon iconfont icon-save save-color"]'  # 保存item按钮
phoneNumberObjectPage_okButton_posId = "OK-_mobileIdDetail_Home_App_anonymousComponent"  # OK按钮
phoneNumberObjectPage_okButton_warningYes_posXpath = ipObjectPage_okButton_warningYes_posXpath

# imei
imeiObjectPage_imsiType_posId = "IMEIimei"
imeiobjectPage_addItem_posXpath = ipObjectPage_addItem_posXpath  # 添加item_id
imeiObjectPage_inputItem_posXpath = '//div[@class="rel-input el-input el-input--small"]//input'
imeiObjectPage_button_saveItem_posXpath = '//div/i[@class="operate-icon iconfont icon-save save-color"]'  # 保存item按钮
imeiObjectPage_okButton_posId = "OK-_mobileIdDetail_Home_App_anonymousComponent"  # OK按钮
imeiObjectPage_okButton_warningYes_posXpath = ipObjectPage_okButton_warningYes_posXpath

# port
# portObjectListPage_createButton_posId = "objectCreate-_OperateBtns_ElRow_Objects_port_Home_App_anonymousComponent"
portObjectListPage_createButton_posXpath = ipObjectListPage_createButton_posXpath
#portObjectListPage_deleteButton_posId = "appDel-_OperateBtns_ElRow_Objects_port_Home_App_anonymousComponent"
portObjectListPage_deleteButton_posXpath = ipObjectListPage_deleteButton_posXpath
portObjectListPage_deleteButton_warningYes_posXpath = ipObjectListPage_deleteButton_warningYes_posXpath
portObjectListPage_deleteButton_warningNo_posCss = "//button[@class='el-button delComponents-ok role-disconnect-btn el-button--default el-button--small']"
# portObjectListPage_dropDown_createButton_posId = "object0-_OperateBtns_ElRow_Objects_port_Home_App_anonymousComponent"
portObjectListPage_dropDown_createButton_posXpath = "//*[contains(@class, 'MuiMenuItem-root') and contains(@class, 'MuiMenuItem-colorNeutral') and contains(@class, 'MuiMenuItem-variantPlain') and contains(@class, 'port-item') and contains(@class, 'css-1rt9hnn')]"
# portObjectListPage_searchLabel_posId = "select-label"
portObjectListPage_searchLabel_posXpath = ipObjectListPage_searchLabel_posXpath
portObjectListPage_searchLabel_selectName_posXpath = "//*[contains(@class, 'dune-search-option-content') and .//*[contains(text(), 'Name')] and .//*[contains(text(), 'contains')]]"
portObjectListPage_allSelect_posXpath = ipObjectListPage_allSelect_posXpath
portObjectListPage_tableTbody_posXpath = ipObjectListPage_tableTbody_posXpath
portObjectPage_inputName_posXpath = ipObjectPage_inputName_posXpath
portobjectPage_addItem_posXpath = ipObjectPage_addItem_posXpath
portObjectPage_inputItem_posXpath = '//*[@class="port-object-interval"]//input'
portObjectPage_button_saveItem_posXpath = ipObjectPage_button_saveItem_posXpath
# portObjectPage_okButton_posId= "OK-_PortDetail_Home_App_anonymousComponent"
portObjectPage_okButton_posXpath = ipObjectPage_okButton_posXpath
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
fqdnobjectPage_addItem_posXpath = "temporary_form"  # 添加item_id
fqdnObjectPage_inputItem_posXpath = '//div[@class="rel-input el-input el-input--small"]//input'
fqdnObjectPage_button_saveItem_posXpath = '//div/i[@class="operate-icon iconfont icon-save save-color"]'  # 保存item按钮
fqdnObjectPage_okButton_posId = "OK-_FqdnDetail_Home_App_anonymousComponent"  # OK按钮
fqdnObjectPage_okButton_warningYes_posXpath = "//div[@class='el-message-box__wrapper']//button[contains(@class, 'el-button--primary operation-confirm')]//span"

# subid
subscriberidObjectListPage_createButton_posId = "objectCreate-_OperateBtns_ElRow_Objects_subscriberid_Home_App_anonymousComponent"
subscriberidObjectListPage_dropDown_createButton_posId = "object0-_OperateBtns_ElRow_Objects_subscriberid_Home_App_anonymousComponent"
subscriberidObjectPage_inputName_posXpath = "//*[@class='biFangName']//input"
subscriberidobjectPage_addItem_posXpath = "temporary_form"
subscriberidObjectPage_inputItem_posXpath = '//div[@class="rel-input el-input el-input--small"]//input'
subscriberidPage_button_saveItem_posXpath = '//div/i[@class="operate-icon iconfont icon-save save-color"]'
subscriberidObjectPage_okButton_posId = "OK-_SubscriberidDetail_Home_App_anonymousComponent"
subscriberidObjectPage_okButton_warningYes_posXpath = "//div[@class='el-message-box__wrapper']//button[contains(@class, 'el-button--primary operation-confirm')]//span"
subscriberidObjectListPage_searchLabel_posId = "select-label"  # 查询框id
subscriberidObjectListPage_searchLabel_selectName_posXpath = '//li[@id="2-_FilteredSearch_ElRow_Objects_subscriberid_Home_App_anonymousComponent"]'  # 查询Name
subscriberidObjectListPage_tableTbody_posXpath = "//div[contains(@class,'ly-table1')]//tbody"
subscriberidObjectListPage_allSelect_posXpath = "//div[@class='page-box-containcheck']//label[contains(@class, 'allCheckbox')]/span/span"
subscriberidObjectListPage_deleteButton_posId = "appDel-_OperateBtns_ElRow_Objects_subscriberid_Home_App_anonymousComponent"
subscriberiObjectListPage_deleteButton_warningYes_posXpath = "//button[@class='el-button delComponents-ok role-disconnect-btn el-button--default el-button--small']"

# subid
apnObjectListPage_createButton_posId = "objectCreate-_OperateBtns_ElRow_Objects_apn_Home_App_anonymousComponent"
apnObjectListPage_dropDown_createButton_posId = "object0-_OperateBtns_ElRow_Objects_apn_Home_App_anonymousComponent"
apnObjectPage_inputName_posXpath = "//*[@class='biFangName']//input"
apnobjectPage_addItem_posXpath = "temporary_form"
apnObjectPage_inputItem_posXpath = '//div[@class="edit-row"]//input'
apnPage_button_saveItem_posXpath = '//div[@class="edit-row"]//div[@class="IconBtn"]//i[contains(class, icon-save)]'
apnObjectPage_okButton_posId = "OK-_apnDetail_Home_App_anonymousComponent"
apnObjectPage_okButton_warningYes_posXpath = "//div[@class='el-message-box__wrapper']//button[contains(@class, 'el-button--primary operation-confirm')]//span"
apnObjectListPage_searchLabel_posId = "select-label"  # 查询框id
apnObjectListPage_searchLabel_selectName_posXpath = '//li[@id="2-_FilteredSearch_ElRow_Objects_apn_Home_App_anonymousComponent"]'  # 查询Name
apnObjectListPage_tableTbody_posXpath = "//div[contains(@class,'ly-table1')]//tbody"
apnObjectListPage_allSelect_posXpath = "//div[@class='page-box-containcheck']//label[contains(@class, 'allCheckbox')]/span/span"
apnObjectListPage_deleteButton_posId = "appDel-_OperateBtns_ElRow_Objects_apn_Home_App_anonymousComponent"
apnObjectListPage_deleteButton_warningYes_posXpath = "//button[@class='el-button delComponents-ok role-disconnect-btn el-button--default el-button--small']"

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
httpSignatureobjectPage_addItem_posXpath = "temporary_form"
httpSignatureObjectPage_item_key_dropDown_posXpath = "//div[@class='SelectInput district-select']//div[@class='el-select inline-input el-select--small']//input"
httpSignatureObjectPage_item_key_dropDown_select_posXpath = "//span[normalize-space(text())='{replaceValue}']"
httpSignatureObjectPage_item_value_select_posXpath  = "//span[normalize-space(text())='{replaceValue}']"
httpSignatureObjectPage_inputItem_posXpath = "//div[@class='expr-collection Expressions']/div[{replaceValue}]//div[contains(@class, 'el-input')][{replaceValueInput}]//input"
#httpSignatureObjectPage_inputItem_posXpath = "//div[@class='expr-collection Expressions']//div[{replaceValue}]//input"
httpSignatureObjectPage_item_value_plus_posXpath = "//i[@class='iconfont icon-Create1 cursor']"
httpSignatureObjectPage_button_saveItem_posXpath = "//div/i[@class='operate-icon iconfont icon-save check']"
httpSignatureObjectPage_okButton_posId = "OK-_HttpSigDetail_Home_App_anonymousComponent"
httpSignatureObjectPage_okButton_warningYes_posXpath = "//button[@class='el-button el-button--default el-button--small el-button--primary operation-confirm']//span"

# url
urlObjectListPage_createButton_posId = "objectCreate-_OperateBtns_ElRow_Objects_url_Home_App_anonymousComponent"
urlObjectListPage_deleteButton_posId = "appDel-_OperateBtns_ElRow_Objects_url_Home_App_anonymousComponent"
urlObjectListPage_dropDown_createButton_posId = "object0-_OperateBtns_ElRow_Objects_url_Home_App_anonymousComponent"
urlObjectPage_inputName_posXpath = ipObjectPage_inputName_posXpath
urlobjectPage_addItem_posXpath = ipObjectPage_addItem_posXpath
urlObjectPage_inputItem_posXpath = "//div[@class='item-box']//input"     # input 输入框，简单的第一个定位，后期优化
urlObjectPage_saveItem_posXpath = "//div[@class='item-box']//i[contains(@class, 'save-color')]"     # input item保存，简单的第一个定位，后期优化
urlObjectPage_sameItem_inputItem_posXpath='(//div[@class="item-box"]//input)[last()]'
urlObjectPage_sameItem_addItem_posXpath='//div[@class="expr-box"]//i[@class="iconfont icon-Create1 cursor"]'
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
keywordsobjectPage_addItem_posXpath = httpSignatureobjectPage_addItem_posXpath
httpSignatureObjectPage_item_key_dropDown_posXpath = "//div[@class='SelectInput district-select']//div[@class='el-select inline-input el-select--small']//input"
httpSignatureObjectPage_item_key_dropDown_select_posXpath = "//span[normalize-space(text())='{replaceValue}']"
keywordsObjectPage_item_value_select_posXpath  = "//span[normalize-space(text())='{replaceValue}']"
keywordsObjectPage_inputItem_posXpath = "//div[contains(@class, 'expr-collection')]//div[{replaceValue}]//input"
keywordsObjectPage_item_value_plus_posXpath = "//div[@class='v-fill-available']//i"
keywordsObjectPage_button_saveItem_posXpath = "//div/i[@class='operate-icon iconfont icon-save check']"
keywordsObjectPage_okButton_posId = "OK-_keywordsDetail_Home_App_anonymousComponent"
keywordsObjectPage_okButton_warningYes_posXpath = "//button[@class='el-button el-button--default el-button--small el-button--primary operation-confirm']//span"

# account
accountObjectListPage_createButton_posId = "objectCreate-_OperateBtns_ElRow_Objects_account_Home_App_anonymousComponent"
accountObjectListPage_deleteButton_posId = "appDel-_OperateBtns_ElRow_Objects_account_Home_App_anonymousComponent"
accountObjectListPage_deleteButton_warningYes_posXpath = httpSignatureObjectListPage_deleteButton_warningYes_posXpath
accountObjectListPage_dropDown_createButton_posId = "object0-_OperateBtns_ElRow_Objects_account_Home_App_anonymousComponent"
accountObjectPage_inputName_posXpath = keywordsObjectPage_inputName_posXpath
accountobjectPage_addItem_posXpath = keywordsobjectPage_addItem_posXpath
accountObjectPage_inputItem_posXpath = urlObjectPage_inputItem_posXpath
accountObjectPage_button_saveItem_posXpath = "//div/i[@class='operate-icon iconfont icon-save check color31739C']"
accountObjectPage_okButton_posId = "OK-_accountsDetail_Home_App_anonymousComponent"
accountObjectPage_okButton_warningYes_posXpath = keywordsObjectPage_okButton_warningYes_posXpath
# 查询
accountObjectPage_searchLabel_posId = httpSignatureObjectListPage_searchLabel_posId
accountObjectListPage_searchLabel_selectName_posXpath = "//*[@id='2-_FilteredSearch_ElRow_Objects_account_Home_App_anonymousComponent']"
accountObjectPage_tableTbody_posXpath = httpSignatureObjectListPage_tableTbody_posXpath
accountObjectPage_allSelect_posXpath = httpSignatureObjectListPage_allSelect_posXpath
accountObjectListPage_deleteButton_warningYes_posXpath = httpSignatureObjectListPage_deleteButton_warningYes_posXpath
accountObjectListPage_deleteButton_posId = "appDel-_OperateBtns_ElRow_Objects_account_Home_App_anonymousComponent"




