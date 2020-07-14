# !/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Author    : Feng Zhaohui
# @Time      : 2019/2/22
# @File      : Init_UI.py
# @Funcyusa  :
# @Version   : 1.0

import ctypes
import time
from win32process import SuspendThread, ResumeThread
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QHeaderView, QFileDialog
from PyQt5.QtCore import pyqtSignal, Qt, QThread
import win32com.client
import win32api
import win32con
import os
import re
import shutil
from gui import UI_IORI_main, UI_devices_config, UI_DUT, UI_NEWDUT, UI_test_seq, UI_testplan, UI_itemparam,\
    UI_losseditor, UI_selectlossfile, UI_about, UI_Frequency_Editor, UI_report_tool, UI_CA_Frequency_Editor
import global_element
import Start_Project
import report_handle
from Equipments import Equipments
import copy
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class DevicesConfigWindow(QMainWindow, UI_devices_config.Ui_Scan_Devices):
    """
        仪器配置界面
        构建仪器配置界面的逻辑，通过此类可构建仪器配置界面实例
    """
    def __init__(self, parent=None):
        super(DevicesConfigWindow, self).__init__(parent)
        self.setupUi(self)
        self.init_example()

        # 设置为模拟对话框，阻塞上一层窗口
        self.setWindowModality(Qt.ApplicationModal)
        # 建立save按钮信号槽关系***********************************************************************************
        self.pushButton_Save.clicked.connect(self.savebtn_click)
        # 建立scan device按钮信号槽关系***************************************
        self.pushButton_scandevice.clicked.connect(self.scandevices)

    # 初始化仪器配置界面实例
    def init_example(self):
        # 初始化checkbox************************************************************
        self.checkBox_CU.setChecked(global_element.str_to_bool(global_element.devices_config_dict['xml']['CU']['CHECK']))
        self.checkBox_SA.setChecked(global_element.str_to_bool(global_element.devices_config_dict['xml']['SA']['CHECK']))
        self.checkBox_ESG.setChecked(global_element.str_to_bool(global_element.devices_config_dict['xml']['ESG']['CHECK']))
        self.checkBox_PSG.setChecked(global_element.str_to_bool(global_element.devices_config_dict['xml']['PSG']['CHECK']))
        self.checkBox_PS.setChecked(global_element.str_to_bool(global_element.devices_config_dict['xml']['PS']['CHECK']))
        self.checkBox_SU.setChecked(global_element.str_to_bool(global_element.devices_config_dict['xml']['SU']['CHECK']))
        # 初始化device_name**********************************************************
        self.comboBox_CU_Name.setCurrentText(global_element.devices_config_dict['xml']['CU']['NAME'])
        self.comboBox_SA_Name.setCurrentText(global_element.devices_config_dict['xml']['SA']['NAME'])
        self.comboBox_ESG_Name.setCurrentText(global_element.devices_config_dict['xml']['ESG']['NAME'])
        self.comboBox_PSG_Name.setCurrentText(global_element.devices_config_dict['xml']['PSG']['NAME'])
        self.comboBox_PS_Name.setCurrentText(global_element.devices_config_dict['xml']['PS']['NAME'])
        self.comboBox_SU_Name.setCurrentText(global_element.devices_config_dict['xml']['SU']['NAME'])
        # 初始化device_address_type**********************************************************
        self.comboBox_CU_AddrType.setCurrentText(global_element.devices_config_dict['xml']['CU']['ADDRESSTYPE'])
        self.comboBox_SA_AddrType.setCurrentText(global_element.devices_config_dict['xml']['SA']['ADDRESSTYPE'])
        self.comboBox_ESG_AddrType.setCurrentText(global_element.devices_config_dict['xml']['ESG']['ADDRESSTYPE'])
        self.comboBox_PSG_AddrType.setCurrentText(global_element.devices_config_dict['xml']['PSG']['ADDRESSTYPE'])
        self.comboBox_PS_AddrType.setCurrentText(global_element.devices_config_dict['xml']['PS']['ADDRESSTYPE'])
        self.comboBox_SU_AddrType.setCurrentText(global_element.devices_config_dict['xml']['SU']['ADDRESSTYPE'])
        # 初始化device_address**********************************************************
        self.lineEdit_CU_Addr.setText(global_element.devices_config_dict['xml']['CU']['ADDRESS'])
        self.lineEdit_SA_Addr.setText(global_element.devices_config_dict['xml']['SA']['ADDRESS'])
        self.lineEdit_ESG_Addr.setText(global_element.devices_config_dict['xml']['ESG']['ADDRESS'])
        self.lineEdit_PSG_Addr.setText(global_element.devices_config_dict['xml']['PSG']['ADDRESS'])
        self.lineEdit_PS_Addr.setText(global_element.devices_config_dict['xml']['PS']['ADDRESS'])
        self.lineEdit_SU_Addr.setText(global_element.devices_config_dict['xml']['SU']['ADDRESS'])

        self.tableWidget_scandevice.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 自适应水平宽度
        self.tableWidget_scandevice.horizontalHeader().setStyleSheet('QHeaderView::section{background:lightblue;}')
        self.tableWidget_scandevice.verticalHeader().setStyleSheet('QHeaderView::section{background:lightblue;}')

    def savebtn_click(self):
        """
            仪器配置界面Save按钮槽函数
            仪器配置界面Save按钮保存界面的设置到全局字典，供主函数调用
        :return:
        """
        # 将自定义配置后的数据传给字典，以供调用***********************************************************
        global_element.devices_config_dict['xml']['CU']['CHECK'] = str(self.checkBox_CU.isChecked())
        global_element.devices_config_dict['xml']['SA']['CHECK'] = str(self.checkBox_SA.isChecked())
        global_element.devices_config_dict['xml']['ESG']['CHECK'] = str(self.checkBox_ESG.isChecked())
        global_element.devices_config_dict['xml']['PSG']['CHECK'] = str(self.checkBox_PSG.isChecked())
        global_element.devices_config_dict['xml']['PS']['CHECK'] = str(self.checkBox_PS.isChecked())
        global_element.devices_config_dict['xml']['SU']['CHECK'] = str(self.checkBox_SU.isChecked())

        global_element.devices_config_dict['xml']['CU']['NAME'] = self.comboBox_CU_Name.currentText()
        global_element.devices_config_dict['xml']['SA']['NAME'] = self.comboBox_SA_Name.currentText()
        global_element.devices_config_dict['xml']['ESG']['NAME'] = self.comboBox_ESG_Name.currentText()
        global_element.devices_config_dict['xml']['PSG']['NAME'] = self.comboBox_PSG_Name.currentText()
        global_element.devices_config_dict['xml']['PS']['NAME'] = self.comboBox_PS_Name.currentText()
        global_element.devices_config_dict['xml']['SU']['NAME'] = self.comboBox_SU_Name.currentText()

        global_element.devices_config_dict['xml']['CU']['ADDRESSTYPE'] = self.comboBox_CU_AddrType.currentText()
        global_element.devices_config_dict['xml']['SA']['ADDRESSTYPE'] = self.comboBox_SA_AddrType.currentText()
        global_element.devices_config_dict['xml']['ESG']['ADDRESSTYPE'] = self.comboBox_ESG_AddrType.currentText()
        global_element.devices_config_dict['xml']['PSG']['ADDRESSTYPE'] = self.comboBox_PSG_AddrType.currentText()
        global_element.devices_config_dict['xml']['PS']['ADDRESSTYPE'] = self.comboBox_PS_AddrType.currentText()
        global_element.devices_config_dict['xml']['SU']['ADDRESSTYPE'] = self.comboBox_SU_AddrType.currentText()

        global_element.devices_config_dict['xml']['CU']['ADDRESS'] = self.lineEdit_CU_Addr.text()
        global_element.devices_config_dict['xml']['SA']['ADDRESS'] = self.lineEdit_SA_Addr.text()
        global_element.devices_config_dict['xml']['ESG']['ADDRESS'] = self.lineEdit_ESG_Addr.text()
        global_element.devices_config_dict['xml']['PSG']['ADDRESS'] = self.lineEdit_PSG_Addr.text()
        global_element.devices_config_dict['xml']['PS']['ADDRESS'] = self.lineEdit_PS_Addr.text()
        global_element.devices_config_dict['xml']['SU']['ADDRESS'] = self.lineEdit_SU_Addr.text()

        # 将用户配置好的数据存入device config.xml文件，以便下次导入记忆的配置*********************
        global_element.dict_to_xml(global_element.devices_config_dict['xml'], global_element.DEVICECONFIGXMLPATH)
        # 保存完数据后关闭界面
        self.close()

    # scan devices按钮槽函数
    def scandevices(self):
        list_idn, list_address = Equipments.scandevice()
        if len(list_idn) > 0:
            self.tableWidget_scandevice.setRowCount(len(list_idn))
            for i in range(len(list_idn)):
                item_ind = QtWidgets.QTableWidgetItem()
                item_ind.setText(','.join(list_idn[i].split(',')[:2]))
                self.tableWidget_scandevice.setItem(i, 0, item_ind)

                item_address = QtWidgets.QTableWidgetItem()
                item_address.setText(list_address[i])
                self.tableWidget_scandevice.setItem(i, 1, item_address)


