#mainPage_navigationBar_logo_posXpath = ".tsg-img-logo"
mainPage_secondLevelMenu_ipAddress_posXpath = '(//span[@class="MuiTypography-root MuiTypography-body1 MuiListItemText-primary css-1cxrtde"])[1]'
mainPage_navigationBar_logo_posXpath = mainPage_secondLevelMenu_ipAddress_posXpath    # 改为引用dashboard路径
mainPage_policyFirstLevelMenu_posXpath = "//*[normalize-space(text())='Policies']" # 一级菜单Policies
mainPage_policySecondLevelMenu_security_posId = "Objects_ProxyInterception"
mainPage_policySecondLevelMenu_security_posXpath = "//*[contains(@class, 'MuiListItem-root') and contains(@class, 'MuiListItem-gutters') and contains(@class, 'menu-security-policy') and contains(@class, 'css-1l56wwh')]"
mainPage_policySecondLevelMenu_intercept_posId = "policy_Intercept"  # 二级菜单intercept
mainPage_policySecondLevelMenu_manipulation_posId = "policy_Manipulation"  # 二级菜单manipulatjion
mainPage_policySecondLevelMenu_shaping_posId = "policy_trafficShaping"  # 二级菜单Shaping
mainPage_policySecondLevelMenu_statistics_posXpath = "//li[contains(@class,'menu-policy')]//span[normalize-space(text())='Statistics']"  # 二级菜单Statistics
mainPage_policySecondLevelMenu_dos_posXpath = "//*[normalize-space(text())='DoS Protection']" # 二级菜单DoS Protection

mainPage_button_menu_posXCss = ".menu-btn span"
mainPage_currentPage_vsysName_posXpath = "//span[@class='root-title']" 
mainPage_vsysTree_vsysName_posXpath = "//div[contains(@class, 'menu-level2')]//article//div[@class='menu-title']/parent::*"    # vsys tree中vsys name定位

mainPage_version_posXpath = "//*[@class='header-user-con']/span[1]" #TSG Version按钮
language_button_posXpath = "//input[@id='anonymousComponent_Home_App_anonymousComponent_language']/.."#快捷切换语言按钮
policyRulePage_addSrcIP_posXpath = '//div[@class="MuiFormControl-root MuiFormControl-vertical MuiFormControl-sizeMd css-t5weby"][1]//i[@class="iconfont icon-Create1 font-[700]"]'
policyRulePage_searchSrcIP_posXpath = '//div[@class="px-[12px] py-[4px] flex"]//input'
policyRulePage_selectSrcIP_posXpath = '//ul[@class="MuiList-root MuiList-vertical MuiList-variantPlain MuiList-colorNeutral MuiList-sizeMd css-1cklc3"]//li[1]//span[@class="truncate"]'
policyRulePage_closeSrcIP_posXpath = '//div[@class="absolute bottom-0 h-[40px] w-[100%] overflow-hidden text-[16px] truncate bg-[--color-background-secondary] flex  justify-center items-center pl-[12px] pr-[38px]"]/button'
ruleListPage_createButton_posXpath = "//*[@class='action-create inline-flex mr-[8px] ']" #Rule列表上方Create按钮
ruleListPage_editButton_posXpath = "//*[@class='action-edit inline-flex mr-[8px] ']" #Rule列表上方Create按钮
ruleListPage_deleteButton_posXpath ="//*[@class='action-delete inline-flex mr-[8px] ']" #Rule列表上方Create按钮
ruleListPage_searchLabel_posXpath = "//div[contains(@class,'MuiAutocomplete-wrapper MuiAutocomplete-multiple')]//input[contains(@class,'MuiAutocomplete-input')]" #搜索输入框
ruleListPage_searchLabel_dropDown_item_posXpath = "//span[normalize-space(text())='{replaceValue}']/../.." #下拉菜单定位
ruleListPage_searchLabel_input_itemContent_posXpath = "//input[contains(@class,'MuiAutocomplete-input')]"  #输入item的值，replaceValue替换实际查询值
ruleListPage_searchLabel_searchButton_posXpath = "//*[@class='MuiButtonBase-root MuiButton-root MuiButton-text MuiButton-textPrimary MuiButton-sizeSmall MuiButton-textSizeSmall MuiButton-colorPrimary MuiButton-root MuiButton-text MuiButton-textPrimary MuiButton-sizeSmall MuiButton-textSizeSmall MuiButton-colorPrimary css-1afa66w']"
ruleListPage_tableTbody_posXpath = "//*[@class='MuiDataGrid-virtualScrollerRenderZone css-1inm7gi']" #Rule列表table
ruleListPage_allSelect_posXpath = "(//*[@class='MuiCheckbox-action css-kit57i']/parent::span)[last()]" # Rule列表选择所有搜索结果All按钮
ruleListPage_delete_tip_warning_posXpath = "//div[contains(@class,'MuiPaper-root MuiPaper-elevation MuiPaper-rounded MuiPaper-elevation24 MuiDialog-paper MuiDialog-paperScrollPaper MuiDialog-paperWidthSm')]//div[contains(@class,'text-center color-[--color-text] mt-[12px] MuiBox-root')]" #删除告警页面提示信息
ruleListPage_delete_tip_button_warningYes_posXpath = "//div[contains(@class,'MuiPaper-root MuiPaper-elevation MuiPaper-rounded MuiPaper-elevation24 MuiDialog-paper MuiDialog-paperScrollPaper MuiDialog-paperWidthSm')]//button[@type='danger']" #删除告警页面，Yes确认删除按钮
ruleListPage_delete_tip_button_warningNo_posXpath = "//div[contains(@class,'MuiPaper-root MuiPaper-elevation MuiPaper-rounded MuiPaper-elevation24 MuiDialog-paper MuiDialog-paperScrollPaper MuiDialog-paperWidthSm')]//button[contains(@class,'MuiButtonBase-root MuiButton-root MuiButton-text MuiButton-textPrimary MuiButton-sizeSmall MuiButton-textSizeSmall MuiButton-colorPrimary')]" ##删除告警页面，No取消删除按钮

rulePage_inputName_posXpath = "//*[@class='MuiInput-input css-fqt4w4']"
rulePage_button_add2Level_condition_posXpath = "//label[normalize-space(text())='{firstType}']/following-sibling::div//label[normalize-space(text())='{secondType}']/following-sibling::div/button"#多层对象添加按钮，例如：Source-IP Address policyRulePage_addSrcIP_posXpath
rulePage_button_add_condition_posXpath = "//label[normalize-space(text())='{}']/following-sibling::div//button"
# rule中侧滑列表的搜索按钮：
rulePage_object_list_search_input_posXpath = "//div[contains(@class,'MuiDrawer-content')]//input[contains(@class,'MuiInput-input')]" #Rule打开Obeject侧滑列表，搜索Object搜索框定位
rulePage_object_list_select_name_posXpath = "//ul[contains(@class,'MuiList-root MuiList-vertical MuiList-variantPlain MuiList-colorNeutral MuiList-sizeMd')]//li//*[normalize-space(text())='{replaceValue}']"#Rule打开Obeject侧滑列表，搜索后选择Object定位
rulePage_object_list_close_button_posXpath = "//div[@class='absolute bottom-0 h-[40px] w-[100%] overflow-hidden text-[16px] truncate bg-[--color-background-secondary] flex  justify-center items-center pl-[12px] pr-[38px]']//button" #Rule打开Obeject侧滑列表，列表界面的关闭按钮定位
rulePage_enable_posXpath = "//div[@class='statistics-policy-is_enabled']//span" #Rule生效/失效按钮
rulePage_okButton_posXpath = "//div[@class='form-action bg-[--color-background] flex justify-center py-[12px] absolute bottom-0 w-full']//button[1]" # OK按钮定位
rulePage_cancelButton_posXpath = "//div[@class='form-action bg-[--color-background] flex justify-center py-[12px] absolute bottom-0 w-full']//button[2]" # Cancel按钮定位
rulePage_okButton_warningYes_posXpath = ""
rulePage_okButton_warningNo_posXpath = ""
rulePage_delete_tip_warning_posXpath = "//div[contains(@class,'MuiPaper-root MuiPaper-elevation MuiPaper-rounded MuiPaper-elevation24 MuiDialog-paper MuiDialog-paperScrollPaper MuiDialog-paperWidthSm')]//div[contains(@class,'text-center color-[--color-text] mt-[12px] MuiBox-root')]" #删除告警页面提示信息
rulePage_delete_tip_button_warningYes_posXpath = "//div[contains(@class,'MuiPaper-root MuiPaper-elevation MuiPaper-rounded MuiPaper-elevation24 MuiDialog-paper MuiDialog-paperScrollPaper MuiDialog-paperWidthSm')]//button[@type='danger']" #删除告警页面，Yes确认删除按钮
rulePage_delete_tip_button_warningNo_posXpath = "//div[contains(@class,'MuiPaper-root MuiPaper-elevation MuiPaper-rounded MuiPaper-elevation24 MuiDialog-paper MuiDialog-paperScrollPaper MuiDialog-paperWidthSm')]//button[contains(@class,'MuiButtonBase-root MuiButton-root MuiButton-text MuiButton-textPrimary MuiButton-sizeSmall MuiButton-textSizeSmall MuiButton-colorPrimary')]" ##删除告警页面，No取消删除按钮
policyRulePage_negateSrcIP_posXpath = "//*[@id='policy_not_negate-_PolicySwitch_ElFormItem_SourceItem_SourceModuleSelect_ElFormItem_ElForm_VPanel_VEditPanel_SecurityAdd_Home_App_anonymousComponent']/span[1]"

policyRulePage_addDstIP_posXpath = "//div[@class='MultipleSelect DestinationsModuleSelect']//i[@class='iconfont icon-Create1 cursor']"
policyRulePage_searchDstIP_posXpath = "//div[@class='destinations list-box']//input[contains(@id, 'object_ip_search')]"
policyRulePage_selectDstIP_posXpath = "//div[@class='CommonListDetail list-detail']//span[normalize-space(text())='{replaceValue}']"
policyRulePage_closeDstIP_posXpath = "//div[@class='destinations list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"

