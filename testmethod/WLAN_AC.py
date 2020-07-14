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

    global_element.Test_wlan_bw = init_parms_list[3]['Value']

    if global_element.Test_wlan_bw == 'VHT20':
        channel_str = init_parms_list[4]['Value']
    elif global_element.Test_wlan_bw == 'VHT40':
        channel_str = init_parms_list[5]['Value']
    elif global_element.Test_wlan_bw == 'VHT80':
        channel_str = init_parms_list[6]['Value']

    channel_str_list = testseq_handle.channelstrtolist(channel_str)

    return channel_str_list


def Adjacentchannelrejection(testitem):
    global_element.emitsingle.stateupdataSingle.emit('Testing in progress of Adjacentchannelrejection channel ' +
                                                     global_element.Test_channel)

    global_element.Test_item = '21.3.18.2_Adjacent channel rejection'

    # 设置WLAN 信令LOSS
    channel_fre = report_handle.fre_wlan_calc(global_element.Test_channel)
    global_element.CU_intance.set_wlan_loss(channel_fre)

    level_list = [-82, -79, -77, -74, -70, -66, -65, -64, -59, -57]
    limit_list = []
    for limit in testitem['limits']['limit']:
        limit_list.append(limit['low'])

    if global_element.Test_wlan_bw == 'VHT20':
        bs_level = str(level_list[eval(global_element.Test_Datarate[-1:])] + 3)
        offset_freq = 20
        gprf_level = str(int(bs_level) + int(limit_list[int(global_element.Test_Datarate[-1:])]))
    elif global_element.Test_wlan_bw == 'VHT40':
        bs_level = str(level_list[eval(global_element.Test_Datarate[-1:])] + 6)
        offset_freq = 40
        gprf_level = str(int(bs_level) + int(limit_list[int(global_element.Test_Datarate[-1:])]))
    elif global_element.Test_wlan_bw == 'VHT80':
        bs_level = str(level_list[eval(global_element.Test_Datarate[-1:])] + 9)
        offset_freq = 80
        gprf_level = str(int(bs_level) + int(limit_list[int(global_element.Test_Datarate[-1:])]))

    half_obw = eval(global_element.Test_wlan_bw[-2:]) / 2
    if (5170 + half_obw) < eval(channel_fre) + offset_freq < (5330 - half_obw)\
            or (5490 + half_obw) < eval(channel_fre) + offset_freq < (5710 - half_obw) \
            or (5735 + half_obw) < eval(channel_fre) + offset_freq < (5835 - half_obw):
        gprf_freq = eval(channel_fre) + offset_freq
    else:
        gprf_freq = eval(channel_fre) - offset_freq

    wavefilename = 'AC_' + global_element.Test_Datarate + '_' + global_element.Test_wlan_bw

    global_element.CU_intance.init_generator(str(gprf_freq), str(gprf_level), wavefilename)

    global_element.CU_intance.set_wlan_bslevel(str(bs_level))

    # 取值
    packets_num = testitem['parms']['Parm'][0]['Value']
    per_result, packets_done = global_element.CU_intance.get_wlan_per(packets_num)

    global_element.Test_remark = 'Uint: %, ' + str(packets_done) + ' packests transmited!'
    high_limit = '10'
    low_limit = 'None'
    report_handle.Reporttool(per_result, low_limit, high_limit)

    global_element.CU_intance.off_gprf()


def NoAdjacentchannelrejection(testitem):
    global_element.emitsingle.stateupdataSingle.emit('Testing in progress of No Adjacentchannelrejection channel ' +
                                                     global_element.Test_channel)
    global_element.Test_item = '21.3.18.3_NO Adjacent channel rejection'

    # 设置WLAN 信令LOSS
    channel_fre = report_handle.fre_wlan_calc(global_element.Test_channel)
    global_element.CU_intance.set_wlan_loss(channel_fre)

    level_list = [-82, -79, -77, -74, -70, -66, -65, -64, -59, -57]
    limit_list = []
    for limit in testitem['limits']['limit']:
        limit_list.append(limit['low'])

    if global_element.Test_wlan_bw == 'VHT20':
        bs_level = str(level_list[eval(global_element.Test_Datarate[-1:])] + 3)
        offset_freq = 40
        gprf_level = str(int(bs_level) + int(limit_list[int(global_element.Test_Datarate[-1:])]))
    elif global_element.Test_wlan_bw == 'VHT40':
        bs_level = str(level_list[eval(global_element.Test_Datarate[-1:])] + 6)
        offset_freq = 80
        gprf_level = str(int(bs_level) + int(limit_list[int(global_element.Test_Datarate[-1:])]))
    elif global_element.Test_wlan_bw == 'VHT80':
        bs_level = str(level_list[eval(global_element.Test_Datarate[-1:])] + 9)
        offset_freq = 160
        gprf_level = str(int(bs_level) + int(limit_list[int(global_element.Test_Datarate[-1:])]))

    half_obw = eval(global_element.Test_wlan_bw[-2:]) / 2
    if (5170 + half_obw) < eval(channel_fre) + offset_freq < (5330 - half_obw)\
            or (5490 + half_obw) < eval(channel_fre) + offset_freq < (5710 - half_obw) \
            or (5735 + half_obw) < eval(channel_fre) + offset_freq < (5835 - half_obw):
        gprf_freq = eval(channel_fre) + offset_freq
    else:
        gprf_freq = eval(channel_fre) - offset_freq

    wavefilename = 'AC_' + global_element.Test_Datarate + '_' + global_element.Test_wlan_bw

    global_element.CU_intance.init_generator(str(gprf_freq), str(gprf_level), wavefilename)

    global_element.CU_intance.set_wlan_bslevel(str(bs_level))

    # 取值
    packets_num = testitem['parms']['Parm'][0]['Value']
    per_result, packets_done = global_element.CU_intance.get_wlan_per(packets_num)

    global_element.Test_remark = 'Uint: %, ' + str(packets_done) + ' packests transmited!'
    high_limit = '10'
    low_limit = 'None'
    report_handle.Reporttool(per_result, low_limit, high_limit)

    global_element.CU_intance.off_gprf()


