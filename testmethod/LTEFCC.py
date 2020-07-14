# !/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Author    : Feng Zhaohui
# @Time      : 2019/4/17
# @File      : LTEFCC.py
# @Funcyusa  :
# @Version   : 1.0

import global_element
import testseq_handle
import report_handle
import time
import os


def initseting(init_parms_list):
    """
    LTEFCC模块initing的处理
    :param init_parms_list:
    :return:
    """
    # 更新测试band信息到全局变量
    global_element.Test_band = init_parms_list[0]['Value']

    # 更新BS LEVEL信息到全局变量
    global_element.Test_bslevel = init_parms_list[2]['Value']

    # 更新Bandwidth信息到全局变量
    global_element.Test_lte_bandwidth = init_parms_list[1]['Value']

    # 获取信道列表
    channel_str = global_element.lte_channel_fortest_dict[global_element.Test_lte_bandwidth][global_element.Test_band]
    channel_str_list = testseq_handle.channelstrtolist(channel_str)  # 将所有信道整理成字符串列表的形式

    return channel_str_list


def Conductedoutputpower(testitem):
    """
    :param testitem:
    :param mode_str:
    :return:
    """

    global_element.Test_item = 'Conducted output power'
    global_element.emitsingle.stateupdataSingle.emit('Testing in progress of Conducted output power……,Band: %s，Bandwidth: %s, '
                                                     'Channel：%s' % (global_element.Test_band,
                                                                     global_element.Test_lte_bandwidth,
                                                                     global_element.Test_channel))
    # 停止功能函数接口

    # 将此项用户的参数初始化
    att_gain = testitem['parms']['Parm'][0]['Value']
    RB_str = testitem['parms']['Parm'][1]['Value']
    mode_str = testitem['parms']['Parm'][2]['Value']
    low_limit_5_26 = testitem['limits']['limit'][0]['low']
    high_limit_5_26 = testitem['limits']['limit'][0]['high']
    low_limit_12_17 = testitem['limits']['limit'][1]['low']
    high_limit_12_17 = testitem['limits']['limit'][1]['high']
    low_limit_2_7_25_41 = testitem['limits']['limit'][2]['low']
    high_limit_2_7_25_41 = testitem['limits']['limit'][2]['high']
    low_limit_4 = testitem['limits']['limit'][3]['low']
    high_limit_4 = testitem['limits']['limit'][3]['high']

    # 设置CU的线损
    dlfre, ulfre = report_handle.freq_gsm_calc(int(global_element.Test_channel))
    global_element.CU_intance.set_lte_loss(ulfre, dlfre)

    # RESET SA
    # global_element.SA_intance.resetself()

    # 设置SA的线损
    # global_element.SA_intance.set_loss(ulfre)

    # SA检查DUT是否有发射对应信号
    # global_element.SA_intance.check_gsm_signal()

    # 开始SA的设置

    if global_element.Test_lte_bandwidth == '1.4MHz':
        RB_list = [1, 3, 6]
    elif global_element.Test_lte_bandwidth == '3MHz':
        RB_list = [1, 8, 15]
    elif global_element.Test_lte_bandwidth == '5MHz':
        RB_list = [1, 12, 25]
    elif global_element.Test_lte_bandwidth == '10MHz':
        RB_list = [1, 25, 50]
    elif global_element.Test_lte_bandwidth == '15MHz':
        RB_list = [1, 36, 75]
    elif global_element.Test_lte_bandwidth == '20MHz':
        RB_list = [1, 50, 100]
    else:
        RB_list = [1, 3, 6]

    mode_list = mode_str.split('/')
    RB_str_list = RB_str.split('/')

    for mode_index in range(len(mode_list)):
        # 停止功能函数接口
        global_element.Test_modulation = mode_list[mode_index]        # 更新全局变量mode
        for RB_indext in range(len(RB_str_list)):
            # 停止功能函数接口
            if RB_str_list[RB_indext] == '1RB':
                RB_count_index = 0
            elif RB_str_list[RB_indext] == 'PRB':
                RB_count_index = 1
            elif RB_str_list[RB_indext] == 'FRB':
                RB_count_index = 2
            else:
                RB_count_index = 0
            global_element.CU_intance.set_lte_ul_modeandRB(mode_list[mode_index], str(RB_list[RB_count_index]))

            if RB_list[RB_count_index] == 1:
                for pos in ['LOW', 'MID', 'HIGH']:
                    # 停止功能函数接口
                    global_element.CU_intance.set_lte_ul_RBoffset(pos)

                    global_element.Test_lte_RB = 'RB: %s, RB Pos: %s' % (str(RB_list[RB_count_index]), pos)
                    time.sleep(2)

                    # # 检查Handover后连接是否正常
                    # time.sleep(2)
                    # state = global_element.CU_intance.lte_connect_state()
                    # if state == False:
                    #     global_element.testseq_judgement_list.append('Inconclusive')
                    #     return

                    # 取值
                    ave_power = global_element.CU_intance.get_lte_power()

                    global_element.Test_remark = 'Reporting Only'
                    report_handle.Reporttool(ave_power, 'None', 'None')

                    # 输出EIRP/ERP
                    if global_element.Test_band == 'FDD-LTE 5' or global_element.Test_band == 'FDD-LTE 26':
                        global_element.Test_item = 'ERP'
                        activehighlimit = high_limit_5_26
                        activelowlimit = low_limit_5_26
                        try:
                            erp_result = str(format(eval(ave_power) + eval(att_gain) - 2.15, '.2f'))
                        except:
                            erp_result = 'NULL'
                        global_element.Test_remark = 'ERP = Conducted Power + ATT gain(' + att_gain + ') - 2.15'
                    elif global_element.Test_band == 'FDD-LTE 12' or global_element.Test_band == 'FDD-LTE 17':
                        global_element.Test_item = 'ERP'
                        activehighlimit = high_limit_12_17
                        activelowlimit = low_limit_12_17
                        try:
                            erp_result = str(format(eval(ave_power) + eval(att_gain) - 2.15, '.2f'))
                        except:
                            erp_result = 'NULL'
                        global_element.Test_remark = 'ERP = Conducted Power + ATT gain(' + att_gain + ') - 2.15'
                    elif global_element.Test_band == 'FDD-LTE 2' or global_element.Test_band == 'FDD-LTE 25' or \
                            global_element.Test_band == 'FDD-LTE 7' or global_element.Test_band == 'TDD-LTE 41' or \
                            global_element.Test_band == 'TDD-LTE 38':
                        global_element.Test_item = 'EIRP'
                        activehighlimit = high_limit_2_7_25_41
                        activelowlimit = low_limit_2_7_25_41
                        try:
                            erp_result = str(format(eval(ave_power) + eval(att_gain), '.2f'))
                        except:
                            erp_result = 'NULL'
                        global_element.Test_remark = 'EIRP = Conducted Power + ATT gain(' + att_gain + ')'
                    elif global_element.Test_band == 'FDD-LTE 4':
                        global_element.Test_item = 'EIRP'
                        activehighlimit = high_limit_4
                        activelowlimit = low_limit_4
                        try:
                            erp_result = str(format(eval(ave_power) + eval(att_gain), '.2f'))
                        except:
                            erp_result = 'NULL'
                        global_element.Test_remark = 'EIRP = Conducted Power + ATT gain(' + att_gain + ')'

                    report_handle.Reporttool(erp_result, activelowlimit, activehighlimit)
                    global_element.Test_item = 'Conducted output power'
                    global_element.Test_remark = ''
            else:
                for pos in ['LOW', 'HIGH']:
                    # 停止功能函数接口
                    global_element.CU_intance.set_lte_ul_RBoffset(pos)

                    global_element.Test_lte_RB = 'RB: %s, RB Pos: %s' % (str(RB_list[RB_indext]), pos)

                    # 取值
                    ave_power = global_element.CU_intance.get_lte_power()

                    global_element.Test_remark = 'Reporting Only'
                    report_handle.Reporttool(ave_power, 'None', 'None')

                    # 输出EIRP/ERP
                    if global_element.Test_band == 'FDD-LTE 5' or global_element.Test_band == 'FDD-LTE 26':
                        global_element.Test_item = 'ERP'
                        activehighlimit = high_limit_5_26
                        activelowlimit = low_limit_5_26
                        try:
                            erp_result = str(format(eval(ave_power) + eval(att_gain) - 2.15, '.2f'))
                        except:
                            erp_result = 'NULL'
                        global_element.Test_remark = 'ERP = Conducted Power + ATT gain(' + att_gain + ') - 2.15'
                    elif global_element.Test_band == 'FDD-LTE 12' or global_element.Test_band == 'FDD-LTE 17':
                        global_element.Test_item = 'ERP'
                        activehighlimit = high_limit_12_17
                        activelowlimit = low_limit_12_17
                        try:
                            erp_result = str(format(eval(ave_power) + eval(att_gain) - 2.15, '.2f'))
                        except:
                            erp_result = 'NULL'
                        global_element.Test_remark = 'ERP = Conducted Power + ATT gain(' + att_gain + ') - 2.15'
                    elif global_element.Test_band == 'FDD-LTE 2' or global_element.Test_band == 'FDD-LTE 25' or \
                            global_element.Test_band == 'FDD-LTE 7' or global_element.Test_band == 'TDD-LTE 41' or \
                            global_element.Test_band == 'TDD-LTE 38':
                        global_element.Test_item = 'EIRP'
                        activehighlimit = high_limit_2_7_25_41
                        activelowlimit = low_limit_2_7_25_41
                        try:
                            erp_result = str(format(eval(ave_power) + eval(att_gain), '.2f'))
                        except:
                            erp_result = 'NULL'
                        global_element.Test_remark = 'EIRP = Conducted Power + ATT gain(' + att_gain + ')'
                    elif global_element.Test_band == 'FDD-LTE 4':
                        global_element.Test_item = 'EIRP'
                        activehighlimit = high_limit_4
                        activelowlimit = low_limit_4
                        try:
                            erp_result = str(format(eval(ave_power) + eval(att_gain), '.2f'))
                        except:
                            erp_result = 'NULL'
                        global_element.Test_remark = 'EIRP = Conducted Power + ATT gain(' + att_gain + ')'

                    report_handle.Reporttool(erp_result, activelowlimit, activehighlimit)
                    global_element.Test_item = 'Conducted output power'
                    global_element.Test_remark = ''

                    # 停止功能函数接口


