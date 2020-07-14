# !/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Author    : Feng Zhaohui
# @Time      : 2019/3/19
# @File      : GSMFCC.py
# @Funcyusa  :
# @Version   : 1.0

import global_element
import testseq_handle
import report_handle
import time
import os


def initseting(init_parms_list):
    """
        GSM模块initing的处理
        :param init_parms_list:
        :return:
        """
    # 更新测试band信息到全局变量
    global_element.Test_band = init_parms_list[0]['Value']

    # 更新BS LEVEL信息到全局变量
    global_element.Test_bslevel = init_parms_list[6]['Value']

    # 获取信道列表
    if global_element.Test_band == 'GSM850':
        channel_str = init_parms_list[1]['Value']
    elif global_element.Test_band == 'GSM900':
        channel_str = init_parms_list[2]['Value']
    elif global_element.Test_band == 'DCS1800':
        channel_str = init_parms_list[3]['Value']
    else:
        channel_str = init_parms_list[4]['Value']
    channel_str_list = testseq_handle.channelstrtolist(channel_str)  # 将所有信道整理成字符串列表的形式

    # 获取PCL列表
    pcl_str = init_parms_list[5]['Value']
    pcl_str_list = testseq_handle.channelstrtolist(pcl_str)  # 将所有pcl整理成字符串列表的形式

    # 获取mode
    mode_str = init_parms_list[7]['Value']

    return channel_str_list, pcl_str_list, mode_str


def Conductedoutputpower(item_dict, mode_str):
    if global_element.Test_band == 'GSM850' or global_element.Test_band == 'PCS1900':
        global_element.Test_item = 'Conducted output power'
        global_element.emitsingle.stateupdataSingle.emit('Testing in progress of Conducted output power……,Channel：%s，PCL：%s' %
                                                         (global_element.Test_channel, global_element.Test_pcl))
        # 停止功能函数接口

        # 将此项用户的参数初始化
        att_gain = item_dict['parms']['Parm']['Value']

        # 设置CU的线损
        dlfre, ulfre = report_handle.freq_gsm_calc(int(global_element.Test_channel))
        global_element.CU_intance.set_gms_loss(ulfre, dlfre)

        # RESET SA
        # global_element.SA_intance.resetself()

        # 设置SA的线损
        # global_element.SA_intance.set_loss(ulfre)

        # SA检查DUT是否有发射对应信号
        # global_element.SA_intance.check_gsm_signal()

        # 开始SA的设置

        # 取值
        if mode_str == 'GSM':
            ave_power = global_element.CU_intance.get_gsm_power()
        elif mode_str == 'GPRS' or mode_str == 'EGPRS':
            ave_power = global_element.CU_intance.get_gprs_power()
        global_element.Test_remark = 'Reporting Only'
        report_handle.Reporttool(ave_power, 'None', 'None')

        # 输出EIRP/ERP
        if global_element.Test_band == 'GSM850':
            global_element.Test_item = 'ERP'
            activehighlimit = '38.45'            # <= 7W(38.45dBm)
            try:
                erp_result = str(format(eval(ave_power) + eval(att_gain) - 2.15, '.2f'))
            except:
                erp_result = 'NULL'
            global_element.Test_remark = 'ERP = Conducted Power + ATT gain(' + att_gain + ') - 2.15'
        else:
            global_element.Test_item = 'EIRP'
            activehighlimit = '33'               # <= 2W(33dBm)
            try:
                erp_result = str(format(eval(ave_power) + eval(att_gain), '.2f'))
            except:
                erp_result = 'NULL'
            global_element.Test_remark = 'EIRP = Conducted Power + ATT gain(' + att_gain + ')'

        report_handle.Reporttool(erp_result, 'None', activehighlimit)
        global_element.Test_remark = ''

        # 停止功能函数接口