class MyFirstWindow(QMainWindow, UI_IORI_main.Ui_ui_IORI):
    """
        主窗口界面
        构建主界面的逻辑，通过此类可构建主界面实例
    """
    def __init__(self, parent=None):
        super(MyFirstWindow, self).__init__(parent)
        self.setupUi(self)
        self.init_example()

        self.test_thread = test_Thread()                  # 实例化一个线程，用来处理测试过程
        self.cwd = 'Report/'                              # 获取当前程序文件位置

        self.figure = plt.figure()  # 可选参数,facecolor为背景颜色
        self.canvas = FigureCanvas(self.figure)
        #
        # self.gridLayout.addWidget(self.canvas)
        # self.setLayout(self.gridLayout)

        # 建立工具栏start工具的信号槽关系*******************************************************************************
        self.actionStart.triggered.connect(self.startbtn_click)
        # 建立工具栏Pause工具的信号槽关系*************************************************
        self.actionPause.triggered.connect(self.pausebtn_click)
        # # 建立工具栏Stop工具的信号槽关系***************************************
        self.actionStop.triggered.connect(self.stopbtn_click)
        # 建立菜单栏DUT按钮信号槽关系***********************************************************************************
        self.actionDUT_Editor.triggered.connect(self.DUT_Editor_click_event)
        # 建立工具栏exit工具的信号槽关系*******************************************************************************
        self.actionExit.triggered.connect(self.exitfunction)
        # 建立菜单栏Help按钮信号槽关系****************************************************************
        self.actionIORI_Help.triggered.connect(self.helpfunction)
        # 建立菜单栏about按钮信号槽关系****************************************************************
        self.actionAbout.triggered.connect(self.aboutme)
        # 建立菜单栏Testpaln信号槽关系****************************************************************
        self.actionTestseq.triggered.connect(self.testseqclick)
        # 建立菜单栏Report信号槽关系****************************************************************
        self.actionReport_Config.triggered.connect(self.reportmenuclick)
        # 建立菜单栏Report tool信号槽关系****************************************************************
        self.actionReport_Tool.triggered.connect(self.reporttoolclick)
        # 建立菜单栏LTE Channel Editor信号槽关系****************************************************************
        self.actionLTE_Channel_Editor.triggered.connect(self.ltechanneleditor)
        # 建立菜单栏LTE CA Channel Editor信号槽关系****************************************************************
        self.actionLTE_CA_Channel_Editor.triggered.connect(self.ltecachanneleditor)
        # 建立菜单栏User Define Loss File信号槽关系**************************************
        self.actionUser_Define_Loss_File.triggered.connect(self.losseditor)
        # 建立菜单栏Select Loss File信号槽关系**************************************
        self.actionSelect_Loss_File.triggered.connect(self.selectlossfile)
        # 建立更新report信号槽关系******************************************************************
        global_element.emitsingle.reportupdataSingle.connect(self.reportupdata)
        # 建立测试线程退出信号槽关系********************************************************
        global_element.emitsingle.thread_exitSingle.connect(self.testthread_exit)
        # 建立更新状态窗口信号槽关系********************************************************
        global_element.emitsingle.stateupdataSingle.connect(self.statewinupdata)
        # 建立更新主界面Judgement信号槽关系******************************************
        global_element.emitsingle.judgementupdataSingle.connect(self.judgementupdata)
        # 建立更新主界面start time信号槽关系******************************************
        global_element.emitsingle.starttimeupdateSingle.connect(self.starttimeupdata)
        # 建立更新主界面stop time信号槽关系******************************************
        global_element.emitsingle.stoptimeupdateSingle.connect(self.stoptimeupdata)
        # 建立更新主界面delta time信号槽关系******************************************
        global_element.emitsingle.timedeltaupdataSingle.connect(self.deltatimeupdata)
        # 建立更新主界面process rate 更新信号槽关系******************************************
        global_element.emitsingle.process_rateupdataSingle.connect(self.processrateupdata)
        # 建立更新主界面summry的信号槽关系
        global_element.emitsingle.summaryupdataSingle.connect(self.summryupdata)
        # logs界面选择模板信号槽关系*************************************************************
        self.comboBox.currentIndexChanged.connect(self.modeupdate)
        # test线程运行完成信号槽关系
        self.test_thread.finished.connect(self.testfinish)

        self.tableWidget_testseq.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 自适应水平宽度
        self.tableWidget_testseq.horizontalHeader().setStyleSheet('QHeaderView::section{background:lightblue;}')
        self.tableWidget_testseq.verticalHeader().setStyleSheet('QHeaderView::section{background:lightblue;}')
        # self.tableWidget_logs.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget_logs.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)   # 自适应水平宽度
        self.tableWidget_logs.horizontalHeader().setStyleSheet('QHeaderView::section{background:lightblue;}')
        self.tableWidget_logs.verticalHeader().setStyleSheet('QHeaderView::section{background:lightblue;}')

    # 初始主界面实例
    def init_example(self):
        self.setWindowState(Qt.WindowMaximized)                     # 初始化为最大化窗口
        # 从Device Config.xml文件中导入初始化配置数据到字典********************************
        global_element.devices_config_dict = global_element.xml_to_dict(global_element.DEVICECONFIGXMLPATH)
        # 从DUT Config文件夹遍历所有DUT配置，保存到列表************************************
        global_element.dut_config_list = global_element.ergodic_dir(global_element.DUTCONFIGXMLPATH)
        # DUT列表内容格式整理*************************************************************
        global_element.dut_config_items_list = ['      ' + x for x in global_element.dut_config_list]
        # 测试序列初始化为空************************************************************
        global_element.Testsequence_dict['seq']['items'] = []
        # 测试序列初始化为空************************************************************
        global_element.Testseq_list = []
        # 初始化logs表格
        list_labls = ['Test Type', 'Test Case', 'Test Items', 'Result', 'Low Limit', 'High Limit', 'Judgement',
                      'Band', 'Channel', 'DL_Freq(MHz)', 'UL_Freq(MHz)', 'PCL', 'Modulation', 'Volt.(V)', 'Temp.(℃)',
                      'Remark', 'Time']
        self.tableWidget_logs.setHorizontalHeaderLabels(list_labls)

    # 主界面 Start按钮槽函数定义************************************************************************
    def startbtn_click(self):
        # 点击start按钮后更新界面控件状态
        self.statusBar().showMessage('Testing in progress……')
        self.actionExit.setEnabled(False)
        self.actionStart.setEnabled(False)
        self.actionPause.setEnabled(True)
        self.actionStop.setEnabled(True)
        self.actionTestseq.setEnabled(False)
        self.actionDUT_Editor.setEnabled(False)
        self.actionReport_Config.setEnabled(False)
        self.actionReport_Tool.setEnabled(False)
        self.actionSelect_Loss_File.setEnabled(False)
        self.actionUser_Define_Loss_File.setEnabled(False)
        self.actionDevices_Config.setEnabled(False)
        self.tableWidget_logs.setRowCount(0)
        self.textBrowser_status.clear()
        row_count = self.tableWidget_testseq.rowCount()
        for i in range(row_count):
            for j in range(1, 5):
                item = QtWidgets.QTableWidgetItem()
                item.setText('')
                self.tableWidget_testseq.setItem(i, j, item)

        rr = self.gridLayout.indexOf(self.canvas)
        if rr != -1:
            plt.cla()
            lables = ['Passed: 0', 'Failed: 0', 'Inconlusive: 0']
            explode = (0.1, 0, 0)
            colors = ['g', 'r', 'y']

            plt.pie([0, 0, 0], explode=explode, labels=lables, colors=colors, autopct='%1.1f%%',
                    shadow=False, startangle=150)
            plt.title('Summary')
            plt.axis('equal')
            self.canvas.draw()

        # 开启另一个线程处理测试过程，以防界面在测试过程中卡死
        self.test_thread.start()

    # 主界面更新summry槽函数
    def summryupdata(self, content_list):

        self.gridLayout.addWidget(self.canvas)
        self.setLayout(self.gridLayout)
        datalist = content_list
        plt.cla()
        lables = ['Passed: ' + str(datalist[0]), 'Failed: ' + str(datalist[1]), 'Inconclusive: ' + str(datalist[2])]
        explode = (0.1, 0, 0)
        colors = ['g', 'r', 'y']

        patches, l_text, p_text = plt.pie(datalist, explode=explode, labels=lables, colors=colors, autopct='%1.1f%%',
                shadow=False, startangle=150)
        plt.title('Summary')
        # for t in l_text:
        #     t.set_size(10)
        # for t in p_text:
        #     t.set_size(20)
        plt.axis('equal')
        plt.legend(loc='upper left', bbox_to_anchor=(-0.1, 1))
        self.canvas.draw()

    # 主界面Pause按钮槽函数
    def pausebtn_click(self):
        # global_element.IsPause = True
        # self.actionPause.setEnabled(False)
        # self.actionStop.setEnabled(False)
        # user_choose = win32api.MessageBox(0, '测试已暂停，按OK继续!', '提醒', win32con.MB_OK)
        # if user_choose == 1:
        #     global_element.IsPause = False
        #     self.actionPause.setEnabled(True)
        #     self.actionStop.setEnabled(True)
        if self.test_thread.handle != -1:
            self.actionPause.setEnabled(False)
            self.actionStop.setEnabled(False)
            ret = SuspendThread(self.test_thread.handle)
            user_choose = win32api.MessageBox(0, 'Test has been suspended, press OK to continue!', 'Tip', win32con.MB_OK)
            if user_choose == 1:
                self.actionPause.setEnabled(True)
                self.actionStop.setEnabled(True)
                ret = ResumeThread(self.test_thread.handle)

    # 主界面Stop按钮槽函数
    def stopbtn_click(self):
        user_choose = win32api.MessageBox(0, 'Confirm to stop testing?', 'Tip', win32con.MB_OKCANCEL)
        if user_choose == 1:
            global_element.IsStop = True                                 # 此参数用于report tool方法是否还能运行
            time.sleep(3)                                                # 等待3秒，以防正在处理的report文件损坏
            self.testthread_exit('User termination test！')
            # global_element.IsStop = True

    # 主界面 Device Config菜单槽函数定义**************************************************************
    def Devices_Config_click_event(self):
        self.deviceconfigwin_example = DevicesConfigWindow()
        self.deviceconfigwin_example.show()

    # 主界面 DUT菜单槽函数定义**************************************************************
    def DUT_Editor_click_event(self):
        self.duteditorwin_example = DUTConfigWindow()
        self.duteditorwin_example.dutnameSignal.connect(self.getdutnameSignal)
        self.duteditorwin_example.dutwincloseSignal.connect(self.dutwinclosepro)
        self.duteditorwin_example.show()

    # 主界面 Testplan菜单槽函数定义**************************************************************
    def testseqclick(self):
        self.testseqwin_exampple = TestseqWindow()
        self.testseqwin_exampple.okbtnclickSingle.connect(self.receiveoksingle)
        self.testseqwin_exampple.show()

    # 当收到test seq界面ok按钮点击的信号后，更新主界面的内容
    def receiveoksingle(self, content):
        if content > 0:
            self.tableWidget_testseq.setRowCount(content)
            for i in range(len(global_element.Testsequence_dict['seq']['items'])):
                self.tableWidget_testseq.setRowHeight(i, 30)
                item = QtWidgets.QTableWidgetItem()
                item.setText(global_element.Testsequence_dict['seq']['items'][i]['@name'])
                self.tableWidget_testseq.setItem(i, 0, item)
        else:
            self.tableWidget_testseq.setRowCount(0)

    # 收到DUT窗口save按钮传回的信号后修改主窗口DUT的名称
    def getdutnameSignal(self, connect):
        self.label_dut.setText(connect)

    # 收到DUT窗口cancel按钮传回的信号后清空主窗口DUT的名称
    def dutwinclosepro(self, content):
        if content == '1':
            self.label_dut.setText('')

    # 主界面 Help菜单槽函数定义**************************************************************
    def helpfunction(self):
        appword = win32com.client.Dispatch('Word.Application')
        appword.visible = 1
        path = 'd:/IORI/Help/manual_of_operation.docx'
        docx = appword.Documents.Open(path)

    # 主界面工具栏exit槽函数定义**************************************************************
    def exitfunction(self):
        result = win32api.MessageBox(0, 'Are you sure want to quit?', 'Tip', win32con.MB_OKCANCEL)
        if result == 1:
            os._exit(0)
            self.close()

    def closeEvent(self, event):
        '''
            以主窗口的函数closeEvent进行重构
            退出软件时结束所有进程
            :param event:
            :return:
        '''
        reply = QtWidgets.QMessageBox.question(self,
                                               'Tip',
                                               'Are you sure want to quit?',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
            os._exit(0)
        else:
            event.ignore()

    # 定义菜单栏report工具的槽函数
    def reportmenuclick(self):
        fileName_choose, filetype = QFileDialog.getSaveFileName(self,
                                                                'Report Preservation',
                                                                self.cwd,
                                                                'Excel Files (*.xlsx);;All Files (*)')

        if fileName_choose != '':
            zhmodel = re.compile(u'[\u4e00-\u9fa5]')
            match = zhmodel.search(fileName_choose)
            if match:
                win32api.MessageBox(0, 'The report path can not contain Chinese!')
                global_element.reportpath = ''
            else:
                global_element.reportpath = fileName_choose

    # 定义报告更新槽函数
    def reportupdata(self, content):
        data_list = content
        current_row_count = self.tableWidget_logs.rowCount()
        self.tableWidget_logs.setRowCount(current_row_count + 1)
        self.tableWidget_logs.setRowHeight(current_row_count, 10)
        for i in range(len(data_list)):
            item = QtWidgets.QTableWidgetItem()
            item.setText(data_list[i])
            if i == 6:
                if data_list[i] == 'Passed':
                    item.setForeground(Qt.green)
                elif data_list[i] == 'Failed':
                    item.setForeground(Qt.red)
                else:
                    item.setForeground(Qt.black)
            self.tableWidget_logs.setItem(current_row_count, i, item)

    # 定义LTE Channel Editor槽函数
    def ltechanneleditor(self):
        self.ltechannelditor_example = LteChannelEditorWin()
        self.ltechannelditor_example.show()

    # 定义LTE Channel Editor槽函数
    def ltecachanneleditor(self):
        self.ltecachannelditor_example = LtecaChannelEditorWin()
        self.ltecachannelditor_example.show()

    # 定义更换logs模板的槽函数
    def modeupdate(self):
        list_GSM_mode = ['Test Type', 'Test Case', 'Test Items', 'Result', 'Low Limit', 'High Limit', 'Judgement',
                      'Band', 'Channel', 'DL_Freq(MHz)', 'UL_Freq(MHz)', 'PCL', 'Modulation', 'Volt.(V)', 'Temp.(℃)',
                      'Remark', 'Time']
        list_WCDMA_mode = ['Test Type', 'Test Case', 'Test Items', 'Result', 'Low Limit', 'High Limit', 'Judgement',
                      'Band', 'Channel', 'DL_Freq(MHz)', 'UL_Freq(MHz)', 'Modulation', 'Volt.(V)', 'Temp.(℃)',
                      'Remark', 'Time']
        list_LTE_mode = ['Test Type', 'Test Case', 'Test Items', 'Result', 'Low Limit', 'High Limit', 'Judgement',
                      'Band', 'BandWidth', 'Channel', 'DL_Freq(MHz)', 'UL_Freq(MHz)', 'RB', 'Modulation', 'Volt.(V)',
                         'Temp.(℃)', 'Remark', 'Time']
        list_BT2_mode = ['Test Type', 'Test Case', 'Test Items', 'Result', 'Low Limit', 'High Limit', 'Judgement',
                         'Packet Type', 'Channel', 'Freq(MHz)', 'Volt.(V)', 'Temp.(℃)', 'Remark', 'Time']
        list_WLAN_mode = ['Test Type', 'Test Case', 'Test Items', 'Result', 'Low Limit', 'High Limit',
                             'Judgement',
                             'DataRate', 'BW', 'Channel', 'Freq(MHz)',
                             'Volt.(V)',
                             'Temp.(℃)', 'Remark', 'Time']
        current_text = self.comboBox.currentText()
        if current_text == 'GSM':
            self.tableWidget_logs.setHorizontalHeaderLabels([''] * 18)
            self.tableWidget_logs.setHorizontalHeaderLabels(list_GSM_mode)
        elif current_text == 'WCDMA':
            self.tableWidget_logs.setHorizontalHeaderLabels([''] * 18)
            self.tableWidget_logs.setHorizontalHeaderLabels(list_WCDMA_mode)
        elif current_text == 'LTE':
            self.tableWidget_logs.setHorizontalHeaderLabels([''] * 18)
            self.tableWidget_logs.setHorizontalHeaderLabels(list_LTE_mode)
        elif current_text == 'BT2':
            self.tableWidget_logs.setHorizontalHeaderLabels([''] * 18)
            self.tableWidget_logs.setHorizontalHeaderLabels(list_BT2_mode)
        elif current_text == 'WLAN':
            self.tableWidget_logs.setHorizontalHeaderLabels([''] * 18)
            self.tableWidget_logs.setHorizontalHeaderLabels(list_WLAN_mode)

    # 定义User Define Loss File按钮的槽函数
    def losseditor(self):
        self.lossfilewin_example = losseditorWindow()
        self.lossfilewin_example.show()

    # 定义Select Loss File按钮的槽函数
    def selectlossfile(self):
        self.selectlossfile_example = lossfileselectWindow()
        self.selectlossfile_example.show()

    # 定义about me按钮的槽函数
    def aboutme(self):
        self.aboutmewin_example = aboutWindow()
        self.aboutmewin_example.show()

    # 定义接收到test线程完成信号后的槽函数
    def testfinish(self):
        self.statusBar().showMessage('The test is completed!')

        self.actionExit.setEnabled(True)
        self.actionStart.setEnabled(True)
        self.actionPause.setEnabled(False)
        self.actionStop.setEnabled(False)
        self.actionTestseq.setEnabled(True)
        self.actionDUT_Editor.setEnabled(True)
        self.actionReport_Config.setEnabled(True)
        self.actionReport_Tool.setEnabled(True)
        self.actionSelect_Loss_File.setEnabled(True)
        self.actionUser_Define_Loss_File.setEnabled(True)
        self.actionDevices_Config.setEnabled(True)

        # self.test_thread.deleteLater()

        win32api.MessageBox(0, 'Test Finished!', 'Tip', win32con.MB_OK)

    # 定义接收到test线程退出信号后的槽函数
    def testthread_exit(self, content):
        if global_element.current_index_seq != -1:
            item = QtWidgets.QTableWidgetItem()
            item.setText('Abort')
            item.setForeground(Qt.darkYellow)
            self.tableWidget_testseq.setItem(global_element.current_index_seq, 1, item)
        time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.textBrowser_status.append(time_now + ':        ' + content)
        self.textBrowser_status.append(time_now + ':        ' + 'Tip:    Program abnormal exit!')
        self.test_thread.terminate()
        # self.test_thread.quit()
        self.test_thread.wait()

    # 定义接收到更新状态窗口信号后的槽函数
    def statewinupdata(self, content):
        time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.textBrowser_status.append(time_now + ':        ' + content)

    # 定义收到更新judgement的信号后的槽函数
    def judgementupdata(self, line_index, content):
        item = QtWidgets.QTableWidgetItem()
        item.setText(content)
        if content == 'Failed':
            item.setForeground(Qt.red)
        elif content == 'Passed':
            item.setForeground(Qt.green)
        elif content == 'Testing':
            item.setForeground(Qt.magenta)
        else:
            item.setForeground(Qt.black)
        self.tableWidget_testseq.setItem(line_index, 1, item)

    # 定义收到更新start time的信号后的槽函数
    def starttimeupdata(self, line_index, content):
        item = QtWidgets.QTableWidgetItem()
        item.setText(content)
        self.tableWidget_testseq.setItem(line_index, 2, item)

    # 定义收到更新stop time的信号后的槽函数
    def stoptimeupdata(self, line_index, content):
        item = QtWidgets.QTableWidgetItem()
        item.setText(content)
        self.tableWidget_testseq.setItem(line_index, 3, item)

    # 定义收到更新delta time的信号后的槽函数
    def deltatimeupdata(self, line_index, content):
        item = QtWidgets.QTableWidgetItem()
        item.setText(content)
        self.tableWidget_testseq.setItem(line_index, 4, item)

    # 定义收到更新测试进度的信号后的槽函数
    def processrateupdata(self, content):
        self.progressBar.setValue(float(content))

    # 定义report tool菜单点击信号的槽函数
    def reporttoolclick(self):
        self.reporttoolwin_example = ReportToolWindow()
        self.reporttoolwin_example.show()


class DUTConfigWindow(QMainWindow, UI_DUT.Ui_Window_DUT):
    """
        DUT配置界面
        构建DUT配置界面的逻辑，通过此类可构建DUT配置界面实例
    """
    dutnameSignal = pyqtSignal(str)
    dutwincloseSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(DUTConfigWindow, self).__init__(parent)
        self.setupUi(self)
        self.init_example()

        # 定义信号槽关系
        self.pushButton_NewDUT.clicked.connect(self.new_dutbtn_clicked)
        self.pushButton_RemoveDUT.clicked.connect(self.removedutbtn_clicked)
        self.pushButton_Saveas.clicked.connect(self.saveasbtn_clicked)
        self.pushButton_ActDUT.clicked.connect(self.actdutbtn_clicked)
        self.pushButton_Save.clicked.connect(self.savebtnclick)
        self.listWidget_DUT.currentRowChanged.connect(self.loadcurrentpara)
        self.pushButton_updata.clicked.connect(self.updataparmtoxml)
        self.pushButton_Cancel.clicked.connect(self.cancelbtnclick)

        # 设置为模拟对话框，阻塞上一层窗口
        self.setWindowModality(Qt.ApplicationModal)

    # 初始化DUT配置界面实例
    def init_example(self):
        self.listWidget_DUT.addItems(global_element.dut_config_items_list)
        global_element.active_dut_dict = {}

    # New dut界面槽函数
    def buildnewdut(self, content):
        if content != 'None':  # 确认返回了可用的DUT NAME
            # 判断DUT是否已经存在
            nameisexist = False
            for i in global_element.dut_config_list:
                if i == content:
                    nameisexist = True
                    break
            if nameisexist:
                win32api.MessageBox(0, 'DUT already exists!', 'Tip', win32con.MB_OK)
            else:
                self.listWidget_DUT.addItem('      ' + content)  # 符合条件的DUT Name加入界面列表
                global_element.dut_config_list.append(content)  # 符合条件的DUT Name加入DUT名称列表
                # 符合条件的DUT Name加入处理后的DUT名称列表
                global_element.dut_config_items_list.append('      ' + content)
                # 创建NEW DUT的xml文件
                shutil.copy(global_element.DEFUALTCONFIGXMLPATH + 'New DUT Config.xml', global_element.DUTCONFIGXMLPATH
                            + content + '.xml')

    # New dut Save as界面槽函数
    def saveasnewdut(self, content):
        # 判断DUT name是否为空
        if not self.listWidget_DUT.currentItem():
            win32api.MessageBox(0, 'Please select an existing DUT!', 'Tip', win32con.MB_OK)
        else:
            # 判断DUT是否已经存在
            nameisexist = False
            for i in global_element.dut_config_list:
                if i == content:
                    nameisexist = True
                    break
            if nameisexist:
                win32api.MessageBox(0, 'DUT already exists!', 'Tip', win32con.MB_OK)
            else:
                currentitemRow = self.listWidget_DUT.currentRow()
                currentitemtext = self.listWidget_DUT.item(currentitemRow).text()

                # 提取选中item内容中空格右边的部分，用于复制xml配置文件
                if '√' in currentitemtext:
                    currentitemtext = currentitemtext[4:]
                else:
                    currentitemtext = currentitemtext[6:]

                self.listWidget_DUT.addItem('      ' + content)  # 符合条件的DUT Name加入界面列表
                global_element.dut_config_list.append(content)  # 符合条件的DUT Name加入字典列表
                # 符合条件的DUT Name处理后加入列表
                global_element.dut_config_items_list.append('      ' + content)
                # 复制已存在的DUT的xml文件为New DUT的xml文件
                shutil.copy(global_element.DUTCONFIGXMLPATH + currentitemtext + '.xml', global_element.DUTCONFIGXMLPATH
                            + content + '.xml')

    # New DUT按钮信号槽函数
    def new_dutbtn_clicked(self):
        self.newdutwin = NEWDUTWindow()
        self.newdutwin.newdutnameSignal.connect(self.buildnewdut)
        self.newdutwin.show()

    # Remove DUT按钮信号槽函数
    def removedutbtn_clicked(self):
        # 判断是否有选中的item,如果有，移除（包含配置文件）
        if self.listWidget_DUT.currentItem():
            currenrow = self.listWidget_DUT.currentRow()
            currenitemtext = self.listWidget_DUT.item(currenrow).text()
            # 从处理后的DUT Name列表中删除所选DUT
            global_element.dut_config_items_list.pop(global_element.dut_config_items_list.index(currenitemtext))
            # 提取选中item内容中空格右边的部分
            if '√' in currenitemtext:
                currenitemtext = currenitemtext[4:]
            else:
                currenitemtext = currenitemtext[6:]

            self.listWidget_DUT.takeItem(currenrow)                                       # 从界面列表删除DUT
            global_element.dut_config_list.pop(global_element.dut_config_list.index(currenitemtext))  # 从DUT列表中删除DUT
            # 删除DUT对应的xml文件
            if os.path.exists(global_element.DUTCONFIGXMLPATH + currenitemtext + '.xml'):
                os.remove(global_element.DUTCONFIGXMLPATH + currenitemtext + '.xml')

    # Save as按钮信号槽函数
    def saveasbtn_clicked(self):
        self.newdutwin = NEWDUTWindow()
        self.newdutwin.newdutnameSignal.connect(self.saveasnewdut)
        self.newdutwin.show()

    # cancel按钮信号槽函数
    def cancelbtnclick(self):
        self.dutwincloseSignal.emit('1')  # 关闭DUT窗口时给主窗口发一个‘1’的信号
        self.close()

    # Active DUT按钮信号槽函数
    def actdutbtn_clicked(self):
        if self.listWidget_DUT.currentItem():
            currentitemRow = self.listWidget_DUT.currentRow()
            currentitemtext = self.listWidget_DUT.item(currentitemRow).text()
            rowcount = self.listWidget_DUT.count()
            if '√' not in currentitemtext:
                # 替换列表控件中的内容
                self.listWidget_DUT.item(currentitemRow).setText('√' + currentitemtext[3:])
                # 替换处理名称后的列表内容
                currentitemtext_index = global_element.dut_config_items_list.index(currentitemtext)
                global_element.dut_config_items_list[currentitemtext_index] = '√' + currentitemtext[3:]

                # 去掉之前有激活的DUT标记
                for i in range(rowcount):
                    if '√' in self.listWidget_DUT.item(i).text() and i != currentitemRow:
                        itemtext = self.listWidget_DUT.item(i).text()
                        itemtext_index = global_element.dut_config_items_list.index(itemtext)
                        global_element.dut_config_items_list[itemtext_index] = '   ' + itemtext[1:]
                        self.listWidget_DUT.item(i).setText('   ' + itemtext[1:])
        else:
            win32api.MessageBox(0, 'Please select a DUT that you want to activate first!', 'Tip', win32con.MB_OK)

    def savebtnclick(self):
        act_dut_str = ''
        for i in global_element.dut_config_items_list:
            if '√' in i:
                act_dut_str = i[4:]
                break
        if act_dut_str == '':
            win32api.MessageBox(0, 'Please activate a DUT!', 'Tip', win32con.MB_OK)
        else:
            self.dutnameSignal.emit(act_dut_str)     # Save按钮发射一个信号（激活DUT的名称）给主界面
            global_element.active_dut_name = act_dut_str
            global_element.active_dut_dict = global_element.xml_to_dict(global_element.DUTCONFIGXMLPATH +
                                                                        act_dut_str + '.xml')
            self.close()

    def loadcurrentpara(self):
        # 提取选中的item中的DUT name，用于选择对应的xml配置文件导入数据
        current_row = self.listWidget_DUT.currentRow()
        current_text = self.listWidget_DUT.item(current_row).text()
        if '√' in current_text:
            current_text = current_text[4:]
        else:
            current_text = current_text[6:]

        # 将对应xml配置文件数据转为字典格式
        global_element.current_dut_dict.clear()
        global_element.current_dut_dict = global_element.xml_to_dict(global_element.DUTCONFIGXMLPATH +
                                                                     current_text + '.xml')

        # 将字典内内容更新到右侧控件，以便用户查看和编辑
        self.lineEdit_DUTfacturer.setText(global_element.current_dut_dict['xml']['DUTCONFIG']['DUTMANUFACTURER'])
        self.lineEdit_DUTSN.setText(global_element.current_dut_dict['xml']['DUTCONFIG']['DUTSN'])
        self.lineEdit_HWrev.setText(global_element.current_dut_dict['xml']['DUTCONFIG']['DUTHWREV'])
        self.lineEdit_SWrev.setText(global_element.current_dut_dict['xml']['DUTCONFIG']['DUTSWREV'])
        self.lineEdit_DUTIMEI.setText(global_element.current_dut_dict['xml']['DUTCONFIG']['DUTIMEI'])
        self.lineEdit_MaxRegTime.setText(global_element.current_dut_dict['xml']['DUTCONFIG']['MAXREGTIME'])
        if global_element.current_dut_dict['xml']['DUTCONFIG']['AUTOMODE'] == '1':
            self.radioButton_ManunalMode.setChecked(True)
        elif global_element.current_dut_dict['xml']['DUTCONFIG']['AUTOMODE'] == '2':
            self.radioButton_PowerMode.setChecked(True)
        elif global_element.current_dut_dict['xml']['DUTCONFIG']['AUTOMODE'] == '3':
            self.radioButton_ATCMD.setChecked(True)
        elif global_element.current_dut_dict['xml']['DUTCONFIG']['AUTOMODE'] == '4':
            self.radioButton_NOSIGN.setChecked(True)
        elif global_element.current_dut_dict['xml']['DUTCONFIG']['AUTOMODE'] == '5':
            self.radioButton_SIGN.setChecked(True)
        elif global_element.current_dut_dict['xml']['DUTCONFIG']['AUTOMODE'] == '0':
            self.radioButton_ManunalMode.setChecked(False)
            self.radioButton_PowerMode.setChecked(False)
            self.radioButton_ATCMD.setChecked(False)
            self.radioButton_NOSIGN.setChecked(False)
            self.radioButton_SIGN.setChecked(False)
        self.lineEdit_COMPort.setText(global_element.current_dut_dict['xml']['DUTCONFIG']['COMPORT'])
        self.lineEdit_COMPort_QRCT.setText(global_element.current_dut_dict['xml']['DUTCONFIG']['COMPORTQRCT'])
        self.comboBox_Nosigntool.setCurrentText(global_element.current_dut_dict['xml']['DUTCONFIG']['NSSW'])
        self.lineEdit_HighVolt.setText(global_element.current_dut_dict['xml']['DUTCONFIG']['HV'])
        self.lineEdit_NorVolt.setText(global_element.current_dut_dict['xml']['DUTCONFIG']['NV'])
        self.lineEdit_LowVolt.setText(global_element.current_dut_dict['xml']['DUTCONFIG']['LV'])
        self.lineEdit_MaxCurrent.setText(global_element.current_dut_dict['xml']['DUTCONFIG']['MAXC'])
        self.lineEdit_HighTemp.setText(global_element.current_dut_dict['xml']['DUTCONFIG']['HT'])
        self.lineEdit_NorTemp.setText(global_element.current_dut_dict['xml']['DUTCONFIG']['NT'])
        self.lineEdit_LowTemp.setText(global_element.current_dut_dict['xml']['DUTCONFIG']['LT'])

    # updata dut config按钮槽函数定义
    def updataparmtoxml(self):
        # 将控件的内容传给字典
        global_element.current_dut_dict['xml']['DUTCONFIG']['DUTMANUFACTURER'] = self.lineEdit_DUTfacturer.text()
        global_element.current_dut_dict['xml']['DUTCONFIG']['DUTSN'] = self.lineEdit_DUTSN.text()
        global_element.current_dut_dict['xml']['DUTCONFIG']['DUTHWREV'] = self.lineEdit_HWrev.text()
        global_element.current_dut_dict['xml']['DUTCONFIG']['DUTSWREV'] = self.lineEdit_SWrev.text()
        global_element.current_dut_dict['xml']['DUTCONFIG']['DUTIMEI'] = self.lineEdit_DUTIMEI.text()
        global_element.current_dut_dict['xml']['DUTCONFIG']['MAXREGTIME'] = self.lineEdit_MaxRegTime.text()
        index_radiobtn_ischecked = '0'
        if self.radioButton_ManunalMode.isChecked():
            index_radiobtn_ischecked = '1'
        elif self.radioButton_PowerMode.isChecked():
            index_radiobtn_ischecked = '2'
        elif self.radioButton_ATCMD.isChecked():
            index_radiobtn_ischecked = '3'
        elif self.radioButton_NOSIGN.isChecked():
            index_radiobtn_ischecked = '4'
        elif self.radioButton_SIGN.isChecked():
            index_radiobtn_ischecked = '5'
        global_element.current_dut_dict['xml']['DUTCONFIG']['AUTOMODE'] = index_radiobtn_ischecked
        global_element.current_dut_dict['xml']['DUTCONFIG']['COMPORT'] = self.lineEdit_COMPort.text()
        global_element.current_dut_dict['xml']['DUTCONFIG']['COMPORTQRCT'] = self.lineEdit_COMPort_QRCT.text()
        global_element.current_dut_dict['xml']['DUTCONFIG']['NSSW'] = self.comboBox_Nosigntool.currentText()
        global_element.current_dut_dict['xml']['DUTCONFIG']['HV'] = self.lineEdit_HighVolt.text()
        global_element.current_dut_dict['xml']['DUTCONFIG']['NV'] = self.lineEdit_NorVolt.text()
        global_element.current_dut_dict['xml']['DUTCONFIG']['LV'] = self.lineEdit_LowVolt.text()
        global_element.current_dut_dict['xml']['DUTCONFIG']['MAXC'] = self.lineEdit_MaxCurrent.text()
        global_element.current_dut_dict['xml']['DUTCONFIG']['HT'] = self.lineEdit_HighTemp.text()
        global_element.current_dut_dict['xml']['DUTCONFIG']['NT'] = self.lineEdit_NorTemp.text()
        global_element.current_dut_dict['xml']['DUTCONFIG']['LT'] = self.lineEdit_LowTemp.text()

        # 将字典的内容传给xml配置文件
        current_row = self.listWidget_DUT.currentRow()
        current_text = self.listWidget_DUT.item(current_row).text()
        if '√' in current_text:
            current_text = current_text[4:]
        else:
            current_text = current_text[6:]
        global_element.dict_to_xml(global_element.current_dut_dict['xml'], global_element.DUTCONFIGXMLPATH +
                                   current_text + '.xml')


class NEWDUTWindow(QMainWindow, UI_NEWDUT.Ui_NewDUT):
    """
        NEW DUT界面
    """
    newdutnameSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(NEWDUTWindow, self).__init__(parent)
        self.setupUi(self)

        # 设置为模拟对话框，阻塞上一层窗口
        self.setWindowModality(Qt.ApplicationModal)

        # OK按钮信号槽关系
        self.pushButton_ok.clicked.connect(self.okbtnclick)
        self.pushButton_cancel.clicked.connect(self.cancelbtnclick)

    def okbtnclick(self):
        if self.lineEdit_dutname.text() =='':
            win32api.MessageBox(0, 'Please enter a NEW DUT name!')
        else:
            sendcontent = self.lineEdit_dutname.text()
            self.newdutnameSignal.emit(sendcontent)
            self.close()

    def cancelbtnclick(self):
        self.close()


class TestseqWindow(QMainWindow, UI_test_seq.Ui_Window_testseq):
    """
        Test sequence界面
    """
    okbtnclickSingle = pyqtSignal(int)

    def __init__(self, parent=None):
        super(TestseqWindow, self).__init__(parent)
        self.setupUi(self)
        self.initexample()

        self.cwd = 'Plan/'   # 获取当前程序文件位置

        # 设置为模拟对话框，阻塞上一层窗口
        self.setWindowModality(Qt.ApplicationModal)

        # 界面控件的信号槽关系
        self.pushButton_addcase.clicked.connect(self.addcasebtnclick)
        self.actionSave_Sequence.triggered.connect(self.slot_action_saveseq)
        self.pushButton_editcase.clicked.connect(self.editcasebtnclick)
        self.listWidget_testseq.itemDoubleClicked.connect(self.editcasebtnclick)
        self.pushButton_copy.clicked.connect(self.copybtnclick)
        self.pushButton_removecase.clicked.connect(self.removebtnclick)
        self.pushButton_up.clicked.connect(self.upbtnclick)
        self.pushButton_down.clicked.connect(self.downbtnclick)
        self.pushButton_enableall.clicked.connect(self.enableallbtnclick)
        self.pushButton_disableall.clicked.connect(self.disableallbtnclick)
        self.listWidget_testseq.itemChanged.connect(self.itemchanged)
        self.pushButton_cancel.clicked.connect(self.cancelbtnclick)
        self.actionLoadSequence.triggered.connect(self.loadseq)
        self.pushButton_ok.clicked.connect(self.okbtnclick)
        self.actionAdd_Sequence.triggered.connect(self.addseq)

    # 初始化窗口实例
    def initexample(self):
        self.listWidget_testseq.clear()
        if len(global_element.Testsequence_dict['seq']['items']) > 0:
            global_element.Testseq_list = global_element.Testsequence_dict['seq']['items']
            global_element.Testseq_list = list(global_element.Testseq_list)
            for i in global_element.Testsequence_dict['seq']['items']:
                item = QtWidgets.QListWidgetItem()
                if i['@enable'] == 'yes':
                    item.setCheckState(Qt.Checked)
                else:
                    item.setCheckState(not Qt.Checked)
                item.setText(i['@name'])
                self.listWidget_testseq.addItem(item)

    # 定义此窗口 add case按钮的槽函数
    def addcasebtnclick(self):
        self.testplanwin_example = TestplanWindow('newplan')                    # 以新建plan的方式初始化弹出窗口
        self.testplanwin_example.okbtn_Signal.connect(self.receivesignalprocess_fornewtestplan)
        self.testplanwin_example.show()

    # 收到new test plan处理函数
    def receivesignalprocess_fornewtestplan(self, content, temptime):
        # 定义一个空字典用来存放用户新建的testplan
        test_seq_item = {}
        test_seq_item['@name'] = content
        test_seq_item['@enable'] = 'yes'
        test_seq_item['@index'] = ''
        test_seq_item['@condition'] = content.split(' ')[1]
        test_seq_item['@tempstabtime'] = temptime
        test_seq_item['item'] = global_element.Testplan_list

        # 逻辑上在字典更新用户新增的testplan
        global_element.Testseq_list.append(test_seq_item)
        for i in range(len(global_element.Testseq_list)):
            global_element.Testseq_list[i]['@index'] = i

        # 界面上更新用户新增的testplan
        item = QtWidgets.QListWidgetItem()
        item.setCheckState(Qt.Checked)
        item.setText(content)
        self.listWidget_testseq.addItem(item)

    # 保存sequence的槽函数
    def slot_action_saveseq(self):
        if len(global_element.Testseq_list) == 0:
            win32api.MessageBox(0, 'No test sequence can be saved!', 'Tip', win32con.MB_OK)
        if len(global_element.Testseq_list) > 0:
            fileName_choose, filetype = QFileDialog.getSaveFileName(self,
                                                                     'Save test sequences',
                                                                     self.cwd,
                                                                     'IORI TestSeq Files (*.IORIseq);;All Files (*)')

            if fileName_choose != '':
                global_element.dict_to_xmlstr({'seq': {'items': global_element.Testseq_list}}, fileName_choose)

    # 载入sequence的槽函数
    def loadseq(self):
        fileName_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                 'Selecting Test Sequences',
                                                                 self.cwd,
                                                                 'IORI TestSeq Files (*.IORIseq);;All Files (*)')
        if fileName_choose != '':
            global_element.Testseq_list = []
            xml_dict = global_element.xml_to_dict(fileName_choose)
            if isinstance(xml_dict['seq']['items'], dict):
                global_element.Testseq_list.append(xml_dict['seq']['items'])
            else:
                global_element.Testseq_list = xml_dict['seq']['items']
            self.listWidget_testseq.clear()
            for i in range(len(global_element.Testseq_list)):
                item = QtWidgets.QListWidgetItem()
                current_text = global_element.Testseq_list[i]['@name']
                if global_element.Testseq_list[i]['@enable'] == 'yes':
                    current_checkstate = Qt.Checked
                else:
                    current_checkstate = not Qt.Checked
                item.setCheckState(current_checkstate)
                item.setText(current_text)
                self.listWidget_testseq.addItem(item)

    # 点击editcase按钮的槽函数
    def editcasebtnclick(self):
        if self.listWidget_testseq.currentItem():
            current_row = self.listWidget_testseq.currentRow()
            # 初始化需要编辑的plan字典
            global_element.editplan_dict = copy.deepcopy(global_element.Testseq_list[current_row])

            self.testplanwin_example = TestplanWindow('editplan')  # 以editplan的方式初始化弹出窗口
            self.testplanwin_example.okbtn_Signal.connect(self.receivesignalprocess_foredittestplan)
            self.testplanwin_example.show()

    # 打开editcase窗口后收到ok信号的槽函数
    def receivesignalprocess_foredittestplan(self, content, temptime):
        # 更新编辑过后的字典
        current_row = self.listWidget_testseq.currentRow()
        global_element.Testseq_list[current_row]['@name'] = content
        global_element.Testseq_list[current_row]['@condition'] = content.split(' ')[1]
        global_element.Testseq_list[current_row]['@tempstabtime'] = temptime
        global_element.Testseq_list[current_row]['item'] = global_element.Testplan_list

        # 界面上更新用户新增的testplan
        self.listWidget_testseq.item(current_row).setText(content)

    # copy按钮槽函数
    def copybtnclick(self):
        if len(self.listWidget_testseq.selectedItems()) > 0:
            selected_item_list = self.listWidget_testseq.selectedItems()
            selected_row_list = []
            for i in selected_item_list:
                if self.listWidget_testseq.indexFromItem(i).row() not in selected_row_list:
                    selected_row_list.append(self.listWidget_testseq.indexFromItem(i).row())

            for i in selected_row_list:
                current_text = self.listWidget_testseq.item(i).text()                   # 更新界面
                current_checkstate = self.listWidget_testseq.item(i).checkState()
                item = QtWidgets.QListWidgetItem()
                item.setText(current_text)
                item.setCheckState(current_checkstate)
                self.listWidget_testseq.addItem(item)
                dict_item = copy.deepcopy(global_element.Testseq_list[i])          # 更新逻辑字典
                # dict_item = dict(dict_item)
                global_element.Testseq_list.append(dict_item)

            # 逻辑列表操作后更新'index'
            for i in range(len(global_element.Testseq_list)):
                global_element.Testseq_list[i]['@index'] = i

    # removecase按钮槽函数
    def removebtnclick(self):
        if len(self.listWidget_testseq.selectedItems()) > 0:
            selected_item_list = self.listWidget_testseq.selectedItems()
            selected_row_list = []
            for i in selected_item_list:
                if self.listWidget_testseq.indexFromItem(i).row() not in selected_row_list:
                    selected_row_list.append(self.listWidget_testseq.indexFromItem(i).row())

            # 更新界面
            selected_row_list.sort()
            selected_row_list.reverse()       # 将列表倒序，从下面开始移除
            for i in selected_row_list:
                # 更新界面
                self.listWidget_testseq.takeItem(i)
                # 更新逻辑字典
                global_element.Testseq_list.pop(i)

            # 更新字典中‘@index’
            for i in range(len(global_element.Testseq_list)):
                global_element.Testseq_list[i]['@index'] = i

    # up按钮槽函数
    def upbtnclick(self):
        if self.listWidget_testseq.currentItem():
            current_row = self.listWidget_testseq.currentRow()

            if current_row != 0:

                # 上移操作后更新界面列表
                # 将要上移的item信息保存
                current_text = self.listWidget_testseq.item(current_row).text()
                current_checkstate = self.listWidget_testseq.item(current_row).checkState()
                # 删除要上移的item
                self.listWidget_testseq.takeItem(current_row)
                # 在上一位置插入item实现上移效果
                insert_item = QtWidgets.QListWidgetItem()
                insert_item.setCheckState(current_checkstate)
                insert_item.setText(current_text)
                self.listWidget_testseq.insertItem(current_row - 1, insert_item)
                self.listWidget_testseq.setCurrentRow(current_row - 1)

                # 在逻辑字典上删除item
                item = global_element.Testseq_list[current_row]
                global_element.Testseq_list.pop(current_row)                # 从逻辑列表中删除
                global_element.Testseq_list.insert(current_row - 1, item)   # 在逻辑列表中对应位置插入实现与上一元素换位

                # 逻辑列表操作后更新'index'
                for i in range(len(global_element.Testseq_list)):
                    global_element.Testseq_list[i]['@index'] = i

    # down按钮槽函数
    def downbtnclick(self):
        if self.listWidget_testseq.currentItem():
            current_row = self.listWidget_testseq.currentRow()
            if current_row != self.listWidget_testseq.count() - 1:

                # 下移操作后更新界面列表
                # 将要下移的item信息保存
                current_text = self.listWidget_testseq.item(current_row).text()
                current_checkstate = self.listWidget_testseq.item(current_row).checkState()

                # 删除要下移的item
                self.listWidget_testseq.takeItem(current_row)
                # 在下一位置插入item实现下移效果
                insert_item = QtWidgets.QListWidgetItem()
                insert_item.setCheckState(current_checkstate)
                insert_item.setText(current_text)
                self.listWidget_testseq.insertItem(current_row + 1, insert_item)
                self.listWidget_testseq.setCurrentRow(current_row + 1)

                # 下移操作后逻辑字典上更新
                item = global_element.Testseq_list[current_row]
                global_element.Testseq_list.pop(current_row)  # 从逻辑列表中删除
                global_element.Testseq_list.insert(current_row + 1, item)  # 在逻辑列表中对应位置插入实现与上一元素换位

                # 逻辑列表操作后更新'index'
                for i in range(len(global_element.Testseq_list)):
                    global_element.Testseq_list[i]['@index'] = i

    # enable all 按钮槽函数
    def enableallbtnclick(self):
        # 更新界面列表
        for i in range(self.listWidget_testseq.count()):
            self.listWidget_testseq.item(i).setCheckState(Qt.Checked)

        # 会自动调用itemchanged函数更新逻辑列表中的‘@enable’,下面两行可能注释
        # # 更新逻辑列表中的‘@enable’
        # for item in global_element.Testplan_list:
        #     item['@enable'] = 'yes'

    # disable all 按钮槽函数
    def disableallbtnclick(self):
        # 更新界面列表
        for i in range(self.listWidget_testseq.count()):
            self.listWidget_testseq.item(i).setCheckState(not Qt.Checked)

        # 会自动调用itemchanged函数更新逻辑列表中的‘@enable’,下面两行可能注释
        # # 更新逻辑列表中的‘@enable’
        # for item in global_element.Testplan_list:
        #     item['@enable'] = 'no'

    # 当test seq列表勾选发生变化时，更新逻辑列表中的‘@enable’
    def itemchanged(self):
        checkstate_list = []
        for i in range(self.listWidget_testseq.count()):
            checkstate_list.append(self.listWidget_testseq.item(i).checkState())

        for i in range(len(global_element.Testseq_list)):
            if checkstate_list[i] == Qt.Checked:
                result_check = 'yes'
            else:
                result_check = 'no'
            global_element.Testseq_list[i]['@enable'] = result_check

    # cancel按钮槽函数
    def cancelbtnclick(self):
        global_element.Testseq_list.clear()
        self.close()

    # ok按钮槽函数
    def okbtnclick(self):
        global_element.Testsequence_dict['seq']['items'] = global_element.Testseq_list
        self.okbtnclickSingle.emit(len(global_element.Testseq_list))
        self.close()

    # 菜单栏add seq槽函数
    def addseq(self):
        fileName_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                'Selecting Test Sequences',
                                                                self.cwd,
                                                                'IORI TestSeq Files (*.IORIseq);;All Files (*)')
        if fileName_choose != '':
            xml_dict = global_element.xml_to_dict(fileName_choose)
            if isinstance(xml_dict['seq']['items'], dict):
                new_list = [xml_dict['seq']['items']]
            else:
                new_list = xml_dict['seq']['items']
            global_element.Testseq_list = global_element.Testseq_list + new_list
            # self.listWidget_testseq.clear()
            for i in new_list:
                item = QtWidgets.QListWidgetItem()
                current_text = i['@name']
                if i['@enable'] == 'yes':
                    current_checkstate = Qt.Checked
                else:
                    current_checkstate = not Qt.Checked
                item.setText(current_text)
                item.setCheckState(current_checkstate)
                self.listWidget_testseq.addItem(item)

            # 更新字典中‘@index’
            for i in range(len(global_element.Testseq_list)):
                global_element.Testseq_list[i]['@index'] = i


