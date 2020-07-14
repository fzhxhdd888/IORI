# !/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Author    : Feng Zhaohui
# @Time      : 2019/2/22
# @File      : global_element.py
# @Funcyusa  :
# @Version   : 1.0

from xml.etree import ElementTree
import xmltodict
import time
import os
from PyQt5.QtCore import pyqtSignal, QObject
from Equipments import CU, PS, SA
import testseq_handle
import cv2


DEVICECONFIGXMLPATH = 'Config/Devices Config.xml'  # 仪器配置文件路径
DUTCONFIGXMLPATH = 'Config/DUT Config/'            # DUT配置文件路径
DEFUALTCONFIGXMLPATH = 'Config/Default Config/'
TESTITEMSCONFIGPATH = 'Config/Default Config/Test Items Config/'

reportpath = ''                                    # 用于存放用户定义的报告路径


total_step = 0                                     # 记录总步数
finished_step = 0                                  # 记录已完成步数
finished_result_list = [0, 0, 0]                   # 记录已完成的步数中有多少PASS，多少FAIL，多少INCONCLUSIVE

current_index_seq = -1                             # 用于记录目前测试seq的index

Test_type = ''                                     # 用于存放测试的模块类型，以便初始化report格式
Test_case = ''                                     # 用于存放测试项，以便生成report时调用
Test_item = ''                                     # 用于存放测试子项，以便生成report时调用
Test_band = ''                                     # 用于存放测试band，以便生成report时调用
Test_channel = ''                                  # 用于存放测试channel，以便生成report时调用
Test_pcl = ''                                      # 用于存放测试GSM时的PCL,以便生成report时调用（only for GSM）
Test_modulation = ''                               # 用于存放测试项的调制方式，以便生成report时调用
Test_temp = ''                                     # 用于存放测试项的温度条件，以便生成report时调用
Test_volt = ''                                     # 用于存放测试项的电压条件，以便生成report时调用
Test_remark = ''                                   # 用于存放测试项的附加的信息，以便生成report时调用
Test_bslevel = ''                                  # 用于存放基站电平
Test_lte_bandwidth = ''                            # 用于存放LTE的Bandwidth (only for LTE)
Test_lte_RB = ''                                   # 用于存放lte 的RB信息
Test_Antenna = ''                                  #
Test_Datarate = ''
Test_wlan_bw = ''
Test_bt_packetype = ''

# BT2 FCC 全局变量
BT2_number_of_channel_istested = False
BT2_dwelltime_istested = False
BT2_fcc_20dbbw_result = {'0_DH5': '', '0_2-DH5': '', '0_3-DH5': '', '39_DH5': '', '39_2-DH5': '', '39_3-DH5': '',
                         '78_DH5': '', '78_2-DH5': '', '78_3-DH5': ''}

CU_DUT_loss = {}                                   # 用于存放CU -> DUT的路径损耗字典数据
CU_DUT_loss_file = ''                              # 用于存放CU -> DUT的路径损耗文件路径
SA_DUT_loss = {}                                   # 用于存放SA -> DUT的路径损耗字典数据
SA_DUT_loss_file = ''                              # 用于存放SA -> DUT的路径损耗文件路径
ESG_DUT_loss = {}                                   # 用于存放SA -> DUT的路径损耗字典数据
ESG_DUT_loss_file = ''                              # 用于存放SA -> DUT的路径损耗文件路径

testseq_final_result = 'Passed'                    # 存放每条test case的测试结果,用于更新主界面Judgement
testseq_judgement_list = []                        # 存放每条test case中每条item测试结果,用于得出最终testseq_final_result
reporthandle_dict = {}                             # 存放用户定义的报告生成信息

fcc_gsm_wcdma_pta_judgement = 'Passed'
fcc_gsm_wcdma_bandedge_judgement = 'Passed'
fcc_gsm_wcdma_cse_judgement = 'Passed'
fcc_gsm_wcdma_erp_judgement = 'Passed'


class emitSingle(QObject):
    reportupdataSingle = pyqtSignal(list)           # report更新时发出的QT信号，用来更新界面数据
    thread_exitSingle = pyqtSignal(str)             # 测试线程退出信号
    stateupdataSingle = pyqtSignal(str)             # 更新状态窗口信号
    starttimeupdateSingle = pyqtSignal(int, str)    # 更新主界面开始时间的信号
    stoptimeupdateSingle = pyqtSignal(int, str)     # 更新主界面结束时间的信号
    judgementupdataSingle = pyqtSignal(int, str)    # 更新主界面Judgement的信号
    timedeltaupdataSingle = pyqtSignal(int, str)    # 更新主界面用时的信号
    statetimeupdataSingle = pyqtSignal(str)         # 更新状态窗口倒计时信号
    process_rateupdataSingle = pyqtSignal(str)      # 更新测试进度信号
    summaryupdataSingle = pyqtSignal(list)          # 更新summry


emitsingle = emitSingle()                          # 实例化发射信号类，以便其它线程调用

IsPause = False                                    # 用来判断是否已选择暂停
IsStop = False                                     # 用来判断是否已选择停止测试

devices_config_dict = {}                           # 仪器配置保存字典（用于测试时调用）
CU_intance = CU.VisaCU('', '', '')                 # 用于存放实例化仪器
SA_intance = SA.VisaSA('', '', '')
PS_intance = PS.VisaPS('', '', '')

dut_config_list = []                               # DUT Config文件列表
dut_config_items_list = []                         # DUT Config界面DUT列表
current_dut_dict = {}                              # 此字典用于存放选中DUT xml文件数据的导入，用于更新窗体右侧控件内容
active_dut_dict = {}
active_dut_name = ''

Test_items_default_config_dict = []                # 此列表用于暂存导入模块xml文件的信息
Testsequence_dict = {'seq': {'items': []}}         # 此字典初始化testseq窗口，保存测试需要调用的参数
Testseq_list = []                                  # 用于用户保存自定义测试计划testseq
Testplan_list = []                                 # 此列表用于暂存用户定义的testplan

editplan_dict = {}                                 # 此字典用于暂存需要编辑的testplan字典
Testitemparms_list = []                            # 此列表或字典用于暂存处于编辑状态的test item的parms
Testitemparms_dict = {}
Testitemlimts_list = []                            # 此列表或字典用于暂存处于编辑状态的test item的limits
Testitemlimts_dict = {}
Testitemparmslimits_state = [0, 0]                 # 此列表存储处于编辑状态的test item是否有可编辑的parms和Limits，
                                                   # 0：没有，1：有1个参数（字典类型），2：有多于1个的参数（列表类型）


