# !/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Author    : Feng Zhaohui
# @Time      : 2019/8/22 10:06 
# @File      : LTECAFCC.py 
# @Software  : PyCharm
# @Version   : 1.0

import global_element
import report_handle
import time
import os


def initseting(init_parms_list):
    """
    LTECAFCC模块initing的处理
    :param init_parms_list:
    :return:
    """
    # 更新测试band信息到全局变量
    global_element.Test_band = init_parms_list[0]['Value']

    # 更新BS LEVEL信息到全局变量
    global_element.Test_bslevel = init_parms_list[1]['Value']

    # 获取带宽组合和信道组合列表
    bw_channel_dict = global_element.lte_ca_channel_fortest_dict[global_element.Test_band]
    bw_list = []
    channel_list = []
    for index, key in enumerate(bw_channel_dict):
        if bw_channel_dict[key] != '':
            bw_list.append(key)
            channel_list.append(bw_channel_dict[key])

    return bw_list, channel_list


def ConductedPowerandEIRP(testitem):
    global_element.Test_item = 'Conducted Power and EIRP'
    global_element.emitsingle.stateupdataSingle.emit(
        'Testing in progress of Conducted Power and EIRP……, Band: %s，Bandwidth: %s, '
        'Channel：%s' % (global_element.Test_band,
                        global_element.Test_lte_bandwidth,
                        global_element.Test_channel))

    # 将此项用户的参数初始化
    att_gain = testitem['parms']['Parm'][0]['Value']
    mode_str = testitem['parms']['Parm'][1]['Value']
    low_limit_5b = testitem['limits']['limit'][0]['low']
    high_limit_5b = testitem['limits']['limit'][0]['high']
    low_limit_12b = testitem['limits']['limit'][1]['low']
    high_limit_12b = testitem['limits']['limit'][1]['high']
    low_limit_2_7_38_41c = testitem['limits']['limit'][2]['low']
    high_limit_2_7_38_41c = testitem['limits']['limit'][2]['high']

    # 设置CU的线损
    test_channel = global_element.Test_channel.split(',')[0].split('|')[1]
    dlfre, ulfre = report_handle.freq_gsm_calc(int(test_channel))
    global_element.CU_intance.set_lteca_loss(ulfre, dlfre)

    # 处理RB设置
    bw_group = [x.split('|')[1] for x in global_element.Test_lte_bandwidth.split(',')]
    rb_group = [str(eval(bw_group[0]) * 5), str(eval(bw_group[1]) * 5)]         # 带宽组合的最大RB数

    # 处理需要测试的调制方式
    mode_list = mode_str.split('/')

    for modetype in mode_list:
        # 更新全局变量
        global_element.Test_modulation = modetype
        # 配置CU mode type
        for i in range(3):              # RB有两种配置需要测试，循环两次
            if i == 0:                  # 第一次，PCC:RB1#MAX,SCC1:RB1#0
                # 更新全局变量
                global_element.Test_lte_RB = 'PCC:RB1#MAX,SCC1:RB1#0'
                # 配置CU调制方式和RB数据
                global_element.CU_intance.set_lteca_ul_modeandRB([modetype, modetype], ['1', '1'])

                # 配置CU RB位置
                global_element.CU_intance.set_lteca_ul_RBoffset(['HIGH', 'LOW'])
            elif i == 1:                  # 第二次，PCC:RB1#0,SCC1:RB1#MAX
                # 更新全局变量
                global_element.Test_lte_RB = 'PCC:RB1#0,SCC1:RB1#MAX'
                # 配置CU调制方式和RB数据
                global_element.CU_intance.set_lteca_ul_modeandRB([modetype, modetype], ['1', '1'])

                # 配置CU RB位置
                global_element.CU_intance.set_lteca_ul_RBoffset(['LOW', 'HIGH'])
            else:                       # 第三次，PCC:FRB#0,SCC1:FRB#0
                # 更新全局变量
                global_element.Test_lte_RB = 'PCC:FRB#0,SCC1:FRB#0'
                # 配置CU调制方式和RB数据
                global_element.CU_intance.set_lteca_ul_modeandRB([modetype, modetype], rb_group)
                # 配置CU RB位置
                global_element.CU_intance.set_lteca_ul_RBoffset(['LOW', 'LOW'])

            global_element.CU_intance.set_lte_maxpower()
            # 取值
            power_result = global_element.CU_intance.get_lteca_power()

            global_element.Test_remark = 'Reporting Only'
            report_handle.Reporttool(power_result, 'None', 'None')

            # 输出EIRP/ERP
            if global_element.Test_band == 'CA_5B':
                global_element.Test_item = 'ERP'
                activehighlimit = high_limit_5b
                activelowlimit = low_limit_5b
                try:
                    erp_result = str(format(eval(power_result) + eval(att_gain) - 2.15, '.2f'))
                except:
                    erp_result = 'NULL'
                global_element.Test_remark = 'ERP = Conducted Power + ATT gain(' + att_gain + ') - 2.15'
            elif global_element.Test_band == 'CA_12B':
                global_element.Test_item = 'ERP'
                activehighlimit = high_limit_12b
                activelowlimit = low_limit_12b
                try:
                    erp_result = str(format(eval(power_result) + eval(att_gain) - 2.15, '.2f'))
                except:
                    erp_result = 'NULL'
                global_element.Test_remark = 'ERP = Conducted Power + ATT gain(' + att_gain + ') - 2.15'
            elif global_element.Test_band in ['CA_2C', 'CA_7C', 'CA_38C', 'CA_41C']:
                global_element.Test_item = 'EIRP'
                activehighlimit = high_limit_2_7_38_41c
                activelowlimit = low_limit_2_7_38_41c
                try:
                    erp_result = str(format(eval(power_result) + eval(att_gain), '.2f'))
                except:
                    erp_result = 'NULL'
                global_element.Test_remark = 'EIRP = Conducted Power + ATT gain(' + att_gain + ')'

            report_handle.Reporttool(erp_result, activelowlimit, activehighlimit)
            global_element.Test_item = 'Conducted output power'
            global_element.Test_remark = ''