policyRulePage_addSrcPort_posXpath = "//div[@zs-label='Source']//p[normalize-space(text())='Port']/ancestor::div[@zs-label='SourceItem']//i[@class='iconfont icon-Create1 cursor']"
policyRulePage_searchSrcPort_posXpath = "//div[@class='SourceList list-box']//input[@id='object_ip_search']"
policyRulePage_selectSrcPort_posXpath = "//div[@class='reference-box el-popover__reference']//span[normalize-space(text())='{replaceValue}']"
policyRulePage_closeSrcPort_posXpath = "//div[@class='SourceList list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"

policyRulePage_addApplication_posXpath = "//label[normalize-space(text())='Application']/following-sibling::div/button"
policyRulePage_searchApplication_posXpath = '//*[@class="px-[12px] py-[4px] flex"]//input'
policyRulePage_selectApplication_posXpath = '//li[@class="MuiListItem-root MuiListItem-colorNeutral MuiListItem-variantPlain css-1linw58"]'
policyRulePage_closeApplication_posXpath = '//*[@class="MuiDrawer-content css-10lcz44"]//button[normalize-space(text())="Cancel"]'
policyRulePage_selectApplicationLabel_posXpath = "//div[@class='el-tabs__nav is-top']//div[normalize-space(text())='Application']"
policyRulePage_selectApplicationGroupLabel_posXpath = "//div[normalize-space(text())='Group']"
policyRulePage_little_button_addApplication_posId = "policy_app_create-_AppSelect_ElFormItem_ElForm_VPanel_VEditPanel_policy_monitor_write_Home_App_anonymousComponent"

policyRulePage_addInternalIP_posXpath = "//div[@zs-label='Internal']//div[@class='MultipleSelect InternalsSelect']//i[@class='iconfont icon-Create1 cursor']"
policyRulePage_searchInternalIP_posXpath = "//div[@class='CommonListDetail list-detail']//input[@id='object_ip_search']"
policyRulePage_selectInternalIP_posXpath = "//div[@class='InternalsList list-box']//span[normalize-space(text())='{replaceValue}']"
policyRulePage_closeInternalIP_posXpath = "//div[@class='InternalsList list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"

policyRulePage_addInternalPort_posXpath = "//label[normalize-space(text())='Internal']/..//label[normalize-space(text())='Port']/following-sibling::div/button"
policyRulePage_searchInternalPort_posXpath = "//input[contains(@class, 'MuiInput-input') and contains(@class, 'css-za5rna')]"
policyRulePage_selectInternalPort_posXpath = "//div[@class='MuiBox-root css-8vsxvh']//span[normalize-space(text())='{replaceValue}']"
policyRulePage_closeInternalPort_posXpath = "(//span[contains(@class, 'MuiTouchRipple-root') and contains(@class, 'css-w0pj6f') and ancestor::*[contains(normalize-space(text()), 'Cancel')]])[1]"

policyRulePage_addDstPort_posXpath = "//label[normalize-space(text())='Destination']/..//label[normalize-space(text())='Port']/following-sibling::div/button"
policyRulePage_searchDstPort_posXpath = policyRulePage_searchInternalPort_posXpath
policyRulePage_selectDstPort_posXpath = policyRulePage_selectInternalPort_posXpath
policyRulePage_closeDstPort_posXpath = policyRulePage_closeInternalPort_posXpath

policyRulePage_addExternalIP_posXpath = "//div[@zs-label='External']//div[@class='MultipleSelect ExternalsSelect']//i[@class='iconfont icon-Create1 cursor']"
policyRulePage_searchExternalIP_posXpath = "//div[@class='ExternalsList list-box']//input[@id='object_ip_search']"
policyRulePage_selectExternalIP_posXpath = "//div[@class='ExternalsList list-box']//span[normalize-space(text())='{replaceValue}']"
policyRulePage_closeExternalIP_posXpath = "//div[@class='ExternalsList list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"

policyRulePage_addExternalPort_posXpath = "//label[normalize-space(text())='External']/..//label[normalize-space(text())='Port']/following-sibling::div/button"
policyRulePage_searchExternalPort_posXpath = policyRulePage_searchInternalPort_posXpath
policyRulePage_selectExternalPort_posXpath = policyRulePage_selectInternalPort_posXpath
policyRulePage_closeExternalPort_posXpath = policyRulePage_closeInternalPort_posXpath

policyRulePage_addUser_posXpath = "//div[@zs-label='Source']//p[normalize-space(text())='User']/ancestor::div[@zs-label='SourceItem']//i[@class='iconfont icon-Create1 cursor']"
policyRulePage_searchUser_posXpath = "//div[@class='SourceList list-box']//input[@id='object_ip_search']"
policyRulePage_selectUser_posXpath = "//div[@class='reference-box el-popover__reference']//span[normalize-space(text())='{replaceValue}']"
policyRulePage_closeUser_posXpath = "//div[@class='SourceList list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"

policyRulePage_addImsi_posXpath = "//div[@zs-label='Source']//p[normalize-space(text())='Device']/ancestor::div[@zs-label='SourceItem']//i[@class='iconfont icon-Create1 cursor']"
policyRulePage_searchImsi_posXpath = "//div[@class='SourceList list-box']//input[@id='object_ip_search']"
policyRulePage_selectImsi_posXpath = "//ul[@class='row-container tableList']//li[1]//div[@class='row-content-cell']"
policyRulePage_closeImsi_posXpath = "//div[@class='SourceList list-box']//button[@class='el-button right-menu-button-close el-button--info el-button--small']"

# phone number
policyRulePage_choosePhoneNumber_posXpath = "//*[@id='tab-phone_number' and contains(concat(' ', @class, ' '), ' el-tabs__item is-top ') and contains(text(), 'Phone Number')]"

# imei
policyRulePage_chooseImei_posXpath = "//*[@id='tab-imei' and contains(concat(' ', @class, ' '), ' el-tabs__item is-top ') and contains(text(), 'IMEI')]"

# apn
policyRulePage_chooseApn_posXpath = "//*[@id='tab-apn' and contains(concat(' ', @class, ' '), ' el-tabs__item is-top ') and contains(text(), 'APN')]"

policyRulePage_addCondition_posXpath = "//button[contains(., 'Add conditions')]//span[contains(@class, 'MuiTouchRipple-root css-w0pj6f')]"
policyRulePage_addConditionImsi_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Device']"
policyRulePage_addCondition_serverFqdn_posXpath = "//ul[@class='MuiList-root MuiList-vertical MuiList-variantPlain MuiList-colorNeutral MuiList-sizeMd css-1xyc0ec']//div[text()='Server FQDN']"
policyRulePage_addCondition_dstPort_posXpath = "(//div[contains(@class, 'MuiListSubheader-root') and contains(@class, 'css-1tpnloi')])[2]/following-sibling::div//div[contains(text(), 'Port')]"
policyRulePage_addCondition_url_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='URL']"
policyRulePage_addCondition_uri_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Protocol Field']/parent::*//div[normalize-space(text())='URI']"
policyRulePage_addCondition_requestHeader_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Request Header']"
policyRulePage_addCondition_responseHeader_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Response Header']"
policyRulePage_addCondition_requestBody_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Request Body']"
policyRulePage_addCondition_responseBody_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Response Body']"
policyRulePage_addCondition_close_posXpath = '//*[@class="MuiDrawer-content css-10lcz44"]//button[normalize-space(text())="Cancel"]'
policyRulePage_addCondition_srcPort_posXpath = "//div[@class='SourceList list-box']//li[3]//div[normalize-space(text())='Port']"
policyRulePage_addCondition_internalIP_posXpath = "//div[@class='MuiDrawer-content css-10lcz44']//li[3]//div[normalize-space(text())='IP Address']"
policyRulePage_addCondition_externalIP_posXpath = "//div[@class='MuiDrawer-content css-10lcz44']//li[4]//div[normalize-space(text())='IP Address']"
policyRulePage_addCondition_internalPort_posXpath = "//div[@class='MuiDrawer-content css-10lcz44']//li[4]//div[normalize-space(text())='Port']"
policyRulePage_addCondition_externalPort_posXpath = "//div[@class='MuiDrawer-content css-10lcz44']//li[4]//div[normalize-space(text())='Port']"
policyRulePage_addCondition_IpProtocol_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='IP Protocol']"
policyRulePage_addCondition_Boolean_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='{replaceValue}']"
#policyRulePage_addCondition_requestHeader_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Request Header']"
policyRulePage_addCondition_ftpAccount_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Account']"
policyRulePage_addCondition_ftpContent_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Content']"
policyRulePage_addCondition_cn_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='CN']"
policyRulePage_addCondition_san_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='SAN']"
policyRulePage_addCondition_qname_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='QNAME']"
policyRulePage_addCondition_mailSubject_posXpath = "//div[@class='css-dob60y']//div[normalize-space(text())='Subject']"
policyRulePage_addCondition_mailContent_posXpath = "//div[@class='css-dob60y']//div[normalize-space(text())='Content']"
policyRulePage_addCondition_mailFrom_posXpath = "//div[@class='css-dob60y']//div[normalize-space(text())='From']"
policyRulePage_addCondition_mailTo_posXpath = "//div[@class='css-dob60y']//div[normalize-space(text())='To']"
policyRulePage_addCondition_mailAccount_posXpath = "//div[@class='css-dob60y']//div[normalize-space(text())='Account']"
policyRulePage_addCondition_mailAttachmentName_posXpath = "//div[@class='css-dob60y']//div[normalize-space(text())='Attachment Name']"
policyRulePage_addCondition_mailAttachmentContent_posXpath = "//div[@class='css-dob60y']//div[normalize-space(text())='Attachment Content']"

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

