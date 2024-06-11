object_page_ln_select_brief_statistics='//*[@id="Briefbrief"]//span[text()="Brief"]'
#Audit Logs
new_audit_logs_record='//table/tbody/tr'
edit_audit_logs_record='(//table/tbody/tr)[2]'
#Object APN===================APN====================APN=================APN=======================APN=================APN================APN================APN================APN
#APN 列表页
listPage_object_apns_exportButton_posxpath = '//*[@class="iconfont icon-export"]' #export
listPage_object_apns_createButton_posId = "objectCreate-_OperateBtns_ElRow_Objects_apn_Home_App_anonymousComponent"    #create按钮id
listPage_object_apns_editButton_posXpah = '//*[@id="appEdit-_OperateBtns_ElRow_Objects_apn_Home_App_anonymousComponent"]//p[contains(text(),"Edit")]'        #edit按钮id
listPage_object_apns_edit_button_posId="appEdit-_OperateBtns_ElRow_Objects_apn_Home_App_anonymousComponent"
listPage_object_apns_delButton_posId = "appDel-_OperateBtns_ElRow_Objects_apn_Home_App_anonymousComponent"      #del按钮id
listPage_object_apns_del_yes_Button_poSeector = 'body > div.el-dialog__wrapper > div > div.el-dialog__footer > span > button.el-button.delComponents-ok.role-disconnect-btn.el-button--default.el-button--small > span'   #del_yes按钮

listPage_objectSearch_apns_selectLabel_posId="select-label" #查询框id
listPage_objectGroup_apns_createButton_posId="object1-_OperateBtns_ElRow_Objects_apn_Home_App_anonymousComponent" #Create-apn group按钮
listPage_object_apnsSelect_createButton_posId="object0-_OperateBtns_ElRow_Objects_apn_Home_App_anonymousComponent" #Create-apn 按钮

listPage_object_APNs_select_First_object_posXpath = '(//td[@rowspan="1"and @colspan="1"]//span[@class="el-checkbox__inner"])[1]'  #列表中第一行数据前的复选框
listPage_object_APNs_select_Second_object_posXpath ='(//td[@rowspan="1"and @colspan="1"]//span[@class="el-checkbox__inner"])[2]'#列表中第二行数据前的复选框
listPage_object_APNs_No_Data_posXpath='//*[@id="ly-table1-groupTable"]//*[@class="el-table__empty-text"]' #列表页No Data按钮
listPage_object_APNs_reference_count_posXpath='(//*[@class="obj-charts-btn pro-port cursorPointer textCenter"])[1]' #列表中第一个元素的reference count


#APN Create&Edit页
apn_ObjectPage_InputName_posXpath='//div[@class="rel-input el-input el-input--mini"]/input'#输入名字
apn_ObjectPage_NameLength_posXpath=''
apn_ObjectPage_addItem_posId = "temporary_form"  #添加item按钮 +
apn_ObjectPage_editItem_posId='//*[@id="router-view-container"]//i[@class="operate-icon iconfont icon-Edit"]' #edit item的安妮
apn_ObjectPage_inputItem_posXpath = '//div[@class="edit-input el-input el-input--small"]/input'    #输入item内容
apn_ObjectPagen_SaveItem_posXpath = '//i[@class="operate-icon iconfont icon-save check color31739C"]' # 保存item按钮

APNsObjectPage_textArea_Description_posXpath= '//*[@id="router-view-container"]//textarea[@placeholder="Please enter the content"]'    #description文本输入区Xpath
APNsObjectPage_button_SaveYes_posXpath = '//*[@id="OK-_apnDetail_Home_App_anonymousComponent"]/span'     # OK按钮
APNsObjectPage_button_warningSaveYes_posXpath = '//button[@class="el-button el-button--default el-button--small el-button--primary operation-confirm"]'   #提示保存Yes按钮警告框
APNsObjectPage_button_warningSaveCancel_posCss = ''    #提示保存取消按钮警告框
APNsObjectPage_button_cancel_posCss = ""      #Cancel按钮

apn_reference_count_list_xpath ='//*[@class="policy-item el-dropdown-menu__item"]' #usage quantity of APN

 #APNs Group Object Create&Edit页
apn_Group_InputName_posXpath='//*[@id="router-view-container"]//input[@maxlength="128"]'
APNs_Group_InputDescripton_posXpath='//*[@id="router-view-container"]//textarea[@maxlength="1024"]'
APNs_Group_sub_Object_addButton_posXpath = '//*[@id="router-view-container"]//div[@class="addobject width300px addobject-long-list obj-content-null cursorPointer borderColor"]'  # APNs_Group添加sub Object按钮
APNs_Group_sub_Object_add_exclude_Button_posXpath='(//div[@class="addobject width300px addobject-long-list obj-content-null cursorPointer borderColor"])[2]' #打开exclude 开关后添加exclude object
APNs_Group_sub_Object_add_new_Button_posXpath = '//*[@id="router-view-container"]//i[@class="iconfont icon-Create1"]'  #新建sub_APNs按钮 +    #ToDo
APNs_Group_sub_Object_add_new_Select_one_Button_posXpath = '//ul[@class="el-dropdown-menu el-popper el-dropdown-menu--small"][2]/li[1]'      #新建选择APNs按钮
APNs_Group_sub_Object_add_new_Select_Group_Button_posXpath = '//ul[@class="el-dropdown-menu el-popper el-dropdown-menu--small"][2]/li[2]'    #新建选择APNs_Group按钮
APNs_Group_sub_Object_list_Select_first_object_Button_posXpath='(//*[@id="router-view-container"]//div[@class="row-content-cell"])[1]' #Subordinate Objects列表页的第一个Object
#1.Sub Object为APN
APNs_Group_sub_Object_add_new_one_inputName_posXpath = '(//*[@id="router-view-container"]//input[@placeholder="Please enter the content"])[2]' # new APNs input Name
#APNs_Group_sub_Object_add_new_add_item_Button_posXpath = '//*[@id="temporary_form"]/i'  # new APNs add items Button + /
APNs_Group_sub_Object_add_new_add_item_Button_posXpath='//div[@class="EditDraw"]//*[@id="temporary_form"]/i'
APNs_Group_sub_Object_add_new_addAPN_item_posXpath = '(//*[@id="router-view-container"]//input[@type="text"])[last()]' # new APNs Item input
APNs_Group_sub_Object_add_new_add_itemAPN_Save_Button_posXpath = '//*[@class="operate-icon iconfont icon-save check color31739C"]'    # new FQDNs 保存item按钮
APNs_Group_sub_Object_add_new_one_OK1_Button_posXpath = '//*[@id="OK-_apnDetail_VDraswer_EditDraw_apnDetail_Home_App_anonymousComponent"]/span' # new APNs CreateOK1
APNs_Group_sub_Object_add_new_one_OK1_Warning_Yes_Button_posXpath = '//*[@class="el-button el-button--default el-button--small el-button--primary operation-confirm"]' # 再次确认创建new APNs
APNs_Group_sub_Object_add_new_one_OK1_Warning_Cancel_Button_posXpath = '/html/body/div[2]/div/div[3]/button[1]' # 再次确认取消new APNs
APNs_Group_sub_Object_add_new_one_Cancel2_Button_posXpath = '//*[@id="Cancle-_apnDetail_VDraswer_EditDraw_apnDetail_Home_App_anonymousComponent"]/span' # new APNs CreateCancel 右下角