def peaktoaverageratio(testitem):
    global_element.Test_item = 'Peak-to-Average Ratio'
    global_element.emitsingle.stateupdataSingle.emit('Testing in progress of Peak-to-Average Ratio……,Band: %s，Bandwidth: %s, '
                                                     'Channel：%s' % (global_element.Test_band,
                                                                     global_element.Test_lte_bandwidth,
                                                                     global_element.Test_channel))
    # 停止功能函数接口

    # 将此项用户的参数初始化
    RB_str = testitem['parms']['Parm'][0]['Value']
    mode_str = testitem['parms']['Parm'][1]['Value']
    activelowlimit = testitem['limits']['limit']['low']
    activehighlimit = testitem['limits']['limit']['high']

    # 设置CU的线损
    dlfre, ulfre = report_handle.freq_gsm_calc(int(global_element.Test_channel))
    global_element.CU_intance.set_lte_loss(ulfre, dlfre)

    # RESET SA
    global_element.SA_intance.resetself()

    # 设置SA的线损
    global_element.SA_intance.set_loss(ulfre)

    # 设置lte为最大功控
    global_element.CU_intance.set_lte_maxpower()

    # SA检查DUT是否有发射对应信号
    result = global_element.SA_intance.check_gsm_signal()
    if result == False:
        global_element.Test_remark = 'SA did not detect the signal!'
        report_handle.Reporttool('NULL', activelowlimit, activehighlimit)
        global_element.Test_remark = ''
    else:
        global_element.emitsingle.stateupdataSingle.emit('SA detection signal is successful!')

        if global_element.Test_lte_bandwidth == '1.4MHz':
            RB_list = [1, 6]
        elif global_element.Test_lte_bandwidth == '3MHz':
            RB_list = [1, 15]
        elif global_element.Test_lte_bandwidth == '5MHz':
            RB_list = [1, 25]
        elif global_element.Test_lte_bandwidth == '10MHz':
            RB_list = [1, 50]
        elif global_element.Test_lte_bandwidth == '15MHz':
            RB_list = [1, 75]
        elif global_element.Test_lte_bandwidth == '20MHz':
            RB_list = [1, 100]
        else:
            RB_list = [1, 6]

        mode_list = mode_str.split('/')
        RB_str_list = RB_str.split('/')

        for mode in mode_list:
            # 停止功能函数接口
            global_element.Test_modulation = mode  # 更新全局变量mode
            for RB in RB_str_list:
                # 停止功能函数接口
                if RB == '1RB':
                    RB_count = RB_list[0]
                elif RB == 'FRB':
                    RB_count = RB_list[1]
                global_element.CU_intance.set_lte_ul_modeandRB(mode, str(RB_count))
                global_element.Test_lte_RB = 'RB: ' + str(RB_count)

                if RB_count == 1:
                    global_element.CU_intance.set_lte_ul_RBoffset('MID')

                # # 检查Handover后连接是否正常
                # time.sleep(2)
                # state = global_element.CU_intance.lte_connect_state()
                # if state == False:
                #     global_element.testseq_judgement_list.append('Inconclusive')
                #     return

                # 开始SA的设置
                global_element.SA_intance.set_reflevel('40')
                global_element.SA_intance.setcenterfrequency(ulfre)
                global_element.SA_intance.setRbwVbw(global_element.Test_lte_bandwidth[:-3],
                                                    str(eval(global_element.Test_lte_bandwidth[:-3]) * 3))
                global_element.SA_intance.setspan(global_element.Test_lte_bandwidth[:-3])
                global_element.SA_intance.settrace('1', 'MAX')
                global_element.SA_intance.setdetector('SAMPLE')
                global_element.SA_intance.sweepconfig(False, True, '', '200', '')

                result = global_element.SA_intance.CCDFON_and_get_value()

                global_element.Test_remark = 'Unit: dB'
                # 取值
                report_handle.Reporttool(result, activelowlimit, activehighlimit)

                # 截图
                picturepath = global_element.reportpath[:global_element.reportpath.index('.')]
                if not os.path.isdir(picturepath + '/LTE FCC/Peak-to-Average Ratio'):
                    os.makedirs(picturepath + '/LTE FCC/Peak-to-Average Ratio')

                picturepath_final = picturepath + '/LTE FCC/Peak-to-Average Ratio/' + global_element.Test_band \
                                    + ' BW' + global_element.Test_lte_bandwidth + ' Channel' + \
                                    global_element.Test_channel + ' RB' + str(RB_count) + ' ' + mode + '.JPG'
                global_element.SA_intance.PrtScn(picturepath_final)

                global_element.SA_intance.CCDFOFF()

                global_element.Test_remark = ''

                # 停止功能函数接口