def peaktoaverageratio(item_dict, mode_str):
    if global_element.Test_band == 'GSM850' or global_element.Test_band == 'PCS1900':
        global_element.Test_item = 'Peak-to-Average Ratio'
        global_element.emitsingle.stateupdataSingle.emit('Testing in progress of Peak-to-Average Ratio,Channel：%s，PCL：%s' %
                                                         (global_element.Test_channel, global_element.Test_pcl))
        # 停止功能函数接口

        # 将此项用户的参数初始化
        # att_gain = item_dict['parms']['Parm']['Value']

        # 设置CU的线损
        dlfre, ulfre = report_handle.freq_gsm_calc(int(global_element.Test_channel))
        global_element.CU_intance.set_gms_loss(ulfre, dlfre)

        # RESET SA
        global_element.SA_intance.resetself()

        # 设置SA的线损
        global_element.SA_intance.set_loss(ulfre)

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
            global_element.SA_intance.sweepconfig(True, True, '', '', '')

            # 停止功能函数接口

            # global_element.SA_intance.startsweep()
            # global_element.SA_intance.sweepiscompleted('200')
            global_element.SA_intance.cont_sweep_seconds(5)

            # 停止功能函数接口

            global_element.SA_intance.settrace('1', 'VIEW')
            global_element.SA_intance.settrace('2', 'MAX')
            # global_element.SA_intance.startsweep()
            # time.sleep(0.5)
            # global_element.SA_intance.sweepiscompleted('200')
            global_element.SA_intance.cont_sweep_seconds(5)

            global_element.SA_intance.markertotrace('1', '1')
            global_element.SA_intance.markertopeak('1')

            global_element.SA_intance.markertotrace('2', '2')
            global_element.SA_intance.markertopeak('2')

            # 停止功能函数接口

            global_element.Test_remark = 'Unit: dB'
            # 取值
            marker1amp = global_element.SA_intance.marker_Y_value('1')
            marker2amp = global_element.SA_intance.marker_Y_value('2')
            amp_delta = format(float(marker2amp) - float(marker1amp), '.2f')

            report_handle.Reporttool(amp_delta, 'None', '13')

            # 截图
            picturepath = global_element.reportpath[:global_element.reportpath.index('.')]
            if not os.path.isdir(picturepath + '/GSM FCC/Peak-to-Average Ratio'):
                os.makedirs(picturepath + '/GSM FCC/Peak-to-Average Ratio')

            picturepath_final = picturepath + '/GSM FCC/Peak-to-Average Ratio/' + mode_str + ' ' + global_element.Test_band\
                                + ' Channel' + global_element.Test_channel + ' PCL' + global_element.Test_pcl + '.JPG'
            global_element.SA_intance.PrtScn(picturepath_final)

            global_element.Test_remark = ''

            # 停止功能函数接口


def pct99OccupiedBandwidth(item_dict, mode_str):
    if global_element.Test_band == 'GSM850' or global_element.Test_band == 'PCS1900':
        global_element.Test_item = '99% Occupied Bandwidth'
        global_element.emitsingle.stateupdataSingle.emit('Testing in progress of 99pct Occupied Bandwidth……,Channel：%s，PCL：%s' %
                                                         (global_element.Test_channel, global_element.Test_pcl))
        # 停止功能函数接口

        # 将此项用户的参数初始化
        # 此项没有用户自定义参数

        # 设置CU的线损
        dlfre, ulfre = report_handle.freq_gsm_calc(int(global_element.Test_channel))
        global_element.CU_intance.set_gms_loss(ulfre, dlfre)

        # RESET SA
        global_element.SA_intance.resetself()

        # 设置SA的线损
        global_element.SA_intance.set_loss(ulfre)

        # SA检查DUT是否有发射对应信号
        result = global_element.SA_intance.check_gsm_signal()
        if result == True:
            global_element.emitsingle.stateupdataSingle.emit('SA detection signal is successful!')
        else:
            return

        # 开始SA的设置

        global_element.SA_intance.set_reflevel('40')
        global_element.SA_intance.setcenterfrequency(ulfre)
        global_element.SA_intance.setRbwVbw('0.003', '0.01')
        global_element.SA_intance.setspan('1')
        global_element.SA_intance.settrace('1', 'MAX')
        global_element.SA_intance.setdetector('MAX PEAK')
        global_element.SA_intance.sweepconfig(True, True, '', '', '')

        # 停止功能函数接口

        OBW = global_element.SA_intance.pctBW('99')     # 取99%带宽值

        # 停止功能函数接口

        global_element.SA_intance.markertotrace('1', '1')
        global_element.SA_intance.markertopeak('1')

        global_element.Test_remark = 'Uint: kHz'
        report_handle.Reporttool(OBW, 'None', 'None')

        # 截图
        picturepath = global_element.reportpath[:global_element.reportpath.index('.')]
        if not os.path.isdir(picturepath + '/GSM FCC/99% Occupied Bandwidth'):
            os.makedirs(picturepath + '/GSM FCC/99% Occupied Bandwidth')

        picturepath_final = picturepath + '/GSM FCC/99% Occupied Bandwidth/' + mode_str + ' ' + global_element.Test_band\
                            + ' Channel' + global_element.Test_channel + ' PCL' + global_element.Test_pcl + '.JPG'
        global_element.SA_intance.PrtScn(picturepath_final)

        global_element.Test_remark = ''

        # 停止功能函数接口