APNs_Group_sub_Object_edit_Button_posXpath='//*[@id="OperateBtn-_OperateBtn_MemberItem_SubObjectsList_ElFormItem_ElForm_VPanel_VEditPanel_apnDetail_Home_App_anonymousComponent"]/i'  #sub object中编辑第一个Object的图标
APNs_Group_sub_Object_edit_add_Button_posXpath =   '(//*[@id="temporary_form"]/i)[last()]' #apn编辑页面的添加按钮
APNs_Group_sub_Object_edit_input_Button_posXpath =  APNs_Group_sub_Object_add_new_addAPN_item_posXpath #input
APNs_Group_sub_Object_edit_save_Button_posXpath =   '//*[@id="router-view-container"]//i[@class="operate-icon iconfont icon-save check color31739C"]'#save
APNs_Group_sub_Object_edit_ok_Button_posid ="OK-_apnDetail_VDraswer_EditDraw_apnDetail_Home_App_anonymousComponent" #OK
#APN查询页面,Object类似
listPage_objectSearch_APNs_select_Id_posXpath = '//li[@id="1-_FilteredSearch_ElRow_Objects_apn_Home_App_anonymousComponent"]'      #查询ID
listPage_objectSearch_APNs_select_Name_posXpath = '//li[@id="2-_FilteredSearch_ElRow_Objects_apn_Home_App_anonymousComponent"]'    #查询Name
listPage_objectSearch_APNs_select_Details_posXpath = '//*[@id="6-_FilteredSearch_ElRow_Objects_apn_Home_App_anonymousComponent"]' #查询Details
listPage_objectSearch_APNs_select_Description_posXpath = '//*[@id="4-_FilteredSearch_ElRow_Objects_apn_Home_App_anonymousComponent"]' #查询Description
listPage_objectSearch_APNs_select_all_posXpath = '//*[@id="1-_FilteredSearch_ElRow_Objects_apn_Home_App_anonymousComponent"]/preceding-sibling::li[1]' #查询所有

listPage_objectSearch_APNs_buttonSearch_posId = "searchQuery"   #查询按钮id
listPage_objectSearch_APNs_buttonClear_posId = "searchClear"      #清空查询按钮id

listPage_objectSearch_APNs_All_Button_posxpath='(//*[@id="router-view-container"]//span[@class="el-checkbox__inner"])[last()]' #列表页ALL Button
#Object Tunnel===================Tunnel====================Tunnel=================Tunnel=======================Tunnel=================Tunnel================Tunnel================Tunnel================APN
#Tunnel列表页
listPage_object_Tunnels_createButton_posId = "app_create-_OperateBtns_ElRow_Objects_tunnel_Home_App_anonymousComponent"   #create按钮id
listPage_object_Tunnels_editButton_posId = "appEdit-_OperateBtns_ElRow_Objects_tunnel_Home_App_anonymousComponent"        #edit按钮id #todo 改为id
listPage_object_Tunnels_editButton_posXPATH='//*[@id="appEdit-_OperateBtns_ElRow_Objects_tunnel_Home_App_anonymousComponent"]'
listPage_object_Tunnels_exportButton_posXPATH='//*[@class="el-button importAndExport el-button--default el-button--small"]' #export按钮
listPage_object_Tunnels_delButton_posId = "appDel-_OperateBtns_ElRow_Objects_tunnel_Home_App_anonymousComponent"      #del按钮id
listPage_object_Tunnels_delButton_posXPATH='//*[@id="appDel-_OperateBtns_ElRow_Objects_tunnel_Home_App_anonymousComponent"]'
listPage_object_Tunnels_del_yes_Button_posXpath = '//button[@class="el-button delComponents-ok role-disconnect-btn el-button--default el-button--small"]//span[contains(text(),"Yes")]'   #del_yes按钮

listPage_objectSearch_Tunnels_selectLabel_posId="select-label" #查询框id
listPage_objectSearch_Tunnels_buttonSearch_posId = "searchQuery"   #查询按钮id
listPage_objectSearch_Tunnels_buttonClear_posId = "searchClear"      #清空查询按钮id

listPage_objectSearch_Tunnels_AllButton_posxpath = listPage_objectSearch_APNs_All_Button_posxpath      #列表的All按钮
listPage_objectSearch_Tunnels_Total_posxpath = '//*[@id="pagination-_pagination_Objects_tunnel_Home_App_anonymousComponent"]//span[@class="el-pagination__total"]' #列表的总条数total
listPage_object_tunnel_type_Button_posXpath='//li[contains(@id,"dropColRes-_ElementSet")]//span[normalize-space(text())="Type"]' #Colum-Type Button
listPage_object_Tunnels_select_First_object_posXpath = listPage_object_APNs_select_First_object_posXpath  #列表中第一行数据前的复选框
listPage_object_Tunnels_select_second_object_posXpath=listPage_object_APNs_select_Second_object_posXpath #列表中第二行数据前的复选框

tunnel_export_pop_window_master_select_button_xpath='//div[@class="el-table__header-wrapper"]//span[@class="el-checkbox__inner"]'#导出object的弹窗中选择总按钮
tunnel_export_pop_window_first_checkbox_button_xpath='(//div[@class="el-dialog__body"]//span[@class="el-checkbox__inner"])[2]' #导出object的弹窗列表中第一条数据
tunnel_export_pop_window_export_num_button_xpath='//*[@class="multipleSelection"]'#计算导出弹窗中导出的个数是多少
tunnel_export_pop_no='(//*[@class="el-button delComponents-close el-button--default el-button--small"])'#导出弹窗中No