def pct99bw(testitem):
    global_element.Test_item = '99% Occupied Bandwidth'
    global_element.emitsingle.stateupdataSingle.emit(
        'Testing in progress of 99pct Occupied Bandwidth……, Band: %s，Bandwidth: %s, '
        'Channel：%s' % (global_element.Test_band,
                        global_element.Test_lte_bandwidth,
                        global_element.Test_channel))

    # 将此项用户的参数初始化
    mode_str = testitem['parms']['Parm']['Value']
    low_limit = testitem['limits']['limit']['low']
    high_limit = testitem['limits']['limit']['high']

    # 设置CU的线损
    test_channel = global_element.Test_channel.split(',')[0].split('|')[1]
    dlfre, ulfre = report_handle.freq_gsm_calc(int(test_channel))
    global_element.CU_intance.set_lteca_loss(ulfre, dlfre)

    # SA设置
    # RESET SA
    global_element.SA_intance.resetself()

    # 设置SA的线损
    global_element.SA_intance.set_loss(ulfre)

    # 设置lte为最大功控
    global_element.CU_intance.set_lte_maxpower()

    # SA检查DUT是否有发射对应信号
    result = global_element.SA_intance.check_lteca_signal()
    if result == False:
        global_element.Test_remark = 'SA did not detect the signal!'
        report_handle.Reporttool('NULL', low_limit, high_limit)
        global_element.Test_remark = ''
    else:
        global_element.emitsingle.stateupdataSingle.emit('SA detection signal is successful!')

        # 处理RB设置
        bw_group = [x.split('|')[1] for x in global_element.Test_lte_bandwidth.split(',')]
        rb_group = [str(eval(bw_group[0]) * 5), str(eval(bw_group[1]) * 5)]  # 带宽组合的最大RB数

        SA_span = format((eval(bw_group[0]) + eval(bw_group[1])) * 1.4, '.1f')   # 设置SA的SPAN为两个CC带宽之和的1.4倍

        # 设置SA的中心频率为两个CC的中心
        pcc_test_channel = global_element.Test_channel.split(',')[0].split('|')[1]
        scc_test_channle = global_element.Test_channel.split(',')[1].split('|')[1]
        pcc_dlfre, pcc_ulfre = report_handle.freq_gsm_calc(int(pcc_test_channel))
        scc_dlfre, scc_ulfre = report_handle.freq_gsm_calc(int(scc_test_channle))
        SA_centerfreq = format((eval(pcc_ulfre) - eval(bw_group[0]) / 2 + eval(scc_ulfre) + eval(bw_group[1]) / 2) / 2,
                               '.2f')

        # 处理需要测试的调制方式
        mode_list = mode_str.split('/')

        for modetype in mode_list:
            # 更新全局变量
            global_element.Test_modulation = modetype
            # 配置CU mode type
            # 更新全局变量
            global_element.Test_lte_RB = 'PCC:FRB#0,SCC1:FRB#0'
            # 配置CU调制方式和RB数据
            global_element.CU_intance.set_lteca_ul_modeandRB([modetype, modetype], rb_group)
            # 配置CU RB位置
            global_element.CU_intance.set_lteca_ul_RBoffset(['LOW', 'LOW'])

            time.sleep(2)

            # 开始SA设置
            global_element.SA_intance.set_reflevel('30')
            global_element.SA_intance.setcenterfrequency(SA_centerfreq)
            global_element.SA_intance.setRbwVbw('1', '3')
            global_element.SA_intance.setspan(SA_span)
            global_element.SA_intance.settrace('1', 'MAX')
            global_element.SA_intance.setdetector('AVERAGE')
            global_element.SA_intance.sweepconfig(True, True, '', '', '')

            OBW = global_element.SA_intance.pctBW('99')  # 取99%带宽值
            OBW_final = format(eval(OBW) / 1000, '.2f')

            # 停止功能函数接口

            global_element.SA_intance.markertotrace('1', '1')
            global_element.SA_intance.markertopeak('1')

            global_element.Test_remark = 'Uint: MHz'
            report_handle.Reporttool(OBW_final, low_limit, high_limit)

            # 截图
            picturepath = global_element.reportpath[:global_element.reportpath.index('.')]
            if not os.path.isdir(picturepath + '/LTE CA FCC/99% Occupied Bandwidth'):
                os.makedirs(picturepath + '/LTE CA FCC/99% Occupied Bandwidth')

            channel_str = global_element.Test_channel.replace(',', '')
            channel_str_final = channel_str.replace('|', '')

            bw_str = global_element.Test_lte_bandwidth.replace(',', '')
            bw_str_final = bw_str.replace('|', '')

            picturepath_final = picturepath + '/LTE CA FCC/99% Occupied Bandwidth/' + global_element.Test_band + \
                                ' BW' + bw_str_final + ' Channel' + channel_str_final + \
                                ' P_FRB S_FRB ' + modetype + '.JPG'
            global_element.SA_intance.PrtScn(picturepath_final)

            global_element.Test_remark = ''


