
# Main Dashboard elements area bottom===================# Main Dashboard elements area bottom===================# Main Dashboard elements area bottom===================# Main Dashboard elements area bottom===================# Main Dashboard elements area bottom===================# Main Dashboard elements area bottom===================
mainPage_main_dashboard_posXpath = "//div[@class='VDropdown']//span[@title='Main Dashboard']"  #主页Main Dashboard，用于切换dashboard
mainPage_create_button_dashboard_posXpath ="//div[@class='VDropdown']//i[@class='el-icon-plus']"  #创建自定义dashboard
mainPage_add_chart_button_posXpath ="//div[@class='CustomDashboard']//div[normalize-space(text())='Add Chart']"  #点击chart添加按钮
mainPage_save_dashboard_button_posXpath ="//i[@class='icon-save iconfont']"  #dashboard保存按钮
mainPage_cancel_button_posXpath ="//i[@class='icon-a-notsave iconfont']"  #自定义dashboard取消按钮
mainPage_cancel_OK_button_posXpath = "//div[@class='el-message-box leavePage ']//span[normalize-space(text())='OK']" #自定义dashboard取消按钮二次确认OK按钮
mainPage_cancel_Cancel_button_posXpath = "//div[@class='el-message-box leavePage ']//span[normalize-space(text())='Cancel']" #自定义dashboard取消按钮二次确认Cacncel按钮
mainPage_delete_dashboard_posXpath ="//div[@class='edit-tools']//i[@class='icon-Delete iconfont']"  #自定义dashboard删除按钮
mainPage_delete_Delete_button_posXpath = "//div[@class='el-message-box el-message-box--center']//span[normalize-space(text())='Delete']"  #自定义dashboard删除二次确认delete按钮
mainPage_delete_Cancel_button_posXpath = "//div[@class='el-message-box el-message-box--center']//span[normalize-space(text())='Cancel']" #自定义dashboard删除二次确认Cancel按钮
mainPage_edit_dashboard_button_posXpath = "//div[@class='edit-tools']//i[@class='icon-Editinpage iconfont']"  #自定义dashboard主页编辑按钮
dashboard_chart_up_button_posXpath = "//div[@class='vbox-title']//i[@class='el-icon-arrow-down el-icon--right']"#单个chart表下拉选择编辑删除，下拉按钮
dashboard_chart_up_edit_button_posXpath = "//div[@class='vbox-title']//i[@class='icon-Editinpage iconfont']" #下拉编辑按钮
dashboard_chart_up_delete_button_posXpath = "//div[@class='vbox-title']//i[@class='icon-Delete iconfont']" #下拉删除按钮
dashboard_chart_name_text_posXpath = "//div[@class='el-form-item el-form-item--small']//div[@class='width280px el-input el-input--small']//input[@class='el-input__inner']" #chart下Nmae输入框
dashboard_chart_visualization_type_posXpath = "//div[@role='radiogroup']//span[normalize-space(text())='type']" #visualization_type选择
dashboard_chart_visualization_type_text_posXpath = "//span[@class='el-radio__input is-checked']/following-sibling::span[1]"
dashboard_chart_data_source_select_up_posXpath = "(//i[@class='el-select__caret el-input__icon el-icon-arrow-up'])[2]"
dashboard_chart_data_source_select_reverse_posXpath = "//i[@class='el-select__caret el-input__icon el-icon-arrow-up is-reverse']"
dashboard_chart_data_source_select_text_posXpath = "//label[text()='Data Source']//parent::*//li[@class='el-select-dropdown__item selected']/span"
dashboard_chart_metric_add_button_posXpath = "//div[@class='Metrics']//i[@class='iconfont icon-Create1 fontsize14']"
dashboard_chart_metric_text_posXpath = "((//div[@class='Metrics']//div[@class='el-select__tags'])[{}]//span[@class='el-select__tags-text'])[{}]"   #拼接每个metric下的text文本
dashboard_chart_save_OK_button_posXpath = "//div[@class='prox-fixed-footer']//span[normalize-space(text())='OK']"
dashboard_chart_save_Cancel_button_posXpath = "//div[@class='prox-fixed-footer']//span[normalize-space(text())='Cancel']"
dashboard_chart_name_text_input_posXpath = "//div[@class='width280px el-input el-input--small']/input"
dashboard_chart_dimension_add_button_posYpath = "//div[@class='Dimension margin-top-2']//div[@class='addCondition width280px addobject addobject-long-list obj-content-null cursor']"
dashboard_chart_dimension_not_add_button_posYpath ="//div[@class='Dimension margin-top-2']//div[@class='addCondition width280px addobject addobject-long-list obj-content-null cursor notAllowed']"
dashboard_chart_dimension_text_posYpath = "(//label[text()='Dimensions']/parent::*//li[@class='el-select-dropdown__item selected']/span)[{}]"
dashboard_chart_filter_add_button_posYpath ="//div[@class='addCondition addobject addobject-long-list obj-content-null cursor margin-top0']//i[@class='iconfont icon-Create1 margin-right5']" #添加and filter条件
dashboard_chart_filter_or_button_posXpath ="//div[normalize-space(text())='Or Condition']/i"
dashboard_chart_filter_add_or_button_posYpath = "//div[@id='addOrCondition0']//i[@class='iconfont icon-Create1 margin-right5']"#添加or filter条件
dashboard_chart_filter_text_posYpath = "(//div[@class='Filters']//div[@class='el-select filter-row-select el-select--small']//li[@class='el-select-dropdown__item selected']/span)[{}]"
dashboard_chart_different_metric_error_text_posYpath ="//div[@class='Metrics']/parent::*/descendant::div[@class='el-form-item__error']" #Metric给出的错误提示
dashboard_chart_name_error_text_posYpath ="//span[normalize-space(text())='Default Name']/parent::*/parent::*//div[@class='el-form-item__error']"#空名称错误提示
dashboard_chart_dimensions_error_text_posXpath ="//label[text()='Dimensions']/parent::*//div[@class='el-form-item__error']"#dimensions错误提示
dashboard_empty_chart_save_alter_text_posXpath ="//*[@role='alert']//p" #空chart保存时错误提示
dashboard_chart_order_by_posXpath ="//label[text()='Order By']/parent::*//div[@class='el-input el-input--small el-input--suffix']"#order by选择按钮
dashboard_chart_order_by_down_posXpath = "//label[text()='Order By']/parent::*//div[@class='el-input el-input--small el-input--suffix is-focus']"
dashboard_chart_limit_posXpath = "//label[contains(text(),'Row Limit')]/parent::*//div[@class='el-input el-input--small el-input--suffix'] | //label[contains(text(),'Series Limit')]/parent::*//div[@class='el-input el-input--small el-input--suffix']"#row limit或series limit选择框
dashboard_chart_limit_down_posXpath = "//label[contains(text(),'Limit')]/parent::*//div[@class='el-input el-input--small el-input--suffix is-focus']"
dashboard_delete_metrci_posXpath = "//div[@class='Metrics']//i[@class='iconfont icon-Clear_c cursor color262626']"
dashboard_no_delete_metrci_posXpath = "//div[@class='Metrics']//i[@class='iconfont icon-Clear_c cursor color262626 notAllowed']"
dashboard_delete_dimensions_posXpath = "//div[@class='Dimension margin-top-2']//i[@class='iconfont icon-Clear_c cursor color262626']"
dashboard_delete_filter_posXpath = "//div[@class='Filters']//i[@class='iconfont icon-Clear_c cursorPointer margin-left10 floatright']"