#Tunnel Create&Edit页
Tunnel_ObjectPage_InputName_posXpath='//*[@id="router-view-container"]//*[@placeholder="Please enter the content" and @type]'#输入名字#
Tunnel_ObjectPage_NameLength_posXpath='//*[(normalize-space(text())="32/32")]'#name超过32后，只截取32个字母，name输入框尾部为32/32
Tunnel_ObjectPage_ChangeColor_posid="swatches_btn-_Swatches_ElFormItem_ElForm_VPanel_VEditPanel_tunnelAdd_Home_App_anonymousComponent" # Color Change button
Tunnel_ObjectPage_YellowColor_posid="switchColor#FFC425" #switch color button
Tunnel_ObjectPage_inputItem_posXpath = '//*[@id="temporary_form"]/i'   #输入item内容
Tunnel_Edit_Page_Type="tunnelType"
Tunnel_Type_GRE='//span[contains(text(),"GRE")]'
Tunnel_Type_IP='//span[contains(text(),"IPv4/IPv6")]'
Tunnel_add_item_button='//*[@id="temporary_form"]/i'
tunnel_ip_list_first = '(//*[@id="router-view-container"]//div[@class="row-content-cell"])[1]'
tunnel_add_endpoint_b= '//*[@id="tunnelAddEndpoint-_tunnelAdd_Home_App_anonymousComponent"]'
tunnel_add_item_2='(//*[@id="temporary_form"]/i)[2]'
tunnel_ip_list_fourth='(//*[@id="router-view-container"]//div[@class="row-content-cell"])[9]'
tunnel_page_description='//*[@id="router-view-container"]//textarea'
tunnel_ip_list_close='(//*[@id="router-view-container"]//*[@class="el-button right-menu-button-close el-button--info el-button--small"])[1]'

tunnel_ip_list_add_button='//*[@id="router-view-container"]//i[@class="iconfont icon-Create1"]'
tunnel_ip_list_select_ip='//li[normalize-space(text())="Address"]'
tunnel_ip_list_select_ip_group='//li[normalize-space(text())="Address Group"]'
tunnel_ip_group_add_subobject='//*[@id="router-view-container"]//i[@class="iconfont icon-Create1 cursor"]'
tunnel_slide_ip_name='//*[@id="router-view-container"]//input[@placeholder="Please enter the content" and @maxlength="128"] '
tunnel_slide_ip_item_add='(//*[@id="temporary_form"]/i)[2]'
tunnel_slide_ip_item_input='//*[@id="router-view-container"]//input[@fetchsuggestions="function () { [native code] }"]'
tunnel_slide_ip_item_save='//*[@id="router-view-container"]//i[@class="operate-icon iconfont icon-save check"]'
tunnel_slide_ip_ok='//*[@id="OK-_IpDetail_VDraswer_EditDraw_tunnelAdd_Home_App_anonymousComponent"]'
tunnel_slide_ip_confirm_ok='//*[@class="el-button el-button--default el-button--small el-button--primary operation-confirm"]'
tunnel_item_search_frame = '(//*[@id="object_ip_search"])[1]'
tunnel_first_row_item='(//*[@id="router-view-container"]//div[@class="row-content-cell"])[1]'
tunnel_ip_group_first_row='//div[@class="IpDetail edit-page"]//div[@class="row-content-cell"][1]'


TunnelsObjectPage_button_SaveYes_posId = "OK-_tunnelAdd_Home_App_anonymousComponent"# OK按钮
TunnelsObjectPage_button_cancel_posId = "userBack-_tunnelAdd_Home_App_anonymousComponent"      #Cancel按钮#todo 改为id
TunnelsObjectPage_button_warningSaveYes_posSelector = 'body > div.el-message-box__wrapper > div > div.el-message-box__btns > button.el-button.el-button--default.el-button--small.el-button--primary.operation-confirm > span'   #提示保存Yes按钮警告框

#Tunnel查询页面,Object类似
listPage_objectSearch_Tunnels_select_all_xpath='//*[@id="1-_FilteredSearch_ElRow_Objects_tunnel_Home_App_anonymousComponent" ]/preceding-sibling::li[1]'
listPage_objectSearch_Tunnels_select_Id_posId = "1-_FilteredSearch_ElRow_Objects_tunnel_Home_App_anonymousComponent"      #查询ID
listPage_objectSearch_Tunnels_select_Name_posId = "2-_FilteredSearch_ElRow_Objects_tunnel_Home_App_anonymousComponent"    #查询Name
listPage_objectSearch_Tunnels_select_IP_posId = "100-_FilteredSearch_ElRow_Objects_tunnel_Home_App_anonymousComponent" #查询IP


#Object Attributes===================Attributes====================Attributes=================Attributes=======================Attributes=================Attributes================

# Attributes 列表页
listPage_object_Attributes_createButton_posId = "app_create-_OperateBtns_ElCol_ElRow_Application_customizedAttr_Home_App_anonymousComponent"  # create按钮id
listPage_object_Attributes_editButton_posId = "appEdit-_OperateBtns_ElCol_ElRow_Application_customizedAttr_Home_App_anonymousComponent" # edit按钮id #todo 改为id
listPage_object_Attributes_delButton_posId = "appDel-_OperateBtns_ElCol_ElRow_Application_customizedAttr_Home_App_anonymousComponent"  # del按钮id
listPage_object_Attributes_del_yes_Button_posXpath = listPage_object_Tunnels_del_yes_Button_posXpath # del_yes按钮

listPage_objectSearch_Attributes_selectLabel_posId = "select-label"  # 查询框id
listPage_objectSearch_Attributes_buttonSearch_posId = "searchQuery"  # 查询按钮id
listPage_objectSearch_Attributes_buttonClear_posId = "searchClear"  # 清空查询按钮id