policyRulePage_addServerFqdn_posXpath = "//label[text()='Server FQDN']/parent::div[@class='flex flex-row group']//i[@class='iconfont icon-Create1 font-[700]']"
policyRulePage_searchServerFqdn_posXpath = "//div[@class='px-[12px] py-[4px] flex']//input"
policyRulePage_selectServerFqdn_posXpath = "//ul[@class='MuiList-root MuiList-vertical MuiList-variantPlain MuiList-colorNeutral MuiList-sizeMd css-1cklc3']//li[1]//div[@class='MuiBox-root css-8vsxvh']"
policyRulePage_closeServerFqdn_posXpath = "//div[@class='absolute bottom-0 h-[40px] w-[100%] overflow-hidden text-[16px] truncate bg-[--color-background-secondary] flex  justify-center items-center pl-[12px] pr-[38px]']//button[text()='Cancel']"
policyRulePage_negateServerFqdn_posXpath = "//div[@class='MultipleSelect DestinationsModuleSelect']//li[{replaceValue}]//label[@id='policy_not_negate-_PolicySwitch_ElFormItem_DestinationsItem_DestinationsModuleSelect_ElFormItem_ElForm_VPanel_VEditPanel_SecurityAdd_Home_App_anonymousComponent']//span[@class='el-checkbox__input']"

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
policyRulePage_addMailFrom_posXpath = '//div[@class="MuiFormControl-root MuiFormControl-vertical MuiFormControl-sizeMd css-t5weby"][3]//i[@class="iconfont icon-Create1 font-[700]"]'
policyRulePage_searchMailFrom_posXpath = '//*[@class="px-[12px] py-[4px] flex"]//input'
policyRulePage_selectMailFrom_posXpath = '//li[@class="MuiListItem-root MuiListItem-colorNeutral MuiListItem-variantPlain css-1linw58"]'
policyRulePage_closeMailFrom_posXpath = '//*[@class="MuiDrawer-content css-10lcz44"]//button[normalize-space(text())="Cancel"]'
#mail to
policyRulePage_addMailTo_posXpath = '//div[@class="MuiFormControl-root MuiFormControl-vertical MuiFormControl-sizeMd css-t5weby"][3]//i[@class="iconfont icon-Create1 font-[700]"]'
policyRulePage_searchMailTo_posXpath = '//*[@class="px-[12px] py-[4px] flex"]//input'
policyRulePage_selectMailTo_posXpath = '//li[@class="MuiListItem-root MuiListItem-colorNeutral MuiListItem-variantPlain css-1linw58"]'
policyRulePage_closeMailTo_posXpath = '//*[@class="MuiDrawer-content css-10lcz44"]//button[normalize-space(text())="Cancel"]'
#mail account
policyRulePage_addMailAccount_posXpath = '//div[@class="MuiFormControl-root MuiFormControl-vertical MuiFormControl-sizeMd css-t5weby"][3]//i[@class="iconfont icon-Create1 font-[700]"]'
policyRulePage_searchMailAccount_posXpath = '//*[@class="px-[12px] py-[4px] flex"]//input'
policyRulePage_selectMailAccount_posXpath = '//li[@class="MuiListItem-root MuiListItem-colorNeutral MuiListItem-variantPlain css-1linw58"]'
policyRulePage_closeMailAccount_posXpath = '//*[@class="MuiDrawer-content css-10lcz44"]//button[normalize-space(text())="Cancel"]'
#mail subject
policyRulePage_addMailSubject_posXpath = '//div[@class="MuiFormControl-root MuiFormControl-vertical MuiFormControl-sizeMd css-t5weby"][3]//i[@class="iconfont icon-Create1 font-[700]"]'
policyRulePage_searchMailSubject_posXpath = '//*[@class="px-[12px] py-[4px] flex"]//input'
policyRulePage_selectMailSubject_posXpath = '//li[@class="MuiListItem-root MuiListItem-colorNeutral MuiListItem-variantPlain css-1linw58"]'
policyRulePage_closeMailSubject_posXpath = '//*[@class="MuiDrawer-content css-10lcz44"]//button[normalize-space(text())="Cancel"]'
#mail attachment name
policyRulePage_addMailAttachmentName_posXpath = '//div[@class="MuiFormControl-root MuiFormControl-vertical MuiFormControl-sizeMd css-t5weby"][3]//i[@class="iconfont icon-Create1 font-[700]"]'
policyRulePage_searchMailAttachmentName_posXpath = '//*[@class="px-[12px] py-[4px] flex"]//input'
policyRulePage_selectMailAttachmentName_posXpath = '//li[@class="MuiListItem-root MuiListItem-colorNeutral MuiListItem-variantPlain css-1linw58"]'
policyRulePage_closeMailAttachmentName_posXpath = '//*[@class="MuiDrawer-content css-10lcz44"]//button[normalize-space(text())="Cancel"]'
#mail attachment content
policyRulePage_addMailAttachmentContent_posXpath = '//div[@class="MuiFormControl-root MuiFormControl-vertical MuiFormControl-sizeMd css-t5weby"][3]//i[@class="iconfont icon-Create1 font-[700]"]'
policyRulePage_searchMailAttachmentContent_posXpath = '//*[@class="px-[12px] py-[4px] flex"]//input'
policyRulePage_selectMailAttachmentContent_posXpath = '//li[@class="MuiListItem-root MuiListItem-colorNeutral MuiListItem-variantPlain css-1linw58"]'
policyRulePage_closeMailAttachmentContent_posXpath = '//*[@class="MuiDrawer-content css-10lcz44"]//button[normalize-space(text())="Cancel"]'
#add mail content
policyRulePage_addMailContent_posXpath = '//div[@class="MuiFormControl-root MuiFormControl-vertical MuiFormControl-sizeMd css-t5weby"][3]//i[@class="iconfont icon-Create1 font-[700]"]'
policyRulePage_searchMailContent_posXpath = '//*[@class="px-[12px] py-[4px] flex"]//input'
policyRulePage_selectMailContent_posXpath = '//li[@class="MuiListItem-root MuiListItem-colorNeutral MuiListItem-variantPlain css-1linw58"]'
policyRulePage_closeMailContent_posXpath = '//*[@class="MuiDrawer-content css-10lcz44"]//button[normalize-space(text())="Cancel"]'
# security
securityRuleListPage_createButton_posXpath = "//*[contains(@class, 'action-create') and contains(@class, 'inline-flex') and contains(@class, 'mr-[8px]')]"
securityRuleListPage_deleteButton_posId ="appDel-_OperateBtns_ElRow_Objects_ProxyInterception_Home_App_anonymousComponent"
securityRuleListpage_okButton_warningYes_posXpath = "//button[@class='el-button delComponents-ok role-disconnect-btn el-button--default el-button--small']"
securityRuleListpage_okButton_warningNo_posXpath = "//button[@class='el-button delComponents-close el-button--info el-button--small']"
securityRuleListPage_searchLable_posId = "select-label"
securityRuleListPage_searchLable_dropDown_item_posXpath = "//div[contains(@class,'el-scrollbar')]//span[normalize-space(text())='{replaceValue}']"   #下拉菜单定位
securityRuleListPage_searchLable_input_itemContent_posXpath = "//div[contains(@class,'ListItem')]//span[normalize-space(text())='{replaceValue}']/ancestor::div[contains(@class,'ListItem')]//input"   #输入item的值，replaceValue替换实际查询值
securityRuleListPage_searchLable_searchButton_posId = "searchQuery"
securityRuleListPage_tableTbody_posXpath = "//div[contains(@class,'ly-table1')]//tbody" 
securityRulelistPage_allSelect_posXpath = "//div[@class='flex flex-row flex-wrap justify-start items-center pl-[18px] mt-[20px]']//span[@class='MuiCheckbox-checkbox css-n110n']"