def dB26OccupiedBandwidth(testitem):
    global_element.Test_item = '26dB Occupied Bandwidth'
    global_element.emitsingle.stateupdataSingle.emit(
        'Testing in progress of 26dB Occupied Bandwidth……,Band: %s，Bandwidth: %s, '
        'Channel：%s' % (global_element.Test_band,
                        global_element.Test_lte_bandwidth,
                        global_element.Test_channel))

    # 将此项用户的参数初始化
    mode_str = testitem['parms']['Parm']['Value']
    activelowlimit = testitem['limits']['limit']['low']
    activehighlimit = testitem['limits']['limit']['high']

    # 设置CU的线损
    test_channel = global_element.Test_channel.split(',')[0].split('|')[1]
    dlfre, ulfre = report_handle.freq_gsm_calc(int(test_channel))
    global_element.CU_intance.set_lte_loss(ulfre, dlfre)

    # RESET SA
    global_element.SA_intance.resetself()

    # 设置SA的线损
    global_element.SA_intance.set_loss(ulfre)

    # 设置lte为最大功控
    global_element.CU_intance.set_lte_maxpower()

    # SA检查DUT是否有发射对应信号
    result = global_element.SA_intance.check_lteca_signal()
    if result == False:
        global_element.Test_remark = 'SA did not detect the signal!'
        report_handle.Reporttool('NULL', activelowlimit, activehighlimit)
        global_element.Test_remark = ''
    else:
        global_element.emitsingle.stateupdataSingle.emit('SA detection signal is successful!')

        # 处理RB设置
        bw_group = [x.split('|')[1] for x in global_element.Test_lte_bandwidth.split(',')]
        rb_group = [str(eval(bw_group[0]) * 5), str(eval(bw_group[1]) * 5)]  # 带宽组合的最大RB数

        SA_span = format((eval(bw_group[0]) + eval(bw_group[1])) * 1.4, '.1f')  # 设置SA的SPAN为两个CC带宽之和的1.4倍

        # 设置SA的中心频率为两个CC的中心
        pcc_test_channel = global_element.Test_channel.split(',')[0].split('|')[1]
        scc_test_channle = global_element.Test_channel.split(',')[1].split('|')[1]
        pcc_dlfre, pcc_ulfre = report_handle.freq_gsm_calc(int(pcc_test_channel))
        scc_dlfre, scc_ulfre = report_handle.freq_gsm_calc(int(scc_test_channle))
        SA_centerfreq = format((eval(pcc_ulfre) - eval(bw_group[0]) / 2 + eval(scc_ulfre) + eval(bw_group[1]) / 2) / 2,
                               '.2f')

        # 处理需要测试的调制方式
        mode_list = mode_str.split('/')

        for modetype in mode_list:
            # 更新全局变量
            global_element.Test_modulation = modetype

            # 配置CU mode type
            # 更新全局变量
            global_element.Test_lte_RB = 'PCC:FRB#0,SCC1:FRB#0'
            # 配置CU调制方式和RB数据
            global_element.CU_intance.set_lteca_ul_modeandRB([modetype, modetype], rb_group)
            # 配置CU RB位置
            global_element.CU_intance.set_lteca_ul_RBoffset(['LOW', 'LOW'])

            time.sleep(2)

            # 开始SA设置
            global_element.SA_intance.set_reflevel('30')
            global_element.SA_intance.setcenterfrequency(SA_centerfreq)
            global_element.SA_intance.setRbwVbw('1', '3')
            global_element.SA_intance.setspan(SA_span)
            global_element.SA_intance.settrace('1', 'MAX')
            global_element.SA_intance.setdetector('AVERAGE')
            global_element.SA_intance.sweepconfig(True, True, '', '', '')

            global_element.SA_intance.markertotrace('1', '1')
            global_element.SA_intance.markertopeak('1')

            OBW = global_element.SA_intance.NDBDBW('26')  # 取26 dB带宽值
            OBW_final = format(eval(OBW) / 1000, '.2f')

            global_element.Test_remark = 'Uint: MHz'
            report_handle.Reporttool(OBW_final, activelowlimit, activehighlimit)

            # 截图
            picturepath = global_element.reportpath[:global_element.reportpath.index('.')]
            if not os.path.isdir(picturepath + '/LTE CA FCC/26dB Occupied Bandwidth'):
                os.makedirs(picturepath + '/LTE CA FCC/26dB Occupied Bandwidth')

            channel_str = global_element.Test_channel.replace(',', '')
            channel_str_final = channel_str.replace('|', '')
            bw_str = global_element.Test_lte_bandwidth.replace(',', '')
            bw_str_final = bw_str.replace('|', '')

            picturepath_final = picturepath + '/LTE CA FCC/26dB Occupied Bandwidth/' + global_element.Test_band + \
                                ' BW' + bw_str_final + ' Channel' + channel_str_final + \
                                ' P_FRB S_FRB ' + modetype + '.JPG'
            global_element.SA_intance.PrtScn(picturepath_final)

            global_element.Test_remark = ''