listPage_object_Attributes_select_First_object_posXpath = listPage_object_APNs_select_First_object_posXpath # 列表中第一行数据前的复选框
listPage_object_Attributes_del_after_ele_posXpath='//*[@class="el-table__empty-text"]' #No data数据
# Attributes 查询页面,Object类似
listPage_objectSearch_Attributes_select_Id_posXpath = '//*[@id="1-_FilteredSearch_ElCol_ElRow_Application_customizedAttr_Home_App_anonymousComponent"]'  # 查询ID  #todo 都改为id
listPage_objectSearch_Attributes_select_Name_posId = "2-_FilteredSearch_ElCol_ElRow_Application_customizedAttr_Home_App_anonymousComponent"  # 查询Name
listPage_objectSearch_Attributes_input_Name_posXpath ='//input[@placeholder="Please enter search value"]'  #输入Name
listPage_objectSearch_Attributes_input_Id_posXpath =listPage_objectSearch_Attributes_input_Name_posXpath #输入Id
# Attributes Create&Edit页
Attributes_ObjectPage_InputName_posXpath = '//*[@id="application_name1"]'  # 输入名字
Attributes_ObjectPage_InputName_posId = "application_name1"
Attributes_ObjectPage_inputParentAttribute_posId = 'attr_parentadd-_Attribute_Home_App_anonymousComponent'  # 选择Parent Attribute +
AttributesObjectPage_UploadedFile_posXpath = '//*[@id="upload_file-_Attribute_Home_App_anonymousComponent"]//input[@name="file"]'  # 上传文件
Attributes_ExecutionTime_posXpath = '//*[@id="attr_time-_Attribute_Home_App_anonymousComponent"]/div/div/div/input'  # 最大执行时间
AttributeValueType_Bool="radio_method0-_Attribute_Home_App_anonymousComponent" #选择类型为布尔值
AttributeValueType_Numerical="radio_method1-_Attribute_Home_App_anonymousComponent" #选择类型Numerical
AttributeValueType_String="radio_method2-_Attribute_Home_App_anonymousComponent" #选择类型为String
Attributes_Select_inputParentAttribute_tcppayload='//div[normalize-space(text())="tcp.payload"]'#todo,需要修改
Attributes_Select_ParentAttribute_tcp='//div[normalize-space(text())="tcp"]' #定位方式
Attributes_Select_ParentAttribute_tcp_payload_c2s_first_data_xpath='//div[normalize-space(text())="tcp.payload.c2s_first_data"]'

AttributesObjectPage_button_SaveYes_posId = "attrAdd_ok-_Attribute_Home_App_anonymousComponent"  # OK按钮
AttributesObjectPage_button_cancel_posId = "attrAdd_cancel-_Attribute_Home_App_anonymousComponent"  # Cancel按钮#todo 改为id
AttributesObjectPage_button_warningSaveYes_posXpath = '//button[@class="el-button el-button--default el-button--small el-button--primary operation-confirm"]'  # 提示保存Yes按钮警告框
AttributesObjectPage_button_warningSaveCancel_posId = '//button[@class="el-button el-button--default el-button--small operation-cancel"]'  # 提示保存取消按钮警告框#todo 改为id

#Attributes模块栏目查询
##Object模块查询栏
Userdefined_first_row_first_column_posXpath = '//th[1]//*[normalize-space(text())="ID"]'                               # 第一行、第一列
Userdefined_second_row_first_column_posXpath = '//tr[1]/td[1]/div//div[4]/span'                                   # 第二行、第一列

Userdefined_first_row_second_column_posXpath = '//th[2]//*[normalize-space(text())="Vsys ID"]'                                            # 第一行、第二列
Userdefined_second_row_second_column_posXpath = '//*[@id="app-table"]/div[3]/table/tbody/tr[1]/td[2]/div | //div[3]/table/tbody/tr[1]/td[2]/div/div/span'                                              # 第二行、第二列

Userdefined_first_row_third_column_posXpath = '//tr/th[3]//span[normalize-space(text())="Attribute Name" or normalize-space(text())="Name"]'               # 第一行、第三列
Userdefined_second_row_third_column_posXpath = '//*[@id="app-table"]/div[3]/table/tbody/tr[1]/td[3]/div/div | //div[3]/table/tbody/tr[1]/td[3]/div/div/div | //div[3]/table/tbody/tr[1]/td[3]/div/div/span/span/span'                                   # 第二行、第三列
#Object Signatures===================Signatures====================Signatures=================Signatures=======================Signatures=================Signatures================
#Signatures列表页的公共元素和Attribute相同，可以复用。
listPage_object_signature_createButton_posId = "app_create-_OperateBtns_ElCol_ElRow_Application_appSignatures_Home_App_anonymousComponent"  # create按钮id
listPage_object_signature_editButton_posId = "appEdit-_OperateBtns_ElCol_ElRow_Application_appSignatures_Home_App_anonymousComponent" # edit按钮id #todo 改为id
listPage_object_signature_delButton_posId = "appDel-_OperateBtns_ElCol_ElRow_Application_appSignatures_Home_App_anonymousComponent"  # del按钮id
listPage_object_signature_del_yes_Button_posXpath = listPage_object_Tunnels_del_yes_Button_posXpath  # del_yes按钮
listPage_object_signature_select_First_object_posXpath =listPage_object_APNs_select_First_object_posXpath #signature列表页第一行数据
listPage_objectSearch_signature_select_Id_posXpath = '//*[@id="1-_FilteredSearch_ElCol_ElRow_Application_appSignatures_Home_App_anonymousComponent"]'  # 查询ID  #todo 都改为id
listPage_objectSearch_signature_select_Name_posId = "2-_FilteredSearch_ElCol_ElRow_Application_appSignatures_Home_App_anonymousComponent"  # 查询Name
listPage_objectSearch_signature_input_Name_posXpath =listPage_objectSearch_Attributes_input_Id_posXpath  #输入Name
Signatures_built_arrtribute_icon_pasXpath ='//div[@class = "el-collapse"]//div[@class = "el-collapse-item is-active"]//*[contains(@class,"icon svg-icon") and not(@style="display: none;")]' #通过内置图标获取所有内置特征
Signatures_built_arrtribute_pasXpath = '//div[@class = "el-collapse"]//div[@class = "el-collapse-item"]' #获取内置特征
list_page_no_data = listPage_object_APNs_No_Data_posXpath #No Data
listPage_signature_first_condition_all_button='(//*[@class="iconfont icon-Conditions tsg-object-icon22 icon-default-color fontsize18"])[1]'
listPage_condition_slide_search_frame='//*[@id="object_ip_search"]'