securityRulePage_inputName_posXpath = "//*[contains(@class, 'MuiInput-input') and contains(@class, 'css-fqt4w4')]"
securityRulePage_selectShunt_posXpath = "//*[contains(@class, 'iconfont') and contains(@class, 'text-[18px]') and contains(@class, 'text-[--color-primary]') and contains(@class, 'icon-Shunt')]"
securityRulePage_selectAllow_posXpath = "//*[contains(@class, 'iconfont') and contains(@class, 'text-[18px]') and contains(@class, 'text-[--color-primary]') and contains(@class, 'icon-Allow')]"
securityRulePage_selectDeny_posXpath = "//*[contains(@class, 'iconfont') and contains(@class, 'text-[18px]') and contains(@class, 'text-[--color-primary]') and contains(@class, 'icon-Deny')]"

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
# redirect- dns
securityRulePage_subAction_redirect_answer0ValueType_posId = "blockselect00"
securityRulePage_subAction_redirect_qtypeAAAA_posXpath = "//span[contains(@class, 'el-radio-button__inner') and normalize-space(text())='AAAA']"
securityRulePage_subAction_redirect_answer0ValueTypeChoose_posXpath="//div[@class='el-select-dropdown el-popper']//ul[@class='el-scrollbar__view el-select-dropdown__list']/li/span[normalize-space(text())='{replaceValue}']"
securityRulePage_subAction_redirect_dnsAnswerValueSelectPlaceholder_posId = "html_profile"
securityRulePage_subAction_redirect_dnsAnswerType0choose_posId = "atype_select00"
securityRulePage_subAction_redirect_dnsAnswerType0chooseValue_posXpath = "//li[@id='dns_atype_select00' and normalize-space() = '{replaceValue}']"
securityRulePage_subAction_redirect_dnsAnswerValueNameSearch_posId = "filedata_profileName"
securityRulePage_subAction_redirect_dnsAnswerValueNameSelect_posId = "filelist_select0"
securityRulePage_subAction_redirect_dnsAnswerValueTTL0_posId = "ttl00"
securityRulePage_subAction_redirect_dnsAnswer0ATextPlaceholder_posId = "A001"
securityRulePage_subAction_redirect_dnsAnswer0AAAATextPlaceholder_posId = "AAAA001"
securityRulePage_subAction_redirect_dnsAnswer0CnameTextPlaceholder_posId = "Cname001"
#alert
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
# rule 页面中Add Condition按钮定位
interceptRulePage_addCondition_posXpath = "//*[@id='policy_condition-_ConditionModuleSelect_ElFormItem_ElForm_VPanel_VEditPanel_policy_Intercept_edit_Home_App_anonymousComponent']"
interceptRulePage_addCondition_close_posXpath = "//div[@class='ToggleDraw']/div[last()]//button[@class='el-button right-menu-button-close el-button--info el-button--small']"
# rule 中添加condition侧滑中选择行定位
interceptRulePage_addCondition_srcIP_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Source']/parent::*//div[normalize-space(text())='IP Address']"
interceptRulePage_addCondition_serverFqdn_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Destination']/parent::*//div[normalize-space(text())='Server FQDN']"
# source ip
interceptRulePage_negateSrcIP_posXpath = "//*[@id='policy_not_negate-_PolicySwitch_ElFormItem_SourceItem_SourceModuleSelect_ElFormItem_ElForm_VPanel_VEditPanel_policy_Intercept_edit_Home_App_anonymousComponent']/span[1]"
# Server FQDN的添加、查询、选中、关闭操作
interceptRulePage_addServerFqdn_posXpath = policyRulePage_addServerFqdn_posXpath
interceptRulePage_searchServerFqdn_posXpath = "//div[@class='rm-content']//input[@id='object_ip_search']"
interceptRulePage_selectServerFqdn_posXpath = policyRulePage_selectServerFqdn_posXpath
interceptRulePage_closeServerFqdn_posXpath = policyRulePage_closeServerFqdn_posXpath
# action parameter trusted
interceptRulePage_intercept_addTrustedSelectBox_posXpath = "//div[@zs-label='keyring_for_trusted']//span[@class='el-input__suffix']//i"   # trusted  选择框  定位
interceptRulePage_intercept_searchTrustedInput_posXpath = "//body/div[last()]/div[@class='el-scrollbar']//input[@placeholder='Search for']"   # trusted profile 对话框查询输入框
interceptRulePage_intercept_searchTrustedDorpItem_posXpath = "//body/div[last()]/div[@class='el-scrollbar']//div[contains(@class, 'select-search-option')]/li[2]"   # trusted profile 对话框查询下拉列表第一个元素
# action parameter untrusted
interceptRulePage_intercept_addUntrustedSelectBox_posXpath = "//div[@zs-label='keyring_for_untrusted']//span[@class='el-input__suffix']//i"   # untrusted  选择框  定位
interceptRulePage_intercept_searchUntrustedInput_posXpath = "//body/div[last()]/div[@class='el-scrollbar']//input[@placeholder='Search for']"   # untrusted profile 对话框查询输入框
interceptRulePage_intercept_searchUntrustedDorpItem_posXpath = "//body/div[last()]/div[@class='el-scrollbar']//div[contains(@class, 'select-search-option')]/li[2]"   # untrusted profile 对话框查询下拉列表第一个元素
# action parameter mirror decrypted traffic
interceptRulePage_intercept_addTrafficMirrorProfileButton_posXpath = "//div[@zs-label='Mirror Decrypted Traffic']//div[@role='switch']"   # traffic decrypted traffic 打开按钮  定位
interceptRulePage_intercept_addVlanIDButton_posXpath = "//div[@zs-label='Add VLAN ID']//div[@role='switch']"   # add vlan id  打开按钮  定位
interceptRulePage_intercept_addTrafficMirrorProfileSelectBox_posXpath = "//div[@zs-label='Traffic Mirror Profile']//span[@class='el-input__suffix']//i"   # traffic decrypted traffic 选择框  定位
interceptRulePage_intercept_searcTrafficMirrorProfileInput_posXpath = "//body/div[last()]/div[@class='el-scrollbar']//input[@placeholder='Search for']"   # traffic decrypted traffic profile 对话框查询输入框
interceptRulePage_intercept_searchTrafficMirrorProfileDorpItem_posXpath = "//body/div[last()]/div[@class='el-scrollbar']//div[contains(@class, 'select-search-option')]/li[2]"   # traffic decrypted traffic profile 对话框查询下拉列表第一个元素
# action parameter decryption profile
interceptRulePage_intercept_addDecryptionProfileSelectBox_posXpath = "//div[@zs-label='Decryption profile']//span[@class='el-input__suffix']//i"   # decryption profile  选择框  定位
interceptRulePage_intercept_searchDecryptionProfileInput_posXpath = "//body/div[last()]/div[@class='el-scrollbar']//input[@placeholder='Search for']"   # decryption profile 对话框查询输入框
interceptRulePage_intercept_searchDecryptionProfileDorpItem_posXpath = "//body/div[last()]/div[@class='el-scrollbar']//div[contains(@class, 'select-search-option')]/li[2]"   # decryption profile 对话框查询下拉列表第一个元素
# action parameter tcp proxy profile
interceptRulePage_intercept_addTcpProfileSelectBox_posXpath = "//div[@zs-label='TCP Proxy Profile']//span[@class='el-input__suffix']//i"   # tcp proxy profile  选择框  定位
interceptRulePage_intercept_searchTcpProfileInput_posXpath = "//body/div[last()]/div[@class='el-scrollbar']//input[@placeholder='Search for']"   # tcp proxy profile 对话框查询输入框
interceptRulePage_intercept_searchTcpProfileDorpItem_posXpath = "//body/div[last()]/div[@class='el-scrollbar']//div[contains(@class, 'select-search-option')]/li[2]"   # tcp proxy profile 对话框查询下拉列表第一个元素
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
manipulationRulePage_addCondition_qname_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Protocol Field']/parent::*//div[normalize-space(text())='QNAME']"
manipulationRulePage_addCondition_serverPort_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Destination']/parent::*//div[normalize-space(text())='Port']"
manipulationRulePage_addCondition_internalIP_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Internal']/parent::*//div[normalize-space(text())='IP Address']"
manipulationRulePage_addCondition_srcPort_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Source']/parent::*//div[normalize-space(text())='Port']"
manipulationRulePage_addCondition_internalPort_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Internal']/parent::*//div[normalize-space(text())='Port']"
manipulationRulePage_addCondition_destinationPort_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='Destination']/parent::*//div[normalize-space(text())='Port']"
manipulationRulePage_addCondition_externalPort_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='External']/parent::*//div[normalize-space(text())='Port']"
manipulationRulePage_addCondition_externalIP_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='External']/parent::*//div[normalize-space(text())='IP Address']"
manipulationRulePage_addCondition_user_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='User']/parent::*//div[normalize-space(text())='User']"
manipulationRulePage_addCondition_imsi_posXpath = "//div[@class='SourceList list-box']/parent::*//div[normalize-space(text())='Device']"
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
# subid user的添加、查询、选中、关闭操作
manipulationRulePage_addUser_posXpath = policyRulePage_addUser_posXpath
manipulationRulePage_searchUser_posXpath = policyRulePage_searchUser_posXpath
manipulationRulePage_selectUser_posXpath = policyRulePage_selectUser_posXpath
manipulationRulePage_closeUser_posXpath = policyRulePage_closeUser_posXpath
# Device imsi 的添加、查询、选中、关闭操作
manipulationRulePage_addImsi_posXpath = policyRulePage_addImsi_posXpath
manipulationRulePage_searchImsi_posXpath = policyRulePage_searchImsi_posXpath
manipulationRulePage_selectImsi_posXpath = policyRulePage_selectImsi_posXpath
manipulationRulePage_closeImsi_posXpath = policyRulePage_closeImsi_posXpath
# Application的添加、查询、选中、关闭操作
manipulationRulePage_addApplication_posXpath = "//div[@class='MultipleSelect AppSelect flex']//span//div[@class='row-content-cell']"
manipulationRulePage_searchDoHApplication_posXpath = "//div[@class='right-menu-content']//span[text()='DoH']"
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
# QNAME的添加、查询、选中、关闭操作
manipulationRulePage_addServerQname_posXpath = policyRulePage_addQname_posXpath
manipulationRulePage_searchQname_posXpath = "//div[@class='rm-content']//input[@id='object_ip_search']"
manipulationRulePage_selectQname_posXpath = policyRulePage_selectQname_posXpath
manipulationRulePage_closeServerQname_posXpath = policyRulePage_closeQname_posXpath
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
manipulationRulePage_redirectDoH_qtypeRadio_posXpath = "//label[text()='Setting Details']/parent::*/div//form/div[1]//input[@value='{replace_qtype}']/parent::*"
manipulationRulePage_redirectDoH_atypeSelectBox_posXpath = "//label[text()='Setting Details']/parent::*/div//form/div[{replace_index}]//i[contains(@class, 'el-select__caret')]"    # repalace_index 多个时索引
manipulationRulePage_redirectDoH_atypeSelectDropItem_posXpath = "//body/div[contains(@class, 'el-select-dropdown')]//span[text()='{replace_atype}']"
manipulationRulePage_redirectDoH_valueInput_posXpath = "//label[text()='Setting Details']/parent::*/div//form/div[{replace_index}]//div[@zs-label='value']//input"
manipulationRulePage_redirectDoH_ttlInput_posXpath = "//label[text()='Setting Details']/parent::*/div//form/div[{replace_index}]//div[@zs-label='TTL']//input"
manipulationRulePage_redirectDoH_add_posXpath = "//label[text()='Setting Details']/parent::*/div//form//i[contains(@class, 'icon-Create1')]"
# action parameter replace
manipulationRulePage_replace_addRegex_posXpath = "//ul[@class='replacelist']//li[{replace_sort}]//div[@zs-label='regexEnable']//div[contains(@class, 'el-switch')]"   # regex 开关定位， replace_sort替换为实际的个数
manipulationRulePage_replace_addSearchInSelectBox_posXpath = "//ul[@class='replacelist']//li[{replace_sort}]//div[@zs-label='搜索区域']//i"   # search in 选择框 定位, replace_sort替换为实际的个数
manipulationRulePage_replace_addSearchInSelectDropItem_posXpath = "//body/div[contains(@class, 'el-select-dropdown')]//li[normalize-space(text())='{replace_type}']"   # search in 下拉框item 定位
manipulationRulePage_replace_addFindInput_posXpath = "//ul[@class='replacelist']//li[{replace_sort}]//div[@zs-label='Fined']//input"   # find 输入框 定位， replace_sort替换为实际的个数
manipulationRulePage_replace_addReplaceWithInput_posXpath = "//ul[@class='replacelist']//li[{replace_sort}]//div[@zs-label='Replace']//input"   # replace with 输入框 定位， replace_sort替换为实际的个数
manipulationRulePage_replace_add_posXpath = "//*[@id='replaceadd_btn']//i"   # replace add 加号添加 定位
# action parameter hijack
manipulationRulePage_hijack_addHijackProfileSelectBox_posXpath = "//div[@zs-label='劫持文件']//i"   # hijack profile  选择框  定位
manipulationRulePage_hijack_searchHijackProfile_posXpath = "//body/div/div[@class='el-scrollbar']//input[@placeholder='Search for']"   # hijack search profile 对话框查询输入框
manipulationRulePage_hijack_searchHijackProfileDorpItem_posXpath = "//body/div/div[@class='el-scrollbar']//div[contains(@class, 'select-search-option')]/li[1]"   # hijack search profile 对话框查询下拉列表第一个元素
# action parameter insert
manipulationRulePage_insert_addInsertProfileSelectBox_posXpath = "//div[@zs-label='劫持文件']//span[@class='el-input__suffix-inner']//i"   # insert script  选择框  定位
manipulationRulePage_insert_searchInsertProfile_posXpath = manipulationRulePage_hijack_searchHijackProfile_posXpath   # insert script search profile 对话框查询输入框
manipulationRulePage_insert_searchInsertProfileDorpItem_posXpath = manipulationRulePage_hijack_searchHijackProfileDorpItem_posXpath   # insert script search profile 对话框查询下拉列表第一个元素
# action parameter edit element
manipulationRulePage_editElement_addSearchScopeWholeFileRadio_posXpath = "//div[@class='man-add-action']//li[{replace_sort}]//span[normalize-space(text())='whole file']"   # replace_sort替换为实际的个数
manipulationRulePage_editElement_addSearchScopeInsideElementRadio_posXpath = "//div[@class='man-add-action']//li[{replace_sort}]//span[normalize-space(text())='inside element']"
manipulationRulePage_editElement_addStartIndicatorInput_posXpath = "//div[@class='man-add-action']//li[{replace_sort}]//label[normalize-space(text())='Start Indicator']/parent::*//input[@id='undefined1']"
manipulationRulePage_editElement_addContainedKeywordInput_posXpath = "//div[@class='man-add-action']//li[{replace_sort}]//label[normalize-space(text())='Contained Keyword']/parent::*//input[@id='undefined1']"
manipulationRulePage_editElement_addSDistanceFromAnchorInput_posXpath = "//div[@class='man-add-action']//li[{replace_sort}]//label[normalize-space(text())='Distance from Anchor']/parent::*//input[@class='el-input__inner']"
manipulationRulePage_editElement_addMarkRadio_posXpath = "//div[@class='man-add-action']//li[{replace_sort}]//label[normalize-space(text())='Treatment']/parent::*//span[normalize-space(text())='Mark']"
manipulationRulePage_editElement_addRemoveRadio_posXpath = "//div[@class='man-add-action']//li[{replace_sort}]//label[normalize-space(text())='Treatment']/parent::*//span[normalize-space(text())='Remove']"
manipulationRulePage_editElement_add_posXpath = "//div[@class='man-add-action']//li[contains(@class, 'replaceadd')]//i"
# action parameter run script profile
manipulationRulePage_insert_addrunScriptProfileSelectBox_posXpath = manipulationRulePage_insert_addInsertProfileSelectBox_posXpath   # run script  选择框  定位
manipulationRulePage_insert_searchrunScriptProfile_posXpath = manipulationRulePage_hijack_searchHijackProfile_posXpath   # insert script search profile 对话框查询输入框
manipulationRulePage_insert_searchrunScriptProfileDorpItem_posXpath = manipulationRulePage_hijack_searchHijackProfileDorpItem_posXpath   # insert script search profile 对话框查询下拉列表第一个元素
# other options
manipulationRulePage_logOptions_all_posXpath = '//*[@id="manipulation_logOption-_Edit_Home_App_anonymousComponent"]//span[normalize-space(text())="All"]'
# effective devices
manipulationRulePage_addEffectiveDevices_posXpath = "//*[@id='manipulation_deviceadd-_DevicesSelect_ElFormItem_ElForm_VPanel_VEditPanel_Edit_Home_App_anonymousComponent']"
manipulationRulePage_selectEffectiveDevices_posXpath = "//div[@class='rm-top']//span[normalize-space(text())='Effective Devices']/ancestor::div[@class='right-menu-content']//ul[@class='device-row-box']//div[normalize-space(text())='{replace_device}']"
manipulationRulePage_closeEffectiveDevices_posXpath = "//div[@class='rm-top']//span[normalize-space(text())='Effective Devices']/ancestor::div[@class='right-menu-content']//div[@class='rigth-menu-button-info']/button/span"