def dict_to_xmlstr(data, filename):
    ff = xmltodict.unparse(data)
    f = open(filename, 'w', encoding='utf-8')
    f.write(ff)
    f.close()
    tree = ElementTree.parse(filename)
    root = tree.getroot()
    prettyXml(root, '\t', '\n')
    tree.write(filename, encoding='utf-8')


# 字典转xml功能函数********************************************************************************************
def dict_to_xml(data, filename):
    def to_xml(data):
        xx = []
        for k, v in data.items():
            if isinstance(v, dict):
                aa = to_xml(v)
                s = '<{key}>{value}</{key}>'.format(key=k, value=aa)
            else:
                s = '<{key}>{value}</{key}>'.format(key=k, value=v)
            xx.append(s)
        return ''.join(xx)
    # return '<xml>'+to_xml(data)+'</xml>'
    xml_data = '<xml>'+to_xml(data)+'</xml>'
    f = open(filename, 'w', encoding='utf-8')
    f.write(xml_data)
    f.close()
    tree = ElementTree.parse(filename)
    root = tree.getroot()
    prettyXml(root, '\t', '\n')
    tree.write(filename, encoding='utf-8')


# 美化xml文件格式************************************************************************************************
def prettyXml(element, indent, newline, level=0):  # element为传进来的elment类，
    if element:
        if element.text == None or element.text.isspace():
            element.text = newline + indent * (level + 1)
        else:
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
    # else:  # 此两行取消注释可以把元素的内容单独成行
    #     element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level

    temp = list(element)
    for subelement in temp:
        if temp.index(subelement) < (len(temp) - 1):
            subelement.tail = newline + indent * (level + 1)
        else:
            subelement.tail = newline + indent * level
        prettyXml(subelement, indent, newline, level=level + 1)


# 将xml文件转换成dict*****************************************************************************************
def xml_to_dict(filename):
    with open(filename, encoding='utf-8') as fd:
        doc = xmltodict.parse(fd.read())
    return doc


# 把字符串转为布尔***************************************************************************************
def str_to_bool(str):
    return True if str.lower() == 'true' else False


# 遍历文件夹下所有文件名********************************************************************************
def ergodic_dir(dir_path):
    filename_fianl_list = []
    filename_list = os.listdir(dir_path)
    for i in filename_list:
        i = i[:-4]
        filename_fianl_list.append(i)
    return filename_fianl_list


# 实现暂停功能
def pausefuction():
    while IsPause:
        time.sleep(1)


# 实现停止功能
def is_stop():
    if IsStop == True:
        emitsingle.thread_exitSingle.emit('User terminates the test!')


# 检查仪器勾选状态
def checkdeviceenable():
    check_device_state = False
    # 检查是否有至少一台仪器勾选
    for item in devices_config_dict['xml'].items():
        if item[1]['CHECK'] == 'True':
            check_device_state = True
            break

    # 如果没有一台处于勾选，发射退出线程信号
    if check_device_state == False:
        emitsingle.thread_exitSingle.emit('Error:   No instrument is checked in the instrument configuration!')
        time.sleep(0.1)


# 检查是否有选择loss文件
def checklossfileselected():
    if CU_DUT_loss_file == '':
        emitsingle.thread_exitSingle.emit('Error:   No path loss file was configured!')
        time.sleep(0.1)


# 检查是否有选择报告保存的路径
def checkreportpath():
    if reportpath == '':
        emitsingle.thread_exitSingle.emit('Error:   Reporting path error!')
        time.sleep(0.1)


# 检查是否有选择DUT
def checkdutactive():
    if active_dut_dict == {}:
        emitsingle.thread_exitSingle.emit('Error:   No DUT was activated!')
        time.sleep(0.1)


# 检查测试序列是否有内容
def checktestseq():
    if len(Testsequence_dict['seq']['items']) == 0:
        emitsingle.thread_exitSingle.emit('Error:   There is nothing in the test sequence!')
        time.sleep(0.1)