class TestplanWindow(QMainWindow, UI_testplan.Ui_Window_testplan):
    """
        Test plan界面
    """
    okbtn_Signal = pyqtSignal(str, str)

    def __init__(self, init_mode, parent=None):
        super(TestplanWindow, self).__init__(parent)
        self.setupUi(self)
        self.init_mode = init_mode
        self.initexample()

        # 设置为模拟对话框，阻塞上一层窗口
        self.setWindowModality(Qt.ApplicationModal)

        # 界面控件的信号槽关系
        self.comboBox_loadmodule.currentIndexChanged.connect(self.loaditems)
        self.pushButton_add.clicked.connect(self.additemtoplan)
        self.pushButton_remove.clicked.connect(self.removeitem)
        self.pushButton_up.clicked.connect(self.upitem)
        self.pushButton_down.clicked.connect(self.downitem)
        self.pushButton_disableall.clicked.connect(self.disable_all)
        self.pushButton_enableall.clicked.connect(self.enable_all)
        self.listWidget_testplan.itemChanged.connect(self.itemchanged)
        self.listWidget_testplan.itemDoubleClicked.connect(self.itemdoubleclick)
        self.comboBox_Volt.currentIndexChanged.connect(self.plantitleupdata)
        self.comboBox_Temp.currentIndexChanged.connect(self.plantitleupdata)
        self.pushButton_cancel.clicked.connect(self.cancelbtnclick)
        self.pushButton_ok.clicked.connect(self.okbtnclick)
        self.listWidget_supporteditems.itemDoubleClicked.connect(self.additemtoplan)

    def initexample(self):
        if self.init_mode == 'newplan':
            global_element.Testplan_list = []  # 打开此窗口时初始化testplan列表为空
            self.plantitleupdata()
        if self.init_mode == 'editplan':
            # global_element.editplan_dict 此字典在父窗口初始化
            mode_name = global_element.editplan_dict['@name'].split(' ')[0]          # 取得editplan的mode名字（如：BT2）
            self.comboBox_loadmodule.setCurrentText(mode_name)

            # 将所选模块的内容加载到界面支持的Items列表中
            global_element.Test_items_default_config_dict = global_element.xml_to_dict(
                global_element.TESTITEMSCONFIGPATH
                + mode_name + '.xml')
            for item in global_element.Test_items_default_config_dict['xml']['TestItems']['item']:
                if item['@Name'] != 'Init seting':
                    self.listWidget_supporteditems.addItem(item['@Name'])

            # 初始化plan additional title
            envi = global_element.editplan_dict['@name'].split(' ')[1]
            temperature = envi[:2]
            volt = envi[2:]
            self.comboBox_Temp.setCurrentText(temperature)
            self.comboBox_Volt.setCurrentText(volt)
            self.plantitleupdata()
            if len(global_element.editplan_dict['@name'].split(' ')) > 2:
                additional_name_str = ' '.join(global_element.editplan_dict['@name'].split(' ')[2:])
                self.lineEdit_plantitle.setText(additional_name_str)

            # 初始化global_element.Testplan_list
            global_element.Testplan_list = list(global_element.editplan_dict['item'])
            # 初始化tesplan窗口列表
            for i in global_element.Testplan_list:
                item = QtWidgets.QListWidgetItem()
                item.setText(i['@Name'])
                if i['@Name'] != 'Init seting':
                    if i['@enable'] == 'yes':
                        item.setCheckState(Qt.Checked)
                    if i['@enable'] == 'no':
                        item.setCheckState(not Qt.Checked)
                self.listWidget_testplan.addItem(item)

    # 选择需要载入的模块，将此模块支持items列出，并将此模块的所有信息初始化成字典
    def loaditems(self):
        global_element.Testplan_list = []  # 切换模块时初始化testplan列表为空
        self.listWidget_testplan.clear()
        self.listWidget_supporteditems.clear()
        module_selected = self.comboBox_loadmodule.currentText()
        if module_selected != '':
            # 将所选模块的内容加载到界面支持的Items列表中
            try:
                global_element.Test_items_default_config_dict = global_element.xml_to_dict(global_element.TESTITEMSCONFIGPATH
                                                                                           + module_selected + '.xml')
                for item in global_element.Test_items_default_config_dict['xml']['TestItems']['item']:
                    if item['@Name'] != 'Init seting':
                        self.listWidget_supporteditems.addItem(item['@Name'])

                # 将init seting加载到plan的界面列表及testplan的逻辑列表中
                item = QtWidgets.QListWidgetItem()
                # item.setCheckState(Qt.Checked)
                item.setText('Init seting')
                self.listWidget_testplan.addItem(item)
                # global_element.Test_items_default_config_dict['xml']['TestItems']['item'][0]['@enable'] = 'yes'
                global_element.Testplan_list.append(global_element.Test_items_default_config_dict['xml']['TestItems']['item'][0])

                self.plantitleupdata()
            except:
                self.comboBox_loadmodule.setCurrentIndex(0)
                win32api.MessageBox(0, 'The module is not supported temporarily!', 'Tip', win32con.MB_OK)
        else:
            self.listWidget_supporteditems.clear()
            self.listWidget_testplan.clear()

    # add按钮槽函数，把选中的items加入plan中
    def additemtoplan(self):
        items_selected_list = self.listWidget_supporteditems.selectedItems()
        if len(items_selected_list) > 0:
            items_selected_text_list = [i.text() for i in list(items_selected_list)]
            for i in items_selected_text_list:

                # 界面testplan列表添加item
                item = QtWidgets.QListWidgetItem()
                item.setCheckState(Qt.Checked)
                item.setText(i)
                self.listWidget_testplan.addItem(item)

                # 将加入的item数据更新入testplan逻辑列表
                for item_index in global_element.Test_items_default_config_dict['xml']['TestItems']['item']:
                    if item_index['@Name'] == i:
                        item = dict(item_index)
                        item['@index'] = ''
                        item['@enable'] = 'yes'
                        global_element.Testplan_list.append(item)
                        break

            for i in range(1, len(global_element.Testplan_list)):
                global_element.Testplan_list[i]['@index'] = i

    # remove按钮槽函数，将testplan中选中的item移除
    def removeitem(self):
        if len(self.listWidget_testplan.selectedItems()) > 0:
            selected_item_list = self.listWidget_testplan.selectedItems()
            selected_row_list = []
            for i in selected_item_list:
                if self.listWidget_testplan.indexFromItem(i).row() not in selected_row_list:
                    selected_row_list.append(self.listWidget_testplan.indexFromItem(i).row())

            # 更新界面
            selected_row_list.sort()
            selected_row_list.reverse()  # 将列表倒序，从下面开始移除
            for i in selected_row_list:
                if i != 0:
                    # 更新界面
                    self.listWidget_testplan.takeItem(i)
                    # 更新逻辑字典
                    global_element.Testplan_list.pop(i)

            # 更新字典中‘@index’
            for i in range(1, len(global_element.Testplan_list)):
                global_element.Testplan_list[i]['@index'] = i

    # up按钮槽函数，向上移动testplan中选中的item
    def upitem(self):
        if self.listWidget_testplan.currentItem():
            current_row = self.listWidget_testplan.currentRow()
            if current_row != 0 and current_row != 1:

                # 上移操作后更新界面列表
                # 将要上移的item信息保存
                current_text = self.listWidget_testplan.item(current_row).text()
                current_checkstate = self.listWidget_testplan.item(current_row).checkState()
                # 删除要上移的item
                self.listWidget_testplan.takeItem(current_row)
                # 在上一位置插入item实现上移效果
                insert_item = QtWidgets.QListWidgetItem()
                insert_item.setCheckState(current_checkstate)
                insert_item.setText(current_text)
                self.listWidget_testplan.insertItem(current_row - 1, insert_item)
                self.listWidget_testplan.setCurrentRow(current_row - 1)

                # 上移操作后更新逻辑列表
                for item in global_element.Testplan_list:
                    if item['@Name'] == current_text:
                        index = global_element.Testplan_list.index(item)       # 找到逻辑列表中item对应的index
                        global_element.Testplan_list.pop(index)                # 从逻辑列表中删除
                        global_element.Testplan_list.insert(index - 1, item)   # 在逻辑列表中对应位置插入实现与上一元素换位
                        break

                # 逻辑列表操作后更新'index'
                for i in range(1, len(global_element.Testplan_list)):
                    global_element.Testplan_list[i]['@index'] = i

    # down按钮槽函数，向下移动testplan中选中的item
    def downitem(self):
        if self.listWidget_testplan.currentItem():
            current_row = self.listWidget_testplan.currentRow()
            if current_row != self.listWidget_testplan.count() - 1 and current_row != 0:

                # 下移操作后更新界面列表
                # 将要下移的item信息保存
                current_text = self.listWidget_testplan.item(current_row).text()
                current_checkstate = self.listWidget_testplan.item(current_row).checkState()

                # 删除要下移的item
                self.listWidget_testplan.takeItem(current_row)
                # 在下一位置插入item实现下移效果
                insert_item = QtWidgets.QListWidgetItem()
                insert_item.setCheckState(current_checkstate)
                insert_item.setText(current_text)
                self.listWidget_testplan.insertItem(current_row + 1, insert_item)
                self.listWidget_testplan.setCurrentRow(current_row + 1)

                # 下移操作后更新逻辑列表
                for item in global_element.Testplan_list:
                    if item['@Name'] == current_text:
                        index = global_element.Testplan_list.index(item)  # 找到逻辑列表中item对应的index
                        global_element.Testplan_list.pop(index)  # 从逻辑列表中删除
                        global_element.Testplan_list.insert(index + 1, item)  # 在逻辑列表中对应位置插入实现与上一元素换位
                        break

                # 逻辑列表操作后更新'index'
                for i in range(1, len(global_element.Testplan_list)):
                    global_element.Testplan_list[i]['@index'] = i

    # disable all按钮槽函数
    def disable_all(self):

        # 更新界面列表
        for i in range(1, self.listWidget_testplan.count()):
            self.listWidget_testplan.item(i).setCheckState(not Qt.Checked)

        # 会自动调用itemchanged函数更新逻辑列表中的‘@enable’,下面两行可能注释
        # # 更新逻辑列表中的‘@enable’
        # for item in global_element.Testplan_list:
        #     item['@enable'] = 'no'

    # enable all按钮槽函数
    def enable_all(self):

        # 更新界面列表
        for i in range(1, self.listWidget_testplan.count()):
            self.listWidget_testplan.item(i).setCheckState(Qt.Checked)

        # 会自动调用itemchanged函数更新逻辑列表中的‘@enable’,下面两行可能注释
        # # 更新逻辑列表中的‘@enable’
        # for item in global_element.Testplan_list:
        #     item['@enable'] = 'yes'

    # 当test plan列表勾选发生变化时，更新逻辑列表中的‘@enable’
    def itemchanged(self):
        checkstate_list = []
        for i in range(1, self.listWidget_testplan.count()):
            checkstate_list.append(self.listWidget_testplan.item(i).checkState())

        for i in range(len(checkstate_list)):
            if checkstate_list[i] == Qt.Checked:
                result_check = 'yes'
            else:
                result_check = 'no'
            global_element.Testplan_list[i + 1]['@enable'] = result_check

    # 双击item弹出item config窗口，并将该item的参数传入，初始化窗口
    def itemdoubleclick(self):
        current_row = self.listWidget_testplan.currentRow()
        self.itemconfigwin_example = itemconfigWindow(global_element.Testplan_list[current_row])
        self.itemconfigwin_example.okbtn_Signal.connect(self.saveitemparmslimits)
        self.itemconfigwin_example.show()

    # 收到item编辑子窗口发射的save号后执行的槽函数
    def saveitemparmslimits(self, content):
        if content == 'ok':
            # 将用户定义的item config内容更新到testplan字典，以备测试时调用及更新的test seq字典时用

            current_row = self.listWidget_testplan.currentRow()    # 确定需要更新的item在列表中的index

            # 更新parms部分
            if global_element.Testitemparmslimits_state[0] == 1:      # parms部分是一个字典类型
                global_element.Testplan_list[current_row]['parms']['Parm'] = global_element.Testitemparms_dict
            if global_element.Testitemparmslimits_state[0] == 2:      # parms部分是一个列表类型
                global_element.Testplan_list[current_row]['parms']['Parm'] = global_element.Testitemparms_list

            # 更新limits部分
            if global_element.Testitemparmslimits_state[1] == 1:      # limits部分是一个字典类型
                global_element.Testplan_list[current_row]['limits']['limit'] = global_element.Testitemlimts_dict
            if global_element.Testitemparmslimits_state[1] == 2:       # limits部分是一个列表类型
                global_element.Testplan_list[current_row]['limits']['limit'] = global_element.Testitemlimts_list

    # 更新plan title
    def plantitleupdata(self):
        temp = self.comboBox_Temp.currentText()
        volt = self.comboBox_Volt.currentText()
        module_name = self.comboBox_loadmodule.currentText()
        self.label_plantitle.setText('%s %s%s' % (module_name, temp, volt))

    # cancel按钮槽函数
    def cancelbtnclick(self):
        global_element.Testplan_list.clear()
        self.close()

    # ok按钮槽函数
    def okbtnclick(self):
        if self.listWidget_testplan.count() > 1:
            content = self.label_plantitle.text() + ' ' + self.lineEdit_plantitle.text()
            Temp_stab_time = self.lineEdit_temptime.text()
            self.okbtn_Signal.emit(content, Temp_stab_time)                   # 将test plan的名称以信号发射给父窗口
            self.close()                                      # 关闭窗口
        else:
            win32api.MessageBox(0, 'Please add at least one test item!')


