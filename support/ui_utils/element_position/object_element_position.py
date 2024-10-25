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
mainPage_secondLevelMenu_keywords_posXpath = '//*[@class="MuiListItemText-root css-1wojmrk"]//span[normalize-space(text())="Keywords"]'
mainPage_secondLevelMenu_url_posXpath = "//span[text()='URLs']"
mainPage_secondLevelMenu_mobileIdentify_posXpath = "//div[@class='MuiListItemText-root css-1wojmrk']//span[text()='Mobile Identities']"
mainPage_secondLevelMenu_fqdn_posXpath = "//div[@class='MuiCollapse-wrapper MuiCollapse-vertical css-hboir5']//span[text()='FQDNs']"  # 二级菜单 fqdn
mainPage_secondLevelMenu_subid_posXpath = "//div[@class='MuiCollapse-wrapper MuiCollapse-vertical css-hboir5']//span[text()='Subscriber IDs']"  # 二级菜单sub id
mainPage_secondLevelMenu_apn_posXpath = "//div[@class='MuiCollapse-wrapper MuiCollapse-vertical css-hboir5']//span[text()='APNs']"  # 二级菜单apn
mainPage_secondLevelMenu_appliactionGroup_posId = "Application_appGroups"  # 二级菜单App Group
mainPage_secondLevelMenu_account_posXpath = '//*[@class="MuiListItemText-root css-1wojmrk"]//span[normalize-space(text())="Accounts"]'
mainPage_secondLevelMenu_flag_posXpath = '//*[@class="MuiListItemText-root css-1wojmrk"]//span[normalize-space(text())="Flags"]'

# Object 列表公共部分定位
objectListPage_search_input_posXpath = "//div[contains(@class,'MuiAutocomplete-wrapper MuiAutocomplete-multiple')]//input[contains(@class,'MuiAutocomplete-input')]" #Object 列表搜索input框定位：
objectListPage_search_dropDown_item_posXpath = "//ul[@role='listbox']//li//div//span[normalize-space(text())='{replaceValue}']/.."
objectListPage_search_button_posXpath = "//*[@class='MuiButtonBase-root MuiButton-root MuiButton-text MuiButton-textPrimary MuiButton-sizeSmall MuiButton-textSizeSmall MuiButton-colorPrimary MuiButton-root MuiButton-text MuiButton-textPrimary MuiButton-sizeSmall MuiButton-textSizeSmall MuiButton-colorPrimary css-1afa66w']"
objectListPage_tableTbody_posXpath = "//*[@class='MuiDataGrid-virtualScrollerRenderZone css-1inm7gi']"
objectListPage_allSelect_posXpath = "//div[@class='flex flex-row flex-wrap justify-start items-center pl-[18px] mt-[20px]']//*[@class='MuiCheckbox-action css-kit57i']/parent::span[last()]//input"
objectListPage_full_text_search_dropDown_item_posXpath = "//ul[@role='listbox']//li[1]" # Object全文检索串
objectListPage_handleButton_posXpath = "//i[@class='iconfont icon-{replaceName}']/parent::*/parent::*" # Object 列表Create、Edit、Delete、Link等操作按钮根据名称定位
objectListPage_dropDown_createButton_posXpath = "//li[@class='MuiMenuItem-root MuiMenuItem-colorNeutral MuiMenuItem-variantPlain {}-item css-1rt9hnn']"
#Object Group公共定位
ObjectListPage_searchLabel_posId = "select-label"  # 查询框id
ObjectListPage_deleteButton_warningYes_posXpath = "//button[@class='el-button delComponents-ok role-disconnect-btn el-button--default el-button--small']"
ObjectListPage_deleteButton_warningNo_posCss = "body>.el-dialog__wrapper .delComponents-close span"
ObjectListPage_allSelect_posXpath = "//div[@class='page-box-containcheck']//label[contains(@class, 'allCheckbox')]/span/span"
ObjectListPage_tableTbody_posXpath = "//div[contains(@class,'ly-table1')]//tbody"
ObjectPage_statistics_select_posXpath = "//label[normalize-space(text())='Statistics']/parent::div//button"
ObjectPage_statistics_select_option_posXpath = "//li//*[normalize-space(text())='{}']/parent::*"#//ul[contains(@class,'base-Popper-root MuiSelect-listbox Mui-expanded css-1ufo3gk')]
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