# 粗略计算测试总步骤，用于显示测试进度
def calc_total_step():
    sum_step = 0
    for i in range(len(Testsequence_dict['seq']['items'])):
        if Testsequence_dict['seq']['items'][i]['@enable'] == 'yes':
            mode_name = Testsequence_dict['seq']['items'][i]['@name'].split(' ')[0]
            if mode_name == 'GSM' or mode_name == 'GSMFCC':
                GSM_band = Testsequence_dict['seq']['items'][i]['item'][0]['parms']['Parm'][0]['Value']
                if GSM_band == 'GSM850':
                    GSM_channel = Testsequence_dict['seq']['items'][i]['item'][0]['parms']['Parm'][1]['Value']
                elif GSM_band == 'GSM900':
                    GSM_channel = Testsequence_dict['seq']['items'][i]['item'][0]['parms']['Parm'][2]['Value']
                elif GSM_band == 'DCS1800':
                    GSM_channel = Testsequence_dict['seq']['items'][i]['item'][0]['parms']['Parm'][3]['Value']
                else:
                    GSM_channel = Testsequence_dict['seq']['items'][i]['item'][0]['parms']['Parm'][4]['Value']
                GSM_channel_list = testseq_handle.channelstrtolist(GSM_channel)
                GSM_pcl = Testsequence_dict['seq']['items'][i]['item'][0]['parms']['Parm'][5]['Value']
                GSM_pcl_list = testseq_handle.channelstrtolist(GSM_pcl)
                items_count = 0
                for item_index in range(1, len(Testsequence_dict['seq']['items'][i]['item'])):
                    if Testsequence_dict['seq']['items'][i]['item'][item_index]['@enable'] == 'yes':
                        items_count += 1
                test_step = len(GSM_channel_list) * len(GSM_pcl_list) * items_count
                sum_step += test_step
            elif mode_name == 'WCDMA' or mode_name == 'WCDMAFCC':
                WCDMA_band = Testsequence_dict['seq']['items'][i]['item'][0]['parms']['Parm'][0]['Value']
                if WCDMA_band == 'Band II':
                    WCDMA_channel = Testsequence_dict['seq']['items'][i]['item'][0]['parms']['Parm'][1]['Value']
                elif WCDMA_band == 'Band IV':
                    WCDMA_channel = Testsequence_dict['seq']['items'][i]['item'][0]['parms']['Parm'][2]['Value']
                elif WCDMA_band == 'Band V':
                    WCDMA_channel = Testsequence_dict['seq']['items'][i]['item'][0]['parms']['Parm'][3]['Value']
                WCDMA_channel_list = testseq_handle.channelstrtolist(WCDMA_channel)
                items_count = 0
                for item_index in range(1, len(Testsequence_dict['seq']['items'][i]['item'])):
                    if Testsequence_dict['seq']['items'][i]['item'][item_index]['@enable'] == 'yes':
                        items_count += 1
                test_step = len(WCDMA_channel_list) * items_count
                sum_step += test_step
            elif mode_name == 'LTE' or mode_name == 'LTEFCC':
                band = Testsequence_dict['seq']['items'][i]['item'][0]['parms']['Parm'][0]['Value']
                bw = Testsequence_dict['seq']['items'][i]['item'][0]['parms']['Parm'][1]['Value']
                lte_channel = lte_channel_fortest_dict[bw][band]
                lte_channel_list = testseq_handle.channelstrtolist(lte_channel)
                items_count = 0
                for item_index in range(1, len(Testsequence_dict['seq']['items'][i]['item'])):
                    if Testsequence_dict['seq']['items'][i]['item'][item_index]['@enable'] == 'yes':
                        items_count += 1
                test_step = len(lte_channel_list) * items_count
                sum_step += test_step
            elif mode_name == 'LTECAFCC':
                band = Testsequence_dict['seq']['items'][i]['item'][0]['parms']['Parm'][0]['Value']
                dict_bw_channel = lte_ca_channel_fortest_dict[band]
                channel_count_total = 0
                for index, key in enumerate(dict_bw_channel):
                    if dict_bw_channel[key] != '':
                        channel_count = len(dict_bw_channel[key].split(','))
                        channel_count_total += channel_count
                items_count = 0
                for item_index in range(1, len(Testsequence_dict['seq']['items'][i]['item'])):
                    if Testsequence_dict['seq']['items'][i]['item'][item_index]['@enable'] == 'yes':
                        items_count += 1
                test_step = channel_count_total * items_count
                sum_step += test_step
            elif mode_name == 'WLAN_B':

                WLAN_channel = Testsequence_dict['seq']['items'][i]['item'][0]['parms']['Parm'][2]['Value']
                WLAN_channel_list = testseq_handle.channelstrtolist(WLAN_channel)
                items_count = 0
                for item_index in range(1, len(Testsequence_dict['seq']['items'][i]['item'])):
                    if Testsequence_dict['seq']['items'][i]['item'][item_index]['@enable'] == 'yes':
                        items_count += 1
                test_step = len(WLAN_channel_list) * items_count
                sum_step += test_step
            elif mode_name == 'WLAN_AC':
                WLAN_bw = Testsequence_dict['seq']['items'][i]['item'][0]['parms']['Parm'][3]['Value']
                if WLAN_bw == 'VHT20':
                    WLAN_channel = Testsequence_dict['seq']['items'][i]['item'][0]['parms']['Parm'][4]['Value']
                elif WLAN_bw == 'VHT40':
                    WLAN_channel = Testsequence_dict['seq']['items'][i]['item'][0]['parms']['Parm'][5]['Value']
                elif WLAN_bw == 'VHT80':
                    WLAN_channel = Testsequence_dict['seq']['items'][i]['item'][0]['parms']['Parm'][6]['Value']
                WLAN_channel_list = testseq_handle.channelstrtolist(WLAN_channel)
                items_count = 0
                for item_index in range(1, len(Testsequence_dict['seq']['items'][i]['item'])):
                    if Testsequence_dict['seq']['items'][i]['item'][item_index]['@enable'] == 'yes':
                        items_count += 1
                test_step = len(WLAN_channel_list) * items_count
                sum_step += test_step
            elif mode_name == 'BT2FCC':

                BT2FCC_channel = Testsequence_dict['seq']['items'][i]['item'][0]['parms']['Parm']['Value']
                BT2FCC_channel_list = testseq_handle.channelstrtolist(BT2FCC_channel)
                items_count = 0
                for item_index in range(1, len(Testsequence_dict['seq']['items'][i]['item'])):
                    if Testsequence_dict['seq']['items'][i]['item'][item_index]['@enable'] == 'yes':
                        items_count += 1
                test_step = len(BT2FCC_channel_list) * items_count
                sum_step += test_step

    return sum_step


def power(x, n):
    s = 1
    while n > 0:
        n = n - 1
        s = s * x

    return s


#  擦除图片不需要的部分
def image_handle(path_image):
    img = cv2.imread(path_image)
    img[0:220, 1:80] = (255, 255, 255)
    time.sleep(1)
    cv2.imwrite(path_image, img)