def dB26OccupiedBandwidth(item_dict, mode_str):
    if global_element.Test_band == 'GSM850' or global_element.Test_band == 'PCS1900':
        global_element.Test_item = '26dB Occupied Bandwidth'
        global_element.emitsingle.stateupdataSingle.emit('Testing in progress of 26dB Occupied Bandwidth……,Channel：%s，PCL：%s' %
                                                         (global_element.Test_channel, global_element.Test_pcl))
        # 停止功能函数接口

        # 将此项用户的参数初始化
        # 此项没有用户自定义参数

        # 设置CU的线损
        dlfre, ulfre = report_handle.freq_gsm_calc(int(global_element.Test_channel))
        global_element.CU_intance.set_gms_loss(ulfre, dlfre)

        # RESET SA
        global_element.SA_intance.resetself()

        # 设置SA的线损
        global_element.SA_intance.set_loss(ulfre)

        # SA检查DUT是否有发射对应信号
        result = global_element.SA_intance.check_gsm_signal()
        if result == False:
            global_element.Test_remark = 'SA did not detect the signal!'
            report_handle.Reporttool('NULL', 'None', 'None')
            global_element.Test_remark = ''
        else:
            global_element.emitsingle.stateupdataSingle.emit('SA detection signal is successful! ')

            # 开始SA的设置

            global_element.SA_intance.set_reflevel('40')
            global_element.SA_intance.setcenterfrequency(ulfre)
            global_element.SA_intance.setRbwVbw('0.003', '0.01')
            global_element.SA_intance.setspan('1')
            global_element.SA_intance.settrace('1', 'MAX')
            global_element.SA_intance.setdetector('MAX PEAK')
            global_element.SA_intance.sweepconfig(True, True, '', '', '')

            global_element.SA_intance.markertotrace('1', '1')
            global_element.SA_intance.markertopeak('1')

            # 停止功能函数接口

            OBW = global_element.SA_intance.NDBDBW('26')     # 取26 dB带宽值

            global_element.Test_remark = 'Uint: kHz'
            report_handle.Reporttool(OBW, 'None', 'None')

            # 截图
            picturepath = global_element.reportpath[:global_element.reportpath.index('.')]
            if not os.path.isdir(picturepath + '/GSM FCC/26dB Occupied Bandwidth'):
                os.makedirs(picturepath + '/GSM FCC/26dB Occupied Bandwidth')

            picturepath_final = picturepath + '/GSM FCC/26dB Occupied Bandwidth/' + mode_str + ' ' \
                                + global_element.Test_band + ' Channel' + global_element.Test_channel \
                                + ' PCL' + global_element.Test_pcl + '.JPG'
            global_element.SA_intance.PrtScn(picturepath_final)

            global_element.Test_remark = ''

            # 停止功能函数接口


