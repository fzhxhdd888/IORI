# !/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Author    : Feng Zhaohui
# @Time      : 2019/6/26
# @File      : WLAN_N.py
# @Funcyusa  :
# @Version   : 1.0

import global_element
import testseq_handle
import report_handle
import time
import os


def initseting(init_parms_list):
    """
    WLANB模块initing的处理
    :param init_parms_list:
    :return:
    """
    # 更新测试band信息到全局变量
    global_element.Test_Antenna = init_parms_list[0]['Value']

    # 更新Datarate信息到全局变量
    global_element.Test_Datarate = init_parms_list[1]['Value']

    # 更新Channel信息到全局变量
    channel_str = init_parms_list[2]['Value']
    channel_str_list = testseq_handle.channelstrtolist(channel_str)  # 将所有信道整理成字符串列表的形式

    return channel_str_list