lte_channel_fortest_dict = {'1.4MHz':                                            # 用于存放lte channel的默认值
                                {'FDD-LTE 1': '',
                                 'FDD-LTE 2': '18607,18900,19193',
                                 'FDD-LTE 3': '19207,19575,19943',
                                 'FDD-LTE 4': '19957,20175,20393',
                                 'FDD-LTE 5': '20407,20525,20643',
                                 'FDD-LTE 6': '',
                                 'FDD-LTE 7': '',
                                 'FDD-LTE 8': '21457,21625,21793',
                                 'FDD-LTE 9': '',
                                 'FDD-LTE 10': '',
                                 'FDD-LTE 11': '',
                                 'FDD-LTE 12': '23017,23095,23173',
                                 'FDD-LTE 13': '',
                                 'FDD-LTE 14': '',
                                 'FDD-LTE 17': '',
                                 'FDD-LTE 18': '',
                                 'FDD-LTE 19': '',
                                 'FDD-LTE 20': '',
                                 'FDD-LTE 21': '',
                                 'FDD-LTE 22': '',
                                 'FDD-LTE 23': '25507,25600,25693',
                                 'FDD-LTE 24': '',
                                 'FDD-LTE 25': '26047,26365,26683',
                                 'FDD-LTE 26': '26697,26865,27033',
                                 'FDD-LTE 27': '27047,27125,27203',
                                 'FDD-LTE 28': '',
                                 'FDD-LTE 30': '',
                                 'FDD-LTE 31': '27767,27785,27803',
                                 'TDD-LTE 33': '',
                                 'TDD-LTE 34': '',
                                 'TDD-LTE 35': '36357,36650,36943',
                                 'TDD-LTE 36': '36957,37250,37543',
                                 'TDD-LTE 37': '',
                                 'TDD-LTE 38': '',
                                 'TDD-LTE 39': '',
                                 'TDD-LTE 40': '',
                                 'TDD-LTE 41': '',
                                 'TDD-LTE 42': '',
                                 'TDD-LTE 43': '',
                                 'TDD-LTE 44': '',
                                 'TDD-LTE 45': '',
                                 'TDD-LTE 46': '',
                                 'TDD-LTE 47': ''},
                            '3MHz':
                                {'FDD-LTE 1': '',
                                 'FDD-LTE 2': '18615,18900,19185',
                                 'FDD-LTE 3': '19215,19575,19935',
                                 'FDD-LTE 4': '19965,20175,20385',
                                 'FDD-LTE 5': '20415,20525,20635',
                                 'FDD-LTE 6': '',
                                 'FDD-LTE 7': '',
                                 'FDD-LTE 8': '21465,21625,21785',
                                 'FDD-LTE 9': '',
                                 'FDD-LTE 10': '',
                                 'FDD-LTE 11': '',
                                 'FDD-LTE 12': '23025,23095,23165',
                                 'FDD-LTE 13': '',
                                 'FDD-LTE 14': '',
                                 'FDD-LTE 17': '',
                                 'FDD-LTE 18': '',
                                 'FDD-LTE 19': '',
                                 'FDD-LTE 20': '',
                                 'FDD-LTE 21': '',
                                 'FDD-LTE 22': '',
                                 'FDD-LTE 23': '25515,25600,25685',
                                 'FDD-LTE 24': '',
                                 'FDD-LTE 25': '26055,26365,26675',
                                 'FDD-LTE 26': '26705,26865,27025',
                                 'FDD-LTE 27': '27055,27125,27195',
                                 'FDD-LTE 28': '27225,27435,27645',
                                 'FDD-LTE 30': '',
                                 'FDD-LTE 31': '27775,27785,27795',
                                 'TDD-LTE 33': '',
                                 'TDD-LTE 34': '',
                                 'TDD-LTE 35': '36365,36650,36935',
                                 'TDD-LTE 36': '36965,37250,37535',
                                 'TDD-LTE 37': '',
                                 'TDD-LTE 38': '',
                                 'TDD-LTE 39': '',
                                 'TDD-LTE 40': '',
                                 'TDD-LTE 41': '',
                                 'TDD-LTE 42': '',
                                 'TDD-LTE 43': '',
                                 'TDD-LTE 44': '45605,46090,46575',
                                 'TDD-LTE 45': '',
                                 'TDD-LTE 46': '',
                                 'TDD-LTE 47': ''},
                            '5MHz':
                                {'FDD-LTE 1': '18025,18300,18575',
                                 'FDD-LTE 2': '18625,18900,19175',
                                 'FDD-LTE 3': '19225,19575,19925',
                                 'FDD-LTE 4': '19975,20175,20375',
                                 'FDD-LTE 5': '20425,20525,20625',
                                 'FDD-LTE 6': '20675,20700,20725',
                                 'FDD-LTE 7': '20775,21100,21425',
                                 'FDD-LTE 8': '21475,21625,21775',
                                 'FDD-LTE 9': '21825,21975,22125',
                                 'FDD-LTE 10': '22175,22450,22725',
                                 'FDD-LTE 11': '22775,22850,22925',
                                 'FDD-LTE 12': '23035,23095,23155',
                                 'FDD-LTE 13': '23205,23230,23255',
                                 'FDD-LTE 14': '23305,23330,23355',
                                 'FDD-LTE 17': '23755,23790,23825',
                                 'FDD-LTE 18': '23875,23925,23975',
                                 'FDD-LTE 19': '24025,24075,24125',
                                 'FDD-LTE 20': '24175,24300,24425',
                                 'FDD-LTE 21': '24475,24525,24575',
                                 'FDD-LTE 22': '24625,25000,25375',
                                 'FDD-LTE 23': '25525,25600,25675',
                                 'FDD-LTE 24': '25725,25870,26015',
                                 'FDD-LTE 25': '26065,26365,26665',
                                 'FDD-LTE 26': '26715,26865,27015',
                                 'FDD-LTE 27': '27065,27125,27185',
                                 'FDD-LTE 28': '27235,27435,27635',
                                 'FDD-LTE 30': '27685,27710,27735',
                                 'FDD-LTE 31': '27785',
                                 'TDD-LTE 33': '36025,36100,36175',
                                 'TDD-LTE 34': '36225,36275,36325',
                                 'TDD-LTE 35': '36375,36650,36925',
                                 'TDD-LTE 36': '36975,37250,37525',
                                 'TDD-LTE 37': '37575,37650,37725',
                                 'TDD-LTE 38': '37775,38000,38225',
                                 'TDD-LTE 39': '38275,38450,38625',
                                 'TDD-LTE 40': '38675,39150,39625',
                                 'TDD-LTE 41': '39675,40620,41565',
                                 'TDD-LTE 42': '41615,42590,43565',
                                 'TDD-LTE 43': '43615,44590,45565',
                                 'TDD-LTE 44': '45615,46090,46565',
                                 'TDD-LTE 45': '46615,46690,46765',
                                 'TDD-LTE 46': '',
                                 'TDD-LTE 47': ''},
                            '10MHz':
                                {'FDD-LTE 1': '18050,18300,18550',
                                 'FDD-LTE 2': '18650,18900,19150',
                                 'FDD-LTE 3': '19250,19575,19900',
                                 'FDD-LTE 4': '20000,20175,20350',
                                 'FDD-LTE 5': '20450,20525,20600',
                                 'FDD-LTE 6': '20700',
                                 'FDD-LTE 7': '20800,21100,21400',
                                 'FDD-LTE 8': '21500,21625,21750',
                                 'FDD-LTE 9': '21850,21975,22100',
                                 'FDD-LTE 10': '22200,22450,22700',
                                 'FDD-LTE 11': '22800,22850,22900',
                                 'FDD-LTE 12': '23060,23095,23130',
                                 'FDD-LTE 13': '23230',
                                 'FDD-LTE 14': '23330',
                                 'FDD-LTE 17': '23780,23790,23800',
                                 'FDD-LTE 18': '23900,23925,23950',
                                 'FDD-LTE 19': '24050,24075,24100',
                                 'FDD-LTE 20': '24200,24300,24400',
                                 'FDD-LTE 21': '24500,24525,24550',
                                 'FDD-LTE 22': '24650,25000,25350',
                                 'FDD-LTE 23': '25550,25600,25650',
                                 'FDD-LTE 24': '25750,25870,25990',
                                 'FDD-LTE 25': '26090,26365,26640',
                                 'FDD-LTE 26': '26740,26865,26990',
                                 'FDD-LTE 27': '27090,27125,27160',
                                 'FDD-LTE 28': '27260,27435,27610',
                                 'FDD-LTE 30': '27710',
                                 'FDD-LTE 31': '',
                                 'TDD-LTE 33': '36050,36100,36150',
                                 'TDD-LTE 34': '36250,36275,36300',
                                 'TDD-LTE 35': '36400,36650,36900',
                                 'TDD-LTE 36': '37000,37250,37500',
                                 'TDD-LTE 37': '37600,37650,37700',
                                 'TDD-LTE 38': '37800,38000,38200',
                                 'TDD-LTE 39': '38300,38450,38600',
                                 'TDD-LTE 40': '38700,39150,39600',
                                 'TDD-LTE 41': '39700,40620,41540',
                                 'TDD-LTE 42': '41640,42590,43540',
                                 'TDD-LTE 43': '43640,44590,45540',
                                 'TDD-LTE 44': '45640,46090,46540',
                                 'TDD-LTE 45': '46640,46690,46740',
                                 'TDD-LTE 46': '46840,50665,54490',
                                 'TDD-LTE 47': '54590,54890,55190'},
                            '15MHz':
                                {'FDD-LTE 1': '18075,18300,18525',
                                 'FDD-LTE 2': '18675,18900,19125',
                                 'FDD-LTE 3': '19275,19575,19875',
                                 'FDD-LTE 4': '20025,20175,20325',
                                 'FDD-LTE 5': '',
                                 'FDD-LTE 6': '',
                                 'FDD-LTE 7': '20825,21100,21375',
                                 'FDD-LTE 8': '',
                                 'FDD-LTE 9': '21875,21975,22075',
                                 'FDD-LTE 10': '22225,22450,22675',
                                 'FDD-LTE 11': '',
                                 'FDD-LTE 12': '',
                                 'FDD-LTE 13': '',
                                 'FDD-LTE 14': '',
                                 'FDD-LTE 17': '',
                                 'FDD-LTE 18': '23925',
                                 'FDD-LTE 19': '24075',
                                 'FDD-LTE 20': '24225,24300,24375',
                                 'FDD-LTE 21': '24525',
                                 'FDD-LTE 22': '24675,25000,25325',
                                 'FDD-LTE 23': '25575,25600,25625',
                                 'FDD-LTE 24': '',
                                 'FDD-LTE 25': '26115,26365,26615',
                                 'FDD-LTE 26': '26765,26865,26965',
                                 'FDD-LTE 27': '',
                                 'FDD-LTE 28': '27285,27435,27585',
                                 'FDD-LTE 30': '',
                                 'FDD-LTE 31': '',
                                 'TDD-LTE 33': '36075,36100,36125',
                                 'TDD-LTE 34': '36275',
                                 'TDD-LTE 35': '36425,36650,36875',
                                 'TDD-LTE 36': '37025,37250,37475',
                                 'TDD-LTE 37': '37625,37650,37675',
                                 'TDD-LTE 38': '37825,38000,38175',
                                 'TDD-LTE 39': '38325,38450,38575',
                                 'TDD-LTE 40': '38725,39150,39575',
                                 'TDD-LTE 41': '39725,40620,41515',
                                 'TDD-LTE 42': '41665,42590,43515',
                                 'TDD-LTE 43': '43665,44590,45515',
                                 'TDD-LTE 44': '45665,46090,46515',
                                 'TDD-LTE 45': '46665,46690,46715',
                                 'TDD-LTE 46': '',
                                 'TDD-LTE 47': ''},
                            '20MHz':
                                {'FDD-LTE 1': '18100,18300,18500',
                                 'FDD-LTE 2': '18700,18900,19100',
                                 'FDD-LTE 3': '19300,19575,19850',
                                 'FDD-LTE 4': '20050,20175,20300',
                                 'FDD-LTE 5': '',
                                 'FDD-LTE 6': '',
                                 'FDD-LTE 7': '20850,21100,21350',
                                 'FDD-LTE 8': '',
                                 'FDD-LTE 9': '21900,21975,22050',
                                 'FDD-LTE 10': '22250,22450,22650',
                                 'FDD-LTE 11': '',
                                 'FDD-LTE 12': '',
                                 'FDD-LTE 13': '',
                                 'FDD-LTE 14': '',
                                 'FDD-LTE 17': '',
                                 'FDD-LTE 18': '',
                                 'FDD-LTE 19': '',
                                 'FDD-LTE 20': '24250,24300,24350',
                                 'FDD-LTE 21': '',
                                 'FDD-LTE 22': '24700,25000,25300',
                                 'FDD-LTE 23': '25600',
                                 'FDD-LTE 24': '',
                                 'FDD-LTE 25': '26140,26365,26590',
                                 'FDD-LTE 26': '',
                                 'FDD-LTE 27': '',
                                 'FDD-LTE 28': '27310,27435,27560',
                                 'FDD-LTE 30': '',
                                 'FDD-LTE 31': '',
                                 'TDD-LTE 33': '36100',
                                 'TDD-LTE 34': '',
                                 'TDD-LTE 35': '36450,36650,36850',
                                 'TDD-LTE 36': '37050,37250,37450',
                                 'TDD-LTE 37': '37650',
                                 'TDD-LTE 38': '37850,38000,38150',
                                 'TDD-LTE 39': '38350,38450,38550',
                                 'TDD-LTE 40': '38750,39150,39550',
                                 'TDD-LTE 41': '39750,40620,41490',
                                 'TDD-LTE 42': '41690,42590,43490',
                                 'TDD-LTE 43': '43690,44590,45490',
                                 'TDD-LTE 44': '45690,46090,46490',
                                 'TDD-LTE 45': '46690',
                                 'TDD-LTE 46': '46890,50665,54440',
                                 'TDD-LTE 47': '54640,54890,55140'}}                      # 用于存放用于测试的lte channel