#Create Signature按钮，Attribute选择general.session.analysis.ap……，Application选择http
Signatures_ObjectPage_InputName_posId = "ApplicationSignaturesAdd_signatureName1" #输入名字
Signatures_ObjectPage_inputParentSignature_posId = 'openSideslipOrCondition'
plus_button='//*[@id="openSideslipOrCondition"]'
addto_condition_button_xpath = '//*[@class="el-form-item el-form-item--small"]//*[@readonly="readonly"]'  # 选择Add按钮的XPath路径
new_condition_button_xpath = '//*[text()="New Condition"]'  # 选择New Condition按钮的XPath路径
new_not_condition_button_xpath = '//*[text()="New Not Condition"]'  # 选择New Not Condition按钮的XPath路径
attribute_name_input_id = "Attribute_Name"  # 选择Attribite Name输入框的ID
general_dropdown_xpath = '//*[text()="tcp"]'  # 选择general下拉框的XPath路径
general_session_analysis_app_id_xpath = '//*[normalize-space(text())="tcp.payload"]'  # 选中general.session.analysis.app_id
select_application_condition_xpath = '//*[@id="orCondition_id"]/i'  # 选择Application+的ID
first_http_checkbox_xpath = '//ul[@class="row-container tableList"]/li[1]//*[@class="reference-box el-popover__reference"]'  # 选择第一个keyword的XPath路径
second_http_checkbox_xpath='//ul[@class="row-container tableList"]/li[2]//*[@class="reference-box el-popover__reference"]'
#first_ssl_checkbox_xpath='//*[@id="router-view-container"]//span[@class="ellipsis list-popover-click" and normalize-space(text())="ssl"]'
second_item_checkbox_xpath = '//ul[@class="row-container tableList"]/li[2]//*[@class="reference-box el-popover__reference"]'  # 选择第一个keyword的XPath路径

ok_button_id = "ApplicationSignaturesAdd_ok"  # OK按钮的ID
ok_component_id = "ApplicationSignaturesAdd_ok_component"  # Object界面的OK按钮的ID(Condition界面)
cancel_component_id = "ApplicationSignaturesAdd_cancel_component"  # Object界面的Cancel按钮的ID
cancel_confirm_yes_button='//button[@class="el-button el-button--default el-button--small el-button--primary operation-confirm-Leave"]'
confirm_yes_button_xpath = '(//*[normalize-space(text())="Yes"])[2]'  # 弹窗再次确认保存Yes按钮的XPath路径
signature_page_total_item='//*[@id="router-view-container"]//div[@class="conditionTotal"]'
signature_edit_page_add_attribute_button='//button[@class="el-button el-button--default el-button--mini"]' #signature edit page add attribute button
signature_Attributes_ObjectPage_InputName_posId = "application_name1"
signature_Attributes_ObjectPage_inputParentAttribute_posId = "attr_parentadd-_Attribute_anonymousComponent_VDraswer_ApplicationSignaturesAdd_Home_App_anonymousComponent"  # 选择Parent Attribute +
signature_attr_search = '(//*[@class="inline el-input__inner"])[2]'#搜索框
signature_attribute_tcp_payload = '(//div[normalize-space(text())="tcp.payload"])[2]'

signature_AttributesObjectPage_UploadedFile_posXpath = '//*[@id="upload_file-_Attribute_anonymousComponent_VDraswer_ApplicationSignaturesAdd_Home_App_anonymousComponent"]/div/div/div/div/input'  # 上传文件
signature_Attributes_ExecutionTime_posXpath = '//*[@id="attr_time-_Attribute_anonymousComponent_VDraswer_ApplicationSignaturesAdd_Home_App_anonymousComponent"]/div/div/div/input'  # 最大执行时间
signature_AttributeValueType_Bool="radio_method0-_Attribute_anonymousComponent_VDraswer_ApplicationSignaturesAdd_Home_App_anonymousComponent" #选择类型为Numerical

ok1 = '//*[@id="attrAdd_ok-_Attribute_anonymousComponent_VDraswer_ApplicationSignaturesAdd_Home_App_anonymousComponent"]' #ok
ok2 = '//*[@class="el-button el-button--default el-button--small el-button--primary operation-confirm"]' #confirm yes
#Object appgroup===================appgroup====================appgroup=================appgroup=======================appgroup=================appgroup================

#app group列表頁的公共元素的和Attribute相同，可以復用
listPage_object_app_group_createButton_posId = "app_create-_OperateBtns_ElCol_ElRow_Application_appGroups_Home_App_anonymousComponent"  # create按钮id
listPage_object_app_group_editButton_posId ="appEdit-_OperateBtns_ElCol_ElRow_Application_appGroups_Home_App_anonymousComponent" # edit按钮id #todo 改为id
listPage_object_app_group_delButton_posId = "appDel-_OperateBtns_ElCol_ElRow_Application_appGroups_Home_App_anonymousComponent"  # del按钮id
listPage_object_app_group_del_yes_Button_posXpath = listPage_object_Tunnels_del_yes_Button_posXpath  # del_yes按钮

listPage_object_app_group_select_First_object_posXpath =listPage_object_APNs_select_First_object_posXpath #signature列表页第一行数据

listPage_objectSearch_app_group_select_Id_posXpath = '//*[@id="1-_FilteredSearch_ElCol_ElRow_Application_appGroups_Home_App_anonymousComponent"]'  # 查询ID  #todo 都改为id
listPage_objectSearch_app_group_select_Name_posId = "2-_FilteredSearch_ElCol_ElRow_Application_appGroups_Home_App_anonymousComponent" # 查询Name
listPage_objectSearch_app_group_input_Name_posXpath ='//*[@id="profileName"]/div[3]/div/input'  #输入Name

list_page_no_data_app_group= listPage_object_APNs_No_Data_posXpath #No Data
#app group列表頁
# listPage_object_appgroup_createButton_posId = "app_create-_OperateBtns_ElCol_ElRow_Application_Home_App_anonymousComponent"  # create按钮id
# listPage_object_appgroup_editButton_posId = "appEdit-_OperateBtns_ElCol_ElRow_Application_Home_App_anonymousComponent"  # edit按钮id #todo 改为id
# listPage_object_appgroup_delButton_posId = "appDel-_OperateBtns_ElCol_ElRow_Application_Home_App_anonymousComponent"  # del按钮id
# listPage_object_appgroup_del_yes_Button_posXpath = '//div[@class="el-dialog__wrapper"]/div/div[3]/span/button[1]/span'  # del_yes按钮

listPage_objectSearch_appgroup_selectLabel_posId = "select-label"  # 查询框id
listPage_objectSearch_appgroup_buttonSearch_posId = "searchQuery"  # 查询按钮id
listPage_objectSearch_appgroup_buttonClear_posId = "searchClear"  # 清空查询按钮id

# listPage_first_appgroup_checkbox_xpath = '//*[@id="ly-table1-groupTable"]//tbody/tr[1]/td[1]/div//div/label'  # 列表页第一个数据的复选框
#listPage_no_appgroup_xpath = '//*[@id="ly-table1-groupTable"]//span[@class="el-table__empty-text"]'  # No data数据