def pct99OccupiedBandwidth(testitem):
    global_element.Test_item = '99% Occupied Bandwidth'
    global_element.emitsingle.stateupdataSingle.emit('Testing in progress of 99pct Occupied Bandwidth……,Band: %s，Bandwidth: %s, '
                                                     'Channel：%s' % (global_element.Test_band,
                                                                     global_element.Test_lte_bandwidth,
                                                                     global_element.Test_channel))
    # 停止功能函数接口

    # 将此项用户的参数初始化
    RB_str = testitem['parms']['Parm'][0]['Value']
    mode_str = testitem['parms']['Parm'][1]['Value']
    activelowlimit = testitem['limits']['limit']['low']
    activehighlimit = testitem['limits']['limit']['high']

    # 设置CU的线损
    dlfre, ulfre = report_handle.freq_gsm_calc(int(global_element.Test_channel))
    global_element.CU_intance.set_lte_loss(ulfre, dlfre)

    # RESET SA
    global_element.SA_intance.resetself()

    # 设置SA的线损
    global_element.SA_intance.set_loss(ulfre)

    # 设置lte为最大功控
    global_element.CU_intance.set_lte_maxpower()

    # SA检查DUT是否有发射对应信号
    result = global_element.SA_intance.check_gsm_signal()
    if result == False:
        global_element.Test_remark = 'SA did not detect the signal!'
        report_handle.Reporttool('NULL', activelowlimit, activehighlimit)
        global_element.Test_remark = ''
    else:
        global_element.emitsingle.stateupdataSingle.emit('SA detection signal is successful!')

        mode_list = mode_str.split('/')
        rb = int(eval(global_element.Test_lte_bandwidth[:-3]) * 5)
        if global_element.Test_lte_bandwidth == '1.4MHz':
            rb -= 1

        for mode in mode_list:
            # 停止功能函数接口
            global_element.Test_modulation = mode
            global_element.CU_intance.set_lte_ul_modeandRB(mode, str(rb))
            global_element.Test_lte_RB = 'RB: ' + str(rb)

            # # 检查Handover后连接是否正常
            # time.sleep(2)
            # state = global_element.CU_intance.lte_connect_state()
            # if state == False:
            #     global_element.testseq_judgement_list.append('Inconclusive')
            #     return

            # 开始SA的设置
            if global_element.Test_lte_bandwidth == '1.4MHz':
                rbw_str = '0.03'
            elif global_element.Test_lte_bandwidth == '3MHz' or global_element.Test_lte_bandwidth == '5MHz':
                rbw_str = '0.1'
            elif global_element.Test_lte_bandwidth == '10MHz' or global_element.Test_lte_bandwidth == '15MHz':
                rbw_str = '0.3'
            elif global_element.Test_lte_bandwidth == '20MHz':
                rbw_str = '1'

            global_element.SA_intance.set_reflevel('30')
            global_element.SA_intance.setcenterfrequency(ulfre)
            global_element.SA_intance.setRbwVbw(rbw_str, str(eval(rbw_str) * 3))
            global_element.SA_intance.setspan(str(eval(global_element.Test_lte_bandwidth[:-3]) * 2))
            global_element.SA_intance.settrace('1', 'MAX')
            global_element.SA_intance.setdetector('MAX PEAK')
            global_element.SA_intance.sweepconfig(True, True, '', '', '')

            # 停止功能函数接口

            OBW = global_element.SA_intance.pctBW('99')  # 取99%带宽值
            OBW_final = format(eval(OBW) / 1000, '.2f')

            # 停止功能函数接口

            global_element.SA_intance.markertotrace('1', '1')
            global_element.SA_intance.markertopeak('1')

            global_element.Test_remark = 'Uint: MHz'
            report_handle.Reporttool(OBW_final, activelowlimit, activehighlimit)

            # 截图
            picturepath = global_element.reportpath[:global_element.reportpath.index('.')]
            if not os.path.isdir(picturepath + '/LTE FCC/99% Occupied Bandwidth'):
                os.makedirs(picturepath + '/LTE FCC/99% Occupied Bandwidth')

            picturepath_final = picturepath + '/LTE FCC/99% Occupied Bandwidth/' + global_element.Test_band + ' BW' + \
                                global_element.Test_lte_bandwidth + ' Channel' + \
                                global_element.Test_channel + ' RB' + str(rb) + ' ' + mode + '.JPG'
            global_element.SA_intance.PrtScn(picturepath_final)

            global_element.Test_remark = ''

            # 停止功能函数接口