lte_channel_default_dict = {'1.4MHz':                                            # 用于存放lte channel的默认值
                                {'FDD-LTE 1': '',
                                 'FDD-LTE 2': '18607,18900,19193',
                                 'FDD-LTE 3': '19207,19575,19943',
                                 'FDD-LTE 4': '19957,20175,20393',
                                 'FDD-LTE 5': '20407,20525,20643',
                                 'FDD-LTE 6': '',
                                 'FDD-LTE 7': '',
                                 'FDD-LTE 8': '21457,21625,21793',
                                 'FDD-LTE 9': '',
                                 'FDD-LTE 10': '',
                                 'FDD-LTE 11': '',
                                 'FDD-LTE 12': '23017,23095,23173',
                                 'FDD-LTE 13': '',
                                 'FDD-LTE 14': '',
                                 'FDD-LTE 17': '',
                                 'FDD-LTE 18': '',
                                 'FDD-LTE 19': '',
                                 'FDD-LTE 20': '',
                                 'FDD-LTE 21': '',
                                 'FDD-LTE 22': '',
                                 'FDD-LTE 23': '25507,25600,25693',
                                 'FDD-LTE 24': '',
                                 'FDD-LTE 25': '26047,26365,26683',
                                 'FDD-LTE 26': '26697,26865,27033',
                                 'FDD-LTE 27': '27047,27125,27203',
                                 'FDD-LTE 28': '',
                                 'FDD-LTE 30': '',
                                 'FDD-LTE 31': '27767,27785,27803',
                                 'TDD-LTE 33': '',
                                 'TDD-LTE 34': '',
                                 'TDD-LTE 35': '36357,36650,36943',
                                 'TDD-LTE 36': '36957,37250,37543',
                                 'TDD-LTE 37': '',
                                 'TDD-LTE 38': '',
                                 'TDD-LTE 39': '',
                                 'TDD-LTE 40': '',
                                 'TDD-LTE 41': '',
                                 'TDD-LTE 42': '',
                                 'TDD-LTE 43': '',
                                 'TDD-LTE 44': '',
                                 'TDD-LTE 45': '',
                                 'TDD-LTE 46': '',
                                 'TDD-LTE 47': ''},
                            '3MHz':
                                {'FDD-LTE 1': '',
                                 'FDD-LTE 2': '18615,18900,19185',
                                 'FDD-LTE 3': '19215,19575,19935',
                                 'FDD-LTE 4': '19965,20175,20385',
                                 'FDD-LTE 5': '20415,20525,20635',
                                 'FDD-LTE 6': '',
                                 'FDD-LTE 7': '',
                                 'FDD-LTE 8': '21465,21625,21785',
                                 'FDD-LTE 9': '',
                                 'FDD-LTE 10': '',
                                 'FDD-LTE 11': '',
                                 'FDD-LTE 12': '23025,23095,23165',
                                 'FDD-LTE 13': '',
                                 'FDD-LTE 14': '',
                                 'FDD-LTE 17': '',
                                 'FDD-LTE 18': '',
                                 'FDD-LTE 19': '',
                                 'FDD-LTE 20': '',
                                 'FDD-LTE 21': '',
                                 'FDD-LTE 22': '',
                                 'FDD-LTE 23': '25515,25600,25685',
                                 'FDD-LTE 24': '',
                                 'FDD-LTE 25': '26055,26365,26675',
                                 'FDD-LTE 26': '26705,26865,27025',
                                 'FDD-LTE 27': '27055,27125,27195',
                                 'FDD-LTE 28': '27225,27435,27645',
                                 'FDD-LTE 30': '',
                                 'FDD-LTE 31': '27775,27785,27795',
                                 'TDD-LTE 33': '',
                                 'TDD-LTE 34': '',
                                 'TDD-LTE 35': '36365,36650,36935',
                                 'TDD-LTE 36': '36965,37250,37535',
                                 'TDD-LTE 37': '',
                                 'TDD-LTE 38': '',
                                 'TDD-LTE 39': '',
                                 'TDD-LTE 40': '',
                                 'TDD-LTE 41': '',
                                 'TDD-LTE 42': '',
                                 'TDD-LTE 43': '',
                                 'TDD-LTE 44': '45605,46090,46575',
                                 'TDD-LTE 45': '',
                                 'TDD-LTE 46': '',
                                 'TDD-LTE 47': ''},
                            '5MHz':
                                {'FDD-LTE 1': '18025,18300,18575',
                                 'FDD-LTE 2': '18625,18900,19175',
                                 'FDD-LTE 3': '19225,19575,19925',
                                 'FDD-LTE 4': '19975,20175,20375',
                                 'FDD-LTE 5': '20425,20525,20625',
                                 'FDD-LTE 6': '20675,20700,20725',
                                 'FDD-LTE 7': '20775,21100,21425',
                                 'FDD-LTE 8': '21475,21625,21775',
                                 'FDD-LTE 9': '21825,21975,22125',
                                 'FDD-LTE 10': '22175,22450,22725',
                                 'FDD-LTE 11': '22775,22850,22925',
                                 'FDD-LTE 12': '23035,23095,23155',
                                 'FDD-LTE 13': '23205,23230,23255',
                                 'FDD-LTE 14': '23305,23330,23355',
                                 'FDD-LTE 17': '23755,23790,23825',
                                 'FDD-LTE 18': '23875,23925,23975',
                                 'FDD-LTE 19': '24025,24075,24125',
                                 'FDD-LTE 20': '24175,24300,24425',
                                 'FDD-LTE 21': '24475,24525,24575',
                                 'FDD-LTE 22': '24625,25000,25375',
                                 'FDD-LTE 23': '25525,25600,25675',
                                 'FDD-LTE 24': '25725,25870,26015',
                                 'FDD-LTE 25': '26065,26365,26665',
                                 'FDD-LTE 26': '26715,26865,27015',
                                 'FDD-LTE 27': '27065,27125,27185',
                                 'FDD-LTE 28': '27235,27435,27635',
                                 'FDD-LTE 30': '27685,27710,27735',
                                 'FDD-LTE 31': '27785',
                                 'TDD-LTE 33': '36025,36100,36175',
                                 'TDD-LTE 34': '36225,36275,36325',
                                 'TDD-LTE 35': '36375,36650,36925',
                                 'TDD-LTE 36': '36975,37250,37525',
                                 'TDD-LTE 37': '37575,37650,37725',
                                 'TDD-LTE 38': '37775,38000,38225',
                                 'TDD-LTE 39': '38275,38450,38625',
                                 'TDD-LTE 40': '38675,39150,39625',
                                 'TDD-LTE 41': '39675,40620,41565',
                                 'TDD-LTE 42': '41615,42590,43565',
                                 'TDD-LTE 43': '43615,44590,45565',
                                 'TDD-LTE 44': '45615,46090,46565',
                                 'TDD-LTE 45': '46615,46690,46765',
                                 'TDD-LTE 46': '',
                                 'TDD-LTE 47': ''},
                            '10MHz':
                                {'FDD-LTE 1': '18050,18300,18550',
                                 'FDD-LTE 2': '18650,18900,19150',
                                 'FDD-LTE 3': '19250,19575,19900',
                                 'FDD-LTE 4': '20000,20175,20350',
                                 'FDD-LTE 5': '20450,20525,20600',
                                 'FDD-LTE 6': '20700',
                                 'FDD-LTE 7': '20800,21100,21400',
                                 'FDD-LTE 8': '21500,21625,21750',
                                 'FDD-LTE 9': '21850,21975,22100',
                                 'FDD-LTE 10': '22200,22450,22700',
                                 'FDD-LTE 11': '22800,22850,22900',
                                 'FDD-LTE 12': '23060,23095,23130',
                                 'FDD-LTE 13': '23230',
                                 'FDD-LTE 14': '23330',
                                 'FDD-LTE 17': '23780,23790,23800',
                                 'FDD-LTE 18': '23900,23925,23950',
                                 'FDD-LTE 19': '24050,24075,24100',
                                 'FDD-LTE 20': '24200,24300,24400',
                                 'FDD-LTE 21': '24500,24525,24550',
                                 'FDD-LTE 22': '24650,25000,25350',
                                 'FDD-LTE 23': '25550,25600,25650',
                                 'FDD-LTE 24': '25750,25870,25990',
                                 'FDD-LTE 25': '26090,26365,26640',
                                 'FDD-LTE 26': '26740,26865,26990',
                                 'FDD-LTE 27': '27090,27125,27160',
                                 'FDD-LTE 28': '27260,27435,27610',
                                 'FDD-LTE 30': '27710',
                                 'FDD-LTE 31': '',
                                 'TDD-LTE 33': '36050,36100,36150',
                                 'TDD-LTE 34': '36250,36275,36300',
                                 'TDD-LTE 35': '36400,36650,36900',
                                 'TDD-LTE 36': '37000,37250,37500',
                                 'TDD-LTE 37': '37600,37650,37700',
                                 'TDD-LTE 38': '37800,38000,38200',
                                 'TDD-LTE 39': '38300,38450,38600',
                                 'TDD-LTE 40': '38700,39150,39600',
                                 'TDD-LTE 41': '39700,40620,41540',
                                 'TDD-LTE 42': '41640,42590,43540',
                                 'TDD-LTE 43': '43640,44590,45540',
                                 'TDD-LTE 44': '45640,46090,46540',
                                 'TDD-LTE 45': '46640,46690,46740',
                                 'TDD-LTE 46': '46840,50665,54490',
                                 'TDD-LTE 47': '54590,54890,55190'},
                            '15MHz':
                                {'FDD-LTE 1': '18075,18300,18525',
                                 'FDD-LTE 2': '18675,18900,19125',
                                 'FDD-LTE 3': '19275,19575,19875',
                                 'FDD-LTE 4': '20025,20175,20325',
                                 'FDD-LTE 5': '',
                                 'FDD-LTE 6': '',
                                 'FDD-LTE 7': '20825,21100,21375',
                                 'FDD-LTE 8': '',
                                 'FDD-LTE 9': '21875,21975,22075',
                                 'FDD-LTE 10': '22225,22450,22675',
                                 'FDD-LTE 11': '',
                                 'FDD-LTE 12': '',
                                 'FDD-LTE 13': '',
                                 'FDD-LTE 14': '',
                                 'FDD-LTE 17': '',
                                 'FDD-LTE 18': '23925',
                                 'FDD-LTE 19': '24075',
                                 'FDD-LTE 20': '24225,24300,24375',
                                 'FDD-LTE 21': '24525',
                                 'FDD-LTE 22': '24675,25000,25325',
                                 'FDD-LTE 23': '25575,25600,25625',
                                 'FDD-LTE 24': '',
                                 'FDD-LTE 25': '26115,26365,26615',
                                 'FDD-LTE 26': '26765,26865,26965',
                                 'FDD-LTE 27': '',
                                 'FDD-LTE 28': '27285,27435,27585',
                                 'FDD-LTE 30': '',
                                 'FDD-LTE 31': '',
                                 'TDD-LTE 33': '36075,36100,36125',
                                 'TDD-LTE 34': '36275',
                                 'TDD-LTE 35': '36425,36650,36875',
                                 'TDD-LTE 36': '37025,37250,37475',
                                 'TDD-LTE 37': '37625,37650,37675',
                                 'TDD-LTE 38': '37825,38000,38175',
                                 'TDD-LTE 39': '38325,38450,38575',
                                 'TDD-LTE 40': '38725,39150,39575',
                                 'TDD-LTE 41': '39725,40620,41515',
                                 'TDD-LTE 42': '41665,42590,43515',
                                 'TDD-LTE 43': '43665,44590,45515',
                                 'TDD-LTE 44': '45665,46090,46515',
                                 'TDD-LTE 45': '46665,46690,46715',
                                 'TDD-LTE 46': '',
                                 'TDD-LTE 47': ''},
                            '20MHz':
                                {'FDD-LTE 1': '18100,18300,18500',
                                 'FDD-LTE 2': '18700,18900,19100',
                                 'FDD-LTE 3': '19300,19575,19850',
                                 'FDD-LTE 4': '20050,20175,20300',
                                 'FDD-LTE 5': '',
                                 'FDD-LTE 6': '',
                                 'FDD-LTE 7': '20850,21100,21350',
                                 'FDD-LTE 8': '',
                                 'FDD-LTE 9': '21900,21975,22050',
                                 'FDD-LTE 10': '22250,22450,22650',
                                 'FDD-LTE 11': '',
                                 'FDD-LTE 12': '',
                                 'FDD-LTE 13': '',
                                 'FDD-LTE 14': '',
                                 'FDD-LTE 17': '',
                                 'FDD-LTE 18': '',
                                 'FDD-LTE 19': '',
                                 'FDD-LTE 20': '24250,24300,24350',
                                 'FDD-LTE 21': '',
                                 'FDD-LTE 22': '24700,25000,25300',
                                 'FDD-LTE 23': '25600',
                                 'FDD-LTE 24': '',
                                 'FDD-LTE 25': '26140,26365,26590',
                                 'FDD-LTE 26': '',
                                 'FDD-LTE 27': '',
                                 'FDD-LTE 28': '27310,27435,27560',
                                 'FDD-LTE 30': '',
                                 'FDD-LTE 31': '',
                                 'TDD-LTE 33': '36100',
                                 'TDD-LTE 34': '',
                                 'TDD-LTE 35': '36450,36650,36850',
                                 'TDD-LTE 36': '37050,37250,37450',
                                 'TDD-LTE 37': '37650',
                                 'TDD-LTE 38': '37850,38000,38150',
                                 'TDD-LTE 39': '38350,38450,38550',
                                 'TDD-LTE 40': '38750,39150,39550',
                                 'TDD-LTE 41': '39750,40620,41490',
                                 'TDD-LTE 42': '41690,42590,43490',
                                 'TDD-LTE 43': '43690,44590,45490',
                                 'TDD-LTE 44': '45690,46090,46490',
                                 'TDD-LTE 45': '46690',
                                 'TDD-LTE 46': '46890,50665,54440',
                                 'TDD-LTE 47': '54640,54890,55140'}}

