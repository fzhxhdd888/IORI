# !/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Author    : Feng Zhaohui
# @Time      : 2019/3/19
# @File      : DUTcontrol.py
# @Funcyusa  :
# @Version   : 1.0

import global_element
import win32api
# from serial import Serial
import time
import serial.tools.list_ports
# import hashlib


# 查找端口
def findPort():
    ports = serial.tools.list_ports.comports()
    for each in ports:
        return str(each)


# 发送AT OFF指令
def sendAT_off(port):
    state = True
    global_element.emitsingle.stateupdataSingle.emit('Send AT command: Close……')
    try:
        comport = 'COM' + str(eval(port) + 1)
        ser = serial.Serial(port=comport, baudrate=9600, timeout=3)
        ser.write(b'AT+CFUN=0\r\n')
        ser.close()
    except:
        state = False

    if state == False:
        try:
            comport = 'COM' + str(eval(port) - 1)
            ser = serial.Serial(port=comport, baudrate=9600, timeout=3)
            ser.write(b'AT+CFUN=0\r\n')
            ser.close()
        except:
            global_element.emitsingle.stateupdataSingle.emit('Error:    Error sending AT command!')


# 发送AT ON指令
def sendAT_on(port):
    state = True
    global_element.emitsingle.stateupdataSingle.emit('Send AT command: Open……')
    try:
        comport = 'COM' + str(eval(port) + 1)
        ser = serial.Serial(port=comport, baudrate=9600, timeout=3)
        ser.write(b'AT+CFUN=1\r\n')
        ser.close()
    except:
        state = False

    if state == False:
        try:
            comport = 'COM' + str(eval(port) - 1)
            ser = serial.Serial(port=comport, baudrate=9600, timeout=3)
            ser.write(b'AT+CFUN=1\r\n')
            ser.close()
        except:
            global_element.emitSingle.stateupdataSingle.emit('Error:    Error sending AT command!')


def duton():
    """
    打开待测样机方法定义
    :return:
    """
    dut_control_type = global_element.active_dut_dict['xml']['DUTCONFIG']['AUTOMODE']
    if dut_control_type == '1':
       win32api.MessageBox(0, 'Please manually power on DUT to be tested!', 'Tip')
    elif dut_control_type == '2':
        global_element.PS_intance.Outputon()
    elif dut_control_type == '3':
        port = global_element.active_dut_dict['xml']['DUTCONFIG']['COMPORT']
        sendAT_on(port)
    else:
        global_element.emitsingle.thread_exitSingle.emit('Please choose the correct cellular test DUT automatic mode')


def dutoff():
    """
    关闭待测样机方法定义
    :return:
    """
    dut_control_type = global_element.active_dut_dict['xml']['DUTCONFIG']['AUTOMODE']
    if dut_control_type == '1':
       win32api.MessageBox(0, 'Please power off DUT to be tested manually!', 'Tip')
    elif dut_control_type == '2':
        global_element.PS_intance.Outputoff()
    elif dut_control_type == '3':
        port = global_element.active_dut_dict['xml']['DUTCONFIG']['COMPORT']
        sendAT_off(port)
    else:
        global_element.emitsingle.thread_exitSingle.emit('Please choose the correct cellular test DUT automatic mode')


def dutoffon():
    """
    重启待测样机方法定义
    :return:
    """
    dut_control_type = global_element.active_dut_dict['xml']['DUTCONFIG']['AUTOMODE']
    if dut_control_type == '1':
       win32api.MessageBox(0, 'Please manually restart DUT to be tested!', 'Tip')
    elif dut_control_type == '2':
        global_element.PS_intance.Outputoffon(global_element.Test_volt, global_element.active_dut_dict['xml']['DUTCONFIG']['MAXC'])
    elif dut_control_type == '3':
        port = global_element.active_dut_dict['xml']['DUTCONFIG']['COMPORT']
        sendAT_off(port)
        time.sleep(5)
        sendAT_on(port)
    else:
        global_element.emitsingle.thread_exitSingle.emit('Please choose the correct cellular test DUT automatic mode')