def dB26OccupiedBandwidth(testitem):

    global_element.Test_item = '26dB Occupied Bandwidth'
    global_element.emitsingle.stateupdataSingle.emit('Testing in progress of 26dB Occupied Bandwidth……,Band: %s，Bandwidth: %s, '
                                                     'Channel：%s' % (global_element.Test_band,
                                                                     global_element.Test_lte_bandwidth,
                                                                     global_element.Test_channel))
    # 停止功能函数接口

    # 将此项用户的参数初始化
    RB_str = testitem['parms']['Parm'][0]['Value']
    mode_str = testitem['parms']['Parm'][1]['Value']
    activelowlimit = testitem['limits']['limit']['low']
    activehighlimit = testitem['limits']['limit']['high']

    # 设置CU的线损
    dlfre, ulfre = report_handle.freq_gsm_calc(int(global_element.Test_channel))
    global_element.CU_intance.set_lte_loss(ulfre, dlfre)

    # RESET SA
    global_element.SA_intance.resetself()

    # 设置SA的线损
    global_element.SA_intance.set_loss(ulfre)

    # 设置lte为最大功控
    global_element.CU_intance.set_lte_maxpower()

    # SA检查DUT是否有发射对应信号
    result = global_element.SA_intance.check_gsm_signal()
    if result == False:
        global_element.Test_remark = 'SA did not detect the signal!'
        report_handle.Reporttool('NULL', activelowlimit, activehighlimit)
        global_element.Test_remark = ''
    else:
        global_element.emitsingle.stateupdataSingle.emit('SA detection signal is successful!')

        mode_list = mode_str.split('/')
        rb = int(eval(global_element.Test_lte_bandwidth[:-3]) * 5)
        if global_element.Test_lte_bandwidth == '1.4MHz':
            rb -= 1

        for mode in mode_list:
            # 停止功能函数接口
            global_element.Test_modulation = mode
            global_element.CU_intance.set_lte_ul_modeandRB(mode, str(rb))
            global_element.Test_lte_RB = 'RB: ' + str(rb)

            # # 检查Handover后连接是否正常
            # time.sleep(2)
            # state = global_element.CU_intance.lte_connect_state()
            # if state == False:
            #     global_element.testseq_judgement_list.append('Inconclusive')
            #     return

            # 开始SA的设置
            if global_element.Test_lte_bandwidth == '1.4MHz':
                rbw_str = '0.03'
            elif global_element.Test_lte_bandwidth == '3MHz' or global_element.Test_lte_bandwidth == '5MHz':
                rbw_str = '0.1'
            elif global_element.Test_lte_bandwidth == '10MHz' or global_element.Test_lte_bandwidth == '15MHz':
                rbw_str = '0.3'
            elif global_element.Test_lte_bandwidth == '20MHz':
                rbw_str = '1'

            global_element.SA_intance.set_reflevel('30')
            global_element.SA_intance.setcenterfrequency(ulfre)
            global_element.SA_intance.setRbwVbw(rbw_str, str(eval(rbw_str) * 3))
            global_element.SA_intance.setspan(str(eval(global_element.Test_lte_bandwidth[:-3]) * 2))
            global_element.SA_intance.settrace('1', 'MAX')
            global_element.SA_intance.setdetector('MAX PEAK')
            global_element.SA_intance.sweepconfig(True, True, '', '', '')

            # 停止功能函数接口

            global_element.SA_intance.markertotrace('1', '1')
            global_element.SA_intance.markertopeak('1')

            # 停止功能函数接口

            OBW = global_element.SA_intance.NDBDBW('26')  # 取26 dB带宽值
            OBW_final = format(eval(OBW) / 1000, '.2f')

            global_element.Test_remark = 'Uint: MHz'
            report_handle.Reporttool(OBW_final, activelowlimit, activehighlimit)

            # 截图
            picturepath = global_element.reportpath[:global_element.reportpath.index('.')]
            if not os.path.isdir(picturepath + '/LTE FCC/26dB Occupied Bandwidth'):
                os.makedirs(picturepath + '/LTE FCC/26dB Occupied Bandwidth')

            picturepath_final = picturepath + '/LTE FCC/26dB Occupied Bandwidth/' + global_element.Test_band + ' BW' + \
                                global_element.Test_lte_bandwidth + ' Channel' + \
                                global_element.Test_channel + ' RB' + str(rb) + ' ' + mode + '.JPG'
            global_element.SA_intance.PrtScn(picturepath_final)

            global_element.Test_remark = ''

            # 停止功能函数接口


