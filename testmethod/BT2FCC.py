# !/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Author    : Feng Zhaohui
# @Time      : 2019/7/15
# @File      : BT2FCC.py
# @Funcyusa  :
# @Version   : 1.0

import global_element
import testseq_handle
import os
import time
import report_handle


def initseting(init_parms_list):
    """
    BT2FCC模块initing的处理
    :param init_parms_list:
    :return:
    """
    # 获取Channel信息
    channel_str = init_parms_list['Value']
    channel_str_list = testseq_handle.channelstrtolist(channel_str)  # 将所有信道整理成字符串列表的形式

    return channel_str_list


def db20_bandwidth(item_dict):
    packettype_str = item_dict['parms']['Parm']['Value']
    packettype_list = packettype_str.split('/')
    global_element.Test_item = '20dB bandwidth Channel'
    for packettype in packettype_list:
        global_element.Test_bt_packetype = packettype
        global_element.emitsingle.stateupdataSingle.emit('Testing in progress of 20dB bandwidth Channel: ' +
                                                         global_element.Test_channel + ' Packet Type: ' + packettype)

        # 设置 Packet Type, hopping type, pattern type
        global_element.CU_intance.set_bt_parms(packettype, False)

        ulfre = report_handle.fre_bt2_calc(global_element.Test_channel)
        if int(global_element.Test_channel) < 39:
            dlfre = '2480'
        else:
            dlfre = '2402'

        # 将此项用户的参数初始化
        low_limit = item_dict['limits']['limit']['low']
        high_limit = item_dict['limits']['limit']['high']

        # 设置CU的线损
        global_element.CU_intance.set_bt_loss(ulfre, dlfre)

        # RESET SA
        global_element.SA_intance.resetself()

        # 设置SA的线损
        global_element.SA_intance.set_loss(ulfre)

        # SA检查DUT是否有发射对应信号
        result = global_element.SA_intance.check_bt_signal()

        if result == False:
            global_element.Test_remark = 'SA did not detect the signal'
            report_handle.Reporttool('NULL', 'None', 'None')
            global_element.Test_remark = ''
        else:
            global_element.emitsingle.stateupdataSingle.emit('SA detection signal is successful!')

            # 开始SA的设置
            global_element.SA_intance.set_reflevel('20')
            global_element.SA_intance.setcenterfrequency(ulfre)
            global_element.SA_intance.setRbwVbw('0.03', '0.3')
            if packettype == 'DH5':
                global_element.SA_intance.setspan('2')
            else:
                global_element.SA_intance.setspan('3')
            global_element.SA_intance.settrace('1', 'MAX')
            global_element.SA_intance.setdetector('MAX PEAK')
            global_element.SA_intance.sweepconfig(True, True, '', '', '')

            global_element.SA_intance.markertotrace('1', '1')
            global_element.SA_intance.markertopeak('1')

            OBW = global_element.SA_intance.NDBDBW('20')     # 取20 dB带宽值
            dict_key = global_element.Test_channel + '_' + packettype
            global_element.BT2_fcc_20dbbw_result[dict_key] = OBW

            global_element.Test_remark = 'Uint: kHz'
            report_handle.Reporttool(OBW, low_limit, high_limit)

            # 截图
            picturepath = global_element.reportpath[:global_element.reportpath.index('.')]
            if not os.path.isdir(picturepath + '/BT2.0/FCC/20 dB BandWidth'):
                os.makedirs(picturepath + '/BT2.0/FCC/20 dB BandWidth')

            picturepath_final = picturepath + '/BT2.0/FCC/20 dB BandWidth/BT2.0 ' + packettype + ' CH' + \
                                global_element.Test_band + ' CH' + global_element.Test_channel + ' ' + ulfre + \
                                'MHz.JPG'
            global_element.SA_intance.PrtScn(picturepath_final)

            global_element.Test_remark = ''

            # 停止功能函数接口


