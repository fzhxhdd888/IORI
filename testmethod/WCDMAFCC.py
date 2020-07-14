# !/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Author    : Feng Zhaohui
# @Time      : 2019/4/17
# @File      : WCDMAFCC.py
# @Funcyusa  :
# @Version   : 1.0

import global_element
import testseq_handle
import report_handle
import os


def initseting(init_parms_list):
    """
    WCDMAFCC模块initing的处理
    :param init_parms_list:
    :return:
    """
    # 更新测试band信息到全局变量
    global_element.Test_band = init_parms_list[0]['Value']

    # 更新BS LEVEL信息到全局变量
    global_element.Test_bslevel = init_parms_list[4]['Value']

    # 获取信道列表
    if global_element.Test_band == 'Band II':
        channel_str = init_parms_list[1]['Value']
    elif global_element.Test_band == 'Band IV':
        channel_str = init_parms_list[2]['Value']
    elif global_element.Test_band == 'Band V':
        channel_str = init_parms_list[3]['Value']
    channel_str_list = testseq_handle.channelstrtolist(channel_str)  # 将所有信道整理成字符串列表的形式

    # 获取mode
    mode_str = init_parms_list[5]['Value']

    return channel_str_list, mode_str


def Conductedoutputpower(testitem, mode_str):
    """
    :param testitem:
    :param mode_str:
    :return:
    """
    if global_element.Test_band == 'Band II' or global_element.Test_band == 'Band IV' \
            or global_element.Test_band == 'Band V':
        global_element.Test_item = 'Conducted output power'
        global_element.emitsingle.stateupdataSingle.emit('Testing in progress of Conducted output power……,Band: %s，Channel：%s' %
                                                         (global_element.Test_band, global_element.Test_channel))
        # 停止功能函数接口

        # 将此项用户的参数初始化
        att_gain = testitem['parms']['Parm']['Value']

        # 设置CU的线损
        dlfre, ulfre = report_handle.freq_gsm_calc(int(global_element.Test_channel))
        global_element.CU_intance.set_wcdma_loss(ulfre, dlfre)

        # RESET SA
        # global_element.SA_intance.resetself()

        # 设置SA的线损
        # global_element.SA_intance.set_loss(ulfre)

        # SA检查DUT是否有发射对应信号
        # global_element.SA_intance.check_gsm_signal()

        # 开始SA的设置

        # 取值
        if mode_str == 'WCDMA':
            ave_power = global_element.CU_intance.get_wcdma_power()
        # elif mode_str == 'GPRS' or mode_str == 'EGPRS':
        #     ave_power = global_element.CU_intance.get_gprs_power()
        global_element.Test_remark = 'Reporting Only'
        report_handle.Reporttool(ave_power, 'None', 'None')

        # 输出EIRP/ERP
        if global_element.Test_band == 'Band V':
            global_element.Test_item = 'ERP'
            activehighlimit = '38.45'            # <= 7W(38.45dBm)
            try:
                erp_result = str(format(eval(ave_power) + eval(att_gain) - 2.15, '.2f'))
            except:
                erp_result = 'NULL'
            global_element.Test_remark = 'ERP = Conducted Power + ATT gain(' + att_gain + ') - 2.15'
        elif global_element.Test_band == 'Band II':
            global_element.Test_item = 'EIRP'
            activehighlimit = '33'               # <= 2W(33dBm)
            try:
                erp_result = str(format(eval(ave_power) + eval(att_gain), '.2f'))
            except:
                erp_result = 'NULL'
            global_element.Test_remark = 'EIRP = Conducted Power + ATT gain(' + att_gain + ')'
        elif global_element.Test_band == 'Band IV':
            global_element.Test_item = 'EIRP'
            activehighlimit = '30'  # <= 1W(30dBm)
            try:
                erp_result = str(format(eval(ave_power) + eval(att_gain), '.2f'))
            except:
                erp_result = 'NULL'
            global_element.Test_remark = 'EIRP = Conducted Power + ATT gain(' + att_gain + ')'

        report_handle.Reporttool(erp_result, 'None', activehighlimit)
        global_element.Test_remark = ''

        # 停止功能函数接口