# 保存策略时，ok cancel warnging定位
manipulationRulePage_enable_posXpath = securityRulePage_enable_posXpath
manipulationRulePage_okButton_yes_posId = "OK-_Edit_Home_App_anonymousComponent"
manipulationRulePage_okButton_warningYes_posXpath = "//div[@class='el-message-box__btns']//button[contains(@class, 'el-button--primary')]"

#service chaining
mainPage_policySecondLevelMenu_servicechaining_posXpath = "//span[normalize-space(text()) = 'Service Chaining']"

serviceChainingRuleListPage_createButton_posXpath = "//span[@class='action-create inline-flex mr-[8px] ']"
serviceChainingRuleListPage_deleteButton_posXpath = "//div[@class='flex justify-start items-center mr-[20px]']//span[text()='Delete']"
serviceChainingRuleListPage_searchLable_posXpath = "//div[@class='MuiAutocomplete-wrapper MuiAutocomplete-multiple css-1h1ala5']//input[@placeholder='Please enter search content']"
serviceChainingRuleListPage_searchLable_dropDown_item_posXpath = "//span[normalize-space(text())='{replaceValue}']/../.."   #下拉菜单定位
serviceChainingRuleListPage_searchLable_input_itemContent_posXpath = "//div[contains(@class,'flex-1 overflow-hidden')]//span[normalize-space(text())='{replaceValue}']/ancestor::div[contains(@class,'flex-1 overflow-hidden')]//input"   #输入item的值，replaceValue替换实际查询值
serviceChainingRuleListPage_searchLable_searchButton_posXpath = "//div[@class='flex-1 overflow-hidden']//i[@class='iconfont icon-sousuo text-[19px]']"
serviceChainingRuleListPage_tableTbody_posXpath = "//div[@class='MuiDataGrid-virtualScrollerRenderZone css-1inm7gi']"

serviceChainingRulePage_inputName_posXpath = "//*[@class='service-chaining-policy-name']//input" 
serviceChainingRulePage_rawTrafficButton_posXpath = "//div[@class='service-chaining-policy-targeted_traffic']//button[1]" 
serviceChainingRulePage_decryptedTrafficButton_posXpath = "//div[@class='service-chaining-policy-targeted_traffic']//button[2]" 
serviceChainingRulePage_negateSrcIP_posXpath = "//div[@zs-label='Source']//p[normalize-space(text())='IP Address']/ancestor::div[@zs-label='SourceItem']//span[@class='el-checkbox__inner']"
serviceChainingRulePage_negateDstIP_posXpath = "//div[@zs-label='Destination']//p[normalize-space(text())='IP Address']/ancestor::div[@zs-label='SourceItem']//span[@class='el-checkbox__inner']"
serviceChainingRulePage_negateUser_posXpath = "//div[@zs-label='Source']//p[normalize-space(text())='User']/ancestor::div[@zs-label='SourceItem']//span[@class='el-checkbox__inner']"
serviceChainingRulePage_negateImsi_posXpath = "//div[@zs-label='Source']//p[normalize-space(text())='Device']/ancestor::div[@zs-label='SourceItem']//span[@class='el-checkbox__inner']"
serviceChainingRulePage_negateSrcPort_posXpath = "//div[@zs-label='Source']//p[normalize-space(text())='Port']/ancestor::div[@zs-label='SourceItem']//span[@class='el-checkbox__inner']"
serviceChainingRulePage_negateDstPort_posXpath = "//div[@zs-label='Destination']//p[normalize-space(text())='Port']/ancestor::div[@zs-label='SourceItem']//span[@class='el-checkbox__inner']"
serviceChainingRulePage_negateServerFqdn_posXpath = "//div[@zs-label='Destination']//p[normalize-space(text())='Server FQDN']/ancestor::div[@zs-label='SourceItem']//span[@class='el-checkbox__inner']"
serviceChainingRulePage_negateInternalPort_posXpath = "//div[@zs-label='Internal']//p[normalize-space(text())='Port']/ancestor::div[@zs-label='SourceItem']//span[@class='el-checkbox__inner']"
serviceChainingRulePage_negateExternalPort_posXpath = "//div[@zs-label='External']//p[normalize-space(text())='Port']/ancestor::div[@zs-label='SourceItem']//span[@class='el-checkbox__inner']"
serviceChainingRulePage_addSrcIP_posXpath = policyRulePage_addSrcIP_posXpath
serviceChainingRulePage_searchSrcIP_posXpath = policyRulePage_searchSrcIP_posXpath
serviceChainingRulePage_selectSrcIP_posXpath = policyRulePage_selectSrcIP_posXpath
serviceChainingRulePage_closeSrcIP_posXpath = policyRulePage_closeSrcIP_posXpath

serviceChainingRulePage_addCondition_user_posXpath = "//div[normalize-space(text())='User']"
serviceChainingRulePage_addUser_posXpath = policyRulePage_addUser_posXpath
serviceChainingRulePage_searchUser_posXpath = policyRulePage_searchUser_posXpath
serviceChainingRulePage_selectUser_posXpath = policyRulePage_selectUser_posXpath
serviceChainingRulePage_closeUser_posXpath = policyRulePage_closeUser_posXpath

serviceChainingRulePage_addCondition_imsi_posXpath = "div[normalize-space(text())='Device']"

serviceChainingRulePage_addDstIP_posXpath = "//label[normalize-space()='Destination']/ancestor::div[@class='MuiFormControl-root MuiFormControl-vertical MuiFormControl-sizeMd css-t5weby']//i[@class='iconfont icon-Create1 font-[700]']"
serviceChainingRulePage_searchDstIP_posXpath =  policyRulePage_searchSrcIP_posXpath
serviceChainingRulePage_selectDstIP_posXpath = policyRulePage_selectSrcIP_posXpath
serviceChainingRulePage_closeDstIP_posXpath = "//div[@class='absolute bottom-0 h-[40px] w-[100%] overflow-hidden text-[16px] truncate bg-[--color-background-secondary] flex  justify-center items-center pl-[12px] pr-[38px]']//button"

serviceChainingRulePage_addApplication_posXpath = "//div[@class='service-chaining-policy-application']//i[@class='iconfont icon-Create1 font-[700]']"
serviceChainingRulePage_searchApplication_posXpath = policyRulePage_searchApplication_posXpath
serviceChainingRulePage_selectApplication_posXpath = rulePage_object_list_select_name_posXpath #policyRulePage_selectApplication_posXpath
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