def pct99BW(item_dict):
    packettype_str = item_dict['parms']['Parm']['Value']
    packettype_list = packettype_str.split('/')
    global_element.Test_item = '99% bandwidth'
    for packettype in packettype_list:
        global_element.Test_bt_packetype = packettype
        global_element.emitsingle.stateupdataSingle.emit('Testing in progress of 99% bandwidth: Channel ' +
                                                         global_element.Test_channel + ' Packet Type: ' + packettype)

        # 设置 Packet Type, hopping type, pattern type
        global_element.CU_intance.set_bt_parms(packettype, False)

        ulfre = report_handle.fre_bt2_calc(global_element.Test_channel)
        if int(global_element.Test_channel) < 39:
            dlfre = '2480'
        else:
            dlfre = '2402'

        # 将此项用户的参数初始化
        low_limit = item_dict['limits']['limit']['low']
        high_limit = item_dict['limits']['limit']['high']

        # 设置CU的线损
        global_element.CU_intance.set_bt_loss(ulfre, dlfre)

        # RESET SA
        global_element.SA_intance.resetself()

        # 设置SA的线损
        global_element.SA_intance.set_loss(ulfre)

        # SA检查DUT是否有发射对应信号
        result = global_element.SA_intance.check_bt_signal()

        if result == False:
            global_element.Test_remark = 'SA did not detect the signal!'
            report_handle.Reporttool('NULL', 'None', 'None')
            global_element.Test_remark = ''
        else:
            global_element.emitsingle.stateupdataSingle.emit('SA detection signal is successful!')

            # 开始SA的设置
            global_element.SA_intance.set_reflevel('20')
            global_element.SA_intance.setcenterfrequency(ulfre)
            global_element.SA_intance.setRbwVbw('0.03', '0.1')
            global_element.SA_intance.setspan('2')
            global_element.SA_intance.settrace('1', 'MAX')
            global_element.SA_intance.setdetector('SAMPLE')
            global_element.SA_intance.sweepconfig(True, True, '', '', '')

            OBW = global_element.SA_intance.pctBW('99')  # 取99%带宽值

            # 停止功能函数接口

            global_element.SA_intance.markertotrace('1', '1')
            global_element.SA_intance.markertopeak('1')

            global_element.Test_remark = 'Uint: kHz'
            report_handle.Reporttool(OBW, low_limit, high_limit)

            # 截图
            picturepath = global_element.reportpath[:global_element.reportpath.index('.')]
            if not os.path.isdir(picturepath + '/BT2.0/FCC/99% bandwidth'):
                os.makedirs(picturepath + '/BT2.0/FCC/99% bandwidth')

            picturepath_final = picturepath + '/BT2.0/FCC/99% bandwidth/BT2.0 ' + packettype + ' CH' + \
                                global_element.Test_band + ' CH' + global_element.Test_channel + ' ' + ulfre + \
                                'MHz.JPG'
            global_element.SA_intance.PrtScn(picturepath_final)

            global_element.Test_remark = ''

            # 停止功能函数接口


