# !/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Author    : Feng Zhaohui
# @Time      : 2019/2/22
# @File      : testseq_handle.py
# @Funcyusa  :
# @Version   : 1.0

import global_element
from datetime import datetime
from testmethod import GSMFCC, WCDMAFCC, LTEFCC, WLAN_B, BT2FCC, LTECAFCC, WLAN_AC
import time
import report_handle


def testseqhandle():
    """
        处理test sequency：
        1. 更新全局变量：Test_type, Test_case, Test_temp, Test_volt
        2. 处理测试过程test sequency窗口内容的更新
        :return:
    """
    testseq = global_element.Testsequence_dict['seq']['items']
    for i in range(len(testseq)):
        global_element.current_index_seq = i                   # 更新目前测试seq的索引号
        # 停止功能函数接口

        enable = testseq[i]['@enable']
        if enable == 'yes':
            start_time = datetime.now()
            start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
            global_element.emitsingle.starttimeupdateSingle.emit(i, start_time_str)
            global_element.emitsingle.judgementupdataSingle.emit(i, 'Testing')
            condition = testseq[i]['@condition']

            # 初始化结果为空
            global_element.testseq_judgement_list = []

            # 更新test type   test case的值，用于生成报告时调用
            global_element.Test_type = testseq[i]['@name'].split(' ')[0]
            global_element.Test_case = testseq[i]['@name']
            global_element.emitsingle.stateupdataSingle.emit('Processing： %s' % global_element.Test_case)

            # 更新test temp   test volt的值，用于生成报告时调用
            if condition[:2] == 'NT':
                global_element.Test_temp = global_element.active_dut_dict['xml']['DUTCONFIG']['NT']
            elif condition[:2] == 'HT':
                global_element.Test_temp = global_element.active_dut_dict['xml']['DUTCONFIG']['HT']
            else:
                global_element.Test_temp = global_element.active_dut_dict['xml']['DUTCONFIG']['LT']

            if condition[-2:] == 'NV':
                global_element.Test_volt = global_element.active_dut_dict['xml']['DUTCONFIG']['NV']
            elif condition[-2:] == 'HV':
                global_element.Test_volt = global_element.active_dut_dict['xml']['DUTCONFIG']['HV']
            else:
                global_element.Test_volt = global_element.active_dut_dict['xml']['DUTCONFIG']['LV']

            # 停止功能函数接口

            global_element.emitsingle.stateupdataSingle.emit('Set the temperature to：%s℃，The voltage is：%sV' %
                                                             (global_element.Test_temp, global_element.Test_volt))

            # 处理testseq中的第i条testplan
            testplanhandle(i)

            # 停止功能函数接口

            # 测试完成第i条testplan后更新judgement
            if 'Not Applicable' in global_element.testseq_judgement_list or \
                    len(global_element.testseq_judgement_list) == 0:
                final_judgement = 'Not Applicable'
            elif 'Failed' in global_element.testseq_judgement_list:
                final_judgement = 'Failed'
            elif 'Inconclusive' in global_element.testseq_judgement_list and \
                    'Failed' not in global_element.testseq_judgement_list:
                final_judgement = 'Inconclusive'
            else:
                final_judgement = 'Passed'
            global_element.emitsingle.judgementupdataSingle.emit(i, final_judgement)

            # 测试完成第i条testplan后更新stop time
            stop_time = datetime.now()
            stop_time_str = stop_time.strftime('%Y-%m-%d %H:%M:%S')
            global_element.emitsingle.stoptimeupdateSingle.emit(i, stop_time_str)
            # 测试完成第i条testplan后更新测试用时
            time_delta_str = time_delta(start_time, stop_time)
            global_element.emitsingle.timedeltaupdataSingle.emit(i, time_delta_str)

            # 停止功能函数接口

            global_element.emitsingle.stateupdataSingle.emit('%s is completed!' % global_element.Test_case)

        else:
            global_element.emitsingle.judgementupdataSingle.emit(i, 'Skip')


def testplanhandle(i):
    """
        处理test sequency中第i条test plan
        :param i:
        :return:
    """
    current_testplan = global_element.Testsequence_dict['seq']['items'][i]['item']
    # 处理test plan中Initing
    if global_element.Test_type == 'GSMFCC':
        # 如里是GSMFCC模式，调用gsmfcc test plan处理方法
        gsmfcc_testplan_handle(current_testplan)
    elif global_element.Test_type == 'WCDMAFCC':
        # 如里是WCDMAFCC模式，调用wcdmafcc test plan处理方法
        wcdmafcc_testplan_handle(current_testplan)
    elif global_element.Test_type == 'LTEFCC':
        # 如果是LTEFCC模式，调用ltefcc test plan处理方法
        ltefcc_testplan_handle(current_testplan)
    elif global_element.Test_type == 'WLAN_B':
        # 如果是WLAN_B模式，调用WLAN_B test plan处理方法
        wlanb_testplan_handle(current_testplan)
    elif global_element.Test_type == 'BT2FCC':
        bt2fcc_testplan_handle(current_testplan)
    elif global_element.Test_type == 'LTECAFCC':
        ltecafcc_tesplan_handle(current_testplan)
    elif global_element.Test_type == 'WLAN_AC':
        wlanac_testplan_handle(current_testplan)