class itemconfigWindow(QMainWindow, UI_itemparam.Ui_Window_itemparam):
    """
        test item config界面
    """
    okbtn_Signal = pyqtSignal(str)      # 自定义一个ok按钮的信号

    def __init__(self, item_dict, parent=None):
        super(itemconfigWindow, self).__init__(parent)
        self.item_dict = item_dict
        self.setupUi(self)
        self.initexample()

        # 设置为模拟对话框，阻塞上一层窗口
        self.setWindowModality(Qt.ApplicationModal)

        # 定义信号槽关系
        self.tableWidget_itemlimit.currentItemChanged.connect(self.displaylimitinfo)
        self.tableWidget_itemconfig.itemSelectionChanged.connect(self.displayparminfo)
        self.pushButton_cancel.clicked.connect(self.cancelbtnclick)
        self.pushButton_ok.clicked.connect(self.okbtnclick)

    # 通过传入字典的内容初始化item config的窗口
    def initexample(self):
        self.tableWidget_itemconfig.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 自适应水平宽度
        self.tableWidget_itemlimit.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 自适应水平宽度
        self.tableWidget_itemconfig.horizontalHeader().setStyleSheet('QHeaderView::section{background:lightblue;}')
        self.tableWidget_itemconfig.verticalHeader().setStyleSheet('QHeaderView::section{background:lightblue;}')
        self.tableWidget_itemlimit.horizontalHeader().setStyleSheet('QHeaderView::section{background:lightblue;}')
        self.tableWidget_itemlimit.verticalHeader().setStyleSheet('QHeaderView::section{background:lightblue;}')

        global_element.Testitemparms_list = []
        global_element.Testitemparms_dict = {}
        global_element.Testitemlimts_list = []
        global_element.Testitemlimts_dict = {}
        global_element.Testitemparmslimits_state = [0, 0]

        # 初始化parm窗口
        try:                                                                       # parms如果有默认配置参数，则初始化，没有则跳过
            if isinstance(self.item_dict['parms']['Parm'], list):                  # 判断是否是列表类型，（因为如果是只有一个参数，将会是字典类型）
                global_element.Testitemparms_list = copy.deepcopy(self.item_dict['parms']['Parm'])
                self.tableWidget_itemconfig.setRowCount(len(global_element.Testitemparms_list))   # 根据parm数量初始化表格控件行数

                for i in range(len(global_element.Testitemparms_list)):
                    item = QtWidgets.QTableWidgetItem()
                    item.setText(global_element.Testitemparms_list[i]['Name'])
                    item.setFlags(Qt.NoItemFlags)
                    self.tableWidget_itemconfig.setItem(i, 0, item)

                    if global_element.Testitemparms_list[i]['Type'] == '1':
                        comboBoxList = global_element.Testitemparms_list[i]['Range'].split(',')
                        comboBox = QtWidgets.QComboBox()
                        comboBox.addItems(comboBoxList)
                        comboBox.setCurrentText(global_element.Testitemparms_list[i]['Value'])
                        self.tableWidget_itemconfig.setCellWidget(i, 1, comboBox)
                    else:
                        item1 = QtWidgets.QTableWidgetItem()
                        item1.setText(global_element.Testitemparms_list[i]['Value'])
                        self.tableWidget_itemconfig.setItem(i, 1, item1)

                global_element.Testitemparmslimits_state[0] = 2      # 记录此item的parms多于1个，是列表类型

            if isinstance(self.item_dict['parms']['Parm'], dict):
                global_element.Testitemparms_dict = copy.deepcopy(self.item_dict['parms']['Parm'])
                self.tableWidget_itemconfig.setRowCount(1)  # 因为是字典类型,只有一个参数
                item = QtWidgets.QTableWidgetItem()
                item.setText(global_element.Testitemparms_dict['Name'])
                item.setFlags(Qt.NoItemFlags)
                self.tableWidget_itemconfig.setItem(0, 0, item)

                if global_element.Testitemparms_dict['Type'] == '1':
                    comboBoxList = global_element.Testitemparms_dict['Range'].split(',')
                    comboBox = QtWidgets.QComboBox()
                    comboBox.addItems(comboBoxList)
                    comboBox.setCurrentText(global_element.Testitemparms_dict['Value'])
                    self.tableWidget_itemconfig.setCellWidget(0, 1, comboBox)
                else:
                    item1 = QtWidgets.QTableWidgetItem()
                    item1.setText(global_element.Testitemparms_dict['Value'])
                    self.tableWidget_itemconfig.setItem(0, 1, item1)

                global_element.Testitemparmslimits_state[0] = 1  # 记录此item的parms等于1个，是字典类型

        except:
            global_element.Testitemparmslimits_state[0] = 0     # 记录此item的parms为空

        try:                                                          # limit如果有默认配置参数，则初始化，没有则跳过
            # 初始化limit窗口
            if isinstance(self.item_dict['limits']['limit'], list):  # 判断是否是列表类型，（因为如果是只有一个参数，将会是字典类型）
                global_element.Testitemlimts_list = copy.deepcopy(self.item_dict['limits']['limit'])
                self.tableWidget_itemlimit.setRowCount(len(global_element.Testitemlimts_list))  # 根据parm数量初始化表格控件行数

                for i in range(len(global_element.Testitemlimts_list)):
                    item = QtWidgets.QTableWidgetItem()
                    item.setText(global_element.Testitemlimts_list[i]['Name'])
                    item.setFlags(Qt.NoItemFlags)
                    self.tableWidget_itemlimit.setItem(i, 0, item)

                    item1 = QtWidgets.QTableWidgetItem()
                    item1.setText(global_element.Testitemlimts_list[i]['low'])
                    self.tableWidget_itemlimit.setItem(i, 1, item1)

                    item2 = QtWidgets.QTableWidgetItem()
                    item2.setText(global_element.Testitemlimts_list[i]['high'])
                    self.tableWidget_itemlimit.setItem(i, 2, item2)

                global_element.Testitemparmslimits_state[1] = 2           # 记录此item的limits多于1个，是列表类型

            if isinstance(self.item_dict['limits']['limit'], dict):
                global_element.Testitemlimts_dict = copy.deepcopy(self.item_dict['limits']['limit'])
                self.tableWidget_itemlimit.setRowCount(1)  # 因为是字典类型,只有一个参数
                item = QtWidgets.QTableWidgetItem()
                item.setText(global_element.Testitemlimts_dict['Name'])
                item.setFlags(Qt.NoItemFlags)
                self.tableWidget_itemlimit.setItem(0, 0, item)

                item1 = QtWidgets.QTableWidgetItem()
                item1.setText(global_element.Testitemlimts_dict['low'])
                self.tableWidget_itemlimit.setItem(0, 1, item1)

                item1 = QtWidgets.QTableWidgetItem()
                item1.setText(global_element.Testitemlimts_dict['high'])
                self.tableWidget_itemlimit.setItem(0, 2, item1)

                global_element.Testitemparmslimits_state[1] = 1       # 记录此item的limits等于1个，是字典类型
        except:
            global_element.Testitemparmslimits_state[1] = 0           # 记录此item的limits为空

    # 定义当前limit框中item改变时，更新remark框中信息的函数
    def displaylimitinfo(self):
        currentitem_row = self.tableWidget_itemlimit.currentRow()
        currentitem_column = self.tableWidget_itemlimit.currentColumn()
        currentrow_name = self.tableWidget_itemlimit.item(currentitem_row, 0).text()

        # 如果是字典类型，取字典的值更新remark内容
        if global_element.Testitemparmslimits_state[1] == 1:
            value_range = global_element.Testitemlimts_dict['Range']
            value_info = global_element.Testitemlimts_dict['info']

            self.label_info.setText('Range: %s\nInfo: %s' % (value_range, value_info))

        # 如果是列表类型，取列表的值更新remark内容
        if global_element.Testitemparmslimits_state[1] == 2:
            # 遍历列表，找到当前limit的index
            for i in global_element.Testitemlimts_list:
                if i['Name'] == currentrow_name:
                    index_currnet = global_element.Testitemlimts_list.index(i)
                    break

            value_range = global_element.Testitemlimts_list[index_currnet]['Range']
            value_info = global_element.Testitemlimts_list[index_currnet]['info']

            self.label_info.setText('Range: %s\nInfo: %s' % (value_range, value_info))

    # 定义当前parm框中item改变时，更新remark框中信息的函数
    def displayparminfo(self):
        currentitem_row = self.tableWidget_itemconfig.currentRow()
        currentrow_name = self.tableWidget_itemconfig.item(currentitem_row, 0).text()

        # 如果是字典类型，取字典的值更新remark内容
        if global_element.Testitemparmslimits_state[0] == 1:
            value_range = global_element.Testitemparms_dict['Range']
            value_info = global_element.Testitemparms_dict['info']
            self.label_info.setText('Range: %s\nInfo: %s' % (value_range, value_info))

        # 如果是列表类型，取列表的值更新remark内容
        if global_element.Testitemparmslimits_state[0] == 2:
            # 遍历列表，找到当前limit的index
            for i in global_element.Testitemparms_list:
                if i['Name'] == currentrow_name:
                    index_currnet = global_element.Testitemparms_list.index(i)
                    break

            value_range = global_element.Testitemparms_list[index_currnet]['Range']
            value_info = global_element.Testitemparms_list[index_currnet]['info']

            self.label_info.setText('Range: %s\nInfo: %s' % (value_range, value_info))

    # cancel按钮槽数
    def cancelbtnclick(self):
        # 清空用到的所有全局变量
        global_element.Testitemparms_list = []
        global_element.Testitemparms_dict = {}
        global_element.Testitemlimts_list = []
        global_element.Testitemlimts_dict = {}
        global_element.Testitemparmslimits_state = [0, 0]

        self.close()   # 关闭窗口

    # ok按钮槽数
    def okbtnclick(self):
        # 用户选择激活界面配置，更新全球变量（parms、limits的字典或列表）

        # 更新parms的字典或列表
        if global_element.Testitemparmslimits_state[0] == 1:    # 如果是字典（一个参数）
            # 因为不知道是combobox还是tablewidgetitem，所以用try
            try:
                global_element.Testitemparms_dict['Value'] = self.tableWidget_itemconfig.item(0, 1).text()
            except:
                pass
            try:
                global_element.Testitemparms_dict['Value'] = self.tableWidget_itemconfig.cellWidget(0, 1).currentText()
            except:
                pass

        if global_element.Testitemparmslimits_state[0] == 2:    # 如果是列表（大于一个参数）
            for i in range(len(global_element.Testitemparms_list)):
                try:
                    global_element.Testitemparms_list[i]['Value'] = self.tableWidget_itemconfig.cellWidget(i, 1).currentText()
                except:
                    pass
                try:
                    global_element.Testitemparms_list[i]['Value'] = self.tableWidget_itemconfig.item(i, 1).text()
                except:
                    pass

        # 更新limits的字典或列表
        if global_element.Testitemparmslimits_state[1] == 1:    # 如果是字典（一个参数）
            global_element.Testitemlimts_dict['low'] = self.tableWidget_itemlimit.item(0, 1).text()
            global_element.Testitemlimts_dict['high'] = self.tableWidget_itemlimit.item(0, 2).text()
        if global_element.Testitemparmslimits_state[1] == 2:    # 如果是列表（大于一个参数）
            for i in range(len(global_element.Testitemlimts_list)):
                global_element.Testitemlimts_list[i]['low'] = self.tableWidget_itemlimit.item(i, 1).text()
                global_element.Testitemlimts_list[i]['high'] = self.tableWidget_itemlimit.item(i, 2).text()

        # 给父窗口发射一个信号（通知父窗口用户选择应用窗口配置，放弃默认配置）
        self.okbtn_Signal.emit('ok')
        # 关闭窗口
        self.close()