def peakoutpurtpower(item_dict):
    packettype_str = item_dict['parms']['Parm']['Value']
    packettype_list = packettype_str.split('/')
    global_element.Test_item = 'Peak Output Power'
    for packettype in packettype_list:
        global_element.Test_bt_packetype = packettype
        global_element.emitsingle.stateupdataSingle.emit('Testing in progress of Peak Output Power: Channel ' +
                                                         global_element.Test_channel + ' Packet Type: ' + packettype)

        # 设置 Packet Type, hopping type, pattern type
        global_element.CU_intance.set_bt_parms(packettype, False)

        ulfre = report_handle.fre_bt2_calc(global_element.Test_channel)
        if int(global_element.Test_channel) < 39:
            dlfre = '2480'
        else:
            dlfre = '2402'

        # 将此项用户的参数初始化
        low_limit = item_dict['limits']['limit']['low']
        high_limit = item_dict['limits']['limit']['high']

        # 设置CU的线损
        global_element.CU_intance.set_bt_loss(ulfre, dlfre)

        # RESET SA
        global_element.SA_intance.resetself()

        # 设置SA的线损
        global_element.SA_intance.set_loss(ulfre)

        # SA检查DUT是否有发射对应信号
        result = global_element.SA_intance.check_bt_signal()

        if result == False:
            global_element.Test_remark = 'SA did not detect the signal'
            report_handle.Reporttool('NULL', 'None', 'None')
            global_element.Test_remark = ''
        else:
            global_element.emitsingle.stateupdataSingle.emit('SA detection signal is successful!')

            # 开始SA的设置
            global_element.SA_intance.set_reflevel('20')
            global_element.SA_intance.setcenterfrequency(ulfre)
            global_element.SA_intance.setRbwVbw('2', '3')
            global_element.SA_intance.setspan('5')
            global_element.SA_intance.settrace('1', 'MAX')
            global_element.SA_intance.setdetector('MAX PEAK')
            global_element.SA_intance.sweepconfig(True, True, '', '', '')

            global_element.SA_intance.cont_sweep_seconds(10)

            global_element.SA_intance.markertotrace('1', '1')
            global_element.SA_intance.markertopeak('1')

            marker1amp = global_element.SA_intance.marker_Y_value('1')

            global_element.Test_remark = 'Unit: dBm'
            report_handle.Reporttool(marker1amp, low_limit, high_limit)

            # 截图
            picturepath = global_element.reportpath[:global_element.reportpath.index('.')]
            if not os.path.isdir(picturepath + '/BT2.0/FCC/Peak Output Power'):
                os.makedirs(picturepath + '/BT2.0/FCC/Peak Output Power')

            picturepath_final = picturepath + '/BT2.0/FCC/Peak Output Power/BT2.0 ' + packettype + ' CH' + \
                                global_element.Test_band + ' CH' + global_element.Test_channel + ' ' + ulfre + \
                                'MHz.JPG'
            global_element.SA_intance.PrtScn(picturepath_final)

            global_element.Test_remark = ''

            # 停止功能函数接口


def numberofchannel(item_dict):
    if global_element.BT2_number_of_channel_istested == False:
        packettype_list = ['DH5']
        ulfre = report_handle.fre_bt2_calc(global_element.Test_channel)
        if int(global_element.Test_channel) < 39:
            dlfre = '2480'
        else:
            dlfre = '2402'
        temp_channel = global_element.Test_channel
        global_element.Test_channel = 'Hopping Frequency'
        global_element.Test_item = 'Number of Hopping Channel'
        for packettype in packettype_list:
            global_element.Test_bt_packetype = packettype
            global_element.emitsingle.stateupdataSingle.emit('Testing in progress of Number of Hopping Channel: Channel ' +
                                                             global_element.Test_channel + ' Packet Type: ' + packettype)

            # 设置 Packet Type, hopping type, pattern type
            global_element.CU_intance.set_bt_parms(packettype, True)

            # 将此项用户的参数初始化
            low_limit = item_dict['limits']['limit']['low']
            high_limit = item_dict['limits']['limit']['high']

            # 设置CU的线损
            global_element.CU_intance.set_bt_loss(ulfre, dlfre)

            # RESET SA
            global_element.SA_intance.resetself()

            # 设置SA的线损
            global_element.SA_intance.set_loss(ulfre)

            # # SA检查DUT是否有发射对应信号
            # result = global_element.SA_intance.check_bt_signal()
            #
            # if result == False:
            #     global_element.Test_remark = 'SA没检测到信号'
            #     report_handle.Reporttool('NULL', 'None', 'None')
            #     global_element.Test_remark = ''
            # else:
            #     global_element.emitsingle.stateupdataSingle.emit('SA检测信号成功！')

            # 开始SA的设置
            global_element.SA_intance.set_reflevel('20')
            global_element.SA_intance.setstartstopfre('2400', '2483.5')
            global_element.SA_intance.setRbwVbw('0.3', '1')
            global_element.SA_intance.settrace('1', 'MAX')
            global_element.SA_intance.setdetector('MAX PEAK')
            global_element.SA_intance.sweepconfig(True, True, '', '', '')

            global_element.SA_intance.cont_sweep_seconds(20)

            global_element.SA_intance.reflev_pos('90')
            time.sleep(0.2)
            global_element.SA_intance.reflev_pos('100')

            global_element.SA_intance.markertotrace('1', '1')
            global_element.SA_intance.markertopeak('1')

            count_peak = global_element.SA_intance.peakmarkercnt('1')

            global_element.Test_remark = 'Number of Hopping Frequency(Channel)'
            report_handle.Reporttool(count_peak, low_limit, high_limit)

            global_element.Test_remark = 'Adaptive Hopping Frequency(Channel)'
            report_handle.Reporttool('20', low_limit, high_limit)

            # 截图
            picturepath = global_element.reportpath[:global_element.reportpath.index('.')]
            if not os.path.isdir(picturepath + '/BT2.0/FCC/Number of Hopping Channel'):
                os.makedirs(picturepath + '/BT2.0/FCC/Number of Hopping Channel')

            picturepath_final = picturepath + \
                                '/BT2.0/FCC/Number of Hopping Channel/BT2.0 Number of Hopping Channel.JPG'
            global_element.SA_intance.PrtScn(picturepath_final)

            global_element.Test_remark = ''
            global_element.BT2_number_of_channel_istested = True
            global_element.Test_channel = temp_channel


