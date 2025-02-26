# -*- coding: utf-8 -*-
'''
@Project : zwdx_minjiang
@File : .py
@description : Equipment control adapter interface
@Author : anonymous
@Date : 2025.02.26
'''
import os
import xlwt
import xlrd
import time
import math
import datetime
import threading
import numpy as np
import pandas as pd
import seaborn as sns
from pathlib import Path
from scipy.stats import norm
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
from collections import defaultdict
from IPython.display import clear_output

from zwdx_minjiang.driver.CTP100_Dev import ZW_CTP100_Dev
from zwdx_minjiang.driver.qulab_toolbox import wavedata as WD
import zwdx_minjiang.driver.ZW_QCS220_DRIVER_20241207 as QCS220

env_para = {}
test_para = {}
trig_para = {}
stop_flag = None # 停止判定,用于中断测试的FLAG
ctp100  = None # CTP100设备对象
qcs220  = None # QCS220设备对象
all_len  = 100 # 存储实验的总长度,打印进度条和画波形时使用
finish_len  = 100 # 存储实验的已完成长度,打印进度条和画波形时使用
sample_rate_hz  = 8e9 # QCS采样率
test_data  = defaultdict(list) # 存储数据
heatmap_mask  = None # 绘制热力图时，控制未绘制的区域不显示
result_dir = None
xml_path = None

def connect(qcsIp='192.168.1.180', qcsPort=8501, ctpIp='192.168.1.200') -> None:
        global ctp100, qcs220
        # 连接CTP
        # ctp100 = ZW_CTP100_Dev(ctpIp)

        # 连接QCS
        qcs220 = QCS220.ZW_QCS220_DRIVER(qcsIp, qcsPort)
        qcs220.performOpen()

def set_result_path(data_path):
    global result_dir,xml_path
    result_dir = f'{data_path}'
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    xml_path = f'{result_dir}/TestItems.xml'

def close_qcs220_all_channels():
    for ch in range(1,15):
        qcs220.setValue("Output", 0, chn=ch) 
        set_qcs220_freq(ch, 0, 2e-6, 0, delay=0e-9, replay_cont=0)
    for ch in range(15,22,1):
        qcs220.setValue('DAC_Offset', 0, chn=ch)