class losseditorWindow(QMainWindow, UI_losseditor.Ui_Edit_loss_file_Window):
    """
        loss editor界面
    """

    def __init__(self, parent=None):
        super(losseditorWindow, self).__init__(parent)
        self.setupUi(self)
        self.cwd = 'RFC/'
        self.initexample()

        # 设置为模拟对话框，阻塞上一层窗口
        self.setWindowModality(Qt.ApplicationModal)

        # 信号槽关系
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_addline.clicked.connect(self.addline)
        self.pushButton_removeline.clicked.connect(self.removeline)
        self.pushButton_creat.clicked.connect(self.creatlossfile)
        self.pushButton_loadfile.clicked.connect(self.loadfile)

    def initexample(self):
        self.tableWidget_lossedit.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 自适应水平宽度
        self.tableWidget_lossedit.horizontalHeader().setStyleSheet('QHeaderView::section{background:lightblue;}')
        self.tableWidget_lossedit.verticalHeader().setStyleSheet('QHeaderView::section{background:lightblue;}')

    # add line按钮槽函数
    def addline(self):
        current_row = self.tableWidget_lossedit.rowCount()
        self.tableWidget_lossedit.setRowCount(current_row + 1)

    # remove line按钮槽函数
    def removeline(self):
        current_row = self.tableWidget_lossedit.rowCount()
        self.tableWidget_lossedit.setRowCount(current_row - 1)

    # creat loss file按钮槽函数
    def creatlossfile(self):
        loss_list = []
        loss_dict = {}
        loss_dict_final = {}
        loss_dict_final['Loss'] = {}
        current_row = self.tableWidget_lossedit.rowCount()
        if current_row > 0:
            for i in range(current_row):
                Freq = self.tableWidget_lossedit.item(i, 0).text()
                loss = self.tableWidget_lossedit.item(i, 1).text()
                loss_dict['Frequency'] = Freq
                loss_dict['Value'] = loss
                loss_list.append(loss_dict)
                loss_dict = {1: 2, 2: 3}     # 此两行代码是让loss_dict与loss_dict失去关联，以便list中已append的元素随便dict变化
                loss_dict.clear()
            loss_dict_final['Loss']['loss'] = loss_list

            fileName_choose, filetype = QFileDialog.getSaveFileName(self,
                                                                    'Save Path Loss Files',
                                                                    self.cwd,
                                                                    'Loss Files (*.IORIloss);;All Files (*)')

            if fileName_choose != '':
                global_element.dict_to_xmlstr(loss_dict_final, fileName_choose)

        else:
            win32api.MessageBox(0, 'There is no data to save Loss File!')

    # 定义load file按钮槽函数
    def loadfile(self):
        self.tableWidget_lossedit.setRowCount(0)
        fileName_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                'Selecting Path Loss Files',
                                                                self.cwd,
                                                                'Loss Files (*.IORIloss);;All Files (*)')
        if fileName_choose != '':
            dict_loss = global_element.xml_to_dict(fileName_choose)
            self.tableWidget_lossedit.setRowCount(len(dict_loss['Loss']['loss']))
            for i in range(len(dict_loss['Loss']['loss'])):
                item = QtWidgets.QTableWidgetItem()
                # print(dict_loss['Loss']['loss'][i]['Frequency'])
                item.setText(dict_loss['Loss']['loss'][i]['Frequency'])
                self.tableWidget_lossedit.setItem(i, 0, item)

                item2 = QtWidgets.QTableWidgetItem()
                item2.setText(dict_loss['Loss']['loss'][i]['Value'])
                self.tableWidget_lossedit.setItem(i, 1, item2)