def hoppingchannelseparation(item_dict):
    packettype_str = item_dict['parms']['Parm']['Value']
    packettype_list = packettype_str.split('/')
    global_element.Test_item = 'Hopping Channel Separation'
    for packettype in packettype_list:
        global_element.Test_bt_packetype = packettype
        if global_element.Test_channel == '0':
            channel_group = '0-1'
            center_freq = '2402.5'
        elif global_element.Test_channel == '39':
            channel_group = '39-40'
            center_freq = '2441.5'
        else:
            channel_group = '77-78'
            center_freq = '2479.5'
        global_element.emitsingle.stateupdataSingle.emit('Testing in progress of Hopping Channel Separation: Channel ' +
                                                         channel_group + ' Packet Type: ' + packettype)

        dict_key = global_element.Test_channel + '_' + packettype

        if global_element.BT2_fcc_20dbbw_result[dict_key] != '':

            bw_20db = global_element.BT2_fcc_20dbbw_result[dict_key]
            # 设置 Packet Type, hopping type, pattern type
            global_element.CU_intance.set_bt_parms(packettype, False)

            ulfre = report_handle.fre_bt2_calc(global_element.Test_channel)
            if int(global_element.Test_channel) < 39:
                dlfre = '2480'
            else:
                dlfre = '2402'

            # # 将此项用户的参数初始化
            # low_limit = item_dict['limits']['limit']['low']
            # high_limit = item_dict['limits']['limit']['high']

            # 设置CU的线损
            global_element.CU_intance.set_bt_loss(ulfre, dlfre)

            # RESET SA
            global_element.SA_intance.resetself()

            # 设置SA的线损
            global_element.SA_intance.set_loss(ulfre)

            # SA检查DUT是否有发射对应信号
            result = global_element.SA_intance.check_bt_signal()

            if result == False:
                global_element.Test_remark = 'SA did not detect the signal!'
                report_handle.Reporttool('NULL', 'None', 'None')
                global_element.Test_remark = ''
            else:
                global_element.emitsingle.stateupdataSingle.emit('SA detection signal is successful!')

                # 开始SA的设置
                global_element.SA_intance.set_reflevel('20')
                global_element.SA_intance.setcenterfrequency(center_freq)
                global_element.SA_intance.setRbwVbw('0.03', '0.1')
                global_element.SA_intance.setspan('2.5')
                global_element.SA_intance.settrace('1', 'MAX')
                global_element.SA_intance.setdetector('MAX PEAK')
                global_element.SA_intance.sweepconfig(True, True, '', '', '')

                global_element.SA_intance.startcontsweep()

                time.sleep(5)
                if global_element.Test_channel == '0':
                    global_element.CU_intance.set_bt2_channel('1')
                elif global_element.Test_channel == '39':
                    global_element.CU_intance.set_bt2_channel('40')
                else:
                    global_element.CU_intance.set_bt2_channel('77')

                time.sleep(7)
                global_element.SA_intance.stopcontsweep()

                global_element.SA_intance.markertotrace('1', '1')
                global_element.SA_intance.serchlimit(str(eval(center_freq) - 1), center_freq)
                global_element.SA_intance.markertopeak('1')
                marker1freq = global_element.SA_intance.marker_X_value('1')

                global_element.SA_intance.markertotrace('2', '1')
                global_element.SA_intance.serchlimit(center_freq, str(eval(center_freq) + 1))
                global_element.SA_intance.markertopeak('2')
                marker2freq = global_element.SA_intance.marker_X_value('2')

                global_element.SA_intance.serchlimit_off()

                HFCHSep = format((eval(marker2freq) - eval(marker1freq)) / 1000, '.2f')

                lowlimit = format((eval(bw_20db) * 2 / 3), '.2f') if eval(bw_20db) * 2 / 3 - 25 > 0 else '25'

                global_element.Test_remark = 'Unit: kHz(Low Limit: 25kHz or 2/3 20dB BW(which is greater.))'
                temp_channel = global_element.Test_channel
                global_element.Test_channel = channel_group

                report_handle.Reporttool(HFCHSep, lowlimit, 'None')

                global_element.Test_remark = ''
                global_element.Test_channel = temp_channel

                # 截图
                picturepath = global_element.reportpath[:global_element.reportpath.index('.')]
                if not os.path.isdir(picturepath + '/BT2.0/FCC/Hopping Channel Separation'):
                    os.makedirs(picturepath + '/BT2.0/FCC/Hopping Channel Separation')

                picturepath_final = picturepath + '/BT2.0/FCC/Hopping Channel Separation/BT2.0 ' + packettype + ' CH' + \
                                    channel_group + 'MHz.JPG'
                global_element.SA_intance.PrtScn(picturepath_final)

                global_element.CU_intance.set_bt2_channel(global_element.Test_channel)

        else:
            global_element.emitsingle.stateupdataSingle.emit('No data of Channel: ' + global_element.Test_channel + ' ' +
                                                             packettype + ' 20dB bandwidth，please test 20dB'
                                                                          ' bandwidth before!')
            global_element.Test_remark = 'No data of Channel: ' + global_element.Test_channel + ' ' + packettype + \
                                         '20dB bandwidth，please test 20dB bandwidth before!'

            temp_channel = global_element.Test_channel
            global_element.Test_channel = channel_group

            report_handle.Reporttool('NULL', 'None', 'None')

            global_element.Test_remark = ''
            global_element.Test_channel = temp_channel