def set_qcs220_freq(ch, fout, data_length, amp=1, delay=0e-9, phi=0, replay_cont=1):
    # 生成dac波形数据，方式1
    # dac_sampling = sample_rate_hz
    # dac_data_len = round(data_length*dac_sampling)
    # fs = dac_sampling/256/1024
    # fout = fout * 1e6
    # if replay_cont:
    #     fout_wr = (fout//fs) * fs
    # else:
    #     fout_wr = fout
    # dac_data = np.sin(np.arange(dac_data_len)*(2*np.pi)*(fout_wr/dac_sampling)) * amp
    
    # 生成dac波形数据，方式2
    fs_fout = sample_rate_hz/256/1024
    fout = fout * 1e6
    if replay_cont:
        fout_wr = (fout//fs_fout) * fs_fout # dac_data_continue
    else:
        fout_wr = fout
    sin1=WD.Sin(fout_wr*2*np.pi, phi, data_length, sample_rate_hz) * amp
    dac_data = sin1.data
    qcs220.setValue("DAC_TriggerDelay", delay, chn=ch) # DAC输出相对触发信号延迟，单位s
    qcs220.setValue("DAC_Replay_count", 100000, chn=ch) # 通道重复播放数量，响应指定数量的触发信号
    qcs220.setValue("DAC_Relpay_continue", replay_cont, chn=ch) # 通道连续波功能，AWG数据首尾相接播放，用于回放连续波
    qcs220.setValue("DAC_Data", dac_data, chn=ch) # 发送波形数据到设备

def set_xy_freq(ch, fout, data_length, amp=1, delay=10e-9, phi=0, wave_type='DC'): 
    fout = fout * 1e6
    sin1 = WD.Sin(fout*2*np.pi, phi, data_length, sample_rate_hz)
    if wave_type.upper() == 'DC':
        gaussian = WD.DC(data_length, sample_rate_hz)
    elif wave_type.upper() == 'GAUSS':
        gaussian = WD.Gaussian2(data_length, sample_rate_hz, a=5)
    else:
        print('None wave type')
    data = (gaussian.data * sin1.data) * amp
    dac_data = data
    replay_times = 100000
    replay_cont = 0
    qcs220.setValue("DAC_TriggerDelay", delay, chn=ch) # DAC输出相对触发信号延迟，单位s
    qcs220.setValue("DAC_Replay_count", replay_times, chn=ch) # 通道重复播放数量，响应指定数量的触发信号
    qcs220.setValue("DAC_Relpay_continue", replay_cont, chn=ch) # 通道连续波功能，AWG数据首尾相接播放，用于回放连续波
    qcs220.setValue("DAC_Data", dac_data, chn=ch) # 发送波形数据到设备


def set_xy_2_freq(ch, fout, data_length, amp=1, ts=0, tDelay=10e-9, wave_type = 'DC'):
    all_time = data_length * 2 + ts
    assert all_time < 30e-6, "pluse length is over [30us]"
    fout = fout * 1e6
    sin1 = WD.Sin(fout*2*np.pi, 0, all_time, sample_rate_hz)
    t = np.zeros(math.ceil(ts*sample_rate_hz))
    if wave_type.upper() == 'DC':
        gaussian1 = WD.DC(data_length, sample_rate_hz)
        gaussian2 = WD.DC(data_length, sample_rate_hz)
    elif wave_type.upper() == 'GAUSS':
        gaussian1 = WD.Gaussian2(data_length, sample_rate_hz, a=5)
        gaussian2 = WD.Gaussian2(data_length, sample_rate_hz, a=5)
    else:
        print('None wave type')
    length = len(gaussian1.data.tolist()) + len(t.tolist()) + len(gaussian2.data.tolist())
    if length > len(sin1.data.tolist()):
        t1 = np.zeros(len(t)-1)
    elif length < len(sin1.data.tolist()):
        t1 = np.append(t,np.zeros(1))
    else:
        t1 = t
    wave = gaussian1.data.tolist() + t1.tolist() + gaussian2.data.tolist()
    data = wave * sin1.data * amp
    dac_data = data
    replay_times = 100000
    replay_cont = 0
    qcs220.setValue("DAC_TriggerDelay", tDelay, chn=ch) # DAC输出相对触发信号延迟，单位s
    qcs220.setValue("DAC_Replay_count", replay_times, chn=ch) # 通道重复播放数量，响应指定数量的触发信号
    qcs220.setValue("DAC_Relpay_continue", replay_cont, chn=ch) # 通道连续波功能，AWG数据首尾相接播放，用于回放连续波
    qcs220.setValue("DAC_Data", dac_data, chn=ch) # 发送波形数据到设备
        

def set_xy_3_pulse(ch, fout, data_length, amp=1, ts=0, tDelay =10e-9, wave_type = 'DC'): # 输入为pi/2脉冲信号
    all_time = data_length * 4 + ts
    assert all_time < 30e-6, "pluse length is over [30us]"
    fout = fout * 1e6
    t = np.arange(1/(2*sample_rate_hz), all_time, 1/sample_rate_hz)
    sin1 = WD.Sin(fout*2*np.pi, 0, all_time, sample_rate_hz)
    t21 = np.zeros(round(ts/2*sample_rate_hz))
    t22 = np.zeros(round(ts/2*sample_rate_hz))
    if wave_type.upper() == 'DC':
        gaussian1_wave = WD.DC(data_length, sample_rate_hz)
        gaussian_mid_wave = WD.DC(data_length*2, sample_rate_hz)
        gaussian2_wave = WD.DC(data_length, sample_rate_hz)
    elif wave_type.upper() == 'GAUSS':
        gaussian1_wave = WD.Gaussian2(data_length, sample_rate_hz, a=5)
        gaussian_mid_wave = WD.Gaussian2(data_length, sample_rate_hz, a=5)
        gaussian2_wave = WD.Gaussian2(data_length, sample_rate_hz, a=5)
    else:
        print('None wave type')
    wave1 = gaussian1_wave.data.tolist() + t21.tolist() + gaussian_mid_wave.data.tolist() + t22.tolist() + gaussian2_wave.data.tolist()
    first = len(gaussian1_wave) + len(t21)
    second = len(gaussian_mid_wave)
    wave_temp, t_temp = None, None
    if len(wave1) > len(t):
        wave_temp = wave1[0:len(t)]
        t_temp = t
        three = len(t) - first - second
    elif len(wave1) < len(t):
        wave_temp = wave1
        t_temp = t[0:len(wave1)]
        three = len(wave1) - first - second
    else:
        wave_temp = wave1
        t_temp = t
        three = len(t) - first - second
    data_temp = np.hstack((wave_temp[0:first] * sin1(t_temp[0:first]) * amp, wave_temp[first:first+second] * sin1(t_temp[first:first+second]) * 2*amp,
                        wave_temp[first+second:first+second+three] * sin1(t_temp[first+second:first+second+three]) * amp))
    dac_data = data_temp
    replay_times = 100000
    replay_cont = 0
    qcs220.setValue("DAC_TriggerDelay", tDelay, chn=ch) # DAC输出相对触发信号延迟，单位s
    qcs220.setValue("DAC_Replay_count", replay_times, chn=ch) # 通道重复播放数量，响应指定数量的触发信号
    qcs220.setValue("DAC_Relpay_continue", replay_cont, chn=ch) # 通道连续波功能，AWG数据首尾相接播放，用于回放连续波
    qcs220.setValue("dac_data", dac_data, chn=ch) # 发送波形数据到设备

def plot_row_data():
    """ 原始数据采集并画波形"""
    # ctp100.trigger_close()
    # ctp100.trigger_ctrl(int(test_para['trig_ch']),trig_para)
    qcs220.stop() 
    close_qcs220_all_channels()
    adc_channel_num = int(test_para['read_in_ch']) # 参数化通道编号
    qcs220.setValue("TriggerOff", 0) #关闭设备对触发源的相应，才能进行配置
    qcs220.setValue("TriggerSource", "Internal" if test_para['trig_mode'] == 0 else 'External') #触发源，Internal（内触发），External（外触发）
    qcs220.setValue("TriggerPeriod", trig_para['trigger_us']*1e-6) #内部触发周期，单位s
    qcs220.setValue("TriggerNumber", int(test_para['shots'])) #内部触发次数
    qcs220.setValue("TriggerContinue", trig_para['trigger_continue']) #内部触发连续触发模式，1开启，0关闭
    qcs220.setValue("ADC_TriggerDelay", test_para['read_in_delay'], chn=adc_channel_num) # ADC采集相对触发信号延迟，单位s
    qcs220.setValue("ADC_TriggerTimes", test_para['shots'], chn=adc_channel_num) # 读取解模重复次数，也就是响应外部触发完成采集、解模判决的次数
    qcs220.setValue("ADC_SaveLen", round(test_para['plot_pw'] *  2.5e9), chn=adc_channel_num) # 采集解模数据样点，按照采样点数计算，最大131072采样点
    set_qcs220_freq(int(test_para['read_out_ch']), test_para['read_out_freq'], test_para['read_out_pw'],test_para['read_out_amp'], delay=test_para['read_out_delay'],replay_cont=0)
    # ctp100.trigger_open()
    qcs220.run()
    chinfo = []
    chinfo.append(0)
    chinfo.append(adc_channel_num)
    adc_data = qcs220.getResult(ch = chinfo, option="raw") # 从设备获取指定通道原始数据
    plt.plot(adc_data)
    plt.show()
    
def delay_test():
    """ 测试1：延时标定"""
    global stop_flag, finish_len, all_len, test_data
    try:
        test_index = 1
        stop_flag = False
        now_time = datetime.datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
        result_name = f'1_延时标定_{env_para["qubit"]}_{now_time}'
        test_data.clear()
        qcs220.stop()
        close_qcs220_all_channels()
        # ctp100.trigger_close()
        # ctp100.trigger_ctrl(int(test_para['trig_ch']), trig_para) 
        adc_chennel_num = int(test_para['read_in_ch']) # 参数化通道编号
        dac_chennel_num = int(test_para['read_out_ch']) # 参数化通道编号
        mul_freq = test_para['read_out_freq'] * 1e6 # 设定采集解模频率
        mul_phase = 0 # 设定采集解模初始相位为0°
        read_data_len = round(test_para['read_in_pw']*2.5e9) # 设定总采集解模样点数量，最高131072点
        mul_f = [[mul_phase, mul_freq]] # 构建解模参数列表
        qcs220.setValue("TriggerOff", 0) #关闭设备对触发源的相应，才能进行配置
        qcs220.setValue("TriggerSource", "Internal" if test_para['trig_mode'] == 0 else 'External') #触发源，Internal（内触发），External（外触发）
        qcs220.setValue("TriggerPeriod", trig_para['trigger_us']*1e-6) #内部触发周期，单位s
        qcs220.setValue("TriggerNumber", int(test_para['shots'])) #内部触发次数
        qcs220.setValue("TriggerContinue", trig_para['trigger_continue']) #内部触发连续触发模式，1开启，0关闭
        qcs220.setValue("MUL_Times", int(test_para['shots']), chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
        qcs220.setValue("MUL_F_Len", read_data_len, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
        qcs220.setValue("MUL_F_Data", mul_f, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
        qcs220.setValue("DAC_TriggerDelay", trig_para['trigger_delay'],chn=dac_chennel_num) #内部触发周期，单位s
        qcs220.setValue("DAC_Replay_count", int(test_para['shots']),chn=dac_chennel_num) #内部触发次数
        qcs220.setValue("DAC_Relpay_continue", trig_para['trigger_continue'],chn=dac_chennel_num) #内部触发连续触发模式，1开启，0关闭
        chinfo = [0, adc_chennel_num]  # 构建获取通道数据通道列表
        delay_list = np.linspace(test_para['read_in_delay']['start'], test_para['read_in_delay']['end'],
                    round(abs(test_para['read_in_delay']['end'] - test_para['read_in_delay']['start'])/test_para['read_in_delay']['step']) + 1)
        finish_len = 0
        all_len = len(delay_list)
        t1 = threading.Thread(target=draw_line_chart,args=(result_dir,result_name,'delay_test','delay/s','mod',))
        t1.start()
        for delay in delay_list:
            if stop_flag:
                break
            # ctp100.trigger_close()
            qcs220.stop()
            qcs220.setValue("MUL_TriggerDelay", delay, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
            qcs220.setValue("MUL_SetPars", 0, chn=adc_chennel_num) # 更新参数
            set_qcs220_freq(int(test_para['read_out_ch']), test_para['read_out_freq'], test_para['read_out_pw'], test_para['read_out_amp'], delay=test_para['read_out_delay'], replay_cont=0)
            # ctp100.trigger_open()
            qcs220.run()  # 启动反射测量过程，DAC输出激励波形，ADC采集解模
            time.sleep(0.01)
            mul_data = qcs220.getResult(ch = chinfo, option="IQ") # 从设备获取指定通道原始数据
            muldata = np.array(mul_data).T[0]
            for i in range(len(muldata)):
                muldata[i] = complex(muldata[i])
            y_mod = np.abs(np.mean(muldata) / read_data_len / (2**13-1))
            test_data['x'].append(delay)
            test_data['y'].append(y_mod)
            finish_len += 1
        saveResult(result_name, test_data, test_index, now_time)
    except:
        stop_flag = True
    finally:
        t1.join()
        
def read_mod():
    # ctp100.trigger_close()
    # ctp100.trigger_ctrl(int(test_para['trig_ch']), trig_para)  
    qcs220.stop()
    close_qcs220_all_channels()
    adc_chennel_num = int(test_para['read_in_ch']) # 参数化通道编号
    dac_chennel_num = int(test_para['read_out_ch']) # 参数化通道编号
    mul_freq = test_para['read_out_freq'] * 1e6 # 设定采集解模频率
    mul_phase = 0 # 设定采集解模初始相位为0°
    read_data_len = round(test_para['read_in_pw']*2.5e9) # 设定总采集解模样点数量，最高131072点
    mul_f = [[mul_phase, mul_freq]] # 构建解模参数列表
    qcs220.setValue("TriggerOff", 0) #关闭设备对触发源的相应，才能进行配置
    qcs220.setValue("TriggerSource", "Internal" if test_para['trig_mode'] == 0 else 'External') #触发源，Internal（内触发），External（外触发）
    qcs220.setValue("TriggerPeriod", trig_para['trigger_us']*1e-6) #内部触发周期，单位s
    qcs220.setValue("TriggerNumber", int(test_para['shots'])) #内部触发次数
    qcs220.setValue("TriggerContinue", trig_para['trigger_continue']) #内部触发连续触发模式，1开启，0关闭
    qcs220.setValue("MUL_TriggerDelay", test_para['read_in_delay'], chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
    qcs220.setValue("MUL_Times", int(test_para['shots']), chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
    qcs220.setValue("MUL_F_Len", read_data_len, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
    qcs220.setValue("MUL_F_Data", mul_f, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
    qcs220.setValue("MUL_SetPars", 0, chn=adc_chennel_num)
    qcs220.setValue("DAC_TriggerDelay", trig_para['trigger_delay'],chn=dac_chennel_num) #内部触发周期，单位s
    qcs220.setValue("DAC_Replay_count", int(test_para['shots']),chn=dac_chennel_num) #内部触发次数
    qcs220.setValue("DAC_Relpay_continue", trig_para['trigger_continue'],chn=dac_chennel_num) #内部触发连续触发模式，1开启，0关闭
    set_qcs220_freq(int(test_para['read_out_ch']), test_para['read_out_freq'], test_para['read_out_pw'], test_para['read_out_amp'], delay=test_para['read_out_delay'], replay_cont=0)
    # ctp100.trigger_open()
    qcs220.run()  # 启动反射测量过程，DAC输出激励波形，ADC采集解模
    time.sleep(0.01)
    chinfo = [0, adc_chennel_num]  # 构建获取通道数据通道列表
    mul_data = qcs220.getResult(ch = chinfo, option="IQ") # 从设备获取指定通道原始数据
    muldata = np.array(mul_data).T[0]
    for i in range(len(muldata)):
        muldata[i] = complex(muldata[i])
    y_mod = np.abs(np.mean(muldata) / read_data_len / (2**13-1))
    print(f'y_mod:{y_mod}')
    plt.plot(muldata.real,muldata.imag,'.')

def sweep_cavity_freq():
    """ 测试2：扫腔频"""
    global stop_flag, finish_len, all_len, test_data
    try:
        test_index = 2
        stop_flag = False
        now_time = datetime.datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
        result_name = f'2_读取腔频率扫描_{env_para["qubit"]}_{now_time}'
        test_data.clear()
        qcs220.stop()
        close_qcs220_all_channels()
        # ctp100.trigger_close()
        # ctp100.trigger_ctrl(int(test_para['trig_ch']), trig_para)
        adc_chennel_num = int(test_para['read_in_ch']) # 参数化通道编号
        dac_chennel_num = int(test_para['read_out_ch']) # 参数化通道编号
        mul_phase = 0 # 设定采集解模初始相位为0°
        read_data_len = round(test_para['read_in_pw']*2.5e9) # 设定总采集解模样点数量，最高131072点
        qcs220.setValue("TriggerOff", 0) #关闭设备对触发源的相应，才能进行配置
        qcs220.setValue("TriggerSource", "Internal" if test_para['trig_mode'] == 0 else 'External') #触发源，Internal（内触发），External（外触发）
        qcs220.setValue("TriggerPeriod", trig_para['trigger_us']*1e-6) #内部触发周期，单位s
        qcs220.setValue("TriggerNumber", int(test_para['shots'])) #内部触发次数
        qcs220.setValue("TriggerContinue", trig_para['trigger_continue']) #内部触发连续触发模式，1开启，0关闭
        qcs220.setValue("MUL_Times", int(test_para['shots']), chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
        qcs220.setValue("MUL_F_Len", read_data_len, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
        ad_trigger_delay = 260e-9 + test_para['read_in_delay']  #AD采集延迟，样点数量，用户可以根据采样率5Gsps和时间计算取整后得到
        qcs220.setValue("MUL_TriggerDelay", ad_trigger_delay, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
        qcs220.setValue("DAC_TriggerDelay", trig_para['trigger_delay'],chn=dac_chennel_num) #内部触发周期，单位s
        qcs220.setValue("DAC_Replay_count", int(test_para['shots']),chn=dac_chennel_num) #内部触发次数
        qcs220.setValue("DAC_Relpay_continue", trig_para['trigger_continue'],chn=dac_chennel_num) #内部触发连续触发模式，1开启，0关闭
        chinfo = [0, adc_chennel_num]  # 构建获取通道数据通道列表
        freq_list = np.around(np.linspace(test_para['sweep_freq']['start'], test_para['sweep_freq']['end'], 
                                round(abs(test_para['sweep_freq']['end'] - test_para['sweep_freq']['start'])/test_para['sweep_freq']['step']) + 1), 2)
        finish_len = 0
        all_len = len(freq_list)
        t1 = threading.Thread(target=draw_line_chart,args=(result_dir,result_name,'sweep_cavity_freq','MHz','mod',))
        t1.start()
        for freq in freq_list:
            if stop_flag:
                break
            # ctp100.trigger_close()
            qcs220.stop()
            set_qcs220_freq(int(test_para['read_out_ch']), freq, test_para['read_out_pw'], test_para['read_out_amp'], delay=test_para['read_out_delay'], replay_cont=0)
            mul_freq = freq * 1e6 # 设定采集解模频率
            mul_f = [[mul_phase, mul_freq]] # 构建解模参数列表
            qcs220.setValue("MUL_F_Data", mul_f, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
            qcs220.setValue("MUL_SetPars", 0, chn=adc_chennel_num) # 更新参数
            # ctp100.trigger_open()
            qcs220.run()  # 启动反射测量过程，DAC输出激励波形，ADC采集解模
            time.sleep(0.01)
            mul_data = qcs220.getResult(ch = chinfo, option="IQ") # 从设备获取指定通道原始数据
            muldata = np.array(mul_data).T[0]
            for i in range(len(muldata)):
                muldata[i] = complex(muldata[i])
            y_mod = np.abs(np.mean(muldata) / read_data_len / (2**13-1))
            test_data['x'].append(freq)
            test_data['y'].append(y_mod)
            finish_len += 1
        saveResult(result_name, test_data, test_index, now_time)
    except:
        stop_flag = True
    finally:
        t1.join()


def sweep_qa_power_freq():
    """测试3：扫描读取腔色散频移扫描"""
    global stop_flag, finish_len, all_len, test_data, heatmap_mask
    try:
        test_index = 3
        stop_flag = False
        now_time = datetime.datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
        result_name = f'3_读取腔色散频移扫描_{env_para["qubit"]}_{now_time}'
        test_data.clear()
        qcs220.stop()
        close_qcs220_all_channels()
        # ctp100.trigger_close()
        # ctp100.trigger_ctrl(int(test_para['trig_ch']), trig_para)
        adc_chennel_num = int(test_para['read_in_ch']) # 参数化通道编号
        dac_chennel_num = int(test_para['read_out_ch']) # 参数化通道编号
        mul_phase = 0 # 设定采集解模初始相位为0°
        read_data_len = round(test_para['read_in_pw']*2.5e9) # 设定总采集解模样点数量，最高131072点
        qcs220.setValue("TriggerOff", 0) #关闭设备对触发源的相应，才能进行配置
        qcs220.setValue("TriggerSource", "Internal" if test_para['trig_mode'] == 0 else 'External') #触发源，Internal（内触发），External（外触发）
        qcs220.setValue("TriggerPeriod", trig_para['trigger_us']*1e-6) #内部触发周期，单位s
        qcs220.setValue("TriggerNumber", int(test_para['shots'])) #内部触发次数
        qcs220.setValue("TriggerContinue", trig_para['trigger_continue']) #内部触发连续触发模式，1开启，0关闭
        qcs220.setValue("MUL_Times", int(test_para['shots']), chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
        qcs220.setValue("MUL_F_Len", read_data_len, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
        ad_trigger_delay = 260e-9 + test_para['read_in_delay']  #AD采集延迟，样点数量，用户可以根据采样率5Gsps和时间计算取整后得到
        qcs220.setValue("MUL_TriggerDelay", ad_trigger_delay, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
        qcs220.setValue("DAC_TriggerDelay", trig_para['trigger_delay'],chn=dac_chennel_num) #内部触发周期，单位s
        qcs220.setValue("DAC_Replay_count", int(test_para['shots']),chn=dac_chennel_num) #内部触发次数
        qcs220.setValue("DAC_Relpay_continue", trig_para['trigger_continue'],chn=dac_chennel_num) #内部触发连续触发模式，1开启，0关闭
        chinfo = [0, adc_chennel_num]  # 构建获取通道数据通道列表
        x_amp_list = np.around(np.linspace(test_para['sweep_amp']['start'], test_para['sweep_amp']['end'], 
                                round(abs(test_para['sweep_amp']['end'] - test_para['sweep_amp']['start'])/test_para['sweep_amp']['step']) + 1), 2)
        y_freq_list = np.around(np.linspace(test_para['sweep_freq']['start'], test_para['sweep_freq']['end'], 
                                round(abs(test_para['sweep_freq']['end'] - test_para['sweep_freq']['start'])/test_para['sweep_freq']['step']) + 1), 2)
        test_data['x'] = x_amp_list
        test_data['y'] = y_freq_list
        z_temp = []
        for i in range(len(x_amp_list)):
            z_temp.append(np.zeros_like(y_freq_list))
        test_data['z'] = z_temp
        heatmap_mask = (np.random.randint(1,size=(len(x_amp_list),len(y_freq_list)))==0)
        all_len = len(x_amp_list) * len(y_freq_list)
        finish_len = 0
        t1 = threading.Thread(target=draw_heatmap_chart,args=(result_dir,result_name,'sweep_qa_power_freq','freq/MHz','amp',))
        t1.start()
        for ix in range(len(x_amp_list)):
            power = x_amp_list[ix]
            for iy in range(len(y_freq_list)):
                if stop_flag:
                    break
                freq = y_freq_list[iy]
                # ctp100.trigger_close()
                qcs220.stop()
                set_qcs220_freq(int(test_para['read_out_ch']), freq, test_para['read_out_pw'], amp=power, delay=test_para['read_out_delay'], replay_cont=0)
                mul_freq = freq * 1e6 # 设定采集解模频率
                mul_f = [[mul_phase, mul_freq]] # 构建解模参数列表
                qcs220.setValue("MUL_F_Data", mul_f, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
                qcs220.setValue("MUL_SetPars", 0, chn=adc_chennel_num) # 更新参数
                qcs220.run()  # 启动反射测量过程，DAC输出激励波形，ADC采集解模
                time.sleep(0.01)
                mul_data = qcs220.getResult(ch = chinfo, option="IQ") # 从设备获取指定通道原始数据
                muldata = np.array(mul_data).T[0]
                for i in range(len(muldata)):
                    muldata[i] = complex(muldata[i])
                iq_lh = np.mean(muldata) / read_data_len / (2**13-1) / power
                test_data['z'][ix][iy] = np.abs(iq_lh)
                heatmap_mask[ix][iy] = False
                finish_len = ix * len(y_freq_list) + iy + 1
        saveResult(result_name, test_data, test_index, now_time)
    except:
        stop_flag = True
    finally:
        t1.join()
            
def sweep_zbias_cavity_freq():
    """测试4：Z偏置扫腔频"""
    global stop_flag, finish_len, all_len, test_data, heatmap_mask
    try:
        test_index = 4
        stop_flag = False
        now_time = datetime.datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
        result_name = f'4_Z偏置扫读取腔频率_{env_para["qubit"]}_{now_time}'
        test_data.clear()
        qcs220.stop()
        close_qcs220_all_channels()
        # ctp100.trigger_close()
        # ctp100.trigger_ctrl(int(test_para['trig_ch']),trig_para)
        adc_chennel_num = int(test_para['read_in_ch']) # 参数化通道编号
        dac_chennel_num = int(test_para['read_out_ch']) # 参数化通道编号
        mul_phase = 0 # 设定采集解模初始相位为0°
        read_data_len = round(test_para['read_in_pw']*2.5e9) # 设定总采集解模样点数量，最高131072点
        qcs220.setValue("TriggerOff", 0) #关闭设备对触发源的相应，才能进行配置
        qcs220.setValue("TriggerSource", "Internal" if test_para['trig_mode'] == 0 else 'External') #触发源，Internal（内触发），External（外触发）
        qcs220.setValue("TriggerPeriod", trig_para['trigger_us']*1e-6) #内部触发周期，单位s
        qcs220.setValue("TriggerNumber", int(test_para['shots'])) #内部触发次数
        qcs220.setValue("TriggerContinue", trig_para['trigger_continue']) #内部触发连续触发模式，1开启，0关闭
        qcs220.setValue("MUL_Times", int(test_para['shots']), chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
        qcs220.setValue("MUL_F_Len", read_data_len, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
        ad_trigger_delay = 260e-9 + test_para['read_in_delay']  #AD采集延迟，样点数量，用户可以根据采样率5Gsps和时间计算取整后得到
        qcs220.setValue("MUL_TriggerDelay", ad_trigger_delay, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
        qcs220.setValue("DAC_TriggerDelay", trig_para['trigger_delay'],chn=dac_chennel_num) #内部触发周期，单位s
        qcs220.setValue("DAC_Replay_count", int(test_para['shots']),chn=dac_chennel_num) #内部触发次数
        qcs220.setValue("DAC_Relpay_continue", trig_para['trigger_continue'],chn=dac_chennel_num) #内部触发连续触发模式，1开启，0关闭
        chinfo = [0, adc_chennel_num]  # 构建获取通道数据通道列表
        x_amp_list = np.around(np.linspace(test_para['sweep_z_amp']['start'], test_para['sweep_z_amp']['end'],
                        round(abs(test_para['sweep_z_amp']['end'] - test_para['sweep_z_amp']['start'])/test_para['sweep_z_amp']['step']) + 1), 2)
        y_freq_list = np.around(np.linspace(test_para['sweep_cavity_freq']['start'], test_para['sweep_cavity_freq']['end'], 
                                round(abs(test_para['sweep_cavity_freq']['end'] - test_para['sweep_cavity_freq']['start'])/test_para['sweep_cavity_freq']['step']) + 1), 2)
        test_data['x'] = x_amp_list
        test_data['y'] = y_freq_list
        z_temp = []
        for i in range(len(x_amp_list)):
            z_temp.append(np.zeros_like(y_freq_list))
        test_data['z'] = z_temp
        heatmap_mask = (np.random.randint(1,size=(len(x_amp_list),len(y_freq_list)))==0)
        all_len = len(x_amp_list) * len(y_freq_list)
        finish_len = 0
        t1 = threading.Thread(target=draw_heatmap_chart,args=(result_dir,result_name,'sweep_zbias_cavity_freq','freq/MHz','zbais',))
        t1.start()
        for ix in range(len(x_amp_list)):
            amp = x_amp_list[ix]
            qcs220.stop()
            qcs220.setValue('DAC_Offset', amp, chn=int(test_para['z_ch']))
            for iy in range(len(y_freq_list)):
                if stop_flag:
                    break
                freq = y_freq_list[iy]
                qcs220.stop()
                # ctp100.trigger_close()
                set_qcs220_freq(int(test_para['read_out_ch']), freq, test_para['read_out_pw'], amp=test_para['read_out_amp'], delay=test_para['read_out_delay'], replay_cont=0)
                mul_freq = freq * 1e6 # 设定采集解模频率
                mul_f = [[mul_phase, mul_freq]] # 构建解模参数列表
                qcs220.setValue("MUL_F_Data", mul_f, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
                qcs220.setValue("MUL_SetPars", 0, chn=adc_chennel_num) # 更新参数
                qcs220.run()  # 启动反射测量过程，DAC输出激励波形，ADC采集解模
                time.sleep(0.01)
                mul_data = qcs220.getResult(ch = chinfo, option="IQ") # 从设备获取指定通道原始数据
                muldata = np.array(mul_data).T[0]
                for i in range(len(muldata)):
                    muldata[i] = complex(muldata[i])
                iq_lh = np.mean(muldata) / read_data_len / (2**13-1)
                test_data['z'][ix][iy] = np.abs(iq_lh)
                heatmap_mask[ix][iy] = False
                finish_len = ix * len(y_freq_list) + iy + 1
        saveResult(result_name, test_data, test_index, now_time)
    except:
        stop_flag = True
    finally:
        t1.join()

def sweep_cavity_freq_fine():
    """测试5：细扫腔频"""
    global stop_flag, finish_len, all_len, test_data
    try:
        test_index = 5
        stop_flag = False
        now_time = datetime.datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
        result_name = f'5_细扫读取腔频率_{env_para["qubit"]}_{now_time}'
        test_data.clear()
        qcs220.stop()
        close_qcs220_all_channels()
        # ctp100.trigger_close()
        # ctp100.trigger_ctrl(int(test_para['trig_ch']), trig_para)
        adc_chennel_num = int(test_para['read_in_ch']) # 参数化通道编号
        dac_chennel_num = int(test_para['read_out_ch']) # 参数化通道编号
        mul_phase = 0 # 设定采集解模初始相位为0°
        read_data_len = round(test_para['read_in_pw']*2.5e9) # 设定总采集解模样点数量，最高131072点
        qcs220.setValue("TriggerOff", 0) #关闭设备对触发源的相应，才能进行配置
        qcs220.setValue("TriggerSource", "Internal" if test_para['trig_mode'] == 0 else 'External') #触发源，Internal（内触发），External（外触发）
        qcs220.setValue("TriggerPeriod", trig_para['trigger_us']*1e-6) #内部触发周期，单位s
        qcs220.setValue("TriggerNumber", int(test_para['shots'])) #内部触发次数
        qcs220.setValue("TriggerContinue", trig_para['trigger_continue']) #内部触发连续触发模式，1开启，0关闭
        qcs220.setValue("MUL_Times", int(test_para['shots']), chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
        qcs220.setValue("MUL_F_Len", read_data_len, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
        ad_trigger_delay = 260e-9 + test_para['read_in_delay']  #AD采集延迟，样点数量，用户可以根据采样率5Gsps和时间计算取整后得到
        qcs220.setValue("MUL_TriggerDelay", ad_trigger_delay, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
        qcs220.setValue("DAC_TriggerDelay", trig_para['trigger_delay'],chn=dac_chennel_num) #内部触发周期，单位s
        qcs220.setValue("DAC_Replay_count", int(test_para['shots']),chn=dac_chennel_num) #内部触发次数
        qcs220.setValue("DAC_Relpay_continue", trig_para['trigger_continue'],chn=dac_chennel_num) #内部触发连续触发模式，1开启，0关闭
        qcs220.setValue('DAC_Offset', test_para['zbias'], chn=int(test_para['z_ch']))
        chinfo = [0, adc_chennel_num]  # 构建获取通道数据通道列表
        freq_list = np.around(np.linspace(test_para['sweep_freq']['start'], test_para['sweep_freq']['end'], 
                                round(abs(test_para['sweep_freq']['end'] - test_para['sweep_freq']['start'])/test_para['sweep_freq']['step']) + 1), 2)
        all_len = len(freq_list)
        finish_len = 0
        t1 = threading.Thread(target=draw_line_chart,args=(result_dir,result_name,'sweep_cavity_freq_fine','MHz','mod',))
        t1.start()
        for freq in freq_list:
            if stop_flag:
                break
            qcs220.stop()
            # ctp100.trigger_close()
            set_qcs220_freq(int(test_para['read_out_ch']), freq, test_para['read_out_pw'], amp=test_para['read_out_amp'], delay=test_para['read_out_delay'], replay_cont=0)
            mul_freq = freq * 1e6 # 设定采集解模频率
            mul_f = [[mul_phase, mul_freq]] # 构建解模参数列表
            qcs220.setValue("MUL_F_Data", mul_f, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
            qcs220.setValue("MUL_SetPars", 0, chn=adc_chennel_num) # 更新参数
            # ctp100.trigger_open()
            qcs220.run()  # 启动反射测量过程，DAC输出激励波形，ADC采集解模
            time.sleep(0.01)
            mul_data = qcs220.getResult(ch = chinfo, option="IQ") # 从设备获取指定通道原始数据
            muldata = np.array(mul_data).T[0]
            for i in range(len(muldata)):
                muldata[i] = complex(muldata[i])
            y_mod = np.abs(np.mean(muldata) / read_data_len / (2**13-1))
            test_data['x'].append(freq)
            test_data['y'].append(y_mod)
            finish_len += 1
        saveResult(result_name, test_data, test_index, now_time)
    except:
        stop_flag = True
    finally:
        t1.join()

def sweep_bit_freq():
    """测试6：扫bit频率"""
    global stop_flag, finish_len, all_len, test_data
    try:
        test_index = 6
        stop_flag = False
        now_time = datetime.datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
        result_name = f'6_扫bit频率_{env_para["qubit"]}_{now_time}'
        test_data.clear()
        qcs220.stop()
        close_qcs220_all_channels()
        # ctp100.trigger_close()
        # ctp100.trigger_ctrl(int(test_para['trig_ch']),trig_para)
        adc_chennel_num = int(test_para['read_in_ch']) # 参数化通道编号
        dac_chennel_num = int(test_para['read_out_ch']) # 参数化通道编号
        xy_timelen = test_para['xy_pw']
        xy_delay = test_para['xy_delay']
        ad_trigger_delay = 260e-9 + xy_timelen  + xy_delay + test_para['read_in_delay'] #AD采集延迟，样点数量，用户可以根据采样率5Gsps和时间计算取整后得到
        mul_freq = test_para['read_out_freq'] * 1e6 # 设定采集解模频率
        mul_phase = 0 # 设定采集解模初始相位为0°
        read_data_len = round(test_para['read_in_pw']*2.5e9) # 设定总采集解模样点数量，最高131072点
        mul_f = [[mul_phase, mul_freq]] # 构建解模参数列表
        qcs220.setValue("TriggerOff", 0) #关闭设备对触发源的相应，才能进行配置
        qcs220.setValue("TriggerSource", "Internal" if test_para['trig_mode'] == 0 else 'External') #触发源，Internal（内触发），External（外触发）
        qcs220.setValue("TriggerPeriod", trig_para['trigger_us']*1e-6) #内部触发周期，单位s
        qcs220.setValue("TriggerNumber", int(test_para['shots'])) #内部触发次数
        qcs220.setValue("TriggerContinue", trig_para['trigger_continue']) #内部触发连续触发模式，1开启，0关闭
        qcs220.setValue("MUL_Times", int(test_para['shots']), chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
        qcs220.setValue("MUL_F_Len", read_data_len, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
        qcs220.setValue("MUL_F_Data", mul_f, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
        qcs220.setValue("DAC_Replay_count", int(test_para['shots']),chn=dac_chennel_num) #内部触发次数
        qcs220.setValue("DAC_Relpay_continue", trig_para['trigger_continue'],chn=dac_chennel_num) #内部触发连续触发模式，1开启，0关闭
        qcs220.setValue('DAC_Offset', test_para['zbias'], chn=int(test_para['z_ch']))
        set_qcs220_freq(int(test_para['read_out_ch']), test_para['read_out_freq'], test_para['read_out_pw'], amp=test_para['read_out_amp'], delay=xy_delay + xy_timelen + test_para['read_out_delay'], replay_cont=0)
        chinfo = [0, adc_chennel_num]  # 构建获取通道数据通道列表
        freq_list = np.around(np.linspace(test_para['sweep_xy_freq']['start'], test_para['sweep_xy_freq']['end'],
                                round(abs(test_para['sweep_xy_freq']['end'] - test_para['sweep_xy_freq']['start'])/test_para['sweep_xy_freq']['step']) + 1), 2)
        all_len = len(freq_list)
        finish_len = 0
        t1 = threading.Thread(target=draw_line_chart,args=(result_dir,result_name,'sweep_bit_freq','freq/MHz','mod',))
        t1.start()
        for freq in freq_list:
            if stop_flag:
                break
            qcs220.stop()
            # ctp100.trigger_close()
            set_xy_freq(int(test_para['xy_ch']), freq, xy_timelen, amp=test_para['xy_amp'], delay=xy_delay, wave_type = test_para['xy_wave_type'])
            qcs220.setValue("MUL_TriggerDelay", ad_trigger_delay, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
            qcs220.setValue("MUL_SetPars", 0, chn=adc_chennel_num) # 更新参数
            # ctp100.trigger_open()
            qcs220.run()  # 启动反射测量过程，DAC输出激励波形，ADC采集解模
            time.sleep(0.01)
            mul_data = qcs220.getResult(ch = chinfo, option="IQ") # 从设备获取指定通道原始数据
            muldata = np.array(mul_data).T[0]
            for i in range(len(muldata)):
                muldata[i] = complex(muldata[i])
            y_mod = np.abs(np.mean(muldata) / read_data_len / (2**13-1))
            test_data['x'].append(freq)
            test_data['y'].append(y_mod)
            finish_len += 1
        saveResult(result_name, test_data, test_index, now_time)
    except:
        stop_flag = True
    finally:
        t1.join()


def sweep_zbias_bit_freq():
    """测试7：Z偏置扫bit频率"""
    global stop_flag, finish_len, all_len, test_data, heatmap_mask
    try:
        test_index = 7
        stop_flag = False
        now_time = datetime.datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
        result_name = f'7_Z偏置扫bit频率_{env_para["qubit"]}_{now_time}'
        test_data.clear()
        qcs220.stop()
        close_qcs220_all_channels()
        # ctp100.trigger_close()
        # ctp100.trigger_ctrl(int(test_para['trig_ch']),trig_para)
        adc_chennel_num = int(test_para['read_in_ch']) # 参数化通道编号
        dac_chennel_num = int(test_para['read_out_ch']) # 参数化通道编号
        mul_freq = test_para['read_out_freq'] * 1e6 # 设定采集解模频率
        mul_phase = 0 # 设定采集解模初始相位为0°
        read_data_len = round(test_para['read_in_pw']*2.5e9) # 设定总采集解模样点数量，最高131072点
        mul_f = [[mul_phase, mul_freq]] # 构建解模参数列表
        qcs220.setValue("TriggerOff", 0) #关闭设备对触发源的相应，才能进行配置
        qcs220.setValue("TriggerSource", "Internal" if test_para['trig_mode'] == 0 else 'External') #触发源，Internal（内触发），External（外触发）
        qcs220.setValue("TriggerPeriod", trig_para['trigger_us']*1e-6) #内部触发周期，单位s
        qcs220.setValue("TriggerNumber", int(test_para['shots'])) #内部触发次数
        qcs220.setValue("TriggerContinue", trig_para['trigger_continue']) #内部触发连续触发模式，1开启，0关闭
        qcs220.setValue("MUL_Times", int(test_para['shots']), chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
        qcs220.setValue("MUL_F_Len", read_data_len, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
        qcs220.setValue("MUL_F_Data", mul_f, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
        ad_trigger_delay = 260e-9 + test_para['xy_pw'] + test_para['xy_delay'] + test_para['read_in_delay'] #AD采集延迟，样点数量，用户可以根据采样率5Gsps和时间计算取整后得到
        qcs220.setValue("MUL_TriggerDelay", ad_trigger_delay, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
        qcs220.setValue("DAC_TriggerDelay", trig_para['trigger_delay'],chn=dac_chennel_num) #内部触发周期，单位s
        qcs220.setValue("DAC_Replay_count", int(test_para['shots']),chn=dac_chennel_num) #内部触发次数
        qcs220.setValue("DAC_Relpay_continue", trig_para['trigger_continue'],chn=dac_chennel_num) #内部触发连续触发模式，1开启，0关闭
        set_qcs220_freq(int(test_para['read_out_ch']), test_para['read_out_freq'], test_para['read_out_pw'], amp=test_para['read_out_amp'], delay=test_para['xy_delay'] + test_para['read_out_delay'] + test_para['xy_pw'], replay_cont=0)
        chinfo = [0, adc_chennel_num]  # 构建获取通道数据通道列表
        y_amp_list = np.around(np.linspace(test_para['sweep_z_amp']['start'], test_para['sweep_z_amp']['end'],
                        round(abs(test_para['sweep_z_amp']['end'] - test_para['sweep_z_amp']['start'])/test_para['sweep_z_amp']['step']) + 1), 2)
        x_freq_list = np.around(np.linspace(test_para['sweep_xy_freq']['start'], test_para['sweep_xy_freq']['end'],
                                round(abs(test_para['sweep_xy_freq']['end'] - test_para['sweep_xy_freq']['start'])/test_para['sweep_xy_freq']['step']) + 1), 2)
        test_data['x'] = x_freq_list
        test_data['y'] = y_amp_list
        z_temp = []
        for i in range(len(x_freq_list)):
            z_temp.append(np.zeros_like(y_amp_list))
        test_data['z'] = z_temp
        heatmap_mask = (np.random.randint(1,size=(len(x_freq_list),len(y_amp_list)))==0)
        all_len = len(x_freq_list) * len(y_amp_list)
        finish_len = 0
        t1 = threading.Thread(target=draw_heatmap_chart,args=(result_dir,result_name,'sweep_zbias_bit_freq','zbais','freq/MHz',))
        t1.start()
        for ix in range(len(x_freq_list)):
            freq = x_freq_list[ix]
            for iy in range(len(y_amp_list)):
                if stop_flag:
                    break
                z_amp = y_amp_list[iy]
                # ctp100.trigger_close()
                qcs220.stop()
                set_xy_freq(int(test_para['xy_ch']), freq, test_para['xy_pw'], amp = test_para['xy_amp'], delay = test_para['xy_delay'],wave_type = test_para['xy_wave_type'])
                qcs220.setValue('DAC_Offset', z_amp, chn=int(test_para['z_ch']))
                qcs220.setValue("MUL_SetPars", 0, chn=adc_chennel_num) # 更新参数
                # ctp100.trigger_open()
                qcs220.run()  # 启动反射测量过程，DAC输出激励波形，ADC采集解模
                time.sleep(0.01)
                mul_data = qcs220.getResult(ch = chinfo, option="IQ") # 从设备获取指定通道原始数据
                muldata = np.array(mul_data).T[0]
                for i in range(len(muldata)):
                    muldata[i] = complex(muldata[i])
                test_data['z'][ix][iy] = np.abs(np.mean(muldata) / read_data_len / (2**13-1))
                heatmap_mask[ix][iy] = False
                finish_len = ix * len(y_amp_list) + iy + 1
        saveResult(result_name, test_data, test_index, now_time)
    except:
        stop_flag = True
    finally:
        t1.join()

def rabi_amp():
    """测试8：RABI幅度"""
    global stop_flag, finish_len, all_len, test_data
    try:
        test_index = 8
        stop_flag = False
        now_time = datetime.datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
        result_name = f'8_RABI幅度_{env_para["qubit"]}_{now_time}'
        test_data.clear()
        qcs220.stop()
        close_qcs220_all_channels()
        # ctp100.trigger_close()
        # ctp100.trigger_ctrl(int(test_para['trig_ch']),trig_para)
        adc_chennel_num = int(test_para['read_in_ch']) # 参数化通道编号
        dac_chennel_num = int(test_para['read_out_ch']) # 参数化通道编号
        mul_freq = test_para['read_out_freq'] * 1e6 # 设定采集解模频率
        mul_phase = 0 # 设定采集解模初始相位为0°
        read_data_len = round(test_para['read_in_pw']*2.5e9) # 设定总采集解模样点数量，最高131072点
        mul_f = [[mul_phase, mul_freq]] # 构建解模参数列表
        qcs220.setValue("TriggerOff", 0) #关闭设备对触发源的相应，才能进行配置
        qcs220.setValue("TriggerSource", "Internal" if test_para['trig_mode'] == 0 else 'External') #触发源，Internal（内触发），External（外触发）
        qcs220.setValue("TriggerPeriod", trig_para['trigger_us']*1e-6) #内部触发周期，单位s
        qcs220.setValue("TriggerNumber", int(test_para['shots'])) #内部触发次数
        qcs220.setValue("TriggerContinue", trig_para['trigger_continue']) #内部触发连续触发模式，1开启，0关闭
        qcs220.setValue("MUL_Times", int(test_para['shots']), chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
        qcs220.setValue("MUL_F_Len", read_data_len, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
        qcs220.setValue("MUL_F_Data", mul_f, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
        ad_trigger_delay = 260e-9 + test_para['xy_pw'] + test_para['xy_delay'] + test_para['read_in_delay'] #AD采集延迟，样点数量，用户可以根据采样率5Gsps和时间计算取整后得到
        qcs220.setValue("MUL_TriggerDelay", ad_trigger_delay, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
        qcs220.setValue("DAC_TriggerDelay", trig_para['trigger_delay'],chn=dac_chennel_num) #内部触发周期，单位s
        qcs220.setValue("DAC_Replay_count", int(test_para['shots']),chn=dac_chennel_num) #内部触发次数
        qcs220.setValue("DAC_Relpay_continue", trig_para['trigger_continue'],chn=dac_chennel_num) #内部触发连续触发模式，1开启，0关闭
        qcs220.setValue('DAC_Offset', test_para['zbias'], chn=int(test_para['z_ch']))
        set_qcs220_freq(int(test_para['read_out_ch']), test_para['read_out_freq'], test_para['read_out_pw'], amp=test_para['read_out_amp'], delay=test_para['xy_delay'] + test_para['xy_pw'] + test_para['read_out_delay'], replay_cont=0)
        chinfo = [0, adc_chennel_num]  # 构建获取通道数据通道列表
        amp_list = np.around(np.linspace(test_para['sweep_xy_amp']['start'], test_para['sweep_xy_amp']['end'],
                        round(abs(test_para['sweep_xy_amp']['end'] - test_para['sweep_xy_amp']['start'])/test_para['sweep_xy_amp']['step']) + 1), 2)
        all_len = len(amp_list)
        finish_len = 0
        t1 = threading.Thread(target=draw_line_chart,args=(result_dir,result_name,'rabi_amp','xy_amp','mod',))
        t1.start()
        for amp in amp_list:
            if stop_flag:
                break
            # ctp100.trigger_close()
            qcs220.stop()
            set_xy_freq(int(test_para['xy_ch']), test_para['xy_freq'], test_para['xy_pw'], amp, delay=test_para['xy_delay'])
            qcs220.setValue("MUL_SetPars", 0, chn=adc_chennel_num) # 更新参数
            # ctp100.trigger_open()
            qcs220.run()  # 启动反射测量过程，DAC输出激励波形，ADC采集解模
            time.sleep(0.01)
            mul_data = qcs220.getResult(ch = chinfo, option="IQ") # 从设备获取指定通道原始数据
            muldata = np.array(mul_data).T[0]
            for i in range(len(muldata)):
                muldata[i] = complex(muldata[i])
            y_mod = np.abs(np.mean(muldata)) / read_data_len / (2**13-1)
            test_data['x'].append(amp)
            test_data['y'].append(y_mod)
            finish_len += 1
        saveResult(result_name, test_data, test_index, now_time)
    except:
        stop_flag = True
    finally:
        t1.join()

def rabi_pw():
    """测试9：RABI脉宽"""
    global stop_flag, finish_len, all_len, test_data
    try:
        test_index = 9
        stop_flag = False
        now_time = datetime.datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
        result_name = f'9_RABI脉宽_{env_para["qubit"]}_{now_time}'
        test_data.clear()
        qcs220.stop()
        close_qcs220_all_channels()
        # ctp100.trigger_close()
        # ctp100.trigger_ctrl(int(test_para['trig_ch']),trig_para)
        adc_chennel_num = int(test_para['read_in_ch']) # 参数化通道编号
        dac_chennel_num = int(test_para['read_out_ch']) # 参数化通道编号
        mul_freq = test_para['read_out_freq'] * 1e6 # 设定采集解模频率
        mul_phase = 0 # 设定采集解模初始相位为0°
        read_data_len = round(test_para['read_in_pw']*2.5e9) # 设定总采集解模样点数量，最高131072点
        mul_f = [[mul_phase, mul_freq]] # 构建解模参数列表
        qcs220.setValue("TriggerOff", 0) #关闭设备对触发源的相应，才能进行配置
        qcs220.setValue("TriggerSource", "Internal" if test_para['trig_mode'] == 0 else 'External') #触发源，Internal（内触发），External（外触发）
        qcs220.setValue("TriggerPeriod", trig_para['trigger_us']*1e-6) #内部触发周期，单位s
        qcs220.setValue("TriggerNumber", int(test_para['shots'])) #内部触发次数
        qcs220.setValue("TriggerContinue", trig_para['trigger_continue']) #内部触发连续触发模式，1开启，0关闭
        qcs220.setValue("MUL_Times", int(test_para['shots']), chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
        qcs220.setValue("MUL_F_Len", read_data_len, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
        qcs220.setValue("MUL_F_Data", mul_f, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
        qcs220.setValue("DAC_TriggerDelay", trig_para['trigger_delay'],chn=dac_chennel_num) #内部触发周期，单位s
        qcs220.setValue("DAC_Replay_count", int(test_para['shots']),chn=dac_chennel_num) #内部触发次数
        qcs220.setValue("DAC_Relpay_continue", trig_para['trigger_continue'],chn=dac_chennel_num) #内部触发连续触发模式，1开启，0关闭
        qcs220.setValue('DAC_Offset', test_para['zbias'], chn=int(test_para['z_ch']))
        chinfo = [0, adc_chennel_num]  # 构建获取通道数据通道列表
        delay_list = np.linspace(test_para['sweep_xy_pw']['start'], test_para['sweep_xy_pw']['end'],
                                round(abs(test_para['sweep_xy_pw']['end'] - test_para['sweep_xy_pw']['start'])/test_para['sweep_xy_pw']['step']) + 1)
        all_len = len(delay_list)
        finish_len = 0
        t1 = threading.Thread(target=draw_line_chart,args=(result_dir,result_name,'rabi_pw','xy_pulse_len/ns','mod',))
        t1.start()
        for add_delay in delay_list:
            if stop_flag:
                break
            # ctp100.trigger_close()
            qcs220.stop()
            set_qcs220_freq(int(test_para['read_out_ch']), test_para['read_out_freq'], test_para['read_out_pw'], amp=test_para['read_out_amp'], delay=test_para['xy_delay'] + add_delay + test_para['read_out_delay'], replay_cont=0)
            set_xy_freq(int(test_para['xy_ch']), test_para['xy_freq'], add_delay, amp=test_para['xy_amp'], delay=test_para['xy_delay'],wave_type = test_para['xy_wave_type']) 
            ad_trigger_delay = 260e-9 + add_delay + test_para['xy_delay'] + test_para['read_in_delay'] #AD采集延迟，样点数量，用户可以根据采样率5Gsps和时间计算取整后得到
            qcs220.setValue("MUL_TriggerDelay", ad_trigger_delay, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
            qcs220.setValue("MUL_SetPars", 0, chn=adc_chennel_num) # 更新参数
            # ctp100.trigger_open()
            qcs220.run()  # 启动反射测量过程，DAC输出激励波形，ADC采集解模
            time.sleep(0.01)
            mul_data = qcs220.getResult(ch = chinfo, option="IQ") # 从设备获取指定通道原始数据
            muldata = np.array(mul_data).T[0]
            for i in range(len(muldata)):
                muldata[i] = complex(muldata[i])
            y_mod = np.abs(np.mean(muldata)) / read_data_len / (2**13-1)
            test_data['x'].append(add_delay*1e9)
            test_data['y'].append(y_mod)
            finish_len += 1
        saveResult(result_name, test_data, test_index, now_time)
    except:
        stop_flag = True
    finally:
        t1.join()

def t1_test():
    """测试10：T1测量"""
    global stop_flag, finish_len, all_len, test_data
    try:
        test_index = 10
        stop_flag = False
        now_time = datetime.datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
        result_name = f'10_T1测量_{env_para["qubit"]}_{now_time}'
        test_data.clear()
        qcs220.stop()
        close_qcs220_all_channels()
        # ctp100.trigger_close()
        # ctp100.trigger_ctrl(int(test_para['trig_ch']),trig_para)
        adc_chennel_num = int(test_para['read_in_ch']) # 参数化通道编号
        dac_chennel_num = int(test_para['read_out_ch']) # 参数化通道编号
        mul_freq = test_para['read_out_freq'] * 1e6 # 设定采集解模频率
        mul_phase = 0 # 设定采集解模初始相位为0°
        read_data_len = round(test_para['read_in_pw']*2.5e9) # 设定总采集解模样点数量，最高131072点
        mul_f = [[mul_phase, mul_freq]] # 构建解模参数列表
        qcs220.setValue("TriggerOff", 0) #关闭设备对触发源的相应，才能进行配置
        qcs220.setValue("TriggerSource", "Internal" if test_para['trig_mode'] == 0 else 'External') #触发源，Internal（内触发），External（外触发）
        qcs220.setValue("TriggerPeriod", trig_para['trigger_us']*1e-6) #内部触发周期，单位s
        qcs220.setValue("TriggerNumber", int(test_para['shots'])) #内部触发次数
        qcs220.setValue("TriggerContinue", trig_para['trigger_continue']) #内部触发连续触发模式，1开启，0关闭
        qcs220.setValue("MUL_Times", int(test_para['shots']), chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
        qcs220.setValue("MUL_F_Len", read_data_len, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
        qcs220.setValue("MUL_F_Data", mul_f, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
        qcs220.setValue("DAC_TriggerDelay", trig_para['trigger_delay'],chn=dac_chennel_num) #内部触发周期，单位s
        qcs220.setValue("DAC_Replay_count", int(test_para['shots']),chn=dac_chennel_num) #内部触发次数
        qcs220.setValue("DAC_Relpay_continue", trig_para['trigger_continue'],chn=dac_chennel_num) #内部触发连续触发模式，1开启，0关闭
        qcs220.setValue('DAC_Offset', test_para['zbias'], chn=int(test_para['z_ch']))
        chinfo = [0, adc_chennel_num]  # 构建获取通道数据通道列表
        delay_list = np.linspace(test_para['sweep_read_delay']['start'], test_para['sweep_read_delay']['end'],
                        round(abs(test_para['sweep_read_delay']['end'] - test_para['sweep_read_delay']['start'])/test_para['sweep_read_delay']['step']) + 1)
        all_len = len(delay_list)
        finish_len = 0
        t1 = threading.Thread(target=draw_line_chart,args=(result_dir,result_name,'t1','tau/ns','mod',))
        t1.start()
        for add_delay in delay_list:
            if stop_flag:
                break
            # ctp100.trigger_close()
            qcs220.stop()
            set_qcs220_freq(int(test_para['read_out_ch']), test_para['read_out_freq'], test_para['read_out_pw'], amp=test_para['read_out_amp'], delay=test_para['xy_delay'] + test_para['xy_pw'] + add_delay + test_para['read_out_delay'], replay_cont=0)
            set_xy_freq(int(test_para['xy_ch']), test_para['xy_freq'], test_para['xy_pw'], amp=test_para['xy_amp'], delay=test_para['xy_delay'],wave_type = test_para['xy_wave_type']) 
            ad_trigger_delay = 260e-9 + test_para['xy_pw'] + test_para['xy_delay'] + test_para['read_in_delay'] + add_delay #AD采集延迟，样点数量，用户可以根据采样率5Gsps和时间计算取整后得到
            qcs220.setValue("MUL_TriggerDelay", ad_trigger_delay, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
            qcs220.setValue("MUL_SetPars", 0, chn=adc_chennel_num) # 更新参数
            # ctp100.trigger_open()
            qcs220.run()  # 启动反射测量过程，DAC输出激励波形，ADC采集解模
            time.sleep(0.01)
            mul_data = qcs220.getResult(ch = chinfo, option="IQ") # 从设备获取指定通道原始数据
            muldata = np.array(mul_data).T[0]
            for i in range(len(muldata)):
                muldata[i] = complex(muldata[i])
            y_mod = np.abs(np.mean(muldata)) / read_data_len / (2**13-1)
            test_data['x'].append(add_delay*1e9)
            test_data['y'].append(y_mod)
            finish_len += 1
        saveResult(result_name, test_data, test_index, now_time)
        t1.join()
        T1_match(test_data['x'],test_data['y'],result_dir,result_name.replace('test','match'))
    except:
        stop_flag = True
        t1.join()

def t2_test():
    """测试11：T2测量"""
    global stop_flag, finish_len, all_len, test_data
    try:
        test_index = 11
        stop_flag = False
        now_time = datetime.datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
        result_name = f'11_T2测量_{env_para["qubit"]}_{now_time}'
        test_data.clear()
        qcs220.stop()
        close_qcs220_all_channels()
        # ctp100.trigger_close()
        # ctp100.trigger_ctrl(int(test_para['trig_ch']),trig_para)
        adc_chennel_num = int(test_para['read_in_ch']) # 参数化通道编号
        dac_chennel_num = int(test_para['read_out_ch']) # 参数化通道编号
        mul_freq = test_para['read_out_freq'] * 1e6 # 设定采集解模频率
        mul_phase = 0 # 设定采集解模初始相位为0°
        read_data_len = round(test_para['read_in_pw']*2.5e9) # 设定总采集解模样点数量，最高131072点
        mul_f = [[mul_phase, mul_freq]] # 构建解模参数列表
        qcs220.setValue("TriggerOff", 0) #关闭设备对触发源的相应，才能进行配置
        qcs220.setValue("TriggerSource", "Internal" if test_para['trig_mode'] == 0 else 'External') #触发源，Internal（内触发），External（外触发）
        qcs220.setValue("TriggerPeriod", trig_para['trigger_us']*1e-6) #内部触发周期，单位s
        qcs220.setValue("TriggerNumber", int(test_para['shots'])) #内部触发次数
        qcs220.setValue("TriggerContinue", trig_para['trigger_continue']) #内部触发连续触发模式，1开启，0关闭
        qcs220.setValue("MUL_Times", int(test_para['shots']), chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
        qcs220.setValue("MUL_F_Len", read_data_len, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
        qcs220.setValue("MUL_F_Data", mul_f, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
        qcs220.setValue("DAC_TriggerDelay", trig_para['trigger_delay'],chn=dac_chennel_num) #内部触发周期，单位s
        qcs220.setValue("DAC_Replay_count", int(test_para['shots']),chn=dac_chennel_num) #内部触发次数
        qcs220.setValue("DAC_Relpay_continue", trig_para['trigger_continue'],chn=dac_chennel_num) #内部触发连续触发模式，1开启，0关闭
        qcs220.setValue('DAC_Offset', test_para['zbias'], chn=int(test_para['z_ch']))
        chinfo = [0, adc_chennel_num]  # 构建获取通道数据通道列表
        t_list = np.linspace(test_para['sweep_t_delay']['start'], test_para['sweep_t_delay']['end'],
                            round(abs(test_para['sweep_t_delay']['end'] - test_para['sweep_t_delay']['start'])/test_para['sweep_t_delay']['step']) + 1)
        all_len = len(t_list)
        finish_len = 0
        t1 = threading.Thread(target=draw_line_chart,args=(result_dir,result_name,'t2','t2(ns)','mod',))
        t1.start()
        for t in t_list:
            if stop_flag:
                break
            # ctp100.trigger_close()
            qcs220.stop()
            xy_delay = test_para['xy_delay']
            xy_one_pluse_timelen = test_para['xy_pw']
            xy_all_timelen = xy_one_pluse_timelen * 2 + t 
            set_qcs220_freq(int(test_para['read_out_ch']), test_para['read_out_freq'], test_para['read_out_pw'], amp=test_para['read_out_amp'], delay=xy_delay + xy_all_timelen + test_para['read_out_delay'], replay_cont=0)
            set_xy_2_freq(int(test_para['xy_ch']), np.round((test_para['xy_freq']-test_para['xy_freq_offset']),2), xy_one_pluse_timelen, amp=test_para['xy_amp'], ts = t,tDelay=xy_delay,wave_type = test_para['xy_wave_type'])    
            ad_trigger_delay = 260e-9 + xy_all_timelen + xy_delay + test_para['read_in_delay']  #AD采集延迟，样点数量，用户可以根据采样率5Gsps和时间计算取整后得到
            qcs220.setValue("MUL_TriggerDelay", ad_trigger_delay, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
            qcs220.setValue("MUL_SetPars", 0, chn=adc_chennel_num) # 更新参数
            # ctp100.trigger_open()
            qcs220.run()  # 启动反射测量过程，DAC输出激励波形，ADC采集解模
            time.sleep(0.01)
            mul_data = qcs220.getResult(ch = chinfo, option="IQ") # 从设备获取指定通道原始数据
            muldata = np.array(mul_data).T[0]
            for i in range(len(muldata)):
                muldata[i] = complex(muldata[i])
            y_mod = np.abs(np.mean(muldata)) / read_data_len / (2**13-1)
            test_data['x'].append(t*1e9)
            test_data['y'].append(y_mod)
            finish_len += 1
        saveResult(result_name, test_data, test_index, now_time)
        t1.join()
        T2_match(test_data['x'],test_data['y'],result_dir,result_name.replace('test','match'),test_para['xy_freq_offset'])
    except:
        stop_flag = True
        t1.join()

def t2_spin_echo():
    """测试11：T2自旋回波"""
    global stop_flag, finish_len, all_len, test_data
    try:
        test_index = 11
        stop_flag = False
        now_time = datetime.datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
        result_name = f'11_T2自旋回波_{env_para["qubit"]}_{now_time}'
        test_data.clear()
        qcs220.stop()
        close_qcs220_all_channels()
        # ctp100.trigger_close()
        # ctp100.trigger_ctrl(int(test_para['trig_ch']),trig_para)
        adc_chennel_num = int(test_para['read_in_ch']) # 参数化通道编号
        dac_chennel_num = int(test_para['read_out_ch']) # 参数化通道编号
        mul_freq = test_para['read_out_freq'] * 1e6 # 设定采集解模频率
        mul_phase = 0 # 设定采集解模初始相位为0°
        read_data_len = round(test_para['read_in_pw']*2.5e9) # 设定总采集解模样点数量，最高131072点
        mul_f = [[mul_phase, mul_freq]] # 构建解模参数列表
        qcs220.setValue("TriggerOff", 0) #关闭设备对触发源的相应，才能进行配置
        qcs220.setValue("TriggerSource", "Internal" if test_para['trig_mode'] == 0 else 'External') #触发源，Internal（内触发），External（外触发）
        qcs220.setValue("TriggerPeriod", trig_para['trigger_us']*1e-6) #内部触发周期，单位s
        qcs220.setValue("TriggerNumber", int(test_para['shots'])) #内部触发次数
        qcs220.setValue("TriggerContinue", trig_para['trigger_continue']) #内部触发连续触发模式，1开启，0关闭
        qcs220.setValue("MUL_Times", int(test_para['shots']), chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
        qcs220.setValue("MUL_F_Len", read_data_len, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
        qcs220.setValue("MUL_F_Data", mul_f, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
        qcs220.setValue("DAC_TriggerDelay", trig_para['trigger_delay'],chn=dac_chennel_num) #内部触发周期，单位s
        qcs220.setValue("DAC_Replay_count", int(test_para['shots']),chn=dac_chennel_num) #内部触发次数
        qcs220.setValue("DAC_Relpay_continue", trig_para['trigger_continue'],chn=dac_chennel_num) #内部触发连续触发模式，1开启，0关闭
        qcs220.setValue('DAC_Offset', test_para['zbias'], chn=int(test_para['z_ch']))
        chinfo = [0, adc_chennel_num]  # 构建获取通道数据通道列表
        t_list = np.linspace(test_para['sweep_t_delay']['start'], test_para['sweep_t_delay']['end'],
                            round(abs(test_para['sweep_t_delay']['end'] - test_para['sweep_t_delay']['start'])/test_para['sweep_t_delay']['step']) + 1)
        all_len = len(t_list)
        finish_len = 0
        t1 = threading.Thread(target=draw_line_chart,args=(result_dir,result_name,'t2_spin_echo','t2(ns)','mod',))
        t1.start()
        for t in t_list:
            if stop_flag:
                break
            # ctp100.trigger_close()
            qcs220.stop()
            xy_delay = test_para['xy_delay']
            xy_one_pluse_timelen = test_para['xy_pw']
            xy_all_timelen = xy_one_pluse_timelen * 2 + t 
            set_qcs220_freq(int(test_para['read_out_ch']), test_para['read_out_freq'], test_para['read_out_pw'], amp=test_para['read_out_amp'], delay=xy_delay + xy_all_timelen + test_para['read_out_delay'], replay_cont=0)
            set_xy_3_pulse(int(test_para['xy_ch']), test_para['xy_freq'], xy_one_pluse_timelen, amp=test_para['xy_amp'], ts = t,tDelay=xy_delay,wave_type = test_para['xy_wave_type'])    
            ad_trigger_delay = 260e-9 + xy_all_timelen + xy_delay + test_para['read_in_delay']  #AD采集延迟，样点数量，用户可以根据采样率5Gsps和时间计算取整后得到
            qcs220.setValue("MUL_TriggerDelay", ad_trigger_delay, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
            qcs220.setValue("MUL_SetPars", 0, chn=adc_chennel_num) # 更新参数
            # ctp100.trigger_open()
            qcs220.run()  # 启动反射测量过程，DAC输出激励波形，ADC采集解模
            time.sleep(0.01)
            mul_data = qcs220.getResult(ch = chinfo, option="IQ") # 从设备获取指定通道原始数据
            muldata = np.array(mul_data).T[0]
            for i in range(len(muldata)):
                muldata[i] = complex(muldata[i])
            y_mod = np.abs(np.mean(muldata)) / read_data_len / (2**13-1)
            test_data['x'].append(t*1e9)
            test_data['y'].append(y_mod)
            finish_len += 1
        saveResult(result_name, test_data, test_index, now_time)
        t1.join()
        T2_match(test_data['x'],test_data['y'],result_dir,result_name.replace('test','match'),test_para['xy_freq_offset'])
    except:
        stop_flag = True
        t1.join()

def __getstate_01IQ(test_para,trig_para):
    """获取01态IQ数据"""
    qcs220.stop()
    close_qcs220_all_channels()
    # ctp100.trigger_close()
    # ctp100.trigger_ctrl(int(test_para['trig_ch']),trig_para)
    adc_chennel_num = int(test_para['read_in_ch']) # 参数化通道编号
    dac_chennel_num = int(test_para['read_out_ch']) # 参数化通道编号
    mul_freq = test_para['read_out_freq'] * 1e6 # 设定采集解模频率
    mul_phase = 0 # 设定采集解模初始相位为0°
    read_data_len = round(test_para['read_in_pw']*2.5e9) # 设定总采集解模样点数量，最高131072点
    mul_f = [[mul_phase, mul_freq]] # 构建解模参数列表
    qcs220.setValue("TriggerOff", 0) #关闭设备对触发源的相应，才能进行配置
    qcs220.setValue("TriggerSource", "Internal" if test_para['trig_mode'] == 0 else 'External') #触发源，Internal（内触发），External（外触发）
    qcs220.setValue("TriggerPeriod", trig_para['trigger_us']*1e-6) #内部触发周期，单位s
    qcs220.setValue("TriggerNumber", int(test_para['shots'])) #内部触发次数
    qcs220.setValue("TriggerContinue", trig_para['trigger_continue']) #内部触发连续触发模式，1开启，0关闭
    qcs220.setValue("MUL_Times", int(test_para['shots']), chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
    qcs220.setValue("MUL_F_Len", read_data_len, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
    qcs220.setValue("MUL_F_Data", mul_f, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
    ad_trigger_delay = 260e-9 + test_para['xy_pw'] + test_para['xy_delay'] + test_para['read_in_delay']  #AD采集延迟，样点数量，用户可以根据采样率5Gsps和时间计算取整后得到
    qcs220.setValue("MUL_TriggerDelay", ad_trigger_delay, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
    qcs220.setValue("DAC_TriggerDelay", trig_para['trigger_delay'],chn=dac_chennel_num) #内部触发周期，单位s
    qcs220.setValue("DAC_Replay_count", int(test_para['shots']),chn=dac_chennel_num) #内部触发次数
    qcs220.setValue("DAC_Relpay_continue", trig_para['trigger_continue'],chn=dac_chennel_num) #内部触发连续触发模式，1开启，0关闭
    qcs220.setValue('DAC_Offset', test_para['zbias'], chn=int(test_para['z_ch']))
    chinfo = [0, adc_chennel_num]  # 构建获取通道数据通道列表

    set_qcs220_freq(int(test_para['read_out_ch']), test_para['read_out_freq'], test_para['read_out_pw'], amp=test_para['read_out_amp'], delay=test_para['read_out_delay'] + test_para['xy_pw'] + test_para['xy_delay'] , replay_cont=0)
    if test_para['state_01'] == 0:# 0态-不给任何信号
        set_xy_freq(int(test_para['xy_ch']), test_para['xy_freq'], 
                        test_para['xy_pw'], test_para['xy_amp_0state'], test_para['xy_delay'],wave_type = test_para['xy_wave_type'] ) 
    elif test_para['state_01'] == 1: # 1态-XY给高斯脉冲
        set_xy_freq(int(test_para['xy_ch']), test_para['xy_freq'], 
                        test_para['xy_pw'], test_para['xy_amp_1state'], test_para['xy_delay'],wave_type = test_para['xy_wave_type'] ) 
    elif test_para['state_01'] == 2: # 叠加态
        set_xy_freq(int(test_para['xy_ch']), test_para['xy_freq'], 
                        test_para['xy_pw'], test_para['xy_amp_muxstate'], test_para['xy_delay'],wave_type = test_para['xy_wave_type'] )   
    else:
        pass
    qcs220.setValue("MUL_SetPars", 0, chn=adc_chennel_num) # 更新参数
    # ctp100.trigger_open()
    qcs220.run()  # 启动反射测量过程，DAC输出激励波形，ADC采集解模
    time.sleep(0.01)
    mul_data = qcs220.getResult(ch = chinfo, option="IQ") # 从设备获取指定通道原始数据
    muldata = np.array(mul_data).T[0]
    real,imag=[],[]    
    for i in range(read_data_len):
        muldata[i] = complex(muldata[i])
        real.append(muldata[i].real/read_data_len)
        imag.append(muldata[i].imag/read_data_len)
    return real,imag,np.abs(np.mean(muldata)/read_data_len/(2**13-1))

def qubit_fidelity():
    """测试12：01态保真度"""
    global stop_flag
    try:
        test_index = 12
        stop_flag = False
        now_time = datetime.datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
        test_data.clear()

        test_para["state_01"] = 0
        x0,y0,mod0 = __getstate_01IQ(test_para,trig_para)
        test_para["state_01"] = 1
        x1,y1,mod1 = __getstate_01IQ(test_para,trig_para)
        for  i in range(len(x0)):
            test_data['x0'].append(x0[i])
            test_data['y0'].append(y0[i])
            test_data['x1'].append(x1[i])
            test_data['y1'].append(y1[i])

        result_name = f'12_01态保真度_{env_para["qubit"]}_mod_{now_time}'
        saveResult(result_name, test_data, test_index, now_time)

        plt.figure(figsize = (8, 8))
        ax = plt.subplot(2,2,1)
        ax.scatter(x0, y0, s = 9, c = 'red', label='|0⟩')
        ax.scatter(x1, y1, s = 9, c = 'blue', label='|1⟩')
        ax.legend(loc='upper right')

        ax = plt.subplot(2,2,2)
        ax.text(0.2, 0.6, f"mod0:{mod0}")
        ax.text(0.2, 0.5, f"mod1:{mod1}")

        ax = plt.subplot(2,2,3)
        ax.scatter(x0, y0, s = 9, c = 'red', label='|0⟩')
        ax.legend( loc='upper right')

        ax = plt.subplot(2,2,4)
        ax.scatter(x1, y1,  s = 9, c = 'blue', label='|1⟩')
        ax.legend(loc='upper right')

        plt.savefig(f'{result_dir}/{result_name}.png',bbox_inches='tight')
        plt.show()
        fidelity(np.asarray(x0),np.asarray(y0),np.asarray(x1),np.asarray(y1),result_dir,result_name)
    except:
        stop_flag = True

def __sweep_freq_01state(qubit_st,test_para,trig_para):
    """01态扫腔频测试函数"""
    qcs220.stop()
    close_qcs220_all_channels()
    # ctp100.trigger_close()
    # ctp100.trigger_ctrl(int(test_para['trig_ch']),trig_para)
    adc_chennel_num = int(test_para['read_in_ch']) # 参数化通道编号
    dac_chennel_num = int(test_para['read_out_ch']) # 参数化通道编号
    mul_phase = 0 # 设定采集解模初始相位为0°
    read_data_len = round(test_para['read_in_pw']*2.5e9) # 设定总采集解模样点数量，最高131072点
    qcs220.setValue("TriggerOff", 0) #关闭设备对触发源的相应，才能进行配置
    qcs220.setValue("TriggerSource", "Internal" if test_para['trig_mode'] == 0 else 'External') #触发源，Internal（内触发），External（外触发）
    qcs220.setValue("TriggerPeriod", trig_para['trigger_us']*1e-6) #内部触发周期，单位s
    qcs220.setValue("TriggerNumber", int(test_para['shots'])) #内部触发次数
    qcs220.setValue("TriggerContinue", trig_para['trigger_continue']) #内部触发连续触发模式，1开启，0关闭
    qcs220.setValue("MUL_Times", int(test_para['shots']), chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
    qcs220.setValue("MUL_F_Len", read_data_len, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
    ad_trigger_delay = 260e-9 + test_para['xy_pw'] + test_para['xy_delay'] + test_para['read_in_delay']  #AD采集延迟，样点数量，用户可以根据采样率5Gsps和时间计算取整后得到
    qcs220.setValue("MUL_TriggerDelay", ad_trigger_delay, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
    qcs220.setValue("DAC_TriggerDelay", trig_para['trigger_delay'],chn=dac_chennel_num) #内部触发周期，单位s
    qcs220.setValue("DAC_Replay_count", int(test_para['shots']),chn=dac_chennel_num) #内部触发次数
    qcs220.setValue("DAC_Relpay_continue", trig_para['trigger_continue'],chn=dac_chennel_num) #内部触发连续触发模式，1开启，0关闭
    qcs220.setValue('DAC_Offset', test_para['zbias'], chn=int(test_para['z_ch']))
    chinfo = [0, adc_chennel_num]  # 构建获取通道数据通道列表
    temp_data = [] 
    y_mod = []
    freq_list = np.around(np.linspace(test_para['sweep_freq']['start'], test_para['sweep_freq']['end'], 
                            round(abs(test_para['sweep_freq']['end'] - test_para['sweep_freq']['start'])/test_para['sweep_freq']['step']) + 1), 2)
    amp = 0 if qubit_st == 0 else test_para['xy_amp']
    for freq in freq_list:
        # ctp100.trigger_close()
        qcs220.stop() 
        set_qcs220_freq(int(test_para['read_out_ch']), freq, test_para['read_out_pw'], amp=test_para['read_out_amp'], delay=test_para['read_out_delay'] + test_para['xy_pw'] + test_para['xy_delay'] , replay_cont=0)
        set_xy_freq(int(test_para['xy_ch']), test_para['xy_freq'], test_para['xy_pw'], amp, test_para['xy_delay'],wave_type = test_para['xy_wave_type'])  
        mul_freq = freq * 1e6 # 设定采集解模频率  
        mul_f = [[mul_phase, mul_freq]] # 构建解模参数列表
        qcs220.setValue("MUL_F_Data", mul_f, chn=adc_chennel_num) # ADC采集相对触发信号延迟，单位s
        qcs220.setValue("MUL_SetPars", 0, chn=adc_chennel_num) # 更新参数
        # ctp100.trigger_open()
        qcs220.run()  # 启动反射测量过程，DAC输出激励波形，ADC采集解模
        time.sleep(0.01)
        mul_data = qcs220.getResult(ch = chinfo, option="IQ") # 从设备获取指定通道原始数据
        muldata = np.array(mul_data).T[0]
        for i in range(len(muldata)):
            muldata[i] = complex(muldata[i])
        temp_data.append(np.mean(muldata))
        y_mod = np.abs(np.asarray(temp_data) /read_data_len / (2**13-1))
    return freq_list, y_mod,temp_data

def sweep_qubit_cavity_freq():
    """测试13：01态扫腔频"""
    global stop_flag
    try:
        test_index = 13
        stop_flag = False
        now_time = datetime.datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
        result_name = f'13_01态扫腔频_{env_para["qubit"]}_{now_time}'
        test_data.clear()
        I0, Q0, res_complex0 = __sweep_freq_01state(0,test_para,trig_para)
        I1, Q1, res_complex1 = __sweep_freq_01state(1,test_para,trig_para)
        delt_Q = np.abs(Q1-Q0)
        delt_complex = [np.abs(res_complex1[i]-res_complex0[i])/round(test_para['read_in_pw'] * 2.5e9)/ (2**13-1)  for i in range(len(res_complex0)) ]
        for  i in range(len(I0)):
            test_data['I0'].append(I0[i])
            test_data['Q0'].append(Q0[i])
            test_data['I1'].append(I1[i])
            test_data['Q1'].append(Q1[i])
            # test_data['delt_Q'].append(delt_Q[i])
            # test_data['delt_complex'].append(delt_complex[i])
        plt.figure(figsize = (7, 5))
        plt.title("sweep01_cavity_freq")
        plt.xlabel('MHz')
        plt.ylabel('mod')
        plt.plot(I0, Q0, label='|0⟩')
        plt.plot(I1, Q1, label='|1⟩')
        plt.plot(I1, delt_Q, label='|1⟩-|0⟩')
        plt.plot(I1, delt_complex, label='abs(|1⟩-|0⟩)')
        plt.legend(loc='upper right')
        plt.savefig(f'{result_dir}/{result_name}.png',bbox_inches='tight')
        plt.show()
        saveResult(result_name, test_data, test_index, now_time)
    except:
        stop_flag = True

def saveResult(result_name, data, id, time):
    try:
        if not os.path.exists(xml_path):
            tree = ET.parse(str(Path(__file__).parent/'TestItems.xml'))
        else:
            tree = ET.parse(xml_path)
        root = tree.getroot()
        for child in root:
            add_element = ET.SubElement(child, 'item')
            add_element.attrib['name'] = str(result_name)
            add_element.attrib['id'] = str(id)
            add_element.attrib['time'] = str(time)
            new_tree = ET.ElementTree(root)
            new_tree.write(xml_path, encoding='utf-8', xml_declaration=True)
        workbook = xlwt.Workbook(encoding='ascii')
        worksheet = workbook.add_sheet("TestConfig")
        index = 0
        for i in env_para:
            worksheet.write(index, 0, 'env')
            worksheet.write(index, 1, i)
            worksheet.write(index, 2, str(env_para[i]))
            index += 1
        for i in test_para:
            worksheet.write(index, 0, 'test')
            worksheet.write(index, 1, i)
            worksheet.write(index, 2, str(test_para[i]))
            index += 1
        for i in trig_para:
            worksheet.write(index, 0, 'trig')
            worksheet.write(index, 1, i)
            worksheet.write(index, 2, str(trig_para[i]))
            index += 1
        worksheet = workbook.add_sheet("test_data")
        index = 0
        keyList = list(data.keys())
        for i,v in enumerate(keyList):
            worksheet.write(index, i, v)
        index += 1
        if len(keyList) == 2:
            for ix in range(len(data[keyList[0]])):
                worksheet.write(index, 0, data[keyList[0]][ix])
                worksheet.write(index, 1, data[keyList[1]][ix])
                index += 1
        elif len(keyList) == 3:
            for ix in range(len(data[keyList[0]])):
                for iy in range(len(data[keyList[1]])):
                    worksheet.write(index, 0, data[keyList[0]][ix])
                    worksheet.write(index, 1, data[keyList[1]][iy])
                    worksheet.write(index, 2, data[keyList[2]][ix][iy])
                    index += 1
        elif len(keyList) == 4:
            for ix in range(len(data[keyList[0]])):
                worksheet.write(index, 0, data[keyList[0]][ix])
                worksheet.write(index, 1, data[keyList[1]][ix])
                worksheet.write(index, 2, data[keyList[2]][ix])
                worksheet.write(index, 3, data[keyList[3]][ix])
                index += 1
        workbook.save(f'{result_dir}/{result_name}.xls')
    finally:
        del workbook

def draw_line_chart(path,result_name,title='test',xlabel='x',ylabel='y'):
    time.sleep(0.1)
    while not stop_flag:
        _finish_len = finish_len
        _all_len = all_len
        mdata = test_data.copy()
        if not len(mdata['x']) == len(mdata['y']):
            continue
        clear_output(wait=True)
        plt.figure(figsize=(7,5))
        plt.title(title) 
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.margins(x = 0)
        plt.plot(mdata['x'], mdata['y'])
        plt.grid()
        finish = round(_finish_len/_all_len*70)
        if _finish_len == _all_len:
            plt.savefig(f'{path}/{result_name}.png',bbox_inches='tight')
        plt.show()
        print(f'\r[{"■"*finish}{"-"*(70-finish)}] {round(finish/70*100)}% ', end="")
        time.sleep(0.5)
        if _finish_len == _all_len:
            break
    
def draw_heatmap_chart(path,result_name,title='test',xlabel='x',ylabel='y'):
    time.sleep(0.1)
    while not stop_flag:
        mdata = test_data.copy()
        hmask = heatmap_mask.copy()
        _finish_len = finish_len
        _all_len = all_len
        clear_output(wait=True)
        plt.figure(figsize=(7, 5))
        sns.set_theme(font_scale=1)
        df = pd.DataFrame(data=mdata['z'], index=mdata['x'] ,columns=mdata['y'])
        sns.heatmap(df,cmap="viridis_r",mask=hmask)
        plt.title(title) 
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.margins(x = 0)
        plt.grid()
        finish = round(_finish_len/_all_len*70)
        if _finish_len == _all_len:
            plt.savefig(f'{path}/{result_name}.png',bbox_inches='tight')
        plt.show()
        print(f'\r[{"■"*finish}{"-"*(70-finish)}] {round(finish/70*100)}% ', end="")
        time.sleep(0.5)
        if _finish_len == _all_len:
            break

def read_data_form_xls(file):
    wb = xlrd.open_workbook(file)
    sheet = wb.sheet_by_name('test_data')
    data = []
    nrows = sheet.nrows
    for i in range(nrows):
        data.append(sheet.row_values(i))
    return data

def funcS(func, beta_list, beta_step_list, x_list, y_list):
    r_list = func(beta_list, x_list) - y_list
    S = (np.sqrt(np.mean(r_list**2)))**2  # 计算均方根并平方
    return r_list, S

def funcJ(func, beta_list, beta_step_list, x_list, y_list):
    r_list = func(beta_list, x_list) - y_list
    S = (np.sqrt(np.mean(r_list**2)))**2
    m = len(beta_list)
    n = len(r_list)
    J_matrix = np.zeros((n, m))
    for cnt_beta in range(m):
        vector_temp = np.zeros(m)
        vector_temp[cnt_beta] = 1
        r_list_diff = func(beta_list + vector_temp * beta_step_list, x_list) - y_list
        J_column = (r_list_diff - r_list) / beta_step_list[cnt_beta]
        J_matrix[:, cnt_beta] = J_column
    return J_matrix, r_list, S

def gradientDescend(func, beta_list, beta_diff_step_list, x_list, y_list, figure_num):
    traditional_lambda_option = 0
    lambda_0 = 100  
    traditional_lambda_multiple = 10
    decreasing_multiple = 5
    increasing_multiple = 2
    max_iteration_num = 40
    lambda_temp = lambda_0 
    REC_lambda_temp = [] 
    REC_S_temp = []
    REC_delta_S = []
    REC_step_length = []
    for cnt in range(max_iteration_num):  
        plt.pause(0.01)  
        y_list_temp = func(beta_list, x_list)
        J_matrix, r_list, S = funcJ(func, beta_list, beta_diff_step_list, x_list, y_list)
        J_sqr = np.dot(J_matrix.T, J_matrix)
        delta_beta_list_0 = -np.linalg.inv(J_sqr + lambda_temp * np.eye(len(J_sqr))) @ J_matrix.T @ r_list
        if np.sum(np.isnan(delta_beta_list_0)) > 0:  
            raise ValueError('NaN due to inv(). Check the initial guess.')
        if traditional_lambda_option == 1:
            beta_list_temp = beta_list + delta_beta_list_0
            _, S_temp = funcS(func, beta_list_temp, beta_diff_step_list, x_list, y_list)
            while S_temp > S:  
                lambda_temp *= traditional_lambda_multiple
                J_sqr = np.dot(J_matrix.T, J_matrix)
                delta_beta_list_0 = -np.linalg.inv(J_sqr + lambda_temp * np.eye(len(J_sqr))) @ J_matrix.T @ r_list
                if np.sum(np.isnan(delta_beta_list_0)) > 0:
                    raise ValueError('NaN due to inv(). Check the initial guess.')
                beta_list_temp = beta_list + delta_beta_list_0
                _, S_temp = funcS(func, beta_list_temp, beta_diff_step_list, x_list, y_list)
            beta_list = beta_list_temp
            lambda_temp /= traditional_lambda_multiple  
        else:  
            beta_list_temp = beta_list + delta_beta_list_0
            _, S_temp = funcS(func, beta_list_temp, beta_diff_step_list, x_list, y_list)
            beta_list = beta_list_temp  
            if S_temp > S:
                lambda_temp *= increasing_multiple  
            else:
                lambda_temp /= decreasing_multiple  
        REC_lambda_temp.append(lambda_temp)
        REC_S_temp.append(S_temp)
        if cnt == 0:
            REC_delta_S.append(1)
        else:
            REC_delta_S.append(REC_S_temp[cnt] / REC_S_temp[cnt - 1])
        REC_step_length.append(np.sqrt(np.mean(delta_beta_list_0**2)))
    _, S_result = funcS(func, beta_list, beta_diff_step_list, x_list, y_list) 
    return beta_list, S_result, cnt, lambda_temp

def T1_match(x,y,resultPath,result_name):
    x_list_original = x
    y_list_original = y
    x_normal = np.max(x_list_original) - np.min(x_list_original) 
    x_list = x_list_original / x_normal
    y_list = y_list_original 
    beta_list = np.array([y_list[0] - y_list[-1], -((x_list[-1] - x_list[0]) / 2) ** -1, y_list[-1]])  
    beta_diff_step_list = np.array([1e-4, 1e-4, 1e-4])  
    def T1_func(beta_list, x):
        return beta_list[0] * np.exp(beta_list[1] * x) + beta_list[2]
    beta_list, S_result, cnt, lambda_temp = gradientDescend(T1_func, beta_list, beta_diff_step_list, x_list, y_list, 2)
    t1 = np.round(((-beta_list[1] / x_normal) ** -1 )/1000,4) 
    y_list_temp = T1_func(beta_list, x_list) 
    plt.figure(figsize=(7,5))
    plt.plot(x_list * x_normal, y_list, 'd', label='exp.', color='b')            
    plt.plot(x_list * x_normal, y_list_temp, label='fitted', color='r')
    plt.title(f'T1 match')
    plt.xlabel('times(ns)')
    plt.ylabel('Amplitude')
    plt.margins(x = 0)
    plt.text(max(x)/2.5, max(y), f"Time:{t1}us")
    plt.legend(loc='upper right')
    plt.savefig(f'{resultPath}/{result_name}.png', dpi=800)
    plt.show()

def T2_match(x,y,resultPath,result_name,xy_freq_offset):
    x_list_original = x
    y_list_original = y
    x_normal = np.max(x_list_original) - np.min(x_list_original) 
    y_normal = np.max(y_list_original) - np.min(y_list_original)
    x_list = x_list_original / x_normal
    y_list = y_list_original / y_normal
    index_min = np.argmin(y_list)  
    index_max = np.argmax(y_list)   
    beta_list = np.array([
        y_list[0] - y_list[-1],
        -((x_list[-1] - x_list[0]) / 2) ** -1,
        y_list[-1],
        (2 * abs(x_list[index_max] - x_list[index_min])) ** -1,0])
    beta_diff_step_list = np.array([1e-4] * 5)  
    def T2_func(beta_list, x):
        return beta_list[0] * np.exp(beta_list[1] * x) * np.cos(2 * np.pi * beta_list[3] * x + beta_list[4]) + beta_list[2]
    beta_list, S_result, cnt, lambda_temp = gradientDescend(T2_func, beta_list, beta_diff_step_list, x_list, y_list, 2)
    y_list_temp = T2_func(beta_list, x_list) 
    t2 = np.round((-beta_list[1] / x_normal) ** -1,4)
    plt.figure(figsize=(7,5))
    plt.plot(x_list * x_normal, y_list, 'd', label='exp.', color='b')            
    plt.plot(x_list * x_normal, y_list_temp, label='fitted', color='r')
    plt.title(f'T2 match')
    plt.xlabel('times(ns)')
    plt.ylabel('Amplitude')
    plt.margins(x = 0)
    plt.text(max(x)+1, (max(y_list)+min(y_list))/2, f"T2:{t2}ns \n Amp:{np.round(beta_list[0],4)} \n Freq:{np.round(beta_list[3],4)}MHz \n Phase:{np.round(beta_list[4],4)} \n ▲Freq:{np.round((beta_list[3]-xy_freq_offset),4)}MHz")
    plt.legend(loc='upper right')
    plt.savefig(f'{resultPath}/{result_name}.png', dpi=800)
    plt.show()

def  fidelity(x0,y0,x1,y1,resultPath,result_name):
    complex_set_0 = x0 + y0 * 1j
    complex_set_1 = x1 + y1 * 1j
    plt.figure(figsize=(7,5))
    plt.scatter(np.real(complex_set_0), np.imag(complex_set_0), s=9, label='0')
    plt.scatter(np.real(complex_set_1), np.imag(complex_set_1), s=9, label='1')
    plt.legend(loc='upper right')
    plt.grid()
    plt.axis('equal')
    center_0_estimate = np.mean(complex_set_0)
    center_1_estimate = np.mean(complex_set_1)  
    plt.scatter(np.real(center_0_estimate), np.imag(center_0_estimate), s=72, marker='D', label='center 0 estimate')
    plt.scatter(np.real(center_1_estimate), np.imag(center_1_estimate), s=72, marker='D', label='center 1 estimate')
    delta_phi = -np.angle(center_1_estimate - center_0_estimate)
    complex_set_0_rotated = complex_set_0 * np.exp(1j * delta_phi)
    complex_set_1_rotated = complex_set_1 * np.exp(1j * delta_phi)
    center_0_estimate_rotated = center_0_estimate * np.exp(1j * delta_phi)
    center_1_estimate_rotated = center_1_estimate * np.exp(1j * delta_phi)
    data_0_original = np.real(complex_set_0_rotated)
    data_1_original = np.real(complex_set_1_rotated)
    min_data = min(np.min(data_0_original), np.min(data_1_original))
    max_data = max(np.max(data_0_original), np.max(data_1_original))
    data_normal = max_data - min_data
    data_0 = data_0_original / data_normal
    data_1 = data_1_original / data_normal
    hist_0, bins_0 = np.histogram(data_0, bins=30, density=True)
    hist_1, bins_1 = np.histogram(data_1, bins=30, density=True)
    line_0_x = (bins_0[:-1] + np.diff(bins_0) / 2)
    line_0_y = hist_0
    line_1_x = (bins_1[:-1] + np.diff(bins_1) / 2)
    line_1_y = hist_1
    std_0 = np.std(data_0)
    beta_list = [1 / (np.sqrt(2 * np.pi) * std_0), np.mean(data_0), std_0]
    beta_diff_step_list = [1e-4, 1e-4, 1e-4]
    def func_gaussian(beta_list, x):
        return beta_list[0] * np.exp(-((x - beta_list[1]) / (np.sqrt(2) * beta_list[2]))**2)
    def func_double_gaussian(beta_list, x):
        return  (beta_list[0] * np.exp(-((x - beta_list[1]) / (np.sqrt(2) * beta_list[2]))**2) + beta_list[3] * np.exp(-((x - beta_list[4]) / (np.sqrt(2) * beta_list[5]))**2))
    beta_list, S_result, cnt, lambda_temp = gradientDescend(func_gaussian, beta_list, beta_diff_step_list, line_0_x, line_0_y, 30)
    beta_list_q0 = np.array([1 / (np.sqrt(2 * np.pi) * std_0), np.mean(data_0), std_0, 
                            0 / (np.sqrt(2 * np.pi) * std_0), np.mean(data_1), std_0])
    beta_diff_step_list_q0 = np.array([1e-4, 1e-4, 1e-4, 1e-4, 1e-4, 1e-4])
    beta_list_q0, S_result_q0, cnt_q0, lambda_temp_q0 = gradientDescend(func_double_gaussian, beta_list_q0, beta_diff_step_list_q0, line_0_x, line_0_y, 35)
    diff_step_modified_option = 0
    if diff_step_modified_option == 1:
        beta_diff_step_list /= 100
        beta_list_2, S_result_2, cnt_2, lambda_temp_2 = gradientDescend(func_gaussian, beta_list, beta_diff_step_list, line_0_x, line_0_y, 40)
        S_result_diff_1 = S_result_2 - S_result
        beta_diff_step_list /= 100
        beta_list_3, S_result_3, cnt_3, lambda_temp_3 = gradientDescend(func_gaussian, beta_list, beta_diff_step_list, line_0_x, line_0_y, 50)
        S_result_diff_2 = S_result_3 - S_result_2
    beta_list_q1 = np.array([1 / (np.sqrt(2 * np.pi) * std_0), np.mean(data_1), std_0, 
                            0 / (np.sqrt(2 * np.pi) * std_0), np.mean(data_0), std_0])
    beta_diff_step_list_q1 = np.array([1e-4, 1e-4, 1e-4, 1e-4, 1e-4, 1e-4])
    beta_list_q1, S_result_q1, cnt_q1, lambda_temp_q1 = gradientDescend(func_double_gaussian, beta_list_q1, beta_diff_step_list_q1, line_1_x, line_1_y, 60)
    if diff_step_modified_option == 1:
        beta_diff_step_list_q1 /= 100
        beta_list_q1_2, S_result_q1_2, cnt_q1_2, lambda_temp_q1_2 = gradientDescend(func_double_gaussian, beta_list_q1, beta_diff_step_list_q1, line_1_x, line_1_y, 70)
        S_result_diff_q1 = S_result_q1_2 - S_result_q1
        beta_diff_step_list_q1 /= 100
        beta_list_q1_3, S_result_q1_3, cnt_q1_3, lambda_temp_q1_3 = gradientDescend(func_double_gaussian, beta_list_q1_2, beta_diff_step_list_q1, line_1_x, line_1_y, 80)
        S_result_diff_q1_2 = S_result_q1_3 - S_result_q1_2
    x_distinct_estimate = (beta_list[1] + beta_list_q1[1]) / 2 
    r_distinct_estimate = abs(beta_list[1] - beta_list_q1[1]) / 2  
    decay_probability_1to0_estimate = (beta_list_q1[3] * beta_list_q1[5] * np.sqrt(2 * np.pi)) / \
        ((beta_list_q1[0] * beta_list_q1[2] * np.sqrt(2 * np.pi)) + (beta_list_q1[3] * beta_list_q1[5] * np.sqrt(2 * np.pi)))
    decay_probability_0to1_estimate = (beta_list_q0[3] * beta_list_q0[5] * np.sqrt(2 * np.pi)) / \
        ((beta_list_q0[0] * beta_list_q0[2] * np.sqrt(2 * np.pi)) + (beta_list_q0[3] * beta_list_q0[5] * np.sqrt(2 * np.pi)))
    e_0_intrinsic_estimate = np.around(norm.cdf(abs(x_distinct_estimate - beta_list[1]), 0, beta_list[2]),4)
    e_1_intrinsic_estimate = np.around(norm.cdf(abs(x_distinct_estimate - beta_list_q1[1]), 0, beta_list_q1[2]),4)
    e_1_estimate = np.around(e_1_intrinsic_estimate * (1 - decay_probability_1to0_estimate),4)
    e_0_estimate = np.around(e_0_intrinsic_estimate * (1 - decay_probability_0to1_estimate),4)
    plt.figure(figsize=(7,5))  
    plt.hist(data_0, bins=30, density=True, alpha=0.5)
    plt.hist(data_1, bins=30, density=True, alpha=0.5)
    plt.plot(line_0_x, line_0_y, label='line of hist 0')
    plt.plot(line_1_x, line_1_y, label='line of hist 1')
    x_vals = np.linspace(np.min(line_0_x), np.max(line_0_x), 100)
    plt.plot(x_vals, func_double_gaussian(beta_list_q0, x_vals), linewidth=4, label='0 fitted double_gaussian')
    plt.plot(x_vals, func_double_gaussian(beta_list_q1, x_vals), linewidth=4, label='1 fitted double_gaussian')
    plt.legend(loc='upper right')
    plt.title(f'QUbit 0fidelity :{e_0_intrinsic_estimate} 1fidelity :{e_1_intrinsic_estimate}')
    plt.savefig(f"{resultPath}/{result_name.replace('mod','fidelity_res')}.png", dpi=800)
    plt.figure(figsize=(7,5))
    plt.scatter(np.real(complex_set_0_rotated), np.imag(complex_set_0_rotated), s=9, label='0 rotated')
    plt.scatter(np.real(complex_set_1_rotated), np.imag(complex_set_1_rotated), s=9, label='1 rotated')
    plt.scatter(np.real(center_0_estimate_rotated), np.imag(center_0_estimate_rotated), s=72, marker='D', label='center 0 estimate rotated')
    plt.scatter(np.real(center_1_estimate_rotated), np.imag(center_1_estimate_rotated), s=72, marker='D', label='center 1 estimate rotated')
    center_0_x = beta_list[1] * data_normal
    center_0_y = np.mean(np.imag(complex_set_0_rotated))
    r_0 = beta_list[2] * data_normal
    phi_list = np.arange(0, 2 * np.pi, 0.01)
    x_temp = center_0_x + 2 * r_0 * np.cos(phi_list)
    y_temp = center_0_y + 2 * r_0 * np.sin(phi_list)
    plt.plot(x_temp, y_temp, linewidth=4)
    center_1_x = beta_list_q1[1] * data_normal
    center_1_y = np.mean(np.imag(complex_set_1_rotated))
    r_1 = beta_list_q1[2] * data_normal
    x_temp = center_1_x + 2 * r_1 * np.cos(phi_list)
    y_temp = center_1_y + 2 * r_1 * np.sin(phi_list)
    plt.plot(x_temp, y_temp, linewidth=4)
    plt.legend(loc='upper right')
    plt.grid()
    plt.axis('equal')
    plt.title(f'QUbit Scatter diagram')
    plt.savefig(f"{resultPath}/{result_name.replace('mod','scatter_diagram')}.png", dpi=800)
    plt.show()
 