objectPage_inputName_posXpath = '//input[@class="MuiInput-input css-fqt4w4"]' # name输入框Xpath
objectPage_addItem_button_posXpath = "//div[@class='mt-[10px] flex justify-center']/button" #添加Item按钮#//div[@class='mt-[10px] flex justify-center']//i[contains(@class,'icon-Create1')]
objectPage_addItemSubstring_button_posXpath = "//div[@class='form-list-row css-xpbhx9']//div[@class='MuiBox-root css-0']//i[@class='iconfont icon-Create1 font-[700]']" #添加Item 子串按钮
objectPage_item_input_posXpath = "(//div[@class='form-list-row css-xpbhx9']//div[@class='MuiBox-root css-0']//input[@class='MuiInput-input css-1u0jcuo'])[last()]" #根据UI特性获取最后一个Item子串输入框
objectPage_saveItem_posXpath = "//div[@class='MuiTableCell-root MuiTableCell-sizeMedium css-zhiahd']//i[@class='operate-icon iconfont icon-save']"
objectPage_okButton_posXpath = "//div[@class='form-action bg-[--color-background] flex justify-center py-[12px] absolute bottom-0 w-full']//button[normalize-space(text())='OK']" #Object界面保存对象按钮

#app group
applicationGroupobjectListPage_createButton_posId="app_create-_OperateBtns_ElCol_ElRow_Application_appGroups_Home_App_anonymousComponent"#create_button
applicationGroupObjectPage_okButton_posId = "OK-_AppGroupDetail_Home_App_anonymousComponent" # OK按钮
appllicationGroupObjectPage_okButton_warningYes_posXpath = "//div[@class='el-message-box__wrapper']//button[contains(@class, 'el-button--primary operation-confirm')]//span"
applicationGroupObjectListPage_deleteButton_posId = id="appDel-_OperateBtns_ElCol_ElRow_Application_appGroups_Home_App_anonymousComponent"