def time_delta(starttime, stoptime):
    """
        已知道开始时间和结束时间，得出以时分秒为格式的时间差（返回字符串格式）
        :param starttime:
        :param stoptime:
        :return:
    """
    time_delta = stoptime - starttime
    time_delta_sec = int(time_delta.total_seconds())
    hour_num = int(time_delta_sec / 3600)
    time_sec_remaining = time_delta_sec % 3600
    min_num = int(time_sec_remaining / 60)
    sec_num = time_sec_remaining % 60
    time_delta_str = '%dh %dm %ds' % (hour_num, min_num, sec_num)
    return time_delta_str


def channelstrtolist(channelstr):
    """
    将界面获取的信道或其它信息整理成列表
    :param channelstr:
    :return:
    """
    channel_list = []
    str_list = channelstr.split(',')
    for i in range(len(str_list)):
        if '-' not in str_list[i]:
            channel_list.append(str_list[i])
        else:
            if ';' not in str_list[i]:
                # print(str_list[i][:str_list[i].find('-')])
                # print(str_list[i][str_list[i].find('-') + 1:])
                list_channel = range(int(str_list[i][:str_list[i].find('-')]), int(str_list[i][str_list[i].find('-') + 1:]) + 1)
                for i in list_channel:
                    channel_list.append(str(i))
            else:
                start_channel = int(str_list[i][:str_list[i].find('-')])
                stop_channel = int(str_list[i][str_list[i].find('-') + 1:str_list[i].find(';')])
                step_channel = int(str_list[i][str_list[i].find(';') + 1:])
                list_channel_step = []
                list_channel_step.append(start_channel)
                channel_add_step = start_channel + step_channel
                while channel_add_step < stop_channel:
                    list_channel_step.append(channel_add_step)
                    channel_add_step += step_channel
                list_channel_step.append(stop_channel)
                for i in list_channel_step:
                    channel_list.append(str(i))

    return channel_list


