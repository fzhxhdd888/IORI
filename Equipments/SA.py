# !/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Author    : Feng Zhaohui
# @Time      : 2019/2/22
# @File      : SA.py
# @Funcyusa  :
# @Version   : 1.0

import visa
import report_handle
import global_element
import time


class VisaSA(object):
    """
        频谱类构建
        定义频谱的类函数和参数
    """
    def __init__(self, device_name, visa_address, visa_address_type,  visaDLL=None, *args):
        self.device_address = visa_address
        self.device_name = device_name
        self.device_address_type = visa_address_type
        self.visaDLL = 'visa32.dll' if visaDLL is None else visaDLL
        if self.device_address_type == 'GPIB':
            self.address = "GPIB0::%s::INSTR" % self.device_address
        elif self.device_address_type == 'TCPIP':
            self.address = "TCPIP::%s::inst0::INSTR" % self.device_address
        self.resourceManager = visa.ResourceManager(self.visaDLL)
        self.VisaLibraryBase1 = self.resourceManager.visalib

    def open(self):
        self.instance = self.resourceManager.open_resource(self.address)
        self.instance_bare = self.resourceManager.open_bare_resource(self.address)

    def close(self):
        if self.instance is not None:
            self.instance.close()
            self.instance = None

    def read_idn(self):
        idn = self.instance.query("*IDN?")
        return idn

    # 检测DUT是否有发出对应的GSM信号
    def check_gsm_signal(self):
        result = True
        if self.device_name in ['FSQ', 'FSU', 'E4440A']:
            global_element.emitsingle.stateupdataSingle.emit('SA Check Signal……')
            DLfre, ULfre = report_handle.freq_gsm_calc(int(global_element.Test_channel))
            self.instance.query('FREQ:CENT ' + ULfre + 'MHz; *OPC?')
            self.set_loss(ULfre)
            self.instance.query('DISP:WIND:TRAC:Y:RLEV 30dBm; *OPC?')
            self.instance.query('FREQ:SPAN 1GHz; *OPC?')
            if self.device_name != 'E4440A':
                self.instance.query('DISP:WIND:TRAC:MODE MAXH; *OPC?')
            elif self.device_name == 'E4440A':
                self.instance.query('TRAC:MODE MAXH; *OPC?')
            self.instance.query('INIT:CONT ON; *OPC?')
            time.sleep(2)
            self.instance.query('INIT:CONT OFF; *OPC?')
            self.instance.query('CALC:MARK1:MAX; *OPC?')
            marker1_amp = self.instance.query('CALC:MARK1:Y?')
            if eval(marker1_amp) < 0:
                global_element.emitsingle.stateupdataSingle.emit('SA did not check the signal!')
                result = False
                time.sleep(1)
            return result

    # 检测DUT是否有发出对应的LTE CA信号
    def check_lteca_signal(self):
        try:
            result = True
            if self.device_name in ['FSQ', 'FSU', 'E4440A']:
                global_element.emitsingle.stateupdataSingle.emit('SA Check Signal……')
                channel = global_element.Test_channel.split(',')[0].split('|')[1]
                DLfre, ULfre = report_handle.freq_gsm_calc(int(channel))
                self.instance.query('FREQ:CENT ' + ULfre + 'MHz; *OPC?')
                self.set_loss(ULfre)
                self.instance.query('DISP:WIND:TRAC:Y:RLEV 30dBm; *OPC?')
                self.instance.query('FREQ:SPAN 1GHz; *OPC?')
                if self.device_name != 'E4440A':
                    self.instance.query('DISP:WIND:TRAC:MODE MAXH; *OPC?')
                elif self.device_name == 'E4440A':
                    self.instance.query('TRAC:MODE MAXH; *OPC?')
                self.instance.query('INIT:CONT ON; *OPC?')
                time.sleep(2)
                self.instance.query('INIT:CONT OFF; *OPC?')
                self.instance.query('CALC:MARK1:MAX; *OPC?')
                marker1_amp = self.instance.query('CALC:MARK1:Y?')
                if eval(marker1_amp) < 0:
                    global_element.emitsingle.stateupdataSingle.emit('SA did not check the signal!')
                    result = False
                    time.sleep(1)
                return result
        except:
            global_element.emitsingle.statetimeupdataSingle.emit('SA check LTE CA signal method exception!')

    # 连续扫描n秒
    def cont_sweep_seconds(self, seconds):
        try:
            if self.device_name in ['FSQ', 'FSU', 'E4440A']:
                self.instance.query('INIT:CONT ON; *OPC?')
                time.sleep(int(seconds))
                self.instance.query('INIT:CONT OFF; *OPC?')
                time.sleep(2)
        except:
            pass

    # 设置SA线损
    def set_loss(self, c_Frequency):
        min_delta_index = 0
        min_delta = 10000000
        for i in range(len(global_element.SA_DUT_loss['Loss']['loss'])):
            delta_i = abs(eval(global_element.SA_DUT_loss['Loss']['loss'][i]['Frequency']) - eval(c_Frequency))
            if delta_i < min_delta:
                min_delta = delta_i
                min_delta_index = i

        loss_value = global_element.SA_DUT_loss['Loss']['loss'][min_delta_index]['Value']

        if self.device_name == 'FSQ' or self.device_name == 'FSU':
            self.instance.write('DISP:TRAC:Y:RLEV:OFFS ' + loss_value + 'dB')
        elif self.device_name == 'E4440A':
            self.instance.write('DISPlay:WINDow:TRACe:Y:RLEV:OFFS ' + loss_value + 'dB')

    # RESET SA
    def resetself(self):
        if self.device_name == 'FSQ' or self.device_name == 'FSU':
            self.instance.query('*CLS;*RST; *OPC?')
        elif self.device_name == 'E4440A':
            self.instance.query('SYSTem:PRESet; *OPC?')

    # SA截屏到PC
    def PrtScn(self, photopath):
        device_session = int(self.instance._session)
        try:
            if self.device_name == 'FSQ' or self.device_name == 'FSU':
                self.instance.write('SYST:DISP:UPD ON')
                self.instance.write('HCOP:DEST \'MMEM\'')
                self.instance.write('HCOP:DEV:LANG JPG')
                self.instance.write('MMEM:NAME \'output11111.JPG\'')
                self.instance.write('HCOP:ITEM:ALL')
                self.instance.write('HCOP:IMM')
                self.instance.write('MMEM:DATA? \'D:\\output11111.JPG\'')
            elif self.device_name == 'E4440A':
                self.instance.write('DISP:FSCR ON')
                self.instance.query("MMEM:STOR:SCR 'C:PICTURE.GIF';*OPC?")
                self.instance.write("MMEM:DATA? 'C:PICTURE.GIF'")

            chunk, status = self.VisaLibraryBase1.read(device_session, 2)

            chunk_list = list(chunk)
            temp = int(chunk_list[1]) - 48
            chunk, status = self.VisaLibraryBase1.read(device_session, temp)
            chunk_list = list(chunk)
            temp1 = 0
            for i in range(temp):
                value_wei = chunk_list[i] - 48
                temp1 = temp1 + value_wei * global_element.power(10, (temp - i - 1))

            self.VisaLibraryBase1.read_to_file(device_session, photopath, temp1)

            global_element.image_handle(photopath)     # 擦除图片部分内容
        except:
            pass

    # SA设置REF level
    def set_reflevel(self, level_str):
        try:
            if self.device_name in ['FSQ', 'FSU', 'E4440A']:
                self.instance.write('DISP:WIND:TRAC:Y:RLEV ' + level_str + 'dBm')
        except:
            global_element.emitsingle.thread_exitSingle.emit('SA set ref level method exception!')

    # SA设置RBW VBW
    def setRbwVbw(self, str_rbw, str_vbw):
        try:
            if self.device_name in ['FSQ', 'FSU', 'E4440A']:
                self.instance.write('BAND:AUTO OFF')
                self.instance.write('BAND ' + str_rbw + 'MHz')

                self.instance.write('BAND:VID:AUTO OFF')
                self.instance.write('BAND:VID ' + str_vbw + 'MHz')
        except:
            global_element.emitsingle.thread_exitSingle.emit('SA set RBW/VBW method exception!')

    # SA设置SPAN
    def setspan(self, str_span):
        try:
            if self.device_name in ['FSQ', 'FSU', 'E4440A']:
                self.instance.write('FREQ:SPAN ' + str_span + 'MHz')
        except:
            global_element.emitsingle.thread_exitSingle.emit('SA set Span method exception!')

    # SA设置trace
    def settrace(self, str_traceindex, str_tracemode):
        try:
            if self.device_name == 'FSQ' or self.device_name == 'FSU':
                if str_tracemode == 'MAX':
                    self.instance.write('DISP:WIND:TRAC' + str_traceindex + ':MODE MAXH')
                elif str_tracemode == 'AVE':
                    self.instance.write('DISP:WIND:TRAC' + str_traceindex + ':MODE AVER')
                elif str_tracemode == 'VIEW':
                    self.instance.write('DISP:WIND:TRAC' + str_traceindex + ':MODE VIEW')
                elif str_tracemode == 'BLANK':
                    self.instance.write('DISP:WIND:TRAC' + str_traceindex + ' OFF')
                else:
                    pass
            elif self.device_name == 'E4440A':
                if str_tracemode == 'MAX':
                    self.instance.write('TRAC' + str_traceindex + ':MODE MAXH')
                elif str_tracemode == 'AVE':
                    self.instance.write('TRAC' + str_traceindex + ':MODE MAXH')
                elif str_tracemode == 'VIEW':
                    self.instance.write('TRAC' + str_traceindex + ':MODE VIEW')
                elif str_tracemode == 'BLANK':
                    self.instance.write('TRAC' + str_traceindex + ':MODE BLAN')
                else:
                    pass
        except:
            global_element.emitsingle.thread_exitSingle.emit('SA set Trace method exception!')

    # SA设置中心频率
    def setcenterfrequency(self, str_frequency):
        try:
            if self.device_name in ['FSQ', 'FSU', 'E4440A']:
                self.instance.write('FREQ:CENT ' + str_frequency + 'MHz')
        except:
            global_element.emitsingle.thread_exitSingle.emit('SA set Center Frequency method exception!')

    # SA 设置start stop Fre
    def setstartstopfre(self, startfre_str, stopfre_str):
        try:
            if self.device_name in ['FSQ', 'FSU', 'E4440A']:
                self.instance.write('FREQ:STAR ' + startfre_str + 'MHz')
                self.instance.write('FREQ:STOP ' + stopfre_str + 'MHz')
        except:
            global_element.emitsingle.thread_exitSingle.emit('SA set start&staop frequency method exception!')

    # SA设置DETECTOR
    def setdetector(self, str_detector):
        try:
            if self.device_name == 'FSQ' or self.device_name == 'FSU':
                if str_detector == 'AUTO PEAK':
                    self.instance.write('DET APE')
                elif str_detector == 'MAX PEAK':
                    self.instance.write('DET POS')
                elif str_detector == 'MIN PEAK':
                    self.instance.write('DET NEG')
                elif str_detector == 'SAMPLE':
                    self.instance.write('DET SAMP')
                elif str_detector == 'RMS':
                    self.instance.write('DET RMS')
                elif str_detector == 'AVERAGE':
                    self.instance.write('DET AVER')
                elif str_detector == 'QPK':
                    self.instance.write('DET QPE')
                else:
                    pass
            elif self.device_name == 'E4440A':
                if str_detector == 'AUTO PEAK':
                    self.instance.write('DET POS')
                elif str_detector == 'MAX PEAK':
                    self.instance.write('DET POS')
                elif str_detector == 'MIN PEAK':
                    self.instance.write('DET NEG')
                elif str_detector == 'SAMPLE':
                    self.instance.write('DET SAMP')
                elif str_detector == 'RMS':
                    self.instance.write('DET AVER')
                elif str_detector == 'AVERAGE':
                    self.instance.write('DET AVER')
                else:
                    pass
        except:
            global_element.emitsingle.thread_exitSingle.emit('SA set Detector method exception!')

    # SA调出Mark并定位到peak
    def markertopeak(self, marker_index):
        try:
            if self.device_name == 'FSQ' or self.device_name == 'FSU':
                self.instance.write('CALC:MARK' + marker_index + ' ON')
                self.instance.write('CALC:MARK' + marker_index + ':MAX')
            elif self.device_name == 'E4440A':
                self.instance.write('CALC:MARK' + marker_index + ':STAT ON')
                self.instance.write('CALC:MARK' + marker_index + ':MAX')
        except:
            global_element.emitsingle.thread_exitSingle.emit('SA set marker to peak method exception!')

    # SA marker to trace
    def markertotrace(self, marker_index, trace_index):
        try:
            if self.device_name in ['FSQ', 'FSU', 'E4440A']:
                self.instance.write('CALC:MARK' + marker_index + ':TRAC ' + trace_index)
        except:
            global_element.emitsingle.thread_exitSingle.emit('SA set marker to trace method exception!')

    # SA 开始扫描
    def startsweep(self):
        try:
            if self.device_name in ['FSQ', 'FSU', 'E4440A']:
                self.instance.write('INITiate:IMMediate')
        except:
            global_element.emitsingle.thread_exitSingle.emit('SA start sweep method exception!')

    # SA Marker的Y值
    def marker_Y_value(self, marker_index):
        try:
            if self.device_name in ['FSQ', 'FSU', 'E4440A']:
                markeramp = self.instance.query('CALC:MARK' + marker_index + ':Y?')
                markerampvalue = format(float(markeramp[:-2]), '.2f')

                return markerampvalue
        except:
            global_element.emitsingle.thread_exitSingle.emit('SA marker Y value method exception!')

    # SA Marker的X值
    def marker_X_value(self, marker_index):
        try:
            if self.device_name in ['FSQ', 'FSU', 'E4440A']:
                markerfreq = self.instance.query('CALC:MARK' + marker_index + ':X?')
                markerfreqvalue = format(float(markerfreq[:-2]), '.2f')

                return markerfreqvalue
        except:
            global_element.emitsingle.thread_exitSingle.emit('SA marker X value method exception!')

    # SA设置扫描方式
    def sweepconfig(self, isCont, isTimeAuto, sweepTime, sweepCount, sweepPoints):
        try:
            if self.device_name in ['FSQ', 'FSU', 'E4440A']:
                if isCont == True:
                    self.instance.write('INIT:CONT ON')
                else:
                    self.instance.write('INIT:CONT OFF')

                if isTimeAuto == True:
                    self.instance.write('SWE:TIME:AUTO ON')
                else:
                    self.instance.write('SWE:TIME ' + sweepTime + 's')

                if self.device_name != 'E4440A':
                    if sweepCount != '':
                        self.instance.write('SWE:COUN ' + sweepCount)
                if sweepPoints != '':
                    self.instance.write('SWE:POIN ' + sweepPoints)
        except:
            global_element.emitsingle.thread_exitSingle.emit('SA set sweep config method exception!')

    # SA开始连续扫描
    def startcontsweep(self):
        try:
            if self.device_name in ['FSQ', 'FSU', 'E4440A']:
                self.instance.write('INIT:CONT ON')
                self.instance.write('INITiate:IMMediate')
        except:
            global_element.emitsingle.thread_exitSingle.emit('SA start cont sweep method exception!')

    # SA停止连续扫描
    def stopcontsweep(self):
        try:
            if self.device_name in ['FSQ', 'FSU', 'E4440A']:
                self.instance.write('INIT:CONT OFF')
        except:
            global_element.emitsingle.thread_exitSingle.emit('SA stop cont sweep method exception!')

    # SA是否扫描完成
    def sweepiscompleted(self, sweepcount):
        try:
            if self.device_name == 'FSQ' or self.device_name == 'FSU':
                time.sleep(1)
                sweepcount_finished = 0
                while sweepcount_finished < int(sweepcount):
                    # 停止功能函数接口
                    sweepcount_finished_str = self.instance.query('SWEep:COUNt:CURRent?')
                    sweepcount_finished_str_final = sweepcount_finished_str[:-1]
                    sweepcount_finished = int(sweepcount_finished_str_final)
                    time.sleep(1)
        except:
            global_element.emitsingle.thread_exitSingle.emit('SA sweep is completed method exception!')

    # SA百分之带宽
    def pctBW(self, width_str):
        try:
            if self.device_name == 'FSQ' or self.device_name == 'FSU':
                time.sleep(1)
                self.instance.write('SENS:POW:BWID ' + width_str + 'PCT')
                self.instance.write('CALC:MARK:FUNC:POW:SEL OBW')
                self.cont_sweep_seconds(15)
                if self.device_name == 'FSQ':
                    OBW_result = self.instance.query('CALC:MARK:FUNC:POW:RES? AOBW')
                else:
                    OBW_result = self.instance.query('CALC:MARK:FUNC:POW:RES? OBW')
                OBW_result_final = str(format(eval(OBW_result.split(',')[0]) / 1000, '.2f'))
            elif self.device_name == 'E4440A':
                time.sleep(1)
                self.instance.write('SENS:OBW:MAXH ON')
                self.instance.write('SENS:OBW:PERC ' + width_str)
                OBW_result = self.instance.query('READ:OBW?')
                time.sleep(15)
                self.stopcontsweep()
                OBW_result = self.instance.query('READ:OBW?')
                OBW_result_final = str(format(eval(OBW_result.split(',')[0]) / 1000, '.2f'))

            return OBW_result_final
        except:
            global_element.emitsingle.thread_exitSingle.emit('SA Pct BW method exception!')

    # SA NDBD带宽
    def NDBDBW(self, NDB_str):
        try:
            if self.device_name == 'FSQ' or self.device_name == 'FSU':
                time.sleep(1)
                self.instance.write('CALC:MARK:FUNC:NDBD ' + NDB_str + 'dB')
                self.cont_sweep_seconds(10)
                self.markertotrace('1', '1')
                self.markertopeak('1')
                time.sleep(0.1)
                NDBD_BW = self.instance.query('CALCulate:MARKer:FUNCtion:NDBDown:RESult?')
                NDBD_BW_final = str(format(eval(NDBD_BW) / 1000, '.2f'))
            elif self.device_name == 'E4440A':
                time.sleep(1)
                self.instance.write('SENS:OBW:MAXH ON')
                self.instance.write('SENS:OBW:XDB -' + NDB_str)
                NDBD_BW = self.instance.query('READ:OBW?')
                time.sleep(15)
                self.stopcontsweep()
                NDBD_BW = self.instance.query('READ:OBW:XDB?')
                NDBD_BW_final = str(format(eval(NDBD_BW) / 1000, '.2f'))
            return NDBD_BW_final
        except:
            global_element.emitsingle.thread_exitSingle.emit('N dB Down method exception!')

    # SA GSM Bandedge spurious功能设置
    def gsmfcc_Spurious_set(self, channel_str):
        try:
            if self.device_name == 'FSQ' or self.device_name == 'FSU':
                self.instance.write('SWEEP:MODE LIST')
                self.instance.write('CALC1:PEAK:AUTO ON')
                range_count = self.instance.query('SENS:LIST:RANG:COUN?')
                range_count_final = range_count[:-1]
                for i in range(int(range_count_final)):
                    self.instance.write('SENS:LIST:RANG:DEL')     # 清空LIST

                if channel_str == '128':
                    self.setstartstopfre('800', '900')
                    start_fre_list = ['820000000', '823000000', '824000000']
                    stop_fre_list = ['823000000', '824000000', '824500000']
                    rbw_list = ['100000', '3000', '10000']
                    vbw_list = ['300000', '10000', '30000']
                    reflev_list = ['30', '30', '35']
                    limit_start_list = ['-13', '-13', '60']
                    limit_stop_list = ['-13', '-13', '60']
                elif channel_str == '251':
                    self.setstartstopfre('800', '900')
                    start_fre_list = ['848500000', '849000000', '850000000']
                    stop_fre_list = ['849000000', '850000000', '855000000']
                    rbw_list = ['10000', '3000', '100000']
                    vbw_list = ['30000', '10000', '300000']
                    reflev_list = ['35', '30', '30']
                    limit_start_list = ['60', '-13', '-13']
                    limit_stop_list = ['60', '-13', '-13']
                elif channel_str == '512':
                    self.setstartstopfre('1800', '1900')
                    start_fre_list = ['1845000000', '1849000000', '1850000000']
                    stop_fre_list = ['1849000000', '1850000000', '1851000000']
                    rbw_list = ['1000000', '3000', '10000']
                    vbw_list = ['3000000', '10000', '30000']
                    reflev_list = ['-20', '30', '35']
                    limit_start_list = ['-13', '-13', '60']
                    limit_stop_list = ['-13', '-13', '60']
                elif channel_str == '810':
                    self.setstartstopfre('1900', '1950')
                    start_fre_list = ['1909000000', '1910000000', '1911000000']
                    stop_fre_list = ['1910000000', '1911000000', '1915000000']
                    rbw_list = ['10000', '3000', '1000000']
                    vbw_list = ['30000', '10000', '3000000']
                    reflev_list = ['35', '30', '-20']
                    limit_start_list = ['60', '-13', '-13']
                    limit_stop_list = ['60', '-13', '-13']

                # 编辑LIST
                for i in range(1, 4):
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':STAR ' + start_fre_list[i-1])
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':STOP ' + stop_fre_list[i-1])
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':FILT:TYPE NORM')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':BAND:RES ' + rbw_list[i-1])
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':BAND:VID ' + vbw_list[i-1])
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':SWE:TIME:AUTO ON')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':DET RMS')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':RLEV ' + reflev_list[i-1])
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':INP:ATT:AUTO ON')
                    self.instance.write('LIST:RANG' + str(i) + ':POIN 600')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':LIM:STAT ON')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':LIM:STAR ' + limit_start_list[i-1])
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':LIM:STOP ' + limit_stop_list[i-1])

                # Start sweept
                self.instance.write('INIT:SPUR')
                time.sleep(15)
                self.instance.write('ABOR')

                result = self.instance.query('CALC:LIM:FAIL?')
                result_final = result[:-1]
                return result_final

        except:
            global_element.emitsingle.thread_exitSingle.emit('SA Bandedge Setting Method Exception!')

    # SA WCDMA Bandedge spurious功能设置
    def wcdmafcc_Spurious_set(self, channel_str):
        try:
            if self.device_name == 'FSQ' or self.device_name == 'FSU':
                self.instance.write('SWEEP:MODE LIST')
                self.instance.write('CALC1:PEAK:AUTO ON')
                range_count = self.instance.query('SENS:LIST:RANG:COUN?')
                range_count_final = range_count[:-1]
                for i in range(int(range_count_final)):
                    self.instance.write('SENS:LIST:RANG:DEL')  # 清空LIST

                high_level = '30'
                low_level = '-20'

                if channel_str == '4132':
                    self.setstartstopfre('820', '829')
                    start_fre_list = ['820000000', '823000000', '824000000']
                    stop_fre_list = ['823000000', '824000000', '829000000']
                    rbw_list = ['100000', '50000', '100000']
                    vbw_list = ['300000', '150000', '300000']
                    reflev_list = [high_level, high_level, high_level]
                    limit_start_list = ['-13', '-13', '60']
                    limit_stop_list = ['-13', '-13', '60']
                elif channel_str == '4233':
                    self.setstartstopfre('844', '855')
                    start_fre_list = ['844000000', '849000000', '850000000']
                    stop_fre_list = ['849000000', '850000000', '855000000']
                    rbw_list = ['100000', '50000', '100000']
                    vbw_list = ['300000', '150000', '300000']
                    reflev_list = [high_level, high_level, high_level]
                    limit_start_list = ['60', '-13', '-13']
                    limit_stop_list = ['60', '-13', '-13']
                elif channel_str == '9262':
                    self.setstartstopfre('1800', '1900')
                    start_fre_list = ['1845000000', '1849000000', '1850000000']
                    stop_fre_list = ['1849000000', '1850000000', '1855000000']
                    rbw_list = ['1000000', '50000', '100000']
                    vbw_list = ['3000000', '150000', '300000']
                    reflev_list = [low_level, high_level, high_level]
                    limit_start_list = ['-13', '-13', '60']
                    limit_stop_list = ['-13', '-13', '60']
                elif channel_str == '9538':
                    self.setstartstopfre('1900', '1950')
                    start_fre_list = ['1905000000', '1910000000', '1911000000']
                    stop_fre_list = ['1910000000', '1911000000', '1915000000']
                    rbw_list = ['100000', '50000', '1000000']
                    vbw_list = ['300000', '150000', '3000000']
                    reflev_list = [high_level, high_level, low_level]
                    limit_start_list = ['60', '-13', '-13']
                    limit_stop_list = ['60', '-13', '-13']
                elif channel_str == '1312':
                    self.setstartstopfre('1705', '1715')
                    start_fre_list = ['1705000000', '1709000000', '1710000000']
                    stop_fre_list = ['1709000000', '1710000000', '1715000000']
                    rbw_list = ['1000000', '50000', '100000']
                    vbw_list = ['3000000', '150000', '300000']
                    reflev_list = [low_level, high_level, high_level]
                    limit_start_list = ['-13', '-13', '60']
                    limit_stop_list = ['-13', '-13', '60']
                elif channel_str == '1513':
                    self.setstartstopfre('1750', '1760')
                    start_fre_list = ['1750000000', '1755000000', '1756000000']
                    stop_fre_list = ['1755000000', '1756000000', '1760000000']
                    rbw_list = ['100000', '50000', '1000000']
                    vbw_list = ['300000', '150000', '3000000']
                    reflev_list = [high_level, high_level, low_level]
                    limit_start_list = ['60', '-13', '-13']
                    limit_stop_list = ['60', '-13', '-13']

                # 编辑LIST
                for i in range(1, 4):
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':STAR ' + start_fre_list[i - 1])
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':STOP ' + stop_fre_list[i - 1])
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':FILT:TYPE NORM')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':BAND:RES ' + rbw_list[i - 1])
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':BAND:VID ' + vbw_list[i - 1])
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':SWE:TIME:AUTO ON')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':DET RMS')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':RLEV ' + reflev_list[i - 1])
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':INP:ATT:AUTO ON')
                    self.instance.write('LIST:RANG' + str(i) + ':POIN 10000')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':LIM:STAT ON')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':LIM:STAR ' + limit_start_list[i - 1])
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':LIM:STOP ' + limit_stop_list[i - 1])

                # Start sweept
                self.instance.write('INIT:SPUR')
                time.sleep(10)
                self.instance.write('ABOR')

                result = self.instance.query('CALC:LIM:FAIL?')
                result_final = result[:-1]
                return result_final
        except:
            global_element.emitsingle.thread_exitSingle.emit('SA Bandedge Setting Method Exception!')

    # SA GSMFCC CSE设置
    def gsmfcc_cse_set(self, band_str):
        try:
            if self.device_name == 'FSQ' or self.device_name == 'FSU':
                self.instance.write('SWEEP:MODE LIST')
                self.instance.write('CALC1:PEAK:AUTO ON')
                range_count = self.instance.query('SENS:LIST:RANG:COUN?')
                range_count_final = range_count[:-1]
                for i in range(int(range_count_final)):
                    self.instance.write('SENS:LIST:RANG:DEL')  # 清空LIST

                if band_str == 'GSM850':
                    self.setstartstopfre('30', '9000')
                    start_fre_list = ['30', '855000000', '1000000000', '3000000000', '7000000000']
                    stop_fre_list = ['820000000', '1000000000', '3000000000', '7000000000', '9000000000']
                elif band_str == 'PCS1900':
                    self.setstartstopfre('30', '19100')
                    start_fre_list = ['30', '1000000000', '1915000000', '3000000000', '7000000000', '13600000000']
                    stop_fre_list = ['1000000000', '1845000000', '3000000000', '7000000000', '13600000000', '19100000000']

                # 编辑LIST
                for i in range(1, len(start_fre_list) + 1):
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':STAR ' + start_fre_list[i - 1])
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':STOP ' + stop_fre_list[i - 1])
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':FILT:TYPE NORM')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':BAND:RES 1000000')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':BAND:VID 3000000')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':SWE:TIME:AUTO ON')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':DET POS')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':RLEV 0')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':INP:ATT:AUTO ON')
                    self.instance.write('LIST:RANG' + str(i) + ':POIN 10000')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':LIM:STAT ON')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':LIM:STAR -13')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':LIM:STOP -13')

                # Start sweept
                self.instance.write('INIT:SPUR')
                time.sleep(10)
                self.instance.write('ABOR')

                time.sleep(3)

                result = self.instance.query('CALC:LIM:FAIL?')
                result_final = result[:-1]
                return result_final
        except:
            global_element.emitsingle.thread_exitSingle.emit('CSE spectrum settings failed!')

    # SA WCDMAFCC CSE设置
    def wcdmafcc_cse_set(self, band_str):
        try:
            if self.device_name == 'FSQ' or self.device_name == 'FSU':
                self.instance.write('SWEEP:MODE LIST')
                self.instance.write('CALC1:PEAK:AUTO ON')
                range_count = self.instance.query('SENS:LIST:RANG:COUN?')
                range_count_final = range_count[:-1]
                for i in range(int(range_count_final)):
                    self.instance.write('SENS:LIST:RANG:DEL')  # 清空LIST

                if band_str == 'Band II':
                    self.setstartstopfre('30', '19100')
                    start_fre_list = ['30', '1000000000', '1915000000', '3000000000', '7000000000', '13600000000']
                    stop_fre_list = ['1000000000', '1845000000', '3000000000', '7000000000', '13600000000', '19100000000']
                elif band_str == 'Band V':
                    self.setstartstopfre('30', '9000')
                    start_fre_list = ['30', '855000000', '1000000000', '3000000000', '7000000000']
                    stop_fre_list = ['820000000', '1000000000', '3000000000', '7000000000', '9000000000']
                elif band_str == 'Band IV':
                    self.setstartstopfre('30', '18000')
                    start_fre_list = ['30', '1000000000', '1760000000', '3000000000', '7000000000', '13600000000']
                    stop_fre_list = ['1000000000', '1705000000', '3000000000', '7000000000', '13600000000', '18000000000']

                # 编辑LIST
                for i in range(1, len(start_fre_list) + 1):
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':STAR ' + start_fre_list[i - 1])
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':STOP ' + stop_fre_list[i - 1])
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':FILT:TYPE NORM')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':BAND:RES 1000000')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':BAND:VID 3000000')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':SWE:TIME:AUTO ON')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':DET POS')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':RLEV 0')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':INP:ATT:AUTO ON')
                    self.instance.write('LIST:RANG' + str(i) + ':POIN 10000')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':LIM:STAT ON')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':LIM:STAR -13')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':LIM:STOP -13')

                # Start sweept
                self.instance.write('INIT:SPUR')
                time.sleep(10)
                self.instance.write('ABOR')

                time.sleep(3)

                result = self.instance.query('CALC:LIM:FAIL?')
                result_final = result[:-1]
                return result_final
        except:
            global_element.emitsingle.thread_exitSingle.emit('CSE spectrum settings failed!')

    # 设置CCDF on
    def CCDFON_and_get_value(self):
        try:
            if self.device_name in ['FSQ', 'FSU']:
                self.instance.write('CALC:STAT:CCDF ON')
                if 'LTE' in global_element.Test_type:
                    self.instance.write('BAND ' + global_element.Test_lte_bandwidth[:-3] + ' MHz')
                self.instance.write('INITiate:IMMediate')
                time.sleep(2)
                result = self.instance.query('CALC:STAT:CCDF:X? P0_1')
                result_final = format(float(result[:-1]), '.2f')

            elif self.device_name == 'E4440A':
                self.instance.write('INIT:CONT OFF')
                result = self.instance.query('READ:PST?')
                time.sleep(3)
                result = self.instance.query('READ:PST?')
                result_final = format(float(result.split(',')[4]), '.2f')
            return result_final
        except:
            global_element.emitsingle.thread_exitSingle.emit('SA set CCDF method exception')

    # 设置CCDF off
    def CCDFOFF(self):
        try:
            if self.device_name in ['FSQ', 'FSU']:
                self.instance.write('CALC:STAT:CCDF OFF')
            elif self.device_name == 'E4440A':
                self.instance.write('CONF:SAN')
        except:
            global_element.emitsingle.thread_exitSingle.emit('SA set CCDF OFF method exception')

    # SA LTE Bandedge spurious功能设置
    def ltefcc_bandedge_set(self, channel_str):
        try:
            if self.device_name == 'FSQ' or self.device_name == 'FSU':
                self.instance.write('SWEEP:MODE LIST')
                self.instance.write('CALC1:PEAK:AUTO ON')
                range_count = self.instance.query('SENS:LIST:RANG:COUN?')
                range_count_final = range_count[:-1]
                for i in range(int(range_count_final)):
                    self.instance.write('SENS:LIST:RANG:DEL')  # 清空LIST

                low_level = '-30'
                high_level = '30'
                high_limit = '40'

                if channel_str == '18607':          # band2 1.4M Low
                    self.setstartstopfre('1840', '1852')
                    start_fre_list = ['1840000000', '1849000000', '1850000000']
                    stop_fre_list = ['1849000000', '1850000000', '1852000000']
                    rbw_list = ['1000000', '20000', '100000']
                    vbw_list = ['3000000', '50000', '3000000']
                    reflev_list = [low_level, high_level, high_level]
                    limit_start_list = ['-13', '-13', high_limit]
                    limit_stop_list = ['-13', '-13', high_limit]
                elif channel_str == '19193':        # band2 1.4M High
                    self.setstartstopfre('1908', '1920')
                    start_fre_list = ['1908000000', '1910000000', '1911000000']
                    stop_fre_list = ['1910000000', '1911000000', '1920000000']
                    rbw_list = ['100000', '20000', '1000000']
                    vbw_list = ['300000', '50000', '3000000']
                    reflev_list = [high_level, high_level, low_level]
                    limit_start_list = [high_limit, '-13', '-13']
                    limit_stop_list = [high_limit, '-13', '-13']
                elif channel_str == '18615':        # band2 3M Low
                    self.setstartstopfre('1840', '1853')
                    start_fre_list = ['1840000000', '1849000000', '1850000000']
                    stop_fre_list = ['1849000000', '1850000000', '1853000000']
                    rbw_list = ['1000000', '30000', '100000']
                    vbw_list = ['3000000', '100000', '300000']
                    reflev_list = [low_level, high_level, high_level]
                    limit_start_list = ['-13', '-13', high_limit]
                    limit_stop_list = ['-13', '-13', high_limit]
                elif channel_str == '19185':        # band2 3M High
                    self.setstartstopfre('1907', '1920')
                    start_fre_list = ['1907000000', '1910000000', '1911000000']
                    stop_fre_list = ['1910000000', '1911000000', '1920000000']
                    rbw_list = ['100000', '30000', '1000000']
                    vbw_list = ['300000', '100000', '3000000']
                    reflev_list = [high_level, high_level, low_level]
                    limit_start_list = [high_limit, '-13', '-13']
                    limit_stop_list = [high_limit, '-13', '-13']
                elif channel_str == '18625':         # band2 5M Low
                    self.setstartstopfre('1840', '1855')
                    start_fre_list = ['1840000000', '1849000000', '1850000000']
                    stop_fre_list = ['1849000000', '1850000000', '1855000000']
                    rbw_list = ['1000000', '50000', '100000']
                    vbw_list = ['3000000', '150000', '300000']
                    reflev_list = [low_level, high_level, high_level]
                    limit_start_list = ['-13', '-13', high_limit]
                    limit_stop_list = ['-13', '-13', high_limit]
                elif channel_str == '19175':          # band2 5M High
                    self.setstartstopfre('1905', '1920')
                    start_fre_list = ['1905000000', '1910000000', '1911000000']
                    stop_fre_list = ['1910000000', '1911000000', '1920000000']
                    rbw_list = ['100000', '50000', '1000000']
                    vbw_list = ['300000', '150000', '3000000']
                    reflev_list = [high_level, high_level, low_level]
                    limit_start_list = [high_limit, '-13', '-13']
                    limit_stop_list = [high_limit, '-13', '-13']
                elif channel_str == '18650':          # band2 10M Low
                    self.setstartstopfre('1840', '1860')
                    start_fre_list = ['1840000000', '1849000000', '1850000000']
                    stop_fre_list = ['1849000000', '1850000000', '1860000000']
                    rbw_list = ['1000000', '100000', '100000']
                    vbw_list = ['3000000', '300000', '300000']
                    reflev_list = [low_level, high_level, high_level]
                    limit_start_list = ['-13', '-13', high_limit]
                    limit_stop_list = ['-13', '-13', high_limit]
                elif channel_str == '19150':           # band2 10M High
                    self.setstartstopfre('1900', '1920')
                    start_fre_list = ['1900000000', '1910000000', '1911000000']
                    stop_fre_list = ['1910000000', '1911000000', '1920000000']
                    rbw_list = ['100000', '100000', '1000000']
                    vbw_list = ['300000', '300000', '3000000']
                    reflev_list = [high_level, high_level, low_level]
                    limit_start_list = [high_limit, '-13', '-13']
                    limit_stop_list = [high_limit, '-13', '-13']
                elif channel_str == '18675':           # band2 15M Low
                    self.setstartstopfre('1840', '1865')
                    start_fre_list = ['1840000000', '1849000000', '1850000000']
                    stop_fre_list = ['1849000000', '1850000000', '1865000000']
                    rbw_list = ['1000000', '150000', '100000']
                    vbw_list = ['3000000', '500000', '300000']
                    reflev_list = [low_level, high_level, high_level]
                    limit_start_list = ['-13', '-13', high_limit]
                    limit_stop_list = ['-13', '-13', high_limit]
                elif channel_str == '19125':           # band2 15 High
                    self.setstartstopfre('1895', '1920')
                    start_fre_list = ['1895000000', '1910000000', '1911000000']
                    stop_fre_list = ['1910000000', '1911000000', '1920000000']
                    rbw_list = ['100000', '150000', '1000000']
                    vbw_list = ['300000', '500000', '3000000']
                    reflev_list = [high_level, high_level, low_level]
                    limit_start_list = [high_limit, '-13', '-13']
                    limit_stop_list = [high_limit, '-13', '-13']
                elif channel_str == '18700':           # band2 20M Low
                    self.setstartstopfre('1840', '1870')
                    start_fre_list = ['1840000000', '1849000000', '1850000000']
                    stop_fre_list = ['1849000000', '1850000000', '1870000000']
                    rbw_list = ['1000000', '200000', '100000']
                    vbw_list = ['3000000', '600000', '300000']
                    reflev_list = [low_level, high_level, high_level]
                    limit_start_list = ['-13', '-13', high_limit]
                    limit_stop_list = ['-13', '-13', high_limit]
                elif channel_str == '19100':           # band2 20M High
                    self.setstartstopfre('1890', '1920')
                    start_fre_list = ['1890000000', '1910000000', '1911000000']
                    stop_fre_list = ['1910000000', '1911000000', '1920000000']
                    rbw_list = ['100000', '200000', '1000000']
                    vbw_list = ['300000', '600000', '3000000']
                    reflev_list = [high_level, high_level, low_level]
                    limit_start_list = [high_limit, '-13', '-13']
                    limit_stop_list = [high_limit, '-13', '-13']
                elif channel_str == '19957':           # band4 1.4M Low
                    self.setstartstopfre('1700', '1712')
                    start_fre_list = ['1700000000', '1709000000', '1710000000']
                    stop_fre_list = ['1709000000', '1710000000', '1712000000']
                    rbw_list = ['1000000', '20000', '100000']
                    vbw_list = ['3000000', '60000', '300000']
                    reflev_list = [low_level, high_level, high_level]
                    limit_start_list = ['-13', '-13', high_limit]
                    limit_stop_list = ['-13', '-13', high_limit]
                elif channel_str == '20393':           # band4 1.4M High
                    self.setstartstopfre('1753', '1765')
                    start_fre_list = ['1753000000', '1755000000', '1756000000']
                    stop_fre_list = ['1755000000', '1756000000', '1765000000']
                    rbw_list = ['100000', '20000', '1000000']
                    vbw_list = ['300000', '60000', '3000000']
                    reflev_list = [high_level, high_level, low_level]
                    limit_start_list = ['60', '-13', '-13']
                    limit_stop_list = ['60', '-13', '-13']
                elif channel_str == '19965':           # band4 3M Low
                    self.setstartstopfre('1700', '1713')
                    start_fre_list = ['1700000000', '1709000000', '1710000000']
                    stop_fre_list = ['1709000000', '1710000000', '1713000000']
                    rbw_list = ['1000000', '30000', '100000']
                    vbw_list = ['3000000', '90000', '300000']
                    reflev_list = [low_level, high_level, high_level]
                    limit_start_list = ['-13', '-13', '60']
                    limit_stop_list = ['-13', '-13', '60']
                elif channel_str == '20385':           # band4 3M High
                    self.setstartstopfre('1752', '1765')
                    start_fre_list = ['1752000000', '1755000000', '1756000000']
                    stop_fre_list = ['1755000000', '1756000000', '1765000000']
                    rbw_list = ['100000', '30000', '1000000']
                    vbw_list = ['300000', '90000', '3000000']
                    reflev_list = [high_level, high_level, low_level]
                    limit_start_list = ['60', '-13', '-13']
                    limit_stop_list = ['60', '-13', '-13']
                elif channel_str == '19975':           # band4 5M Low
                    self.setstartstopfre('1700', '1715')
                    start_fre_list = ['1700000000', '1709000000', '1710000000']
                    stop_fre_list = ['1709000000', '1710000000', '1715000000']
                    rbw_list = ['1000000', '50000', '100000']
                    vbw_list = ['3000000', '150000', '300000']
                    reflev_list = [low_level, high_level, high_level]
                    limit_start_list = ['-13', '-13', '60']
                    limit_stop_list = ['-13', '-13', '60']
                elif channel_str == '20375':           # band4 5M High
                    self.setstartstopfre('1750', '1765')
                    start_fre_list = ['1750000000', '1755000000', '1756000000']
                    stop_fre_list = ['1755000000', '1756000000', '1765000000']
                    rbw_list = ['100000', '50000', '1000000']
                    vbw_list = ['300000', '150000', '3000000']
                    reflev_list = [high_level, high_level, low_level]
                    limit_start_list = ['60', '-13', '-13']
                    limit_stop_list = ['60', '-13', '-13']
                elif channel_str == '20000':           # band4 10M Low
                    self.setstartstopfre('1700', '1720')
                    start_fre_list = ['1700000000', '1709000000', '1710000000']
                    stop_fre_list = ['1709000000', '1710000000', '1720000000']
                    rbw_list = ['1000000', '100000', '100000']
                    vbw_list = ['3000000', '300000', '300000']
                    reflev_list = [low_level, high_level, high_level]
                    limit_start_list = ['-13', '-13', '60']
                    limit_stop_list = ['-13', '-13', '60']
                elif channel_str == '20350':           # band4 10M High
                    self.setstartstopfre('1745', '1765')
                    start_fre_list = ['1745000000', '1755000000', '1756000000']
                    stop_fre_list = ['1755000000', '1756000000', '1765000000']
                    rbw_list = ['100000', '100000', '1000000']
                    vbw_list = ['300000', '300000', '3000000']
                    reflev_list = [high_level, high_level, low_level]
                    limit_start_list = ['60', '-13', '-13']
                    limit_stop_list = ['60', '-13', '-13']
                elif channel_str == '20025':           # band4 15M Low
                    self.setstartstopfre('1700', '1725')
                    start_fre_list = ['1700000000', '1709000000', '1710000000']
                    stop_fre_list = ['1709000000', '1710000000', '1725000000']
                    rbw_list = ['1000000', '150000', '100000']
                    vbw_list = ['3000000', '450000', '300000']
                    reflev_list = [low_level, high_level, high_level]
                    limit_start_list = ['-13', '-13', '60']
                    limit_stop_list = ['-13', '-13', '60']
                elif channel_str == '20325':           # band4 15M High
                    self.setstartstopfre('1740', '1765')
                    start_fre_list = ['1740000000', '1755000000', '1756000000']
                    stop_fre_list = ['1755000000', '1756000000', '1765000000']
                    rbw_list = ['100000', '150000', '1000000']
                    vbw_list = ['300000', '450000', '3000000']
                    reflev_list = [high_level, high_level, low_level]
                    limit_start_list = ['60', '-13', '-13']
                    limit_stop_list = ['60', '-13', '-13']
                elif channel_str == '20050':           # band4 20M Low
                    self.setstartstopfre('1700', '1730')
                    start_fre_list = ['1700000000', '1709000000', '1710000000']
                    stop_fre_list = ['1709000000', '1710000000', '1730000000']
                    rbw_list = ['1000000', '200000', '100000']
                    vbw_list = ['3000000', '600000', '300000']
                    reflev_list = [low_level, high_level, high_level]
                    limit_start_list = ['-13', '-13', '60']
                    limit_stop_list = ['-13', '-13', '60']
                elif channel_str == '20300':           # band4 20M High
                    self.setstartstopfre('1735', '1765')
                    start_fre_list = ['1735000000', '1755000000', '1756000000']
                    stop_fre_list = ['1755000000', '1756000000', '1765000000']
                    rbw_list = ['100000', '200000', '1000000']
                    vbw_list = ['300000', '600000', '3000000']
                    reflev_list = [high_level, high_level, low_level]
                    limit_start_list = ['60', '-13', '-13']
                    limit_stop_list = ['60', '-13', '-13']
                elif channel_str == '20407':           # band5 1.4M Low
                    self.setstartstopfre('815', '826')
                    start_fre_list = ['815000000', '823000000', '824000000']
                    stop_fre_list = ['823000000', '824000000', '826000000']
                    rbw_list = ['100000', '20000', '100000']
                    vbw_list = ['300000', '60000', '300000']
                    reflev_list = [low_level, high_level, high_level]
                    limit_start_list = ['-13', '-13', '60']
                    limit_stop_list = ['-13', '-13', '60']
                elif channel_str == '20643':           # band5 1.4M High
                    self.setstartstopfre('847', '860')
                    start_fre_list = ['847000000', '849000000', '850000000']
                    stop_fre_list = ['849000000', '850000000', '860000000']
                    rbw_list = ['100000', '20000', '100000']
                    vbw_list = ['300000', '60000', '300000']
                    reflev_list = [high_level, high_level, low_level]
                    limit_start_list = ['60', '-13', '-13']
                    limit_stop_list = ['60', '-13', '-13']
                elif channel_str == '20415':           # band5 3M Low
                    self.setstartstopfre('815', '827')
                    start_fre_list = ['815000000', '823000000', '824000000']
                    stop_fre_list = ['823000000', '824000000', '827000000']
                    rbw_list = ['100000', '30000', '100000']
                    vbw_list = ['300000', '90000', '300000']
                    reflev_list = [low_level, high_level, high_level]
                    limit_start_list = ['-13', '-13', '60']
                    limit_stop_list = ['-13', '-13', '60']
                elif channel_str == '20635':           # band5 3M High
                    self.setstartstopfre('846', '860')
                    start_fre_list = ['846000000', '849000000', '850000000']
                    stop_fre_list = ['849000000', '850000000', '860000000']
                    rbw_list = ['100000', '30000', '100000']
                    vbw_list = ['300000', '90000', '300000']
                    reflev_list = [high_level, high_level, low_level]
                    limit_start_list = ['60', '-13', '-13']
                    limit_stop_list = ['60', '-13', '-13']
                elif channel_str == '20425':           # band5 5M Low
                    self.setstartstopfre('815', '829')
                    start_fre_list = ['815000000', '823000000', '824000000']
                    stop_fre_list = ['823000000', '824000000', '829000000']
                    rbw_list = ['100000', '50000', '100000']
                    vbw_list = ['300000', '150000', '300000']
                    reflev_list = [low_level, high_level, high_level]
                    limit_start_list = ['-13', '-13', '60']
                    limit_stop_list = ['-13', '-13', '60']
                elif channel_str == '20625':           # band5 5M High
                    self.setstartstopfre('844', '860')
                    start_fre_list = ['844000000', '849000000', '850000000']
                    stop_fre_list = ['849000000', '850000000', '860000000']
                    rbw_list = ['100000', '50000', '100000']
                    vbw_list = ['300000', '150000', '300000']
                    reflev_list = [high_level, high_level, low_level]
                    limit_start_list = ['60', '-13', '-13']
                    limit_stop_list = ['60', '-13', '-13']
                elif channel_str == '20450':           # band5 10M Low
                    self.setstartstopfre('815', '834')
                    start_fre_list = ['815000000', '823000000', '824000000']
                    stop_fre_list = ['823000000', '824000000', '834000000']
                    rbw_list = ['100000', '100000', '100000']
                    vbw_list = ['300000', '300000', '300000']
                    reflev_list = [low_level, high_level, high_level]
                    limit_start_list = ['-13', '-13', '60']
                    limit_stop_list = ['-13', '-13', '60']
                elif channel_str == '20600':           # band5 10M High
                    self.setstartstopfre('839', '860')
                    start_fre_list = ['839000000', '849000000', '850000000']
                    stop_fre_list = ['849000000', '850000000', '860000000']
                    rbw_list = ['100000', '100000', '100000']
                    vbw_list = ['300000', '300000', '300000']
                    reflev_list = [high_level, high_level, low_level]
                    limit_start_list = ['60', '-13', '-13']
                    limit_stop_list = ['60', '-13', '-13']
                elif channel_str == '20775':           # band7 5M Low
                    self.setstartstopfre('2475', '2505')
                    start_fre_list = ['2475000000', '2490000000', '2495000000', '2496000000']
                    stop_fre_list = ['2490000000', '2495000000', '2496000000', '2505000000']
                    rbw_list = ['1000000', '1000000', '50000', '100000']
                    vbw_list = ['3000000', '3000000', '150000', '300000']
                    reflev_list = [low_level, low_level, high_level, high_level]
                    limit_start_list = ['-25', '-13', '-13', '60']
                    limit_stop_list = ['-25', '-13', '-13', '60']
                elif channel_str == '21425':           # band7 5M High
                    self.setstartstopfre('2565', '2595')
                    start_fre_list = ['2565000000', '2570000000', '2571000000', '2575000000', '2576000000']
                    stop_fre_list = ['2570000000', '2571000000', '2575000000', '2576000000', '2595000000']
                    rbw_list = ['100000', '100000', '1000000', '1000000', '1000000']
                    vbw_list = ['300000', '300000', '3000000', '3000000', '3000000']
                    reflev_list = [high_level, high_level, low_level, low_level, low_level]
                    limit_start_list = ['60', '-10', '-10', '-13', '-25']
                    limit_stop_list = ['60', '-10', '-10', '-13', '-25']
                elif channel_str == '20800':           # band7 10M Low
                    self.setstartstopfre('2475', '2510')
                    start_fre_list = ['2475000000', '2490000000', '2495000000', '2496000000']
                    stop_fre_list = ['2490000000', '2495000000', '2496000000', '2510000000']
                    rbw_list = ['1000000', '1000000', '100000', '100000']
                    vbw_list = ['3000000', '3000000', '300000', '300000']
                    reflev_list = [low_level, low_level, high_level, high_level]
                    limit_start_list = ['-25', '-13', '-13', '60']
                    limit_stop_list = ['-25', '-13', '-13', '60']
                elif channel_str == '21400':           # band7 10M High
                    self.setstartstopfre('2560', '2595')
                    start_fre_list = ['2560000000', '2570000000', '2571000000', '2575000000', '2580000000']
                    stop_fre_list = ['2570000000', '2571000000', '2575000000', '2580000000', '2595000000']
                    rbw_list = ['100000', '200000', '1000000', '1000000', '1000000']
                    vbw_list = ['300000', '600000', '3000000', '3000000', '3000000']
                    reflev_list = [high_level, high_level, low_level, low_level, low_level]
                    limit_start_list = ['60', '-10', '-10', '-13', '-25']
                    limit_stop_list = ['60', '-10', '-10', '-13', '-25']
                elif channel_str == '20825':           # band7 15M Low
                    self.setstartstopfre('2475', '2515')
                    start_fre_list = ['2475000000', '2490000000', '2495000000', '2496000000']
                    stop_fre_list = ['2490000000', '2495000000', '2496000000', '2515000000']
                    rbw_list = ['1000000', '1000000', '150000', '100000']
                    vbw_list = ['3000000', '3000000', '450000', '300000']
                    reflev_list = [low_level, low_level, high_level, high_level]
                    limit_start_list = ['-25', '-13', '-13', '60']
                    limit_stop_list = ['-25', '-13', '-13', '60']
                elif channel_str == '21375':           # band7 15M High
                    self.setstartstopfre('2555', '2595')
                    start_fre_list = ['2555000000', '2570000000', '2571000000', '2575000000', '2585000000']
                    stop_fre_list = ['2570000000', '2571000000', '2575000000', '2585000000', '2595000000']
                    rbw_list = ['100000', '300000', '1000000', '1000000', '1000000']
                    vbw_list = ['300000', '900000', '3000000', '3000000', '3000000']
                    reflev_list = [high_level, high_level, low_level, low_level, low_level]
                    limit_start_list = ['60', '-10', '-10', '-13', '-25']
                    limit_stop_list = ['60', '-10', '-10', '-13', '-25']
                elif channel_str == '20850':           # band7 20M Low
                    self.setstartstopfre('2475', '2520')
                    start_fre_list = ['2475000000', '2490000000', '2495000000', '2496000000']
                    stop_fre_list = ['2490000000', '2495000000', '2496000000', '2520000000']
                    rbw_list = ['1000000', '1000000', '200000', '100000']
                    vbw_list = ['3000000', '3000000', '600000', '300000']
                    reflev_list = [low_level, low_level, high_level, high_level]
                    limit_start_list = ['-25', '-13', '-13', '60']
                    limit_stop_list = ['-25', '-13', '-13', '60']
                elif channel_str == '21350':           # band7 20M High
                    self.setstartstopfre('2550', '2595')
                    start_fre_list = ['2550000000', '2570000000', '2571000000', '2575000000', '2590000000']
                    stop_fre_list = ['2570000000', '2571000000', '2575000000', '2590000000', '2595000000']
                    rbw_list = ['100000', '500000', '1000000', '1000000', '1000000']
                    vbw_list = ['300000', '1500000', '3000000', '3000000', '3000000']
                    reflev_list = [high_level, high_level, low_level, low_level, low_level]
                    limit_start_list = ['60', '-10', '-10', '-13', '-25']
                    limit_stop_list = ['60', '-10', '-10', '-13', '-25']
                elif channel_str == '23017':           # band12 1.4M Low
                    self.setstartstopfre('690', '701')
                    start_fre_list = ['690000000', '698000000', '699000000']
                    stop_fre_list = ['698000000', '699000000', '701000000']
                    rbw_list = ['100000', '30000', '100000']
                    vbw_list = ['300000', '100000', '300000']
                    reflev_list = [low_level, high_level, high_level]
                    limit_start_list = ['-13', '-13', '60']
                    limit_stop_list = ['-13', '-13', '60']
                elif channel_str == '23173':           # band12 1.4M High
                    self.setstartstopfre('714', '725')
                    start_fre_list = ['714000000', '716000000', '716100000']
                    stop_fre_list = ['716000000', '716100000', '725000000']
                    rbw_list = ['100000', '30000', '100000']
                    vbw_list = ['300000', '100000', '300000']
                    reflev_list = [high_level, high_level, low_level]
                    limit_start_list = ['60', '-13', '-13']
                    limit_stop_list = ['60', '-13', '-13']
                elif channel_str == '23025':           # band12 3M Low
                    self.setstartstopfre('690', '702')
                    start_fre_list = ['690000000', '698000000', '699000000']
                    stop_fre_list = ['698000000', '699000000', '702000000']
                    rbw_list = ['100000', '30000', '100000']
                    vbw_list = ['300000', '100000', '300000']
                    reflev_list = [low_level, high_level, high_level]
                    limit_start_list = ['-13', '-13', '60']
                    limit_stop_list = ['-13', '-13', '60']
                elif channel_str == '23165':           # band12 3M High
                    self.setstartstopfre('713', '725')
                    start_fre_list = ['713000000', '716000000', '716100000']
                    stop_fre_list = ['716000000', '716100000', '725000000']
                    rbw_list = ['100000', '30000', '100000']
                    vbw_list = ['300000', '100000', '300000']
                    reflev_list = [high_level, high_level, low_level]
                    limit_start_list = ['60', '-13', '-13']
                    limit_stop_list = ['60', '-13', '-13']
                elif channel_str == '23035':           # band12 5M Low
                    self.setstartstopfre('690', '704')
                    start_fre_list = ['690000000', '698000000', '699000000']
                    stop_fre_list = ['698000000', '699000000', '704000000']
                    rbw_list = ['100000', '30000', '100000']
                    vbw_list = ['300000', '100000', '300000']
                    reflev_list = [low_level, high_level, high_level]
                    limit_start_list = ['-13', '-13', '60']
                    limit_stop_list = ['-13', '-13', '60']
                elif channel_str == '23155':           # band12 5M High
                    self.setstartstopfre('711', '725')
                    start_fre_list = ['711000000', '716000000', '716100000']
                    stop_fre_list = ['716000000', '716100000', '725000000']
                    rbw_list = ['100000', '30000', '100000']
                    vbw_list = ['300000', '100000', '300000']
                    reflev_list = [high_level, high_level, low_level]
                    limit_start_list = ['60', '-13', '-13']
                    limit_stop_list = ['60', '-13', '-13']
                elif channel_str == '23060':           # band12 10M Low
                    self.setstartstopfre('690', '709')
                    start_fre_list = ['690000000', '698000000', '699000000']
                    stop_fre_list = ['698000000', '699000000', '709000000']
                    rbw_list = ['100000', '30000', '100000']
                    vbw_list = ['300000', '100000', '300000']
                    reflev_list = [low_level, high_level, high_level]
                    limit_start_list = ['-13', '-13', '60']
                    limit_stop_list = ['-13', '-13', '60']
                elif channel_str == '23130':           # band12 10M High
                    self.setstartstopfre('706', '725')
                    start_fre_list = ['706000000', '716000000', '716100000']
                    stop_fre_list = ['716000000', '716100000', '725000000']
                    rbw_list = ['100000', '30000', '100000']
                    vbw_list = ['300000', '100000', '300000']
                    reflev_list = [high_level, high_level, low_level]
                    limit_start_list = ['60', '-13', '-13']
                    limit_stop_list = ['60', '-13', '-13']
                elif channel_str == '23755':           # band17 5M Low
                    self.setstartstopfre('690', '709')
                    start_fre_list = ['690000000', '703900000', '704000000']
                    stop_fre_list = ['703900000', '704000000', '709000000']
                    rbw_list = ['100000', '30000', '100000']
                    vbw_list = ['300000', '100000', '300000']
                    reflev_list = [high_level, high_level, high_level]
                    limit_start_list = ['-13', '-13', '60']
                    limit_stop_list = ['-13', '-13', '60']
                elif channel_str == '23825':           # band17 5M High
                    self.setstartstopfre('711', '725')
                    start_fre_list = ['711000000', '716000000', '716100000']
                    stop_fre_list = ['716000000', '716100000', '725000000']
                    rbw_list = ['100000', '30000', '100000']
                    vbw_list = ['300000', '100000', '300000']
                    reflev_list = [high_level, high_level, high_level]
                    limit_start_list = ['60', '-13', '-13']
                    limit_stop_list = ['60', '-13', '-13']
                elif channel_str == '23780':           # band17 10M Low
                    self.setstartstopfre('690', '714')
                    start_fre_list = ['690000000', '703900000', '704000000']
                    stop_fre_list = ['703900000', '704000000', '714000000']
                    rbw_list = ['100000', '30000', '100000']
                    vbw_list = ['300000', '100000', '300000']
                    reflev_list = [high_level, high_level, high_level]
                    limit_start_list = ['-13', '-13', '60']
                    limit_stop_list = ['-13', '-13', '60']
                elif channel_str == '23800':           # band17 10M High
                    self.setstartstopfre('706', '725')
                    start_fre_list = ['706000000', '716000000', '716100000']
                    stop_fre_list = ['716000000', '716100000', '725000000']
                    rbw_list = ['100000', '30000', '100000']
                    vbw_list = ['300000', '100000', '300000']
                    reflev_list = [high_level, high_level, high_level]
                    limit_start_list = ['60', '-13', '-13']
                    limit_stop_list = ['60', '-13', '-13']
                elif channel_str == '26047':           # band25 1.4M Low
                    self.setstartstopfre('1840', '1852')
                    start_fre_list = ['1840000000', '1849000000', '1850000000']
                    stop_fre_list = ['1849000000', '1850000000', '1852000000']
                    rbw_list = ['1000000', '20000', '100000']
                    vbw_list = ['3000000', '60000', '300000']
                    reflev_list = [low_level, high_level, high_level]
                    limit_start_list = ['-13', '-13', '60']
                    limit_stop_list = ['-13', '-13', '60']
                elif channel_str == '26683':           # band25 1.4M High
                    self.setstartstopfre('1913', '1925')
                    start_fre_list = ['1913000000', '1915000000', '1916000000']
                    stop_fre_list = ['1915000000', '1916000000', '1925000000']
                    rbw_list = ['100000', '20000', '1000000']
                    vbw_list = ['300000', '60000', '3000000']
                    reflev_list = [high_level, high_level, low_level]
                    limit_start_list = ['60', '-13', '-13']
                    limit_stop_list = ['60', '-13', '-13']
                elif channel_str == '26055':           # band25 3M Low
                    self.setstartstopfre('1840', '1853')
                    start_fre_list = ['1840000000', '1849000000', '1850000000']
                    stop_fre_list = ['1849000000', '1850000000', '1853000000']
                    rbw_list = ['1000000', '30000', '100000']
                    vbw_list = ['3000000', '100000', '300000']
                    reflev_list = [low_level, high_level, high_level]
                    limit_start_list = ['-13', '-13', '60']
                    limit_stop_list = ['-13', '-13', '60']
                elif channel_str == '26675':           # band25 3M High
                    self.setstartstopfre('1912', '1925')
                    start_fre_list = ['1912000000', '1915000000', '1916000000']
                    stop_fre_list = ['1915000000', '1916000000', '1925000000']
                    rbw_list = ['100000', '30000', '1000000']
                    vbw_list = ['300000', '100000', '3000000']
                    reflev_list = [high_level, high_level, low_level]
                    limit_start_list = ['60', '-13', '-13']
                    limit_stop_list = ['60', '-13', '-13']
                elif channel_str == '26065':           # band25 5M Low
                    self.setstartstopfre('1840', '1855')
                    start_fre_list = ['1840000000', '1849000000', '1850000000']
                    stop_fre_list = ['1849000000', '1850000000', '1855000000']
                    rbw_list = ['1000000', '50000', '100000']
                    vbw_list = ['3000000', '150000', '300000']
                    reflev_list = [low_level, high_level, high_level]
                    limit_start_list = ['-13', '-13', '60']
                    limit_stop_list = ['-13', '-13', '60']
                elif channel_str == '26665':           # band25 5M High
                    self.setstartstopfre('1910', '1925')
                    start_fre_list = ['1910000000', '1915000000', '1916000000']
                    stop_fre_list = ['1915000000', '1916000000', '1925000000']
                    rbw_list = ['100000', '50000', '1000000']
                    vbw_list = ['300000', '150000', '3000000']
                    reflev_list = [high_level, high_level, low_level]
                    limit_start_list = ['60', '-13', '-13']
                    limit_stop_list = ['60', '-13', '-13']
                elif channel_str == '26090':           # band25 10M Low
                    self.setstartstopfre('1840', '1860')
                    start_fre_list = ['1840000000', '1849000000', '1850000000']
                    stop_fre_list = ['1849000000', '1850000000', '1860000000']
                    rbw_list = ['1000000', '100000', '100000']
                    vbw_list = ['3000000', '300000', '300000']
                    reflev_list = [low_level, high_level, high_level]
                    limit_start_list = ['-13', '-13', '60']
                    limit_stop_list = ['-13', '-13', '60']
                elif channel_str == '26640':           # band25 10M High
                    self.setstartstopfre('1905', '1925')
                    start_fre_list = ['1905000000', '1915000000', '1916000000']
                    stop_fre_list = ['1915000000', '1916000000', '1925000000']
                    rbw_list = ['100000', '100000', '1000000']
                    vbw_list = ['300000', '300000', '3000000']
                    reflev_list = [high_level, high_level, low_level]
                    limit_start_list = ['60', '-13', '-13']
                    limit_stop_list = ['60', '-13', '-13']
                elif channel_str == '26115':           # band25 15M Low
                    self.setstartstopfre('1840', '1865')
                    start_fre_list = ['1840000000', '1849000000', '1850000000']
                    stop_fre_list = ['1849000000', '1850000000', '1865000000']
                    rbw_list = ['1000000', '150000', '100000']
                    vbw_list = ['3000000', '450000', '300000']
                    reflev_list = [low_level, high_level, high_level]
                    limit_start_list = ['-13', '-13', '60']
                    limit_stop_list = ['-13', '-13', '60']
                elif channel_str == '26615':           # band25 15M High
                    self.setstartstopfre('1900', '1925')
                    start_fre_list = ['1900000000', '1915000000', '1916000000']
                    stop_fre_list = ['1915000000', '1916000000', '1925000000']
                    rbw_list = ['100000', '150000', '1000000']
                    vbw_list = ['300000', '450000', '3000000']
                    reflev_list = [high_level, high_level, low_level]
                    limit_start_list = ['60', '-13', '-13']
                    limit_stop_list = ['60', '-13', '-13']
                elif channel_str == '26140':           # band25 20M Low
                    self.setstartstopfre('1840', '1870')
                    start_fre_list = ['1840000000', '1849000000', '1850000000']
                    stop_fre_list = ['1849000000', '1850000000', '1870000000']
                    rbw_list = ['1000000', '200000', '100000']
                    vbw_list = ['3000000', '600000', '300000']
                    reflev_list = [low_level, high_level, high_level]
                    limit_start_list = ['-13', '-13', '60']
                    limit_stop_list = ['-13', '-13', '60']
                elif channel_str == '26590':           # band25 20M High
                    self.setstartstopfre('1895', '1925')
                    start_fre_list = ['1895000000', '1915000000', '1916000000']
                    stop_fre_list = ['1915000000', '1916000000', '1925000000']
                    rbw_list = ['100000', '200000', '1000000']
                    vbw_list = ['300000', '600000', '3000000']
                    reflev_list = [high_level, high_level, low_level]
                    limit_start_list = ['60', '-13', '-13']
                    limit_stop_list = ['60', '-13', '-13']
                elif channel_str == '26697':           # band26 1.4M Low
                    self.setstartstopfre('805', '816')
                    start_fre_list = ['805000000', '813000000', '814000000']
                    stop_fre_list = ['813000000', '814000000', '816000000']
                    rbw_list = ['100000', '20000', '100000']
                    vbw_list = ['300000', '60000', '300000']
                    reflev_list = [high_level, high_level, high_level]
                    limit_start_list = ['-13', '-13', '60']
                    limit_stop_list = ['-13', '-13', '60']
                elif channel_str == '27033':           # band26 1.4M High
                    self.setstartstopfre('847', '860')
                    start_fre_list = ['847000000', '849000000', '850000000']
                    stop_fre_list = ['849000000', '850000000', '860000000']
                    rbw_list = ['100000', '20000', '100000']
                    vbw_list = ['300000', '60000', '300000']
                    reflev_list = [high_level, high_level, high_level]
                    limit_start_list = ['60', '-13', '-13']
                    limit_stop_list = ['60', '-13', '-13']
                elif channel_str == '26705':           # band26 3M Low
                    self.setstartstopfre('805', '817')
                    start_fre_list = ['805000000', '813000000', '814000000']
                    stop_fre_list = ['813000000', '814000000', '817000000']
                    rbw_list = ['100000', '30000', '100000']
                    vbw_list = ['300000', '90000', '300000']
                    reflev_list = [high_level, high_level, high_level]
                    limit_start_list = ['-13', '-13', '60']
                    limit_stop_list = ['-13', '-13', '60']
                elif channel_str == '27025':           # band26 3M High
                    self.setstartstopfre('846', '860')
                    start_fre_list = ['846000000', '849000000', '850000000']
                    stop_fre_list = ['849000000', '850000000', '860000000']
                    rbw_list = ['100000', '30000', '100000']
                    vbw_list = ['300000', '90000', '300000']
                    reflev_list = [high_level, high_level, high_level]
                    limit_start_list = ['60', '-13', '-13']
                    limit_stop_list = ['60', '-13', '-13']
                elif channel_str == '26715':           # band26 5M Low
                    self.setstartstopfre('805', '819')
                    start_fre_list = ['805000000', '813000000', '814000000']
                    stop_fre_list = ['813000000', '814000000', '819000000']
                    rbw_list = ['100000', '50000', '100000']
                    vbw_list = ['300000', '150000', '300000']
                    reflev_list = [high_level, high_level, high_level]
                    limit_start_list = ['-13', '-13', '60']
                    limit_stop_list = ['-13', '-13', '60']
                elif channel_str == '27015':           # band26 5M High
                    self.setstartstopfre('844', '860')
                    start_fre_list = ['844000000', '849000000', '850000000']
                    stop_fre_list = ['849000000', '850000000', '860000000']
                    rbw_list = ['100000', '50000', '100000']
                    vbw_list = ['300000', '150000', '300000']
                    reflev_list = [high_level, high_level, high_level]
                    limit_start_list = ['60', '-13', '-13']
                    limit_stop_list = ['60', '-13', '-13']
                elif channel_str == '26740':           # band26 10M Low
                    self.setstartstopfre('805', '824')
                    start_fre_list = ['805000000', '813000000', '814000000']
                    stop_fre_list = ['813000000', '814000000', '824000000']
                    rbw_list = ['100000', '100000', '100000']
                    vbw_list = ['300000', '300000', '300000']
                    reflev_list = [high_level, high_level, high_level]
                    limit_start_list = ['-13', '-13', '60']
                    limit_stop_list = ['-13', '-13', '60']
                elif channel_str == '26990':           # band26 10M High
                    self.setstartstopfre('839', '860')
                    start_fre_list = ['839000000', '849000000', '850000000']
                    stop_fre_list = ['849000000', '850000000', '860000000']
                    rbw_list = ['100000', '100000', '100000']
                    vbw_list = ['300000', '300000', '300000']
                    reflev_list = [high_level, high_level, high_level]
                    limit_start_list = ['60', '-13', '-13']
                    limit_stop_list = ['60', '-13', '-13']
                elif channel_str == '26765':           # band26 15M Low
                    self.setstartstopfre('805', '829')
                    start_fre_list = ['805000000', '813000000', '814000000']
                    stop_fre_list = ['813000000', '814000000', '829000000']
                    rbw_list = ['100000', '150000', '100000']
                    vbw_list = ['300000', '450000', '300000']
                    reflev_list = [high_level, high_level, high_level]
                    limit_start_list = ['-13', '-13', '60']
                    limit_stop_list = ['-13', '-13', '60']
                elif channel_str == '26965':           # band26 15M High
                    self.setstartstopfre('834', '860')
                    start_fre_list = ['834000000', '849000000', '850000000']
                    stop_fre_list = ['849000000', '850000000', '860000000']
                    rbw_list = ['100000', '150000', '100000']
                    vbw_list = ['300000', '450000', '300000']
                    reflev_list = [high_level, high_level, high_level]
                    limit_start_list = ['60', '-13', '-13']
                    limit_stop_list = ['60', '-13', '-13']
                elif channel_str == '37775':           # band38 5M Low
                    self.setstartstopfre('2535', '2576')
                    start_fre_list = ['2535000000', '2564000000', '2569000000', '2570000000']
                    stop_fre_list = ['2564000000', '2569000000', '2570000000', '2576000000']
                    rbw_list = ['1000000', '1000000', '50000', '100000']
                    vbw_list = ['3000000', '3000000', '150000', '300000']
                    reflev_list = [low_level, low_level, low_level, high_level]
                    limit_start_list = ['-25', '-13', '-13', '60']
                    limit_stop_list = ['-25', '-13', '-13', '60']
                elif channel_str == '38225':           # band38 5M High
                    self.setstartstopfre('2614', '2645')
                    start_fre_list = ['2614000000', '2620000000', '2621000000', '2625000000', '2626000000']
                    stop_fre_list = ['2620000000', '2621000000', '2625000000', '2626000000', '2645000000']
                    rbw_list = ['100000', '100000', '1000000', '1000000', '1000000']
                    vbw_list = ['300000', '300000', '3000000', '3000000', '3000000']
                    reflev_list = [high_level, low_level, low_level, low_level, low_level]
                    limit_start_list = ['60', '-10', '-10', '-13', '-25']
                    limit_stop_list = ['60', '-10', '-10', '-13', '-25']
                elif channel_str == '37800':           # band38 10M Low
                    self.setstartstopfre('2545', '2580')
                    start_fre_list = ['2545000000', '25600000000', '2569000000', '2570000000']
                    stop_fre_list = ['2560000000', '2569000000', '2570000000', '2580000000']
                    rbw_list = ['1000000', '1000000', '100000', '100000']
                    vbw_list = ['3000000', '3000000', '300000', '300000']
                    reflev_list = [low_level, low_level, low_level, high_level]
                    limit_start_list = ['-25', '-13', '-13', '60']
                    limit_stop_list = ['-25', '-13', '-13', '60']
                elif channel_str == '38200':           # band38 10M High
                    self.setstartstopfre('2610', '2645')
                    start_fre_list = ['2610000000', '2620000000', '2621000000', '2625000000', '2630000000']
                    stop_fre_list = ['2620000000', '2621000000', '2625000000', '2630000000', '2645000000']
                    rbw_list = ['100000', '200000', '1000000', '1000000', '1000000']
                    vbw_list = ['300000', '600000', '3000000', '3000000', '3000000']
                    reflev_list = [high_level, low_level, low_level, low_level, low_level]
                    limit_start_list = ['60', '-10', '-10', '-13', '-25']
                    limit_stop_list = ['60', '-10', '-10', '-13', '-25']
                elif channel_str == '37825':           # band38 15M Low
                    self.setstartstopfre('2540', '2585')
                    start_fre_list = ['2540000000', '2555000000', '2569000000', '2570000000']
                    stop_fre_list = ['2555000000', '2569000000', '2570000000', '2585000000']
                    rbw_list = ['1000000', '1000000', '150000', '100000']
                    vbw_list = ['3000000', '3000000', '450000', '300000']
                    reflev_list = [low_level, low_level, low_level, high_level]
                    limit_start_list = ['-25', '-13', '-13', '60']
                    limit_stop_list = ['-25', '-13', '-13', '60']
                elif channel_str == '38175':           # band38 15M High
                    self.setstartstopfre('2605', '2645')
                    start_fre_list = ['2605000000', '2620000000', '2621000000', '2625000000', '2635000000']
                    stop_fre_list = ['2620000000', '2621000000', '2625000000', '2635000000', '2645000000']
                    rbw_list = ['100000', '300000', '1000000', '1000000', '1000000']
                    vbw_list = ['300000', '900000', '3000000', '3000000', '3000000']
                    reflev_list = [high_level, low_level, low_level, low_level, low_level]
                    limit_start_list = ['60', '-10', '-10', '-13', '-25']
                    limit_stop_list = ['60', '-10', '-10', '-13', '-25']
                elif channel_str == '37850':           # band38 20M Low
                    self.setstartstopfre('2535', '2590')
                    start_fre_list = ['2535000000', '2550000000', '2569000000', '2570000000']
                    stop_fre_list = ['2550000000', '2569000000', '2570000000', '2590000000']
                    rbw_list = ['1000000', '1000000', '200000', '100000']
                    vbw_list = ['3000000', '3000000', '600000', '300000']
                    reflev_list = [low_level, low_level, low_level, high_level]
                    limit_start_list = ['-25', '-13', '-13', '60']
                    limit_stop_list = ['-25', '-13', '-13', '60']
                elif channel_str == '38150':           # band38 20M High
                    self.setstartstopfre('2600', '2645')
                    start_fre_list = ['2600000000', '2620000000', '2621000000', '2625000000', '2640000000']
                    stop_fre_list = ['2620000000', '2621000000', '2625000000', '2640000000', '2645000000']
                    rbw_list = ['100000', '500000', '1000000', '1000000', '1000000']
                    vbw_list = ['300000', '1500000', '3000000', '3000000', '3000000']
                    reflev_list = [high_level, low_level, low_level, low_level, low_level]
                    limit_start_list = ['60', '-10', '-10', '-13', '-25']
                    limit_stop_list = ['60', '-10', '-10', '-13', '-25']
                elif channel_str == '39675':           # band41 5M Low
                    self.setstartstopfre('2475', '2501')
                    start_fre_list = ['2475000000', '2490000000', '2495000000', '2496000000']
                    stop_fre_list = ['2490000000', '2495000000', '2496000000', '2501000000']
                    rbw_list = ['1000000', '1000000', '50000', '100000']
                    vbw_list = ['3000000', '3000000', '150000', '300000']
                    reflev_list = [low_level, low_level, low_level, high_level]
                    limit_start_list = ['-25', '-13', '-13', '60']
                    limit_stop_list = ['-25', '-13', '-13', '60']
                elif channel_str == '41565':           # band41 5M High
                    self.setstartstopfre('2685', '2715')
                    start_fre_list = ['2685000000', '2690000000', '2691000000', '2695000000', '2696000000']
                    stop_fre_list = ['2690000000', '2691000000', '2695000000', '2696000000', '2715000000']
                    rbw_list = ['100000', '100000', '1000000', '1000000', '1000000']
                    vbw_list = ['300000', '300000', '3000000', '3000000', '3000000']
                    reflev_list = [high_level, low_level, low_level, low_level, low_level]
                    limit_start_list = ['60', '-10', '-10', '-13', '-25']
                    limit_stop_list = ['60', '-10', '-10', '-13', '-25']
                elif channel_str == '39700':           # band41 10M Low
                    self.setstartstopfre('2475', '2506')
                    start_fre_list = ['2475000000', '2490000000', '2495000000', '2496000000']
                    stop_fre_list = ['2490000000', '2495000000', '2496000000', '2506000000']
                    rbw_list = ['1000000', '1000000', '100000', '100000']
                    vbw_list = ['3000000', '3000000', '300000', '300000']
                    reflev_list = [low_level, low_level, low_level, high_level]
                    limit_start_list = ['-25', '-13', '-13', '60']
                    limit_stop_list = ['-25', '-13', '-13', '60']
                elif channel_str == '41540':           # band41 10M High
                    self.setstartstopfre('2680', '2715')
                    start_fre_list = ['2680000000', '2690000000', '2691000000', '2695000000', '2700000000']
                    stop_fre_list = ['2690000000', '2691000000', '2695000000', '2700000000', '2715000000']
                    rbw_list = ['100000', '200000', '1000000', '1000000', '1000000']
                    vbw_list = ['300000', '600000', '3000000', '3000000', '3000000']
                    reflev_list = [high_level, low_level, low_level, low_level, low_level]
                    limit_start_list = ['60', '-10', '-10', '-13', '-25']
                    limit_stop_list = ['60', '-10', '-10', '-13', '-25']
                elif channel_str == '39725':           # band41 15M Low
                    self.setstartstopfre('2475', '2511')
                    start_fre_list = ['2475000000', '2490000000', '2495000000', '2496000000']
                    stop_fre_list = ['2490000000', '2495000000', '2496000000', '2511000000']
                    rbw_list = ['1000000', '1000000', '150000', '100000']
                    vbw_list = ['3000000', '3000000', '450000', '300000']
                    reflev_list = [low_level, low_level, low_level, high_level]
                    limit_start_list = ['-25', '-13', '-13', '60']
                    limit_stop_list = ['-25', '-13', '-13', '60']
                elif channel_str == '41515':           # band41 15M High
                    self.setstartstopfre('2675', '2715')
                    start_fre_list = ['2675000000', '2690000000', '2691000000', '2695000000', '2705000000']
                    stop_fre_list = ['2690000000', '2691000000', '2695000000', '2705000000', '2715000000']
                    rbw_list = ['100000', '300000', '1000000', '1000000', '1000000']
                    vbw_list = ['300000', '900000', '3000000', '3000000', '3000000']
                    reflev_list = [high_level, low_level, low_level, low_level, low_level]
                    limit_start_list = ['60', '-10', '-10', '-13', '-25']
                    limit_stop_list = ['60', '-10', '-10', '-13', '-25']
                elif channel_str == '39750':           # band41 20M Low
                    self.setstartstopfre('2475', '2516')
                    start_fre_list = ['2475000000', '2490000000', '2495000000', '2496000000']
                    stop_fre_list = ['2490000000', '2495000000', '2496000000', '2516000000']
                    rbw_list = ['1000000', '1000000', '200000', '100000']
                    vbw_list = ['3000000', '3000000', '600000', '300000']
                    reflev_list = [low_level, low_level, low_level, high_level]
                    limit_start_list = ['-25', '-13', '-13', '60']
                    limit_stop_list = ['-25', '-13', '-13', '60']
                elif channel_str == '41490':           # band41 20M High
                    self.setstartstopfre('2670', '2715')
                    start_fre_list = ['2670000000', '2690000000', '2691000000', '2695000000', '2710000000']
                    stop_fre_list = ['2690000000', '2691000000', '2695000000', '2710000000', '2715000000']
                    rbw_list = ['100000', '500000', '1000000', '1000000', '1000000']
                    vbw_list = ['300000', '1500000', '3000000', '3000000', '3000000']
                    reflev_list = [high_level, low_level, low_level, low_level, low_level]
                    limit_start_list = ['60', '-10', '-10', '-13', '-25']
                    limit_stop_list = ['60', '-10', '-10', '-13', '-25']

                # 编辑LIST
                for i in range(1, len(start_fre_list) + 1):
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':STAR ' + start_fre_list[i - 1])
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':STOP ' + stop_fre_list[i - 1])
                    # if global_element.Test_band in ['TDD-LTE 41', 'FDD-LTE 7', 'TDD-LTE 38']:
                    #     self.instance.write('SENS:LIST:RANG' + str(i) + ':FILT:TYPE CHAN')
                    # else:
                    #     self.instance.write('SENS:LIST:RANG' + str(i) + ':FILT:TYPE NORM')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':FILT:TYPE CHAN')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':BAND:RES ' + rbw_list[i - 1])
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':BAND:VID ' + vbw_list[i - 1])
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':SWE:TIME:AUTO ON')
                    # self.instance.write('SENS:LIST:RANG' + str(i) + ':SWE:TIME 0.5')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':DET RMS')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':RLEV ' + reflev_list[i - 1])
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':INP:ATT:AUTO ON')
                    self.instance.write('LIST:RANG' + str(i) + ':POIN 1000')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':LIM:STAT ON')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':LIM:STAR ' + limit_start_list[i - 1])
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':LIM:STOP ' + limit_stop_list[i - 1])

                # Start sweept
                self.instance.write('INIT:SPUR')
                time.sleep(10)
                self.instance.write('ABOR')

                result = self.instance.query('CALC:LIM:FAIL?')
                result_final = result[:-1]
                return result_final
        except:
            global_element.emitsingle.stateupdataSingle.emit('SA Bandedge Setting Method Exception!')
            return 'NULL'

    # SA LTE CA Bandedge spurious功能设置
    def ltecafcc_bandedge_set(self, bw_group, channel_group):
        try:
            EBW = eval(bw_group[0]) + eval(bw_group[1])
            EBW_span = EBW * 1.2
            rbw = str(EBW * 1e6 / 1e2)
            vbw = str(eval(rbw) * 3)

            if self.device_name == 'FSQ' or self.device_name == 'FSU':
                self.instance.write('SWEEP:MODE LIST')
                self.instance.write('CALC1:PEAK:AUTO ON')
                range_count = self.instance.query('SENS:LIST:RANG:COUN?')
                range_count_final = range_count[:-1]
                for i in range(int(range_count_final)):
                    self.instance.write('SENS:LIST:RANG:DEL')  # 清空LIST

                low_level = '-30'
                high_level = '30'
                high_limit = '40'
                low_dect = 'RMS'
                high_dect = 'APE'

                if channel_group in [['18633', '18750'], ['18700', '18817'], ['18653', '18773'], ['18675', '18795'],
                                     ['18655', '18799'], ['18700', '18844'], ['18675', '18825'], ['18678', '18849'],
                                     ['18700', '18871'], ['18700', '18898']]:                             # CA_2C  Low
                    self.setstartstopfre('1840', str(1850 + EBW_span))
                    start_fre_list = ['1840000000', '1849000000', '1850000000']
                    stop_fre_list = ['1849000000', '1850000000', str((1850 + EBW_span) * 1e6)]
                    rbw_list = ['1000000', rbw, '100000']
                    vbw_list = ['3000000', vbw, '3000000']
                    reflev_list = [low_level, high_level, high_level]
                    limit_start_list = ['-13', '-13', high_limit]
                    limit_stop_list = ['-13', '-13', high_limit]
                    dect_list = [low_dect, low_dect, high_dect]
                elif channel_group in [['18983', '19100'], ['19050', '19167'], ['19005', '19125'], ['19027', '19147'],
                                       ['18956', '19100'], ['19001', '19145'], ['18975', '19125'], ['18929', '19100'],
                                       ['18951', '19122'], ['18902', '19100']]:                           # CA_2C High
                    self.setstartstopfre(str(1910 - EBW_span), '1920')
                    start_fre_list = [str((1910 - EBW_span) * 1e6), '1910000000', '1911000000']
                    stop_fre_list = ['1910000000', '1911000000', '1920000000']
                    rbw_list = ['100000', rbw, '1000000']
                    vbw_list = ['300000', vbw, '3000000']
                    reflev_list = [high_level, high_level, low_level]
                    limit_start_list = [high_limit, '-13', '-13']
                    limit_stop_list = [high_limit, '-13', '-13']
                    dect_list = [high_dect, low_dect, low_dect]
                elif channel_group in [['20416', '20455'], ['20425', '20464'], ['20428', '20500'], ['20450', '20522'],
                                       ['20450', '20549']]:                                  # CA_5B Low
                    self.setstartstopfre('815', str(824 + EBW_span))
                    start_fre_list = ['815000000', '823000000', '824000000']
                    stop_fre_list = ['823000000', '824000000', str((824 + EBW_span) * 1e6)]
                    rbw_list = ['100000', rbw, '100000']
                    vbw_list = ['300000', vbw, '300000']
                    reflev_list = [low_level, high_level, high_level]
                    limit_start_list = ['-13', '-13', high_limit]
                    limit_stop_list = ['-13', '-13', high_limit]
                    dect_list = [low_dect, low_dect, high_dect]
                elif channel_group in [['20586', '20625'], ['20595', '20634'],
                             ['20528', '20600'], ['20550', '20622'], ['20501', '20600']]:                 # CA_5B High
                    self.setstartstopfre(str(849 - EBW_span), '860')
                    start_fre_list = [str((849 - EBW_span) * 1e6), '849000000', '850000000']
                    stop_fre_list = ['849000000', '850000000', '860000000']
                    rbw_list = ['100000', rbw, '100000']
                    vbw_list = ['300000', vbw, '300000']
                    reflev_list = [high_level, high_level, low_level]
                    limit_start_list = [high_limit, '-13', '-13']
                    limit_stop_list = [high_limit, '-13', '-13']
                    dect_list = [high_dect, low_dect, low_dect]
                elif channel_group in [['20805', '20949'],
                             ['20850', '20994'], ['20825', '20975'], ['20828', '20999'], ['20850', '21021'],
                             ['20850', '21048']]:                                             # CA_7C Low
                    self.setstartstopfre('2436', str(2496 + EBW_span))
                    x_value = EBW if EBW - 6 > 0 else 6
                    edge_value = str((2496 - x_value) * 1e6)
                    start_fre_list = ['2436000000', edge_value, '2495000000', '2496000000']
                    stop_fre_list = [edge_value, '2495000000', '2496000000', str((2496 + EBW_span) * 1e6)]
                    rbw_list = ['1000000', '1000000', rbw, '100000']
                    vbw_list = ['3000000', '3000000', vbw, '300000']
                    reflev_list = [low_level, low_level, high_level, high_level]
                    limit_start_list = ['-25', '-13', '-13', high_limit]
                    limit_stop_list = ['-25', '-13', '-13', high_limit]
                    dect_list = [low_dect, low_dect, low_dect, high_dect]
                elif channel_group in [['21206', '21350'],
                             ['21251', '21395'], ['21225', '21375'], ['21179', '21350'], ['21201', '21372'],
                             ['21152', '21350']]:                                               # CA_7C High
                    x_value = EBW if EBW - 6 > 0 else 6
                    edge_value = str((2570 + x_value) * 1e6)
                    self.setstartstopfre(str(2570 - EBW_span), '2630')
                    start_fre_list = [str((2570 - EBW_span) * 1e6), '2570000000', '2571000000', '2575000000', edge_value]
                    stop_fre_list = ['2570000000', '2571000000', '2575000000', edge_value, '2630']
                    rbw_list = ['100000', str(2 * eval(rbw)), '1000000', '1000000', '1000000']
                    vbw_list = ['300000', str(2 * eval(rbw)), '3000000', '3000000', '3000000']
                    reflev_list = [high_level, high_level, low_level, low_level, low_level]
                    limit_start_list = [high_limit, '-10', '-10', '-13', '-25']
                    limit_stop_list = [high_limit, '-10', '-10', '-13', '-25']
                    dect_list = [high_dect, low_dect, low_dect, low_dect]
                elif channel_group in [['23035', '23083'], ['23035', '23107']]:                    # CA_12B Low
                    self.setstartstopfre('690', str(699 + EBW_span))
                    start_fre_list = ['690000000', '698000000', '699000000']
                    stop_fre_list = ['698000000', '699000000', str((699 + EBW_span) * 1e6)]
                    rbw_list = ['100000', rbw, '100000']
                    vbw_list = ['300000', vbw, '300000']
                    reflev_list = [low_level, high_level, high_level]
                    limit_start_list = ['-13', '-13', high_limit]
                    limit_stop_list = ['-13', '-13', high_limit]
                    dect_list = [low_dect, low_dect, high_dect]
                elif channel_group in [['23107', '23155'], ['23058', '23130']]:                    # CA_12B High
                    self.setstartstopfre(str(716 - EBW_span), '725')
                    start_fre_list = [str((716 - EBW_span) * 1e6), '716000000', '716100000']
                    stop_fre_list = ['716000000', '716100000', '725000000']
                    rbw_list = ['100000', rbw, '100000']
                    vbw_list = ['300000', vbw, '300000']
                    reflev_list = [high_level, high_level, low_level]
                    limit_start_list = [high_limit, '-13', '-13']
                    limit_stop_list = [high_limit, '-13', '-13']
                    dect_list = [high_dect, low_dect, low_dect]
                elif channel_group in [['39683', '39800'], ['39750', '39867'], ['39705', '39849'], ['39750', '39894'],
                                       ['39725', '39875'], ['39728', '39899'], ['39750', '39921'], ['39750', '39948']]:
                    # CA_41C Low
                    x_value = EBW if EBW - 6 > 0 else 6
                    edge_value = str((2496 - x_value) * 1e6)
                    self.setstartstopfre('2436', str(2496 + EBW_span))
                    start_fre_list = ['2436000000', edge_value, '2495000000', '2496000000']
                    stop_fre_list = [edge_value, '2495000000', '2496000000', str((2496 + EBW_span) * 1e6)]
                    rbw_list = ['1000000', '1000000', rbw, '100000']
                    vbw_list = ['3000000', '3000000', vbw, '300000']
                    reflev_list = [low_level, low_level, high_level, high_level]
                    limit_start_list = ['-25', '-13', '-13', high_limit]
                    limit_stop_list = ['-25', '-13', '-13', high_limit]
                    dect_list = [low_dect, low_dect, low_dect, high_dect]
                elif channel_group in [['41373', '41490'], ['41440', '41557'], ['41346', '41490'], ['41391', '41535'],
                                       ['41365', '41515'], ['41319', '41490'], ['41341', '41512'], ['41292', '41490']]:
                    # CA_41C High
                    x_value = EBW if EBW - 6 > 0 else 6
                    edge_value = str((2690 + x_value) * 1e6)
                    self.setstartstopfre(str(2690 - EBW_span), '2750')
                    start_fre_list = [str((2690 - EBW_span) * 1e6), '2690000000', '2691000000', '2695000000', edge_value]
                    stop_fre_list = ['2690000000', '2691000000', '2695000000', edge_value, '2750000000']
                    rbw_list = ['100000', str(2 * eval(rbw)), '1000000', '1000000', '1000000']
                    vbw_list = ['300000', str(2 * eval(rbw)), '3000000', '3000000', '3000000']
                    reflev_list = [high_level, high_level, low_level, low_level, low_level]
                    limit_start_list = [high_limit, '-10', '-10', '-13', '-25']
                    limit_stop_list = [high_limit, '-10', '-10', '-13', '-25']
                    dect_list = [high_dect, low_dect, low_dect, low_dect, low_dect]
                elif channel_group in [['37825', '37975'], ['37850', '38048']]:
                    # CA_38C Low
                    x_value = EBW if EBW - 6 > 0 else 6
                    edge_value = str((2570 - x_value) * 1e6)
                    self.setstartstopfre('2510', str(2570 + EBW_span))
                    start_fre_list = ['2510000000', edge_value, '2569000000', '2570000000']
                    stop_fre_list = [edge_value, '2569000000', '2570000000', str((2570 + EBW_span) * 1e6)]
                    rbw_list = ['1000000', '1000000', rbw, '100000']
                    vbw_list = ['3000000', '3000000', vbw, '300000']
                    reflev_list = [low_level, low_level, high_level, high_level]
                    limit_start_list = ['-25', '-13', '-13', high_limit]
                    limit_stop_list = ['-25', '-13', '-13', high_limit]
                    dect_list = [low_dect, low_dect, low_dect, high_dect]
                elif channel_group in [['38025', '38175'], ['37952', '38150']]:
                    # CA_38C High
                    x_value = EBW if EBW - 6 > 0 else 6
                    edge_value = str((2620 + x_value) * 1e6)
                    self.setstartstopfre(str(2620 - EBW_span), '2680')
                    start_fre_list = [str((2620 - EBW_span) * 1e6), '2620000000', '2621000000', '2625000000', edge_value]
                    stop_fre_list = ['2620000000', '2621000000', '2625000000', edge_value, '2680000000']
                    rbw_list = ['100000', str(2 * eval(rbw)), '1000000', '1000000', '1000000']
                    vbw_list = ['300000', str(2 * eval(rbw)), '3000000', '3000000', '3000000']
                    reflev_list = [high_level, high_level, low_level, low_level, low_level]
                    limit_start_list = [high_limit, '-10', '-10', '-13', '-25']
                    limit_stop_list = [high_limit, '-10', '-10', '-13', '-25']
                    dect_list = [high_dect, low_dect, low_dect, low_dect, low_dect]

                # 编辑LIST
                for i in range(1, len(start_fre_list) + 1):
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':STAR ' + start_fre_list[i - 1])
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':STOP ' + stop_fre_list[i - 1])
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':FILT:TYPE CHAN')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':BAND:RES ' + rbw_list[i - 1])
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':BAND:VID ' + vbw_list[i - 1])
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':SWE:TIME:AUTO ON')
                    # self.instance.write('SENS:LIST:RANG' + str(i) + ':SWE:TIME 0.5')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':DET ' + dect_list[i - 1])
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':RLEV ' + reflev_list[i - 1])
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':INP:ATT:AUTO ON')
                    self.instance.write('LIST:RANG' + str(i) + ':POIN 1000')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':LIM:STAT ON')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':LIM:STAR ' + limit_start_list[i - 1])
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':LIM:STOP ' + limit_stop_list[i - 1])

                # Start sweept
                self.instance.write('INIT:SPUR')
                time.sleep(15)
                self.instance.write('ABOR')

                result = self.instance.query('CALC:LIM:FAIL?')
                result_final = result[:-1]
                return result_final
        except:
            global_element.emitsingle.stateupdataSingle.emit('SA LTE CA Bandedge Setting Method Exception!')
            return 'NULL'

    # SA LTEFCC CSE设置
    def ltefcc_cse_set(self, band_str):
        try:
            if self.device_name == 'FSQ' or self.device_name == 'FSU':
                self.instance.write('SWEEP:MODE LIST')
                self.instance.write('CALC1:PEAK:AUTO ON')
                range_count = self.instance.query('SENS:LIST:RANG:COUN?')
                range_count_final = range_count[:-1]
                for i in range(int(range_count_final)):
                    self.instance.write('SENS:LIST:RANG:DEL')  # 清空LIST

                if band_str == 'FDD-LTE 2':
                    self.setstartstopfre('30', '19500')
                    start_fre_list = ['30', '1000000000', '1920000000', '3000000000', '9000000000', '13000000000']
                    stop_fre_list = ['1000000000', '1840000000', '3000000000', '9000000000', '13000000000',
                                     '19500000000']
                    rbw_list = ['100000', '1000000', '1000000', '1000000', '1000000', '1000000']
                elif band_str == 'FDD-LTE 4':
                    self.setstartstopfre('30', '18000')
                    start_fre_list = ['30', '1000000000', '1765000000', '3000000000', '9000000000', '13000000000']
                    stop_fre_list = ['1000000000', '1700000000', '3000000000', '9000000000', '13000000000',
                                     '18000000000']
                    rbw_list = ['100000', '1000000', '1000000', '1000000', '1000000', '1000000']
                elif band_str == 'FDD-LTE 5':
                    self.setstartstopfre('30', '9000')
                    start_fre_list = ['30', '860000000', '1000000000', '3000000000', '7000000000']
                    stop_fre_list = ['815000000', '1000000000', '3000000000', '7000000000', '9000000000']
                    rbw_list = ['100000', '100000', '1000000', '1000000', '1000000']
                elif band_str == 'FDD-LTE 7':
                    self.setstartstopfre('30', '26000')
                    start_fre_list = ['30', '1000000000', '2580000000', '5000000000', '10000000000', '18000000000']
                    stop_fre_list = ['1000000000', '2490000000', '5000000000', '10000000000', '18000000000',
                                     '26000000000']
                    rbw_list = ['100000', '1000000', '1000000', '1000000', '1000000', '1000000']
                elif band_str == 'FDD-LTE 12':
                    self.setstartstopfre('30', '9000')
                    start_fre_list = ['30', '725000000', '1000000000', '3000000000', '7000000000']
                    stop_fre_list = ['690000000', '1000000000', '3000000000', '7000000000', '9000000000']
                    rbw_list = ['100000', '100000', '1000000', '1000000', '1000000']
                elif band_str == 'FDD-LTE 17':
                    self.setstartstopfre('30', '9000')
                    start_fre_list = ['30', '725000000', '1000000000', '3000000000', '7000000000']
                    stop_fre_list = ['690000000', '1000000000', '3000000000', '7000000000', '9000000000']
                    rbw_list = ['100000', '100000', '1000000', '1000000', '1000000']
                elif band_str == 'FDD-LTE 25':
                    self.setstartstopfre('30', '19500')
                    start_fre_list = ['30', '1000000000', '1920000000', '3000000000', '9000000000', '13000000000']
                    stop_fre_list = ['1000000000', '1840000000', '3000000000', '9000000000', '13000000000',
                                     '19500000000']
                    rbw_list = ['100000', '1000000', '1000000', '1000000', '1000000', '1000000']
                elif band_str == 'FDD-LTE 26':
                    self.setstartstopfre('30', '9000')
                    start_fre_list = ['30', '860000000', '1000000000', '3000000000', '7000000000']
                    stop_fre_list = ['815000000', '1000000000', '3000000000', '7000000000', '9000000000']
                    rbw_list = ['100000', '100000', '1000000', '1000000', '1000000']
                elif band_str in ['TDD-LTE 41', 'TDD-LTE 38']:
                    self.setstartstopfre('30', '26000')
                    start_fre_list = ['30', '1000000000', '2715000000', '3000000000', '7000000000', '10000000000',
                                      '14000000000', '18000000000']
                    stop_fre_list = ['1000000000', '2475000000', '3000000000', '7000000000', '10000000000',
                                     '14000000000', '18000000000', '26000000000']
                    rbw_list = ['100000', '1000000', '1000000', '1000000', '1000000', '1000000', '1000000', '1000000']

                # 编辑LIST
                for i in range(1, len(start_fre_list) + 1):
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':STAR ' + start_fre_list[i - 1])
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':STOP ' + stop_fre_list[i - 1])
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':FILT:TYPE NORM')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':BAND:RES ' + rbw_list[i - 1])
                    vbw_str = str(eval(rbw_list[i - 1]) * 3)
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':BAND:VID ' + vbw_str)
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':SWE:TIME:AUTO ON')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':DET POS')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':RLEV 0')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':INP:ATT:AUTO ON')
                    self.instance.write('LIST:RANG' + str(i) + ':POIN 10000')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':LIM:STAT ON')
                    if global_element.Test_band in ['FDD-LTE 7', 'TDD-LTE 38', 'TDD-LTE 41']:
                        self.instance.write('SENS:LIST:RANG' + str(i) + ':LIM:STAR -25')
                        self.instance.write('SENS:LIST:RANG' + str(i) + ':LIM:STOP -25')
                    else:
                        self.instance.write('SENS:LIST:RANG' + str(i) + ':LIM:STAR -13')
                        self.instance.write('SENS:LIST:RANG' + str(i) + ':LIM:STOP -13')

                # Start sweept
                self.instance.write('INIT:SPUR')
                time.sleep(10)
                self.instance.write('ABOR')

                time.sleep(3)

                result = self.instance.query('CALC:LIM:FAIL?')
                result_final = result[:-1]
                return result_final

        except:
            global_element.emitsingle.stateupdataSingle.emit('CSE spectrum settings failed!')
            return 'NULL'

    # SA LTECA FCC CSE设置
    def ltecafcc_cse_set(self, band_str):
        try:
            if self.device_name == 'FSQ' or self.device_name == 'FSU':
                self.instance.write('SWEEP:MODE LIST')
                self.instance.write('CALC1:PEAK:AUTO ON')
                range_count = self.instance.query('SENS:LIST:RANG:COUN?')
                range_count_final = range_count[:-1]
                for i in range(int(range_count_final)):
                    self.instance.write('SENS:LIST:RANG:DEL')  # 清空LIST

                if band_str == 'CA_2C':
                    self.setstartstopfre('30', '19500')
                    start_fre_list = ['30', '1000000000', '1920000000', '3000000000', '9000000000', '13000000000']
                    stop_fre_list = ['1000000000', '1840000000', '3000000000', '9000000000', '13000000000',
                                     '19500000000']
                    rbw_list = ['100000', '1000000', '1000000', '1000000', '1000000', '1000000']
                elif band_str == 'CA_5B':
                    self.setstartstopfre('30', '9000')
                    start_fre_list = ['30', '860000000', '1000000000', '3000000000', '7000000000']
                    stop_fre_list = ['815000000', '1000000000', '3000000000', '7000000000', '9000000000']
                    rbw_list = ['100000', '100000', '1000000', '1000000', '1000000']
                elif band_str == 'CA_7C':
                    self.setstartstopfre('30', '26000')
                    start_fre_list = ['30', '1000000000', '2580000000', '5000000000', '10000000000', '18000000000']
                    stop_fre_list = ['1000000000', '2490000000', '5000000000', '10000000000', '18000000000',
                                     '26000000000']
                    rbw_list = ['100000', '1000000', '1000000', '1000000', '1000000', '1000000']
                elif band_str == 'CA_12B':
                    self.setstartstopfre('30', '9000')
                    start_fre_list = ['30', '725000000', '1000000000', '3000000000', '7000000000']
                    stop_fre_list = ['690000000', '1000000000', '3000000000', '7000000000', '9000000000']
                    rbw_list = ['100000', '100000', '1000000', '1000000', '1000000']
                elif band_str in ['CA_41C', 'CA_38C']:
                    self.setstartstopfre('30', '26000')
                    start_fre_list = ['30', '1000000000', '2715000000', '3000000000', '7000000000', '10000000000',
                                      '14000000000', '18000000000']
                    stop_fre_list = ['1000000000', '2475000000', '3000000000', '7000000000', '10000000000',
                                     '14000000000', '18000000000', '26000000000']
                    rbw_list = ['100000', '1000000', '1000000', '1000000', '1000000', '1000000', '1000000',
                                '1000000']

                # 编辑LIST
                for i in range(1, len(start_fre_list) + 1):
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':STAR ' + start_fre_list[i - 1])
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':STOP ' + stop_fre_list[i - 1])
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':FILT:TYPE NORM')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':BAND:RES ' + rbw_list[i - 1])
                    vbw_str = str(eval(rbw_list[i - 1]) * 3)
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':BAND:VID ' + vbw_str)
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':SWE:TIME:AUTO ON')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':DET POS')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':RLEV 0')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':INP:ATT:AUTO ON')
                    self.instance.write('LIST:RANG' + str(i) + ':POIN 10000')
                    self.instance.write('SENS:LIST:RANG' + str(i) + ':LIM:STAT ON')
                    if global_element.Test_band in ['CA_7C', 'CA_38C', 'CA_41C']:
                        self.instance.write('SENS:LIST:RANG' + str(i) + ':LIM:STAR -25')
                        self.instance.write('SENS:LIST:RANG' + str(i) + ':LIM:STOP -25')
                    else:
                        self.instance.write('SENS:LIST:RANG' + str(i) + ':LIM:STAR -13')
                        self.instance.write('SENS:LIST:RANG' + str(i) + ':LIM:STOP -13')

                # Start sweept
                self.instance.write('INIT:SPUR')
                time.sleep(10)
                self.instance.write('ABOR')

                time.sleep(3)

                result = self.instance.query('CALC:LIM:FAIL?')
                result_final = result[:-1]
                return result_final

        except:
            global_element.emitsingle.stateupdataSingle.emit('CSE spectrum settings failed!')
            return 'NULL'

    # 检测DUT是否有发出对应的BT信号
    def check_bt_signal(self):
        result = True
        if self.device_name == 'FSQ' or self.device_name == 'FSU' or self.device_name == 'E4440A':
            global_element.emitsingle.stateupdataSingle.emit('SA check the signal……')
            ULfre = report_handle.fre_bt2_calc(int(global_element.Test_channel))
            self.instance.query('FREQ:CENT ' + ULfre + 'MHz; *OPC?')
            self.set_loss(ULfre)
            self.instance.query('DISP:WIND:TRAC:Y:RLEV 30dBm; *OPC?')
            self.instance.query('FREQ:SPAN 1GHz; *OPC?')
            self.instance.query('DISP:WIND:TRAC:MODE MAXH; *OPC?')
            self.instance.query('INIT:CONT ON; *OPC?')
            time.sleep(2)
            self.instance.query('INIT:CONT OFF; *OPC?')
            self.instance.query('CALC:MARK1:MAX; *OPC?')
            marker1_amp = self.instance.query('CALC:MARK1:Y?')
            if eval(marker1_amp) < -5:
                global_element.emitsingle.stateupdataSingle.emit('SA did not check the signal!')
                result = False
                time.sleep(1)
            return result

    def peakmarkercnt(self, traceindex):
        try:
            if self.device_name in ['FSQ', 'FSU', 'E4440A']:
                markamp1 = self.instance.query("CALCulate:MARKer" + traceindex + ":X?")
                markamp1_result = format(eval(markamp1) / 1000000, '.2f')
                self.instance.write("CALC:MARK" + traceindex + ":MAX:LEFT")
                markamp2 = self.instance.query("CALCulate:MARKer" + traceindex + ":X?")
                markamp2_result = format(eval(markamp2) / 1000000, '.2f')

                while markamp1_result != markamp2_result:
                    markamp1 = self.instance.query("CALCulate:MARKer" + traceindex + ":X?")
                    markamp1_result = format(eval(markamp1) / 1000000, '.2f')
                    self.instance.write("CALC:MARK" + traceindex + ":MAX:LEFT")
                    markamp2 = self.instance.query("CALCulate:MARKer" + traceindex + ":X?")
                    markamp2_result = format(eval(markamp2) / 1000000, '.2f')

                count_peak = 0
                markamp1 = self.instance.query("CALCulate:MARKer" + traceindex + ":X?")
                markamp1_result = format(eval(markamp1) / 1000000, '.2f')
                self.instance.write("CALC:MARK" + traceindex + ":MAX:RIGH")
                markamp2 = self.instance.query("CALCulate:MARKer" + traceindex + ":X?")
                markamp2_result = format(eval(markamp2) / 1000000, '.2f')
                while markamp1_result != markamp2_result:
                    markamp1 = self.instance.query("CALCulate:MARKer" + traceindex + ":X?")
                    markamp1_result = format(eval(markamp1) / 1000000, '.2f')
                    self.instance.write("CALC:MARK" + traceindex + ":MAX:RIGH")
                    markamp2 = self.instance.query("CALCulate:MARKer" + traceindex + ":X?")
                    markamp2_result = format(eval(markamp2) / 1000000, '.2f')
                    count_peak += 1

                return str(count_peak)
        except:
            global_element.emitsingle.thread_exitSingle.emit('SA peakmarkercnt method exception!')

    def reflev_pos(self, pos):
        if self.device_name == 'FSQ' or self.device_name == 'FSU':
            self.instance.write('DISP:WIND:TRAC:Y:RPOS ' + pos + 'PCT')

    def serchlimit(self, lowfreq, highfreq):
        try:
            if self.device_name == 'FSQ' or self.device_name == 'FSU':
                self.instance.write('CALC:MARK:X:SLIM ON')
                self.instance.write("CALC:MARK:X:SLIM:LEFT " + lowfreq + "MHZ")
                self.instance.write("CALC:MARK:X:SLIM:RIGH " + highfreq + "MHZ")
        except:
            global_element.emitsingle.stateupdataSingle.emit('Error:    SA set search limit error!')

    def serchlimit_off(self):
        try:
            if self.device_name == 'FSQ' or self.device_name == 'FSU':
                self.instance.write('CALC:MARK:X:SLIM OFF')
        except:
            global_element.emitsingle.stateupdataSingle.emit('Error:    SA set search limit off error!')

    def trig_ifp_set(self):
        try:
            if self.device_name == 'FSQ' or self.device_name == 'FSU':
                self.instance.write('TRIG:SOUR IFP')
        except:
            global_element.emitsingle.stateupdataSingle.emit('Error:    SA set TRIG IF POWER error!')

    def MoveMarker(self, markerindex, markerposition):
        try:
            if self.device_name == 'FSQ' or self.device_name == 'FSU':
                self.instance.write("CALCulate:MARKer" + str(markerindex) + ":X " + str(markerposition))
        except:
            global_element.emitsingle.stateupdataSingle.emit('Error:    SA Setting Move Marker Error!')

    def MarkerDLT(self):
        try:
            if self.device_name == 'FSQ' or self.device_name == 'FSU':
                DLTResult = self.instance.query("CALC1:DELT2:X:REL?")
                return DLTResult
        except:
            global_element.emitsingle.stateupdataSingle.emit('Error:    SA set Marker DELTA error!')

    def Linedisplay(self, linevalue):
        try:
            if self.device_name == 'FSQ' or self.device_name == 'FSU':
                self.instance.write("CALC:DLIN1 " + linevalue + "dBm")
                self.instance.write('CALC:DLIN1:STAT ON')
        except:
            global_element.emitsingle.stateupdataSingle.emit('Error:    SA set Line display error!')

    def set_sweep_points(self, sweeppoints):
        try:
            if self.device_name == 'FSQ' or self.device_name == 'FSU':
                self.instance.write("SWE:POIN " + sweeppoints)

        except Exception as e:
            global_element.emitsingle.stateupdataSingle.emit('Error:    SA set sweep points error!(' + str(e) + ')')

    def next_peak(self, markerindex):
        try:
            if self.device_name == 'FSQ' or self.device_name == 'FSU':
                self.instance.write("CALC:MARK" + markerindex + ":MAX:NEXT")

        except Exception as e:
            global_element.emitsingle.stateupdataSingle.emit('Error:    SA set next peak error!(' + str(e) + ')')