# ip object
ipObjectListPage_createButton_posXpath= '//span[@class="action-create inline-flex mr-[8px] "]/button' # create按钮id
ipObjectListPage_dropDown_createButton_posXpath = '//li[@class="MuiMenuItem-root MuiMenuItem-colorNeutral MuiMenuItem-variantPlain ip-item css-1rt9hnn"]'  # 从下拉菜单中选择Address
ipObjectListPage_dropDown_createGroupButton_posId = "object1-_OperateBtns_ElRow_Objects_ip_Home_App_anonymousComponent"
ipObjectListPage_searchLabel_posXpath = '//*[@class="MuiAutocomplete-wrapper MuiAutocomplete-multiple css-1h1ala5"]/input' # 查询框id
ipObjectListPage_searchLabel_selectName_posXpath = '//*[@class="MuiInput-input css-1u0jcuo"]'  # 查询Name
ipObjectListPage_deleteButton_posXpath = '//*[@class="action-delete inline-flex mr-[8px] "]'
ipObjectListPage_deleteButton_warningYes_posXpath = '//button[normalize-space(text())="Yes"]'
ipObjectListPage_deleteButton_warningNo_posCss = "body>.el-dialog__wrapper .delComponents-close span"
ipObjectListPage_allSelect_posXpath = objectListPage_allSelect_posXpath #'(//*[@class="MuiCheckbox-action css-kit57i"]/parent::span)[last()]//input'
ipObjectListPage_search_input_posXpath = objectListPage_search_input_posXpath
ipObjectListPage_search_dropDown_item_posXpath = objectListPage_search_dropDown_item_posXpath
ipObjectListPage_search_button_posXpath = objectListPage_search_button_posXpath
ipObjectListPage_tableTbody_posXpath = objectListPage_tableTbody_posXpath #'//*[@class="MuiDataGrid-virtualScrollerRenderZone css-1inm7gi"]'
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
imsiObjectPage_imsiType_posXpath = "//*[@class='mobile-identity-object-sub_type']//button[1]"
imsiobjectPage_addItem_posXpath = ipObjectPage_addItem_posXpath  # 添加item_id
#imsiObjectPage_inputItem_posXpath = '//div[@class="rel-input el-input el-input--small"]//input'
imsiObjectPage_inputItem_posXpath = "//div[@class='scrollbar']//input"
imsiObjectPage_button_saveItem_posXpath = "//div[@class='scrollbar']//i[@class='operate-icon iconfont icon-save']"  # 保存item按钮
imsiObjectPage_okButton_posXpath = "//div[@class='form-action bg-[--color-background] flex justify-center py-[12px] absolute bottom-0 w-full']//button[text()='OK']"  # OK按钮
imsiObjectPage_okButton_warningYes_posXpath = ipObjectPage_okButton_warningYes_posXpath
mobile_identitiesObjectListPage_createButton_posXpath = '//span[@class="action-create inline-flex mr-[8px] "]/button'  # create按钮id
mobile_identitiesObjectListPage_dropDown_createButton_posXpath = "//ul[@class='base-Popper-root MuiMenu-root Mui-expanded MuiMenu-variantOutlined MuiMenu-colorNeutral MuiMenu-sizeMd css-1iuehdr']//li[1]"  # 从下拉菜单中选择Mobile Identity
imsiObjectListPage_searchLabel_posXpath = ipObjectListPage_searchLabel_posId = "//div[@class='MuiAutocomplete-wrapper MuiAutocomplete-multiple css-1h1ala5']//input"  # 查询框id
imsiObjectListPage_searchLabel_selectName_posXpath = '//li[@id="2-_FilteredSearch_ElRow_Objects_mobile_identity_Home_App_anonymousComponent"]'  # 查询Name
imsiObjectListPage_deleteButton_posId = "//div[@class='flex justify-start items-center mr-[20px]']//span[text()='Delete']"
imsiObjectListPage_deleteButton_warningYes_posXpath = ipObjectListPage_deleteButton_warningYes_posXpath
imsiObjectListPage_allSelect_posXpath = objectListPage_allSelect_posXpath
imsiObjectListPage_search_input_posXpath = objectListPage_search_input_posXpath
imsiObjectListPage_search_dropDown_item_posXpath = objectListPage_search_dropDown_item_posXpath
imsiObjectListPage_search_button_posXpath = objectListPage_search_button_posXpath
imsiObjectListPage_tableTbody_posXpath = objectListPage_tableTbody_posXpath
mobile_identitiesObjectPage_inputName_posXpath = ipObjectPage_inputName_posXpath # name输入框Xpath


# phone number
phoneNumberObjectPage_phoneNumberType_posXpath = "//*[@class='mobile-identity-object-sub_type']//button[2]"
phoneNumberobjectPage_addItem_posXpath = ipObjectPage_addItem_posXpath  # 添加item_id
phoneNumberObjectPage_inputItem_posXpath = ipObjectPage_addItem_posXpath
phoneNumberObjectPage_button_saveItem_posXpath = '//div/i[@class="operate-icon iconfont icon-save save-color"]'  # 保存item按钮
phoneNumberObjectPage_okButton_posId = "OK-_mobileIdDetail_Home_App_anonymousComponent"  # OK按钮
phoneNumberObjectPage_okButton_warningYes_posXpath = ipObjectPage_okButton_warningYes_posXpath