serviceChainingRulePage_addSFFProfile_posXpath = "//label[normalize-space(text())='SFF Profile']/ancestor::div[@class='MuiFormControl-root MuiFormControl-horizontal MuiFormControl-sizeMd css-90yvhw']//i[@class='iconfont icon-Create1 font-[700]']"
serviceChainingRulePage_searchSFFProfile_posXpath = "//div[@class='px-[12px] py-[4px] flex']//input"
serviceChainingRulePage_selectSFFProfile_posXpath = "//div[@class='pt-[2px] overflow-hidden flex-1']//div[text()='{replaceValue}']"
serviceChainingRulePage_closeSFFProfile_posXpath = serviceChainingRulePage_closeDstIP_posXpath
serviceChainingRulePage_enable_posXpath = "//div[@class='service-chaining-policy-is_enabled']//span[@class='MuiSwitch-root MuiSwitch-sizeMedium css-wj9ris']"
serviceChainingRulePage_okButton_posXpach = "//div[@class='form-action bg-[--color-background] flex justify-center py-[12px] absolute bottom-0 w-full']//button[1]"
serviceChainingRulePage_warningYes_posXpath = "//button[@class='el-button el-button--default el-button--small el-button--primary operation-confirm']"
serviceChainingRuleListPage_warningYes_posXpath = "//div[@class='MuiDialogActions-root flex !justify-center items-center MuiDialogActions-spacing css-vplbg4']//button[text()='Yes']"
serviceChainingRulePage_addConditionQname_posXpath = "//div[normalize-space(text())='QNAME']"

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
mainPage_policySecondLevelMenu_monitor_posXpath = "//span[normalize-space(text())='Monitor']"
monitorRuleListPage_createButton_posXpath = '//i[@class="iconfont icon-Create"]'
monitorRuleListPage_deleteButton_posXpath = '//i[@class="iconfont icon-Delete"]'
monitorRuleListPage_searchLable_posXpath = '//input[@class="MuiAutocomplete-input css-qdyksh"]'
monitorRuleListPage_searchLable_dropDown_item_posXpath = "//div[@class='dune-search-option-content']//span[contains(text(),'{replaceValue}')]/ancestor::div[1]"   #下拉菜单定位
monitorRuleListPage_searchLable_input_itemContent_posXpath = '//*[@class="MuiInput-input css-1u0jcuo"]'   #输入item的值，replaceValue替换实际查询值
monitorRuleListPage_searchLable_searchButton_posXpath = '//div[@class="flex"]/button'
monitorRuleListPage_tableTbody_posXpath = '//div[@class="MuiDataGrid-virtualScrollerRenderZone css-1inm7gi"]'
monitorRulelistPage_allSelect_posXpath = '//div[@class="flex flex-row flex-wrap justify-start items-center pl-[18px] mt-[20px]"]//input[@class="MuiCheckbox-input css-1jj0cvj"]'
monitorRuleListpage_okButton_warningYes_posXpath= '//div[@class="MuiDialogActions-root flex !justify-center items-center MuiDialogActions-spacing css-vplbg4"]/button[1]'
monitorRuleListpage_okButton_warningNo_posXpath= '//div[@class="MuiDialogActions-root flex !justify-center items-center MuiDialogActions-spacing css-vplbg4"]/button[2]'
#monitor新建页/编辑页面按钮
monitorRulePage_inputName_posXpath = '//div[@class="monitor-policy-name"]//input'
monitorRulePage_mirrorTrafficButton_posXpath ='//*[text()="Mirror Traffic"]/ancestor::div[@class="MuiFormControl-root MuiFormControl-horizontal MuiFormControl-sizeMd css-90yvhw"]//*[@class="MuiSwitch-root MuiSwitch-sizeMedium css-wj9ris"]'
monitorRulePage_packetCaptureButton_posXpath = '//*[text()="Packet Capture"]/ancestor::div[@class="MuiFormControl-root MuiFormControl-horizontal MuiFormControl-sizeMd css-90yvhw"]//*[@class="MuiSwitch-root MuiSwitch-sizeMedium css-wj9ris"]'
monitorRulePage_addSrcIP_posXpath = policyRulePage_addSrcIP_posXpath
monitorRulePage_searchSrcIP_posXpath = policyRulePage_searchSrcIP_posXpath
monitorRulePage_selectSrcIP_posXpath = policyRulePage_selectSrcIP_posXpath
monitorRulePage_closeSrcIP_posXpath = policyRulePage_closeSrcIP_posXpath
monitorRulePage_negateSrcIP_posXpath = policyRulePage_negateSrcIP_posXpath
monitorRulePage_addApplication_posXpath = policyRulePage_addApplication_posXpath
monitorRulePage_searchApplication_posXpath = policyRulePage_searchApplication_posXpath
monitorRulePage_selectApplication_posXpath = policyRulePage_selectApplication_posXpath
monitorRulePage_closeApplication_posXpath = policyRulePage_closeApplication_posXpath
monitorRulePage_selectApplicationLabel_posXpath = policyRulePage_selectApplicationLabel_posXpath
monitorRulePage_selectApplicationGroupLabel_posXpath = policyRulePage_selectApplicationGroupLabel_posXpath
monitorRulePage_addCondition_posXpath = policyRulePage_addCondition_posXpath
monitorRulePage_packetCapture_posXpath = "//form[@class='el-form policy_edit el-form--label-left']//div[17]//span"
monitorRulePage_packetCapture_depth_posXpath = '//div[@class="MuiInputBase-root MuiOutlinedInput-root MuiInputBase-colorPrimary MuiInputBase-sizeSmall css-6a5w4u"]/input'
monitorRulePage_logOptions_all_posXpath = '//div[@ class="monitor-policy-log_option"]//button[2]'
monitorRulePage_okButton_warningYes_posXpath = "//button[@class='el-button el-button--default el-button--small el-button--primary operation-confirm']"
monitorRulePage_logOptions_all_posXpath = '//*[@id="monitor_log_options-_policy_monitor_write_Home_App_anonymousComponent"]//span[normalize-space(text())="All"]'
##monitor 添加profile的按钮
monitorRulePage_addVLANIDButton_posXpath = '//div[@class="monitor-policy-vlanID"]'
monitorRulePage_firstSelectMirrorProfile_posXpath='//div[@class="monitor-policy-mirror_profile"]//i'
monitorRulePage_searchMirrorProfile_posXpath = '//div[@class="px-[12px] py-[4px] flex"]//input'
monitorRulePage_selectMirrorProfile_posXpath = "//div[contains(@class, 'MuiListItemButton-root MuiListItemButton-colorNeutral MuiListItemButton-variantPlain css-18mv95p') and div[contains(text(), '{replaceValue}')]]"
monitorRulePage_addProfile_plusButton_posXpath= '//i[@class="iconfont icon-Create1"]'
monitorRulePage_addProfile_inputName_posXpath='//div[@class="[object Object]-name"]//input[@class="MuiInput-input css-fqt4w4"]'
monitorRulePage_addProfile_inputVLANID_posXpath='//div[@class="[object Object]-value"]//input'
monitorRulePage_addProfile_addVLANID_plusButton_posXpath='//div[@class="css-1v3ex2l"]/div[2]//i' #创建profile的时候多点了一步加号
monitorRulePage_saveProile_ok_posXpath='//div[@class="MuiDrawer-content css-10lcz44"]//div[@class="form-action bg-[--color-background] flex justify-center py-[12px] absolute bottom-0 w-full"]/button[1]'
monitorRulePage_saveProile_warningYes_posXpath='//button[@class="el-button el-button--default el-button--small el-button--primary operation-confirm"]'
#monitor新建页/编辑页按钮
monitorRulePage_enable_posXpath = '//*[text()="Enabled"]/ancestor::div[@class="MuiFormControl-root MuiFormControl-horizontal MuiFormControl-sizeMd css-90yvhw"]//*[@class="MuiSwitch-root MuiSwitch-sizeMedium css-wj9ris"]'
monitorRulePage_okButton_posId = '//div[@class="form-action bg-[--color-background] flex justify-center py-[12px] absolute bottom-0 w-full"]/button[1]'
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
monitorRulePage_addCondition_url_posXpath = "//div[@class='SourceList list-box']//div[normalize-space(text())='URL']  |  //div[@class='SourceList list-box']//div[normalize-space(text())='URI']"
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
statisticsRuleListPage_createButton_posXpath = ruleListPage_createButton_posXpath
statisticsRuleListPage_editButton_posXpath = ruleListPage_editButton_posXpath
statisticsRuleListPage_deleteButton_posXpath = ruleListPage_deleteButton_posXpath
statisticsRuleListpage_okButton_warningYes_posXpath = securityRuleListpage_okButton_warningYes_posXpath
statisticsRuleListPage_searchLabel_posXpath = ruleListPage_searchLabel_posXpath #
statisticsRuleListPage_searchLabel_dropDown_item_posXpath = ruleListPage_searchLabel_dropDown_item_posXpath #
statisticsRuleListPage_searchLabel_input_itemContent_posXpath = ruleListPage_searchLabel_input_itemContent_posXpath #
statisticsRuleListPage_searchLabel_searchButton_posXpath = ruleListPage_searchLabel_searchButton_posXpath #
statisticsRruleListPage_tableTbody_posXpath = ruleListPage_tableTbody_posXpath #
statisticsRruleListPage_allSelect_posXpath = ruleListPage_allSelect_posXpath #
statisticsRuleListPage_delete_tip_button_warningYes_posXpath = ruleListPage_delete_tip_button_warningYes_posXpath #"//button[@class='el-button delComponents-ok role-disconnect-btn el-button--default el-button--small']"
statisticsRuleListPage_delete_tip_button_warningNo_posXpath = ruleListPage_delete_tip_button_warningNo_posXpath #"//button[@class='el-button delComponents-close el-button--info el-button--small']"
# 名字输入定位
statisticsRulePage_inputName_posXpath = rulePage_inputName_posXpath
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
## Source IP Address的添加、查询、选中、关闭操作
statisticsRulePage_addSrcIP_posXpath = rulePage_button_add2Level_condition_posXpath.format(firstType="Source", secondType="IP Address") #"//div[@zs-label='Source']//div[normalize-space(text())='IP Address']/ancestor::div[@zs-label='SourceItem']//i[contains(@class, 'icon-Create1')]"
statisticsRulePage_searchSrcIP_posXpath = rulePage_object_list_search_input_posXpath #"//div[@class='SourceList list-box']//div[@class='CommonListDetail list-detail']//input[@id='object_ip_search']"
statisticsRulePage_selectSrcIP_posXpath = rulePage_object_list_select_name_posXpath #"//div[@class='SourceList list-box']//span[normalize-space(text())='{replaceValue}']"
statisticsRulePage_closeSrcIP_posXpath = rulePage_object_list_close_button_posXpath #"//div[@class='SourceList list-box']//div[@class='rigth-menu-button-info']//button"
# Source Port的添加、查询、选中、关闭操作
statisticsRulePage_addSourcePort_posXpath = rulePage_button_add2Level_condition_posXpath.format(firstType="Source", secondType="IP Port") #policyRulePage_addInternalPort_posXpath
statisticsRulePage_searchSourcePort_posXpath = rulePage_object_list_search_input_posXpath #policyRulePage_searchInternalPort_posXpath
statisticsRulePage_selectSourcePort_posXpath = rulePage_object_list_select_name_posXpath #policyRulePage_selectInternalPort_posXpath
statisticsRulePage_closeSourcePort_posXpath = rulePage_object_list_close_button_posXpath #policyRulePage_closeInternalPort_posXpath
# Source Subid User的添加、查询、选中、关闭操作
statisticsRulePage_addUser_posXpath = rulePage_button_add2Level_condition_posXpath.format(firstType="Source",secondType="User") #policyRulePage_addUser_posXpath
statisticsRulePage_searchUser_posXpath = rulePage_object_list_search_input_posXpath #policyRulePage_searchUser_posXpath
statisticsRulePage_selectUser_posXpath = rulePage_object_list_select_name_posXpath #policyRulePage_selectUser_posXpath
statisticsRulePage_closeUser_posXpath = rulePage_object_list_close_button_posXpath #policyRulePage_closeUser_posXpath
# Source Device imsi 的添加、查询、选中、关闭操作
statisticsRulePage_addImsi_posXpath = rulePage_button_add2Level_condition_posXpath.format(firstType="Source",secondType="Device") #policyRulePage_addImsi_posXpath
statisticsRulePage_searchImsi_posXpath = rulePage_object_list_search_input_posXpath #policyRulePage_searchImsi_posXpath
statisticsRulePage_selectImsi_posXpath = rulePage_object_list_select_name_posXpath #policyRulePage_selectImsi_posXpath
statisticsRulePage_closeImsi_posXpath = rulePage_object_list_close_button_posXpath #policyRulePage_closeImsi_posXpath
## Destination IP Address的添加、查询、选中、关闭操作
statisticsRulePage_addDstIP_posXpath = rulePage_button_add2Level_condition_posXpath.format(firstType="Destination",secondType="IP Address") #"//div[@zs-label='Destination']//div[normalize-space(text())='IP Address']/ancestor::div[@zs-label='SourceItem']//i[contains(@class, 'icon-Create1')]"
statisticsRulePage_searchDstIP_posXpath = rulePage_object_list_search_input_posXpath #"//div[@class='destinations list-box']//div[@class='CommonListDetail list-detail']//input[@id='object_ip_search']"
statisticsRulePage_selectDstIP_posXpath = rulePage_object_list_select_name_posXpath #"//div[@class='destinations list-box']//span[normalize-space(text())='{replaceValue}']"
statisticsRulePage_closeDstIP_posXpath = rulePage_object_list_close_button_posXpath #"//div[@class='destinations list-box']//div[@class='rigth-menu-button-info']//button"
# Source Port的添加、查询、选中、关闭操作
statisticsRulePage_addDestinationPort_posXpath = rulePage_button_add2Level_condition_posXpath.format(firstType="Destination",secondType="IP Port") #policyRulePage_addInternalPort_posXpath
statisticsRulePage_searchDestinationPort_posXpath = rulePage_object_list_search_input_posXpath #policyRulePage_searchInternalPort_posXpath
statisticsRulePage_selectDestinationPort_posXpath = rulePage_object_list_select_name_posXpath #policyRulePage_selectInternalPort_posXpath
statisticsRulePage_closeDestinationPort_posXpath = rulePage_object_list_close_button_posXpath #policyRulePage_closeInternalPort_posXpath
## Internal IP的添加、查询、选中、关闭操作
statisticsRulePage_addInternalIP_posXpath = rulePage_button_add2Level_condition_posXpath.format(firstType="Internal",secondType="IP Address") #policyRulePage_addInternalIP_posXpath
statisticsRulePage_searchInternalIP_posXpath = rulePage_object_list_search_input_posXpath #policyRulePage_searchInternalIP_posXpath
statisticsRulePage_selectInternalIP_posXpath = rulePage_object_list_select_name_posXpath #policyRulePage_selectInternalIP_posXpath
statisticsRulePage_closeInternalIP_posXpath = rulePage_object_list_close_button_posXpath #policyRulePage_closeInternalIP_posXpath
# Internal Port的添加、查询、选中、关闭操作
statisticsRulePage_addInternalPort_posXpath = rulePage_button_add2Level_condition_posXpath.format(firstType="Internal",secondType="IP Port") #policyRulePage_addInternalPort_posXpath
statisticsRulePage_searchInternalPort_posXpath = rulePage_object_list_search_input_posXpath #policyRulePage_searchInternalPort_posXpath
statisticsRulePage_selectInternalPort_posXpath = rulePage_object_list_select_name_posXpath #policyRulePage_selectInternalPort_posXpath
statisticsRulePage_closeInternalPort_posXpath = rulePage_object_list_close_button_posXpath #policyRulePage_closeInternalPort_posXpath
# External IP的添加、查询、选中、关闭操作
statisticsRulePage_addExternalIP_posXpath = rulePage_button_add2Level_condition_posXpath.format(firstType="External",secondType="IP Address") #policyRulePage_addExternalIP_posXpath
statisticsRulePage_searchExternalIP_posXpath = rulePage_object_list_search_input_posXpath #policyRulePage_searchExternalIP_posXpath
statisticsRulePage_selectExternalIP_posXpath = rulePage_object_list_select_name_posXpath #policyRulePage_selectExternalIP_posXpath
statisticsRulePage_closeExternalIP_posXpath = rulePage_object_list_close_button_posXpath #policyRulePage_closeExternalIP_posXpath
# External Port的添加、查询、选中、关闭操作
statisticsRulePage_addExternalPort_posXpath = rulePage_button_add2Level_condition_posXpath.format(firstType="External",secondType="IP Port") #policyRulePage_addInternalPort_posXpath
statisticsRulePage_searchExternalPort_posXpath = rulePage_object_list_search_input_posXpath #policyRulePage_searchInternalPort_posXpath
statisticsRulePage_selectExternalPort_posXpath = rulePage_object_list_select_name_posXpath #policyRulePage_selectInternalPort_posXpath
statisticsRulePage_closeExternalPort_posXpath = rulePage_object_list_close_button_posXpath #policyRulePage_closeInternalPort_posXpath
# Application的添加、查询、选中、关闭操作
statisticsRulePage_addApplication_posXpath = rulePage_button_add_condition_posXpath.format("Application") #policyRulePage_addApplication_posXpath
statisticsRulePage_searchApplication_posXpath = rulePage_object_list_search_input_posXpath #policyRulePage_searchApplication_posXpath
statisticsRulePage_selectApplication_posXpath = rulePage_object_list_select_name_posXpath #policyRulePage_selectApplication_posXpath
statisticsRulePage_closeApplication_posXpath = rulePage_object_list_close_button_posXpath #policyRulePage_closeApplication_posXpath
statisticsRulePage_selectApplicationLabel_posXpath = policyRulePage_selectApplicationLabel_posXpath
statisticsRulePage_selectApplicationGroupLabel_posXpath = policyRulePage_selectApplicationGroupLabel_posXpath
# Server FQDN的添加、查询、选中、关闭操作
statisticsRulePage_addServerFqdn_posXpath = rulePage_button_add2Level_condition_posXpath.format(firstType="Destination",secondType="Server FQDN")
statisticsRulePage_searchServerFqdn_posXpath = rulePage_object_list_search_input_posXpath #policyRulePage_searchServerFqdn_posXpath
statisticsRulePage_selectServerFqdn_posXpath = rulePage_object_list_select_name_posXpath #policyRulePage_selectServerFqdn_posXpath
statisticsRulePage_closeServerFqdn_posXpath = rulePage_object_list_close_button_posXpath #policyRulePage_closeServerFqdn_posXpath
# url的添加、查询、选中、关闭操作
statisticsRulePage_addUrl_posXpath = rulePage_button_add2Level_condition_posXpath.format(firstType="Protocol Field",secondType="URL")
statisticsRulePage_searchUrl_posXpath = rulePage_object_list_search_input_posXpath #policyRulePage_searchUrl_posXpath
statisticsRulePage_selectUrl_posXpath = rulePage_object_list_select_name_posXpath #policyRulePage_selectUrl_posXpath
statisticsRulePage_closeUrl_posXpath = rulePage_object_list_close_button_posXpath #policyRulePage_closeUrl_posXpath
# request header的添加、查询、选中、关闭操作
statisticsRulePage_addRequestHeader_posXpath = rulePage_button_add2Level_condition_posXpath.format(firstType="Protocol Field",secondType="Request Header") #policyRulePage_addRequestHeader_posXpath
statisticsRulePage_searchRequestHeader_posXpath = rulePage_object_list_search_input_posXpath #policyRulePage_searchRequestHeader_posXpath
statisticsRulePage_selectRequestHeader_posXpath = rulePage_object_list_select_name_posXpath #policyRulePage_selectRequestHeader_posXpath
statisticsRulePage_closeRequestHeader_posXpath = rulePage_object_list_close_button_posXpath #policyRulePage_closeRequestHeader_posXpath
# response header的添加、查询、选中、关闭操作
statisticsRulePage_addResponseHeader_posXpath = rulePage_button_add2Level_condition_posXpath.format(firstType="Protocol Field",secondType="Response Header") #policyRulePage_addRequestHeader_posXpath
statisticsRulePage_searchResponseHeader_posXpath = rulePage_object_list_search_input_posXpath #policyRulePage_searchRequestHeader_posXpath
statisticsRulePage_selectResponseHeader_posXpath = rulePage_object_list_select_name_posXpath #policyRulePage_selectRequestHeader_posXpath
statisticsRulePage_closeResponseHeader_posXpath = rulePage_object_list_close_button_posXpath #policyRulePage_closeRequestHeader_posXpath
# request Body的添加、查询、选中、关闭操作
statisticsRulePage_addRequestBody_posXpath = rulePage_button_add2Level_condition_posXpath.format(firstType="Protocol Field",secondType="Request Body") #policyRulePage_addRequestHeader_posXpath
statisticsRulePage_searchRequestBody_posXpath = rulePage_object_list_search_input_posXpath #policyRulePage_searchRequestHeader_posXpath
statisticsRulePage_selectRequestBody_posXpath = rulePage_object_list_select_name_posXpath #policyRulePage_selectRequestHeader_posXpath
statisticsRulePage_closeRequestBody_posXpath = rulePage_object_list_close_button_posXpath #policyRulePage_closeRequestHeader_posXpath
# Response Body的添加、查询、选中、关闭操作
statisticsRulePage_addResponseBody_posXpath = rulePage_button_add2Level_condition_posXpath.format(firstType="Protocol Field",secondType="Response Body") #policyRulePage_addRequestHeader_posXpath
statisticsRulePage_searchResponseBody_posXpath = rulePage_object_list_search_input_posXpath #policyRulePage_searchRequestHeader_posXpath
statisticsRulePage_selectResponseBody_posXpath = rulePage_object_list_select_name_posXpath #policyRulePage_selectRequestHeader_posXpath
statisticsRulePage_closeResponseBody_posXpath = rulePage_object_list_close_button_posXpath #policyRulePage_closeRequestHeader_posXpath
# Template添加按钮定位
statisticsRulePage_add_template_posXpath = rulePage_button_add_condition_posXpath.format("Statistics Template") #rulePage_object_list_search_input_posXpath #"//div[@class='el-form-item__content']/div[@class='addobject width300px addobject-long-list obj-content-null cursorPointer borderColor']"   # resposne code 选择框
statisticsRulePage_search_template_posXpath = rulePage_object_list_search_input_posXpath #"//div[@class='CommonListDetail list-detail']//div[contains(@class, 'object-item-seach')]//input"
statisticsRulePage_select_template_posXpath = rulePage_object_list_select_name_posXpath #"//div[@class='CommonListDetail list-detail']//div[@class='UaPopover TemplatePopover popover']"
statisticsRulePage_close_template_posXpath = rulePage_object_list_close_button_posXpath #"//div[@class='FlagList list-box']//div[@class='rigth-menu-button-info']"
# 保存策略时，ok cancel warnging定位
statisticsRulePage_enable_posXpath = rulePage_enable_posXpath
statisticsRulePage_okButton_posXpath = rulePage_okButton_posXpath # ""
statisticsRulePage_cancelButton_posXpath = rulePage_cancelButton_posXpath #"//div[@class='form-action bg-[--color-background] flex justify-center py-[12px] absolute bottom-0 w-full']//button[2]"
statisticsRulePage_okButton_warningYes_posXpath = rulePage_okButton_warningYes_posXpath #"//button[@class='el-button el-button--default el-button--small el-button--primary operation-confirm']"
statisticsRulePage_okButton_warningNo_posXpath = rulePage_okButton_warningNo_posXpath #"//button[@class='el-button el-button--default el-button--small el-button--primary operation-confirm']"
statisticsRulePage_delete_tip_button_warningYes_posXpath = rulePage_delete_tip_button_warningYes_posXpath #"//button[@class='el-button delComponents-ok role-disconnect-btn el-button--default el-button--small']"
statisticsRulePage_delete_tip_button_warningNo_posXpath = rulePage_delete_tip_button_warningNo_posXpath #"//button[@class='el-button delComponents-close el-button--info el-button--small']"