def gsmfcc_testplan_handle(current_testplan):
    # 检测是否有SA和CU
    if global_element.devices_config_dict['xml']['CU']['CHECK'] == 'False' or global_element.devices_config_dict['xml']['SA']['CHECK'] == 'False':
        global_element.emitsingle.thread_exitSingle.emit('Test GSM FCC must have CU and SA!')
        time.sleep(0.1)

    # 检查DUT 控制方式
    if global_element.active_dut_dict['xml']['DUTCONFIG']['AUTOMODE'] not in ['1', '2', '3']:
        global_element.testseq_judgement_list.append('Inconclusive')
        global_element.emitsingle.stateupdataSingle.emit('To test GSM, please select the automatic control mode of DUT '
                                                         'in cellular mode.')
        return

    # 检测综测仪是否有GSM信令选件
    global_element.CU_intance.check_gsmsin_option()

    # 处理init seting，获取band, channel, pcl信息
    init_parms_list = current_testplan[0]['parms']['Parm']
    channel_str_list, pcl_str_list, mode_str = GSMFCC.initseting(init_parms_list)
    global_element.Test_modulation = mode_str

    # 如果是 GSM900 或 DCS1800，直接跳过测试（FCC不用测GSM900和DCS1800）
    if global_element.Test_band == 'GSM900' or global_element.Test_band == 'DCS1800':
        global_element.testseq_judgement_list.append('Not Applicable')
        return

    # 停止功能函数接口

    if mode_str == 'GSM':
        # 综测仪GSM信令的初始化设置
        result = global_element.CU_intance.gsmsin_init_setting()
        if result == False:
            global_element.testseq_judgement_list.append('Inconclusive')
            time.sleep(10)
            return

        # 停止功能函数接口

        # 开启DUT并等待DUT注册上CU
        issync = global_element.CU_intance.check_dut_issync()

        # 3次未能注册上则退出此条
        if issync == False:
            global_element.emitsingle.stateupdataSingle.emit('DUT registration failed!')
            global_element.testseq_judgement_list.append('Inconclusive')
            return

        time.sleep(2)

        # 成功注册后建立call
        # 停止功能函数接口
        isconnected = global_element.CU_intance.callsetup()

        # 如果没能建立call退出此条
        if isconnected == False:
            global_element.emitsingle.stateupdataSingle.emit('DUT failed to establish connection!')
            global_element.testseq_judgement_list.append('Inconclusive')
            return

        time.sleep(2)

        # 按channel列表循环处理
        for channel in channel_str_list:
            # 停止功能函数接口
            global_element.Test_channel = channel          # 更新全局变量channel
            global_element.CU_intance.set_gsm_channel(channel)     # 设置综测仪GSM channel
            # 按pcl列表循环处理
            for pcl in pcl_str_list:
                global_element.emitsingle.stateupdataSingle.emit('Channel：%s, PCL：%s' % (channel, pcl))
                global_element.Test_pcl = pcl              # 更新全局变量pcl
                global_element.CU_intance.set_gsm_pcl(pcl)     # 设置综测仪GSM pcl
                # 停止功能函数接口
                for testitem in current_testplan[1:]:
                    # 停止功能函数接口
                    if testitem['@enable'] == 'yes':
                        if testitem['@Name'] == 'Conducted output power':
                            GSMFCC.Conductedoutputpower(testitem, mode_str)
                        elif testitem['@Name'] == 'Peak-to-Average Ratio':
                            GSMFCC.peaktoaverageratio(testitem, mode_str)
                        elif testitem['@Name'] == '99% Occupied Bandwidth':
                            GSMFCC.pct99OccupiedBandwidth(testitem, mode_str)
                        elif testitem['@Name'] == '26dB Occupied Bandwidth':
                            GSMFCC.dB26OccupiedBandwidth(testitem, mode_str)
                        elif testitem['@Name'] == 'Band edge':
                            GSMFCC.Bandedge(testitem, mode_str)
                        elif testitem['@Name'] == 'Conducted Spurious emissions':
                            GSMFCC.ConductedSpuriousemissions(testitem, mode_str)
                        elif testitem['@Name'] == 'Frequency stability':
                            GSMFCC.Frequencystability(testitem, mode_str)
                        else:
                            pass

                        # # 更新进度
                        global_element.finished_step += 1
                        process_rate = format(global_element.finished_step * 100 / global_element.total_step, '.2f')
                        global_element.emitsingle.process_rateupdataSingle.emit(process_rate)
                        # 停止功能函数接口

                        # 更新summary
                        global_element.emitsingle.summaryupdataSingle.emit(global_element.finished_result_list)

    elif mode_str == 'GPRS' or mode_str == 'EGPRS':
        # 综测仪GPRS信令的初始化设置
        global_element.CU_intance.gprsfccsin_init_setting(mode_str)
        time.sleep(2)

        # 停止功能函数接口

        # 开启DUT并等待DUT注册上CU
        issync = global_element.CU_intance.check_dut_gprs_issync()

        # 3次未能注册上则退出此条
        if issync == False:
            global_element.emitsingle.stateupdataSingle.emit('DUT registration failed!')
            global_element.testseq_judgement_list.append('Inconclusive')
            return

        time.sleep(2)

        # 成功注册后建立数据连接
        # 停止功能函数接口
        isconnected = global_element.CU_intance.callsetup_gprs()

        # 如果没能建立数据连接退出此条
        if isconnected == False:
            global_element.emitsingle.stateupdataSingle.emit('DUT failed to establish connection!')
            global_element.testseq_judgement_list.append('Inconclusive')
            return

        time.sleep(2)

        # 按channel列表循环处理
        for channel in channel_str_list:
            # 停止功能函数接口
            global_element.Test_channel = channel  # 更新全局变量channel
            global_element.CU_intance.set_gprs_channel(channel)  # 设置综测仪GPRS channel
            # 按pcl列表循环处理
            for pcl in pcl_str_list:
                global_element.emitsingle.stateupdataSingle.emit('Channel：%s, PCL：%s' % (channel, pcl))
                global_element.Test_pcl = pcl  # 更新全局变量pcl
                global_element.CU_intance.set_gprs_pcl(pcl)  # 设置综测仪GPRS pcl
                # 停止功能函数接口
                for testitem in current_testplan[1:]:
                    # 停止功能函数接口
                    if testitem['@enable'] == 'yes':
                        if testitem['@Name'] == 'Conducted output power':
                            GSMFCC.Conductedoutputpower(testitem, mode_str)
                        elif testitem['@Name'] == 'Peak-to-Average Ratio':
                            GSMFCC.peaktoaverageratio(testitem, mode_str)
                        elif testitem['@Name'] == '99% Occupied Bandwidth':
                            GSMFCC.pct99OccupiedBandwidth(testitem, mode_str)
                        elif testitem['@Name'] == '26dB Occupied Bandwidth':
                            GSMFCC.dB26OccupiedBandwidth(testitem, mode_str)
                        elif testitem['@Name'] == 'Band edge':
                            GSMFCC.Bandedge(testitem, mode_str)
                        elif testitem['@Name'] == 'Conducted Spurious emissions':
                            GSMFCC.ConductedSpuriousemissions(testitem, mode_str)
                        elif testitem['@Name'] == 'Frequency stability':
                            GSMFCC.Frequencystability(testitem, mode_str)
                        else:
                            pass

                        # # 更新进度
                        global_element.finished_step += 1
                        process_rate = format(global_element.finished_step * 100 / global_element.total_step, '.2f')
                        global_element.emitsingle.process_rateupdataSingle.emit(process_rate)
                        # 停止功能函数接口

                        # 更新summary
                        global_element.emitsingle.summaryupdataSingle.emit(global_element.finished_result_list)