def dwelltime(item_dict):
    if global_element.BT2_dwelltime_istested == False:
        packettype_str = item_dict['parms']['Parm']['Value']
        packettype_list = packettype_str.split('/')
        ulfre = report_handle.fre_bt2_calc(global_element.Test_channel)
        if int(global_element.Test_channel) < 39:
            dlfre = '2480'
        else:
            dlfre = '2402'
        tempchannel = global_element.Test_channel
        global_element.Test_channel = 'Hopping Frequency'
        global_element.Test_item = 'Dwell Time'
        for packettype in packettype_list:
            global_element.Test_bt_packetype = packettype
            global_element.emitsingle.stateupdataSingle.emit('Testing in progress of Dwell Time: ' + ' Packet Type: ' + packettype)

            # 设置 Packet Type, hopping type, pattern type
            global_element.CU_intance.set_bt_parms(packettype, True)

            # 将此项用户的参数初始化
            low_limit = item_dict['limits']['limit']['low']
            high_limit = item_dict['limits']['limit']['high']

            # 设置CU的线损
            global_element.CU_intance.set_bt_loss(ulfre, dlfre)

            # RESET SA
            global_element.SA_intance.resetself()

            # 设置SA的线损
            global_element.SA_intance.set_loss(ulfre)

            # # SA检查DUT是否有发射对应信号
            # result = global_element.SA_intance.check_bt_signal()
            #
            # if result == False:
            #     global_element.Test_remark = 'SA没检测到信号'
            #     report_handle.Reporttool('NULL', 'None', 'None')
            #     global_element.Test_remark = ''
            # else:
            #     global_element.emitsingle.stateupdataSingle.emit('SA检测信号成功！')

            # 开始SA的设置
            global_element.SA_intance.set_reflevel('20')
            global_element.SA_intance.setcenterfrequency('2480')
            global_element.SA_intance.setspan('0')
            global_element.SA_intance.setRbwVbw('1', '1')
            global_element.SA_intance.settrace('1', 'MAX')
            global_element.SA_intance.setdetector('MAX PEAK')
            global_element.SA_intance.sweepconfig(True, False, '0.015', '', '')
            global_element.SA_intance.stopcontsweep()

            global_element.SA_intance.trig_ifp_set()

            global_element.SA_intance.cont_sweep_seconds(15)

            global_element.SA_intance.markertotrace('1', '1')
            global_element.SA_intance.markertopeak('1')

            global_element.SA_intance.MoveMarker('1', '0')

            movestep = '0.00001'
            moveposition = '0'
            marker1amp1 = '0'
            marker1amp2 = '0'
            marker2amp1 = '0'
            marker2amp2 = '0'
            marker1freq2 = '0'
            while eval(marker1amp2) - eval(marker1amp1) < 10:
                moveposition = str(eval(moveposition) + eval(movestep))
                marker1amp1 = global_element.SA_intance.marker_Y_value('1')
                global_element.SA_intance.MoveMarker('1', moveposition)
                marker1amp2 = global_element.SA_intance.marker_Y_value('1')
                marker1freq2 = global_element.SA_intance.marker_X_value('1')

            global_element.SA_intance.markertotrace('2', '1')
            global_element.SA_intance.markertopeak('2')
            global_element.SA_intance.MoveMarker('2', marker1freq2)

            while eval(marker2amp1) - eval(marker2amp2) < 10:
                moveposition = str(eval(moveposition) + eval(movestep))
                marker2amp1 = global_element.SA_intance.marker_Y_value('2')
                global_element.SA_intance.MoveMarker('2', moveposition)
                marker2amp2 = global_element.SA_intance.marker_Y_value('2')

            global_element.SA_intance.MoveMarker('2', str(eval(moveposition) - eval(movestep)))

            global_element.SA_intance.reflev_pos('95')
            time.sleep(0.2)
            global_element.SA_intance.reflev_pos('100')

            PacTransferTime = global_element.SA_intance.MarkerDLT()

            DwellTimeNormal = format(eval(PacTransferTime) * 106.67 * 1e3, '.2f')
            DwellTimeAFH = format(eval(PacTransferTime) * 53.33 * 1e3, '.2f')

            global_element.Test_remark = 'Unit: ms, Packet Transfer Time: ' + format(eval(PacTransferTime) * 1e3, '.2f') + 'ms NOR'

            report_handle.Reporttool(DwellTimeNormal, low_limit, high_limit)

            global_element.Test_remark = 'Unit: ms, Packet Transfer Time: ' + format(eval(PacTransferTime) * 1e3,
                                                                                     '.2f') + 'ms AFH'
            report_handle.Reporttool(DwellTimeAFH, low_limit, high_limit)


            # 截图
            picturepath = global_element.reportpath[:global_element.reportpath.index('.')]
            if not os.path.isdir(picturepath + '/BT2.0/FCC/Dwell Time'):
                os.makedirs(picturepath + '/BT2.0/FCC/Dwell Time')

            picturepath_final = picturepath + '/BT2.0/FCC/Dwell Time/BT2.0 ' + packettype + '.JPG'
            global_element.SA_intance.PrtScn(picturepath_final)

        global_element.BT2_dwelltime_istested = True
        global_element.Test_remark = ''
        global_element.Test_channel = tempchannel