# 策略编辑界面右侧信息
statisticsRulePage_rightInfo_lastHitTime_posXpath = "//form[@class='el-form paper-grid-right el-form--label-top']//table//tr[1]//td[2]"
statisticsRulePage_rightInfo_firstHitTime_posXpath = "//form[@class='el-form paper-grid-right el-form--label-top']//table//tr[2]//td[2]"
statisticsRulePage_rightInfo_throughput_posXpath = "//form[@class='el-form paper-grid-right el-form--label-top']//table//tr[3]//td[2]"
statisticsRulePage_rightInfo_hitCount_posXpath = "//form[@class='el-form paper-grid-right el-form--label-top']//table//tr[4]//td[2]"
statisticsRulePage_rightInfo_72hoursHitCount_posXpath = "//form[@class='el-form paper-grid-right el-form--label-top']//table//tr[5]//td[2]"#//td[normalize-space(text())='Hit Count (72 hours)']/parent::tr/td[2]

# DoS Protection
dosRuleListPage_createButton_posXpath = '//*[@class="action-create inline-flex mr-[8px] "]'
dosRuleListPage_editButton_posXpath = '//*[@class="action-edit inline-flex mr-[8px] "]'
dosRuleListPage_deleteButton_posXpath ='//*[@class="action-delete inline-flex mr-[8px] "]'
dosRuleListpage_okButton_warningYes_posXpath = '//div[@class="MuiDialogActions-root flex !justify-center items-center MuiDialogActions-spacing css-vplbg4"]//button[normalize-space(text())="Yes"]'
dosRuleListpage_okButton_warningNo_posXpath = "//button[@class='el-button delComponents-close el-button--info el-button--small']"
dosRuleListPage_searchLable_posXpath = '//*[@class="MuiAutocomplete-wrapper MuiAutocomplete-multiple css-1h1ala5"]'
dosRuleListPage_searchLable_dropDown_item_posXpath = '//span[normalize-space(text())="{replaceValue}"]/../..'   #下拉菜单定位
dosRuleListPage_searchLable_input_itemContent_posXpath = '//*[@class="MuiInput-input css-1u0jcuo"]'  #输入item的值，replaceValue替换实际查询值
dosRuleListPage_searchLable_searchButton_posXpath = '//*[@class="MuiButtonBase-root MuiButton-root MuiButton-text MuiButton-textPrimary MuiButton-sizeSmall MuiButton-textSizeSmall MuiButton-colorPrimary MuiButton-root MuiButton-text MuiButton-textPrimary MuiButton-sizeSmall MuiButton-textSizeSmall MuiButton-colorPrimary css-1afa66w"]'
dosRuleListPage_tableTbody_posXpath = '//*[@class="MuiDataGrid-virtualScrollerRenderZone css-1inm7gi"]'
dosRuleListPage_allSelect_posXpath = '(//*[@class="MuiCheckbox-action css-kit57i"]/parent::span)[last()]'