def wcdmafcc_testplan_handle(current_testplan):
    # 检测是否有SA和CU
    if global_element.devices_config_dict['xml']['CU']['CHECK'] == 'False' or \
            global_element.devices_config_dict['xml']['SA']['CHECK'] == 'False':
        global_element.emitsingle.thread_exitSingle.emit('Test WCDMA FCC must have CU and SA!')
        time.sleep(0.1)

    # 检查DUT 控制方式
    if global_element.active_dut_dict['xml']['DUTCONFIG']['AUTOMODE'] not in ['1', '2', '3']:
        global_element.testseq_judgement_list.append('Inconclusive')
        global_element.emitsingle.stateupdataSingle.emit(
            'To test WCDMA, please select the automatic control mode of DUT '
            'in cellular mode.')
        return

    # 检测综测仪是否有WCDMA信令选件
    global_element.CU_intance.check_wcdmasin_option()

    # 处理init seting，获取band, channel, pcl信息
    init_parms_list = current_testplan[0]['parms']['Parm']
    channel_str_list, mode_str = WCDMAFCC.initseting(init_parms_list)
    if mode_str == 'WCDMA':
        global_element.Test_modulation = 'RMC 12.2K'
    elif mode_str == 'HSDPA':
        global_element.Test_modulation = 'HSDPA'
    elif mode_str == 'HSUPA':
        global_element.Test_modulation = 'HSUPA'

    # 如果不是 band2, band4 或 band5，直接跳过测试（FCC只需要测这几个BAND）
    if global_element.Test_band != 'Band II' and global_element.Test_band != 'Band IV' \
            and global_element.Test_band != 'Band V':
        global_element.testseq_judgement_list.append('Not Applicable')
        return

    # 停止功能函数接口

    if mode_str == 'WCDMA':
        # 综测仪WCDMA信令的初始化设置
        global_element.CU_intance.wcdma_init_setting()
        time.sleep(0.1)

        # 停止功能函数接口

        # 开启DUT并等待DUT注册上CU
        issync = global_element.CU_intance.check_dut_issync_wcdma()

        # 3次未能注册上则退出此条
        if issync == False:
            global_element.emitsingle.stateupdataSingle.emit('DUT registration failed!')
            global_element.testseq_judgement_list.append('Inconclusive')
            return

        time.sleep(2)

        # 成功注册后建立数据连接
        # 停止功能函数接口
        isconnected = global_element.CU_intance.wcdmacallsetup()

        # 如果没能建立连接退出此条
        if isconnected == False:
            global_element.emitsingle.stateupdataSingle.emit('DUT failed to establish connection!')
            global_element.testseq_judgement_list.append('Inconclusive')
            return

        time.sleep(2)

        # 按channel列表循环处理
        for channel in channel_str_list:
            # 停止功能函数接口
            global_element.Test_channel = channel  # 更新全局变量channel
            global_element.CU_intance.set_wcdma_channel(channel)  # 设置综测仪wcdma channel
            time.sleep(3)

            for testitem in current_testplan[1:]:
                # 停止功能函数接口
                if testitem['@enable'] == 'yes':
                    if testitem['@Name'] == 'Conducted output power':
                        WCDMAFCC.Conductedoutputpower(testitem, mode_str)
                    elif testitem['@Name'] == 'Peak-to-Average Ratio':
                        WCDMAFCC.peaktoaverageratio(testitem, mode_str)
                    elif testitem['@Name'] == '99% Occupied Bandwidth':
                        WCDMAFCC.pct99OccupiedBandwidth(testitem, mode_str)
                    elif testitem['@Name'] == '26dB Occupied Bandwidth':
                        WCDMAFCC.dB26OccupiedBandwidth(testitem, mode_str)
                    elif testitem['@Name'] == 'Band edge':
                        WCDMAFCC.Bandedge(testitem, mode_str)
                    elif testitem['@Name'] == 'Conducted Spurious emissions':
                        WCDMAFCC.ConductedSpuriousemissions(testitem, mode_str)
                    elif testitem['@Name'] == 'Frequency stability':
                        WCDMAFCC.Frequencystability(testitem, mode_str)
                    else:
                        pass

                    # # 更新进度
                    global_element.finished_step += 1
                    process_rate = format(global_element.finished_step * 100 / global_element.total_step, '.2f')
                    global_element.emitsingle.process_rateupdataSingle.emit(process_rate)
                    # 停止功能函数接口

                    # 更新summary
                    global_element.emitsingle.summaryupdataSingle.emit(global_element.finished_result_list)

        global_element.CU_intance.wcdma_call_disconnect()


