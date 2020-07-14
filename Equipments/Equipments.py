# !/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Author    : Feng Zhaohui
# @Time      : 2019/2/22
# @File      : Equipments.py
# @Funcyusa  :
# @Version   : 1.0


import visa
from Equipments import CU, PS, SA
import global_element
import time


def scandevice():
    """
        通过visa扫描仪器
    :return: 仪器idn列表和地址列表
    """
    visaDLL = 'visa32.dll'
    list_address = []
    list_device_idn = []
    rm = visa.ResourceManager(visaDLL)
    device_list = rm.list_resources()
    if len(device_list) > 0:
        for i in device_list:
            try:
                inst = rm.open_resource(i)
                idn = inst.query('*IDN?')
                list_device_idn.append(idn)
                list_address.append(i)
            except:
                pass
    return list_device_idn, list_address


# 初始化已勾选的设备
def init_devices_checked():
    global_element.emitsingle.stateupdataSingle.emit('Instrument Initialization…………')
    for device in global_element.devices_config_dict['xml'].items():
        if device[1]['CHECK'] == 'True':
            device_type = device[0]
            device_name = device[1]['NAME']
            device_addr_type = device[1]['ADDRESSTYPE']
            device_addr = device[1]['ADDRESS']

            if device_type == 'CU':
                global_element.emitsingle.stateupdataSingle.emit('Initialization of CU…………')
                time.sleep(2)
                intance_CU = CU.VisaCU(device_name, device_addr, device_addr_type)
                try:
                    intance_CU.open()
                    cu_idn = intance_CU.read_idn()
                    global_element.emitsingle.stateupdataSingle.emit('%s Initialization of the CU is successful!' % cu_idn)
                    global_element.CU_intance = intance_CU                            # 初始化成功后将实例保存到全局变量中，以便调用
                except:
                    global_element.emitsingle.thread_exitSingle.emit('The CU initialization failed!')
                    time.sleep(0.1)
            elif device_type == 'SA':
                global_element.emitsingle.stateupdataSingle.emit('SA Initialization…………')
                time.sleep(2)
                intance_SA = SA.VisaSA(device_name, device_addr, device_addr_type)
                try:
                    intance_SA.open()
                    sa_idn = intance_SA.read_idn()
                    global_element.emitsingle.stateupdataSingle.emit('%s SA initialization success!' % sa_idn)
                    global_element.SA_intance = intance_SA
                except:
                    global_element.emitsingle.thread_exitSingle.emit('Initialization Failure of SA!')
                    time.sleep(0.1)
            elif device_type == 'ESG':
                global_element.emitsingle.stateupdataSingle.emit('ESG initialization…………')
                global_element.emitsingle.thread_exitSingle.emit('ESG is not supported yet!')
                time.sleep(0.1)
            elif device_type == 'PSG':
                global_element.emitsingle.stateupdataSingle.emit('PSG initialization…………')
                global_element.emitsingle.thread_exitSingle.emit('PSG is not supported yet!')
                time.sleep(0.1)
            elif device_type == 'PS':
                global_element.emitsingle.stateupdataSingle.emit('Initialization of DC Power Supply…………')
                time.sleep(2)
                intance_PS = PS.VisaPS(device_name, device_addr, device_addr_type)
                try:
                    intance_PS.open()
                    ps_idn = intance_PS.read_idn()
                    global_element.emitsingle.stateupdataSingle.emit('%s Initialization of DC power supply is '
                                                                     'successful!' % ps_idn)
                    global_element.PS_intance = intance_PS
                except:
                    global_element.emitsingle.thread_exitSingle.emit('Initialization failure of DC power supply!')
                    time.sleep(0.1)
            elif device_type == 'SU':
                global_element.emitsingle.stateupdataSingle.emit('SU initialization…………')
                global_element.emitsingle.thread_exitSingle.emit('SU is not supported yet!')
                time.sleep(0.1)