class lossfileselectWindow(QMainWindow, UI_selectlossfile.Ui_Window_selectlossfile):
    """
        loss file select界面
    """

    def __init__(self, parent=None):
        super(lossfileselectWindow, self).__init__(parent)
        self.setupUi(self)
        self.cwd = 'RFC/'

        self.initexample()

        # 设置为模拟对话框，阻塞上一层窗口
        self.setWindowModality(Qt.ApplicationModal)

        # 信号槽关系
        self.pushButton_selectCUloss.clicked.connect(self.selectCUloss)
        self.pushButton_selectSAloss.clicked.connect(self.selectSAloss)
        self.pushButton_selectESGloss.clicked.connect(self.selectESGloss)
        self.pushButton_ok.clicked.connect(self.okbtnclick)

    def initexample(self):
        self.lineEdit_CUlossfile.setText(global_element.CU_DUT_loss_file)
        self.lineEdit_SAlossfile.setText(global_element.SA_DUT_loss_file)

    # 定义select CU loss按钮槽函数
    def selectCUloss(self):
        fileName_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                'Select path loss file!',
                                                                self.cwd,
                                                                'Loss Files (*.IORIloss);;All Files (*)')
        if fileName_choose != '':
            self.lineEdit_CUlossfile.setText(fileName_choose)

    # 定义select SA loss按钮槽函数
    def selectSAloss(self):
        fileName_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                'Select path loss file!',
                                                                self.cwd,
                                                                'Loss Files (*.IORIloss);;All Files (*)')
        if fileName_choose != '':
            self.lineEdit_SAlossfile.setText(fileName_choose)

    # 定义select ESG loss按钮槽函数
    def selectESGloss(self):
        fileName_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                'Select path loss file!',
                                                                self.cwd,
                                                                'Loss Files (*.IORIloss);;All Files (*)')
        if fileName_choose != '':
            self.lineEdit_ESGLOSS.setText(fileName_choose)

    # 定义ok按钮槽函数
    def okbtnclick(self):
        if self.lineEdit_CUlossfile.text() != '':
            try:
                global_element.CU_DUT_loss_file = self.lineEdit_CUlossfile.text()
                global_element.CU_DUT_loss = global_element.xml_to_dict(self.lineEdit_CUlossfile.text())
            except:
                global_element.CU_DUT_loss_file = ''
                global_element.CU_DUT_loss = {}
                win32api.MessageBox(0, 'CU - > DUT path loss file error!')
        else:
            global_element.CU_DUT_loss_file = ''
            global_element.CU_DUT_loss = {}
        if self.lineEdit_SAlossfile.text() != '':
            try:
                global_element.SA_DUT_loss_file = self.lineEdit_SAlossfile.text()
                global_element.SA_DUT_loss = global_element.xml_to_dict(self.lineEdit_SAlossfile.text())
            except:
                win32api.MessageBox(0, 'SA -> DUT path loss file error!')
                global_element.SA_DUT_loss_file = ''
                global_element.SA_DUT_loss = {}
        else:
            global_element.SA_DUT_loss_file = ''
            global_element.SA_DUT_loss = {}
        if self.lineEdit_ESGLOSS.text() != '':
            try:
                global_element.ESG_DUT_loss_file = self.lineEdit_ESGLOSS.text()
                global_element.ESG_DUT_loss = global_element.xml_to_dict(self.lineEdit_ESGLOSS.text())
            except:
                win32api.MessageBox(0, 'ESG -> DUT path loss file error!')
                global_element.ESG_DUT_loss_file = ''
                global_element.ESG_DUT_loss = {}
        else:
            global_element.ESG_DUT_loss_file = ''
            global_element.ESG_DUT_loss = {}
        self.close()