def bandedge(testitem):
    support_channel_group = [['18633', '18750'], ['18700', '18817'], ['18653', '18773'], ['18675', '18795'],
                             ['18655', '18799'], ['18700', '18844'], ['18675', '18825'], ['18678', '18849'],
                             ['18700', '18871'], ['18700', '18898'], ['20416', '20455'], ['20425', '20464'],
                             ['20428', '20500'], ['20450', '20522'], ['20450', '20549'], ['20805', '20949'],
                             ['20850', '20994'], ['20825', '20975'], ['20828', '20999'], ['20850', '21021'],
                             ['20850', '21048'], ['23035', '23083'], ['23035', '23107'], ['37825', '37975'],
                             ['37850', '38048'], ['39683', '39800'], ['39750', '39867'], ['39705', '39849'],
                             ['39750', '39894'], ['39725', '39875'], ['39728', '39899'], ['39750', '39921'],
                             ['39750', '39948'],
                             ['18983', '19100'], ['19050', '19167'], ['19005', '19125'], ['19027', '19147'],
                             ['18956', '19100'], ['19001', '19145'], ['18975', '19125'], ['18929', '19100'],
                             ['18951', '19122'], ['18902', '19100'], ['20586', '20625'], ['20595', '20634'],
                             ['20528', '20600'], ['20550', '20622'], ['20501', '20600'], ['21206', '21350'],
                             ['21251', '21395'], ['21225', '21375'], ['21179', '21350'], ['21201', '21372'],
                             ['21152', '21350'], ['23107', '23155'], ['23058', '23130'], ['38025', '38175'],
                             ['37952', '38150'], ['41373', '41490'], ['41440', '41557'], ['41346', '41490'],
                             ['41391', '41535'], ['41365', '41515'], ['41319', '41490'], ['41341', '41512'],
                             ['41292', '41490']]

    p_channel = global_element.Test_channel.split(',')[0].split('|')[1]
    s_channel = global_element.Test_channel.split(',')[1].split('|')[1]
    channel_group = [p_channel, s_channel]
    bw_group = [x.split('|')[1] for x in global_element.Test_lte_bandwidth.split(',')]
    if channel_group in support_channel_group:
        global_element.Test_item = 'Band edge'
        global_element.emitsingle.stateupdataSingle.emit('Testing in progressBand edge……,Band: %s，Bandwidth: %s, '
                                                         'Channel：%s' % (global_element.Test_band,
                                                                         global_element.Test_lte_bandwidth,
                                                                         global_element.Test_channel))

        # 将此项用户的参数初始化
        mode_str = testitem['parms']['Parm']['Value']

        # 设置CU的线损
        test_channel = global_element.Test_channel.split(',')[0].split('|')[1]
        dlfre, ulfre = report_handle.freq_gsm_calc(int(test_channel))
        global_element.CU_intance.set_lte_loss(ulfre, dlfre)

        # RESET SA
        global_element.SA_intance.resetself()

        # 设置SA的线损
        global_element.SA_intance.set_loss(ulfre)

        # 设置lte为最大功控
        global_element.CU_intance.set_lte_maxpower()

        # SA检查DUT是否有发射对应信号
        result = global_element.SA_intance.check_lteca_signal()
        if result == False:
            global_element.Test_remark = 'SA did not detect the signal!'
            report_handle.Reporttool('NULL', 'None', 'None')
            global_element.Test_remark = ''
        else:
            global_element.emitsingle.stateupdataSingle.emit('SA detection signal is successful!')

            mode_list = mode_str.split('/')

            for modetype in mode_list:
                # 更新全局变量
                global_element.Test_modulation = modetype

                for i in range(2):                            # 需要测试两种RB配置，循环两次
                    if i == 0:
                        # 更新全局变量
                        global_element.Test_lte_RB = 'PCC:1RB#0,SCC1:1RB#MAX'
                        # 配置CU调制方式和RB数据
                        global_element.CU_intance.set_lteca_ul_modeandRB([modetype, modetype], ['1', '1'])
                        # 配置CU RB位置
                        global_element.CU_intance.set_lteca_ul_RBoffset(['LOW', 'HIGH'])
                        rb_str = 'P_1RB#0 S_1RB#MAX'
                    else:
                        # 更新全局变量
                        global_element.Test_lte_RB = 'PCC:FRB#0,SCC1:FRB#0'
                        # 配置CU调制方式和RB数据
                        global_element.CU_intance.set_lteca_ul_modeandRB([modetype, modetype], [str(eval(bw_group[0]) * 5), str(eval(bw_group[1]) * 5)])
                        # 配置CU RB位置
                        global_element.CU_intance.set_lteca_ul_RBoffset(['LOW', 'LOW'])
                        rb_str = 'P_FRB S_FRB'

                    time.sleep(2)

                    # 开始SA的设置
                    global_element.SA_intance.settrace('1', 'MAX')
                    global_element.SA_intance.sweepconfig(True, True, '', '', '')

                    result = global_element.SA_intance.ltecafcc_bandedge_set(bw_group, channel_group)

                    global_element.Test_remark = 'Reference screenshot of this result!'
                    if result == '1':
                        report_handle.Reporttool('1', '-1', '1')
                    elif result == 'NULL':
                        report_handle.Reporttool('NULL', '-1', '1')
                    else:
                        report_handle.Reporttool('0', '-1', '1')

                    # 截图
                    picturepath = global_element.reportpath[:global_element.reportpath.index('.')]
                    if not os.path.isdir(picturepath + '/LTE CA FCC/Band edge'):
                        os.makedirs(picturepath + '/LTE CA FCC/Band edge')

                    channel_str = global_element.Test_channel.replace(',', '')
                    channel_str_final = channel_str.replace('|', '')
                    bw_str = global_element.Test_lte_bandwidth.replace(',', '')
                    bw_str_final = bw_str.replace('|', '')

                    picturepath_final = picturepath + '/LTE CA FCC/Band edge/' + global_element.Test_band + \
                                        ' BW' + bw_str_final + ' Channel' + channel_str_final + \
                                        ' ' + rb_str + ' ' + modetype + '.JPG'
                    global_element.SA_intance.PrtScn(picturepath_final)

                    global_element.Test_remark = ''