#apn group create
appgroup_inputname_xpath='//*[@id="router-view-container"]//input[@placeholder="Please enter the content"]'#name输入框
application_select_box_xpath = '(//*[@id="router-view-container"]//i[@class="iconfont icon-Create1 cursor"])[1]'  # Application选择框大➕
application_select_little_plus_xpath='(//*[@id="router-view-container"]//div[@class="object-item-add"])[1]'
http_selection_xpath = '(//*[@id="router-view-container"]//*[normalize-space(text())="http"])[2]'  # 选择http
appgroup_exclude_app_switch_xpath = '//*[@id="router-view-container"]//span[@class="el-switch__core"]'  # Exclude App开启框
appgroup_exclude_app_selection_xpath = '(//*[@id="router-view-container"]//i[@class="iconfont icon-Create1 cursor"])[2]'  # 选择Exclude App
ssl_selection_xpath = '(//*[@id="router-view-container"]//*[normalize-space(text())="dns"])[2]'  # 选择ssl
ftp_selection_xpath='(//*[@id="router-view-container"]//*[normalize-space(text())="ftp"])[2]'
appgroup_description_input_xpath = '//*[@id="router-view-container"]//textarea'  # description输入框

appgroup_ok_button_posId = "OK-_AppGroupDetail_Home_App_anonymousComponent"  # OK
appgroup_confirm_ok_button_xpath = '//*[@class="el-button el-button--default el-button--small el-button--primary operation-confirm"]'  # confirm ok
appgroup_cancel_button_posId = "Cancle-_AppGroupDetail_Home_App_anonymousComponent"  # cancel
appgroup_confirm_appgroup_cancel_button_xpath = '//*[@class="el-button el-button--default el-button--small el-button--primary operation-confirm"]'  # confirm cancel

appgroup_slide_app_ok='//*[@id="application_sub-_AppOperate_VDraswer_EditDraw_AppGroupDetail_Home_App_anonymousComponent"]/span'
appgroup_slide_app_confirm_ok='//button[@class="el-button el-button--default el-button--small el-button--primary operation-confirm"]'
appgroup_slide_app_add_signature_button='//*[@id="application_signature"]/i'
appgroup_slide_app_list_first_one='(//*[@class="white-space"])[1]'
appgroup_slide_app_name='(//*[@id="router-view-container"]//input[@placeholder="Please enter the content"])[2]'
appgroup_slide_risk='(//*[@id="application_subcategory0-_AppOperate_VDraswer_EditDraw_AppGroupDetail_Home_App_anonymousComponent"])[3]'
appgroup_total_1='(//*[@id="router-view-container"]//div[@class="total textRight"])[1]'
appgroup_total_2='(//*[@id="router-view-container"]//div[@class="total textRight"])[2]'
appgroup_first_row_item_in_app='(//*[@id="router-view-container"]//div[@class="row-content-cell"])[1]'
#Object application===================application====================application=================application=======================application=================application================
#app group列表頁的公共元素的和Attribute相同，可以復用
#app group列表頁
listPage_object_application_createButton_posId = "app_create-_OperateBtns_ElCol_ElRow_Application_Home_App_anonymousComponent"  # create按钮id
listPage_object_application_editButton_posId = "appEdit-_OperateBtns_ElCol_ElRow_Application_Home_App_anonymousComponent"  # edit按钮id #todo 改为id
listPage_object_application_delButton_posId = "appDel-_OperateBtns_ElCol_ElRow_Application_Home_App_anonymousComponent"  # del按钮id
listPage_object_application_del_yes_Button_posXpath = listPage_object_Tunnels_del_yes_Button_posXpath  # del_yes按钮

listPage_objectSearch_application_selectLabel_posId = "select-label"  # 查询框id
listPage_objectSearch_application_buttonSearch_posId = "searchQuery"  # 查询按钮id
listPage_objectSearch_application_buttonClear_posId = "searchClear"  # 清空查询按钮id

listPage_first_application_checkbox_xpath = listPage_object_APNs_select_First_object_posXpath # 列表页第一个数据的复选框
listPage_no_application_xpath = '//*[@id="app-table-_AppTable_Application_Home_App_anonymousComponent"]//span[@class="el-table__empty-text"]'  # No data数据

application_listPage_All_id="appAll0" #All按鈕
application_listPage_builtin_id="appAll1" #Buit-in按鈕
application_listPage_imported_id="appAll2" #imported按鈕

#app create&modify
application_inputname_xpath='//*[@id="router-view-container"]//input[@placeholder="Please enter the content"]'#name输入框
application_input_longname_xpath='//*[@id="application_longname1"]'#long name输入框
application_description_input_xpath = '//*[@id="router-view-container"]//textarea'  # description输入框
application_select_category_dropwmn_id = "application_eventkeying1"  # Category select

application_select_subcategory_dropwmn_id =  "application_eventkeying2" # Subcategory select
application_select_content_dropwmn_id = "application_eventkeying3" # Content select
application_select_risk_dropwmn_id = "application_eventkeying4"  # Risk select

application_select_parentapp_dropdown_xpath = '//*[@id="application_parentApp"]'  # Parent App下拉框
application_select_signature_dropwmn_id="application_signature"#signature dropdown

application_ok_button_posId = "application_sub-_AppOperate_Home_App_anonymousComponent"  # OK
application_confirm_ok_button_xpath = appgroup_confirm_ok_button_xpath  # confirm ok
application_cancel_button_posId = "application_back-_AppOperate_Home_App_anonymousComponent"  # cancel
application_confirm_application_cancel_button_xpath = appgroup_confirm_appgroup_cancel_button_xpath  # confirm cancel'

application_category_businesystem_xpath='//*[(normalize-space(text())="business-systems")]'
application_subcategory_authservice_xpath='//*[(normalize-space(text())="auth-service")]'
application_content_voicecall_xpath='//*[(normalize-space(text())="voice-call")]'
application_risk_is0_xpath='(//*[@id="application_subcategory0-_AppOperate_Home_App_anonymousComponent"])[3] '#risk為0時則subcategory0，risk為1則是subcategory1

app_category_xpath='//*[@id="application_category{}-_AppOperate_Home_App_anonymousComponent"]'  #0-4
app_sub_category_xpath='(//*[@id="application_subcategory{}-_AppOperate_Home_App_anonymousComponent"])[3] |  //*[@id="application_subcategory{}"]' #0-3
app_content_xpath='(//*[@id="application_subcategory{}-_AppOperate_Home_App_anonymousComponent"])[last()]' #0-3
app_risk_xpath='(//*[@id="application_subcategory{}-_AppOperate_Home_App_anonymousComponent"])[last()]' #0-3
app_characteristics_xpath='(//*[@class="el-checkbox"]//span[@class="el-checkbox__inner"])[{}]' #1-9