def peaktoaverageratio(testitem, mode_str):
    if global_element.Test_band == 'Band II' or global_element.Test_band == 'Band IV' \
            or global_element.Test_band == 'Band V':
        global_element.Test_item = 'Peak-to-Average Ratio'
        global_element.emitsingle.stateupdataSingle.emit('Testing in progress of Peak-to-Average Ratio……,Band: %s，Channel：%s' %
                                                         (global_element.Test_band, global_element.Test_channel))
        # 停止功能函数接口

        # 将此项用户的参数初始化
        # att_gain = item_dict['parms']['Parm']['Value']

        # 设置CU的线损
        dlfre, ulfre = report_handle.freq_gsm_calc(int(global_element.Test_channel))
        global_element.CU_intance.set_wcdma_loss(ulfre, dlfre)

        # RESET SA
        global_element.SA_intance.resetself()

        # 设置SA的线损
        global_element.SA_intance.set_loss(ulfre)

        global_element.CU_intance.set_wcdma_pcl_max()

        # SA检查DUT是否有发射对应信号
        result = global_element.SA_intance.check_gsm_signal()
        if result == False:
            global_element.Test_remark = 'SA did not detect the signal!'
            report_handle.Reporttool('NULL', 'None', '13')
            global_element.Test_remark = ''
        else:
            global_element.emitsingle.stateupdataSingle.emit('SA detection signal is successful!')

            # 开始SA的设置
            global_element.SA_intance.set_reflevel('40')
            global_element.SA_intance.setcenterfrequency(ulfre)
            global_element.SA_intance.setRbwVbw('1', '3')
            global_element.SA_intance.setspan('1')
            global_element.SA_intance.settrace('1', 'MAX')
            global_element.SA_intance.setdetector('RMS')
            global_element.SA_intance.sweepconfig(False, True, '', '200', '')

            # 停止功能函数接口

            result = global_element.SA_intance.CCDFON_and_get_value()

            global_element.Test_remark = 'Unit: dB'
            # 取值
            report_handle.Reporttool(result, 'None', '13')

            # 截图
            picturepath = global_element.reportpath[:global_element.reportpath.index('.')]
            if not os.path.isdir(picturepath + '/WCDMA FCC/Peak-to-Average Ratio'):
                os.makedirs(picturepath + '/WCDMA FCC/Peak-to-Average Ratio')

            picturepath_final = picturepath + '/WCDMA FCC/Peak-to-Average Ratio/' + mode_str + ' ' + global_element.Test_band \
                                + ' Channel' + global_element.Test_channel + '.JPG'
            global_element.SA_intance.PrtScn(picturepath_final)

            global_element.SA_intance.CCDFOFF()

            global_element.Test_remark = ''

            # 停止功能函数接口


def pct99OccupiedBandwidth(testitem, mode_str):
    if global_element.Test_band == 'Band II' or global_element.Test_band == 'Band IV' \
            or global_element.Test_band == 'Band V':
        global_element.Test_item = '99% Occupied Bandwidth'
        global_element.emitsingle.stateupdataSingle.emit('Testing in progress of 99pct Occupied Bandwidth……,Band: %s，Channel：%s' %
                                                         (global_element.Test_band, global_element.Test_channel))
        # 停止功能函数接口

        # 将此项用户的参数初始化
        # 此项没有用户自定义参数

        # 设置CU的线损
        dlfre, ulfre = report_handle.freq_gsm_calc(int(global_element.Test_channel))
        global_element.CU_intance.set_wcdma_loss(ulfre, dlfre)

        # RESET SA
        global_element.SA_intance.resetself()

        # 设置SA的线损
        global_element.SA_intance.set_loss(ulfre)

        global_element.CU_intance.set_wcdma_pcl_max()

        # SA检查DUT是否有发射对应信号
        result = global_element.SA_intance.check_gsm_signal()
        if result == False:
            global_element.Test_remark = 'SA did not detect the signal!'
            report_handle.Reporttool('NULL', 'None', 'None')
            global_element.Test_remark = ''
        else:
            global_element.emitsingle.stateupdataSingle.emit('SA detection signal is successful!')

            # 开始SA的设置

            global_element.SA_intance.set_reflevel('30')
            global_element.SA_intance.setcenterfrequency(ulfre)
            global_element.SA_intance.setRbwVbw('0.1', '0.3')
            global_element.SA_intance.setspan('10')
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
            report_handle.Reporttool(OBW_final, 'None', 'None')

            # 截图
            picturepath = global_element.reportpath[:global_element.reportpath.index('.')]
            if not os.path.isdir(picturepath + '/WCDMA FCC/99% Occupied Bandwidth'):
                os.makedirs(picturepath + '/WCDMA FCC/99% Occupied Bandwidth')

            picturepath_final = picturepath + '/WCDMA FCC/99% Occupied Bandwidth/' + mode_str + ' ' \
                                + global_element.Test_band + ' Channel' + global_element.Test_channel + '.JPG'
            global_element.SA_intance.PrtScn(picturepath_final)

            global_element.Test_remark = ''

            # 停止功能函数接口