def bandedge(item_dict):
    if global_element.Test_channel in ['0', '78']:              # 只测高低信道
        packettype_str = item_dict['parms']['Parm']['Value']
        packettype_list = packettype_str.split('/')

        for i in range(2):
            if i == 0:
                global_element.Test_item = 'Conducted Band Edges'
            else:
                global_element.Test_item = 'Conducted Band Edges(Hopping Mode)'

            for packettype in packettype_list:
                global_element.Test_bt_packetype = packettype
                if i == 0:
                    global_element.emitsingle.stateupdataSingle.emit('Testing in progress of Conducted Band Edges: ' +
                                                                     global_element.Test_channel + ' Packet Type: ' + packettype)
                    # 设置 Packet Type, hopping type, pattern type
                    global_element.CU_intance.set_bt_parms(packettype, False)
                else:
                    global_element.emitsingle.stateupdataSingle.emit('Testing in progress of Conducted Band Edges(Hopping Mode): ' +
                                                                     global_element.Test_channel + ' Packet Type: ' + packettype)
                    # 设置 Packet Type, hopping type, pattern type
                    global_element.CU_intance.set_bt_parms(packettype, True)

                ulfre = report_handle.fre_bt2_calc(global_element.Test_channel)
                if int(global_element.Test_channel) < 39:
                    dlfre = '2480'
                else:
                    dlfre = '2402'

                # # 将此项用户的参数初始化
                # low_limit = item_dict['limits']['limit']['low']
                # high_limit = item_dict['limits']['limit']['high']

                # 设置CU的线损
                global_element.CU_intance.set_bt_loss(ulfre, dlfre)

                # RESET SA
                global_element.SA_intance.resetself()

                # 设置SA的线损
                global_element.SA_intance.set_loss(ulfre)

                # SA检查DUT是否有发射对应信号
                result = global_element.SA_intance.check_bt_signal()

                if result == False:
                    global_element.Test_remark = 'SA did not detect the signal!'
                    report_handle.Reporttool('NULL', 'None', 'None')
                    global_element.Test_remark = ''
                else:
                    global_element.emitsingle.stateupdataSingle.emit('SA detection signal is successful!')

                    # 开始SA的设置
                    global_element.SA_intance.set_reflevel('20')
                    if global_element.Test_channel == '0':
                        global_element.SA_intance.setstartstopfre('2395', '2405')
                    else:
                        global_element.SA_intance.setstartstopfre('2477.5', '2489.5')
                    global_element.SA_intance.setRbwVbw('0.1', '0.3')
                    global_element.SA_intance.settrace('1', 'MAX')
                    global_element.SA_intance.setdetector('MAX PEAK')

                    sweeptime = 5 if i == 0 else 20
                    global_element.SA_intance.sweepconfig(True, True, '', '', '')

                    global_element.SA_intance.cont_sweep_seconds(sweeptime)

                    global_element.SA_intance.markertotrace('1', '1')
                    global_element.SA_intance.markertopeak('1')

                    marker1amp = global_element.SA_intance.marker_Y_value('1')
                    linevalue = format(eval(marker1amp) - 20, '.2f')

                    global_element.SA_intance.Linedisplay(linevalue)

                    global_element.SA_intance.markertotrace('2', '1')

                    if global_element.Test_channel == '0':
                        global_element.SA_intance.serchlimit('2395', '2400')
                    else:
                        global_element.SA_intance.serchlimit('2483.5', '2489.5')

                    global_element.SA_intance.markertopeak('2')
                    bandedge_result = global_element.SA_intance.marker_Y_value('2')

                    global_element.Test_remark = 'Unit: dBm, High Limit: Peak Ampt(' + str(marker1amp) + 'dBm) -20dBc'

                    report_handle.Reporttool(bandedge_result, 'None', linevalue)

                    # 截图
                    picturepath = global_element.reportpath[:global_element.reportpath.index('.')]
                    if not os.path.isdir(picturepath + '/BT2.0/FCC/Conducted Band Edges'):
                        os.makedirs(picturepath + '/BT2.0/FCC/Conducted Band Edges')

                    if i == 0:
                        picturepath_final = picturepath + '/BT2.0/FCC/Conducted Band Edges/BT2.0 '+packettype+\
                                            ' CH'+global_element.Test_channel+' '+ulfre+'MHz.JPG'
                    else:
                        picturepath_final = picturepath + '/BT2.0/FCC/Conducted Band Edges/BT2.0 '+packettype+' CH'+\
                                            global_element.Test_channel+' '+ulfre+'MHz(Frequency Hopping).JPG'

                    global_element.SA_intance.PrtScn(picturepath_final)

        global_element.Test_remark = ''


