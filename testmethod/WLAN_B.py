# !/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Author    : Feng Zhaohui
# @Time      : 2019/6/26
# @File      : WLAN_B.py
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


def Adjacentchannelrejection(testitem):
    global_element.emitsingle.stateupdataSingle.emit('Testing in progress of Adjacentchannelrejection channel ' +
                                                     global_element.Test_channel)

    # 设置WLAN 信令LOSS
    channel_fre = report_handle.fre_wlan_calc(global_element.Test_channel)
    global_element.CU_intance.set_wlan_loss(channel_fre)

    if global_element.Test_Datarate == '1' or global_element.Test_Datarate == '2':
        offset_freq = 30
        gprf_level = -39
        bs_power = -74
    elif global_element.Test_Datarate == '5.5' or global_element.Test_Datarate == '11':
        offset_freq = 25
        gprf_level = -35
        bs_power = -70

    if eval(channel_fre) + offset_freq > 2472:
        gprf_freq = eval(channel_fre) - offset_freq
    else:
        gprf_freq = eval(channel_fre) + offset_freq

    if global_element.Test_Datarate != '5.5':
        wavefilename = global_element.Test_Datarate + 'M'
    else:
        wavefilename = '5M'

    global_element.CU_intance.init_generator(str(gprf_freq), str(gprf_level), wavefilename)

    global_element.CU_intance.set_wlan_bslevel(str(bs_power))

    # 取值
    packets_num = testitem['parms']['Parm'][0]['Value']
    per_result = global_element.CU_intance.get_wlan_per(packets_num)

    global_element.emitsingle.stateupdataSingle.emit(global_element.Test_channel + ' per_result:' + per_result)

    global_element.CU_intance.off_gprf()