def ltefcc_testplan_handle(current_testplan):
    # 检测是否有SA和CU
    if global_element.devices_config_dict['xml']['CU']['CHECK'] == 'False' or \
            global_element.devices_config_dict['xml']['SA']['CHECK'] == 'False':
        global_element.emitsingle.thread_exitSingle.emit('Test LTE FCC must have CU and SA!')
        time.sleep(0.1)

    # 检查DUT 控制方式
    if global_element.active_dut_dict['xml']['DUTCONFIG']['AUTOMODE'] not in ['1', '2', '3']:
        global_element.testseq_judgement_list.append('Inconclusive')
        global_element.emitsingle.stateupdataSingle.emit(
            'To test LTE, please select the automatic control mode of DUT '
            'in cellular mode.')
        return

    # 检测综测仪是否有LTE信令选件
    result = global_element.CU_intance.check_ltesin_option()
    if result == False:
        global_element.emitsingle.stateupdataSingle.emit('The CU does not support LTE signaling mode')
        global_element.testseq_judgement_list.append('Inconclusive')
        return

    # 处理init seting，获取band, channel, BW信息
    init_parms_list = current_testplan[0]['parms']['Parm']
    channel_str_list = LTEFCC.initseting(init_parms_list)

    # 停止功能函数接口

    # 综测仪LTE信令的初始化设置
    result = global_element.CU_intance.lte_init_setting(channel_str_list)
    if result == False:
        global_element.emitsingle.stateupdataSingle.emit('Error in initializing LTE signaling parameters of CU!')
        global_element.testseq_judgement_list.append('Inconclusive')
        return
    time.sleep(0.1)

    # 停止功能函数接口

    # 开启DUT并等待DUT注册上CU
    issync = global_element.CU_intance.check_dut_issync_lte()

    # 3次未能注册上则退出此条
    if issync == False:
        global_element.emitsingle.stateupdataSingle.emit('DUT registration failed!')
        global_element.testseq_judgement_list.append('Inconclusive')
        return

    time.sleep(2)

    # 成功注册后建立数据连接
    # 停止功能函数接口
    isconnected = global_element.CU_intance.ltecallsetup()

    # 如果没能建立连接退出此条
    if isconnected == False:
        global_element.emitsingle.stateupdataSingle.emit('DUT failed to establish connection!')
        global_element.testseq_judgement_list.append('Inconclusive')
        return

    time.sleep(2)

    # 设置 BW
    global_element.CU_intance.set_lte_BW(global_element.Test_lte_bandwidth)

    # 按channel列表循环处理
    for channel in channel_str_list:
        if channel != '':
            # 停止功能函数接口
            global_element.Test_channel = channel  # 更新全局变量channel
            global_element.CU_intance.set_lte_channel(channel)  # 设置综测仪lte channel
            time.sleep(3)

            for testitem in current_testplan[1:]:
                # 停止功能函数接口
                if testitem['@enable'] == 'yes':
                    if testitem['@Name'] == 'Conducted output power':
                        LTEFCC.Conductedoutputpower(testitem)
                    elif testitem['@Name'] == 'Peak-to-Average Ratio':
                        LTEFCC.peaktoaverageratio(testitem)
                    elif testitem['@Name'] == '99% Occupied Bandwidth':
                        LTEFCC.pct99OccupiedBandwidth(testitem)
                    elif testitem['@Name'] == '26dB Occupied Bandwidth':
                        LTEFCC.dB26OccupiedBandwidth(testitem)
                    elif testitem['@Name'] == 'Band edge':
                        LTEFCC.Bandedge(testitem)
                    elif testitem['@Name'] == 'Conducted Spurious emissions':
                        LTEFCC.ConductedSpuriousemissions(testitem)
                    elif testitem['@Name'] == 'Frequency stability':
                        LTEFCC.Frequencystability(testitem)
                    else:
                        pass

                    # # 更新进度
                    global_element.finished_step += 1
                    process_rate = format(global_element.finished_step * 100 / global_element.total_step, '.2f')
                    global_element.emitsingle.process_rateupdataSingle.emit(process_rate)
                    # 停止功能函数接口

                    # 更新summary
                    global_element.emitsingle.summaryupdataSingle.emit(global_element.finished_result_list)