Object_Application_set_button = '//span[@id="eventfixed"]/i'
Object_Application_select_cancel = '//button[@id="dropColALlFalse-_ElementSet_AppTable_Application_Home_App_anonymousComponent"]'
Object_Application_select_Ok = '//button[@id="dropColOK-_ElementSet_AppTable_Application_Home_App_anonymousComponent"]/span'
Object_Application_column_default = '//table/thead/tr/th[{}]/div/div/span'
Object_Application_select_All = '//button[@id="dropColAll-_ElementSet_AppTable_Application_Home_App_anonymousComponent"]'
Object_Application_import_button_xpath = '(//button[@class="el-button importAndExport el-button--default el-button--small"]/i)[1]'
Object_Application_upload_button_xpath = '//input[@class="el-upload__input"]'
Object_Application_file_ok = '(//button[@class="el-button right-menu-button-close el-button--info el-button--small"])[4]'
Object_Application_success_detail_css = '.el-message__content'
Object_Application_Name_column = '//table/tbody/tr[{}]/td[4]/div/div[1]'
Object_Application_page_number = '//div[@id="pagination-_pagination_AppTable_Application_Home_App_anonymousComponent"]/div[1]/ul/li[{}]'
Object_Application_next_page = '//div[@id="pagination-_pagination_AppTable_Application_Home_App_anonymousComponent"]/div[1]/button[2]/i'
Object_Application_page_input_xpath = '//div[@id="pagination-_pagination_AppTable_Application_Home_App_anonymousComponent"]/div[1]/span/div/input'
Object_Application_Audit_Logs_xpath ='//i[@class="iconfont icon-a-Adminlogs icon-style"]'
Object_Application_Audit_Logs_page_xpath = '//div[@class="LocalationDraswer lstsub right-show-edit right-show-edit-other"]/div/div/div[@class="rm-top"]/span[1]'
Object_Application_create_cancel = '//button[@id="application_back-_AppOperate_Home_App_anonymousComponent"]'
Object_Application_first_column = '//*[@id="app-table-_AppTable_Application_Home_App_anonymousComponent"]/div[3]/table/tbody/tr/td[{}]'
Object_Application_create_Category_first = '(//*[@class="el-select-dropdown__item selected"])[last()]'
Object_Application_create_blank = '//*[@id="application_description"]'
Object_Application_create_Subcategory_first = Object_Application_create_Category_first
Object_Application_create_Content_first = Object_Application_create_Category_first
Object_Application_create_Risk_first = Object_Application_create_Category_first
Object_Application_input_error_name = '//div[@class="el-form-item__error"]'
Object_Application_upload_error_detail_xpath = '//div[@class="importTips"]/p'
Object_Application_properties_error_xpath = '(//div[@class="el-form-item__error"])[{}]'
Object_Application_upload_repeat_error_xpath = '(//div[@class="el-table__body-wrapper is-scrolling-none"]/table[@class="el-table__body"]/tbody/tr[@class="el-table__row"]/td[3]/div[@class="cell"])[3]'
Object_Application_upload_cancel = '(//button[@class="el-button right-menu-button-close el-button--info el-button--small"])[4]'
Object_Application_clear_search_input = '//*[@id="searchClear"]'
Object_Application_create_drop_input_xpath = '//*[@class="denyAction"]//input[@class="el-input__inner"]'
Object_Application_create_drop_input_error = '//*[@id="proxy-_AppOperate_Home_App_anonymousComponent"]//div[@class="el-form-item__error"]'
Object_Application_create_limit_error = '//*[@id="proxy-_AppOperate_Home_App_anonymousComponent"]//div[@class="el-form-item__error"]'