# imei
imeiObjectPage_imsiType_posXpath = "//*[@class='mobile-identity-object-sub_type']//button[3]"
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
portObjectListPage_allSelect_posXpath = objectListPage_allSelect_posXpath
portObjectListPage_tableTbody_posXpath = objectListPage_tableTbody_posXpath
portObjectListPage_search_input_posXpath = objectListPage_search_input_posXpath
portObjectListPage_search_dropDown_item_posXpath = objectListPage_search_dropDown_item_posXpath
portObjectListPage_search_button_posXpath = objectListPage_search_button_posXpath
portObjectPage_inputName_posXpath = ipObjectPage_inputName_posXpath
portObjectPage_addItem_posXpath = objectPage_addItem_button_posXpath
portObjectPage_inputItem_posXpath = '//*[@class="port-object-interval"]//input'
portObjectPage_button_saveItem_posXpath = ipObjectPage_button_saveItem_posXpath
# portObjectPage_okButton_posId= "OK-_PortDetail_Home_App_anonymousComponent"
portObjectPage_okButton_posXpath = ipObjectPage_okButton_posXpath
portObjectPage_okButton_warningYes_posXpath = "//button[@class='el-button el-button--default el-button--small el-button--primary operation-confirm']//span"

# fqdn
fqdnObjectListPage_createButton_posXpath = "//div[@class='flex justify-start items-center mr-[20px]']//span[text()='Create']"  # create按钮
fqdnObjectListPage_dropDown_createButton_posXpath = "//ul[@class='base-Popper-root MuiMenu-root Mui-expanded MuiMenu-variantOutlined MuiMenu-colorNeutral MuiMenu-sizeMd css-1iuehdr']//li[1]"  # 从下拉菜单中选择FQDN
fqdnObjectListPage_dropDown_createGroupButton_posXpath = "//ul[@class='base-Popper-root MuiMenu-root Mui-expanded MuiMenu-variantOutlined MuiMenu-colorNeutral MuiMenu-sizeMd css-1iuehdr']//li[2]"
fqdnObjectListPage_searchLabel_posXpath = "//div[@class='MuiAutocomplete-wrapper MuiAutocomplete-multiple css-1h1ala5']//input" # 查询框
fqdnObjectListPage_searchLabel_selectName_posXpath = "//span[normalize-space(text())='{replaceValue}']/../.."  # 查询Name
fqdnObjectListPage_deleteButton_posXpath = "//div[@class='flex justify-start items-center mr-[20px]']//span[text()='Delete']"
fqdnObjectListPage_deleteButton_warningYes_posXpath = "//div[@class='MuiDialogActions-root flex !justify-center items-center MuiDialogActions-spacing css-vplbg4']//button[text()='Yes']"
fqdnObjectListPage_deleteButton_warningNo_posCss = "body>.el-dialog__wrapper .delComponents-close span"
fqdnObjectListPage_allSelect_posXpath = objectListPage_allSelect_posXpath
fqdnObjectListPage_tableTbody_posXpath = objectListPage_tableTbody_posXpath
fqdnObjectListPage_search_input_posXpath = objectListPage_search_input_posXpath
fqdnObjectListPage_search_dropDown_item_posXpath = objectListPage_search_dropDown_item_posXpath
fqdnObjectListPage_search_button_posXpath = objectListPage_search_button_posXpath
fqdnObjectPage_inputName_posXpath = "//*[@class='fqdn-object-name']//input" # name输入框Xpath
fqdnobjectPage_addItem_posXpath = "//div[@class='mt-[10px] flex justify-center']//i"  # 添加item_id
fqdnObjectPage_inputItem_posXpath = "//div[@class='scrollbar']//input"
fqdnObjectPage_button_saveItem_posXpath = "//div[@class='scrollbar']//i[@class='operate-icon iconfont icon-save']"  # 保存item按钮
fqdnObjectPage_okButton_posXpath = "//div[@class='form-action bg-[--color-background] flex justify-center py-[12px] absolute bottom-0 w-full']//button[text()='OK']"  # OK按钮
fqdnObjectPage_okButton_warningYes_posXpath = "//div[@class='el-message-box__wrapper']//button[contains(@class, 'el-button--primary operation-confirm')]//span"

