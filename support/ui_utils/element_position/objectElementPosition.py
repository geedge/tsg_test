mainPage_navigationBar_logo_posCss = ".tsg-img-logo"
mainPage_button_menu_posXCss = ".menu-btn span"    #menu按钮定位
mainPage_objectSearch_buttonSearch_posId = "searchQuery"  # 查询按钮id
mainPage_currentPage_vsysName_posXpath = "//span[@class='root-title']"    # 当前页面中vsys name
mainPage_vsysTree_vsysName_posXpath = "//div[contains(@class, 'menu-level2')]//article//div[@class='menu-title']"    # vsys tree中vsys name定位
mainPage_firstLevelMenu_Objects_posId = "object"  # 一级菜单Global Objects
mainPage_secondLevelMenu_ipAddress_posId = "Objects_ip"  # 二级菜单IP Addresses
mainPage_secondLevelMenu_port_posId = "Objects_port"

mainPage_button_menu_posXCss = ".menu-btn span"
mainPage_currentPage_vsysName_posXpath = "//span[@class='root-title']" 
mainPage_vsysTree_vsysName_posXpath = "//div[contains(@class, 'menu-level2')]//article//div[@class='menu-title']"    # vsys tree中vsys name定位

# ip object
ipObjectListPage_createButton_posId = "objectCreate-_OperateBtns_ElRow_Objects_ip_Home_App_anonymousComponent"  # create按钮id
ipObjectListPage_dropDown_createIpButton_posId = 'object0-_OperateBtns_ElRow_Objects_ip_Home_App_anonymousComponent'  # 从下拉菜单中选择Address
ipObjectListPage_searchLabel_posId = "select-label"  # 查询框id
ipObjectListPage_searchLabel_selectName_posXpath = '//li[@id="2-_FilteredSearch_ElRow_Objects_ip_Home_App_anonymousComponent"]'  # 查询Name
ipObjectListPage_deleteButton_posId = "appDel-_OperateBtns_ElRow_Objects_ip_Home_App_anonymousComponent"
ipObjectListPage_deleteButton_warningYes_posXpath = "//button[@class='el-button delComponents-ok role-disconnect-btn el-button--default el-button--small']"
ipObjectListPage_deleteButton_warningNo_posCss = "body>.el-dialog__wrapper .delComponents-close span"
ipObjectListPage_allSelect_posXpath = "//div[@class='page-box-containcheck']//label[contains(@class, 'allCheckbox')]/span/span"
ipObjectListPage_tableTbody_posXpath = "//div[contains(@class,'ly-table1')]//tbody" 
ipObjectPage_inputName_posXpath = "//*[@class='biFangName']//input" # name输入框Xpath
ipObjectPage_geographyType_posId = "Geographygeo_location"
ipObjectPage_ipLearningType_posId = "Geographygeo_location"
ipObjectPage_addItem_posId = "temporary_form"  # 添加item_id
ipObjectPage_inputItem_posXpath = '//div[@class="ip-input el-input el-input--small"]//input'
ipObjectPage_button_saveItem_posXpath = '//div/i[@class="operate-icon iconfont icon-save check"]'  # 保存item按钮
# ipObjectPage_okButton_posXpath = '//button[@id="OK-_IpDetail_Home_App_anonymousComponent"]/span'  # OK按钮
ipObjectPage_okButton_posId = "OK-_IpDetail_Home_App_anonymousComponent"  # OK按钮
ipObjectPage_okButton_warningYes_posXpath = "//div[@class='el-message-box__wrapper']//button[contains(@class, 'el-button--primary operation-confirm')]/span"

# port
portObjectListPage_createButton_posId = "objectCreate-_OperateBtns_ElRow_Objects_port_Home_App_anonymousComponent"
portObjectListPage_deleteButton_posId = "appDel-_OperateBtns_ElRow_Objects_port_Home_App_anonymousComponent"
portObjectListPage_deleteButton_warningYes_posXpath = "//button[@class='el-button delComponents-ok role-disconnect-btn el-button--default el-button--small']"
portObjectListPage_deleteButton_warningNo_posCss = "//button[@class='el-button delComponents-ok role-disconnect-btn el-button--default el-button--small']"
portObjectListPage_dropDown_createIpButton_posId = "object0-_OperateBtns_ElRow_Objects_port_Home_App_anonymousComponent"
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