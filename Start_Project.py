# !/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Author    : Feng Zhaohui
# @Time      : 2019/2/22
# @File      : Start_Project.py
# @Funcyusa  :
# @Version   : 1.0


import sys
from PyQt5.QtWidgets import QApplication
from gui import Init_UI
import global_element
from Equipments import Equipments
import testseq_handle
# from PyQt5.QtWidgets import QSplashScreen, QLabel
# from PyQt5 import QtGui
# from PyQt5.QtCore import Qt
# import time


def start_test():
    """
        测试线程处理的主函数，处理整个测试过程
    :return:
    """

    global_element.finished_result_list = [0, 0, 0]
    global_element.emitsingle.process_rateupdataSingle.emit('0')
    global_element.finished_step = 0
    global_element.IsStop = False
    global_element.checkdeviceenable()                          # 检查是否有勾选仪器
    global_element.checklossfileselected()                      # 检查是否有选择线损文件
    global_element.checkreportpath()                            # 检查报告路径
    global_element.checkdutactive()                             # 检查是否有激活的DUT
    global_element.checktestseq()                               # 检查测试序列中是否有内容

    # 计算测试步骤，用于更新进度条
    global_element.total_step = global_element.calc_total_step()
    #
    Equipments.init_devices_checked()                           # 初始化已勾选的设备（根据地址实例化，以便测试时调用）

    testseq_handle.testseqhandle()                             # 处理测试序列

    # global_element.SA_intance.close()
    # global_element.CU_intance.close()


def main():
    """
        主函数
    :return:
    """
    app = QApplication(sys.argv)
    # splash = QSplashScreen(QtGui.QPixmap('./image/feiji.GIF'))
    # splash.show()
    # font = QtGui.QFont()
    # font.setPointSize(16)
    # font.setBold(True)
    # font.setWeight(75)
    # splash.setFont(font)
    # if True:
    #     splash.showMessage('>>>', Qt.AlignBottom, Qt.red)
    #     time.sleep(0.2)
    #     splash.showMessage('>>>>>>', Qt.AlignBottom, Qt.red)
    #     time.sleep(0.2)
    #     splash.showMessage('>>>>>>>>>', Qt.AlignBottom, Qt.red)
    #     time.sleep(0.2)
    #     splash.showMessage('>>>>>>>>>>>>', Qt.AlignBottom, Qt.red)
    #     time.sleep(0.2)
    # app.processEvents()

    myfirstwin_example = Init_UI.MyFirstWindow()
    myfirstwin_example.show()
    # splash.finish(myfirstwin_example)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