# subid
subscriberidObjectListPage_createButton_posXpath = "//div[@class='flex justify-start items-center mr-[20px]']//span[text()='Create']"
subscriberidObjectListPage_dropDown_createButton_posXpath = "//ul[@class='base-Popper-root MuiMenu-root Mui-expanded MuiMenu-variantOutlined MuiMenu-colorNeutral MuiMenu-sizeMd css-1iuehdr']//li[1]"
subscriberidObjectPage_inputName_posXpath = '//*[@class="MuiInput-root MuiInput-variantOutlined MuiInput-colorNeutral MuiInput-sizeMd MuiInput-formControl css-uzf287"]//input'
subscriberidobjectPage_addItem_posXpath = "//div[@class='mt-[10px] flex justify-center']//i"
subscriberidObjectPage_inputItem_posXpath = "//div[@class='scrollbar']//input"
subscriberidPage_button_saveItem_posXpath = '//*[@class="flex flex-row items-center"]//i[@class="operate-icon iconfont icon-save"]'
subscriberidObjectPage_okButton_posXpath = "//div[@class='form-action bg-[--color-background] flex justify-center py-[12px] absolute bottom-0 w-full']//button[text()='OK']"
subscriberidObjectPage_okButton_warningYes_posXpath = "//div[@class='el-message-box__wrapper']//button[contains(@class, 'el-button--primary operation-confirm')]//span"
subscriberidObjectListPage_searchLabel_posXpath = "//div[@class='MuiAutocomplete-wrapper MuiAutocomplete-multiple css-1h1ala5']//input"  # 查询框id
subscriberidObjectListPage_searchLabel_selectName_posXpath ='//*[@class="base-Popper-root MuiAutocomplete-listbox css-18r31z0"]//li[3]'  # 查询Name
#subscriberidObjectListPage_tableTbody_posXpath = '//*[@class="MuiDataGrid-virtualScrollerRenderZone css-1inm7gi"]'
#subscriberidObjectListPage_allSelect_posXpath = '(//*[@class="MuiCheckbox-action css-kit57i"]/parent::span)[last()]//input'
subscriberidObjectListPage_deleteButton_posXpath = '//*[@class="action-delete inline-flex mr-[8px] "]'
subscriberiObjectListPage_deleteButton_warningYes_posXpath = '//button[normalize-space(text())="Yes"]'
subscriberidObjectListPage_searchLabel_posId = "select-label"  # 查询框id
subscriberidObjectListPage_allSelect_posXpath = objectListPage_allSelect_posXpath
subscriberidObjectListPage_search_input_posXpath = objectListPage_search_input_posXpath
subscriberidObjectListPage_search_dropDown_item_posXpath = objectListPage_search_dropDown_item_posXpath
subscriberidObjectListPage_search_button_posXpath = objectListPage_search_button_posXpath
subscriberidObjectListPage_tableTbody_posXpath = objectListPage_tableTbody_posXpath
subscriberidObjectListPage_deleteButton_posId = "appDel-_OperateBtns_ElRow_Objects_subscriberid_Home_App_anonymousComponent"

