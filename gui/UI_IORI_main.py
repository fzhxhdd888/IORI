# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_IORI_main.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ui_IORI(object):
    def setupUi(self, ui_IORI):
        ui_IORI.setObjectName("ui_IORI")
        ui_IORI.resize(1093, 840)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./image/me.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ui_IORI.setWindowIcon(icon)
        ui_IORI.setIconSize(QtCore.QSize(32, 32))
        print(type(ui_IORI))
        ui_IORI.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.centralwidget = QtWidgets.QWidget(ui_IORI)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(5, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMinimumSize(QtCore.QSize(10, 0))
        font = QtGui.QFont()
        font.setFamily("Arial Unicode MS")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("./image/dut.ico"))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.label_dut = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_dut.sizePolicy().hasHeightForWidth())
        self.label_dut.setSizePolicy(sizePolicy)
        self.label_dut.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_dut.setFont(font)
        self.label_dut.setText("")
        self.label_dut.setObjectName("label_dut")
        self.horizontalLayout.addWidget(self.label_dut)
        spacerItem1 = QtWidgets.QSpacerItem(5, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout_6.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem2 = QtWidgets.QSpacerItem(5, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial Narrow")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.tabWidget.setFont(font)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_4.addWidget(self.label_3)
        self.tableWidget_testseq = QtWidgets.QTableWidget(self.tab)
        self.tableWidget_testseq.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_testseq.setObjectName("tableWidget_testseq")
        self.tableWidget_testseq.setColumnCount(5)
        self.tableWidget_testseq.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_testseq.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_testseq.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_testseq.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setBackground(QtGui.QColor(255, 255, 255))
        self.tableWidget_testseq.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setBackground(QtGui.QColor(253, 253, 253))
        self.tableWidget_testseq.setHorizontalHeaderItem(4, item)
        self.tableWidget_testseq.horizontalHeader().setHighlightSections(True)
        self.verticalLayout_4.addWidget(self.tableWidget_testseq)
        self.verticalLayout_5.addLayout(self.verticalLayout_4)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.textBrowser_status = QtWidgets.QTextBrowser(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser_status.sizePolicy().hasHeightForWidth())
        self.textBrowser_status.setSizePolicy(sizePolicy)
        self.textBrowser_status.setMinimumSize(QtCore.QSize(0, 0))
        self.textBrowser_status.setObjectName("textBrowser_status")
        self.verticalLayout_3.addWidget(self.textBrowser_status)
        self.horizontalLayout_6.addLayout(self.verticalLayout_3)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_6.addLayout(self.gridLayout)
        self.verticalLayout_5.addLayout(self.horizontalLayout_6)
        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tab_3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem3 = QtWidgets.QSpacerItem(5, 17, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem4 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem4)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem5)
        self.label_5 = QtWidgets.QLabel(self.tab_3)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_5.addWidget(self.label_5)
        self.comboBox = QtWidgets.QComboBox(self.tab_3)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout_5.addWidget(self.comboBox)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.tableWidget_logs = QtWidgets.QTableWidget(self.tab_3)
        self.tableWidget_logs.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_logs.setObjectName("tableWidget_logs")
        self.tableWidget_logs.setColumnCount(18)
        self.tableWidget_logs.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_logs.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_logs.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_logs.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_logs.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_logs.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_logs.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_logs.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_logs.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_logs.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_logs.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_logs.setHorizontalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_logs.setHorizontalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_logs.setHorizontalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_logs.setHorizontalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_logs.setHorizontalHeaderItem(14, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_logs.setHorizontalHeaderItem(15, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_logs.setHorizontalHeaderItem(16, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_logs.setHorizontalHeaderItem(17, item)
        self.verticalLayout.addWidget(self.tableWidget_logs)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        spacerItem6 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem6)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        spacerItem7 = QtWidgets.QSpacerItem(5, 17, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem7)
        self.tabWidget.addTab(self.tab_3, "")
        self.horizontalLayout_4.addWidget(self.tabWidget)
        spacerItem8 = QtWidgets.QSpacerItem(5, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem8)
        self.verticalLayout_6.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(100, 0))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setMinimumSize(QtCore.QSize(0, 1))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_3.addWidget(self.progressBar)
        self.verticalLayout_6.addLayout(self.horizontalLayout_3)
        ui_IORI.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ui_IORI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1093, 23))
        self.menubar.setObjectName("menubar")
        self.menuDevices_Config = QtWidgets.QMenu(self.menubar)
        self.menuDevices_Config.setObjectName("menuDevices_Config")
        self.menuDUT = QtWidgets.QMenu(self.menubar)
        self.menuDUT.setObjectName("menuDUT")
        self.menuProject = QtWidgets.QMenu(self.menubar)
        self.menuProject.setObjectName("menuProject")
        self.menuSystem = QtWidgets.QMenu(self.menubar)
        self.menuSystem.setObjectName("menuSystem")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuTest_Plan = QtWidgets.QMenu(self.menubar)
        self.menuTest_Plan.setObjectName("menuTest_Plan")
        self.menuReport = QtWidgets.QMenu(self.menubar)
        self.menuReport.setObjectName("menuReport")
        self.menuCalibration = QtWidgets.QMenu(self.menubar)
        self.menuCalibration.setObjectName("menuCalibration")
        ui_IORI.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ui_IORI)
        self.statusbar.setObjectName("statusbar")
        ui_IORI.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(ui_IORI)
        self.toolBar.setIconSize(QtCore.QSize(25, 25))
        self.toolBar.setObjectName("toolBar")
        ui_IORI.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionDevices_Config = QtWidgets.QAction(ui_IORI)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("./image/device.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDevices_Config.setIcon(icon1)
        self.actionDevices_Config.setObjectName("actionDevices_Config")
        self.actionDUT_Editor = QtWidgets.QAction(ui_IORI)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("./image/dut.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDUT_Editor.setIcon(icon2)
        self.actionDUT_Editor.setObjectName("actionDUT_Editor")
        self.actionStart = QtWidgets.QAction(ui_IORI)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("./image/start.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionStart.setIcon(icon3)
        self.actionStart.setObjectName("actionStart")
        self.actionPause = QtWidgets.QAction(ui_IORI)
        self.actionPause.setEnabled(False)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("./image/pause.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPause.setIcon(icon4)
        self.actionPause.setObjectName("actionPause")
        self.actionStop = QtWidgets.QAction(ui_IORI)
        self.actionStop.setEnabled(False)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("./image/stop.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionStop.setIcon(icon5)
        self.actionStop.setObjectName("actionStop")
        self.actionExit = QtWidgets.QAction(ui_IORI)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("./image/Exit.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon6)
        self.actionExit.setObjectName("actionExit")
        self.actionIORI_Help = QtWidgets.QAction(ui_IORI)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("./image/timg.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionIORI_Help.setIcon(icon7)
        self.actionIORI_Help.setObjectName("actionIORI_Help")
        self.actionAbout = QtWidgets.QAction(ui_IORI)
        self.actionAbout.setObjectName("actionAbout")
        self.actionTestseq = QtWidgets.QAction(ui_IORI)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("./image/seq.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionTestseq.setIcon(icon8)
        self.actionTestseq.setObjectName("actionTestseq")
        self.actionLoad_Test_Sequence = QtWidgets.QAction(ui_IORI)
        self.actionLoad_Test_Sequence.setIcon(icon8)
        self.actionLoad_Test_Sequence.setObjectName("actionLoad_Test_Sequence")
        self.actionReport_Config = QtWidgets.QAction(ui_IORI)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("./image/rep2.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionReport_Config.setIcon(icon9)
        self.actionReport_Config.setObjectName("actionReport_Config")
        self.actionUser_Define_Loss_File = QtWidgets.QAction(ui_IORI)
        self.actionUser_Define_Loss_File.setObjectName("actionUser_Define_Loss_File")
        self.actionSelect_Loss_File = QtWidgets.QAction(ui_IORI)
        self.actionSelect_Loss_File.setObjectName("actionSelect_Loss_File")
        self.actionLTE_Channel_Editor = QtWidgets.QAction(ui_IORI)
        self.actionLTE_Channel_Editor.setObjectName("actionLTE_Channel_Editor")
        self.actionReport_Tool = QtWidgets.QAction(ui_IORI)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/ico/rep2.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionReport_Tool.setIcon(icon10)
        self.actionReport_Tool.setObjectName("actionReport_Tool")
        self.actionLTE_CA_Channel_Editor = QtWidgets.QAction(ui_IORI)
        self.actionLTE_CA_Channel_Editor.setObjectName("actionLTE_CA_Channel_Editor")
        self.menuDevices_Config.addSeparator()
        self.menuDevices_Config.addAction(self.actionDevices_Config)
        self.menuDUT.addAction(self.actionDUT_Editor)
        self.menuProject.addAction(self.actionStart)
        self.menuProject.addAction(self.actionPause)
        self.menuProject.addAction(self.actionStop)
        self.menuSystem.addAction(self.actionExit)
        self.menuSystem.addAction(self.actionLTE_Channel_Editor)
        self.menuSystem.addAction(self.actionLTE_CA_Channel_Editor)
        self.menuHelp.addAction(self.actionIORI_Help)
        self.menuHelp.addAction(self.actionAbout)
        self.menuTest_Plan.addAction(self.actionTestseq)
        self.menuReport.addAction(self.actionReport_Config)
        self.menuReport.addAction(self.actionReport_Tool)
        self.menuCalibration.addAction(self.actionSelect_Loss_File)
        self.menuCalibration.addAction(self.actionUser_Define_Loss_File)
        self.menubar.addAction(self.menuSystem.menuAction())
        self.menubar.addAction(self.menuProject.menuAction())
        self.menubar.addAction(self.menuTest_Plan.menuAction())
        self.menubar.addAction(self.menuDUT.menuAction())
        self.menubar.addAction(self.menuReport.menuAction())
        self.menubar.addAction(self.menuCalibration.menuAction())
        self.menubar.addAction(self.menuDevices_Config.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionStart)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionPause)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionStop)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionDUT_Editor)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionTestseq)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionReport_Config)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionDevices_Config)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionIORI_Help)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionExit)

        self.retranslateUi(ui_IORI)
        self.tabWidget.setCurrentIndex(0)
        self.actionDevices_Config.triggered.connect(ui_IORI.Devices_Config_click_event)
        QtCore.QMetaObject.connectSlotsByName(ui_IORI)

    def retranslateUi(self, ui_IORI):
        _translate = QtCore.QCoreApplication.translate
        ui_IORI.setWindowTitle(_translate("ui_IORI", "IORI"))
        self.label_3.setText(_translate("ui_IORI", "Test Sequences:"))
        item = self.tableWidget_testseq.horizontalHeaderItem(0)
        item.setText(_translate("ui_IORI", "Test Case Name"))
        item = self.tableWidget_testseq.horizontalHeaderItem(1)
        item.setText(_translate("ui_IORI", "Judgement"))
        item = self.tableWidget_testseq.horizontalHeaderItem(2)
        item.setText(_translate("ui_IORI", "Start Time"))
        item = self.tableWidget_testseq.horizontalHeaderItem(3)
        item.setText(_translate("ui_IORI", "Stop Time"))
        item = self.tableWidget_testseq.horizontalHeaderItem(4)
        item.setText(_translate("ui_IORI", "Duration"))
        self.label_4.setText(_translate("ui_IORI", "Status:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("ui_IORI", "Overview"))
        self.label_5.setText(_translate("ui_IORI", "Select Mode:"))
        self.comboBox.setItemText(0, _translate("ui_IORI", "GSM"))
        self.comboBox.setItemText(1, _translate("ui_IORI", "WCDMA"))
        self.comboBox.setItemText(2, _translate("ui_IORI", "LTE"))
        self.comboBox.setItemText(3, _translate("ui_IORI", "BT2"))
        self.comboBox.setItemText(4, _translate("ui_IORI", "WLAN"))
        self.tableWidget_logs.setSortingEnabled(False)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("ui_IORI", "Logs"))
        self.label_2.setText(_translate("ui_IORI", "Rate of Progress:"))
        self.menuDevices_Config.setTitle(_translate("ui_IORI", "Devices Config"))
        self.menuDUT.setTitle(_translate("ui_IORI", "DUT"))
        self.menuProject.setTitle(_translate("ui_IORI", "Project"))
        self.menuSystem.setTitle(_translate("ui_IORI", "System"))
        self.menuHelp.setTitle(_translate("ui_IORI", "Help"))
        self.menuTest_Plan.setTitle(_translate("ui_IORI", "Test Plan"))
        self.menuReport.setTitle(_translate("ui_IORI", "Report"))
        self.menuCalibration.setTitle(_translate("ui_IORI", "Calibration"))
        self.toolBar.setWindowTitle(_translate("ui_IORI", "toolBar"))
        self.actionDevices_Config.setText(_translate("ui_IORI", "Devices Config"))
        self.actionDUT_Editor.setText(_translate("ui_IORI", "DUT Editor"))
        self.actionStart.setText(_translate("ui_IORI", "Start"))
        self.actionPause.setText(_translate("ui_IORI", "Pause"))
        self.actionStop.setText(_translate("ui_IORI", "Stop"))
        self.actionExit.setText(_translate("ui_IORI", "Exit"))
        self.actionIORI_Help.setText(_translate("ui_IORI", "IORI Help"))
        self.actionAbout.setText(_translate("ui_IORI", "About"))
        self.actionTestseq.setText(_translate("ui_IORI", "Test Plan Sequence"))
        self.actionLoad_Test_Sequence.setText(_translate("ui_IORI", "Load Test Sequence"))
        self.actionReport_Config.setText(_translate("ui_IORI", "Report Config"))
        self.actionUser_Define_Loss_File.setText(_translate("ui_IORI", "User Define Loss File"))
        self.actionSelect_Loss_File.setText(_translate("ui_IORI", "Select Loss File"))
        self.actionLTE_Channel_Editor.setText(_translate("ui_IORI", "LTE Channel Editor"))
        self.actionReport_Tool.setText(_translate("ui_IORI", "Report Tool"))
        self.actionLTE_CA_Channel_Editor.setText(_translate("ui_IORI", "LTE CA Channel Editor"))
# import rs_rc