def cse(item_dict):
    packettype_str = item_dict['parms']['Parm']['Value']
    packettype_list = packettype_str.split('/')
    global_element.Test_item = 'Conducted Spurious Emissions'
    for packettype in packettype_list:
        global_element.Test_bt_packetype = packettype
        global_element.emitsingle.stateupdataSingle.emit('Testing in progress of Conducted Spurious Emissions: ' +
                                                         global_element.Test_channel + ' Packet Type: ' + packettype)
        # 设置 Packet Type, hopping type, pattern type
        global_element.CU_intance.set_bt_parms(packettype, False)

        ulfre = report_handle.fre_bt2_calc(global_element.Test_channel)
        if int(global_element.Test_channel) < 39:
            dlfre = '2480'
        else:
            dlfre = '2402'

        # # 将此项用户的参数初始化
        # low_limit = item_dict['limits']['limit']['low']
        # high_limit = item_dict['limits']['limit']['high']

        # 设置CU的线损
        global_element.CU_intance.set_bt_loss(ulfre, dlfre)

        # RESET SA
        global_element.SA_intance.resetself()

        # 设置SA的线损
        global_element.SA_intance.set_loss(ulfre)

        # SA检查DUT是否有发射对应信号
        result = global_element.SA_intance.check_bt_signal()

        if result == False:
            global_element.Test_remark = 'SA did not detect the signal!'
            report_handle.Reporttool('NULL', 'None', 'None')
            global_element.Test_remark = ''
        else:
            global_element.emitsingle.stateupdataSingle.emit('SA detection signal is successful!')

            for i in [1, 2]:
                # 开始SA的设置(30MHz-3GHz)
                global_element.SA_intance.set_reflevel('15')
                if i == 1:
                    global_element.SA_intance.setstartstopfre('30', '3000')
                else:
                    global_element.SA_intance.setstartstopfre('2000', '25000')
                global_element.SA_intance.setRbwVbw('0.1', '0.3')
                global_element.SA_intance.settrace('1', 'MAX')
                global_element.SA_intance.setdetector('MAX PEAK')

                global_element.SA_intance.sweepconfig(True, True, '', '', '')
                global_element.SA_intance.set_sweep_points('10001')

                global_element.SA_intance.cont_sweep_seconds(15)

                global_element.SA_intance.markertotrace('1', '1')
                global_element.SA_intance.markertopeak('1')

                peak_value = global_element.SA_intance.marker_Y_value('1')
                line_value = format(eval(peak_value) - 20, '.2f')

                global_element.SA_intance.Linedisplay(line_value)

                global_element.SA_intance.next_peak('1')

                peak_value_2 = global_element.SA_intance.marker_Y_value('1')
                if i == 1:
                    global_element.Test_remark = 'CSE 30MHz-3GHz'
                else:
                    global_element.Test_remark = 'CSE 2GHz-25GHz'
                report_handle.Reporttool(peak_value_2, 'None', line_value)

                # 截图
                picturepath = global_element.reportpath[:global_element.reportpath.index('.')]
                if not os.path.isdir(picturepath + '/BT2.0/FCC/Conducted Spurious Emissions'):
                    os.makedirs(picturepath + '/BT2.0/FCC/Conducted Spurious Emissions')

                if i == 1:
                    picturepath_final = picturepath + '/BT2.0/FCC/Conducted Spurious Emissions/BT2.0 ' + packettype + \
                                        ' CH' + global_element.Test_channel + ' ' + ulfre + 'MHz(30MHz~3GHz).JPG'
                else:
                    picturepath_final = picturepath + '/BT2.0/FCC/Conducted Spurious Emissions/BT2.0 ' + packettype +\
                                        ' CH' + global_element.Test_channel + ' ' + ulfre + 'MHz(2GHz~25GHz).JPG'

                global_element.SA_intance.PrtScn(picturepath_final)

            global_element.Test_remark = ''