def dB26OccupiedBandwidth(testitem, mode_str):
    if global_element.Test_band == 'Band II' or global_element.Test_band == 'Band IV' \
            or global_element.Test_band == 'Band V':
        global_element.Test_item = '26dB Occupied Bandwidth'
        global_element.emitsingle.stateupdataSingle.emit('Testing in progress of 26dB Occupied Bandwidth……,Band: %s，Channel：%s' %
                                                         (global_element.Test_band, global_element.Test_channel))
        # 停止功能函数接口

        # 将此项用户的参数初始化
        # 此项没有用户自定义参数

        # 设置CU的线损
        dlfre, ulfre = report_handle.freq_gsm_calc(int(global_element.Test_channel))
        global_element.CU_intance.set_wcdma_loss(ulfre, dlfre)

        # RESET SA
        global_element.SA_intance.resetself()

        # 设置SA的线损
        global_element.SA_intance.set_loss(ulfre)

        global_element.CU_intance.set_wcdma_pcl_max()

        # SA检查DUT是否有发射对应信号
        result = global_element.SA_intance.check_gsm_signal()
        if result == False:
            global_element.Test_remark = 'SA did not detect the signal!'
            report_handle.Reporttool('NULL', 'None', 'None')
            global_element.Test_remark = ''
        else:
            global_element.emitsingle.stateupdataSingle.emit('SA detection signal is successful!')

            # 开始SA的设置

            global_element.SA_intance.set_reflevel('30')
            global_element.SA_intance.setcenterfrequency(ulfre)
            global_element.SA_intance.setRbwVbw('0.1', '0.3')
            global_element.SA_intance.setspan('10')
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
            report_handle.Reporttool(OBW_final, 'None', 'None')

            # 截图
            picturepath = global_element.reportpath[:global_element.reportpath.index('.')]
            if not os.path.isdir(picturepath + '/WCDMA FCC/26dB Occupied Bandwidth'):
                os.makedirs(picturepath + '/WCDMA FCC/26dB Occupied Bandwidth')

            picturepath_final = picturepath + '/WCDMA FCC/26dB Occupied Bandwidth/' + mode_str + ' ' \
                                + global_element.Test_band + ' Channel' + global_element.Test_channel + '.JPG'
            global_element.SA_intance.PrtScn(picturepath_final)

            global_element.Test_remark = ''

            # 停止功能函数接口


def Bandedge(testitem, mode_str):
    if global_element.Test_band == 'Band II' or global_element.Test_band == 'Band IV' \
            or global_element.Test_band == 'Band V':
        if global_element.Test_channel == '9262' or global_element.Test_channel == '9538' or \
                global_element.Test_channel == '1312' or global_element.Test_channel == '1513' or \
                global_element.Test_channel == '4132' or global_element.Test_channel == '4233':
            global_element.Test_item = 'Band edge'
            global_element.emitsingle.stateupdataSingle.emit('Testing in progress of Band edge……,Band: %s，Channel：%s' %
                                                         (global_element.Test_band, global_element.Test_channel))
            # 停止功能函数接口

            # 将此项用户的参数初始化
            # 此项没有用户自定义参数

            # 设置CU的线损
            dlfre, ulfre = report_handle.freq_gsm_calc(int(global_element.Test_channel))
            global_element.CU_intance.set_wcdma_loss(ulfre, dlfre)

            # RESET SA
            global_element.SA_intance.resetself()

            # 设置SA的线损
            global_element.SA_intance.set_loss(ulfre)

            global_element.CU_intance.set_wcdma_pcl_max()

            # SA检查DUT是否有发射对应信号
            result = global_element.SA_intance.check_gsm_signal()
            if result == False:
                global_element.Test_remark = 'SA did not detect the signal!'
                report_handle.Reporttool('NULL', 'None', 'None')
                global_element.Test_remark = ''
            else:
                global_element.emitsingle.stateupdataSingle.emit('SA detection signal is successful!')

                # 开始SA的设置
                global_element.SA_intance.settrace('1', 'MAX')
                global_element.SA_intance.sweepconfig(True, True, '', '', '')

                # 停止功能函数接口

                result = global_element.SA_intance.wcdmafcc_Spurious_set(global_element.Test_channel)

                global_element.Test_remark = 'Reference screenshot of this result!'
                if result == '1':
                    report_handle.Reporttool('1', '-1', '1')
                else:
                    report_handle.Reporttool('0', '-1', '1')

                # 截图
                picturepath = global_element.reportpath[:global_element.reportpath.index('.')]
                if not os.path.isdir(picturepath + '/WCDMA FCC/Band edge'):
                    os.makedirs(picturepath + '/WCDMA FCC/Band edge')

                picturepath_final = picturepath + '/WCDMA FCC/Band edge/' + mode_str + ' ' + global_element.Test_band \
                                    + ' Channel' + global_element.Test_channel + '.JPG'
                global_element.SA_intance.PrtScn(picturepath_final)

                global_element.Test_remark = ''

                # 停止功能函数接口