def ltecafcc_tesplan_handle(current_testplan):
    # 检测是否有SA和CU
    if global_element.devices_config_dict['xml']['CU']['CHECK'] == 'False' or \
            global_element.devices_config_dict['xml']['SA']['CHECK'] == 'False':
        global_element.emitsingle.thread_exitSingle.emit('Test LTE CA FCC must have CU and SA!')
        time.sleep(0.1)

    # 检查DUT 控制方式
    if global_element.active_dut_dict['xml']['DUTCONFIG']['AUTOMODE'] not in ['1', '2', '3']:
        global_element.testseq_judgement_list.append('Inconclusive')
        global_element.emitsingle.stateupdataSingle.emit(
            'To test LTE CA, please select the automatic control mode of DUT '
            'in cellular mode.')
        return

    # 检测综测仪是否有LTE信令选件
    result = global_element.CU_intance.check_ltesin_option()
    if result == False:
        global_element.emitsingle.stateupdataSingle.emit('The CU does not support LTE CA signaling mode')
        global_element.testseq_judgement_list.append('Inconclusive')
        return

    # 处理init seting，获取band, channel, BW信息
    init_parms_list = current_testplan[0]['parms']['Parm']
    bw_list, channel_list = LTECAFCC.initseting(init_parms_list)

    # 综测仪LTE CA信令的初始化设置
    result = global_element.CU_intance.lteca_init_setting(bw_list, channel_list)
    if result == False:
        global_element.emitsingle.stateupdataSingle.emit('Error in initializing LTE CA signaling parameters of CU!')
        global_element.testseq_judgement_list.append('Inconclusive')
        return
    time.sleep(0.1)

    # 开启DUT并等待DUT注册上CU
    issync = global_element.CU_intance.check_dut_issync_lte()

    # 3次未能注册上则退出此条
    if issync == False:
        global_element.emitsingle.stateupdataSingle.emit('DUT registration failed!')
        global_element.testseq_judgement_list.append('Inconclusive')
        return

    time.sleep(2)

    # 成功注册后建立数据连接
    for i in range(3):
        isconnected = global_element.CU_intance.ltecacallsetup()
        if isconnected in [False, None]:
            time.sleep(5)
            continue
        elif isconnected == True:
            break

    # 如果没能建立连接退出此条
    if isconnected in [False, None]:
        global_element.emitsingle.stateupdataSingle.emit('DUT failed to establish connection!')
        global_element.testseq_judgement_list.append('Inconclusive')
        return

    time.sleep(2)

    # 设置 BW
    for bw_index in range(len(bw_list)):
        bw_group = bw_list[bw_index].split('+')
        global_element.Test_lte_bandwidth = 'PCC|%s, SCC|%s' % (bw_group[0], bw_group[1])  # 更新全局变量
        # 设置 CA BW
        global_element.CU_intance.set_lteca_BW(bw_group)

        # 处理每一个带宽组合的信道
        channel_str_list = channelstrtolist(channel_list[bw_index])  # 处理为['a+b', 'c+d', 'e+f']的格式

        for channel_index in range(len(channel_str_list)):
            channel_group = channel_str_list[channel_index].split('+')
            global_element.Test_channel = 'PCC|%s, SCC|%s' % (channel_group[0], channel_group[1])  # 更新全局变量
            global_element.CU_intance.set_lteca_channel(channel_group)                             # 配置CU信道

            # 切换BW and channel 后等待5秒检查连接状态
            time.sleep(5)
            for i in range(3):
                check_state = global_element.CU_intance.check_ca_connect_state()
                if check_state in [False, None]:
                    time.sleep(5)
                    continue
                elif check_state == True:
                    break
            if check_state in [False, None]:
                global_element.emitsingle.stateupdataSingle.emit('DUT failed to connect CU!')
                global_element.testseq_judgement_list.append('Inconclusive')
                return

            for testitem in current_testplan[1:]:
                if testitem['@enable'] == 'yes':
                    if testitem['@Name'] == 'Conducted Power and EIRP':
                        LTECAFCC.ConductedPowerandEIRP(testitem)
                    elif testitem['@Name'] == '99% Occupied Bandwidth':
                        LTECAFCC.pct99bw(testitem)
                    elif testitem['@Name'] == '26dB Occupied Bandwidth':
                        LTECAFCC.dB26OccupiedBandwidth(testitem)
                    elif testitem['@Name'] == 'Band edge':
                        LTECAFCC.bandedge(testitem)
                    elif testitem['@Name'] == 'Out of Band Emissions':
                        LTECAFCC.OutofBandEmissions(testitem)
                    elif testitem['@Name'] == 'Frequency stability':
                        LTECAFCC.freq_error(testitem)
                    elif testitem['@Name'] == 'Peak-to-Average Ratio':
                        LTECAFCC.peaktoaveragerate(testitem)

                    # # 更新进度
                    global_element.finished_step += 1
                    process_rate = format(global_element.finished_step * 100 / global_element.total_step, '.2f')
                    global_element.emitsingle.process_rateupdataSingle.emit(process_rate)
                    # 停止功能函数接口

                    # 更新summary
                    global_element.emitsingle.summaryupdataSingle.emit(global_element.finished_result_list)