def Bandedge(testitem):
    channel_support_list = ['18607', '19193', '18615', '19185', '18625', '19175', '18650', '19150', '18675', '19125',
                            '18700', '19100', '19957', '20393', '19965', '20385', '19975', '20375', '20000', '20350',
                            '20025', '20325', '20050', '20300', '20407', '20643', '20415', '20635', '20425', '20625',
                            '20450', '20600', '20775', '21425', '20800', '21400', '20825', '21375', '20850', '21350',
                            '23017', '23173', '23025', '23165', '23035', '23155', '23060', '23130', '23755', '23825',
                            '23780', '23800', '26683', '26675', '26665', '26640', '26615', '26590', '26697', '27033',
                            '26705', '27025', '26715', '27015', '26740', '26990', '26765', '26965', '39675', '41565',
                            '39700', '41540', '39725', '41515', '39750', '41490', '26047', '26055', '26065', '26090',
                            '26115', '26140', '37775', '38225', '37800', '38200', '37825', '38175', '37850', '38150']
    low_channel_list = ['18607', '18615', '18625', '18650', '18675',
                            '18700', '19957', '19965', '19975', '20000',
                            '20025', '20050', '20407', '20415', '20425',
                            '20450', '20775', '20800', '20825', '20850',
                            '23017', '23025', '23035', '23060', '23755',
                            '23780', '26697',
                            '26705', '26715', '26740', '26765', '39675',
                            '39700', '39725', '39750', '26047', '26055', '26065', '26090',
                            '26115', '26140', '37775', '37800', '37825', '37850']
    if global_element.Test_channel in channel_support_list:
        global_element.Test_item = 'Band edge'
        global_element.emitsingle.stateupdataSingle.emit('Testing in progressBand edge……,Band: %s，Bandwidth: %s, '
                                                     'Channel：%s' % (global_element.Test_band,
                                                                     global_element.Test_lte_bandwidth,
                                                                     global_element.Test_channel))
        # 停止功能函数接口

        # 将此项用户的参数初始化
        RB_str = testitem['parms']['Parm'][0]['Value']
        mode_str = testitem['parms']['Parm'][1]['Value']

        # 设置CU的线损
        dlfre, ulfre = report_handle.freq_gsm_calc(int(global_element.Test_channel))
        global_element.CU_intance.set_lte_loss(ulfre, dlfre)

        # RESET SA
        global_element.SA_intance.resetself()

        # 设置SA的线损
        global_element.SA_intance.set_loss(ulfre)

        # 设置lte为最大功控
        global_element.CU_intance.set_lte_maxpower()

        # SA检查DUT是否有发射对应信号
        result = global_element.SA_intance.check_gsm_signal()
        if result == False:
            global_element.Test_remark = 'SA did not detect the signal!'
            report_handle.Reporttool('NULL', 'None', 'None')
            global_element.Test_remark = ''
        else:
            global_element.emitsingle.stateupdataSingle.emit('SA detection signal is successful!')

            mode_list = mode_str.split('/')
            rb_str_list = RB_str.split('/')

            if global_element.Test_lte_bandwidth == '1.4MHz':
                RB_list = [1, 6]
            elif global_element.Test_lte_bandwidth == '3MHz':
                RB_list = [1, 15]
            elif global_element.Test_lte_bandwidth == '5MHz':
                RB_list = [1, 25]
            elif global_element.Test_lte_bandwidth == '10MHz':
                RB_list = [1, 50]
            elif global_element.Test_lte_bandwidth == '15MHz':
                RB_list = [1, 75]
            elif global_element.Test_lte_bandwidth == '20MHz':
                RB_list = [1, 100]

            for mode in mode_list:
                # 停止功能函数接口
                global_element.Test_modulation = mode
                for rb_str in rb_str_list:
                    # 停止功能函数接口
                    if rb_str == '1RB':
                        rb = RB_list[0]
                    elif rb_str == 'FRB':
                        rb = RB_list[1]

                    global_element.CU_intance.set_lte_ul_modeandRB(mode, str(rb))
                    global_element.Test_lte_RB = 'RB: ' + str(rb)

                    if rb == 1:
                        if global_element.Test_channel in low_channel_list:
                            global_element.CU_intance.set_lte_ul_RBoffset('LOW')
                        else:
                            global_element.CU_intance.set_lte_ul_RBoffset('HIGH')

                    # # 检查Handover后连接是否正常
                    # time.sleep(2)
                    # state = global_element.CU_intance.lte_connect_state()
                    # if state == False:
                    #     global_element.testseq_judgement_list.append('Inconclusive')
                    #     return

                    # 开始SA的设置
                    global_element.SA_intance.settrace('1', 'MAX')
                    global_element.SA_intance.sweepconfig(True, True, '', '', '')

                    # 停止功能函数接口

                    result = global_element.SA_intance.ltefcc_bandedge_set(global_element.Test_channel)

                    global_element.Test_remark = 'Reference screenshot of this result!'
                    if result == '1':
                        report_handle.Reporttool('1', '-1', '1')
                    elif result == 'NULL':
                        report_handle.Reporttool('NULL', '-1', '1')
                    else:
                        report_handle.Reporttool('0', '-1', '1')

                    # 截图
                    picturepath = global_element.reportpath[:global_element.reportpath.index('.')]
                    if not os.path.isdir(picturepath + '/LTE FCC/Band edge'):
                        os.makedirs(picturepath + '/LTE FCC/Band edge')

                    picturepath_final = picturepath + '/LTE FCC/Band edge/' + global_element.Test_band + ' BW' + \
                                        global_element.Test_lte_bandwidth + ' Channel' + \
                                        global_element.Test_channel + ' RB' + str(rb) + ' ' + mode + '.JPG'
                    global_element.SA_intance.PrtScn(picturepath_final)

                    global_element.Test_remark = ''

                    # 停止功能函数接口