Object_Application_create_first_signature_edit = '(//i[@id="application_proadd10"])[1]'  #编辑Application页面Signature的按钮
Object_Application_create_signature_name_input = '//input[@id="ApplicationSignaturesAdd_signatureName1"]'
Object_Application_create_edit_signature_add_condition_button = '//div[@id="openSideslipOrCondition"]/i'
#Object_Application_create_edit_signature_add_to_input = '(//form/div[1]/div/div/div/input)[2]'
#Object_Application_create_edit_signature_add_to_Condition1_selector ='//ul[@class="el-scrollbar__view el-select-dropdown__list"]/li/span[text()="New Condition"]'   #Add to下拉框的Condition1的xpath路径
#Object_Application_create_edit_signature_Attribute_name_input = '//div[@id="Attribute_Name"]'   #edit_signature模块下Condition中Attribute添加按钮xpath路径
Edit_signature_Condition_Attribute_ip = '(//div[@class="el-collapse-item__header"])[{}]'             #Traffic Attribute下的ip项路径
Edit_signature_Condition_Attribute_ip_src = '//div[@class="el-collapse-item is-active"]/div[@class="el-collapse-item__wrap"]/div/div[contains(text(),"ip.src")]'   #ip.src项
Edit_signature_Condition_Add_IP_button = '//div[@id="orCondition_id"]/i[@class="iconfont icon-Create1"]'   #添加IP按钮
Edit_signature_Condition_Add_IP_choose = '(//div[@class="el-checkbox-group"]/ul/li/label[1]/span/div/span/div/span)[{}]'
Edit_signature_Condition_OK_button = '//button[@id="ApplicationSignaturesAdd_ok"]'
Edit_signature_OK_button = '//button[@id="ApplicationSignaturesAdd_ok_component"]'
Edit_signature_OK_button_confirm_yes = '//div[@class="el-message-box__btns"]/button[2]'
Edit_signature_Create_ip_OK =  '//*[@id="OK-_IpDetail_orConditionSideslip_ElFormItem_AttributeType_ElForm_anonymousComponent_VDraswer_ApplicationSignaturesAdd_AppOperate_Home_App_anonymousComponent"]'
Edit_signature_Create_FQND_ok = '//*[@id="OK-_FqdnDetail_orConditionSideslip_ElFormItem_AttributeType_ElForm_anonymousComponent_VDraswer_ApplicationSignaturesAdd_AppOperate_Home_App_anonymousComponent"]'
Edit_signature_Create_FQND_confirm_yes = '//*[@class="el-button el-button--default el-button--small el-button--primary operation-confirm"]'
User_defined_search_type_name = '//ul[@class="el-scrollbar__view el-select-dropdown__list"]/li/span[text()="Name"]'
User_defined_search_type_name_input = listPage_objectSearch_Attributes_input_Name_posXpath
User_defined_search_type_delete = '//*[@class="el-tooltip tooltip"]/p[contains(text(),"Delete")]'
User_defined_search_type_delete_confirm_yes = '//*[@class="el-button delComponents-ok role-disconnect-btn el-button--default el-button--small"]'
Edit_signature_Condition_edit_button = '//div[@id="hijackAddContentType"]//i[@class="iconfont icon-Edit edit conditionEdit"]'
edit_signature_condition_attribute_name_button='//*[@id="Attribute_Name"]//span[@class="float-left addspanover bifang-obj-content-objectName-fields-new"]'
Edit_signature_Condition_clear_attribute = '(//i[@class="iconfont icon-Delete_X float-right"])[1]'
#Edit_signature_Condition_active_second = '//div[@class="el-collapse-item is-active"]/div[@class="el-collapse-item__wrap"]/div/div[2]'
Edit_signature_Condition_active_first = '(//div[@class="el-collapse-item is-active"]//*[@class="el-tooltip el-dropdown-menu__item relative-item cursorPointer item"])[1]'
Edit_signature_Condition_add_FQDN = '//div[@id="orCondition_id"]/i'
Edit_signature_Condition_add_items = '//div[@id="temporary_form"]/i'
User_defined_search_result_first =listPage_object_APNs_select_First_object_posXpath
User_defined_edit_button = listPage_object_signature_editButton_posId
#Edit_signature_remove_first_condition = '//div[@id="hijackAddContentType"]/div[2]/div/div[2]/div/div[2]/i[2]'        #Edit Signature页面移除第一行condition按钮xpath路径
User_defined_edit_signature_create_ip_ok = '//*[@id="OK-_IpDetail_orConditionSideslip_ElFormItem_AttributeType_ElForm_anonymousComponent_VDraswer_ApplicationSignaturesAdd_Home_App_anonymousComponent"]'   #user_define页面的创建ip时的保存ok按钮路径
User_defined_edit_signature_create_fqdn_ok = '//*[@id="OK-_FqdnDetail_orConditionSideslip_ElFormItem_attribute-type_ElForm_anonymousComponent_VDraswer_ApplicationSignaturesAdd_Home_App_anonymousComponent"]'#user_define页面的创建fqdn时的保存ok按钮路径
Edit_Ip_input = '//input[@placeholder="Please enter the content" and @value-key="label"]'
Edit_Ip_input_save_xpath = '//*[@class="operate-icon iconfont icon-save check"]'
Edit_Ip_OK = '//*[@id="OK-_IpDetail_Home_App_anonymousComponent"]'
Edit_Ip_OK_confirm_yes = '(//div[@class="el-message-box__btns"]/button)[2]'
Edit_fqdn_button = '//*[@id="appEdit-_OperateBtns_ElRow_Objects_fqdn_Home_App_anonymousComponent"]//p[@class="text-content text"]'
Edit_fqdn_clear_first_condition = '//*[@class="operate-icon iconfont icon-Delete_X del"]'
Edit_fqdn_items_input = '//input[@id="onlyMarvel"]'
Edit_fqdn_items_input_save = '//*[@id="router-view-container"]//i[@class="operate-icon iconfont icon-save save-color"]'   #输入item后保存按钮xpath路径
Edit_fqdn_Ok_button = '//*[@id="OK-_FqdnDetail_Home_App_anonymousComponent"]'
Fqdns_first_details = '(//*[@id="multilineItemDetails-_MultilineTableCell_ElTableBody_ElTable_Objects_fqdn_Home_App_anonymousComponent"]//span[@class="el-tooltip tsg_ellipsis mouse-hover-click"])[1]'    #fqdn下第一行的details内容xpath路径
Applications_create_signature_input = '//*[@id="objectName_seach-_checkList_component_Surrogate_component_ElForm_AppOperate_Home_App_anonymousComponent"]'
Applications_vote_signature_first_view = '(//*[@class="iconfont icon-View"])[1]'

app_signature_attribute_new_fqdn_add_button= '(//*[@id="proxy-_AppOperate_Home_App_anonymousComponent"]//*[@class="iconfont icon-Create1"])[5]'
app_signature_attribute_new_fqdn_select_fqdn_button='(//*[@class="el-dropdown-menu__item"])[1]'
app_signature_attribute_new_fqdn_name_button='(//*[@class="el-form-item__content"]//input[@placeholder="Please enter the content"])[3] '
app_signature_attribute_new_fqdn_item_content_button=Edit_fqdn_items_input




Applications_create_check_send_Tcp_reset = '(//*[@id="proxy-_AppOperate_Home_App_anonymousComponent"]//span[@class="el-checkbox__inner"])[1]'
Applications_create_default_packet =  Object_Application_create_drop_input_xpath
Applications_create_check_send_ICMP_reset ='(//div[@class="denyAction"]//span[@class="el-checkbox__inner"])[2]'
Applications_create_rate_limiting = '//*[@id="Rate-limitingrate_limit"]/span'
Applications_create_rate_limiting_input = Object_Application_create_drop_input_xpath
Applications_create_Drop_button = '//*[@id="Dropdrop"]/span'
Admin_application = '//*[@id="Application_applications"]/a'
Admin_application_edit_button = '//*[@id="appEdit-_OperateBtns_ElCol_ElRow_Application_Home_App_anonymousComponent"]//p[@class="text-content text"]'
Applications_total_page = '//*[@id="pagination-_pagination_AppTable_Application_Home_App_anonymousComponent"]/span'
Applications_category_collaboration = '(//*[@id="security-content"]//div[@class="item-value el-row"])[1]'
Applications_clear_filters = '//*[@id="filter_btn-_Application_Home_App_anonymousComponent"]/span'
Applications_row = '//table/tbody/tr[{}]/td[2]/div/div'    #application主页面各行xpath路径
Applications_export_button = '//*[@class="iconfont icon-export"]'   #Applications主页面导出按钮xpath路径
Applications_export_select_box = '(//*[@class="el-dialog__body"]//span[@class="el-checkbox__input is-checked"]/span)[{}]'  #导出页面勾选框xpath路径
Applications_create_properties = '//form/div[1]/div[2]/div[{}]/label'
Applications_create_properties_subcategory = '//li[contains(text(),"{}")]'

application_search_by_name="2-_FilteredSearch_ElCol_ElRow_Application_Home_App_anonymousComponent"
application_search_by_id="1-_FilteredSearch_ElCol_ElRow_Application_Home_App_anonymousComponent"
application_search_id_xpath =  '//ul[@class="el-scrollbar__view el-select-dropdown__list"]/li/span[text()="ID"]'
Application_create_ip = '//div[@class="CreateBtn rm-search-button"]/div/button'
Application_create_ip_address = '(//ul[@class="el-dropdown-menu el-popper el-dropdown-menu--small"]/li)[1]'