def wlanb_testplan_handle(current_testplan):
    # 检测是否CU
    if global_element.devices_config_dict['xml']['CU']['CHECK'] == 'False':
        global_element.emitsingle.thread_exitSingle.emit('Test WLAN B must have CU!')
        time.sleep(0.1)

    # 检查DUT 控制方式
    if global_element.active_dut_dict['xml']['DUTCONFIG']['AUTOMODE'] not in ['4', '5']:
        global_element.testseq_judgement_list.append('Inconclusive')
        global_element.emitsingle.stateupdataSingle.emit(
            'To test wlan, please select the automatic control mode of DUT '
            'in Un-cellular mode.')
        return

    # 检测综测仪是否有WLAN信令选件
    result = global_element.CU_intance.check_wlansin_option()
    if result == False:
        global_element.emitsingle.stateupdataSingle.emit('The CU does not support WLAN signaling mode')
        global_element.testseq_judgement_list.append('Inconclusive')
        return

    # 处理init seting，获取datarate, channel, Antenna信息
    init_parms_list = current_testplan[0]['parms']['Parm']
    channel_str_list = WLAN_B.initseting(init_parms_list)

    # 综测仪WLAN信令的初始化设置
    result = global_element.CU_intance.wlan_init_setting()
    if result == False:
        global_element.emitsingle.stateupdataSingle.emit('WLAN signaling parameter initialization error in the CU!')
        global_element.testseq_judgement_list.append('Inconclusive')
        return
    time.sleep(0.1)
    global_element.emitsingle.stateupdataSingle.emit('Initialization of WLAN signaling parameters of the CU is '
                                                     'completed!')

    for channel in channel_str_list:
        if channel != '':
            global_element.Test_channel = channel  # 更新全局变量channel
            freq = report_handle.fre_wlan_calc(channel)
            global_element.CU_intance.set_wlan_channel(freq)  # 设置综测仪wlan channel
            time.sleep(3)

            result = global_element.CU_intance.check_wlan_connect_state()
            if result == False:
                global_element.emitsingle.stateupdataSingle.emit('DUT failed to establish connection!')
                global_element.testseq_judgement_list.append('Inconclusive')
                return

            for testitem in current_testplan[1:]:
                if testitem['@enable'] == 'yes':
                    if testitem['@Name'] == '16.3.8.4_Adjacent channel rejection':
                        WLAN_B.Adjacentchannelrejection(testitem)
                    # elif testitem['@Name'] == 'Peak-to-Average Ratio':
                    #     LTEFCC.peaktoaverageratio(testitem)
                    # elif testitem['@Name'] == '99% Occupied Bandwidth':
                    #     LTEFCC.pct99OccupiedBandwidth(testitem)
                    # elif testitem['@Name'] == '26dB Occupied Bandwidth':
                    #     LTEFCC.dB26OccupiedBandwidth(testitem)
                    # elif testitem['@Name'] == 'Band edge':
                    #     LTEFCC.Bandedge(testitem)
                    # elif testitem['@Name'] == 'Conducted Spurious emissions':
                    #     LTEFCC.ConductedSpuriousemissions(testitem)
                    # elif testitem['@Name'] == 'Frequency stability':
                    #     LTEFCC.Frequencystability(testitem)
                    else:
                        pass

                    # # 更新进度
                    global_element.finished_step += 1
                    process_rate = format(global_element.finished_step * 100 / global_element.total_step, '.2f')
                    global_element.emitsingle.process_rateupdataSingle.emit(process_rate)
                    # 停止功能函数接口

                    # 更新summary
                    global_element.emitsingle.summaryupdataSingle.emit(global_element.finished_result_list)


def bt2fcc_testplan_handle(current_testplan):
    # 初始化一些全局变量
    global_element.BT2_number_of_channel_istested = False
    global_element.BT2_dwelltime_istested = False
    global_element.BT2_fcc_20dbbw_result = {'0_DH5': '', '0_2-DH5': '', '0_3-DH5': '', '39_DH5': '', '39_2-DH5': '',
                                            '39_3-DH5': '', '78_DH5': '', '78_2-DH5': '', '78_3-DH5': ''}
    # 检测是否CU和SA
    if global_element.devices_config_dict['xml']['CU']['CHECK'] == 'False' or \
            global_element.devices_config_dict['xml']['SA']['CHECK'] == 'False':
        global_element.emitsingle.thread_exitSingle.emit('Test BT2 FCC must have CU and SA!')
        time.sleep(0.1)

    # 检查DUT 控制方式
    if global_element.active_dut_dict['xml']['DUTCONFIG']['AUTOMODE'] not in ['4', '5']:
        global_element.testseq_judgement_list.append('Inconclusive')
        global_element.emitsingle.stateupdataSingle.emit(
            'To test BT, please select the automatic control mode of DUT '
            'in Un-cellular mode.')
        return

    # 检测线损文件
    if global_element.CU_DUT_loss_file == '' or global_element.SA_DUT_loss_file == '':
        global_element.emitsingle.stateupdataSingle.emit('Tip: Lack of path loss file configuration!')
        global_element.testseq_judgement_list.append('Inconclusive')
        return

    if global_element.active_dut_dict['xml']['DUTCONFIG']['AUTOMODE'] != '5':
        global_element.emitsingle.stateupdataSingle.emit('Tip: BT2 FCC only supports signaling test mode!')
        global_element.testseq_judgement_list.append('Inconclusive')
        return

    # 检测综测仪是否有BT2信令选件
    result = global_element.CU_intance.check_btsin_option()
    if result == False:
        global_element.emitsingle.stateupdataSingle.emit('The CU does not support BT signaling mode')
        global_element.testseq_judgement_list.append('Inconclusive')
        return

    # 处理init seting，获取channel信息
    init_parms_list = current_testplan[0]['parms']['Parm']
    channel_str_list = BT2FCC.initseting(init_parms_list)

    # 综测仪BT信令的初始化设置
    result = global_element.CU_intance.bt2_init_setting()
    if result == False:
        global_element.emitsingle.stateupdataSingle.emit('The CU initialized the BT2 signaling parameters wrong!')
        global_element.testseq_judgement_list.append('Inconclusive')
        return
    time.sleep(0.1)
    global_element.emitsingle.stateupdataSingle.emit('Initialization of BT2 signaling parameters is completed!')

    # bt2建立信令连接
    result = global_element.CU_intance.bt2_checkAndconnect()
    if result == False:
        global_element.testseq_judgement_list.append('Inconclusive')
        return

    for channel in channel_str_list:
        global_element.Test_channel = channel  # 更新全局变量channel
        # freq = report_handle.fre_bt2_calc(channel)
        global_element.CU_intance.set_bt2_channel(channel)  # 设置综测仪bt2 channel
        time.sleep(3)

        for testitem in current_testplan[1:]:
            if testitem['@enable'] == 'yes':
                if testitem['@Name'] == '20dB bandwidth':
                    BT2FCC.db20_bandwidth(testitem)
                elif testitem['@Name'] == '99% bandwidth':
                    BT2FCC.pct99BW(testitem)
                elif testitem['@Name'] == 'Peak Output Power':
                    BT2FCC.peakoutpurtpower(testitem)
                elif testitem['@Name'] == 'Number of Channel':
                    BT2FCC.numberofchannel(testitem)
                elif testitem['@Name'] == 'Hopping Channel Separation':
                    BT2FCC.hoppingchannelseparation(testitem)
                elif testitem['@Name'] == 'Dwell Time':
                    BT2FCC.dwelltime(testitem)
                elif testitem['@Name'] == 'Conducted Band Edges':
                    BT2FCC.bandedge(testitem)
                elif testitem['@Name'] == 'Conducted Spurious Emissions':
                    BT2FCC.cse(testitem)
                else:
                    pass

                # 更新进度
                global_element.finished_step += 1
                process_rate = format(global_element.finished_step * 100 / global_element.total_step, '.2f')
                global_element.emitsingle.process_rateupdataSingle.emit(process_rate)
                # 停止功能函数接口

                # 更新summary
                global_element.emitsingle.summaryupdataSingle.emit(global_element.finished_result_list)