list_lte_band = ['FDD-LTE 1', 'FDD-LTE 2', 'FDD-LTE 3', 'FDD-LTE 4', 'FDD-LTE 5', 'FDD-LTE 6', 'FDD-LTE 7', 'FDD-LTE 8',
                 'FDD-LTE 9', 'FDD-LTE 10', 'FDD-LTE 11', 'FDD-LTE 12', 'FDD-LTE 13', 'FDD-LTE 14', 'FDD-LTE 17',
                 'FDD-LTE 18', 'FDD-LTE 19', 'FDD-LTE 20', 'FDD-LTE 21', 'FDD-LTE 22', 'FDD-LTE 23', 'FDD-LTE 24',
                 'FDD-LTE 25', 'FDD-LTE 26', 'FDD-LTE 27', 'FDD-LTE 28', 'FDD-LTE 30', 'FDD-LTE 31', 'TDD-LTE 33',
                 'TDD-LTE 34', 'TDD-LTE 35', 'TDD-LTE 36', 'TDD-LTE 37', 'TDD-LTE 38', 'TDD-LTE 39', 'TDD-LTE 40',
                 'TDD-LTE 41', 'TDD-LTE 42', 'TDD-LTE 43', 'TDD-LTE 44', 'TDD-LTE 45', 'TDD-LTE 46', 'TDD-LTE 47']

