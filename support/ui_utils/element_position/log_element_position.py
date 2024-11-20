#mainPage_navigationBar_logo_posXpath = ".tsg-img-logo"
mainPage_secondLevelMenu_ipAddress_posXpath = '(//span[@class="MuiTypography-root MuiTypography-body1 MuiListItemText-primary css-1cxrtde"])[1]'
mainPage_navigationBar_logo_posXpath = mainPage_secondLevelMenu_ipAddress_posXpath    # 改为引用dashboard路径
# mainPage_button_menu_posXCss = ".menu-btn span"    #menu按钮定位
# mainPage_logSearch_buttonSearch_posId = "searchQuery"  # 查询按钮id
# mainPage_currentPage_vsysName_posXpath = "//span[@class='root-title']"    # 当前页面中vsys name
# mainPage_vsysTree_vsysName_posXpath = "//div[contains(@class, 'menu-level2')]//article//div[@class='menu-title']/parent::*"    # vsys tree中vsys name定位
#mainPage_navigationBar_logo_posCss = ".tsg-img-logo"
mainPage_firstLevelMenu_dashboards_posCss = '//span[text()="Dashboards"]'
mainPage_navigationBar_logo_posCss = mainPage_firstLevelMenu_dashboards_posCss    # 改为引用dashboard路径
mainPage_button_menu_posXCss = '//span[@class="text-[14px] font-normal MuiBox-root css-98rk20"]'    #menu按钮定位
mainPage_logSearch_buttonSearch_posId = '//i[@class="iconfont icon-sousuo text-[19px]"]'  # 查询按钮id
mainPage_currentPage_vsysName_posXpath = '//div[@class="MuiBox-root css-0"]'   # 当前页面中vsys name
mainPage_vsysTree_vsysName_posXpath = '//span[@class="vsysItem"]'   # vsys tree中vsys name定位
mainPage_firstLevelMenu_logs_posId = "Log"  # 一级菜单Global Objects
mainPage_secondLevelMenu_sessionRecords_posId = '//div[@class="MuiListItem-root MuiListItem-gutters menu-session-record-log css-1l56wwh"]'  # 二级菜单IP Addresses

#Logs界面公共定位
logListPage_addFilterButton_posId = '//div[@class="flex flex-row flex-1 items-center overflow-hidden"]/button' #Logs列表界面的Add Filter按钮定位
logListPage_enterModelButton_posId = '//i[@class="iconfont icon-wenzi text-[16px] cursor-pointer mx-[8px]"]' #Logs列表搜索条件切换输入模式按钮：选择模式样式：el-tooltip iconfont facedted-search-icon icon-wenzi；输入模式样式：el-tooltip iconfont facedted-search-icon icon-screen
logListPage_clearButton_posId = "facedClear" #Logs列表搜索条件清空按钮
logListPage_queryButton_posId = '//i[@class="iconfont icon-sousuo text-[19px]"]' #Logs列表搜索按钮
logListPage_enterModel_posXpath = "//span[@role='presentation']" #Logs列表搜索条件输入框
logListPage_totalText_posXpath = "//div[@class='search-addition-info search-row']//div[1]" #Total信息定位
logListPage_searchField_input_posXpath = "//div[@class='el-input el-input--small el-input--suffix is-focus']/input" # 点击Add Filter按钮后的输入框
logListPage_searchRuleList_operation_posXpath = "//span[@id='{}']" #operatorhas\operatornotEmpty\operatorempty
logListPage_search_text_area_posXpath = "//textarea[@id='TextSearch']"