def OutofBandEmissions(testitem):
    global_element.Test_item = 'Out of Band Emissions'
    global_element.emitsingle.stateupdataSingle.emit(
        'Testing in progress of Out of Band Emissions……,Band: %s，Bandwidth: %s, '
        'Channel：%s' % (global_element.Test_band,
                        global_element.Test_lte_bandwidth,
                        global_element.Test_channel))

    # 将此项用户的参数初始化
    mode_str = testitem['parms']['Parm']['Value']

    # 设置CU的线损
    test_channel = global_element.Test_channel.split(',')[0].split('|')[1]
    dlfre, ulfre = report_handle.freq_gsm_calc(int(test_channel))
    global_element.CU_intance.set_lte_loss(ulfre, dlfre)

    # RESET SA
    global_element.SA_intance.resetself()

    # 设置SA的线损
    global_element.SA_intance.set_loss(ulfre)

    # 设置lte为最大功控
    global_element.CU_intance.set_lte_maxpower()

    # SA检查DUT是否有发射对应信号
    result = global_element.SA_intance.check_lteca_signal()
    if result == False:
        global_element.Test_remark = 'SA did not detect the signal!'
        report_handle.Reporttool('NULL', 'None', 'None')
        global_element.Test_remark = ''
    else:
        global_element.emitsingle.stateupdataSingle.emit('SA detection signal is successful!')

        mode_list = mode_str.split('/')

        for mode in mode_list:
            # 更新全局变量
            global_element.Test_modulation = mode

            # 配置CU mode type
            # 更新全局变量
            global_element.Test_lte_RB = 'PCC:1RB#MAX,SCC1:1RB#0'
            # 配置CU调制方式和RB数据
            global_element.CU_intance.set_lteca_ul_modeandRB([mode, mode], ['1', '1'])
            # 配置CU RB位置
            global_element.CU_intance.set_lteca_ul_RBoffset(['HIGH', 'LOW'])

            time.sleep(2)

            # 开始SA的设置
            global_element.SA_intance.settrace('1', 'AVE')
            global_element.SA_intance.sweepconfig(True, True, '', '', '')

            time.sleep(1)

            result = global_element.SA_intance.ltecafcc_cse_set(global_element.Test_band)

            global_element.Test_remark = 'Reference screenshot of this result!'
            if result == '1':
                report_handle.Reporttool('1', '-1', '1')
            elif result == 'NULL':
                report_handle.Reporttool('NULL', '-1', '1')
            else:
                report_handle.Reporttool('0', '-1', '1')

            channel_str = global_element.Test_channel.replace(',', '')
            channel_str_final = channel_str.replace('|', '')
            bw_str = global_element.Test_lte_bandwidth.replace(',', '')
            bw_str_final = bw_str.replace('|', '')
            rb_str = 'P_1RB#MAX S_1RB#0'

            # 截图
            picturepath = global_element.reportpath[:global_element.reportpath.index('.')]
            if not os.path.isdir(picturepath + '/LTE CA FCC/Out of Band Emissions'):
                os.makedirs(picturepath + '/LTE CA FCC/Out of Band Emissions')

            picturepath_final = picturepath + '/LTE CA FCC/Out of Band Emissions/' + global_element.Test_band + \
                                ' BW' + bw_str_final + ' Channel' + channel_str_final + \
                                ' ' + rb_str + ' ' + mode + '.JPG'
            global_element.SA_intance.PrtScn(picturepath_final)

            global_element.Test_remark = ''