def ConductedSpuriousemissions(testitem):
    # 停止功能函数接口
    band_support_list = ['FDD-LTE 2', 'FDD-LTE 4', 'FDD-LTE 5', 'FDD-LTE 7', 'FDD-LTE 12', 'FDD-LTE 17', 'FDD-LTE 25',
                         'FDD-LTE 26', 'TDD-LTE 38', 'TDD-LTE 41']
    if global_element.Test_band in band_support_list:
        global_element.Test_item = 'Conducted Spurious emissions'
        global_element.emitsingle.stateupdataSingle.emit('Testing in progress of Conducted Spurious emissions……,Band: %s，Bandwidth: %s, '
                                                     'Channel：%s' % (global_element.Test_band,
                                                                     global_element.Test_lte_bandwidth,
                                                                     global_element.Test_channel))
        # 停止功能函数接口

        # 将此项用户的参数初始化
        RB_str = testitem['parms']['Parm'][0]['Value']
        mode_str = testitem['parms']['Parm'][1]['Value']

        # 设置CU的线损
        dlfre, ulfre = report_handle.freq_gsm_calc(int(global_element.Test_channel))
        global_element.CU_intance.set_lte_loss(ulfre, dlfre)

        # RESET SA
        global_element.SA_intance.resetself()

        # 设置SA的线损
        global_element.SA_intance.set_loss(ulfre)

        # 设置lte为最大功控
        global_element.CU_intance.set_lte_maxpower()

        # SA检查DUT是否有发射对应信号
        result = global_element.SA_intance.check_gsm_signal()
        if result == False:
            global_element.Test_remark = 'SA did not detect the signal!'
            report_handle.Reporttool('NULL', 'None', 'None')
            global_element.Test_remark = ''
        else:
            global_element.emitsingle.stateupdataSingle.emit('SA detection signal is successful!')

            mode_list = mode_str.split('/')

            for mode in mode_list:
                # 停止功能函数接口
                global_element.Test_modulation = mode

                global_element.CU_intance.set_lte_ul_modeandRB(mode, '1')
                global_element.Test_lte_RB = 'RB: 1'
                global_element.CU_intance.set_lte_ul_RBoffset('LOW')

                # # 检查Handover后连接是否正常
                # time.sleep(2)
                # state = global_element.CU_intance.lte_connect_state()
                # if state == False:
                #     global_element.testseq_judgement_list.append('Inconclusive')
                #     return

                # 开始SA的设置
                global_element.SA_intance.settrace('1', 'AVE')
                global_element.SA_intance.sweepconfig(True, True, '', '', '')

                # 停止功能函数接口
                time.sleep(1)


                result = global_element.SA_intance.ltefcc_cse_set(global_element.Test_band)

                global_element.Test_remark = 'Reference screenshot of this result!'
                if result == '1':
                    report_handle.Reporttool('1', '-1', '1')
                elif result == 'NULL':
                    report_handle.Reporttool('NULL', '-1', '1')
                else:
                    report_handle.Reporttool('0', '-1', '1')

                # 截图
                picturepath = global_element.reportpath[:global_element.reportpath.index('.')]
                if not os.path.isdir(picturepath + '/LTE FCC/Conducted Spurious emissions'):
                    os.makedirs(picturepath + '/LTE FCC/Conducted Spurious emissions')

                picturepath_final = picturepath + '/LTE FCC/Conducted Spurious emissions/' + global_element.Test_band \
                                    + ' BW' + global_element.Test_lte_bandwidth + ' Channel' \
                                    + global_element.Test_channel + ' RB 1 ' + mode + '.JPG'
                global_element.SA_intance.PrtScn(picturepath_final)

                global_element.Test_remark = ''
                # 停止功能函数接口