class aboutWindow(QMainWindow, UI_about.Ui_Window_about):
    """
        about me界面
    """
    def __init__(self, parent=None):
        super(aboutWindow, self).__init__(parent)
        self.setupUi(self)

        # 设置为模拟对话框，阻塞上一层窗口
        self.setWindowModality(Qt.ApplicationModal)


class LteChannelEditorWin(QMainWindow, UI_Frequency_Editor.Ui_Frequency_Editor_Window):
    """
        about me界面
    """
    def __init__(self, parent=None):
        super(LteChannelEditorWin, self).__init__(parent)
        self.setupUi(self)

        self.initingintance()

        # 设置为模拟对话框，阻塞上一层窗口
        self.setWindowModality(Qt.ApplicationModal)

        self.pushButton_save.clicked.connect(self.savefunc)
        self.pushButton_default.clicked.connect(self.defaultfunc)
        self.pushButton_cancel.clicked.connect(self.cancelfunc)

    def initingintance(self):
        self.tableWidget_1_4.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 自适应水平宽度
        self.tableWidget_1_4.horizontalHeader().setStyleSheet('QHeaderView::section{background:lightblue;}')
        self.tableWidget_1_4.verticalHeader().setStyleSheet('QHeaderView::section{background:lightblue;}')

        self.tableWidget_3.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 自适应水平宽度
        self.tableWidget_3.horizontalHeader().setStyleSheet('QHeaderView::section{background:lightblue;}')
        self.tableWidget_3.verticalHeader().setStyleSheet('QHeaderView::section{background:lightblue;}')

        self.tableWidget_5.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 自适应水平宽度
        self.tableWidget_5.horizontalHeader().setStyleSheet('QHeaderView::section{background:lightblue;}')
        self.tableWidget_5.verticalHeader().setStyleSheet('QHeaderView::section{background:lightblue;}')

        self.tableWidget_10.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 自适应水平宽度
        self.tableWidget_10.horizontalHeader().setStyleSheet('QHeaderView::section{background:lightblue;}')
        self.tableWidget_10.verticalHeader().setStyleSheet('QHeaderView::section{background:lightblue;}')

        self.tableWidget_15.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 自适应水平宽度
        self.tableWidget_15.horizontalHeader().setStyleSheet('QHeaderView::section{background:lightblue;}')
        self.tableWidget_15.verticalHeader().setStyleSheet('QHeaderView::section{background:lightblue;}')

        self.tableWidget_20.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 自适应水平宽度
        self.tableWidget_20.horizontalHeader().setStyleSheet('QHeaderView::section{background:lightblue;}')
        self.tableWidget_20.verticalHeader().setStyleSheet('QHeaderView::section{background:lightblue;}')

        for i in range(43):
            self.tableWidget_1_4.item(i, 1).setText(global_element.lte_channel_fortest_dict['1.4MHz'][global_element.list_lte_band[i]])
            self.tableWidget_3.item(i, 1).setText(global_element.lte_channel_fortest_dict['3MHz'][global_element.list_lte_band[i]])
            self.tableWidget_5.item(i, 1).setText(global_element.lte_channel_fortest_dict['5MHz'][global_element.list_lte_band[i]])
            self.tableWidget_10.item(i, 1).setText(global_element.lte_channel_fortest_dict['10MHz'][global_element.list_lte_band[i]])
            self.tableWidget_15.item(i, 1).setText(global_element.lte_channel_fortest_dict['15MHz'][global_element.list_lte_band[i]])
            self.tableWidget_20.item(i, 1).setText(global_element.lte_channel_fortest_dict['20MHz'][global_element.list_lte_band[i]])

    def savefunc(self):
        dict_1_4 = {}
        dict_3 = {}
        dict_5 = {}
        dict_10 = {}
        dict_15 = {}
        dict_20 = {}
        for i in range(43):                       # 遍历lte channel编辑表格控件的第2列
            dict_1_4[self.tableWidget_1_4.item(i, 0).text()] = self.tableWidget_1_4.item(i, 1).text()
            dict_3[self.tableWidget_3.item(i, 0).text()] = self.tableWidget_3.item(i, 1).text()
            dict_5[self.tableWidget_5.item(i, 0).text()] = self.tableWidget_5.item(i, 1).text()
            dict_10[self.tableWidget_10.item(i, 0).text()] = self.tableWidget_10.item(i, 1).text()
            dict_15[self.tableWidget_15.item(i, 0).text()] = self.tableWidget_15.item(i, 1).text()
            dict_20[self.tableWidget_20.item(i, 0).text()] = self.tableWidget_20.item(i, 1).text()

        global_element.lte_channel_fortest_dict['1.4MHz'] = dict_1_4
        global_element.lte_channel_fortest_dict['3MHz'] = dict_3
        global_element.lte_channel_fortest_dict['5MHz'] = dict_5
        global_element.lte_channel_fortest_dict['10MHz'] = dict_10
        global_element.lte_channel_fortest_dict['15MHz'] = dict_15
        global_element.lte_channel_fortest_dict['20MHz'] = dict_20

        # print(global_element.lte_channel_fortest_dict)

        self.close()

    def defaultfunc(self):
        for i in range(43):
            self.tableWidget_1_4.item(i, 1).setText(
                global_element.lte_channel_default_dict['1.4MHz'][global_element.list_lte_band[i]])
            self.tableWidget_3.item(i, 1).setText(
                global_element.lte_channel_default_dict['3MHz'][global_element.list_lte_band[i]])
            self.tableWidget_5.item(i, 1).setText(
                global_element.lte_channel_default_dict['5MHz'][global_element.list_lte_band[i]])
            self.tableWidget_10.item(i, 1).setText(
                global_element.lte_channel_default_dict['10MHz'][global_element.list_lte_band[i]])
            self.tableWidget_15.item(i, 1).setText(
                global_element.lte_channel_default_dict['15MHz'][global_element.list_lte_band[i]])
            self.tableWidget_20.item(i, 1).setText(
                global_element.lte_channel_default_dict['20MHz'][global_element.list_lte_band[i]])

    def cancelfunc(self):
        self.close()