def freq_error(testitem):
    global_element.Test_item = 'Frequency stability'
    global_element.emitsingle.stateupdataSingle.emit(
        'Testing in progress of Frequency stability……, Band: %s，Bandwidth: %s, '
        'Channel：%s' % (global_element.Test_band,
                        global_element.Test_lte_bandwidth,
                        global_element.Test_channel))

    # 将此项用户的参数初始化
    mode_str = testitem['parms']['Parm']['Value']

    # 设置CU的线损
    test_channel = global_element.Test_channel.split(',')[0].split('|')[1]
    dlfre, ulfre = report_handle.freq_gsm_calc(int(test_channel))
    global_element.CU_intance.set_lteca_loss(ulfre, dlfre)

    # # 处理RB设置
    # bw_group = [x.split('|')[1] for x in global_element.Test_lte_bandwidth.split(',')]
    # rb_group = [str(eval(bw_group[0]) * 5), str(eval(bw_group[1]) * 5)]         # 带宽组合的最大RB数

    # 处理需要测试的调制方式
    mode_list = mode_str.split('/')

    for modetype in mode_list:
        # 更新全局变量
        global_element.Test_modulation = modetype
        # 配置CU mode type

        # 更新全局变量
        global_element.Test_lte_RB = 'PCC:RB1#MAX,SCC1:RB1#0'
        # 配置CU调制方式和RB数据
        global_element.CU_intance.set_lteca_ul_modeandRB([modetype, modetype], ['1', '1'])

        # 配置CU RB位置
        global_element.CU_intance.set_lteca_ul_RBoffset(['HIGH', 'LOW'])

        global_element.CU_intance.set_lte_maxpower()

        # 取值
        fre_er_result = global_element.CU_intance.get_lteca_frequencyerror(ulfre)

        global_element.Test_remark = 'Unit: ppm'
        report_handle.Reporttool(fre_er_result, 'None', '20')

        global_element.Test_remark = ''