# apn
apnObjectListPage_createButton_posXpath = "//div[@class='flex justify-start items-center mr-[20px]']//span[text()='Create']"
apnObjectListPage_dropDown_createButton_posXpath = "//ul[@class='base-Popper-root MuiMenu-root Mui-expanded MuiMenu-variantOutlined MuiMenu-colorNeutral MuiMenu-sizeMd css-1iuehdr']//li[1]"
apnObjectPage_inputName_posXpath = '//*[@class="MuiInput-root MuiInput-variantOutlined MuiInput-colorNeutral MuiInput-sizeMd MuiInput-formControl css-uzf287"]//input'
apnobjectPage_addItem_posXpath = "//div[@class='mt-[10px] flex justify-center']//i"
apnObjectPage_inputItem_posXpath = "//div[@class='scrollbar']//input"
apnPage_button_saveItem_posXpath = '//*[@class="flex flex-row items-center"]//i[@class="operate-icon iconfont icon-save"]'
apnObjectPage_okButton_posXpath = "//div[@class='form-action bg-[--color-background] flex justify-center py-[12px] absolute bottom-0 w-full']//button[text()='OK']"
apnObjectPage_okButton_warningYes_posXpath = "//div[@class='el-message-box__wrapper']//button[contains(@class, 'el-button--primary operation-confirm')]//span"
apnObjectListPage_searchLabel_posXpath= "//div[@class='MuiAutocomplete-wrapper MuiAutocomplete-multiple css-1h1ala5']//input"  # 查询框id
apnObjectListPage_searchLabel_selectName_posXpath = '//*[@class="base-Popper-root MuiAutocomplete-listbox css-18r31z0"]//li[3]'  # 查询Name
apnObjectListPage_tableTbody_posXpath = '//*[@class="MuiDataGrid-virtualScrollerRenderZone css-1inm7gi"]'
apnObjectListPage_allSelect_posXpath = '(//*[@class="MuiCheckbox-action css-kit57i"]/parent::span)[last()]//input'
apnObjectListPage_deleteButton_posXpath = '//*[@class="action-delete inline-flex mr-[8px] "]'
apnObjectListPage_deleteButton_warningYes_posXpath = '//button[normalize-space(text())="Yes"]'
apnObjectListPage_searchLabel_posId = "select-label"  # 查询框id
#apnObjectListPage_allSelect_posXpath = objectListPage_allSelect_posXpath
apnObjectListPage_search_input_posXpath = objectListPage_search_input_posXpath
apnObjectListPage_search_dropDown_item_posXpath = objectListPage_search_dropDown_item_posXpath
apnObjectListPage_search_button_posXpath = objectListPage_search_button_posXpath
#apnObjectListPage_tableTbody_posXpath = objectListPage_tableTbody_posXpath
apnObjectListPage_deleteButton_posId = "appDel-_OperateBtns_ElRow_Objects_apn_Home_App_anonymousComponent"
#apnObjectListPage_deleteButton_warningYes_posXpath = "//button[@class='el-button delComponents-ok role-disconnect-btn el-button--default el-button--small']"

# http signature
httpSignatureObjectListPage_createButton_posId = "objectCreate-_OperateBtns_ElRow_Objects_http_signature_Home_App_anonymousComponent"
httpSignatureObjectListPage_deleteButton_posId = "appDel-_OperateBtns_ElRow_Objects_http_signature_Home_App_anonymousComponent"
httpSignatureObjectListPage_deleteButton_warningYes_posXpath = '//button[normalize-space(text())="Yes"]'
# httpSignatureObjectListPage_deleteButton_warningNo_posCss
httpSignatureObjectListPage_dropDown_createButton_posId = "object0-_OperateBtns_ElRow_Objects_http_signature_Home_App_anonymousComponent"
httpSignatureObjectListPage_searchLabel_posXpath = '//*[@class="MuiAutocomplete-wrapper MuiAutocomplete-multiple css-1h1ala5"]//input'
httpSignatureObjectListPage_searchLabel_selectName_posXpath = "//li[@id='2-_FilteredSearch_ElRow_Objects_http_signature_Home_App_anonymousComponent']"
httpSignatureObjectListPage_allSelect_posXpath = objectListPage_allSelect_posXpath
httpSignatureObjectListPage_search_input_posXpath = objectListPage_search_input_posXpath
httpSignatureObjectListPage_search_dropDown_item_posXpath = objectListPage_search_dropDown_item_posXpath
httpSignatureObjectListPage_search_button_posXpath = objectListPage_search_button_posXpath
httpSignatureObjectListPage_tableTbody_posXpath = objectListPage_tableTbody_posXpath
httpSignatureObjectPage_inputName_posXpath = '//*[@class="MuiInput-root MuiInput-variantOutlined MuiInput-colorNeutral MuiInput-sizeMd MuiInput-formControl css-uzf287"]//input'
httpSignatureobjectPage_addItem_posXpath = '//*[@class="mt-[10px] flex justify-center"]//i'
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
urlObjectListPage_createButton_posXpath = objectListPage_handleButton_posXpath.format(replaceName='Create')
urlObjectListPage_deleteButton_posXpath = objectListPage_handleButton_posXpath.format(replaceName='Delete')#"appDel-_OperateBtns_ElRow_Objects_url_Home_App_anonymousComponent"
urlObjectListPage_dropDown_createButton_posXpath = objectListPage_dropDown_createButton_posXpath.format("url")
urlObjectPage_inputName_posXpath = objectPage_inputName_posXpath
urlObjectPage_addItem_posXpath = objectPage_addItem_button_posXpath
urlObjectPage_addItemSubstring_button_posXpath = objectPage_addItemSubstring_button_posXpath
urlObjectPage_inputItem_posXpath = objectPage_item_input_posXpath #'//*[@class="MuiInput-input css-1u0jcuo"]'     # input 输入框，简单的第一个定位，后期优化
urlObjectPage_saveItem_posXpath = objectPage_saveItem_posXpath #"//div[@class='item-box']//i[contains(@class, 'save-color')]"     # input item保存，简单的第一个定位，后期优化
urlObjectPage_sameItem_inputItem_posXpath ='(//div[@class="item-box"]//input)[last()]'
urlObjectPage_sameItem_addItem_posXpath ='//*[@class="mt-[10px] flex justify-center"]//i'
urlObjectPage_okButton_posXpath = objectPage_okButton_posXpath
urlObjectPage_okButton_warningYes_posXpath = httpSignatureObjectPage_okButton_warningYes_posXpath
# 查询
urlObjectPage_searchLabel_posXpath = httpSignatureObjectListPage_searchLabel_posXpath
urlObjectListPage_searchLabel_selectName_posXpath = "//*[@id='2-_FilteredSearch_ElRow_Objects_url_Home_App_anonymousComponent']"
urlObjectListPage_allSelect_posXpath = objectListPage_allSelect_posXpath
urlObjectListPage_search_input_posXpath = objectListPage_search_input_posXpath
urlObjectListPage_search_dropDown_item_posXpath = objectListPage_search_dropDown_item_posXpath
urlObjectListPage_search_button_posXpath = objectListPage_search_button_posXpath
urlObjectListPage_tableTbody_posXpath = objectListPage_tableTbody_posXpath
urlObjectListPage_deleteButton_warningYes_posXpath = httpSignatureObjectListPage_deleteButton_warningYes_posXpath