lte_ca_channel_fortest_dict = {'CA_2C': {'5+20': '18633+18750,18808+18925,18983+19100',
                                         '20+5': '18700+18817,18875+18992,19050+19167',
                                         '10+15': '18653+18773,18829+18949,19005+19125',
                                         '15+10': '18675+18795,18851+18971,19027+19147',
                                         '10+20': '18655+18799,18806+18950,18956+19100',
                                         '20+10': '18700+18844,18851+18995,19001+19145',
                                         '15+15': '18675+18825,18825+18975,18975+19125',
                                         '15+20': '18678+18849,18803+18974,18929+19100',
                                         '20+15': '18700+18871,18826+18997,18951+19122',
                                         '20+20': '18700+18898,18801+18999,18902+19100'},
                               'CA_5B': {'3+5': '20416+20455,20501+20540,20586+20625',
                                         '5+3': '20425+20464,20510+20549,20595+20634',
                                         '5+10': '20428+20500,20478+20550,20528+20600',
                                         '10+5': '20450+20522,20500+20572,20550+20622',
                                         '10+10': '20450+20549,20476+20575,20501+20600'},
                               'CA_7C': {'10+20': '20805+20949,21006+21150,21206+21350',
                                         '20+10': '20850+20994,21051+21195,21251+21395',
                                         '15+15': '20825+20975,21025+21175,21225+21375',
                                         '15+20 ': '20828+20999,21003+21174,21179+21350',
                                         '20+15': '20850+21021,21026+21197,21201+21372',
                                         '20+20': '20850+21048,21001+21199,21152+21350'},
                               'CA_12B': {'5+5': '23035+23083,23070+23118,23107+23155',
                                          '5+10': '23035+23107,23045+23117,23058+23130'},
                               'CA_38C': {'15+15': '37825+37975,37925+38075,38025+38175',
                                          '20+20': '37850+38048,37901+38099,37952+38150'},
                               'CA_41C': {'5+20': '39683+39800,40528+40645,41373+41490',
                                          '20+5': '39750+39867,40595+40712,41440+41557',
                                          '10+20': '39705+39849,40526+40670,41346+41490',
                                          '20+10': '39750+39894,40571+40715,41391+41535',
                                          '15+15': '39725+39875,40545+40695,41365+41515',
                                          '15+20': '39728+39899,40523+40694,41319+41490',
                                          '20+15': '39750+39921,40546+40717,41341+41512',
                                          '20+20': '39750+39948,40521+40719,41292+41490'}}