def peaktoaveragerate(testitem):
    # TODO:最终结果是否要减去Duty Cycle Factor
    global_element.Test_item = 'Peak-to-Average Ratio'
    global_element.emitsingle.stateupdataSingle.emit(
        'Testing in progress of Peak-to-Average Ratio……, Band: %s，Bandwidth: %s, '
        'Channel：%s' % (global_element.Test_band,
                        global_element.Test_lte_bandwidth,
                        global_element.Test_channel))

    # 将此项用户的参数初始化
    mode_str = testitem['parms']['Parm']['Value']
    low_limit = testitem['limits']['limit']['low']
    high_limit = testitem['limits']['limit']['high']

    # 设置CU的线损
    test_channel = global_element.Test_channel.split(',')[0].split('|')[1]
    dlfre, ulfre = report_handle.freq_gsm_calc(int(test_channel))
    global_element.CU_intance.set_lteca_loss(ulfre, dlfre)

    # 处理RB设置
    bw_group = [x.split('|')[1] for x in global_element.Test_lte_bandwidth.split(',')]
    rb_group = [str(eval(bw_group[0]) * 5), str(eval(bw_group[1]) * 5)]         # 带宽组合的最大RB数

    # 处理需要测试的调制方式
    mode_list = mode_str.split('/')

    for modetype in mode_list:
        # 更新全局变量
        global_element.Test_modulation = modetype
        # 配置CU mode type

        # 更新全局变量
        global_element.Test_lte_RB = 'PCC:FRB#0,SCC1:FRB#0'
        # 配置CU调制方式和RB数据
        global_element.CU_intance.set_lteca_ul_modeandRB([modetype, modetype], rb_group)

        # 配置CU RB位置
        global_element.CU_intance.set_lteca_ul_RBoffset(['LOW', 'LOW'])

        global_element.CU_intance.set_lte_maxpower()

        # 取值
        fre_er_result = global_element.CU_intance.get_lteca_ptar()

        global_element.Test_remark = 'Unit: dB'
        report_handle.Reporttool(fre_er_result, low_limit, high_limit)

        global_element.Test_remark = ''