# keywords
keywordsObjectListPage_createButton_posXpath = '//span[@class="action-create inline-flex mr-[8px] "]/button'
keywordsObjectListPage_deleteButton_posId = '//*[@class="action-delete inline-flex mr-[8px] "]'
keywordsObjectListPage_deleteButton_warningYes_posXpath = httpSignatureObjectListPage_deleteButton_warningYes_posXpath
# httpSignatureObjectListPage_deleteButton_warningNo_posCss
keywordsObjectListPage_dropDown_createButton_posXpath = '//li[@class="MuiMenuItem-root MuiMenuItem-colorNeutral MuiMenuItem-variantPlain keyword-item css-1rt9hnn"]'
keywordsObjectListPage_searchLabel_posXpath = httpSignatureObjectListPage_searchLabel_posXpath
keywordsObjectListPage_searchLabel_selectName_posXpath = '//*[@class="base-Popper-root MuiAutocomplete-listbox css-18r31z0"]//li[3]'
keywordsObjectListPage_tableTbody_posXpath = httpSignatureObjectListPage_tableTbody_posXpath
keywordsObjectListPage_allSelect_posXpath = objectListPage_allSelect_posXpath
keywordsObjectListPage_search_input_posXpath = objectListPage_search_input_posXpath
keywordsObjectListPage_search_dropDown_item_posXpath = objectListPage_search_dropDown_item_posXpath
keywordsObjectListPage_search_button_posXpath = objectListPage_search_button_posXpath
keywordsObjectPage_inputName_posXpath = httpSignatureObjectPage_inputName_posXpath
keywordsobjectPage_addItem_posXpath = httpSignatureobjectPage_addItem_posXpath
keywordsObjectPage_item_value_select_posXpath  = "//button[normalize-space(text())='{replaceValue}']"
keywordsObjectPage_inputItem_posXpath = "//div[contains(@class, 'pl-[40px] pt-[0!important]')]//div[{replaceValue}]//input"
keywordsObjectPage_item_value_plus_posXpath = '//*[@class="customRow css-863uk6"]//i'
keywordsObjectPage_button_saveItem_posXpath = '//*[@class="flex flex-row items-center"]//i[@class="operate-icon iconfont icon-save"]'
keywordsObjectPage_okButton_posXpath = '//*[@class="form-action bg-[--color-background] flex justify-center py-[12px] absolute bottom-0 w-full"]//button[1]'
keywordsObjectPage_okButton_warningYes_posXpath = "//button[@class='el-button el-button--default el-button--small el-button--primary operation-confirm']//span"