dosRulePage_inputName_posXpath = '//*[@class="MuiInput-input css-fqt4w4"]'
dosRulePage_selectProtect_posXpath ='//button[normalize-space(text())="Protect"]'
dosRulePage_selectDeny_posXpath = "(//button[normalize-space(text())='Deny'])[1]"
dosRulePage_selectAllow_posXpath = "//button[normalize-space(text())='Allow']"

dosRulePage_addApplication_posXpath = "//label[normalize-space(text())='Application']/following-sibling::div/button"
dosRulePage_searchApplication_posXpath = '//*[@class="px-[12px] py-[4px] flex"]//input'
dosRulePage_selectApplication_posXpath = rulePage_object_list_select_name_posXpath #'//ul[@class="MuiList-root MuiList-vertical MuiList-variantPlain MuiList-colorNeutral MuiList-sizeMd css-1cklc3"]//li[1]//span[@class="truncate"]'
dosRulePage_closeApplication_posXpath ='//*[@class="MuiDrawer-content css-10lcz44"]//button[normalize-space(text())="Cancel"]'
dosRulePage_selectApplicationLabel_posXpath = ''

dosRulePage_addSrcIP_posXpath = "(//label[normalize-space(text())='IP Address']/following-sibling::div/button)[1]"
dosRulePage_searchSrcIP_posXpath = dosRulePage_searchApplication_posXpath
dosRulePage_selectSrcIP_posXpath = dosRulePage_selectApplication_posXpath
dosRulePage_closeSrcIP_posXpath = dosRulePage_closeApplication_posXpath

dosRulePage_thresholdRateType_posXpath = "//button[normalize-space(text())='Rate']"
dosRulePage_thresholdConcurrencyType_posXpath = "//button[normalize-space(text())='Concurrency']"
dosRulePage_groupBy_dropDownBox_posXpath = '//*[@class="dos-protection-policy-group_by"]'
dosRulePage_groupBy_select_posXpath = "//li[normalize-space(text())='{replaceValue}']"
dosRulePage_requestPerPeriod_posXpath = "//label[normalize-space(text())='Request Per Period']/parent::*//input"
dosRulePage_countingPeriod_dropDownBox_posXpath = '//*[@class="dos-protection-policy-counting_period"]'
dosRulePage_countingPeriod_select_posXpath =  "//ul[@class='base-Popper-root MuiSelect-listbox Mui-expanded css-icfck1']//li[normalize-space(text())='{replaceValue}']"
dosRulePage_concurrentSsessions_posXpath = "//label[normalize-space(text())='Concurrent Sessions']/parent::*//input"

dosRulePage_mitigationBehavior_deny_posXpath = "(//button[normalize-space(text())='Deny'])[last()]"
dosRulePage_mitigationBehavior_none_posXpath = "//button[normalize-space(text())='None']"
dosRulePage_mitigationTimeouts_dropDownBox_posXpath = "//label[normalize-space(text())='Mitigation Timeouts']/parent::*//button"
policyRulePage_mitigationTimeouts_select_posXpath =  "//ul[@class='base-Popper-root MuiSelect-listbox Mui-expanded css-icfck1']//li[normalize-space(text())='{replaceValue}']"
dosRulePage_mitigationTimeouts_select_top_posXpath = policyRulePage_mitigationTimeouts_select_posXpath
dosRulePage_mitigationTimeouts_select_bottom_posXpath =policyRulePage_mitigationTimeouts_select_posXpath

dosRulePage_enable_posXpath = '//*[@class="dos-protection-policy-is_enabled"]'
dosRulePage_ok_posXpath = "//button[normalize-space(text())='OK']"
dosRulePage_okButton_warningYes_posXpath = "//button[@class='el-button el-button--default el-button--small el-button--primary operation-confirm']"
dosRulePage_cancel_posId = "//button[normalize-space(text())='Cancel']"



