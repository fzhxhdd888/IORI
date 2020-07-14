# !/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Author    : Feng Zhaohui
# @Time      : 2019/2/22
# @File      : CU.py
# @Funcyusa  :
# @Version   : 1.0

import visa
import global_element
from testseq_handle import channelstrtolist
import time
import DUTcontrol


class VisaCU(object):
    """
        综测仪类构建
        定义综测仪的类函数和参数
    """
    def __init__(self, device_name, visa_address, visa_address_type,  visaDLL=None, *args):
        self.device_address = visa_address
        self.device_name = device_name
        self.device_address_type = visa_address_type
        self.visaDLL = 'visa32.dll' if visaDLL is None else visaDLL
        if self.device_address_type == 'GPIB':
            if self.device_name == 'CMW500':
                self.address = "GPIB0::%s::INSTR" % self.device_address
            if self.device_name == 'CMU200':
                self.address = "GPIB0::%s::0::INSTR" % self.device_address
        elif self.device_address_type == 'TCPIP':
            self.address = "TCPIP::%s::inst0::INSTR" % self.device_address
        self.resourceManager = visa.ResourceManager(self.visaDLL)

    def open(self):
        self.instance = self.resourceManager.open_resource(self.address)

    def close(self):
        if self.instance is not None:
            self.instance.close()
            self.instance = None

    def read_idn(self):
        idn = self.instance.query("*IDN?")
        return idn

    # 检查综测试仪是否有GSM 信令选件
    def check_gsmsin_option(self):
        if self.device_name == 'CMW500':
            gsm_option = self.instance.query('SYST:OPT:VERS? "CMW_GSM_Sig"')
        elif self.device_name == 'CMU200':
            option_str = self.instance.query('0;*OPT?')
            option_str_list = option_str.split(',')
            if 'K21' in option_str_list:        # 目前以检测是否有GSM900 Sig的信令为参考
                gsm_option = '1'
        else:
            gsm_option = '0'
        if gsm_option == '0':
            global_element.emitsingle.thread_exitSingle.emit('Error:    CU does not support GSM signaling mode!')

    # 检查综测试仪是否有WCDMA 信令选件
    def check_wcdmasin_option(self):
        if self.device_name == 'CMW500':
            wcdma_option = self.instance.query('SYST:OPT:VERS? "CMW_WCDMA_Sig"')
        elif self.device_name == 'CMU200':
            option_str = self.instance.query('0;*OPT?')
            option_str_list = option_str.split(',')
            if 'K68' in option_str_list:   # 目前以检测是否有Band I的信令为参考
                wcdma_option = '1'
        else:
            wcdma_option = '0'
        if wcdma_option == '0':
            global_element.emitsingle.thread_exitSingle.emit('Error:    The CU does not support WCDMA signaling mode!')

    # 检查综测试仪是否有LTE 信令选件
    def check_ltesin_option(self):
        if self.device_name == 'CMW500':
            wcdma_option = self.instance.query('SYST:OPT:VERS? "CMW_LTE_Sig"')
        else:
            wcdma_option = '0'
        if wcdma_option == '0':
            result = False
        else:
            result = True
        return result

    # 检查综测试仪是否有wlan 信令选件
    def check_wlansin_option(self):
        if self.device_name == 'CMW500':
            wcdma_option = self.instance.query('SYST:OPT:VERS? "CMW_WLAN_Sig"')
        else:
            wcdma_option = '0'
        if wcdma_option == '0':
            result = False
        else:
            result = True
        return result

    # 检查综测试仪是否有BT 信令选件
    def check_btsin_option(self):
        if self.device_name == 'CMW500':
            wcdma_option = self.instance.query('SYST:OPT:VERS? "CMW_BLUETOOTH_Sig"')
        else:
            wcdma_option = '0'
        if wcdma_option == '0':
            result = False
        else:
            result = True
        return result

    # 综测仪GSM模块初始化设置
    def gsmsin_init_setting(self):
        try:
            global_element.emitsingle.stateupdataSingle.emit('Initializing the GSM parameters of the CU……')
            if self.device_name == 'CMW500':
                self.instance.write('SYST:RES:ALL')
                time.sleep(3)
                self.instance.query('*OPC?')

                sys_state = self.instance.query('syst:err?')
                sys_state_int = sys_state.split(',')[0]
                while sys_state_int != '0':
                    time.sleep(1)
                    sys_state = self.instance.query('syst:err?')
                    sys_state_int = sys_state.split(',')[0]

                self.instance.write('ROUT:GSM:MEAS:SCEN:CSP \'GSM Sig1\'')
                time.sleep(0.1)
                # self.instance.query('CONF:BASE:FDC:RCL; *OPC?')
                # time.sleep(0.1)
                self.instance.query('CONF:GSM:SIGN:CELL:SEC:AUTH OFF; *OPC?')        # 关闭鉴权
                time.sleep(0.1)
                self.instance.query('CONF:GSM:SIGN:CELL:BSP 2; *OPC?')
                time.sleep(0.1)
                self.instance.query('CONF:GSM:SIGN:CELL:BSAG 0; *OPC?')
                time.sleep(0.1)
                self.instance.query('CONF:GSM:SIGN:CELL:PLUP 0; *OPC?')
                time.sleep(0.1)
                self.instance.query('CONF:GSM:SIGN:CELL:BSAG 0; *OPC?')
                time.sleep(0.1)
                self.instance.query('CONF:GSM:SIGN:CELL:DTX OFF; *OPC?')
                time.sleep(0.1)
                self.instance.query('ROUT:GSM:SIGN:SCEN:SCELl RF1C,RX1,RF1C,TX1; *OPC?')
                time.sleep(0.1)
                self.instance.query('CONF:GSM:SIGN:CELL:IME ON; *OPC?')
                time.sleep(0.1)
                if global_element.Test_band == 'GSM850':
                    self.instance.query('CONF:GSM:SIGN:BAND G085; *OPC?')
                    time.sleep(0.1)
                    self.instance.query('CONF:GSM:SIGN:RFS:CHAN:TCH 192; *OPC?')
                    time.sleep(0.1)
                    self.instance.query('CONF:GSM:SIGN:RFS:CHAN:BCCH 162; *OPC?')
                    time.sleep(0.1)
                elif global_element.Test_band == 'GSM900':
                    self.instance.query('CONF:GSM:SIGN:BAND G09; *OPC?')
                    time.sleep(0.1)
                    self.instance.query('CONF:GSM:SIGN:RFS:CHAN:TCH 62; *OPC?')
                    time.sleep(0.1)
                    self.instance.query('CONF:GSM:SIGN:RFS:CHAN:BCCH 92; *OPC?')
                    time.sleep(0.1)
                elif global_element.Test_band == 'DCS1800':
                    self.instance.query('CONF:GSM:SIGN:BAND G18; *OPC?')
                    time.sleep(0.1)
                    self.instance.query('CONF:GSM:SIGN:RFS:CHAN:TCH 700; *OPC?')
                    time.sleep(0.1)
                    self.instance.query('CONF:GSM:SIGN:RFS:CHAN:BCCH 670; *OPC?')
                    time.sleep(0.1)
                elif global_element.Test_band == 'PCS1900':
                    self.instance.query('CONF:GSM:SIGN:BAND G19; *OPC?')
                    time.sleep(0.1)
                    self.instance.query('CONF:GSM:SIGN:RFS:CHAN:TCH 661; *OPC?')
                    time.sleep(0.1)
                    self.instance.query('CONF:GSM:SIGN:RFS:CHAN:BCCH 631; *OPC?')
                    time.sleep(0.1)
                self.instance.query('CONF:GSM:SIGN:CELL:MNC:DIG TWO; *OPC?')
                time.sleep(0.1)
                self.instance.query('CONF:GSM:SIGN:CELL:MCC 1; MNC 1; LAC 1; *OPC?')
                time.sleep(0.1)
                self.instance.query('CONF:GSM:SIGN:RFS:LEV:TCH:CSW ' + global_element.Test_bslevel + '; *OPC?')
                time.sleep(0.1)
                self.instance.query('CONF:GSM:SIGN:RFS:PCL:TCH:CSW 10; *OPC?')
                time.sleep(0.1)
                self.instance.query('CONF:GSM:SIGN:CONNection:CSWitched:DSOurce ECHO; *OPC?')
                time.sleep(0.1)
                self.instance.query('CONF:GSM:SIGN:CONN:CSW:TMOD FV1; *OPC?')
                time.sleep(0.1)
                self.instance.query('CONF:GSM:SIGN:RFS:PMAX:BCCH 0; *OPC?')
                time.sleep(0.1)
                self.instance.query('CONF:GSM:SIGN:CELL:PSD ON; *OPC?')
                time.sleep(0.1)
                self.instance.query('CONF:GSM:SIGN:CELL:PSW:PDPC ACC; *OPC?')
                time.sleep(0.1)
                # self.instance.query('CONF:GSM:SIGN:ETOE OFF; *OPC?')
                # time.sleep(0.1)

                cu_dut_loss = global_element.CU_DUT_loss['Loss']['loss'][0]['Value']  # 取第一个loss值作为初始loss
                self.instance.write('CONF:GSM:SIGN:RFS:EATT:OUTP ' + cu_dut_loss)
                self.instance.write('CONF:GSM:SIGN:RFS:EATT:INP ' + cu_dut_loss)

                self.instance.write('SOUR:GSM:SIGN:CELL:STAT ON')
                time.sleep(3)
                # self.instance.query('*OPC?')

                sys_state = self.instance.query('syst:err?')
                sys_state_int = sys_state.split(',')[0]
                while sys_state_int != '0':
                    time.sleep(1)
                    sys_state = self.instance.query('syst:err?')
                    sys_state_int = sys_state.split(',')[0]

                # 检查GSM蜂窝是否打开，一直到打开为止
                isok = False
                while not isok:
                    time.sleep(0.5)
                    status = self.instance.query('SOUR:GSM:SIGN:CELL:STAT:ALL?')
                    onok = status.split(',')[1]
                    if onok == 'ADJ\n':
                        isok = True

            if self.device_name == 'CMU200':
                time.sleep(0.1)
                self.instance.write('0;SYST:RES:ALL')
                time.sleep(10)
                if global_element.Test_band == 'GSM850':
                    self.instance.write('0;SYST:REM:ADDR:SEC 1,"GSM850MS_Sig"')
                elif global_element.Test_band == 'GSM900':
                    self.instance.write('0;SYST:REM:ADDR:SEC 1,"GSM900MS_Sig"')
                elif global_element.Test_band == 'DCS1800':
                    self.instance.write('0;SYST:REM:ADDR:SEC 1,"GSM1800MS_Sig"')
                elif global_element.Test_band == 'PCS1900':
                    self.instance.write('0;SYST:REM:ADDR:SEC 1,"GSM1900MS_Sig"')

                cu_dut_loss = global_element.CU_DUT_loss['Loss']['loss'][0]['Value']  # 取第一个loss值作为初始loss
                self.instance.write('1;SENS:CORR:LOSS:INP2 ' + cu_dut_loss)
                self.instance.write('1;SENS:CORR:LOSS:OUTP2 ' + cu_dut_loss)
                self.instance.write('1;PROC:SIGN:ACT SON')
                time.sleep(10)
                # self.instance.query('1;*RST;*OPC?')
                self.instance.query('1;*CLS;*OPC?')
                time.sleep(2)
                self.instance.query('0;*ESR?')
                time.sleep(0.1)
                self.instance.write('0;CONF:SYNC:FREQ:REF 1.000000E+007')
                time.sleep(0.1)
                self.instance.write('0;CONF:SYNC:FREQ:REF:MODE INT')
                time.sleep(0.1)
                self.instance.query('1;PROC:SIGN:ACT SOFF;*OPC?')
                time.sleep(0.1)
                self.instance.write('1;CONF:NETW:IDEN:MNC:DIG TWO')
                time.sleep(0.1)
                self.instance.write('1;CONF:NETW:SMOD:IMSI:MCC 001')
                time.sleep(0.1)
                self.instance.write('1;CONF:NETW:SMOD:IMSI:MNC 01')
                time.sleep(0.1)
                self.instance.write('1;CONF:NETW:SMOD:IMSI:MSIN "2345678901"')
                time.sleep(0.1)
                self.instance.write('0;SYST:GTRM:COMP OFF')
                time.sleep(0.1)
                status_CSW = self.instance.query('1;SIGN:CSW:STAT?')
                time.sleep(0.1)
                self.instance.write('1;CONF:NETW:NSUP GSM')
                time.sleep(0.1)
                self.instance.write('1;CONF:MSS:CCH:PMAX 0')
                time.sleep(0.1)
                self.instance.write('1;CONF:NETW:SMOD:TRAF FRV1')
                time.sleep(0.1)

                if global_element.Test_band == 'GSM850':
                    self.instance.write('1;CONF:MSS:MS:PCL 5')
                    self.instance.write('1;CONF:BSS:CHAN 128')
                    self.instance.write('1;CONF:BSS:CCH:CHAN 128')
                elif global_element.Test_band == 'GSM900':
                    self.instance.write('1;CONF:MSS:MS:PCL 5')
                    self.instance.write('1;CONF:BSS:CHAN 975')
                    self.instance.write('1;CONF:BSS:CCH:CHAN 975')
                elif global_element.Test_band == 'DCS1800':
                    self.instance.write('1;CONF:MSS:MS:PCL 0')
                    self.instance.write('1;CONF:BSS:CHAN 512')
                    self.instance.write('1;CONF:BSS:CCH:CHAN 512')
                elif global_element.Test_band == 'DCS1900':
                    self.instance.write('1;CONF:MSS:MS:PCL 0')
                    self.instance.write('1;CONF:BSS:CHAN 512')
                    self.instance.write('1;CONF:BSS:CCH:CHAN 512')

                self.instance.write('1;CONF:BSS:MSL:RLEV -75.000000')
                self.instance.write('1;CONF:BSS:LEV:UTIM -75.000000')
                self.instance.write('1;CONF:BSS:CCH:LEV:ABS -85.000000')
                self.instance.write('1;INP:STAT RF2')
                self.instance.write('1;OUTP:STAT RF2')
                self.instance.write('1;CONF:BSS:MSL:MTIM 3')
                self.instance.query('1;SIGN:CSW:STAT?')
                self.instance.write('1;CONF:NETW:IDEN:LAC 1')
                self.instance.query('1;SIGN:CSW:STAT?')
                self.instance.query('1;PROC:SIGN:ACT SON;*OPC?')
                time.sleep(2)

            return True

        except:
            global_element.emitsingle.stateupdataSingle.emit('Error:    Error in initializing GSM parameters of CU!')
            return False

    # 在规定时间内检查DUT是否已经连接CU
    def check_dut_issync(self):
        try:
            global_element.emitsingle.stateupdataSingle.emit('Waiting for DUT registration synchronization……')
            issync = False

            for i in range(3):
                if not issync:
                    # 如果没注册上，重启DUT
                    DUTcontrol.dutoffon()

                    # 从用户配置获取注册的等待时间
                    maxtime = int(global_element.active_dut_dict['xml']['DUTCONFIG']['MAXREGTIME'])
                    for wait_time in range(maxtime, 0, -1):
                        # 停止功能函数接口
                        # 查询是否注册
                        if self.device_name == 'CMW500':
                            checkresult = self.instance.query('FETC:GSM:SIGN:CELL:CSW:STAT?')
                            time.sleep(0.5)
                        if self.device_name == 'CMU200':
                            checkresult = self.instance.query('1;SIGN:CSW:STAT?')
                            time.sleep(0.5)

                        if checkresult == 'SYNC\n':
                            global_element.emitsingle.stateupdataSingle.emit('DUT has been registered successfully!')
                            time.sleep(0.5)
                            issync = True
                            time.sleep(2)
                            break

                        global_element.emitsingle.stateupdataSingle.emit('Waiting for DUT registration '
                                                                         'synchronization……，The waiting time is %d '
                                                                         'seconds left. ' % wait_time)
                        time.sleep(0.5)
                else:
                    break

            return issync
        except:
            global_element.emitsingle.thread_exitSingle.emit('Error:     The CU checks whether the registration method '
                                                             'is wrong!')

    # 在规定时间内检查DUT是否已经连接CU
    def check_dut_issync_wcdma(self):
        try:
            global_element.emitsingle.stateupdataSingle.emit('Waiting for DUT registration synchronization……')
            issync = False

            for i in range(3):
                if not issync:
                    # 如果没注册上，重启DUT
                    DUTcontrol.dutoffon()

                    # 从用户配置获取注册的等待时间
                    maxtime = int(global_element.active_dut_dict['xml']['DUTCONFIG']['MAXREGTIME'])
                    for wait_time in range(maxtime, 0, -1):
                        # 停止功能函数接口
                        # 查询是否注册
                        if self.device_name == 'CMW500':
                            checkresult = self.instance.query('FETC:WCDM:SIGN:CSW:STAT?')
                            time.sleep(0.5)

                            if checkresult == 'REG\n' or checkresult == 'CEST\n':
                                global_element.emitsingle.stateupdataSingle.emit('DUT has been registered successfully!')
                                time.sleep(0.5)
                                issync = True
                                break

                        if self.device_name == 'CMU200':
                            state_psw = self.instance.query('5;SIGN:PSW:STAT?')
                            state = self.instance.query('5;SIGN:STAT?')
                            time.sleep(0.5)

                            if state_psw == 'ATT\n' and state == 'REG\n':
                                global_element.emitsingle.stateupdataSingle.emit('DUT has been registered successfully!')
                                time.sleep(0.5)
                                issync = True
                                break

                            if state == 'CEST\n':
                                global_element.emitsingle.stateupdataSingle.emit('DUT has been registered successfully!')
                                time.sleep(0.5)
                                issync = True
                                break

                        global_element.emitsingle.stateupdataSingle.emit('Waiting for DUT registration '
                                                                         'synchronization……，The waiting time is %d '
                                                                         'seconds left.' % wait_time)
                        time.sleep(0.5)
                else:
                    break

            return issync
        except:
            global_element.emitsingle.thread_exitSingle.emit('Error:     The CU checks whether the registration method '
                                                             'is wrong!')

    # 建立GSM call
    def callsetup(self):
        try:
            global_element.emitsingle.stateupdataSingle.emit('DUT Connection……')
            isconnected = False
            if self.device_name == 'CMW500':
                self.instance.write('CALL:GSM:SIGN:CSW:ACT CONN')
                for i in range(3):
                    state = self.instance.query('FETC:GSM:SIGN:CELL:CSW:STAT?')
                    if state == 'CEST\n':
                        global_element.emitsingle.stateupdataSingle.emit('DUT Connection Successful!')
                        isconnected = True
                        break
                    elif state == 'SYNC\n':
                        self.instance.write('CALL:GSM:SIGN:CSW:ACT CONN')
                    elif state == 'ALER\n':
                        global_element.emitsingle.stateupdataSingle.emit('The bell is ringing. Please answer it at DUT.')
                    time.sleep(5)
            if self.device_name == 'CMU200':
                self.instance.write('1;PROC:SIGN:ACT MTC')
                time.sleep(2)
                for j in range(3):
                    state = self.instance.query('1;SIGN:CSW:STAT?')
                    if state == 'CEST\n':
                        global_element.emitsingle.stateupdataSingle.emit('DUT Connection Successful!')
                        isconnected = True
                        break
                    elif state == 'SYNC\n':
                        self.instance.write('1;PROC:SIGN:ACT MTC')
                    elif state == 'ALER\n':
                        global_element.emitsingle.stateupdataSingle.emit('The bell is ringing. Please answer it at DUT.')
                    else:
                        pass
                    time.sleep(5)

            return isconnected
        except:
            global_element.emitsingle.thread_exitSingle.emit('The DUT connection to the CU failed!')

    # 建立wcdma数据连接
    def wcdmacallsetup(self):
        try:
            global_element.emitsingle.stateupdataSingle.emit('DUT Connection……')
            isconnected = False
            if self.device_name == 'CMW500':
                self.instance.write('CALL:WCDM:SIGN:CSW:ACT CONN')
                for i in range(3):
                    state = self.instance.query('FETC:WCDM:SIGN:CSW:STAT?')
                    if state == 'CEST\n':
                        global_element.emitsingle.stateupdataSingle.emit('DUT Connection Successful!')
                        isconnected = True
                        break
                    elif state == 'REG\n':
                        self.instance.write('CALL:GSM:SIGN:CSW:ACT CONN')
                    elif state == 'PAG\n' or state == 'CONN\n':
                        time.sleep(5)

            if self.device_name == 'CMU200':
                self.instance.write('5;PROC:SIGN:ACT CTM')
                time.sleep(2)
                for j in range(3):
                    # # 停止功能函数接口
                    state_psw = self.instance.query('5;SIGN:PSW:STAT?')
                    time.sleep(0.2)
                    state_s = self.instance.query('5;SIGN:STAT?')
                    time.sleep(0.2)
                    if state_s == 'CEST\n':
                        global_element.emitsingle.stateupdataSingle.emit('DUT Connection Successful!')
                        isconnected = True
                        break
                    elif state_s == 'REG\n':
                        self.instance.write('5;PROC:SIGN:ACT CTM')
                    elif state_s == 'PAG\n':
                        time.sleep(5)
                    time.sleep(5)

            return isconnected
        except:
            global_element.emitsingle.thread_exitSingle.emit('The DUT connection to the CU failed!')

    # 设置GSM channel
    def set_gsm_channel(self, channel):
        if self.device_name == 'CMW500':
            self.instance.query('CONF:GSM:SIGN:RFS:CHAN:TCH ' + channel + '; *OPC?')
        if self.device_name == 'CMU200':
            self.instance.query('1;PROC:SIGN:CHAN ' + channel + '; *OPC?')

    # 设置GPRS channel
    def set_gprs_channel(self, channel):
        try:
            if self.device_name == 'CMW500':
                self.instance.query('CONF:GSM:SIGN:RFS:CHAN:TCH ' + channel + '; *OPC?')
            if self.device_name == 'CMU200':
                self.instance.query('1;PROC:SIGN:PDAT:MSL:CHAN ' + channel + '; *OPC?')
        except:
            global_element.emitsingle.thread_exitSingle.emit('The GPRS channel setup of the CU failed!')

    # 设置WCDMA channel
    def set_wcdma_channel(self, channel):
        if self.device_name == 'CMW500':
            self.instance.query('CONFigure:WCDMa:SIGN:RFSettings:CHANnel:UL ' + channel + '; *OPC?')

        if self.device_name == 'CMU200':
            if global_element.Test_band == 'Band II':
                channel_final = str(eval(channel) + 400)
            elif global_element.Test_band == 'Band IV' or global_element.Test_band == 'Band V':
                channel_final = str(eval(channel) + 225)

            self.instance.query('5;CONF:BSS:CHAN ' + channel_final + ';*OPC?')

    # 设置GSM PCL
    def set_gsm_pcl(self, pcl):
        if self.device_name == 'CMW500':
            self.instance.query('CONF:GSM:SIGN:RFS:PCL:TCH:CSW ' + pcl + '; *OPC?')
        if self.device_name == 'CMU200':
            self.instance.query('1;PROC:SIGN:MS:PCL ' + pcl + '; *OPC?')

    # 设置GPRS PCL
    def set_gprs_pcl(self, pcl):
        try:
            if global_element.Test_band == 'GSM850' or global_element.Test_band == 'GSM900':
                pcl_final = eval(pcl) - 2
            elif global_element.Test_band == 'DCS1800' or global_element.Test_band == 'PCS1900':
                pcl_final = eval(pcl) + 3
            else:
                global_element.emitsingle.thread_exitSingle.emit('Unsupported GPRS BAND!')

            pcl_str_final_cmu = (',' + str(pcl_final)) * 8
            pcl_str_final_cmw = ','.join([str(pcl_final)] * 8)

            if self.device_name == 'CMW500':
                self.instance.query('CONFigure:GSM:SIGN1:CONNection:PSWitched:SCONfig:GAMMa:UL ' + pcl_str_final_cmw
                                    + '; *OPC?')
                pass
            if self.device_name == 'CMU200':
                self.instance.query('1;PROC:SIGN:PDAT:TCH:MSL:MS:SCON OFF,OFF,ON,OFF,OFF,OFF,OFF,OFF' +
                                    pcl_str_final_cmu + '; *OPC?')
        except:
            global_element.emitsingle.thread_exitSingle.emit('The GPRS PCL setup of the CU failed!')

    # 设置GSM loss
    def set_gms_loss(self, ul_frequency, dl_frequency):
        ul_min_delta_index = 0
        ul_min_delta = 10000000
        dl_min_delta_index = 0
        dl_min_delta = 10000000
        for i in range(len(global_element.CU_DUT_loss['Loss']['loss'])):
            ul_delta_i = abs(eval(global_element.CU_DUT_loss['Loss']['loss'][i]['Frequency']) - eval(ul_frequency))
            dl_delta_i = abs(eval(global_element.CU_DUT_loss['Loss']['loss'][i]['Frequency']) - eval(dl_frequency))
            if ul_delta_i < ul_min_delta:
                ul_min_delta = ul_delta_i
                ul_min_delta_index = i
            if dl_delta_i < dl_min_delta:
                dl_min_delta = dl_delta_i
                dl_min_delta_index = i

        ul_loss_value = global_element.CU_DUT_loss['Loss']['loss'][ul_min_delta_index]['Value']
        dl_loss_value = global_element.CU_DUT_loss['Loss']['loss'][dl_min_delta_index]['Value']
        if self.device_name == 'CMW500':
            self.instance.write('CONF:GSM:SIGN:RFS:EATT:OUTP ' + ul_loss_value)
            self.instance.write('CONF:GSM:SIGN:RFS:EATT:INP ' + dl_loss_value)
        if self.device_name == 'CMU200':
            self.instance.write('1;SENS:CORR:LOSS:INP2 ' + ul_loss_value)
            self.instance.write('1;SENS:CORR:LOSS:OUTP2 ' + dl_loss_value)

    # 设置WCDMA loss
    def set_wcdma_loss(self, ul_frequency, dl_frequency):
        ul_min_delta_index = 0
        ul_min_delta = 10000000
        dl_min_delta_index = 0
        dl_min_delta = 10000000
        for i in range(len(global_element.CU_DUT_loss['Loss']['loss'])):
            ul_delta_i = abs(eval(global_element.CU_DUT_loss['Loss']['loss'][i]['Frequency']) - eval(ul_frequency))
            dl_delta_i = abs(eval(global_element.CU_DUT_loss['Loss']['loss'][i]['Frequency']) - eval(dl_frequency))
            if ul_delta_i < ul_min_delta:
                ul_min_delta = ul_delta_i
                ul_min_delta_index = i
            if dl_delta_i < dl_min_delta:
                dl_min_delta = dl_delta_i
                dl_min_delta_index = i

        ul_loss_value = global_element.CU_DUT_loss['Loss']['loss'][ul_min_delta_index]['Value']
        dl_loss_value = global_element.CU_DUT_loss['Loss']['loss'][dl_min_delta_index]['Value']
        if self.device_name == 'CMW500':
            self.instance.write('CONF:WCDMA:SIGN:RFS:EATT:OUTP ' + ul_loss_value)
            time.sleep(0.5)
            self.instance.write('CONF:WCDMA:SIGN:RFS:EATT:INP ' + dl_loss_value)
            time.sleep(0.5)

        if self.device_name == 'CMU200':
            self.instance.write('5;SENS:CORR:LOSS:INP2 ' + ul_loss_value)
            self.instance.write('5;SENS:CORR:LOSS:OUTP2 ' + dl_loss_value)

    # 获取GSM 功率
    def get_gsm_power(self):
        average_power_str = ''
        if self.device_name == 'CMW500':
            self.instance.write('CONF:GSM:MEAS:MEV:REP SING')
            self.instance.write('TRIGger:GSM:MEAS:MEValuation:SOURce "GSM Sig1: FrameTrigger"')
            self.instance.write("TRIGger:GSM:MEAS:MEValuation:TOUT ON")
            self.instance.write("TRIGger:GSM:MEAS:MEValuation:TOUT 0.1")
            self.instance.write("CONFigure:GSM:MEAS:MEValuation:MVIew ANY,ANY,ANY,ANY,ANY,ANY,ANY,ANY")
            self.instance.write("CONFigure:GSM:MEAS:MEValuation:MSLots 0,8,3")
            self.instance.write("CONFigure:GSM:MEAS:MEValuation:RESult ON,ON,ON,ON,ON,ON,ON,ON,ON,ON,OFF,OFF")
            # self.instance.write("CONFigure:GSM:MEAS:MEValuation:SCOunt:PVTime " + TestCount)
            self.instance.write("INITiate:GSM:MEAS:MEValuation")

            state = self.instance.query('FETCh:GSM:MEAS:MEValuation:STATe:ALL?')

            while state[:3] == 'RUN':
                state = self.instance.query('FETCh:GSM:MEAS:MEValuation:STATe:ALL?')
                time.sleep(0.5)

            time.sleep(1)
            pvt_result_str = self.instance.query('FETCh:GSM:MEAS1:MEValuation:PVTime?')
            try:
                average_power_str = str(format(eval(pvt_result_str.split(',')[5]), '.2f'))
            except:
                average_power_str = 'NULL'

        if self.device_name == 'CMU200':
            self.instance.write('1;CONF:RXQ:BER1:CONT:LEV:UNT -18.000000')
            self.instance.write('1;PROC:SIGN:TIM 3')
            self.instance.query('1;*CLS;*OPC?')
            self.instance.query('0;*ESR?')
            self.instance.write('1;CONF:POW:CONT SCAL,30')
            self.instance.write('1;CONF:POW:NORM:GMSK:CONT ARR,30')
            self.instance.write('1;CONF:POW:NORM:GMSK:CONT:REP SING,SON,NONE')
            self.instance.write('1;INIT:POW:NORM:GMSK')

            state = self.instance.query('1;FETC:POW:NORM:STAT?')

            while state[:3] == 'RUN':
                state = self.instance.query('1;FETC:POW:NORM:STAT?')
                time.sleep(0.5)

            time.sleep(1)
            pvt_result_str = self.instance.query('1;FETC:POW?')
            try:
                average_power_str = str(format(eval(pvt_result_str.split(',')[1]), '.2f'))
            except:
                average_power_str = 'NULL'

        return average_power_str

    # 获取wcdma 功率
    def get_wcdma_power(self):
        average_power_str = ''
        if self.device_name == 'CMW500':
            self.instance.query('CONFigure:WCDMa:SIGN:UL:TPC:MODE A1S1; SET ALL1; SET ALL1;*OPC?')
            self.instance.query('*OPC?')
            self.instance.query('CONFigure:WCDMa:SIGN:UL:TPC:TPOWer:REFerence?')
            self.instance.query("CONFigure:WCDMa:SIGN:RFSettings:COPower -56.10;*OPC?")
            self.instance.query("CONFigure:WCDMa:SIGN:RFSettings:ENPMode ULPC;*OPC?")
            self.instance.query("CONFigure:WCDMa:SIGN:UL:TPC:MODE A1S1; SET CLOop; TPOWer -3.0;*OPC?")
            self.instance.query("CONFigure:WCDMa:SIGN:UL:TPC:STATe?")
            self.instance.write('CONFigure:WCDMa:SIGN:DL:LEVel:PCPich -3.3; PCCPch -5.3; PSCH -8.3; SSCH -8.3;  '
                                'PICH -8.3; DPCH -10.3')
            self.instance.query('CONFigure:WCDMa:MEAS:MEValuation:RESult:ALL ON,OFF,OFF,ON,ON,OFF,OFF,OFF,OFF,OFF,OFF,'
                                'ON,OFF,OFF,OFF,OFF,OFF,OFF;*OPC?')
            self.instance.query('CONFigure:WCDMa:SIGN:UL:TPC:MODE A1S1; SET ALL1; SET ALL1;*OPC?')
            self.instance.write('CONFigure:WCDMa:MEAS:MEValuation:LIMit:EMASk:RELative -47.50,-47.50,-37.50,-33.50,'
                                '-48.50,-33.50')
            self.instance.query('CONFigure:WCDMa:MEAS:MEValuation:LIMit:EMASk:ABSolute -48.50,-13.00,-15.00,A;*OPC?')
            self.instance.query('CONFigure:WCDMa:SIGN:UL:TPC:TPOWer?')
            self.instance.query('CONFigure:WCDMa:SIGN:UL:TPC:STATe?')
            self.instance.write('CONFigure:WCDMa:SIGN:RFSettings:COPower -93.00')
            self.instance.query('CONFigure:WCDMa:SIGN:RFSettings:CARRier2:COPower -56.10;*OPC?')

            self.instance.write("INITiate:WCDMa:MEAS:MEValuation")
            time.sleep(1)
            state = self.instance.query('FETCh:WCDMa:MEAS:MEValuation:STATe?')

            while state[:3] == 'RUN':
                state = self.instance.query('FETCh:WCDMa:MEAS:MEValuation:STATe?')
                time.sleep(0.5)

            time.sleep(1)
            pvt_result_str = self.instance.query('FETCh:WCDMa:MEAS:MEValuation:TRACe:UEPower:AVERage?')
            try:
                average_power_str = str(format(eval(pvt_result_str.split(',')[1][:-1]), '.2f'))
            except:
                average_power_str = 'NULL'
            pass

        if self.device_name == 'CMU200':
            self.instance.write('5;TRIG:SOUR AUTO')
            self.instance.write('5;CONF:BSS:TPC:MODE ALG1')
            self.instance.write('5;CONF:BSS:PHYS:LEV:DPDC -10.3')
            self.instance.write('5;CONF:BSS:PHYS:LEV:CPIC:PRIM -7.000000')
            self.instance.write('5;CONF:BSS:PHYS:LEV:CCPC:PRIM -5.300000')
            self.instance.write('5;CONF:BSS:PHYS:LEV:SCH:SEC -8.300000')
            self.instance.write('5;CONF:BSS:PHYS:LEV:SCH:PRIM -8.300000')
            self.instance.write('5;SENS:LEV:MODE AUTO')
            self.instance.write('5;CONF:MOD:OVER:WCDM:DPCH:CONT:STAT 10')
            self.instance.write('5;LEV:MODE MAN')
            self.instance.write('5;LEV:MAX 33')
            self.instance.write('5;CONF:BSS:TPC:PTYP ALL1')
            self.instance.write('5;CONF:BSS:TPC:PSET SET1')
            self.instance.write('5;CONF:SPEC:EMAS:CONT:RMOD ARR')
            self.instance.write('5;INIT:SPEC:EMAS')

            state = self.instance.query('5;FETC:SPEC:EMAS:STAT?')

            while state[:3] == 'RUN':
                time.sleep(0.5)
                state = self.instance.query('5;FETC:SPEC:EMAS:STAT?')
                time.sleep(0.5)

            time.sleep(0.5)
            emas_result_str = self.instance.query('5;FETC:SCAL:SPEC:EMAS?')
            try:
                average_power_str = str(format(eval(emas_result_str.split(',')[3]), '.2f'))
            except:
                average_power_str = 'NULL'

            self.instance.write('5;ABOR:SPEC:EMAS')

        return average_power_str

    # 设置wcdma功控为MAX
    def set_wcdma_pcl_max(self):
        try:
            if self.device_name == 'CMW500':
                self.instance.query('CONFigure:WCDMa:SIGN:UL:TPC:MODE A1S1; SET ALL1; SET ALL1;*OPC?')
        except:
            global_element.emitsingle.stateupdataSingle.emit('Error:    The synthesizer set up WCDMA maximum power '
                                                             'control error!')

    # 获取GSM 功率
    def get_gprs_power(self):
        average_power_str = ''
        if self.device_name == 'CMW500':
            self.instance.write('CONF:GSM:MEAS:MEV:REP SING')
            self.instance.write('CONFigure:GSM:SIGN1:RFSettings:LEVel:TCH -80.00')
            self.instance.write('TRIGger:GSM:MEAS:MEValuation:SOURce "GSM Sig1: FrameTrigger"')
            self.instance.write("TRIGger:GSM:MEAS:MEValuation:TOUT ON")
            self.instance.write("TRIGger:GSM:MEAS:MEValuation:TOUT 0.1")
            self.instance.write('CONFigure:GSM:MEAS1:MEValuation:ABSearch OFF')
            self.instance.write("CONFigure:GSM:MEAS1:MEValuation:MVIew ANY,ANY,ANY,ANY,ANY,ANY,ANY,ANY")
            self.instance.write("CONFigure:GSM:MEAS1:MEValuation:SCOunt:PVTime 10")
            self.instance.write("CONFigure:GSM:MEAS1:MEValuation:SCOunt:MODulation 10")
            self.instance.write("CONFigure:GSM:SIGN1:CONNection:PSWitched:CATYpe NBURsts")
            self.instance.query('*opc?')
            self.instance.write("INITiate:GSM:MEAS1:MEValuation")

            state = self.instance.query('FETCh:GSM:MEAS1:MEValuation:STATe?')

            while state[:3] == 'RUN':
                state = self.instance.query('FETCh:GSM:MEAS1:MEValuation:STATe?')
                time.sleep(0.5)

            time.sleep(1)
            pvt_result_str = self.instance.query('FETCh:GSM:MEAS1:MEValuation:PVTime?')
            try:
                average_power_str = str(format(eval(pvt_result_str.split(',')[5]), '.2f'))
            except:
                average_power_str = 'NULL'
            pass

        if self.device_name == 'CMU200':
            self.instance.write('1;CONF:POW:NORM:EPSK:CONT:RPM DCOM')
            time.sleep(0.1)
            self.instance.write('1;CONF:POW:MSL:SCO 1')
            time.sleep(0.1)
            self.instance.write('1;CONF:MCON:MSL:MESL 2')
            time.sleep(0.1)
            self.instance.write('1;CONF:POW:MSL:CONT ARR, 50')
            time.sleep(0.1)
            self.instance.write('1;CONF:POW:MSL:CONT:REP SING,SON,NONE')
            time.sleep(0.1)
            self.instance.write('1;CONF:POW:MSL:MVi ANY,ANY,ANY,ANY')
            time.sleep(0.1)
            self.instance.write('1;INIT:POW:MSL')
            time.sleep(0.1)

            state = self.instance.query('1;FETC:POW:MSL:STAT?')

            while state[:3] == 'RUN':
                time.sleep(0.5)
                state = self.instance.query('1;FETC:POW:MSL:STAT?')
                time.sleep(0.5)

            time.sleep(1)
            pvt_result_str = self.instance.query('1;FETC:POW:MSL?')
            try:
                average_power_str = str(format(eval(pvt_result_str.split(',')[2]), '.2f'))
            except:
                average_power_str = 'NULL'

        return average_power_str

    # 获取GSM 频率误差
    def get_gsm_freerror(self, ulfre):
        max_freerror_str = ''
        if self.device_name == 'CMW500':
            self.instance.write('CONF:GSM:MEAS:MEV:REP SING')
            self.instance.write('TRIGger:GSM:MEAS:MEValuation:SOURce "GSM Sig1: FrameTrigger"')
            self.instance.write("TRIGger:GSM:MEAS:MEValuation:TOUT ON")
            self.instance.write("TRIGger:GSM:MEAS:MEValuation:TOUT 0.1")
            self.instance.write("CONFigure:GSM:MEAS:MEValuation:MVIew ANY,ANY,ANY,ANY,ANY,ANY,ANY,ANY")
            self.instance.write("CONFigure:GSM:MEAS:MEValuation:MSLots 0,8,3")
            self.instance.write("CONFigure:GSM:MEAS:MEValuation:RESult ON,ON,ON,ON,ON,ON,ON,ON,ON,ON,OFF,OFF")
            # self.instance.write("CONFigure:GSM:MEAS:MEValuation:SCOunt:PVTime " + TestCount)
            self.instance.write("INITiate:GSM:MEAS:MEValuation")

            state = self.instance.query('FETCh:GSM:MEAS:MEValuation:STATe:ALL?')

            while state[:3] == 'RUN':
                state = self.instance.query('FETCh:GSM:MEAS:MEValuation:STATe:ALL?')
                time.sleep(0.5)

            time.sleep(1)
            pvt_result_str = self.instance.query('FETCh:GSM:MEAS1:MEValuation:MODulation:MAXimum?')
            try:
                max_freerror = str(format(eval(pvt_result_str.split(',')[10]), '.2f'))
                max_freerror_str = str(format(eval(max_freerror) / eval(ulfre), '.2f'))
            except:
                max_freerror_str = 'NULL'

        if self.device_name == 'CMU200':
            self.instance.write('1;CONF:RXQ:BER1:CONT:LEV:UNT -18.000000')
            self.instance.write('1;PROC:SIGN:TIM 3')
            self.instance.query('1;*CLS;*OPC?')
            self.instance.query('0;*ESR?')
            self.instance.write('1;CONF:POW:CONT SCAL,30')
            self.instance.write('1;CONF:MOD:XPER:CONT ARR,30')
            self.instance.write('1;CONF:MOD:XPER:CONT:REP SING,SON,NONE')
            self.instance.write('1;CONF:MOD:XPER:TIME:DEC STAN')
            self.instance.write('1;INIT:MOD:XPER')

            state = self.instance.query('1;FETC:MOD:XPER:STAT?')

            while state[:3] == 'RUN':
                state = self.instance.query('1;FETC:MOD:XPER:STAT?')
                time.sleep(0.5)

            time.sleep(1)
            freerror_str = self.instance.query('1;FETC:MOD:XPER?')
            try:
                max_freerror = format(eval(freerror_str.split(',')[14]), '.2f')
                max_freerror_str = str(format(eval(max_freerror) / eval(ulfre), '.2f'))
            except:
                max_freerror_str = 'NULL'

        return max_freerror_str

    # 获取GPRS 频率误差
    def get_gprs_freerror(self, ulfre):
        max_freerror_str = ''
        if self.device_name == 'CMW500':
            self.instance.write('CONF:GSM:MEAS:MEV:REP SING')
            self.instance.write('TRIGger:GSM:MEAS:MEValuation:SOURce "GSM Sig1: FrameTrigger"')
            self.instance.write("TRIGger:GSM:MEAS:MEValuation:TOUT ON")
            self.instance.write("TRIGger:GSM:MEAS:MEValuation:TOUT 0.1")
            self.instance.write('CONFigure:GSM:MEAS1:MEValuation:ABSearch OFF')
            self.instance.write("CONFigure:GSM:MEAS1:MEValuation:MVIew ANY,ANY,ANY,ANY,ANY,ANY,ANY,ANY")
            self.instance.write("CONFigure:GSM:MEAS1:MEValuation:SCOunt:PVTime 10")
            self.instance.write("CONFigure:GSM:MEAS1:MEValuation:SCOunt:MODulation 10")
            self.instance.write("CONFigure:GSM:SIGN1:CONNection:PSWitched:CATYpe NBURsts")
            self.instance.query('*opc?')
            self.instance.write("INITiate:GSM:MEAS1:MEValuation")
            #
            state = self.instance.query('FETCh:GSM:MEAS1:MEValuation:STATe?')

            while state[:3] == 'RUN':
                state = self.instance.query('FETCh:GSM:MEAS1:MEValuation:STATe?')
                time.sleep(0.5)

            time.sleep(1)

            freerror_str = self.instance.query('FETCh:GSM:MEAS1:MEValuation:MODulation:MAXimum?')
            try:
                max_freerror = format(eval(freerror_str.split(',')[10]), '.2f')
                max_freerror_str = str(format(eval(max_freerror) / eval(ulfre), '.2f'))
            except:
                max_freerror_str = 'NULL'

        if self.device_name == 'CMU200':
            self.instance.write('1;LEV:MAX 38.0')
            self.instance.write('1;LEV:MODE AUT')
            self.instance.query('1;SIGN:PDAT:SERV?')
            self.instance.query('1;*OPC?')
            self.instance.write('1;LEV:MODE MAN')
            self.instance.write('1;PROC:NETW:PDAT:CATY NBUR')
            self.instance.write('1;CONF:MOD:XPER:GMSK:EREP OFF')
            self.instance.write('1;CONF:MOD:XPER:GMSK:CONT SCAL,50')
            self.instance.write('1;CONF:MOD:XPER:GMSK:CONT:REP SING,NONE,NONE')
            self.instance.write('1;CONF:MCON:MSL:MESL 2')
            self.instance.write('1;INIT:MOD:XPER:GMSK')

            state = self.instance.query('1;FETC:MOD:XPER:GMSK:STAT?')

            while state[:3] == 'RUN':
                time.sleep(0.5)
                state = self.instance.query('1;FETC:MOD:XPER:GMSK:STAT?')
                time.sleep(0.5)

            time.sleep(1)
            freerror_str = self.instance.query('1;FETC:MOD:XPER:GMSK?')
            try:
                max_freerror = format(eval(freerror_str.split(',')[14]), '.2f')
                max_freerror_str = str(format(eval(max_freerror) / eval(ulfre), '.2f'))
            except:
                max_freerror_str = 'NULL'

        return max_freerror_str

    # 综测GPRS模块初始化设置
    def gprsfccsin_init_setting(self, mode_str):
        try:
            if mode_str == 'GPRS':
                global_element.emitsingle.stateupdataSingle.emit('Initializing the GPRS parameters of the CU……')
            elif mode_str == 'EGPRS':
                global_element.emitsingle.stateupdataSingle.emit('Initializing the EGPRS parameters of the CU……')
            if self.device_name == 'CMW500':

                self.instance.write('SYST:RES:ALL')
                time.sleep(3)
                self.instance.query('*OPC?')

                self.instance.write('ROUT:GSM:MEAS:SCEN:CSP \'GSM Sig1\'')
                time.sleep(0.1)
                self.instance.query('CONF:BASE:FDC:RCL; *OPC?')
                time.sleep(0.1)
                self.instance.query('CONF:GSM:SIGN:CELL:SEC:AUTH OFF; *OPC?')  # 关闭鉴权
                time.sleep(0.1)
                self.instance.query('CONF:GSM:SIGN:CELL:BSP 2; *OPC?')
                time.sleep(0.1)
                self.instance.query('CONF:GSM:SIGN:CELL:BSAG 0; *OPC?')
                time.sleep(0.1)
                self.instance.query('CONF:GSM:SIGN:CELL:PLUP 0; *OPC?')
                time.sleep(0.1)
                self.instance.query('CONF:GSM:SIGN:CELL:BSAG 0; *OPC?')
                time.sleep(0.1)
                self.instance.query('CONF:GSM:SIGN:CELL:DTX OFF; *OPC?')
                time.sleep(0.1)
                self.instance.query('ROUT:GSM:SIGN:SCEN:SCELl RF1C,RX1,RF1C,TX1; *OPC?')
                time.sleep(0.1)
                self.instance.query('CONF:GSM:SIGN:CELL:IME ON; *OPC?')
                time.sleep(0.1)
                if global_element.Test_band == 'GSM850':
                    self.instance.query('CONF:GSM:SIGN:BAND G085; *OPC?')
                    time.sleep(0.1)
                    self.instance.query('CONF:GSM:SIGN:RFS:CHAN:TCH 192; *OPC?')
                    time.sleep(0.1)
                    self.instance.query('CONF:GSM:SIGN:RFS:CHAN:BCCH 162; *OPC?')
                    time.sleep(0.1)
                elif global_element.Test_band == 'GSM900':
                    self.instance.query('CONF:GSM:SIGN:BAND G09; *OPC?')
                    time.sleep(0.1)
                    self.instance.query('CONF:GSM:SIGN:RFS:CHAN:TCH 62; *OPC?')
                    time.sleep(0.1)
                    self.instance.query('CONF:GSM:SIGN:RFS:CHAN:BCCH 92; *OPC?')
                    time.sleep(0.1)
                elif global_element.Test_band == 'DCS1800':
                    self.instance.query('CONF:GSM:SIGN:BAND G18; *OPC?')
                    time.sleep(0.1)
                    self.instance.query('CONF:GSM:SIGN:RFS:CHAN:TCH 700; *OPC?')
                    time.sleep(0.1)
                    self.instance.query('CONF:GSM:SIGN:RFS:CHAN:BCCH 670; *OPC?')
                    time.sleep(0.1)
                elif global_element.Test_band == 'PCS1900':
                    self.instance.query('CONF:GSM:SIGN:BAND G19; *OPC?')
                    time.sleep(0.1)
                    self.instance.query('CONF:GSM:SIGN:RFS:CHAN:TCH 661; *OPC?')
                    time.sleep(0.1)
                    self.instance.query('CONF:GSM:SIGN:RFS:CHAN:BCCH 631; *OPC?')
                    time.sleep(0.1)
                else:
                    global_element.emitsingle.thread_exitSingle.emit('Unsupported GSM BAND:', global_element.Test_band)

                self.instance.write('CONF:GSM:SIGN:RFS:HOPP:ENAB:TCH OFF')
                self.instance.write('CONF:GSM:SIGN:CELL:MNC:DIG TWO')
                self.instance.write('CONF:GSM:SIGN:CELL:MCC 1; MNC 1; LAC 1')
                self.instance.query('CONF:GSM:SIGN:RFS:LEV:TCH:CSW ' + global_element.Test_bslevel + '; *OPC?')
                self.instance.write('CONF:GSM:SIGN:RFS:PCL:TCH:CSW 5')
                self.instance.write('CONFigure:GSM:SIGN:CONNection:CSWitched:DSOurce ECHO')
                self.instance.write('CONF:GSM:SIGN:CONN:CSW:TMOD FV1; TSL 5; CID "*#0123456789"')
                self.instance.write('CONF:GSM:SIGN:RFS:PMAX:BCCH 0')
                self.instance.write('CONF:GSM:SIGN:CELL:PSD ON')
                self.instance.write('CONF:GSM:SIGN:CELL:PSW:PDPC ACC')
                # self.instance.write('CONF:GSM:SIGN:ETOE OFF')
                self.instance.write('ABORt:GSM:MEAS1:MEValuation')
                self.instance.write('CONFigure:GSM:SIGN1:CONNection:CSWitched:TMODe FV1')
                # 配置多时系
                self.instance.write('CONFigure:GSM:SIGN1:CONNection:PSWitched:SCONfig:ENABle:UL OFF,OFF,OFF,ON,'
                                    'OFF,OFF,OFF,OFF')
                self.instance.write('CONFigure:GSM:SIGN1:CONNection:PSWitched:SCONfig:ENABle:DL:CARRier1 OFF,OFF,OFF,'
                                    'ON,OFF,OFF,OFF,OFF')
                self.instance.write('CONFigure:GSM:SIGN1:CONNection:PSWitched:SCONfig:LEVel:DL:CARRier1 OFF,OFF,OFF,'
                                    'ON,OFF,OFF,OFF,OFF')
                self.instance.write('CONFigure:GSM:SIGN1:CONNection:PSWitched:SCONfig:GAMMa:UL 3,3,3,3,3,3,3,3')

                self.instance.write('CONFigure:GSM:SIGN1:CONNection:PSWitched:SERVice TMA')
                self.instance.write('CONFigure:GSM:SIGN1:CONNection:PSWitched:DSOurce PR9')
                self.instance.write('CONFigure:GSM:SIGN1:CONNection:PSWitched:NOPDus 0')
                if mode_str == 'GPRS':
                    self.instance.write('CONFigure:GSM:SIGN1:CONNection:PSWitched:TLEVel GPRS')
                    self.instance.write('CONFigure:GSM:SIGN1:CONNection:PSWitched:CSCHeme:UL C1')
                    self.instance.write('CONFigure:GSM:SIGN1:CONNection:PSWitched:SCONfig:CSCHeme:DL:CARRier1 C1,C1,C1,'
                                        'C1,C1,C1,C1,C1')
                elif mode_str == 'EGPRS':
                    self.instance.write('CONFigure:GSM:SIGN1:CONNection:PSWitched:TLEVel EGPRs')
                    self.instance.write('CONFigure:GSM:SIGN1:CONNection:PSWitched:CSCHeme:UL MC5')
                    self.instance.write('CONFigure:GSM:SIGN1:CONNection:PSWitched:SCONfig:CSCHeme:DL:CARRier1 MC5,MC5,'
                                        'MC5,MC5,MC5,MC5,MC5,MC5')

                cu_dut_loss = global_element.CU_DUT_loss['Loss']['loss'][0]['Value']  # 取第一个loss值作为初始loss
                self.instance.write('CONF:GSM:SIGN:RFS:EATT:OUTP ' + cu_dut_loss)
                self.instance.write('CONF:GSM:SIGN:RFS:EATT:INP ' + cu_dut_loss)

                self.instance.write('SOUR:GSM:SIGN:CELL:STAT ON')
                time.sleep(3)
                # self.instance.query('*OPC?')

                sys_state = self.instance.query('syst:err?')
                sys_state_int = sys_state.split(',')[0]
                while sys_state_int != '0':
                    time.sleep(1)
                    sys_state = self.instance.query('syst:err?')
                    sys_state_int = sys_state.split(',')[0]

                # 检查GSM蜂窝是否打开，一直到打开为止
                isok = False
                while not isok:
                    time.sleep(0.5)
                    status = self.instance.query('SOUR:GSM:SIGN:CELL:STAT:ALL?')
                    onok = status.split(',')[1]
                    if onok == 'ADJ\n':
                        isok = True

            if self.device_name == 'CMU200':
                time.sleep(0.1)
                self.instance.write('0;SYST:RES:ALL')
                time.sleep(10)
                if global_element.Test_band == 'GSM850':
                    self.instance.write('0;SYST:REM:ADDR:SEC 1,"GSM850MS_Sig"')
                elif global_element.Test_band == 'GSM900':
                    self.instance.write('0;SYST:REM:ADDR:SEC 1,"GSM900MS_Sig"')
                elif global_element.Test_band == 'DCS1800':
                    self.instance.write('0;SYST:REM:ADDR:SEC 1,"GSM1800MS_Sig"')
                elif global_element.Test_band == 'PCS1900':
                    self.instance.write('0;SYST:REM:ADDR:SEC 1,"GSM1900MS_Sig"')

                self.instance.write('1;CONF:NETW:IDEN:MNC:DIG TWO')
                self.instance.write('1;CONF:NETW:SMOD:IMSI:MCC 001')
                self.instance.write('1;CONF:NETW:SMOD:IMSI:MNC 01')
                self.instance.write('1;CONF:NETW:SMOD:IMSI:MSIN "2345678901"')
                self.instance.write('0;SYST:GTRM:COMP OFF')
                self.instance.write('1;CONF:BSS:CCH:AUXT:CHTY OFF')
                self.instance.query('1;PROC:SIGN:PDAT:ACT SOFF;*OPC?')
                if mode_str == 'GPRS':
                    self.instance.write('1;CONF:NETW:NSUP GGPR')
                elif mode_str == 'EGPRS':
                    self.instance.write('1;CONF:NETW:NSUP GEGP')
                self.instance.write('1;CONF:NETW:MSER PDAT')
                self.instance.write('1;CONF:BSS:PDAT:MSL:PZER 0')
                self.instance.write('1;CONF:NETW:PDAT:NOPD 0')
                self.instance.write('1;CONF:BSS:CCH:MODE BATC')
                self.instance.write('1;CONF:MSS:CCH:PMAX 0')
                self.instance.query('1;CONF:BSS:PDAT:MSL:CHAN?')
                self.instance.write('1;CONF:BSS:CCH:AUXT:CHTY BCCH')
                self.instance.write('1;CONF:BSS:CCH:AUXT:CCCH ON')
                self.instance.write('1;CONF:BSS:CCH:AUXT:LEV:ABS -70.000000')
                if global_element.Test_band == 'GSM850':
                    self.instance.write('1;CONF:BSS:CCH:AUXT:CHAN 231')
                elif global_element.Test_band == 'GSM900':
                    self.instance.write('1;CONF:BSS:CCH:AUXT:CHAN 36')
                elif global_element.Test_band == 'DCS1800':
                    self.instance.write('1;CONF:BSS:CCH:AUXT:CHAN 720')
                elif global_element.Test_band == 'PCS1900':
                    self.instance.write('1;CONF:BSS:CCH:AUXT:CHAN 631')
                self.instance.query('1;BSS:PDAT:MSL:RLEV?')
                self.instance.write('1;CONF:BSS:PDAT:TCH:MSL:MTIM 2')
                # self.instance.write('1;CONF:BSS:PDAT:TCH:MSL:SCON OFF,OFF,ON,OFF,OFF,OFF,OFF,OFF,0,0,0,0,0,0,0,0')
                # self.instance.write('1;CONF:MSS:PDAT:TCH:MSL:SCON OFF,OFF,ON,OFF,OFF,OFF,OFF,OFF,3,3,3,3,3,3,3,3')
                if mode_str == 'GPRS':
                    self.instance.write('1;CONF:NETW:PDAT:GPRS:CSCH CS1')
                elif mode_str == 'EGPRS':
                    self.instance.write('1;CONF:NETW:PDAT:GPRS:CSCH MCS1')
                if global_element.Test_band == 'GSM850':
                    self.instance.write('1;CONF:BSS:PDAT:TCH:MSL:SCON OFF,OFF,ON,OFF,OFF,OFF,OFF,OFF,0,0,0,0,0,0,0,0')
                    self.instance.write('1;CONF:MSS:PDAT:TCH:MSL:SCON OFF,OFF,ON,OFF,OFF,OFF,OFF,OFF,3,3,3,3,3,3,3,3')
                    self.instance.write('1;CONF:BSS:PDAT:MSL:CHAN 128')
                elif global_element.Test_band == 'GSM900':
                    self.instance.write('1;CONF:BSS:PDAT:TCH:MSL:SCON OFF,OFF,ON,OFF,OFF,OFF,OFF,OFF,0,0,0,0,0,0,0,0')
                    self.instance.write('1;CONF:MSS:PDAT:TCH:MSL:SCON OFF,OFF,ON,OFF,OFF,OFF,OFF,OFF,3,3,3,3,3,3,3,3')
                    self.instance.write('1;CONF:BSS:PDAT:MSL:CHAN 975')
                elif global_element.Test_band == 'DCS1800':
                    self.instance.write('1;CONF:BSS:PDAT:TCH:MSL:SCON OFF,OFF,ON,OFF,OFF,OFF,OFF,OFF,0,0,0,0,0,0,0,0')
                    self.instance.write('1;CONF:MSS:PDAT:TCH:MSL:SCON OFF,OFF,ON,OFF,OFF,OFF,OFF,OFF,3,3,3,3,3,3,3,3')
                    self.instance.write('1;CONF:BSS:PDAT:MSL:CHAN 512')
                elif global_element.Test_band == 'PCS1900':
                    self.instance.write('1;CONF:BSS:PDAT:TCH:MSL:SCON OFF,OFF,ON,OFF,OFF,OFF,OFF,OFF,0,0,0,0,0,0,0,0')
                    self.instance.write('1;CONF:MSS:PDAT:TCH:MSL:SCON OFF,OFF,ON,OFF,OFF,OFF,OFF,OFF,3,3,3,3,3,3,3,3')
                    self.instance.write('1;CONF:BSS:PDAT:MSL:CHAN 512')

                self.instance.write('1;CONF:NETW:PDAT:NOPD 0')
                self.instance.write('1;INP:STAT RF2')
                self.instance.write('1;OUTP:STAT RF2')
                cu_dut_loss = global_element.CU_DUT_loss['Loss']['loss'][0]['Value']  # 取第一个loss值作为初始loss
                self.instance.write('1;SENS:CORR:LOSS:INP2 ' + cu_dut_loss)
                self.instance.write('1;SENS:CORR:LOSS:OUTP2 ' + cu_dut_loss)
                self.instance.write('1;LEV:MAX 38.0')
                self.instance.write('1;LEV:MODE AUT')
                self.instance.query('0;*ESR?')
                time.sleep(0.1)
                self.instance.query('1;SIGN:PDAT:STAT?')
                self.instance.write('1;CONF:NETW:IDEN:LAC 1')
                self.instance.query('1;SIGN:PDAT:STAT?')
                self.instance.query('1;PROC:SIGN:PDAT:ACT SON;*OPC?')
                time.sleep(10)
        except:
            if mode_str == 'GPRS':
                global_element.emitsingle.thread_exitSingle.emit('Error:    Error in initializing GPRS parameters of '
                                                                 'synthesizer!')
            elif mode_str == 'EGPRS':
                global_element.emitsingle.thread_exitSingle.emit('Error:    Error in initializing EGPRS parameters of '
                                                                 'synthesizer!')

    # 在规定时间内检查DUT是否已经连接CU
    def check_dut_gprs_issync(self):
        try:
            global_element.emitsingle.stateupdataSingle.emit('Waiting for DUT registration synchronization……')
            issync = False

            for i in range(3):
                if not issync:
                    # 如果没注册上，重启DUT
                    DUTcontrol.dutoffon()

                    # 从用户配置获取注册的等待时间
                    maxtime = int(global_element.active_dut_dict['xml']['DUTCONFIG']['MAXREGTIME'])
                    for wait_time in range(maxtime, 0, -1):
                        
                        # 查询是否注册
                        if self.device_name == 'CMW500':
                            checkresult_csw = self.instance.query('FETC:GSM:SIGN:CELL:CSW:STAT?')
                            checkresult_pdat = self.instance.query('FETCh:GSM:SIGN1:PSWitched:STATe?')
                            time.sleep(1)
                        elif self.device_name == 'CMU200':
                            checkresult_csw = self.instance.query('1;SIGN:CSW:STAT?')
                            checkresult_pdat = self.instance.query('1;SIGN:PDAT:STAT?')
                            time.sleep(1)
                        else:
                            checkresult_csw = ''
                            checkresult_pdat = ''

                        if checkresult_csw == 'SYNC\n' and checkresult_pdat == 'ATT\n':
                            global_element.emitsingle.stateupdataSingle.emit('DUT has been registered successfully!')
                            time.sleep(0.5)
                            issync = True
                            break

                        global_element.emitsingle.stateupdataSingle.emit('Waiting for DUT registration synchronization……，'
                                                                         'Waiting time is %d seconds left' % wait_time)
                        time.sleep(1)
                else:
                    break

            return issync
        except:
            global_element.emitsingle.thread_exitSingle.emit('DUT registered CU failed!')

    # 建立GPRS call
    def callsetup_gprs(self):
        try:
            global_element.emitsingle.stateupdataSingle.emit('DUT Connection……')
            isconnected = False
            if self.device_name == 'CMW500':
                self.instance.write('CALL:GSM:SIGN1:PSWitched:ACTion CONNect')
                for i in range(3):
                    state = self.instance.query('FETCh:GSM:SIGN1:PSWitched:STATe?')
                    if state == 'TBF\n':
                        global_element.emitsingle.stateupdataSingle.emit('DUT Connection Successful!')
                        isconnected = True
                        break
                    elif state == 'SYNC\n':
                        self.instance.write('CALL:GSM:SIGN1:PSWitched:ACTion CONNect')
                    elif state == 'CTIP\n':
                        time.sleep(3)
                    time.sleep(5)
                pass
            if self.device_name == 'CMU200':
                self.instance.query('1;PROC:SIGN:PDAT:ACT CTMA;*OPC?')
                for j in range(3):
                    state_pdat = self.instance.query('1;SIGN:PDAT:STAT?')
                    if state_pdat == 'TEST\n':
                        global_element.emitsingle.stateupdataSingle.emit('DUT Connection Successful!')
                        isconnected = True
                        break
                    elif state_pdat == 'ATT\n':
                        self.instance.write('1;PROC:SIGN:PDAT:ACT CTMA;*OPC?')
                    elif state_pdat == 'CTBF\n':
                        time.sleep(2)
                    time.sleep(3)
            return isconnected
        except:
            global_element.emitsingle.thread_exitSingle.emit('The DUT connection to the CU failed!')

    # 综测仪WCDMA模块初始化设置
    def wcdma_init_setting(self):
        try:
            global_element.emitsingle.stateupdataSingle.emit('Initializing WCDMA parameters of CU……')
            if self.device_name == 'CMW500':
                self.instance.write('SYST:RES:ALL')
                time.sleep(3)
                self.instance.query('*OPC?')

                sys_state = self.instance.query('syst:err?')
                sys_state_int = sys_state.split(',')[0]
                while sys_state_int != '0':
                    time.sleep(1)
                    sys_state = self.instance.query('syst:err?')
                    sys_state_int = sys_state.split(',')[0]

                self.instance.query('ROUT:WCDM:MEAS:SCEN:CSP \'WCDMA Sig1\'; *OPC?')
                time.sleep(0.1)
                # self.instance.query('CONF:BASE:FDC:RCL; *OPC?')
                # time.sleep(0.1)
                self.instance.query('CONF:WCDM:SIGN:UER:ENAB OFF; *OPC?')        # 关闭鉴权
                time.sleep(0.1)
                self.instance.query('ROUT:WCDM:SIGN:SCEN:SCEL RF1C,RX1,RF1C,TX1; *OPC?')
                time.sleep(0.1)
                self.instance.query('CONF:WCDM:SIGN:RFSettings:CARRier1:COPower -56.1; *OPC?')
                time.sleep(0.1)
                self.instance.query('CONFigure:WCDMa:SIGN:RFSettings:CARRier1:AWGN OFF; *OPC?')
                time.sleep(0.1)
                if global_element.Test_band == 'Band II':
                    self.instance.query('CONFigure:WCDMa:SIGN:CARRier1:BAND OB2;*OPC?')
                    self.instance.query('CONFigure:WCDMa:SIGN:RFSettings:CARRier1:CHANnel:DL 9662;*OPC?')
                    self.instance.query('CONFigure:WCDMa:SIGN:RFSettings:CHANnel:UL 9262;*OPC?')
                elif global_element.Test_band == 'Band IV':
                    self.instance.query('CONFigure:WCDMa:SIGN:CARRier1:BAND OB4;*OPC?')
                    self.instance.query('CONFigure:WCDMa:SIGN:RFSettings:CARRier1:CHANnel:DL 1537;*OPC?')
                    self.instance.query('CONFigure:WCDMa:SIGN:RFSettings:CHANnel:UL 1312;*OPC?')
                elif global_element.Test_band == 'Band V':
                    self.instance.query('CONFigure:WCDMa:SIGN:CARRier1:BAND OB5;*OPC?')
                    self.instance.query('CONFigure:WCDMa:SIGN:RFSettings:CARRier1:CHANnel:DL 4357;*OPC?')
                    self.instance.query('CONFigure:WCDMa:SIGN:RFSettings:CHANnel:UL 4132;*OPC?')
                self.instance.query('CONF:WCDM:SIGN:UL:SCOD #H0; *OPC?')
                time.sleep(0.1)
                self.instance.query('CONFigure:WCDMa:SIGN:CELL:CARRier1:SCODe #H0; *OPC?')
                time.sleep(0.1)
                self.instance.query('CONF:WCDM:SIGN:UL:TPC:SET CLO;MODE A1S1;TPOW -20; *OPC?')
                time.sleep(0.1)
                self.instance.query('CONF:WCDM:SIGN:DL:CARR1:LEV:PCP -3.3; *OPC?')
                time.sleep(0.1)
                self.instance.query('CONF:WCDM:SIGN:DL:LEVel:PSCH -8.3; SSCH -8.3; PCCP -5.3; SCCP -5.3; PICH -8.3;'
                                    ' AICH -8.3; *OPC?')
                time.sleep(0.1)
                self.instance.query('CONF:WCDM:SIGN:DL:LEV:DPCH ON; DPCH -10.3; *OPC?')
                time.sleep(0.1)
                self.instance.query('CONF:WCDM:SIGN:CELL:PSD ON; *OPC?')
                time.sleep(0.1)
                self.instance.query('CONF:WCDM:SIGN:CELL:MCC 1;MNC 1, D2;LAC 1; *OPC?')
                time.sleep(0.1)
                self.instance.query('CONF:WCDM:SIGN:UER:ENAB OFF; *OPC?')
                time.sleep(0.1)
                self.instance.query('CONF:WCDM:SIGN:CELL:RESelection:QUALity -18, -115; *OPC?')
                time.sleep(0.1)
                self.instance.query('CONF:WCDM:SIGN:DL:ENH:DPCH:POFF 0; *OPC?')
                time.sleep(0.1)
                self.instance.query('CONF:WCDM:SIGN:CELL:SEC:AUTH ON;ENAB ON;SKEY #H000102030405060708090A0B0C0D0E0F;'
                                    'OPC #H00000000000000000000000000000000;SIMC C3G; *OPC?')
                time.sleep(0.1)
                self.instance.query('CONF:WCDM:SIGN:UL:PRAC:DRXC 8; *OPC?')
                time.sleep(0.1)
                self.instance.query('CONF:WCDM:SIGN:CONN:RMC:KTLR OFF; *OPC?')
                time.sleep(0.1)
                self.instance.query('CONF:WCDM:SIGN:CONN:UET TEST; *OPC?')
                time.sleep(0.1)
                self.instance.query('CONFigure:WCDMa:SIGN:CONNection:TMODe:TYPE RMC; *OPC?')
                time.sleep(0.1)
                self.instance.query('CONF:WCDM:SIGN:CONN:RMC:TMOD MODE2; *OPC?')
                time.sleep(0.1)
                self.instance.query('CONF:WCDM:SIGN:CONN:RMC:DRAT R12K2,R12K2; *OPC?')
                time.sleep(0.1)
                self.instance.query('CONF:WCDM:SIGN:UPL:GFAC:RMC1 8, 15; RMC2 8, 15; RMC3 8, 15; RMC4 8, 15; *OPC?')
                time.sleep(0.1)
                self.instance.query('SYST:OPT:VERS? "CMW_Data_Application_Support"')
                time.sleep(0.1)
                # self.instance.query('CONF:WCDM:SIGN:ETOE OFF; *OPC?')
                # time.sleep(0.1)
                self.instance.query('SOUR:WCDM:SIGN:CELL:STAT OFF; *OPC?')
                time.sleep(0.1)
                self.instance.query('SOUR:WCDM:SIGN:CELL:STAT:ALL?')
                time.sleep(0.1)

                cu_dut_loss = global_element.CU_DUT_loss['Loss']['loss'][0]['Value']  # 取第一个loss值作为初始loss
                self.instance.write('CONF:WCDMA:SIGN:RFS:EATT:OUTP ' + cu_dut_loss)
                self.instance.write('CONF:WCDMA:SIGN:RFS:EATT:INP ' + cu_dut_loss)

                self.instance.write('SOUR:WCDM:SIGN:CELL:STAT ON')
                time.sleep(3)
                # self.instance.query('*OPC?')

                sys_state = self.instance.query('syst:err?')
                sys_state_int = sys_state.split(',')[0]
                while sys_state_int != '0':
                    time.sleep(1)
                    sys_state = self.instance.query('syst:err?')
                    sys_state_int = sys_state.split(',')[0]

                # # 检查GSM蜂窝是否打开，一直到打开为止
                isok = False
                while not isok:
                    time.sleep(0.5)
                    status = self.instance.query('SOUR:WCDM:SIGN:CELL:STAT:ALL?')
                    onok = status.split(',')[1]
                    if onok == 'ADJ\n':
                        isok = True

                self.instance.query('ROUT:WCDM:SIGN1?')
                time.sleep(0.1)

            if self.device_name == 'CMU200':
                time.sleep(0.1)
                # self.instance.write('0;SYST:RES:ALL')
                # time.sleep(10)
                self.instance.write('0;SYST:REM:ADDR:SEC 5,"WCDMA19UEFDD_Sig"')
                # self.instance.query('5;*RST;*OPC?')
                time.sleep(0.2)
                self.instance.query('5;*CLS;*OPC?')
                time.sleep(0.2)
                self.instance.query('0;*ESR?')
                time.sleep(0.2)

                self.instance.write('0;CONF:SYNC:FREQ:REF 1.000000E+007')
                time.sleep(0.1)
                self.instance.write('0;CONF:SYNC:FREQ:REF:MODE INT')
                time.sleep(0.1)
                self.instance.write('5;CONF:NETW:REQ:SKEY "0001020304050607","08090A0B0C0D0E0F"')
                self.instance.write('5;CONF:NETW:IDEN:IMSI "001012345678901"')
                self.instance.write('5;CONF:NETW:IDEN:MCC 001')
                self.instance.write('5;CONF:NETW:IDEN:LAC 3')
                self.instance.write('0;SYST:GTRM:COMP OFF')
                self.instance.write('5;PROC:SIGN:ACT SOFF')
                self.instance.write('5;INP:STAT RF2')
                self.instance.write('5;OUTP:STAT RF2')
                self.instance.write('5;CONF:NETW:IDEN:MNC:DIG TWO')
                self.instance.write('5;CONF:NETW:IDEN:MNC 01')
                self.instance.write('5;CONF:NETW:IDEN:MCC 001')
                if global_element.Test_band == 'Band II':
                    self.instance.write('5;CONF:NETW:OBAN OB2')
                elif global_element.Test_band == 'Band IV':
                    self.instance.write('5;CONF:NETW:OBAN OB4')
                elif global_element.Test_band == 'Band V':
                    self.instance.write('5;CONF:NETW:OBAN OB5')
                self.instance.write('5;UNIT:UES:CHAN CH')
                self.instance.write('5;UNIT:BSS:CHAN CH')
                self.instance.write('5;CONF:BSS:LREF OPOW')
                self.instance.write('5;CONF:BSS:OPOW ' + global_element.Test_bslevel)
                self.instance.write('5;CONF:BSS:PHYS:LEV:CPIC:PRIM -7.000000')
                self.instance.write('5;CONF:BSS:PHYS:LEV:CCPC:PRIM -5.300000')
                self.instance.write('5;CONF:BSS:PHYS:LEV:SCH:SEC -8.300000')
                self.instance.write('5;CONF:BSS:PHYS:LEV:SCH:PRIM -8.300000')
                self.instance.query('5;SIGN:STAT?')
                time.sleep(0.2)
                self.instance.write('5;CONF:BSS:PHYS:LEV:PICH -8.300000')
                self.instance.write('5;CONF:BSS:PHYS:LEV:CCPC:SEC -10.300000')
                self.instance.write('5;CONF:BSS:PHYS:LEV:CPIC:PRIM -3.300000')
                self.instance.query('5;CONF:UES:PCON:TPOW:VAL?')
                time.sleep(0.2)
                self.instance.write('5;CONF:UES:PCON:TPOW:VAL 0.000000')
                self.instance.write('5;CONF:BSS:TPC:PTYP CLOP')
                self.instance.write('5;LEV:MODE AUTO')
                self.instance.write('5;CONF:BSS:TPC:PSET SET1')
                self.instance.write('5;CONF:BSS:DCH:TYPE RMC')
                self.instance.write('5;CONF:BSS:DCH:RMC:TMOD MODE2')
                self.instance.write('5;CONF:BSS:DCH:RMC:TYPE RMC12')
                self.instance.write('5;CONF:BSS:DCH:RMC:RTYP 12.2')
                if global_element.Test_band == 'Band II':
                    self.instance.write('5;CONF:BSS:CHAN 9662')
                elif global_element.Test_band == 'Band IV':
                    self.instance.write('5;CONF:BSS:CHAN 1537')
                elif global_element.Test_band == 'Band V':
                    self.instance.write('5;CONF:BSS:CHAN 4357')
                self.instance.write('5;CONF:RXQ:BER:CONT:REP SING,NONE,NONE')
                self.instance.write('5;CONF:BSS:DCH:RMC:SDTC PR9')

                self.instance.write('5;LEV:MAX 33')
                self.instance.write('5;CONF:BSS:TPC:PTYP ALL1')
                self.instance.write('5;CONF:BSS:TPC:PSET SET1')

                cu_dut_loss = global_element.CU_DUT_loss['Loss']['loss'][0]['Value']  # 取第一个loss值作为初始loss
                self.instance.write('5;SENS:CORR:LOSS:INP2 ' + cu_dut_loss)
                self.instance.write('5;SENS:CORR:LOSS:OUTP2 ' + cu_dut_loss)
                self.instance.query('*OPC?')

                self.instance.write('5;CONF:BSS:LREF OPOW')
                self.instance.write('5;CONF:BSS:OPOW ' + global_element.Test_bslevel)
                self.instance.write('5;CONF:BSS:PHYS:LEV:CPIC:PRIM -7.000000')
                self.instance.write('5;CONF:BSS:PHYS:LEV:CCPC:PRIM -5.300000')
                self.instance.write('5;CONF:BSS:PHYS:LEV:SCH:SEC -8.300000')
                self.instance.write('5;CONF:BSS:PHYS:LEV:SCH:PRIM -8.300000')
                self.instance.query('5;SIGN:STAT?')
                time.sleep(0.2)
                self.instance.write('5;CONF:BSS:PHYS:LEV:PICH -8.300000')
                self.instance.write('5;CONF:BSS:PHYS:LEV:CCPC:SEC -10.300000')
                self.instance.write('5;CONF:BSS:PHYS:LEV:CPIC:PRIM -3.300000')
                self.instance.query('5;SIGN:STAT?')
                time.sleep(0.2)

                self.instance.query('5;PROC:SIGN:ACT SON;*OPC?')
                time.sleep(10)

        except:
            global_element.emitsingle.thread_exitSingle.emit('Error:    WCDMA parameter initialization error of CU!')

    # wcdma断开连接
    def wcdma_call_disconnect(self):
        try:
            if self.device_name == 'CMW500':
                pass
            elif self.device_name == 'CMU200':
                self.instance.write('5;LEV:MAX 30')
                self.instance.write('5;CONF:BSS:TPC:PTYP1 CLOP')
                self.instance.write('5;CONF:BSS:TPC:PSET SET1')
                self.instance.query('5;SIGN:STAT?')
                time.sleep(0.2)
                self.instance.query('5;SIGN:PSW:STAT?')
                time.sleep(0.2)
                self.instance.write('5;PROC:SIGN:ACT CREL')
                time.sleep(0.5)
                self.instance.write('5;PROC:SIGN:PSW:ACT PREL')
                time.sleep(0.2)
                self.instance.write('5;PROC:SIGN:ACT SOFF')
        except:
            global_element.emitsingle.thread_exitSingle.emit('Failed to disconnect DUT from CU!')

    # 获取wcdma frequency error
    def get_wcdma_frequencyerror(self, ulfre):
        max_freerror_str = ''
        if self.device_name == 'CMW500':
            self.instance.write('CONFigure:WCDMa:SIGN:RFSettings:COPower -56.10')
            self.instance.write('CONFigure:WCDMa:SIGN:RFSettings:CARRier2:COPower -56.10')
            self.instance.write("CONFigure:WCDMa:SIGN:RFSettings:ENPMode ULPC")
            self.instance.write("CONFigure:WCDMa:SIGN:UL:TPC:MODE A1S1; SET CLOop; TPOWer -3.0")
            self.instance.write("CONFigure:WCDMa:SIGN:DL:LEVel:PCPich -3.3; PCCPch -5.3; PSCH -8.3; SSCH -8.3;  "
                                "PICH -8.3; DPCH -10.3")
            self.instance.write("CONFigure:WCDMa:MEAS:MEValuation:RESult:ALL OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,"
                                "OFF,OFF,ON,OFF,OFF,OFF,OFF,OFF")
            self.instance.query("*OPC?")
            self.instance.query("CONFigure:WCDMa:SIGN:UL:TPC:MODE A1S1; SET ALL1; SET ALL1;*opc?")
            self.instance.write("CONFigure:WCDMa:SIGN:RFSettings:COPower -104.00")
            self.instance.query("CONFigure:WCDMa:SIGN:RFSettings:COPower -104.00;*opc?")
            self.instance.query("CONFigure:WCDMa:SIGN:RFSettings:CARRier2:COPower -56.10;*opc?")
            self.instance.query("CONFigure:WCDMa:SIGN:RFSettings:CARRier2:COPower -56.10;*opc?")

            self.instance.write("INITiate:WCDMa:MEAS:MEValuation")

            #
            state = self.instance.query('FETCh:WCDMa:MEAS:MEValuation:STATe?')

            while state[:3] == 'RUN':
                state = self.instance.query('FETCh:WCDMa:MEAS:MEValuation:STATe?')
                time.sleep(0.5)

            time.sleep(1)
            result_str = self.instance.query('FETCh:WCDMa:MEAS:MEValuation:TRACe:FERRor:MAX?')
            try:
                result_freerror_str = str(format(eval(result_str.split(',')[1]), '.2f'))
                max_freerror_str = format(eval(result_freerror_str) / eval(ulfre), '.2f')
            except:
                max_freerror_str = 'NULL'
            pass

        if self.device_name == 'CMU200':
            # self.instance.write('5;CONF:BSS:LREF OPOW')
            # self.instance.write('5;CONF:BSS:OPOW -80.000000')
            # self.instance.query('5;CONF:BSS:PHYS:LEV:CPIC:PRIM -7.000000')
            # self.instance.query('5;CONF:BSS:PHYS:LEV:CCPC:PRIM -5.300000')
            # self.instance.write('5;CONF:BSS:PHYS:LEV:SCH:SEC -8.300000')
            # self.instance.write('5;CONF:BSS:PHYS:LEV:SCH:PRIM -8.300000')
            # self.instance.query('5;SIGN:STAT?')
            # self.instance.write('5;CONF:BSS:PHYS:LEV:CPIC:PRIM -3.300000')
            # self.instance.query('5;SIGN:STAT?')
            self.instance.query('5;CONF:UES:PCON:TPOW:VAL?')
            self.instance.write('5;CONF:UES:PCON:TPOW:VAL 0.000000')
            self.instance.write('5;CONF:BSS:TPC:PTYP CLOP')
            self.instance.write('5;LEV:MODE AUTO')
            self.instance.write('5;CONF:BSS:TPC:PSET SET1')
            self.instance.query('5;*OPC?')
            self.instance.write('5;TRIG:SOUR AUTO')
            self.instance.write('5;CONF:BSS:TPC:MODE ALG1')
            self.instance.write('5;CONF:BSS:TPC:PSET SET1')
            self.instance.write('5;CONF:BSS:PHYS:LEV:DPDC -10.300000')
            self.instance.write('5;CONF:BSS:PHYS:LEV:CPIC:PRIM -7.000000')
            self.instance.write('5;CONF:BSS:PHYS:LEV:CCPC:PRIM -5.300000')
            self.instance.write('5;CONF:BSS:PHYS:LEV:SCH:SEC -8.300000')
            self.instance.write('5;CONF:BSS:PHYS:LEV:SCH:PRIM -8.300000')
            self.instance.query('5;SIGN:STAT?')
            self.instance.write('5;LEV:MODE AUTO')
            self.instance.write('5;LEV:MAX 33')
            self.instance.write('5;CONF:BSS:TPC:PTYP ALL1')
            self.instance.write('5;CONF:BSS:TPC:PSET SET1')
            self.instance.write('5;CONF:BSS:OPOW -80.000000')
            self.instance.write('5;CONF:MOD:OVER:WCDM:DPCH:CONT:STAT 10')
            self.instance.write('5;CONF:MOD:OVER:WCDM:DPCH:CONT:REP SING,NONE,NONE')

            result_str = self.instance.query('5;READ:MOD:OVER:WCDM:DPCH?')
            try:
                result_freerror_str = format(eval(result_str.split(',')[26]), '.2f')
                max_freerror_str = format(eval(result_freerror_str) / eval(ulfre), '.2f')
            except:
                max_freerror_str = 'NULL'

        return max_freerror_str

    # 综测仪LTE模块初始化设置
    def lte_init_setting(self, channel_list):
        result = True
        try:
            global_element.emitsingle.stateupdataSingle.emit('Initializing the LTE parameters of the CU……')
            if self.device_name == 'CMW500':
                self.instance.write('SYST:RES:ALL')
                time.sleep(3)
                # self.instance.query('*OPC?')

                sys_state = self.instance.query('syst:err?')
                sys_state_int = sys_state.split(',')[0]
                while sys_state_int != '0':
                    time.sleep(1)
                    sys_state = self.instance.query('syst:err?')
                    sys_state_int = sys_state.split(',')[0]

                self.instance.query('ROUT:LTE:MEAS:SCEN:CSP \'LTE Sig1\'; *OPC?')
                time.sleep(0.1)
                # self.instance.write('CONF:BASE:FDC:RCL')
                # time.sleep(0.5)
                #
                # sys_state = self.instance.query('syst:err?')
                # sys_state_int = sys_state.split(',')[0]
                # while sys_state_int != '0':
                #     time.sleep(1)
                #     sys_state = self.instance.query('syst:err?')
                #     sys_state_int = sys_state.split(',')[0]

                self.instance.query('CONF:LTE:SIGN:UER:ENAB OFF; *OPC?')  # 关闭鉴权
                time.sleep(0.1)
                self.instance.query('ROUT:LTE:SIGN:SCEN:SCEL RF1C,RX1,RF1C,TX1; *OPC?')
                time.sleep(0.1)
                self.instance.write('SOUR:LTE:SIGN:CELL:STAT OFF')
                time.sleep(0.1)
                self.instance.query('SOUR:LTE:SIGN:CELL:STAT:ALL?')
                time.sleep(0.1)
                self.instance.query('ROUTe:LTE:SIGN:SCENario?')
                time.sleep(0.1)
                self.instance.query('ROUTe:LTE:SIGN:SCENario:SCEL?')
                time.sleep(0.1)
                self.instance.query('CONF:LTE:SIGN:CELL:ULS:QAM64:ENAB?')
                time.sleep(0.1)
                self.instance.write('CONF:LTE:SIGN:DMOD:UCSP OFF')
                if 'FDD' in global_element.Test_band:
                    self.instance.write('CONF:LTE:SIGN:DMOD FDD')
                else:
                    self.instance.write('CONF:LTE:SIGN:DMOD TDD')
                # self.instance.write('CONF:LTE:SIGN:ETOE OFF')
                band_str = global_element.Test_band.split(' ')[1]
                self.instance.write('CONF:LTE:SIGN:BAND OB' + band_str)
                self.instance.write('CONF:LTE:SIGN:RFS:CHAN:UL ' + global_element.lte_channel_default_dict['10MHz'][global_element.Test_band].split(',')[1])
                self.instance.write('CONF:LTE:SIGN:CELL:BAND:DL B100')
                self.instance.write('CONF:LTE:SIGN:CELL:PCID 0')
                self.instance.write('CONF:LTE:SIGN:CELL:SCC1:PCID 1')
                self.instance.write('CONF:LTE:SIGN:CELL:SCC2:PCID 2')
                self.instance.write('CONF:LTE:SIGN:CELL:SCC3:PCID 3')
                self.instance.write('CONF:LTE:SIGN:CELL:SCC4:PCID 4')
                self.instance.write('CONF:LTE:SIGN:DL:RSEP:LEV ' + global_element.Test_bslevel)
                self.instance.write('CONF:LTE:SIGN:DL:SSS:POFF 0')
                self.instance.write('CONF:LTE:SIGN:DL:PBCH:POFF 0')
                self.instance.write('CONF:LTE:SIGN:DL:PSS:POFF 0')
                self.instance.write('CONF:LTE:SIGN:DL:PCF:POFF 0')
                self.instance.write('CONF:LTE:SIGN:DL:PDCC:POFF 0')
                self.instance.write('CONF:LTE:SIGN:DL:OCNG OFF')
                self.instance.write('CONF:LTE:SIGN:DL:PDSC:RIND 0')
                self.instance.write('CONF:LTE:SIGN:UL:PUSC:OLNP -20')
                self.instance.write('CONF:LTE:SIGN:DL:PDSC:PA ZERO')
                self.instance.write('CONF:LTE:SIGN:DL:AWGN OFF')
                self.instance.write('CONF:LTE:SIGN:UL:PUSC:TPC:SET CLO')
                self.instance.write('CONF:LTE:SIGN:UL:PMAX 24')
                self.instance.write('CONF:LTE:SIGN:CELL:SEC:AUTH ON')
                self.instance.write('CONF:LTE:SIGN:CELL:SEC:NAS ON')
                self.instance.write('CONF:LTE:SIGN:CELL:SEC:AS ON')
                self.instance.write('CONF:LTE:SIGN:CELL:SEC:IALG S3G')
                self.instance.write('CONF:LTE:SIGN:CELL:SEC:MIL OFF')
                self.instance.write('CONF:LTE:SIGN:CELL:SEC:SKEY #H000102030405060708090A0B0C0D0E0F')
                self.instance.write('CONF:LTE:SIGN:CELL:SEC:OPC #H00000000000000000000000000000000')
                self.instance.write('CONF:LTE:SIGN:CELL:UEID:IMSI "001010123456063"')
                self.instance.write('CONF:LTE:SIGN:CELL:MCC 1')
                self.instance.write('CONF:LTE:SIGN:CELL:MNC:DIG TWO')
                self.instance.write('CONF:LTE:SIGN:CELL:MNC 1')
                self.instance.write('CONF:LTE:SIGN:CELL:TAC 1')
                self.instance.write('CONF:LTE:SIGN:CELL:CID:EUTR #B0000000000000010000000000000')
                self.instance.write('CONF:LTE:SIGN:CONN:CTYP TEST')
                self.instance.write('CONF:LTE:SIGN:CELL:NAS:EPSN OFF')
                self.instance.write('CONF:LTE:SIGN:CELL:NAS:IMSV NSUP')
                self.instance.write('CONF:LTE:SIGN:CELL:NAS:EMCB NSUP')
                self.instance.write('CONF:LTE:SIGN:CELL:NAS:EPCL NSUP')
                self.instance.write('CONF:LTE:SIGN:CELL:NAS:CSLC NSUP')
                self.instance.write('CONF:LTE:SIGN:CONN:RLCM UM')
                self.instance.write('CONF:LTE:SIGN:CONN:TMODe ON')
                self.instance.write('CONF:LTE:SIGN:CONN:DLPadding ON')
                self.instance.write('CONF:LTE:SIGN:CONN:DLE 0')

                # self.instance.write('CONF:LTE:SIGN:CONN:ASEM NS01')
                self.instance.write('CONF:LTE:SIGN:CONN:KRRC ON')
                self.instance.write('CONF:LTE:SIGN:CONN:FCH BHAN')
                self.instance.write('CONF:LTE:SIGN:CONN:OBCH RED')
                self.instance.write('CONF:LTE:SIGN:CONN:AMDB ON')
                self.instance.write('CONF:LTE:SIGN:CONN:STYP RMC')
                self.instance.write('CONF:LTE:SIGN:CELL:PRAC:PCIN 12')
                self.instance.write('CONF:LTE:SIGN:CELL:PRAC:NRPR OFF')
                self.instance.write('CONF:LTE:SIGN:CELL:PRAC:PRST P2DB')
                self.instance.write('CONF:LTE:SIGN:CONN:TSCH SISO')
                self.instance.write('CONF:LTE:SIGN:UL:PUCC:CLTP -20')
                self.instance.write('CONF:LTE:SIGN:CONN:RMC:DL N50,QPSK,KEEP')
                self.instance.write('CONF:LTE:SIGN:CONN:RMC:UL N50,QPSK,KEEP')
                self.instance.write('CONF:LTE:SIGN:CONN:FCO FC4')
                self.instance.write('CONF:LTE:SIGN:CONN:RMC:RBP:DL LOW')
                self.instance.write('CONF:LTE:SIGN:CONN:RMC:RBP:UL LOW')
                self.instance.write('CONF:LTE:SIGN:UL:PUSC:TPC:CLTP -20')
                self.instance.write('CONF:LTE:SIGN:CELL:TOUT:OSYN 30')
                self.instance.write('CONF:LTE:SIGN:CELL:PRAC:LRS 123')
                self.instance.write('CONF:LTE:SIGN:CELL:PRAC:PCIN 12')
                self.instance.write('CONF:LTE:SIGN:CELL:PRAC:PFOF 0')
                self.instance.write('CONF:LTE:SIGN:CELL:PRAC:ZCZC 9')
                self.instance.write('CONF:LTE:SIGN:CONN:SCHM:ENAB OFF')
                self.instance.write('CONF:LTE:SIGN:CONN:SCHM 1,0,0,0,0,0')
                self.instance.write('CONF:LTE:SIGN:CELL:SRS:ENAB OFF')
                self.instance.write('CONF:LTE:SIGN:CELL:SRS:MCEN OFF')
                self.instance.write('CONF:LTE:SIGN:CELL:SCC1:SRS:ENAB OFF')
                self.instance.write('CONF:LTE:SIGN:CELL:SCC1:SRS:MCEN OFF')
                self.instance.write('CONF:LTE:SIGN:CELL:SCC2:SRS:ENAB OFF')
                self.instance.write('CONF:LTE:SIGN:CELL:SCC2:SRS:MCEN OFF')
                self.instance.write('CONF:LTE:SIGN:CELL:SCC3:SRS:ENAB OFF')
                self.instance.write('CONF:LTE:SIGN:CELL:SCC3:SRS:MCEN OFF')
                self.instance.write('CONF:LTE:SIGN:CELL:SCC4:SRS:ENAB OFF')
                self.instance.write('CONF:LTE:SIGN:CELL:SCC4:SRS:MCEN OFF')
                self.instance.write('CONF:LTE:SIGN:CELL:TDD:SPEC OFF')
                self.instance.query('SENSe:LTE:SIGN:CONNection:PCC:TSCHeme?')

                cu_dut_loss = global_element.CU_DUT_loss['Loss']['loss'][0]['Value']  # 取第一个loss值作为初始loss
                self.instance.write('CONF:LTE:SIGN:RFS:EATT:OUTP ' + cu_dut_loss)
                self.instance.write('CONF:LTE:SIGN:RFS:EATT:INP ' + cu_dut_loss)

                # BaseStationEnable
                self.instance.write('SOUR:LTE:SIGN:CELL:STAT ON')
                time.sleep(3)
                # self.instance.query('*OPC?')

                sys_state = self.instance.query('syst:err?')
                sys_state_int = sys_state.split(',')[0]
                while sys_state_int != '0':
                    time.sleep(1)
                    sys_state = self.instance.query('syst:err?')
                    sys_state_int = sys_state.split(',')[0]

                # # 检查LTE蜂窝是否打开，一直到打开为止
                isok = False
                while not isok:
                    time.sleep(0.5)
                    status = self.instance.query('SOUR:LTE:SIGN:CELL:STAT:ALL?')
                    onok = status.split(',')[1]
                    if onok == 'ADJ\n':
                        isok = True

                self.instance.query('ROUTe:LTE:SIGN1?')
                time.sleep(0.1)

                global_element.emitsingle.stateupdataSingle.emit('Initialization of LTE signaling parameters of the CU '
                                                                 'is completed!')

        except:
            result = False

        return result

    # 综测仪LTE CA模块初始化设置
    def lteca_init_setting(self, bw_list, channel_list):
        # 取第一个带宽组合中的第一个信道组合
        channel_str_list = channelstrtolist(channel_list[0])
        channel_first_group = channel_str_list[0].split('+')
        # 取第一个带宽组合
        bw_first_group = bw_list[0].split('+')

        result = True
        try:
            global_element.emitsingle.stateupdataSingle.emit('Initializing the LTE CA parameters of the CU……')
            if self.device_name == 'CMW500':
                self.instance.write('SYST:RES:ALL')
                time.sleep(3)
                # self.instance.query('*OPC?')

                state = False
                while state == False:
                    time.sleep(2)
                    try:
                        sys_state = self.instance.query('syst:err?')
                        state = True
                    except:
                        pass
                sys_state_int = sys_state.split(',')[0]
                while sys_state_int != '0':
                    time.sleep(1)
                    sys_state = self.instance.query('syst:err?')
                    sys_state_int = sys_state.split(',')[0]

                self.instance.query('ROUT:LTE:MEAS:SCEN:CSP \'LTE Sig1\'; *OPC?')
                time.sleep(0.1)

                self.instance.query('CONF:LTE:SIGN:UER:ENAB OFF; *OPC?')  # 关闭鉴权
                time.sleep(0.1)
                self.instance.write('SOUR:LTE:SIGN:CELL:STAT OFF')
                self.instance.write('CONFigure:LTE:SIGN:SCC:AMODe AUTO')
                self.instance.write('CONF:LTE:SIGN:SCC:UUL ON')
                self.instance.write('ROUTe:LTE:SIGN:SCENario:CATR:FLEXible SUA1,RF1C,RX1,RF1C,TX1,SUA2,RF1C,TX3,RF1C,'
                                    'RX3')
                time.sleep(1)
                state = False
                while state == False:
                    time.sleep(2)
                    try:
                        sys_state = self.instance.query('syst:err?')
                        state = True
                    except:
                        pass

                sys_state_int = sys_state.split(',')[0]
                while sys_state_int != '0':
                    time.sleep(1)
                    sys_state = self.instance.query('syst:err?')
                    sys_state_int = sys_state.split(',')[0]

                self.instance.query('SOUR:LTE:SIGN:CELL:STAT:ALL?')
                time.sleep(0.1)
                self.instance.write('CONF:LTE:SIGN:DMOD:UCSP OFF')
                if global_element.Test_band in ['CA_2C', 'CA_5B', 'CA_7C', 'CA_12B']:
                    self.instance.write('CONF:LTE:SIGN:DMOD FDD')
                elif global_element.Test_band in ['CA_38C', 'CA_41C']:
                    self.instance.write('CONF:LTE:SIGN:DMOD TDD')
                self.instance.write('CONF:LTE:SIGN:ETOE OFF')

                # 配置PCC初始频段
                band_list = ['CA_2C', 'CA_5B', 'CA_7C', 'CA_12B', 'CA_38C', 'CA_41C']
                band_cmd_list = ['OB2', 'OB5', 'OB7', 'OB12', 'OB38', 'OB41']
                for index in range(len(band_list)):
                    if global_element.Test_band == band_list[index]:
                        self.instance.write('CONF:LTE:SIGN:BAND ' + band_cmd_list[index])
                        break

                # 配置PCC初始带宽
                bw_list = ['1.4', '3', '5', '10', '15', '20']
                bw_cmd_list = ['014', '030', '050', '100', '150', '200']
                for index_bw in range(len(bw_list)):
                    if bw_list[index_bw] == bw_first_group[0]:
                        self.instance.write('CONF:LTE:SIGN:CELL:BAND:DL B' + bw_cmd_list[index_bw])
                        break

                # 配置PCC初始信道
                self.instance.write('CONF:LTE:SIGN:RFS:CHAN:UL ' + channel_first_group[0])

                self.instance.write('CONF:LTE:SIGN:CELL:PCID 0')
                self.instance.write('CONF:LTE:SIGN:CELL:SCC1:PCID 1')
                self.instance.write('CONF:LTE:SIGN:CELL:SCC2:PCID 2')
                self.instance.write('CONF:LTE:SIGN:CELL:SCC3:PCID 3')
                self.instance.write('CONF:LTE:SIGN:CELL:SCC4:PCID 4')
                self.instance.write('CONF:LTE:SIGN:DL:RSEP:LEV ' + global_element.Test_bslevel)
                self.instance.write('CONF:LTE:SIGN:DL:SSS:POFF 0')
                self.instance.write('CONF:LTE:SIGN:DL:PBCH:POFF 0')
                self.instance.write('CONF:LTE:SIGN:DL:PSS:POFF 0')
                self.instance.write('CONF:LTE:SIGN:DL:PCF:POFF 0')
                self.instance.write('CONF:LTE:SIGN:DL:PDCC:POFF 0')
                self.instance.write('CONF:LTE:SIGN:DL:OCNG OFF')
                self.instance.write('CONF:LTE:SIGN:DL:PDSC:RIND 0')
                self.instance.write('CONF:LTE:SIGN:UL:PUSC:OLNP -20')
                self.instance.write('CONF:LTE:SIGN:DL:PDSC:PA ZERO')
                self.instance.write('CONF:LTE:SIGN:DL:AWGN OFF')
                self.instance.write('CONF:LTE:SIGN:UL:PUSC:TPC:SET CLO')
                self.instance.write('CONF:LTE:SIGN:UL:PMAX 24')
                self.instance.write('CONF:LTE:SIGN:CELL:SEC:AUTH ON')
                self.instance.write('CONF:LTE:SIGN:CELL:SEC:NAS ON')
                self.instance.write('CONF:LTE:SIGN:CELL:SEC:AS ON')
                self.instance.write('CONF:LTE:SIGN:CELL:SEC:IALG S3G')
                self.instance.write('CONF:LTE:SIGN:CELL:SEC:MIL OFF')
                self.instance.write('CONF:LTE:SIGN:CELL:SEC:SKEY #H000102030405060708090A0B0C0D0E0F')
                self.instance.write('CONF:LTE:SIGN:CELL:SEC:OPC #H00000000000000000000000000000000')
                self.instance.write('CONF:LTE:SIGN:CELL:UEID:IMSI "001010123456063"')
                self.instance.write('CONF:LTE:SIGN:CELL:MCC 1')
                self.instance.write('CONF:LTE:SIGN:CELL:MNC:DIG TWO')
                self.instance.write('CONF:LTE:SIGN:CELL:MNC 1')
                self.instance.write('CONF:LTE:SIGN:CELL:TAC 1')
                self.instance.write('CONF:LTE:SIGN:CELL:CID:EUTR #B0000000000000010000000000000')
                self.instance.write('CONF:LTE:SIGN:CONN:CTYP TEST')
                self.instance.write('CONF:LTE:SIGN:CELL:NAS:EPSN OFF')
                self.instance.write('CONF:LTE:SIGN:CELL:NAS:IMSV NSUP')
                self.instance.write('CONF:LTE:SIGN:CELL:NAS:EMCB NSUP')
                self.instance.write('CONF:LTE:SIGN:CELL:NAS:EPCL NSUP')
                self.instance.write('CONF:LTE:SIGN:CELL:NAS:CSLC NSUP')
                self.instance.write('CONF:LTE:SIGN:CONN:RLCM UM')
                self.instance.write('CONF:LTE:SIGN:CONN:TMODe ON')
                self.instance.write('CONF:LTE:SIGN:CONN:DLPadding ON')
                self.instance.write('CONF:LTE:SIGN:CONN:DLE 0')
                # self.instance.write('CONF:LTE:SIGN:CONN:ASEM NS01')
                self.instance.write('CONF:LTE:SIGN:CONN:KRRC ON')
                self.instance.write('CONF:LTE:SIGN:CONN:FCH BHAN')
                self.instance.write('CONF:LTE:SIGN:CONN:OBCH RED')
                self.instance.write('CONF:LTE:SIGN:CONN:AMDB ON')
                self.instance.write('CONF:LTE:SIGN:CONN:STYP RMC')
                self.instance.write('CONF:LTE:SIGN:CELL:PRAC:PCIN 12')
                self.instance.write('CONF:LTE:SIGN:CELL:PRAC:NRPR OFF')
                self.instance.write('CONF:LTE:SIGN:CELL:PRAC:PRST P2DB')
                self.instance.write('CONF:LTE:SIGN:CONN:TSCH SISO')
                self.instance.write('CONF:LTE:SIGN:CONN:RMC:DL N6,Q16,KEEP')
                self.instance.write('CONF:LTE:SIGN:CONN:RMC:UL N1,QPSK,KEEP')
                self.instance.write('CONF:LTE:SIGN:CONN:FCO FC4')
                self.instance.write('CONF:LTE:SIGN:CONN:RMC:RBP:DL LOW')
                self.instance.write('CONF:LTE:SIGN:CONN:RMC:RBP:UL LOW')
                self.instance.write('CONF:LTE:SIGN:UL:PUSC:TPC:CLTP -20')
                self.instance.write('CONF:LTE:SIGN:CELL:TOUT:OSYN 30')
                self.instance.write('CONF:LTE:SIGN:CELL:PRAC:LRS 123')
                self.instance.write('CONF:LTE:SIGN:CELL:PRAC:PCIN 12')
                self.instance.write('CONF:LTE:SIGN:CELL:PRAC:PFOF 0')
                self.instance.write('CONF:LTE:SIGN:CELL:PRAC:ZCZC 9')
                self.instance.write('CONF:LTE:SIGN:CONN:SCHM:ENAB OFF')
                self.instance.write('CONF:LTE:SIGN:CONN:SCHM 1,0,0,0,0,0')
                self.instance.write('CONF:LTE:SIGN:CELL:SRS:ENAB OFF')
                self.instance.write('CONF:LTE:SIGN:CELL:SRS:MCEN OFF')
                self.instance.write('CONF:LTE:SIGN:CELL:SCC1:SRS:ENAB OFF')
                self.instance.write('CONF:LTE:SIGN:CELL:SCC1:SRS:MCEN OFF')
                self.instance.write('CONF:LTE:SIGN:CELL:SCC2:SRS:ENAB OFF')
                self.instance.write('CONF:LTE:SIGN:CELL:SCC2:SRS:MCEN OFF')
                self.instance.write('CONF:LTE:SIGN:CELL:SCC3:SRS:ENAB OFF')
                self.instance.write('CONF:LTE:SIGN:CELL:SCC3:SRS:MCEN OFF')
                self.instance.write('CONF:LTE:SIGN:CELL:SCC4:SRS:ENAB OFF')
                self.instance.write('CONF:LTE:SIGN:CELL:SCC4:SRS:MCEN OFF')
                self.instance.write('CONF:LTE:SIGN:CELL:TDD:SPEC OFF')
                self.instance.write('CONF:LTE:SIGN:CELL:SSUB 7')
                self.instance.write('CONF:LTE:SIGN:CELL:ULDL 1')
                self.instance.write('CONF:LTE:SIGN:SCC:UUL ON')

                # 配置SCC初始频段
                for index in range(len(band_list)):
                    if global_element.Test_band == band_list[index]:
                        self.instance.write('CONF:LTE:SIGN:SCC:BAND ' + band_cmd_list[index])
                        break

                self.instance.write('CONF:LTE:SIGN:DL:SCC:RSEP:LEV ' + global_element.Test_bslevel)
                self.instance.write('CONF:LTE:SIGN:DL:SCC:SSS:POFF 0')
                self.instance.write('CONF:LTE:SIGN:DL:SCC:PBCH:POFF 0')
                self.instance.write('CONF:LTE:SIGN:DL:SCC:PSS:POFF 0')
                self.instance.write('CONF:LTE:SIGN:DL:SCC:PCF:POFF 0')
                self.instance.write('CONF:LTE:SIGN:DL:SCC:PDCC:POFF 0')
                self.instance.write('CONF:LTE:SIGN:DL:SCC:OCNG OFF')
                self.instance.write('CONF:LTE:SIGN:DL:SCC:PDSC:RIND 0')

                # 配置SCC初始带宽
                for index_bw in range(len(bw_list)):
                    if bw_list[index_bw] == bw_first_group[1]:
                        self.instance.write('CONF:LTE:SIGN:CELL:BAND:SCC:DL B' + bw_cmd_list[index_bw])
                        break

                # 配置SCC初始信道
                self.instance.write('CONF:LTE:SIGN:RFS:SCC:CHAN:UL ' + channel_first_group[1])

                self.instance.write('CONF:LTE:SIGN:DL:SCC:PDSC:PA ZERO')
                self.instance.write('CONF:LTE:SIGN:DL:SCC:AWGN OFF')
                self.instance.write('CONF:LTE:SIGN:CONN:SCC:STYP RMC')
                self.instance.write('CONF:LTE:SIGN:CONN:SCC:RMC:DL N1,Q16,KEEP')
                self.instance.write('CONF:LTE:SIGN:CONN:FCO FC4')
                self.instance.write('CONF:LTE:SIGN:CONN:SCC:RMC:RBP:DL LOW')
                self.instance.write('CONF:LTE:SIGN:CONN:SCC:RMC:RBP:UL LOW')
                self.instance.write('CONF:LTE:SIGN:CONN:SCC:SCHM:ENAB OFF')
                self.instance.write('CONF:LTE:SIGN:CONN:SCC:SCHM 1,0,0,0,0,0')
                self.instance.write('CONF:LTE:SIGN:CONN:SCC:TSCH SISO')
                self.instance.write('ROUT:LTE:SIGN:SCEN:CATR RF1C,RX1,RF1C,TX1,RF1C,TX3,RF1C,RX3')

                cu_dut_loss = global_element.CU_DUT_loss['Loss']['loss'][0]['Value']  # 取第一个loss值作为初始loss
                self.instance.write('CONF:LTE:SIGN:RFS:EATT:OUTP ' + cu_dut_loss)
                self.instance.write('CONF:LTE:SIGN:RFS:SCC:EATT:OUTP ' + cu_dut_loss)

                self.instance.write('CONF:LTE:SIGN:RFS:EATT:INP ' + cu_dut_loss)
                self.instance.write('CONF:LTE:SIGN:RFS:SCC:EATT:INP ' + cu_dut_loss)

                # BaseStationEnable
                self.instance.write('SOUR:LTE:SIGN:CELL:STAT ON')
                time.sleep(3)
                # self.instance.query('*OPC?')

                sys_state = self.instance.query('syst:err?')
                sys_state_int = sys_state.split(',')[0]
                while sys_state_int != '0':
                    time.sleep(1)
                    sys_state = self.instance.query('syst:err?')
                    sys_state_int = sys_state.split(',')[0]

                # # 检查LTE蜂窝是否打开，一直到打开为止
                isok = False
                while not isok:
                    time.sleep(0.5)
                    status = self.instance.query('SOUR:LTE:SIGN:CELL:STAT:ALL?')
                    onok = status.split(',')[1]
                    if onok == 'ADJ\n':
                        isok = True

                self.instance.query('ROUTe:LTE:SIGN1?')
                time.sleep(0.1)

                global_element.emitsingle.stateupdataSingle.emit(
                    'Initialization of LTE signaling parameters of the CU '
                    'is completed!')

        except:
            result = False

        return result

    # 在规定时间内检查DUT是否已经连接CU
    def check_dut_issync_lte(self):
        issync = False
        try:
            global_element.emitsingle.stateupdataSingle.emit('Waiting for DUT registration synchronization……')
            for i in range(3):
                if not issync:
                    # 如果没注册上，重启DUT
                    DUTcontrol.dutoffon()

                    # 从用户配置获取注册的等待时间
                    maxtime = int(global_element.active_dut_dict['xml']['DUTCONFIG']['MAXREGTIME'])
                    for wait_time in range(maxtime, 0, -1):
                        # 停止功能函数接口
                        # 查询是否注册
                        if self.device_name == 'CMW500':
                            checkresult = self.instance.query('FETC:LTE:SIGN:PSW:STAT?')
                            time.sleep(0.5)

                            if checkresult == 'ATT\n':
                                global_element.emitsingle.stateupdataSingle.emit('DUT has been registered successfully!')
                                time.sleep(0.5)
                                issync = True
                                break

                        global_element.emitsingle.stateupdataSingle.emit('Waiting for DUT registration synchronization……，'
                                                                         'Waiting time is %d seconds left' % wait_time)
                        time.sleep(0.5)
                else:
                    break

        except:
            global_element.emitsingle.stateupdataSingle.emit('Error:    The CU checks whether the registration method '
                                                             'is wrong!')

        return issync

    # 建立LTE数据连接
    def ltecallsetup(self):
        isconnected = False
        try:
            global_element.emitsingle.stateupdataSingle.emit('DUT Connection……')

            if self.device_name == 'CMW500':
                self.instance.write('CALL:LTE:SIGN:PSW:ACT CONN')
                for i in range(3):
                    state = self.instance.query('FETC:LTE:SIGN:PSW:STAT?')
                    if state == 'CEST\n':
                        global_element.emitsingle.stateupdataSingle.emit('DUT Connection Successful!')
                        isconnected = True
                        break
                    elif state == 'ATT\n':
                        self.instance.write('CALL:LTE:SIGN:PSW:ACT CONN')
                    elif state == 'PAG\n' or state == 'CONN\n':
                        time.sleep(5)

        except:
            global_element.emitsingle.stateupdataSingle.emit('Error:    The method of connecting the DUT to the CU is '
                                                             'wrong!')
            isconnected = False

        return isconnected

    # 建立LTE CA数据连接
    def ltecacallsetup(self):
        isconnected = False
        try:
            global_element.emitsingle.stateupdataSingle.emit('DUT Connection……')

            if self.device_name == 'CMW500':
                self.instance.write('CALL:LTE:SIGN:PSW:ACT CONN')
                for i in range(3):
                    state = self.instance.query('FETC:LTE:SIGN:PSW:STAT?')
                    if state == 'CEST\n':
                        global_element.emitsingle.stateupdataSingle.emit('DUT Connection Successful!')
                        scc_state = self.instance.query('FETC:LTE:SIGN:SCC:STAT?')
                        if scc_state == 'OFF\n':
                            self.instance.write('CALL:LTE:SIGN:SCC:ACT MAC')
                            time.sleep(2)
                        isconnected = True
                        break
                    elif state == 'ATT\n':
                        self.instance.write('CALL:LTE:SIGN:PSW:ACT CONN')
                    elif state == 'PAG\n' or state == 'CONN\n':
                        time.sleep(5)
                    else:
                        time.sleep(10)

        except:
            global_element.emitsingle.stateupdataSingle.emit(
                'Error:    The method of connecting the DUT to the CU is '
                'wrong!')
            isconnected = False

        return isconnected

    # 检测LTE数据连接状态
    def lte_connect_state(self):
        isconnected = False
        try:
            if self.device_name == 'CMW500':
                state = self.instance.query('FETC:LTE:SIGN:PSW:STAT?')
                if state == 'CEST\n':
                    isconnected = True
                else:
                    global_element.emitsingle.stateupdataSingle.emit('LTE connection disconnected!')
                    sync_state = self.check_dut_issync_lte()
                    if sync_state == False:
                        global_element.emitsingle.stateupdataSingle.emit('DUT registration failed!')
                        return
                    else:
                        is_called = self.ltecallsetup()
                        if is_called == False:
                            global_element.emitsingle.stateupdataSingle.emit('DUT failed to establish connection!')
                            return
                        else:
                            global_element.emitsingle.stateupdataSingle.emit('DUT Connection Successful!')
                            isconnected = True
        except:
            global_element.emitsingle.stateupdataSingle.emit('Error:    The method of connecting the DUT to the '
                                                             'CU is wrong!')
            isconnected = False

        return isconnected

    # 设置lte channel
    def set_lte_channel(self, channel):
        try:
            if self.device_name == 'CMW500':
                self.instance.write('CONF:LTE:SIGN:RFS:CHAN:UL  ' + channel)
                time.sleep(2)
                sys_state = self.instance.query('syst:err?')
                sys_state_int = sys_state.split(',')[0]
                while sys_state_int != '0':
                    time.sleep(1)
                    sys_state = self.instance.query('syst:err?')
                    sys_state_int = sys_state.split(',')[0]
        except:
            global_element.emitsingle.stateupdataSingle.emit('Error:    Error setting LTE Channel in the CU!')

    # 设置lte 2ca channel
    def set_lteca_channel(self, channel_group):
        try:
            if self.device_name == 'CMW500':
                self.instance.write('CONF:LTE:SIGN:RFS:CHAN:UL ' + channel_group[0])
                time.sleep(2)
                sys_state = self.instance.query('syst:err?')
                sys_state_int = sys_state.split(',')[0]
                while sys_state_int != '0':
                    time.sleep(1)
                    sys_state = self.instance.query('syst:err?')
                    sys_state_int = sys_state.split(',')[0]

                self.instance.write('CONF:LTE:SIGN:RFS:SCC:CHAN:UL ' + channel_group[1])
                time.sleep(2)
                sys_state = self.instance.query('syst:err?')
                sys_state_int = sys_state.split(',')[0]
                while sys_state_int != '0':
                    time.sleep(1)
                    sys_state = self.instance.query('syst:err?')
                    sys_state_int = sys_state.split(',')[0]
        except:
            global_element.emitsingle.stateupdataSingle.emit('Error:    Error setting LTE CA Channel in the CU!')

    # 设置lte 2CA BW
    def set_lteca_BW(self, bw_group):
        try:
            bw_list = ['1.4', '3', '5', '10', '15', '20']
            bw_cmd_list = ['014', '030', '050', '100', '150', '200']

            if self.device_name == 'CMW500':

                index_pcc = bw_list.index(bw_group[0])
                index_scc = bw_list.index(bw_group[1])
                self.instance.write('CONF:LTE:SIGN:CELL:BAND:DL B' + bw_cmd_list[index_pcc])
                time.sleep(1)
                self.instance.write('CONF:LTE:SIGN:CELL:BAND:SCC:DL B' + bw_cmd_list[index_scc])

                sys_state = self.instance.query('syst:err?')
                sys_state_int = sys_state.split(',')[0]
                while sys_state_int != '0':
                    time.sleep(1)
                    sys_state = self.instance.query('syst:err?')
                    sys_state_int = sys_state.split(',')[0]

                time.sleep(2)
        except:
            global_element.emitsingle.stateupdataSingle.emit('Error:    Error in setting LTE CA BW for CU!')

    # 设置lte BW
    def set_lte_BW(self, BW):
        try:
            if BW == '1.4MHz':
                bw_str = '014'
            elif BW == '3MHz':
                bw_str = '030'
            elif BW == '5MHz':
                bw_str = '050'
            elif BW == '10MHz':
                bw_str = '100'
            elif BW == '15MHz':
                bw_str = '150'
            elif BW == '20MHz':
                bw_str = '200'
            else:
                bw_str = '100'

            if self.device_name == 'CMW500':
                self.instance.write('CONF:LTE:SIGN:CELL:BAND:DL B' + bw_str)
        except:
            global_element.emitsingle.stateupdataSingle.emit('Error:    Error in setting LTE BW for CU!')

    # 设置lte loss
    def set_lte_loss(self, ul_frequency, dl_frequency):
        ul_min_delta_index = 0
        ul_min_delta = 10000000
        dl_min_delta_index = 0
        dl_min_delta = 10000000
        for i in range(len(global_element.CU_DUT_loss['Loss']['loss'])):
            ul_delta_i = abs(eval(global_element.CU_DUT_loss['Loss']['loss'][i]['Frequency']) - eval(ul_frequency))
            dl_delta_i = abs(eval(global_element.CU_DUT_loss['Loss']['loss'][i]['Frequency']) - eval(dl_frequency))
            if ul_delta_i < ul_min_delta:
                ul_min_delta = ul_delta_i
                ul_min_delta_index = i
            if dl_delta_i < dl_min_delta:
                dl_min_delta = dl_delta_i
                dl_min_delta_index = i

        ul_loss_value = global_element.CU_DUT_loss['Loss']['loss'][ul_min_delta_index]['Value']
        dl_loss_value = global_element.CU_DUT_loss['Loss']['loss'][dl_min_delta_index]['Value']
        if self.device_name == 'CMW500':
            self.instance.write('CONF:LTE:SIGN:RFS:EATT:OUTP ' + ul_loss_value)
            time.sleep(0.5)
            self.instance.write('CONF:LTE:SIGN:RFS:EATT:INP ' + dl_loss_value)
            time.sleep(0.5)

    # 设置lte loss
    def set_lteca_loss(self, ul_frequency, dl_frequency):
        ul_min_delta_index = 0
        ul_min_delta = 10000000
        dl_min_delta_index = 0
        dl_min_delta = 10000000
        for i in range(len(global_element.CU_DUT_loss['Loss']['loss'])):
            ul_delta_i = abs(eval(global_element.CU_DUT_loss['Loss']['loss'][i]['Frequency']) - eval(ul_frequency))
            dl_delta_i = abs(eval(global_element.CU_DUT_loss['Loss']['loss'][i]['Frequency']) - eval(dl_frequency))
            if ul_delta_i < ul_min_delta:
                ul_min_delta = ul_delta_i
                ul_min_delta_index = i
            if dl_delta_i < dl_min_delta:
                dl_min_delta = dl_delta_i
                dl_min_delta_index = i

        ul_loss_value = global_element.CU_DUT_loss['Loss']['loss'][ul_min_delta_index]['Value']
        dl_loss_value = global_element.CU_DUT_loss['Loss']['loss'][dl_min_delta_index]['Value']
        if self.device_name == 'CMW500':
            self.instance.write('CONF:LTE:SIGN:RFS:EATT:OUTP ' + ul_loss_value)
            self.instance.write('CONF:LTE:SIGN:RFS:SCC:EATT:OUTP ' + ul_loss_value)
            time.sleep(0.5)
            self.instance.write('CONF:LTE:SIGN:RFS:EATT:INP ' + dl_loss_value)
            self.instance.write('CONF:LTE:SIGN:RFS:SCC:EATT:INP ' + dl_loss_value)
            time.sleep(0.5)

    # 设置lte 调制方式
    def set_lte_ul_modeandRB(self, mode, rb_count):
        if mode == '16-QAM':
            mode_str = 'Q16'
        elif mode == '64-QAM':
            mode_str = 'Q64'
        elif mode == 'QPSK':
            mode_str = 'QPSK'
        try:
            if self.device_name == 'CMW500':
                self.instance.write('CONF:LTE:SIGN:CONN:RMC:UL N' + rb_count + ',' + mode_str + ',KEEP')
        except:
            global_element.emitsingle.stateupdataSingle.emit('Error:    Error in setting LTE modulation mode and RB '
                                                             'number of the CU!')

    # 设置lte 2ca 调制方式
    def set_lteca_ul_modeandRB(self, mode_group, rb_ul_count_group):
        for index in range(len(mode_group)):
            if mode_group[index] == '16-QAM':
                mode_str = 'Q16'
            elif mode_group[index] == '64-QAM':
                mode_str = 'Q64'
            elif mode_group[index] == 'QPSK':
                mode_str = 'QPSK'
            try:
                if self.device_name == 'CMW500':
                    if index == 0:
                        self.instance.write('CONF:LTE:SIGN:CONN:PCC:RMC:UL N' + rb_ul_count_group[index] + ',' +
                                            mode_str + ',KEEP')
                    elif index == 1:
                        self.instance.write('CONF:LTE:SIGN:CONN:SCC1:RMC:UL N' + rb_ul_count_group[index] + ',' +
                                            mode_str + ',KEEP')
            except:
                global_element.emitsingle.stateupdataSingle.emit(
                    'Error:    Error in setting LTE CA modulation mode and RB '
                    'number of the CU!')

    # 设置lte RF Offset
    def set_lte_ul_RBoffset(self, rboffset):
        try:
            if self.device_name == 'CMW500':
                self.instance.write('CONF:LTE:SIGN:CONN:RMC:RBP:UL ' + rboffset)
        except:
            global_element.emitsingle.stateupdataSingle.emit('Error:    Error in setting LTE RB position for CU!')

    # 设置lte 2CA RB Offset
    def set_lteca_ul_RBoffset(self, rboffset_group):
        try:
            if self.device_name == 'CMW500':
                self.instance.write('CONF:LTE:SIGN:CONN:PCC:RMC:RBP:UL ' + rboffset_group[0])
                self.instance.write('CONF:LTE:SIGN:CONN:SCC:RMC:RBP:UL ' + rboffset_group[1])
        except:
            global_element.emitsingle.stateupdataSingle.emit('Error:    Error in setting LTE CA RB position for CU!')

    # 获取lte power
    def get_lte_power(self):
        average_power_str = ''
        if self.device_name == 'CMW500':
            self.instance.write('CONF:LTE:MEAS:MEV:REP SING')
            self.instance.write('CONF:LTE:SIGN:EBL:REP SING')
            self.instance.write('CONF:LTE:MEAS:MEV:SCON NONE')
            self.instance.write('CONF:LTE:MEAS:MEV:MOD:MSCH AUTO')
            self.instance.write('CONF:LTE:MEAS:MEV:RBAL:AUTO ON')
            self.instance.write('TRIG:LTE:MEAS:MEV:SOUR \'LTE Sig1: FrameTrigger\'')
            self.instance.write('CONF:LTE:SIGN:DL:RSEP:LEV -85.0')
            self.instance.write('CONF:LTE:SIGN:CONN:UET RMC')
            self.instance.write('CONF:LTE:MEAS:MEV:RES:ALL OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF')
            self.instance.write('CONFigure:LTE:SIGN:DL:PDSCh:PA ZERO')
            self.instance.write('CONFigure:LTE:SIGN:DL:PDSCh:RINDex 0')
            self.instance.write('CONF:LTE:SIGN:DL:PSS:POFF 0')
            self.instance.write('CONF:LTE:SIGN:DL:SSS:POFF 0')
            self.instance.write('CONF:LTE:SIGN:DL:PBCH:POFF 0')
            self.instance.write('CONF:LTE:SIGN:DL:PCFich:POFF 0')
            self.instance.write('CONF:LTE:SIGN:DL:PHICh:POFF 0')
            self.instance.write('CONF:LTE:SIGN:DL:PDCCh:POFF 0')
            self.instance.write('CONF:LTE:MEAS:MEV:RES:TXM ON')
            self.instance.query('CONFigure:LTE:SIGN:RFSettings:ENPMode ULPC;*OPC?')
            self.instance.query('CONFigure:LTE:SIGN:UL:PUSCh:TPC:SET MAXP;*OPC?')
            self.instance.query('CONF:LTE:MEAS:MEV:CTYP AUTO;*OPC?')
            if 'TDD' in global_element.Test_band:
                self.instance.write('CONF:LTE:MEAS:MEV:MSUB 2,1,0')

            self.instance.write('INIT:LTE:MEAS:MEV')
            time.sleep(0.5)

            state = self.instance.query('FETC:LTE:MEAS:MEV:STAT:ALL?')

            while state[:3] == 'RUN':
                state = self.instance.query('FETC:LTE:MEAS:MEV:STAT:ALL?')
                time.sleep(0.5)

            time.sleep(1)
            pvt_result_str = self.instance.query('FETC:LTE:MEAS:MEV:MOD:AVER?')
            try:
                average_power_str = str(format(eval(pvt_result_str.split(',')[17]), '.2f'))
            except:

                    # # 开启DUT并等待DUT注册上CU
                    # global_element.emitsingle.stateupdataSingle.emit('取值失败，DUT与CU将重新建立连接！')
                    # issync = global_element.CU_intance.check_dut_issync_lte()
                    #
                    # # 3次未能注册上则退出此条
                    # if issync == True:
                    #     global_element.emitsingle.stateupdataSingle.emit('DUT注册成功！')
                    #
                    #     time.sleep(2)
                    #
                    #     # 成功注册后建立数据连接
                    #     global_element.pausefuction()
                    #     isconnected = global_element.CU_intance.ltecallsetup()
                    #
                    #     # 如果没能建立连接退出此条
                    #     if isconnected == True:
                    #         global_element.emitsingle.stateupdataSingle.emit('DUT建立连接成功！')
                    #         count += 1
                    #         self.get_lte_power()
                    time.sleep(8)

                    self.instance.write('INIT:LTE:MEAS:MEV')
                    time.sleep(0.5)

                    state = self.instance.query('FETC:LTE:MEAS:MEV:STAT:ALL?')

                    while state[:3] == 'RUN':
                        state = self.instance.query('FETC:LTE:MEAS:MEV:STAT:ALL?')
                        time.sleep(0.5)

                    time.sleep(1)
                    pvt_result_str = self.instance.query('FETC:LTE:MEAS:MEV:MOD:AVER?')
                    try:
                        average_power_str = str(format(eval(pvt_result_str.split(',')[17]), '.2f'))
                    except:
                        average_power_str = 'NULL'

            return average_power_str

    # 设置lte为最大功率
    def set_lte_maxpower(self):
        try:
            if self.device_name == 'CMW500':
                self.instance.query('CONFigure:LTE:SIGN:UL:PUSCh:TPC:SET MAXP;*OPC?')
                self.instance.write('CONFigure:LTE:SIGN:UL:PUSCh:TPC:CLTPower 24')
        except:
            global_element.emitsingle.stateupdataSingle.emit('Error:    Setting LTE maximum power control error!')

    # 获取lte frequency error
    def get_lte_frequencyerror(self, ulfre):
        try:
            max_freerror_str = ''
            if self.device_name == 'CMW500':
                self.instance.write('CONF:LTE:MEAS:MEV:RES:TXM ON')
                self.instance.query('CONF:LTE:SIGN:CONN:DLP ON;*OPC?')
                self.instance.write("CONF:LTE:SIGN:DL:RSEP:LEV -120.6")
                self.instance.write("CONFigure:LTE:SIGN:RFSettings:ENPMode ULPC")
                self.instance.write("CONF:LTE:MEAS:MEV:SCO:MOD 20")
                self.instance.write("CONFigure:LTE:MEAS:CAGGregation:MCARrier PCC")
                self.instance.query("*OPC?")
                self.instance.query("CONF:LTE:MEAS:MEV:MOD:MSCH QPSK;*opc?")
                self.instance.write("CONF:LTE:MEAS:MEV:RBAL:AUTO ON")
                self.instance.query("CONF:LTE:MEAS:MEV:CTYP AUTO;*OPC?")
                self.instance.query("FETC:LTE:SIGN:PSW:STAT?")
                if 'TDD' in global_element.Test_band:
                    self.instance.write('CONF:LTE:MEAS:MEV:MSUB 2,1,0')

                self.instance.write("INIT:LTE:MEAS:MEV")

                #
                state = self.instance.query('FETC:LTE:MEAS:MEV:STAT:ALL?')

                while state[:3] == 'RUN':
                    state = self.instance.query('FETC:LTE:MEAS:MEV:STAT:ALL?')
                    time.sleep(0.5)

                time.sleep(1)
                result_str = self.instance.query('FETC:LTE:MEAS:MEV:MOD:AVER?')

                result_freerror_str = str(format(eval(result_str.split(',')[15]), '.2f'))
                max_freerror_str = format(eval(result_freerror_str) / eval(ulfre), '.2f')

                return max_freerror_str

        except:
            global_element.emitsingle.stateupdataSingle.emit('Error:    The CU methon of get value is wrong! ')
            return 'NULL'

    # 获取lte ca frequency error
    def get_lteca_frequencyerror(self, ulfre):
        try:
            max_freerror_str = ''
            if self.device_name == 'CMW500':
                self.instance.write('CONFigure:LTE:MEAS:MEValuation:MSUBframes 0,10,3')
                self.instance.write('CONFigure:LTE:SIGN:CONNection:SCC1:TRANsmission TM1')
                self.instance.write('CONFigure:LTE:SIGN:CONNection:TRANsmission TM1')
                self.instance.write('CONFigure:LTE:SIGN:SCC1:UUL ON')
                self.instance.write('CONFigure:LTE:SIGN:SCC1:CAGGregation:MODE INTR')
                self.instance.write('CONFigure:LTE:SIGN:CONNection:SCC1:DCIFormat D1A')
                self.instance.write('CONFigure:LTE:SIGN:CONNection:DCIFormat D1A')
                self.instance.write('CONFigure:LTE:SIGN:CONNection:DLPadding OFF')
                self.instance.write('CONF:LTE:MEAS:MEV:RES:ALL OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF')
                self.instance.write('CONF:LTE:MEAS:MEV:RES:TXM ON')
                self.instance.write('CONF:LTE:MEAS:MEV:RES:SEM ON')
                self.instance.write('TRIGger:LTE:MEAS:MEValuation:SOURce "LTE Sig1: FrameTrigger SCC1"')
                self.instance.write('CONFigure:LTE:MEAS:MEValuation:SCOunt:MODulation 20')
                self.instance.query('CONF:LTE:SIGN:DL:RSEP:LEV -85;*OPC?')
                self.instance.query('CONF:LTE:SIGN:DL:SCC:RSEP:LEV -85;*OPC?')
                self.instance.write('CONFigure:LTE:MEAS:CAGGregation:MCARrier PCC')
                self.instance.write('CONFigure:LTE:SIGN:UL:PUSCh:TPC:SET MAXP')
                self.instance.write('CONFigure:LTE:SIGN:RFSettings:SCC1:ENPMode ULPC')
                self.instance.write('CONFigure:LTE:MEAS:CAGGregation:MCARrier PCC')
                self.instance.write('CONF:LTE:MEAS:MEV:RBAL:AUTO ON')
                self.instance.write('CONF:LTE:MEAS:MEV:CTYP AUTO')

                self.instance.write("INIT:LTE:MEAS:MEV")

                #
                state = self.instance.query('FETC:LTE:MEAS:MEV:STAT:ALL?')

                while state[:3] == 'RUN':
                    state = self.instance.query('FETC:LTE:MEAS:MEV:STAT:ALL?')
                    time.sleep(0.5)

                time.sleep(1)
                result_str = self.instance.query('FETC:LTE:MEAS:MEV:MOD:AVER?')

                result_freerror_str = str(format(eval(result_str.split(',')[15]), '.2f'))
                max_freerror_str = format(eval(result_freerror_str) / eval(ulfre), '.3f')

                return max_freerror_str

        except:
            global_element.emitsingle.stateupdataSingle.emit('Error:    The CU methon of get value is wrong! ')
            return 'NULL'

    # 综测仪WLAN模块初始化设置
    def wlan_init_setting(self):
        result = True
        try:
            global_element.emitsingle.stateupdataSingle.emit('Initialization of WLAN parameters of the CU……')
            if self.device_name == 'CMW500':
                self.instance.write('SYST:RES:ALL')
                time.sleep(3)
                # self.instance.query('*OPC?')

                sys_state = self.instance.query('syst:err?')
                sys_state_int = sys_state.split(',')[0]
                while sys_state_int != '0':
                    time.sleep(1)
                    sys_state = self.instance.query('syst:err?')
                    sys_state_int = sys_state.split(',')[0]

                self.instance.query('ROUT:WLAN:MEAS:SCEN:CSP \'WLAN Sig1\'; *OPC?')
                time.sleep(0.1)
                self.instance.write('SOURce:WLAN:SIGN:STATe OFF')
                self.instance.write('ROUTe:WLAN:SIGN:SCENario:SCELl RF1C,RX1,RF1C,TX1')
                self.instance.write('CONFigure:WLAN:SIGN:CONNection:OMODe AP')
                self.instance.write('CONFigure:WLAN:SIGN:CONNection:SRATes ENAB')
                if global_element.Test_Datarate == '1':
                    daterate_cmd = 'MAND,DIS,DIS,DIS'
                elif global_element.Test_Datarate == '2':
                    daterate_cmd = 'DIS,MAND,DIS,DIS'
                elif global_element.Test_Datarate == '5.5':
                    daterate_cmd = 'DIS,DIS,MAND,DIS'
                elif global_element.Test_Datarate == '11':
                    daterate_cmd = 'DIS,DIS,DIS,MAND'
                elif global_element.Test_Datarate == '6':
                    daterate_cmd = 'MAND,DIS,DIS,DIS,DIS,DIS,DIS,DIS'
                elif global_element.Test_Datarate == '9':
                    daterate_cmd = 'DIS,MAND,DIS,DIS,DIS,DIS,DIS,DIS'
                elif global_element.Test_Datarate == '12':
                    daterate_cmd = 'DIS,DIS,MAND,DIS,DIS,DIS,DIS,DIS'
                elif global_element.Test_Datarate == '18':
                    daterate_cmd = 'DIS,DIS,DIS,MAND,DIS,DIS,DIS,DIS'
                elif global_element.Test_Datarate == '24':
                    daterate_cmd = 'DIS,DIS,DIS,DIS,MAND,DIS,DIS,DIS'
                elif global_element.Test_Datarate == '36':
                    daterate_cmd = 'DIS,DIS,DIS,DIS,DIS,MAND,DIS,DIS'
                elif global_element.Test_Datarate == '48':
                    daterate_cmd = 'DIS,DIS,DIS,DIS,DIS,DIS,MAND,DIS'
                elif global_element.Test_Datarate == '54':
                    daterate_cmd = 'DIS,DIS,DIS,DIS,DIS,DIS,DIS,MAND'
                elif global_element.Test_Datarate == 'MCS0':
                    daterate_cmd = 'SUPP,NOTS,NOTS,NOTS,NOTS,NOTS,NOTS,NOTS'
                elif global_element.Test_Datarate == 'MCS1':
                    daterate_cmd = 'NOTS,SUPP,NOTS,NOTS,NOTS,NOTS,NOTS,NOTS'
                elif global_element.Test_Datarate == 'MCS2':
                    daterate_cmd = 'NOTS,NOTS,SUPP,NOTS,NOTS,NOTS,NOTS,NOTS'
                elif global_element.Test_Datarate == 'MCS3':
                    daterate_cmd = 'NOTS,NOTS,NOTS,SUPP,NOTS,NOTS,NOTS,NOTS'
                elif global_element.Test_Datarate == 'MCS4':
                    daterate_cmd = 'NOTS,NOTS,NOTS,NOTS,SUPP,NOTS,NOTS,NOTS'
                elif global_element.Test_Datarate == 'MCS5':
                    daterate_cmd = 'NOTS,NOTS,NOTS,NOTS,NOTS,SUPP,NOTS,NOTS'
                elif global_element.Test_Datarate == 'MCS6':
                    daterate_cmd = 'NOTS,NOTS,NOTS,NOTS,NOTS,NOTS,SUPP,NOTS'
                elif global_element.Test_Datarate == 'MCS7':
                    daterate_cmd = 'NOTS,NOTS,NOTS,NOTS,NOTS,NOTS,NOTS,SUPP'


                if global_element.Test_type == 'WLAN_B':
                    self.instance.write('CONFigure:WLAN:SIGN:CONNection:STANdard BSTD')
                    self.instance.write('CONFigure:WLAN:SIGN:CONNection:SRATes:DSSSconf ' + daterate_cmd)
                elif global_element.Test_type == 'WLAN_A':
                    self.instance.write('CONFigure:WLAN:SIGN:CONNection:STANdard ASTD')
                    self.instance.write('CONFigure:WLAN:SIGN:CONNection:SRATes:OFDMconf ' + daterate_cmd)
                elif global_element.Test_type == 'WLAN_G':
                    self.instance.write('CONFigure:WLAN:SIGN:CONNection:STANdard GOST')
                    self.instance.write('CONFigure:WLAN:SIGN:CONNection:SRATes:OFDMconf ' + daterate_cmd)
                elif global_element.Test_type == 'WLAN_N':
                    self.instance.write('CONFigure:WLAN:SIGN:CONNection:STANdard GONS ')
                    self.instance.write('CONFigure:WLAN:SIGN:CONNection:SRATes:OFDMconf DIS,DIS,DIS,DIS,DIS,DIS,DIS,DIS')
                    self.instance.write('CONFigure:WLAN:SIGN:CONNection:SRATes:OMCSconf ' + daterate_cmd)
                elif global_element.Test_type == 'WLAN_AC':
                    self.instance.write('CONFigure:WLAN:SIGN:CONNection:STANdard ACST ')
                    self.instance.write('CONFigure:WLAN:SIGN:CONNection:SRATes:VHTC MC09')
                    self.instance.write('CONFigure:WLAN:SIGN:RFS:OCW BW' + global_element.Test_wlan_bw[-2:])

                if global_element.Test_wlan_bw == 'VTH20':
                    self.instance.write('CONFigure:WLAN:SIGN:RFSettings:CHAN 36')
                elif global_element.Test_wlan_bw == 'VTH40':
                    self.instance.write('CONFigure:WLAN:SIGN:RFSettings:CHAN 38')
                elif global_element.Test_wlan_bw == 'VTH80':
                    self.instance.write('CONFigure:WLAN:SIGN:RFSettings:CHAN 42')

                self.instance.write('CONFigure:WLAN:SIGN:RFSettings:BOPower -40')
                self.instance.write('CONFigure:WLAN:SIGN:RFSettings:EPEPower 35')
                self.instance.write('CONFigure:WLAN:SIGN:IPVFour:STATic:IPADdress:DESTination 192,168,1,100')
                self.instance.write('CONFigure:WLAN:SIGN:IPVFour:STATic:SMASk 255,255,255,0')
                self.instance.write('CONFigure:WLAN:SIGN:IPVFour:STATic:IPADdress:GATeway 192,168,1,1')
                self.instance.write('CONFigure:WLAN:SIGN:IPVFour:DHCP ON')
                self.instance.write('CONFigure:WLAN:SIGN:PGEN:CONFig ON,100,1000,DEF')

                # 打开信号
                wlan_signal_state = self.instance.query('SOURce:WLAN:SIGN:STATe?')

                if wlan_signal_state != 'ON\n':
                    self.instance.write('SOURce:WLAN:SIGN:STATe ON')

                while wlan_signal_state != 'ON\n':
                    wlan_signal_state = self.instance.query('SOURce:WLAN:SIGN:STATe?')
                    time.sleep(1)

                self.instance.write('ROUTe:WLAN:MEAS:SCENario:CSPath  "WLAN Sig1"')
                self.instance.write('TRIGger:WLAN:MEAS:MEValuation:SOURce "WLAN Sig1: RXFrameTrigger"')

                if global_element.Test_Datarate == '1':
                    TEMPSTR = "D1MB"
                elif global_element.Test_Datarate == '2':
                    TEMPSTR = "D2MB"
                elif global_element.Test_Datarate == '5.5':
                    TEMPSTR = "C55M "
                elif global_element.Test_Datarate == '11':
                    TEMPSTR = "C11M "
                elif global_element.Test_Datarate == '6':
                    TEMPSTR = "BR12"
                elif global_element.Test_Datarate == '9':
                    TEMPSTR = "BR34"
                elif global_element.Test_Datarate == '12':
                    TEMPSTR = "QR12"
                elif global_element.Test_Datarate == '18':
                    TEMPSTR = "QR34"
                elif global_element.Test_Datarate == '24':
                    TEMPSTR = "Q1M12"
                elif global_element.Test_Datarate == '36':
                    TEMPSTR = "Q1M34"
                elif global_element.Test_Datarate == '48':
                    TEMPSTR = "Q6M23"
                elif global_element.Test_Datarate == '54':
                    TEMPSTR = "Q6M34"
                elif global_element.Test_Datarate == 'MCS0':
                    TEMPSTR = "MCS"
                else:
                    TEMPSTR = global_element.Test_Datarate

                self.instance.write("CONFigure:WLAN:SIGN:PER:MCRate " + TEMPSTR)
                time.sleep(1)
                self.instance.write("CONFigure:WLAN:SIGN:PER:MCRate " + TEMPSTR)

                # self.instance.write('ROUTe:WLAN:MEAS:RFSettings:CONNector RF1C')
                # self.instance.write('CONFigure:WLAN:MEAS:RFSettings:FREQuency 2412MHz')
                # self.instance.write('CONFigure:WLAN:MEAS:RFSettings:ENPower 30')
                # self.instance.write('CONFigure:WLAN:MEAS:RFSettings:UMARgin 0')
                #
                # self.instance.write('CONFigure:WLAN:MEAS:MEValuation:REPetition SING')
                # self.instance.write('CONFigure:WLAN:MEAS:MEValuation:SCONdition NONE')
                # self.instance.write('CONFigure:WLAN:MEAS:MEValuation:SCOunt:MODulation 20')
                # self.instance.write('CONFigure:WLAN:MEAS:MEValuation:SCOunt:TSMask 20')
                # self.instance.write('CONFigure:WLAN:MEAS:MEValuation:SCOunt:PVT 20')
                #
                # self.instance.write('CONFigure:WLAN:MEAS:MEValuation:COMPensation:EFTaps ON,11')
                # self.instance.write('CONFigure:WLAN:MEAS:MEValuation:EMEThod ST2007')
                #
                # self.instance.write('CONFigure:WLAN:MEAS:MEValuation:COMPensation:TRACking:PHASe ON')
                # self.instance.write('CONFigure:WLAN:MEAS:MEValuation:COMPensation:TRACking:TIMing ON')
                #
                # if any([global_element.Test_type == 'WLAN_A', global_element.Test_type == 'WLAN_G']):
                #     self.instance.write('CONFigure:WLAN:MEAS:MEValuation:COMPensation:CESTimation PRE')
                # else:
                #     self.instance.write('CONFigure:WLAN:MEAS:MEValuation:COMPensation:CESTimation PAYL')
                #
                # self.instance.write('CONFigure:WLAN:MEAS:MEValuation:RESult:TSMask ON')
                # self.instance.write('CONFigure:WLAN:MEAS:MEValuation:RESult:PVTime ON')
                # self.instance.write('CONFigure:WLAN:MEAS:MEValuation:TSMask:OBWPercent ON')
                #
                # self.instance.write('CONFigure:WLAN:MEAS:MEValuation:RESult:SFLatness ON')
                #
                # if global_element.Test_type == 'WLAN_B':
                #     self.instance.write('CONFigure:WLAN:MEAS:ISIGnal:STANdard BDSS')
                #     self.instance.write('CONFigure:WLAN:MEAS:ISIGnal:ELENgth RED')
                # elif global_element.Test_type == 'WLAN_A' or global_element.Test_type == 'WLAN_G':
                #     self.instance.write('CONFigure:WLAN:MEAS:ISIGnal:STANdard AOFD')
                # elif global_element.Test_type == 'WLAN_N':
                #     self.instance.write('CONFigure:WLAN:MEAS:ISIGnal:STANdard NSIS')
                #     self.instance.write('CONFigure:WLAN:MEAS:ISIGnal:BTYPe MIX')
                #     if global_element.Test_wlan_bw == 'HT20':
                #         self.instance.write('CONFigure:WLAN:MEAS:ISIGnal:BWIDth BW20')
                #     elif global_element.Test_wlan_bw == 'HT40':
                #         self.instance.write('CONFigure:WLAN:MEAS:ISIGnal:BWIDth BW40')
                # elif global_element.Test_type == 'WLAN_AC':
                #     self.instance.write('CONFigure:WLAN:MEAS:ISIGnal:STANdard ACS')
                #     self.instance.write('CONFigure:WLAN:MEAS:ISIGnal:BTYPe MIX')
                #     if global_element.Test_wlan_bw == 'VHT20':
                #         self.instance.write('CONFigure:WLAN:MEAS:ISIGnal:BWIDth BW20')
                #     elif global_element.Test_wlan_bw == 'VHT40':
                #         self.instance.write('CONFigure:WLAN:MEAS:ISIGnal:BWIDth BW40')
                #     elif global_element.Test_wlan_bw == 'VHT80':
                #         self.instance.write('CONFigure:WLAN:MEAS:ISIGnal:BWIDth BW80')
                #     elif global_element.Test_wlan_bw == 'VHT160':
                #         self.instance.write('CONFigure:WLAN:MEAS:ISIGnal:BWIDth BW160')

        except:

            result = False

        return result

    # 设置wlan channel
    def set_wlan_channel(self, freq):
        try:
            if self.device_name == 'CMW500':
                self.instance.write('CONFigure:WLAN:SIGN:RFSettings:FREQuency ' + freq + 'MHz')
                time.sleep(2)
                sys_state = self.instance.query('syst:err?')
                sys_state_int = sys_state.split(',')[0]
                while sys_state_int != '0':
                    time.sleep(1)
                    sys_state = self.instance.query('syst:err?')
                    sys_state_int = sys_state.split(',')[0]
        except:
            global_element.emitsingle.stateupdataSingle.emit('Error:    WLAN Channel Error Setting Up in CU!')

    # check wlan 连接状态
    def check_wlan_connect_state(self):
        try:
            check_result = True
            if self.device_name == 'CMW500':
                state_connect = 'NULL'
                while state_connect != 'ASS\n':
                    state_connect = self.instance.query('FETC:WLAN:SIGN:PSW:STAT?')
                    time.sleep(1)

                state_power = self.instance.query('SENS:WLAN:SIGN:SINF:RXP?')
                while float(state_power.split(',')[0]) < -5:
                    time.sleep(1)
                    state_power = self.instance.query('SENS:WLAN:SIGN:SINF:RXP?')
                    global_element.emitsingle.stateupdataSingle.emit('pls reconnect UE!')

            return check_result
        except:
            global_element.emitsingle.thread_exitSingle.emit('The DUT connection to the CU failed!')

    # CMW 发射ARB波形
    def init_generator(self, freq, level, ARBfile):
        try:
            if self.device_name == 'CMW500':
                self.instance.write('ROUT:GPRF:GEN:SCEN:IQO RF4C,TX2')
                self.instance.write('SOUR:GPRF:GEN:RFS:FREQ ' + freq + 'MHz')

                self.instance.write('SOURce:GPRF:GEN:RFSettings:LEVel ' + level)
                self.set_gprf_loss(freq)
                self.instance.write('SOUR:GPRF:GEN:BBM ARB')
                self.instance.write("SOURce:GPRF:GEN:ARB:FILE \"D:\\HX\\" + ARBfile + ".wv\"")
                self.instance.write('TRIG:GPRF:GEN:ARB:AUT ON')
                self.instance.write('SOURce:GPRF:GEN:STATe ON')
        except:
            global_element.emitsingle.stateupdataSingle.emit('Error:    CMW500 failed to transmit ARB waveform!')

    # 设置GPRF loss
    def set_gprf_loss(self, frequency):
        min_delta_index = 0
        min_delta = 10000000
        for i in range(len(global_element.ESG_DUT_loss['Loss']['loss'])):
            delta_i = abs(eval(global_element.ESG_DUT_loss['Loss']['loss'][i]['Frequency']) - eval(frequency))
            if delta_i < min_delta:
                min_delta = delta_i
                min_delta_index = i

        loss_value = global_element.ESG_DUT_loss['Loss']['loss'][min_delta_index]['Value']

        if self.device_name == 'CMW500':
            self.instance.write('SOUR:GPRF:GEN:RFS:EATT ' + loss_value)

    # 设置WLAN loss
    def set_wlan_loss(self, frequency):
        min_delta_index = 0
        min_delta = 10000000
        for i in range(len(global_element.CU_DUT_loss['Loss']['loss'])):
            delta_i = abs(eval(global_element.CU_DUT_loss['Loss']['loss'][i]['Frequency']) - eval(frequency))
            if delta_i < min_delta:
                min_delta = delta_i
                min_delta_index = i

        loss_value = global_element.CU_DUT_loss['Loss']['loss'][min_delta_index]['Value']

        if self.device_name == 'CMW500':
            self.instance.write('CONF:WLAN:SIGN:RFS:EATT:OUTP ' + loss_value)
            self.instance.write('CONF:WLAN:SIGN:RFS:EATT:INP ' + loss_value)

    def set_wlan_bslevel(self, level):
        if self.device_name == 'CMW500':
            self.instance.write('CONFigure:WLAN:SIGN:RFSettings:BOPower ' + level)

    def get_wlan_per(self, packets):
        if self.device_name == 'CMW500':
            self.instance.write('CONF:WLAN:SIGN:PER:PACK ' + str(packets))
            if global_element.Test_type == 'WLAN_AC':
                if global_element.Test_Datarate != 'MCS0':
                    self.instance.write('CONF:WLAN:SIGN:PER:FDEF VHT,BW'+ global_element.Test_wlan_bw[-2:] + ',' + global_element.Test_Datarate)
                else:
                    self.instance.write('CONF:WLAN:SIGN:PER:FDEF VHT,BW' + global_element.Test_wlan_bw[-2:] + ',MCS')

            elif global_element.Test_type == 'WLAN_N':
                self.instance.write('CONF:WLAN:SIGN:PER:FDEF HTM,BW' + global_element.Test_wlan_bw[
                                                                       -2:] + ',' + global_element.Test_Datarate)
            packets_done = 0
            while packets_done < int(packets):
                self.instance.write('INITiate:WLAN:SIGN:PER')

                state_run = self.instance.query('FETCh:WLAN:SIGN:PER:STATe:ALL?')

                while state_run[:3] != 'RDY':
                    time.sleep(1)
                    state_run = self.instance.query('FETCh:WLAN:SIGN:PER:STATe:ALL?')

                packets_state = self.instance.query('FETCh:WLAN:SIGN:PER?')
                try:
                    packets_done = int(packets_state.split(',')[2])
                    if packets_done < int(packets):
                        global_element.emitsingle.stateupdataSingle.emit(str(packets_done) + 'packets transmited!' + str(packets) + ' not transmit finish, will retry!')
                except:
                    global_element.emitsingle.stateupdataSingle.emit('Call drop, will retry!')
                    packets_done = 0

            per_str = self.instance.query('FETCh:WLAN:SIGN:PER?')
            try:
                ff = per_str.split(',')[1]
                per_result = str(format(eval(per_str.split(',')[1]), '.2f'))
            except:
                per_result = 'NULL'

            return per_result, packets_done

    def off_gprf(self):
        if self.device_name == 'CMW500':
            self.instance.write('SOURce:GPRF:GEN:STATe OFF')

    # 综测仪BT2模块初始化设置
    def bt2_init_setting(self):
        result = True
        try:
            global_element.emitsingle.stateupdataSingle.emit('Initialization of BT Signaling Parameters of CU……')
            if self.device_name == 'CMW500':
                self.instance.write('SYST:RES:ALL')
                time.sleep(3)
                # self.instance.query('*OPC?')

                sys_state = self.instance.query('syst:err?')
                sys_state_int = sys_state.split(',')[0]
                while sys_state_int != '0':
                    time.sleep(1)
                    sys_state = self.instance.query('syst:err?')
                    sys_state_int = sys_state.split(',')[0]

                self.instance.query('ROUT:BLU:MEAS:SCEN:CSP \'Bluetooth Sig1\'; *OPC?')
                time.sleep(0.1)
                self.instance.write('CONF:BLU:MEAS:ISIG:DMODe AUTO')
                time.sleep(0.1)
                self.instance.write('ROUTe:BLU:SIGN:SCENario:OTRX RF1C,RX1,RF1C,TX1')
                self.instance.write('SYSTem:BASE:REF:FREQ:SOURce INTernal')
                self.instance.write('CONF:BLU:SIGN:RFSettings:ENPower 10')
                self.instance.write('CONF:BLU:SIGN:RFSettings:ARANging OFF')
                self.instance.write('CONF:BLU:SIGN:CONN:BDAD:EUT #H123456789012')
                self.instance.write('CONF:BLU:SIGN:CONN:BTYP BR')
                # 打开信号
                bt_signal_state = self.instance.query('SOURce:BLU:SIGN:STATe?')

                if bt_signal_state != 'ON\n':
                    self.instance.write('SOURce:BLU:SIGN:STATe ON')

                while bt_signal_state != 'ON\n':
                    bt_signal_state = self.instance.query('SOURce:BLU:SIGN:STATe?')
                    time.sleep(1)

                self.instance.write('CONF:BLU:SIGN:CONN:BDAD:CMW #H123456123456')
                self.instance.write('CONF:BLU:SIGN:CONN:SVT 8000')
                self.instance.write('CONF:BLU:SIGN:CONN:PAG:PSRMode R0')
                self.instance.write('CONF:BLU:SIGN:CONN:PAG:TOUT 8192')
                self.instance.write('CONF:BLU:SIGN:CONN:INQ:ILENgth 10')
                # self.instance.write('CONF:BLU:SIGN:CONN:INQ:NOResponses 1')
                self.instance.write('CONF:BLU:SIGN:TMOD LOOP')
                self.instance.write('CONF:BLU:SIGN:RFSettings:HOPP OFF')
                self.instance.write('CONF:BLU:SIGN:CONN:PACK:PTYP:BRATe DH1')
                self.instance.write('CONF:BLU:SIGN:CONN:PACK:PLEN:BRATe 27,183,339')
                self.instance.write('CONF:BLU:SIGN:CONN:PACK:PATT:BRATe P44')
                self.instance.write('CONF:BLU:SIGN:RFSettings:CHAN:LOOP 0,0')
                self.instance.write('CONF:BLU:SIGN:CONN:WHIT OFF')
                self.instance.write('CONF:BLU:SIGN:CONN:DELay OFF')

                # 设置初始线损
                cu_dut_loss = global_element.CU_DUT_loss['Loss']['loss'][0]['Value']  # 取第一个loss值作为初始loss
                self.instance.write('CONF:BLU:SIGN:RFS:EATT:OUTP ' + cu_dut_loss)
                self.instance.write('CONF:BLU:SIGN:RFS:EATT:INP ' + cu_dut_loss)

        except:

            result = False

        return result

    # 综测仪BT2模块初始化设置
    def bt2_checkAndconnect(self):
        result = True
        try:
            if self.device_name == 'CMW500':
                self.instance.write('CONF:BLU:SIGN:RFSettings:LEVel -60')
                global_element.emitsingle.stateupdataSingle.emit('BT Connecting,pls wait!')
                state = self.instance.query('FETCH:BLU:SIGN:CONN:STATe?')
                i = 1
                while state != 'TCON\n':
                    time.sleep(0.5)
                    self.instance.write('CALL:BLU:SIGN:CONN:ACT INQ')
                    state = self.instance.query('FETCH:BLU:SIGN:CONN:STATe?')
                    while state != 'SBY\n' and state != 'TCON\n':
                        time.sleep(2)
                        state = self.instance.query('FETCH:BLU:SIGN:CONN:STATe?')

                    inquire_result = self.instance.query('CONF:BLU:SIGN:CONN:INQ:PTARgets:CATalog?')
                    inquire_num = inquire_result.split(',')[0]
                    if inquire_num == '0':
                        if i == 5:
                            global_element.emitsingle.stateupdataSingle.emit("Can't find DUT,pls check DUT and connection "
                                                                             "cable state!")
                            result = False
                            break
                    elif inquire_num == '1':
                        self.instance.write('CALL:BLU:SIGN:CONN:ACT TMConnect')
                        time.sleep(3)
                        state = self.instance.query('FETCH:BLU:SIGN:CONN:STATe?')

                        while state == 'CNNecting:\n':
                            time.sleep(1)
                            state = self.instance.query('FETCH:BLU:SIGN:CONN:STATe?')

                        if state == 'TCON\n':
                            global_element.emitsingle.stateupdataSingle.emit('DUT conncet to CU succeed!')
                            result = True
                            break
                        else:
                            if i == 5:
                                global_element.emitsingle.stateupdataSingle.emit("BT connection is fail!")
                                break
                    elif int(inquire_num) > 1:
                        global_element.emitsingle.stateupdataSingle.emit("Find 2 or more DUTs,pls check!")
                        break
                    i += 1
        except:
            pass

        return result

    # 设置bt2 channel
    def set_bt2_channel(self, channel):
        try:
            if self.device_name == 'CMW500':
                if int(channel) < 39:
                    channel_dl = '78'
                else:
                    channel_dl = '0'
                self.instance.write('CONF:BLU:SIGN:RFS:CHAN:LOOP ' + channel + ',' + channel_dl)
                time.sleep(2)
                sys_state = self.instance.query('syst:err?')
                sys_state_int = sys_state.split(',')[0]
                while sys_state_int != '0':
                    time.sleep(1)
                    sys_state = self.instance.query('syst:err?')
                    sys_state_int = sys_state.split(',')[0]
        except:
            global_element.emitsingle.stateupdataSingle.emit('Error:    Error in setting BT2 Channel for CU!')

    # 设置bt packet type
    def set_bt_parms(self, packettype, hoppingtype):
        try:
            if self.device_name == 'CMW500':
                if packettype[0] == 'D':
                    self.instance.write('CONF:BLU:SIGN:CONN:BTYPe BR')
                    self.instance.write('CONF:BLU:SIGN:CONN:PACK:PTYP:BRAT ' + packettype)
                else:
                    self.instance.write('CONF:BLU:SIGN:CONN:BTYPe EDR')
                    packettype_final = 'E' + packettype[0] + packettype[4] + 'P'
                    self.instance.write('CONF:BLU:SIGN:CONN:PACK:PTYP:EDR ' + packettype_final)

                if hoppingtype == True:
                    self.instance.write('CONF:BLU:SIGN:RFS:HOPP ON')
                else:
                    self.instance.write('CONF:BLU:SIGN:RFS:HOPP OFF')

                self.instance.write('CONF:BLU:SIGN:TMOD LOOP')
                self.instance.write('CONF:BLU:SIGN:CONN:PACK:PATT:BRAT PRBS9')
                self.instance.write('CONF:BLU:MEAS:MEV:RES:ALL OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF')
                self.instance.write('CONF:BLU:MEAS:MEV:RES:PVT ON')

                # 设置为最大功率
                powerstate = self.instance.query('SENS:BLU:SIGN:EUT:PCON:STAT?')
                while powerstate[-4:] != 'MAX\n':
                    time.sleep(0.2)
                    self.instance.write('CONF:BLU:SIGN:CONN:PCON:STEP:ACT UP')
                    time.sleep(0.2)
                    powerstate = self.instance.query('SENS:BLU:SIGN:EUT:PCON:STAT?')



        except:
            global_element.emitsingle.stateupdataSingle.emit('Error:    Error in setting BT parameters of CU!')

    # 设置GSM loss
    def set_bt_loss(self, ul_frequency, dl_frequency):
        ul_min_delta_index = 0
        ul_min_delta = 10000000
        dl_min_delta_index = 0
        dl_min_delta = 10000000
        for i in range(len(global_element.CU_DUT_loss['Loss']['loss'])):
            ul_delta_i = abs(eval(global_element.CU_DUT_loss['Loss']['loss'][i]['Frequency']) - eval(ul_frequency))
            dl_delta_i = abs(eval(global_element.CU_DUT_loss['Loss']['loss'][i]['Frequency']) - eval(dl_frequency))
            if ul_delta_i < ul_min_delta:
                ul_min_delta = ul_delta_i
                ul_min_delta_index = i
            if dl_delta_i < dl_min_delta:
                dl_min_delta = dl_delta_i
                dl_min_delta_index = i

        ul_loss_value = global_element.CU_DUT_loss['Loss']['loss'][ul_min_delta_index]['Value']
        dl_loss_value = global_element.CU_DUT_loss['Loss']['loss'][dl_min_delta_index]['Value']
        if self.device_name == 'CMW500':
            self.instance.write('CONF:BLU:SIGN:RFS:EATT:OUTP ' + ul_loss_value)
            self.instance.write('CONF:BLU:SIGN:RFS:EATT:INP ' + dl_loss_value)

    # 获取LTE 2CA 功率值
    def get_lteca_power(self):
        try:
            result_final = ''
            if self.device_name == 'CMW500':
                self.instance.write('CONFigure:LTE:MEAS:MEValuation:MSUBframes 0,10,3')
                self.instance.write('CONFigure:LTE:SIGN:CONNection:SCC1:TRANsmission TM1')
                self.instance.write('CONFigure:LTE:SIGN:CONNection:TRANsmission TM1')
                self.instance.write('CONFigure:LTE:SIGN:SCC1:UUL ON')
                self.instance.write('CONFigure:LTE:SIGN:SCC1:CAGGregation:MODE INTR')
                self.instance.write('CONFigure:LTE:SIGN:CONNection:SCC1:DCIFormat D1A')
                self.instance.write('CONFigure:LTE:SIGN:CONNection:DCIFormat D1A')
                self.instance.write('CONFigure:LTE:SIGN:CONNection:DLPadding OFF')
                self.instance.write('CONF:LTE:MEAS:MEV:RES:ALL OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF')
                self.instance.write('CONF:LTE:MEAS:MEV:RES:TXM ON')
                self.instance.write('CONF:LTE:MEAS:MEV:RES:SEM ON')
                self.instance.write('TRIGger:LTE:MEAS:MEValuation:SOURce "LTE Sig1: FrameTrigger SCC1"')
                self.instance.write('CONFigure:LTE:MEAS:MEValuation:SCOunt:MODulation 20')
                self.instance.query('CONF:LTE:SIGN:DL:RSEP:LEV -85;*OPC?')
                self.instance.query('CONF:LTE:SIGN:DL:SCC:RSEP:LEV -85;*OPC?')
                # self.instance.query('CONFigure:LTE:SIGN:CONNection:SCC1:STYPe UDCH;*OPC?')
                self.instance.query('CONFigure:LTE:SIGN:CONNection:MCLuster:UL OFF;*OPC?')
                self.instance.write('CONFigure:LTE:MEAS:CAGGregation:MCARrier PCC')
                self.instance.write('CONFigure:LTE:SIGN:UL:PUSCh:TPC:SET MAXP')
                self.instance.write('CONFigure:LTE:SIGN:RFSettings:SCC1:ENPMode ULPC')
                self.instance.write('CONFigure:LTE:SIGN:UL:JUPower ON')
                self.instance.write('CONFigure:LTE:SIGN:RFSettings:SCC1:ENPower 29')
                # self.instance.query('CONFigure:LTE:SIGN:CONNection:STYPe UDCH;*OPC?')
                self.instance.write('CONFigure:LTE:MEAS:CAGGregation:MCARrier PCC')
                self.instance.write('CONF:LTE:MEAS:MEV:RBAL:AUTO ON')
                self.instance.write('CONF:LTE:MEAS:MEV:CTYP AUTO')

                self.instance.query('CONFigure:LTE:SIGN:RFSettings:ENPMode ULPC;*OPC?')
                self.instance.write('CONFigure:LTE:SIGN:RFSettings:ENPower 29')

                self.instance.write('INIT:LTE:MEAS:MEV')
                time.sleep(1)
                run_state = self.instance.query('FETC:LTE:MEAS:MEV:STAT:ALL?')
                while run_state.split(',')[0] != 'RDY':
                    time.sleep(1)
                    run_state = self.instance.query('FETC:LTE:MEAS:MEV:STAT:ALL?')

                result_str = self.instance.query('FETC:LTE:MEAS:MEV:MOD:AVER?')
                result_final = str(format(eval(result_str.split(',')[17]), '.2f'))

        except:
            result_final = 'NULL'

        return result_final

    # 获取LTE 2CA peak to average result
    def get_lteca_ptar(self):
        try:
            result_final = ''
            if self.device_name == 'CMW500':
                self.instance.write('CONFigure:LTE:MEAS:MEValuation:MSUBframes 0,10,3')
                self.instance.write('CONFigure:LTE:SIGN:CONNection:SCC1:TRANsmission TM1')
                self.instance.write('CONFigure:LTE:SIGN:CONNection:TRANsmission TM1')
                self.instance.write('CONFigure:LTE:SIGN:SCC1:UUL ON')
                self.instance.write('CONFigure:LTE:SIGN:SCC1:CAGGregation:MODE INTR')
                self.instance.write('CONFigure:LTE:SIGN:CONNection:SCC1:DCIFormat D1A')
                self.instance.write('CONFigure:LTE:SIGN:CONNection:DCIFormat D1A')
                self.instance.write('CONFigure:LTE:SIGN:CONNection:DLPadding OFF')
                self.instance.write(
                    'CONF:LTE:MEAS:MEV:RES:ALL OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF,OFF')
                self.instance.write('CONF:LTE:MEAS:MEV:RES:TXM ON')
                self.instance.write('CONF:LTE:MEAS:MEV:RES:SEM ON')
                self.instance.write('TRIGger:LTE:MEAS:MEValuation:SOURce "LTE Sig1: FrameTrigger SCC1"')
                self.instance.write('CONFigure:LTE:MEAS:MEValuation:SCOunt:MODulation 20')
                self.instance.query('CONF:LTE:SIGN:DL:RSEP:LEV -85;*OPC?')
                self.instance.query('CONF:LTE:SIGN:DL:SCC:RSEP:LEV -85;*OPC?')
                # self.instance.query('CONFigure:LTE:SIGN:CONNection:SCC1:STYPe UDCH;*OPC?')
                self.instance.query('CONFigure:LTE:SIGN:CONNection:MCLuster:UL OFF;*OPC?')
                self.instance.write('CONFigure:LTE:MEAS:CAGGregation:MCARrier PCC')
                self.instance.write('CONFigure:LTE:SIGN:UL:PUSCh:TPC:SET MAXP')
                self.instance.write('CONFigure:LTE:SIGN:RFSettings:SCC1:ENPMode ULPC')
                self.instance.write('CONFigure:LTE:SIGN:UL:JUPower ON')
                self.instance.write('CONFigure:LTE:SIGN:RFSettings:SCC1:ENPower 29')
                # self.instance.query('CONFigure:LTE:SIGN:CONNection:STYPe UDCH;*OPC?')
                self.instance.write('CONFigure:LTE:MEAS:CAGGregation:MCARrier PCC')
                self.instance.write('CONF:LTE:MEAS:MEV:RBAL:AUTO ON')
                self.instance.write('CONF:LTE:MEAS:MEV:CTYP AUTO')

                self.instance.query('CONFigure:LTE:SIGN:RFSettings:ENPMode ULPC;*OPC?')
                self.instance.write('CONFigure:LTE:SIGN:RFSettings:ENPower 29')

                self.instance.write('INIT:LTE:MEAS:MEV')
                time.sleep(1)
                run_state = self.instance.query('FETC:LTE:MEAS:MEV:STAT:ALL?')
                while run_state.split(',')[0] != 'RDY':
                    time.sleep(1)
                    run_state = self.instance.query('FETC:LTE:MEAS:MEV:STAT:ALL?')

                result_str = self.instance.query('FETC:LTE:MEAS:MEV:MOD:AVER?')
                ave_result = str(format(eval(result_str.split(',')[17]), '.2f'))
                peak_result = str(format(eval(result_str.split(',')[18]), '.2f'))
                result_final = str(format(eval(peak_result) - eval(ave_result), '.2f'))
        except:
            result_final = 'NULL'

        return result_final

    # 检查LTE CA连接状态
    def check_ca_connect_state(self):
        check_state = False
        try:
            if self.device_name == 'CMW500':
                # 释放连接再重连，确认是否还能连接
                self.instance.write('CALL:LTE:SIGN:PSW:ACT DISC')
                time.sleep(2)
                self.instance.write('CALL:LTE:SIGN:PSW:ACT CONN')
                time.sleep(4)

                connect_state = self.instance.query('FETC:LTE:SIGN:PSW:STAT?')
                if connect_state != 'CEST\n':
                    time.sleep(10)
                    connect_state = self.instance.query('FETC:LTE:SIGN:PSW:STAT?')
                    if connect_state == 'ON\n':
                        issync = self.check_dut_issync_lte()
                        if issync == True:
                            call_state = self.ltecacallsetup()
                            if call_state == True:
                                self.instance.write('CALL:LTE:SIGN:SCC:ACT MAC')
                                check_state = True
                    elif connect_state == 'ATT\n':
                        call_state = self.ltecacallsetup()
                        if call_state == True:
                            self.instance.write('CALL:LTE:SIGN:SCC:ACT MAC')
                            check_state = True
                    elif connect_state == 'CEST\n':
                        self.instance.write('CALL:LTE:SIGN:SCC:ACT MAC')
                        check_state = True

                else:
                    self.instance.write('CALL:LTE:SIGN:SCC:ACT MAC')
                    check_state = True

                return check_state
        except:
            global_element.emitsingle.statetimeupdataSingle.emit('Error:    CU check DUT connect state method'
                                                                 ' exception!')