# account
accountObjectListPage_createButton_posXpath = '//span[@class="action-create inline-flex mr-[8px] "]/button'
accountObjectListPage_deleteButton_warningYes_posXpath = httpSignatureObjectListPage_deleteButton_warningYes_posXpath
accountObjectListPage_dropDown_createButton_posXpath = '//li[@class="MuiMenuItem-root MuiMenuItem-colorNeutral MuiMenuItem-variantPlain account-item css-1rt9hnn"]'
accountObjectPage_inputName_posXpath = keywordsObjectPage_inputName_posXpath
accountobjectPage_addItem_posXpath = keywordsobjectPage_addItem_posXpath
accountObjectPage_inputItem_posXpath = urlObjectPage_inputItem_posXpath
accountObjectPage_button_saveItem_posXpath = '//*[@class="flex flex-row items-center"]//i[@class="operate-icon iconfont icon-save"]'
accountObjectPage_okButton_posXpath = '//*[@class="form-action bg-[--color-background] flex justify-center py-[12px] absolute bottom-0 w-full"]//button[1]'
accountObjectPage_okButton_warningYes_posXpath = keywordsObjectPage_okButton_warningYes_posXpath

#flag
flagObjectListPage_createButton_posXpath = '//span[@class="action-create inline-flex mr-[8px] "]/button'
flagObjectListPage_deleteButton_posId = "appDel-_OperateBtns_ElRow_Objects_account_Home_App_anonymousComponent"
flagObjectListPage_deleteButton_warningYes_posXpath = httpSignatureObjectListPage_deleteButton_warningYes_posXpath
flagObjectListPage_dropDown_createButton_posXpath = '//*[@class="MuiMenuItem-root MuiMenuItem-colorNeutral MuiMenuItem-variantPlain flag-item css-1rt9hnn"]'
flagObjectPage_inputName_posXpath = keywordsObjectPage_inputName_posXpath
flagObjectPage_addItem_posXpath = keywordsobjectPage_addItem_posXpath
flagObjectPage_inputItem_posXpath = urlObjectPage_inputItem_posXpath
flagObjectPage_button_saveItem_posXpath = '//*[@class="flex flex-row items-center"]//i[@class="operate-icon iconfont icon-save"]'
flagObjectPage_okButton_posXpath = '//*[@class="form-action bg-[--color-background] flex justify-center py-[12px] absolute bottom-0 w-full"]//button[1]'
flagObjectPage_okButton_warningYes_posXpath = keywordsObjectPage_okButton_warningYes_posXpath
# 查询
accountObjectPage_searchLabel_posXpath = httpSignatureObjectListPage_searchLabel_posXpath
accountObjectListPage_searchLabel_selectName_posXpath = '//*[@class="base-Popper-root MuiAutocomplete-listbox css-18r31z0"]//li[2]'
accountObjectListPage_allSelect_posXpath = objectListPage_allSelect_posXpath
accountObjectListPage_search_input_posXpath = objectListPage_search_input_posXpath
accountObjectListPage_search_dropDown_item_posXpath = objectListPage_search_dropDown_item_posXpath
accountObjectListPage_search_button_posXpath = objectListPage_search_button_posXpath
accountObjectListPage_tableTbody_posXpath = objectListPage_tableTbody_posXpath
accountObjectListPage_deleteButton_posXpath = '//*[@class="action-delete inline-flex mr-[8px] "]'




