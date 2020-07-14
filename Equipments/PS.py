# !/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Author    : Feng Zhaohui
# @Time      : 2019/2/22
# @File      : PS.py
# @Funcyusa  :
# @Version   : 1.0

import visa
import time
import global_element


class VisaPS(object):
    """
        直流电源类构建
        定义直流电源的类函数和参数
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

    def open(self):
        self.instance = self.resourceManager.open_resource(self.address)

    def close(self):
        if self.instance is not None:
            self.instance.close()
            self.instance = None

    def read_idn(self):
        idn = self.instance.query('*IDN?')
        return idn

    # 设置电压及限流，并重启电源
    def Outputoffon(self, volt, curr):
        if self.device_name == 'E3632A':
            global_element.emitsingle.stateupdataSingle.emit('Restart DUT……')
            self.instance.write('OUTP OFF')
            time.sleep(2)
            self.instance.write('VOLT ' + volt)
            self.instance.write('CURR ' + curr)
            self.instance.write('OUTP ON')

    # 设置电压及限流，并关闭电源
    def Outputoff(self):
        if self.device_name == 'E3632A':
            global_element.emitsingle.stateupdataSingle.emit('Power off DUT')
            self.instance.write('OUTP OFF')