def Bandedge(item_dict, mode_str):
    if global_element.Test_band == 'GSM850' or global_element.Test_band == 'PCS1900':
        if global_element.Test_channel == '128' or global_element.Test_channel == '251' or \
                global_element.Test_channel == '512' or global_element.Test_channel == '810':
            global_element.Test_item = 'Band edge'
            global_element.emitsingle.stateupdataSingle.emit('Testing in progress of Band edge……,Channel：%s，PCL：%s' %
                                                             (global_element.Test_channel, global_element.Test_pcl))
            # 停止功能函数接口

            # 将此项用户的参数初始化
            # 此项没有用户自定义参数

            # 设置CU的线损
            dlfre, ulfre = report_handle.freq_gsm_calc(int(global_element.Test_channel))
            global_element.CU_intance.set_gms_loss(ulfre, dlfre)

            # RESET SA
            global_element.SA_intance.resetself()

            # 设置SA的线损
            global_element.SA_intance.set_loss(ulfre)

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

                result = global_element.SA_intance.gsmfcc_Spurious_set(global_element.Test_channel)

                global_element.Test_remark = 'Reference screenshot of this result!'
                if result == '1':
                    report_handle.Reporttool('1', '-1', '1')
                else:
                    report_handle.Reporttool('0', '-1', '1')

                # 截图
                picturepath = global_element.reportpath[:global_element.reportpath.index('.')]
                if not os.path.isdir(picturepath + '/GSM FCC/Band edge'):
                    os.makedirs(picturepath + '/GSM FCC/Band edge')

                picturepath_final = picturepath + '/GSM FCC/Band edge/' + mode_str + ' ' + global_element.Test_band \
                                    + ' Channel' + global_element.Test_channel + ' PCL' + global_element.Test_pcl + '.JPG'
                global_element.SA_intance.PrtScn(picturepath_final)

                global_element.Test_remark = ''

                # 停止功能函数接口


def ConductedSpuriousemissions(item_dict, mode_str):
    # 停止功能函数接口
    if global_element.Test_band == 'GSM850' or global_element.Test_band == 'PCS1900':
            global_element.Test_item = 'Conducted Spurious emissions'
            global_element.emitsingle.stateupdataSingle.emit('Testing in progress of Conducted Spurious emissions……,Channel：%s，PCL：%s' %
                                                             (global_element.Test_channel, global_element.Test_pcl))
            # 停止功能函数接口

            # 将此项用户的参数初始化
            # 此项没有用户自定义参数

            # 设置CU的线损
            dlfre, ulfre = report_handle.freq_gsm_calc(int(global_element.Test_channel))
            global_element.CU_intance.set_gms_loss(ulfre, dlfre)

            # RESET SA
            global_element.SA_intance.resetself()

            # 设置SA的线损
            global_element.SA_intance.set_loss(ulfre)

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

                result = global_element.SA_intance.gsmfcc_cse_set(global_element.Test_band)

                global_element.Test_remark = 'Reference screenshot of this result!'
                if result == '1':
                    report_handle.Reporttool('1', '-1', '1')
                else:
                    report_handle.Reporttool('0', '-1', '1')

                # 截图
                picturepath = global_element.reportpath[:global_element.reportpath.index('.')]
                if not os.path.isdir(picturepath + '/GSM FCC/Conducted Spurious emissions'):
                    os.makedirs(picturepath + '/GSM FCC/Conducted Spurious emissions')

                picturepath_final = picturepath + '/GSM FCC/Conducted Spurious emissions/' + mode_str \
                                    + ' ' + global_element.Test_band + ' Channel' + global_element.Test_channel + ' PCL' \
                                    + global_element.Test_pcl + '.JPG'
                global_element.SA_intance.PrtScn(picturepath_final)

                global_element.Test_remark = ''

            # 停止功能函数接口


def Frequencystability(item_dict, mode_str):
    if global_element.Test_band == 'GSM850' or global_element.Test_band == 'PCS1900':
        global_element.Test_item = 'Frequency stability'
        global_element.emitsingle.stateupdataSingle.emit('Testing in progress of Frequency stability……,Channel：%s，PCL：%s' %
                                                         (global_element.Test_channel, global_element.Test_pcl))
        # 停止功能函数接口

        # 将此项用户的参数初始化
        # 此项没有用户自定义参数

        # 设置CU的线损
        dlfre, ulfre = report_handle.freq_gsm_calc(int(global_element.Test_channel))
        global_element.CU_intance.set_gms_loss(ulfre, dlfre)

        # 停止功能函数接口

        if mode_str == 'GSM':
            result = global_element.CU_intance.get_gsm_freerror(ulfre)
        elif mode_str == 'GPRS' or mode_str == 'EGPRS':
            result = global_element.CU_intance.get_gprs_freerror(ulfre)

        global_element.Test_remark = 'Unit: ppm'

        report_handle.Reporttool(result, 'None', '2.5')

        global_element.Test_remark = ''

        # 停止功能函数接口