lte_ca_channel_default_dict = {'CA_2C': {'5+20': '18633+18750,18808+18925,18983+19100',
                                         '20+5': '18700+18817,18875+18992,19050+19167',
                                         '10+15': '18653+18773,18829+18949,19005+19125',
                                         '15+10': '18675+18795,18851+18971,19027+19147',
                                         '10+20': '18655+18799,18806+18950,18956+19100',
                                         '20+10': '18700+18844,18851+18995,19001+19145',
                                         '15+15': '18675+18825,18825+18975,18975+19125',
                                         '15+20': '18678+18849,18803+18974,18929+19100',
                                         '20+15': '18700+18871,18826+18997,18951+19122',
                                         '20+20': '18700+18898,18801+18999,18902+19100'},
                               'CA_5B': {'3+5': '20416+20455,20501+20540,20586+20625',
                                         '5+3': '20425+20464,20510+20549,20595+20634',
                                         '5+10': '20428+20500,20478+20550,20528+20600',
                                         '10+5': '20450+20522,20500+20572,20550+20622',
                                         '10+10': '20450+20549,20476+20575,20501+20600'},
                               'CA_7C': {'10+20': '20805+20949,21006+21150,21206+21350',
                                         '20+10': '20850+20994,21051+21195,21251+21395',
                                         '15+15': '20825+20975,21025+21175,21225+21375',
                                         '15+20 ': '20828+20999,21003+21174,21179+21350',
                                         '20+15': '20850+21021,21026+21197,21201+21372',
                                         '20+20': '20850+21048,21001+21199,21152+21350'},
                               'CA_12B': {'5+5': '23035+23083,23070+23118,23107+23155',
                                          '5+10': '23035+23107,23045+23117,23058+23130'},
                               'CA_38C': {'15+15': '37825+37975,37925+38075,38025+38175',
                                          '20+20': '37850+38048,37901+38099,37952+38150'},
                               'CA_41C': {'5+20': '39683+39800,40528+40645,41373+41490',
                                          '20+5': '39750+39867,40595+40712,41440+41557',
                                          '10+20': '39705+39849,40526+40670,41346+41490',
                                          '20+10': '39750+39894,40571+40715,41391+41535',
                                          '15+15': '39725+39875,40545+40695,41365+41515',
                                          '15+20': '39728+39899,40523+40694,41319+41490',
                                          '20+15': '39750+39921,40546+40717,41341+41512',
                                          '20+20': '39750+39948,40521+40719,41292+41490'}}