class LtecaChannelEditorWin(QMainWindow, UI_CA_Frequency_Editor.Ui_MainWindow_CA_Freq_Editor):
    """
        LTE CA Channel editor界面
    """
    def __init__(self, parent=None):
        super(LtecaChannelEditorWin, self).__init__(parent)
        self.setupUi(self)

        self.initingintance()

        # 设置为模拟对话框，阻塞上一层窗口
        self.setWindowModality(Qt.ApplicationModal)

        self.pushButton_ok.clicked.connect(self.savefunc)
        self.pushButton_setdefaultvalue.clicked.connect(self.defaultfunc)

    def initingintance(self):
        table_list = [self.tableWidget_2C, self.tableWidget_5B, self.tableWidget_7C, self.tableWidget_12B,
                      self.tableWidget_38C, self.tableWidget_41C]
        table_title_list = ['CA_2C', 'CA_5B', 'CA_7C', 'CA_12B', 'CA_38C', 'CA_41C']
        for i in range(len(table_list)):
            table_list[i].horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 自适应水平宽度
            table_list[i].horizontalHeader().setStyleSheet('QHeaderView::section{background:lightblue;}')
            table_list[i].verticalHeader().setStyleSheet('QHeaderView::section{background:lightblue;}')

            table_row_count = len(global_element.lte_ca_channel_fortest_dict[table_title_list[i]])
            table_list[i].setRowCount(table_row_count)

            j = 0
            for key, value in enumerate(global_element.lte_ca_channel_fortest_dict[table_title_list[i]]):
                item_bw = QtWidgets.QTableWidgetItem()
                item_bw.setText(value)
                table_list[i].setItem(j, 0, item_bw)

                item_channel = QtWidgets.QTableWidgetItem()
                item_channel.setText(global_element.lte_ca_channel_fortest_dict[table_title_list[i]][value])
                table_list[i].setItem(j, 1, item_channel)

                j += 1

    def savefunc(self):
        dict_2C = {}
        dict_5B = {}
        dict_7C = {}
        dict_12B = {}
        dict_38C = {}
        dict_41C = {}
        table_list = [self.tableWidget_2C, self.tableWidget_5B, self.tableWidget_7C, self.tableWidget_12B,
                      self.tableWidget_38C, self.tableWidget_41C]
        table_title_list = ['CA_2C', 'CA_5B', 'CA_7C', 'CA_12B', 'CA_38C', 'CA_41C']
        for i in range(len(table_list)):
            row_count = table_list[i].rowCount()
            for j in range(row_count):
                if table_title_list[i] == 'CA_2C':
                    dict_2C[table_list[i].item(j, 0).text()] = table_list[i].item(j, 1).text()
                elif table_title_list[i] == 'CA_5B':
                    dict_5B[table_list[i].item(j, 0).text()] = table_list[i].item(j, 1).text()
                elif table_title_list[i] == 'CA_7C':
                    dict_7C[table_list[i].item(j, 0).text()] = table_list[i].item(j, 1).text()
                elif table_title_list[i] == 'CA_12B':
                    dict_12B[table_list[i].item(j, 0).text()] = table_list[i].item(j, 1).text()
                elif table_title_list[i] == 'CA_38C':
                    dict_38C[table_list[i].item(j, 0).text()] = table_list[i].item(j, 1).text()
                elif table_title_list[i] == 'CA_41C':
                    dict_41C[table_list[i].item(j, 0).text()] = table_list[i].item(j, 1).text()

        global_element.lte_ca_channel_fortest_dict['CA_2C'] = dict_2C
        global_element.lte_ca_channel_fortest_dict['CA_5B'] = dict_5B
        global_element.lte_ca_channel_fortest_dict['CA_7C'] = dict_7C
        global_element.lte_ca_channel_fortest_dict['CA_12B'] = dict_12B
        global_element.lte_ca_channel_fortest_dict['CA_38C'] = dict_38C
        global_element.lte_ca_channel_fortest_dict['CA_41C'] = dict_41C

        self.close()

    def defaultfunc(self):
        table_list = [self.tableWidget_2C, self.tableWidget_5B, self.tableWidget_7C, self.tableWidget_12B,
                      self.tableWidget_38C, self.tableWidget_41C]
        table_title_list = ['CA_2C', 'CA_5B', 'CA_7C', 'CA_12B', 'CA_38C', 'CA_41C']
        for i in range(len(table_list)):
            j = 0
            for index, key in enumerate(global_element.lte_ca_channel_default_dict[table_title_list[i]]):
                table_list[i].item(j, 0).setText(key)
                table_list[i].item(j, 1).setText(global_element.lte_ca_channel_default_dict[table_title_list[i]][key])
                j += 1


class ReportToolWindow(QMainWindow, UI_report_tool.Ui_Window_report_tool):
    """
        报告处理界面
        构建报告处理界面的逻辑，通过此类可构建报告处理界面实例
    """
    def __init__(self, parent=None):
        super(ReportToolWindow, self).__init__(parent)
        self.setupUi(self)

        self.report_thread = reporthandle_Thread()

        self.cwd = 'Report/'

        # 设置为模拟对话框，阻塞上一层窗口
        self.setWindowModality(Qt.ApplicationModal)

        # 建立信号槽关系
        self.pushButton_scandatesource.clicked.connect(self.scandateclick)
        self.pushButton_scanreportadd.clicked.connect(self.scanreportaddr)
        self.pushButton_cancel.clicked.connect(self.cancelclicked)
        self.pushButton_creatreport.clicked.connect(self.creatrpbtnclicked)
        self.report_thread.finished.connect(self.finishedhandle)

        global_element.reporthandle_dict = {}

    # 定义scan date source槽函数
    def scandateclick(self):
        fileName_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                'Select data to be processed',
                                                                self.cwd,
                                                                'IORI Report Files (*.xlsx);;All Files (*)')
        if fileName_choose != '':
            self.lineEdit_datesource.setText(fileName_choose)

    # 定义scan report address槽函数
    def scanreportaddr(self):
        fileName_choose, filetype = QFileDialog.getSaveFileName(self,
                                                                'Save word reports',
                                                                self.cwd,
                                                                'IORI Report Files (*.docx);;All Files (*)')

        if fileName_choose != '':
            self.lineEdit_reportadd.setText(fileName_choose)

    # 定义cancel按钮clicked的槽函数
    def cancelclicked(self):
        global_element.reporthandle_dict = {}
        self.close()

    # 定义creat report按钮clicked的槽函数
    def creatrpbtnclicked(self):
        # 将用户定义的信息更新进字典
        global_element.reporthandle_dict['objectname'] = self.lineEdit_objectname.text()
        global_element.reporthandle_dict['testedby'] = self.comboBox_testedby.currentText()
        global_element.reporthandle_dict['grantno'] = self.lineEdit_grantNo.text()
        global_element.reporthandle_dict['reportno'] = self.lineEdit_reportNo.text()
        global_element.reporthandle_dict['dateofrec'] = self.dateEdit_receipt.text()
        global_element.reporthandle_dict['dateofstart'] = self.dateEdit_teststart.text()
        global_element.reporthandle_dict['dateofstop'] = self.dateEdit_teststop.text()
        global_element.reporthandle_dict['dateofissue'] = self.dateEdit_issue.text()
        global_element.reporthandle_dict['datasource'] = self.lineEdit_datesource.text()
        global_element.reporthandle_dict['reportaddr'] = self.lineEdit_reportadd.text()
        global_element.reporthandle_dict['checkgsm'] = self.checkBox_gsmfcc.checkState()
        global_element.reporthandle_dict['checkwcdma'] = self.checkBox_wcdmafcc.checkState()
        global_element.reporthandle_dict['checklte'] = self.checkBox_ltefcc.checkState()
        global_element.reporthandle_dict['brand'] = self.lineEdit_brand.text()
        global_element.reporthandle_dict['producttype'] = self.lineEdit_producttype.text()
        global_element.reporthandle_dict['brandaddr'] = self.lineEdit_brandaddr.text()
        global_element.reporthandle_dict['hwversion'] = self.lineEdit_hwversion.text()
        global_element.reporthandle_dict['swversion'] = self.lineEdit_swversion.text()

        time.sleep(0.2)

        self.report_thread.start()      # 开始处理报告的进程

        self.setEnabled(False)

    # 定义线程完成后的槽函数
    def finishedhandle(self):
        self.setEnabled(True)


class test_Thread(QThread):
    """
        线程类，界面窗口处理耗时任务时另开一个线程，防止耗时任务卡死界面(测试进程)
    """
    handle = -1

    def __init__(self):
        super(test_Thread, self).__init__()

    def run(self):
        try:
            self.handle = ctypes.windll.kernel32.OpenThread(win32con.PROCESS_ALL_ACCESS, False,
                                                            int(QThread.currentThreadId()))
        except:
            pass

        Start_Project.start_test()


class reporthandle_Thread(QThread):
    """
        线程类，界面窗口处理耗时任务时另开一个线程，防止耗时任务卡死界面（处理report进程）
    """
    handle = -1

    def __init__(self):
        super(reporthandle_Thread, self).__init__()

    def run(self):
        try:
            self.handle = ctypes.windll.kernel32.OpenThread(win32con.PROCESS_ALL_ACCESS, False,
                                                            int(QThread.currentThreadId()))
        except:
            pass

        report_handle.fccreporthandle()