def ConductedSpuriousemissions(testitem, mode_str):
    # 停止功能函数接口
    if global_element.Test_band == 'Band II' or global_element.Test_band == 'Band IV' \
            or global_element.Test_band == 'Band V':
        global_element.Test_item = 'Conducted Spurious emissions'
        global_element.emitsingle.stateupdataSingle.emit('Testing in progress of Conducted Spurious emissions……,Band: %s，Channel：%s' %
                                                         (global_element.Test_band, global_element.Test_channel))
        # 停止功能函数接口

        # 将此项用户的参数初始化
        # 此项没有用户自定义参数

        # 设置CU的线损
        dlfre, ulfre = report_handle.freq_gsm_calc(int(global_element.Test_channel))
        global_element.CU_intance.set_wcdma_loss(ulfre, dlfre)

        # RESET SA
        global_element.SA_intance.resetself()

        # 设置SA的线损
        global_element.SA_intance.set_loss(ulfre)

        global_element.CU_intance.set_wcdma_pcl_max()

        # SA检查DUT是否有发射对应信号
        result = global_element.SA_intance.check_gsm_signal()
        if result == False:
            global_element.Test_remark = 'SA did not detect the signal!'
            report_handle.Reporttool('NULL', 'None', 'None')
            global_element.Test_remark = ''
        else:
            global_element.emitsingle.stateupdataSingle.emit('SA detection signal is successful!')

            # 开始SA的设置
            global_element.SA_intance.settrace('1', 'MAX')
            global_element.SA_intance.sweepconfig(True, True, '', '', '')

            # 停止功能函数接口

            result = global_element.SA_intance.wcdmafcc_cse_set(global_element.Test_band)

            global_element.Test_remark = 'Reference screenshot of this result!'
            if result == '1':
                report_handle.Reporttool('1', '-1', '1')
            else:
                report_handle.Reporttool('0', '-1', '1')

            # 截图
            picturepath = global_element.reportpath[:global_element.reportpath.index('.')]
            if not os.path.isdir(picturepath + '/WCDMA FCC/Conducted Spurious emissions'):
                os.makedirs(picturepath + '/WCDMA FCC/Conducted Spurious emissions')

            picturepath_final = picturepath + '/WCDMA FCC/Conducted Spurious emissions/' + mode_str \
                                + ' ' + global_element.Test_band + ' Channel' + global_element.Test_channel + '.JPG'
            global_element.SA_intance.PrtScn(picturepath_final)

            global_element.Test_remark = ''

            # 停止功能函数接口


def Frequencystability(testitem, mode_str):
    if global_element.Test_band == 'Band II' or global_element.Test_band == 'Band IV' \
            or global_element.Test_band == 'Band V':
        global_element.Test_item = 'Frequency stability'
        global_element.emitsingle.stateupdataSingle.emit('Testing in progress of Frequency stability……,Band: %s，Channel：%s' %
                                                         (global_element.Test_band, global_element.Test_channel))
        # 停止功能函数接口

        # 将此项用户的参数初始化
        # 此项没有用户自定义参数

        # 设置CU的线损
        dlfre, ulfre = report_handle.freq_gsm_calc(int(global_element.Test_channel))
        global_element.CU_intance.set_wcdma_loss(ulfre, dlfre)

        # 停止功能函数接口

        if mode_str == 'WCDMA':
            result = global_element.CU_intance.get_wcdma_frequencyerror(ulfre)

        global_element.Test_remark = 'Unit: ppm'

        report_handle.Reporttool(result, 'None', '2.5')

        global_element.Test_remark = ''

        # 停止功能函数接口