def Frequencystability(testitem):
    if global_element.Test_lte_bandwidth == '10MHz':

        # 此项支持channel(10MHz 的 MID channel)
        channel_support_list = ['18900', '20175', '20525', '21100', '23095', '23790', '26365', '26865', '38000', '40620']

        if global_element.Test_channel in channel_support_list:

            global_element.Test_item = 'Frequency stability'
            global_element.emitsingle.stateupdataSingle.emit('Testing in progress of Frequency stability……,Band: %s，Bandwidth: %s, '
                                                         'Channel：%s' % (global_element.Test_band,
                                                                         global_element.Test_lte_bandwidth,
                                                                         global_element.Test_channel))
            # 停止功能函数接口

            # 将此项用户的参数初始化
            RB_str = testitem['parms']['Parm'][0]['Value']
            mode_str = testitem['parms']['Parm'][1]['Value']

            # 设置CU的线损
            dlfre, ulfre = report_handle.freq_gsm_calc(int(global_element.Test_channel))
            global_element.CU_intance.set_lte_loss(ulfre, dlfre)

            # 设置lte为最大功控
            global_element.CU_intance.set_lte_maxpower()

            global_element.CU_intance.set_lte_ul_modeandRB(mode_str, '1')
            global_element.CU_intance.set_lte_ul_RBoffset('LOW')
            global_element.Test_modulation = mode_str
            global_element.Test_lte_RB = 'RB: 1'
            time.sleep(2)

            # # 检查Handover后连接是否正常
            # time.sleep(2)
            # state = global_element.CU_intance.lte_connect_state()
            # if state == False:
            #     global_element.testseq_judgement_list.append('Inconclusive')
            #     return

            result = global_element.CU_intance.get_lte_frequencyerror(ulfre)

            global_element.Test_remark = 'Unit: ppm'

            report_handle.Reporttool(result, 'None', '2.5')

            global_element.Test_remark = ''

            # 停止功能函数接口