def wlanac_testplan_handle(current_testplan):
    # 检测是否CU
    if global_element.devices_config_dict['xml']['CU']['CHECK'] == 'False':
        global_element.emitsingle.thread_exitSingle.emit('Test WLAN AC must have CU!')
        time.sleep(0.1)

    # 检查DUT 控制方式
    if global_element.active_dut_dict['xml']['DUTCONFIG']['AUTOMODE'] not in ['4', '5']:
        global_element.testseq_judgement_list.append('Inconclusive')
        global_element.emitsingle.stateupdataSingle.emit(
            'To test wlan, please select the automatic control mode of DUT '
            'in Un-cellular mode.')
        return

    # 检测综测仪是否有WLAN信令选件
    result = global_element.CU_intance.check_wlansin_option()
    if result == False:
        global_element.emitsingle.stateupdataSingle.emit('The CU does not support WLAN signaling mode')
        global_element.testseq_judgement_list.append('Inconclusive')
        return

    # 处理init seting，获取datarate, channel, Antenna信息
    init_parms_list = current_testplan[0]['parms']['Parm']
    channel_str_list = WLAN_AC.initseting(init_parms_list)

    # 综测仪WLAN信令的初始化设置
    result = global_element.CU_intance.wlan_init_setting()
    if result == False:
        global_element.emitsingle.stateupdataSingle.emit('WLAN signaling parameter initialization error in the CU!')
        global_element.testseq_judgement_list.append('Inconclusive')
        return
    time.sleep(0.1)
    global_element.emitsingle.stateupdataSingle.emit('Initialization of WLAN signaling parameters of the CU is '
                                                     'completed!')

    for channel in channel_str_list:
        if channel != '':
            global_element.Test_channel = channel  # 更新全局变量channel
            freq = report_handle.fre_wlan_calc(channel)
            global_element.CU_intance.set_wlan_channel(freq)  # 设置综测仪wlan channel
            time.sleep(3)

            result = global_element.CU_intance.check_wlan_connect_state()
            if result == False:
                global_element.emitsingle.stateupdataSingle.emit('DUT failed to establish connection!')
                global_element.testseq_judgement_list.append('Inconclusive')
                return

            for testitem in current_testplan[1:]:
                if testitem['@enable'] == 'yes':
                    if testitem['@Name'] == '21.3.18.2_Adjacent channel rejection':
                        WLAN_AC.Adjacentchannelrejection(testitem)
                    elif testitem['@Name'] == '21.3.18.3_NO Adjacent channel rejection':
                        WLAN_AC.NoAdjacentchannelrejection(testitem)
                    # elif testitem['@Name'] == '99% Occupied Bandwidth':
                    #     LTEFCC.pct99OccupiedBandwidth(testitem)
                    # elif testitem['@Name'] == '26dB Occupied Bandwidth':
                    #     LTEFCC.dB26OccupiedBandwidth(testitem)
                    # elif testitem['@Name'] == 'Band edge':
                    #     LTEFCC.Bandedge(testitem)
                    # elif testitem['@Name'] == 'Conducted Spurious emissions':
                    #     LTEFCC.ConductedSpuriousemissions(testitem)
                    # elif testitem['@Name'] == 'Frequency stability':
                    #     LTEFCC.Frequencystability(testitem)
                    else:
                        pass

                    # 更新进度
                    global_element.finished_step += 1
                    process_rate = format(global_element.finished_step * 100 / global_element.total_step, '.2f')
                    global_element.emitsingle.process_rateupdataSingle.emit(process_rate)
                    # 停止功能函数接口

                    # 更新summary
                    global_element.emitsingle.summaryupdataSingle.emit(global_element.finished_result_list)