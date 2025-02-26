from InstrumentWraps.ZWDX.ZW_QCS220_DRIVER_20241207 import ZW_QCS220_DRIVER
import NLab.Utils.common as cm
import NLab.Instruments.Instrument as _Instr_
import numpy as np
import time

cm.rl(_Instr_)


class DeviceBase():

    def __init__(self):
        pass


class ZW_QCS220(DeviceBase, _Instr_.INSTR):
    __device = 'ZW-QCS220' 
    __version = 'v1.1'
    __Date = '2024.12.07'

    __ad_ch_num = 4
    __da_ch_num = 20

    __ad_ch_num = 2
    __da_microwave_num = 14
    __da_dc_num = 8

    __TRIG_STATUS_CLOSE = 0
    __TRIG_STATUS_OPEN = 1
    trigger_status = __TRIG_STATUS_CLOSE

    def __init__(self,
                 addr: str,
                 da_nyquist=[1, 1, 1],
                 da_sampling=[8, 8, 8],
                 triggerparams=[0, 200, 1000, 0]):
        '''
        Parameters
        ----------
        addr : str
            设备ip.
        da_Nyquist : DA的奈奎斯特域设定
            [0] 1~6 DA通道共用一个奈奎斯特域设置
            [1] 7~14 DA通道共用一个奈奎斯特域设置
            [2] 15~22 DA通道共用一个奈奎斯特域设置
            取值：
              0: 使用第一奈奎斯特域 提高0 ~ samplin_grate/2的输出功率. 
              1: 使用第二奈奎斯特域 提高samplin_grate/2 ~ samplin_grate的输出功率. 
              The default is 1.
        da_sampling: DA的采样率(单位GHz) 默认采样率 6Gsps
            [0] 1~6 DA通道共用一个采样率
            [1] 7~14 DA通道共用一个采样率
            [2] 15~22 DA通道共用一个采样率
        triggerparams: 设备基本工作参数
            [0] 触发源:
               0: Internal 内触发
               1: External 外触发
            [1] 内部触发周期(单位us), 如 200
            [2] 内触发信号生成次数, 如 1000
            [3] 内部触发连续触发模式
               1开启 0关闭
        Returns
        -------
        None.
          
        '''
        super(ZW_QCS220, self).__init__()
        self.qcs_driver = ZW_QCS220_DRIVER(addr)
        self.qcs_driver.performOpen()
        self.ad_sampling = 2.5e9
        self.da_sampling = da_sampling
        # self.da_nyquist = [1,1,1]
        self.da_nyquist = da_nyquist
        # print(f"triggerparams:{triggerparams}")
        # 触发源 1：使用外部触发源；0：使用内部触发源
        self.trigger_source = triggerparams[0]
        # 内触发信号周期，单位us
        self.trigger_us = triggerparams[1]
        # 内触发信号生成次数
        self.trigger_num = triggerparams[2]
        # 1 : 一直生成内触发信号，此时trigger_num无效; 0 : 生成trigger_num次的内触发信号
        self.trigger_continue = triggerparams[3]
        self.init_trigger_conf()
        self.dac_samplingRate(1, da_sampling[0])
        self.dac_samplingRate(7, da_sampling[1])
        self.dac_samplingRate(15, da_sampling[2])
        self.dac_Nyquist(1, da_nyquist[0])
        self.dac_Nyquist(7, da_nyquist[1])
        self.dac_Nyquist(15, da_nyquist[2])
        self.connect()

    def init_trigger_conf(self):
        # 设定设备基本工作参数
        # 关闭设备对触发源的响应，才能进行配置
        self.qcs_driver.triggerClose()
        # 触发源，Internal（内触发），External（外触发）
        self.qcs_driver.setValue(
            "TriggerSource",
            "Internal" if self.trigger_source == 0 else "External")
        # 内部触发周期，单位s，需 us 转 s
        self.qcs_driver.setValue("TriggerPeriod", self.trigger_us * 1e-6)
        # 内部触发次数
        self.qcs_driver.setValue("TriggerNumber", self.trigger_num)
        # 内部触发连续触发模式，1开启，0关闭
        self.qcs_driver.setValue("TriggerContinue", self.trigger_continue)

    def connect(self):
        for _ch in range(self.__da_microwave_num):
            xy_ch = _ch + 1
            setattr(self, f'OUT{xy_ch}', _XYChannel(self, xy_ch))

        for _ch in range(self.__da_dc_num):
            z_ch = _ch + 15
            setattr(self, f'OUTZ{z_ch}', _ZChannel(self, z_ch))

        for _ch in range(self.__ad_ch_num):
            probe_ch = _ch + 1
            setattr(self, f'IN{probe_ch}', _Probe(self, probe_ch))

    def dac_samplingRate(self, ch, sampling):
        '''
        设置out通道的DAC采样率
        22个out通道分为ch1~6，ch7~14，ch15~22三组，根据设定的ch直接修改该组所有通道的采样率
          1~6 DA通道共用一个采样率
          7~14 DA通道共用一个采样率
          15~22 DA通道共用一个采样率
        Parameters
        ----------
        ch : 通道，1~22
        sampling : 采样率，单位GHz
        Returns
        -------
        None.
        '''
        # 设定设备默认采样率，ZW-QCS220-RFAWG为XY轴控制、耦合控制设备，默认采样率6Gsps
        self.qcs_driver.setValue('DAC_Sampling', sampling, chn=ch)

    def dac_Nyquist(self, ch, Nyquist):
        '''
        设置out通道的DAC 奈奎斯特域
        22个out通道分为ch1~6，ch7~14，ch15~22三组，根据设定的ch直接修改该组所有通道的奈奎斯特域
          1~6 DA通道共用一个奈奎斯特域设置
          7~14 DA通道共用一个奈奎斯特域设置
          15~22 DA通道共用一个奈奎斯特域设置
        Parameters
        ----------
        ch : 通道，1~22
        Nyquist : 奈奎斯特域
            normal 0: 使用第一奈奎斯特域，提高0 ~ samplin_grate/2的输出功率. 
            mix    1: 使用第二奈奎斯特域，提高samplin_grate/2 ~ samplin_grate的输出功率. 
        Returns
        -------
        None.
        '''
        self.qcs_driver.setValue("Nyquist",
                                 "mix" if Nyquist == 1 else "normal",
                                 chn=ch)

    def trigger_close(self, k=None):
        """ 关闭设备的触发使能 """
        if self.trigger_status == self.__TRIG_STATUS_CLOSE:
            return
        self.qcs_driver.stop()
        self.trigger_status = self.__TRIG_STATUS_CLOSE

    def trigger_open(self, k=None):
        """ 开启设备的触发使能 """
        if self.trigger_status == self.__TRIG_STATUS_OPEN:
            return
        self.qcs_driver.Trig()
        self.trigger_status = self.__TRIG_STATUS_OPEN

    def qcs_arm(self, k=None):
        '''
        开启设备的触发使能
        Returns
        -------
        None.

        '''
        self.trigger_open()

    def measure(self, k=None):
        self.IN1.read_demod_ctrl(self.IN1.shots_demod_f)
        self.IN2.read_demod_ctrl(self.IN2.shots_demod_f)
        self.qcs_arm()
        self.IN1.read_demod()
        self.IN2.read_demod()
    
    def measure_set_read_demod_ctrl(self, k=None):
        """
        measure 拆分第一部分，用于外部触发嵌入，如 DG645
        """
        self.IN1.read_demod_ctrl(self.IN1.shots_demod_f)
        self.IN2.read_demod_ctrl(self.IN2.shots_demod_f)
    
    def measure_read_demod(self, k=None):
        """
        measure 拆分第二部分，用于外部触发嵌入，如 DG645
        """
        self.IN1.read_demod()
        self.IN2.read_demod()

    Q = {
        "qcs_arm": qcs_arm, 
        "arm_and_measure": measure,
        "measure_set_read_demod_ctrl": measure_set_read_demod_ctrl,
        "measure_read_demod": measure_read_demod
    }


class _XYChannel(_Instr_.INSTR):
    #CH1~4 为QA OUT 通道，默认采样率8G，写入波形最大长度262144点，32.768us
    #CH5~20 为CTRL OUT通道高，默认采样率6G，可更改采样率，写入波形最大长度491520点，6G采样率下81.92us

    def __init__(self, dev: "DeviceBase", ch=1):
        self.dev = dev
        self.ch = ch
        self._en = False
        self.delay = None
        self.w = None
        self.da_sampling = 8e9
        self.replay_count = 100000
        self.replay_continue = 0 #为1时将波形首尾相接反复输出
        self.init_conf()
    
    def init_conf(self):
        # 通道重复播放数量，响应指定数量的触发信号
        self.dev.qcs_driver.setValue("DAC_Replay_count", self.replay_count, chn=self.ch)
        # 通道连续波功能，AWG数据首尾相接播放，用于回放连续波
        self.dev.qcs_driver.setValue("DAC_Relpay_continue", self.replay_continue, chn=self.ch)

    def wave(self, w_delay_ns):
        self.dev.trigger_close()
        # DAC输出相对触发信号延迟，单位s
        if self.delay != w_delay_ns["delay"]:
            self.delay = w_delay_ns["delay"]
            self.dev.qcs_driver.setValue("DAC_TriggerDelay", self.delay, chn=self.ch)
        # 发送波形数据到设备
        w = w_delay_ns["w"]
        self.dev.qcs_driver.setValue("DAC_Data", w, chn=self.ch)

    def output(self, b):
        self.dev.trigger_close()
        self._en = bool(b)
        if self._en:
            self.dev.qcs_driver.on(self.ch)
        else:
            self.dev.qcs_driver.off(self.ch)

    W = {
        "wave": wave,
        "output": output,
    }


class _ZChannel(_Instr_.INSTR):
    #CH15~22 为z OUT 通道，默认采样率8G，写入波形最大长度491520点，8G采样率下61.44us

    def __init__(self, dev: "DeviceBase", ch=15):
        self.dev = dev
        self.ch = ch
        self._en = False
        self.delay = 0
        self.da_sampling = 8e9
        self.replay_count = 100000
        self.replay_continue = 0 #为1时将波形首尾相接反复输出
        self.init_conf()

    def init_conf(self):
        # 通道重复播放数量，响应指定数量的触发信号
        self.dev.qcs_driver.setValue("DAC_Replay_count", self.replay_count, chn=self.ch)
        # 通道连续波功能，AWG数据首尾相接播放，用于回放连续波
        self.dev.qcs_driver.setValue("DAC_Relpay_continue", self.replay_continue, chn=self.ch)

    def wave(self, w_delay_ns):
        self.dev.trigger_close()
        # DAC输出相对触发信号延迟，单位s
        if self.delay != w_delay_ns["delay"]:
            self.delay = w_delay_ns["delay"]
            self.dev.qcs_driver.setValue("DAC_TriggerDelay", self.delay, chn=self.ch)
        # 发送波形数据到设备
        w = w_delay_ns["w"]
        self.dev.qcs_driver.setValue("DAC_Data", w, chn=self.ch)

    def output(self, b):
        self.dev.trigger_close()
        self._en = bool(b)
        if self._en:
            self.dev.qcs_driver.on(self.ch)
        else:
            self.dev.qcs_driver.off(self.ch)

    def dc_voltage(self, voltage):
        '''
        设置基准电压
        Parameters
        ----------
        voltage : 基准电压，0~1v
        Returns
        -------
        None.

        '''
        self.dev.trigger_close()
        self.voltage = voltage
        self.dev.qcs_driver.setValue('DAC_Offset', self.voltage, chn=self.ch) # 设置通道（15~22）偏置电压V

    W = {
        "wave": wave,
        "output": output,
        "dc_voltage": dc_voltage,
    }


class _Probe(_Instr_.INSTR):

    def __init__(self, dev: "DeviceBase", ch=1):
        self.dev = dev
        self.ch = ch
        self.delay = None
        self.demod_f = []
        self.wave_data = None
        self.demod_data = None
        self.SGS = None  # single shot temp cache
        self.AVG = None  # average temp cache
        self.freqList = []
        self.save_points = []
        self.times = 0
        self.ad_sampling = 2.5e9

    def read_wave_ctrl(self, times_save):
        '''
        波形采集功能参数控制
        Parameters
        ----------
        times : int
            采集次数.
        save_len_ns : int
            单次采集长度，单位ns.单通道总的采集长度最大为13107.2ns
        Returns
        -------
        None.

        '''
        self.dev.trigger_close()
        # ADC采集相对触发信号延迟，单位s
        if self.delay != times_save["delay"]:
            self.delay = times_save["delay"]
            self.dev.qcs_driver.setValue("ADC_TriggerDelay", self.delay, chn=self.ch)
        # 读取解模重复次数，也就是响应外部触发完成采集、解模判决的次数
        if self.times != times_save["times"]:
            self.times = times_save["times"]
            self.dev.qcs_driver.setValue("ADC_TriggerTimes", self.times, chn=self.ch)
        # 采集解模数据样点，按照采样点数计算，最大131072采样点
        save_len_ns = times_save["save_len_ns"]
        read_len = round(save_len_ns / 1e9 * self.ad_sampling)
        self.dev.qcs_driver.setValue("ADC_SaveLen", read_len, chn=self.ch)

    def read_wave(self, k=None):
        '''
        读取采集的波形
        Returns
        -------
        np.array，内部为int
            采集的波形数据.

        '''
        # TODO sleet(1) 干什么的？
        time.sleep(1)
        # 从设备获取指定通道原始数据，入参 ch 列表第一位 0 是占位符（用于兼容其他地方接口）
        wave_data = self.dev.qcs_driver.getResult(ch=[0, self.ch], option="raw")
        self.wave_data = wave_data / self.times
        return self.wave_data

    def read_demod_ctrl(self, shots_demod_f):
        '''
        解调功能参数控制
        Parameters
        ----------
        shots : int
            解调次数.
        demod_len : int
            解模长度，单位ns，最大13107.2ns
        demod_f : list，二维
            解调参数列表.
            [[start_phase, freq]
             [start_phase, freq]
             ...
             [start_phase, freq]        
            ]
            第一维是解模模块，每路ad通道最大32个
            第二维是单个解模模块的工作参数
            start_phase：起始相位，弧度
            freq:频率，Hz
        Returns
        -------
        None.

        '''
        demod_len = shots_demod_f["demod_len"]
        shots = shots_demod_f["shots"]
        self.demod_f = shots_demod_f["demod_f"]
        delay = shots_demod_f["delay"]
        demod_len_i = round(demod_len / 1e9 * self.ad_sampling)
        temp = []
        self.freqList = []
        for i in self.demod_f:
            temp.append([i[0], i[1]])
            self.freqList.append(i[1])
            self.save_points = demod_len_i
        self.dev.trigger_close()
        # 配置采集解模参数列表到设备
        # 设定解模触发延迟，与采集时间片时间累加在一起
        self.dev.qcs_driver.setValue("MUL_TriggerDelay", delay, chn=self.ch)
        # 设定采集解模次数
        self.dev.qcs_driver.setValue("MUL_Times", shots, chn=self.ch)
        # 总采集解模样点数量，多次读取应该覆盖所有时间片总长度
        self.dev.qcs_driver.setValue("MUL_F_Len", demod_len_i, chn=self.ch)
        # 采集解模配置信息表写入
        self.dev.qcs_driver.setValue("MUL_F_Data", temp, chn=self.ch)
        # 调用rpc设置
        self.dev.qcs_driver.setValue("MUL_SetPars", 0, chn=self.ch)

    def set_demod_ctrl(self, shots_demod_f):
        self.shots_demod_f = shots_demod_f

    def read_demod(self, k=None):
        '''
        读取解调结果
        Returns
        -------
        np.array,内部数值为complex
            二维，第一维是解调模块，第二维是具体的数值

        '''
        # 从设备获取指定通道解模数据
        mul_data = self.dev.qcs_driver.getResult(ch=[0, self.ch], option="IQ")
        self.demod_data = np.array(mul_data).T # 转置后以16个通道数为行
        for i in range(len(self.demod_data)): # 遍历各个通道
            self.demod_data[i] /= 2**13
            self.demod_data[i] /= self.save_points
        self.SGS = self.demod_data # 各通道解模数据
        self.AVG = np.mean(self.demod_data, axis=1) # 各通道均值数据（计算每一行均值）
        return self.demod_data

    def average(self, k=None):
        idx = int(k[1:])
        if self.AVG is None:
            print(f"ch {self.ch} ATS warning: fetch nothing")
            return 0
        if idx < len(self.freqList):
            return self.AVG[idx]
        else:
            print(f"ch {self.ch} ATS warning: list index out of range")
            return 0

    def single_shot(self, k=None):
        idx = int(k[1:])
        if self.SGS is None:
            print(f"ch {self.ch} ATS warning: fetch nothing")
            return np.ones((16, ))
        if idx < len(self.freqList):
            return self.SGS[idx]
        else:
            print(f"ch {self.ch} ATS warning: list index out of range")
            return np.ones((16, ))

    W = {
        "read_wave_ctrl": read_wave_ctrl,
        "set_demod_ctrl": set_demod_ctrl,
    }

    Q = {
        "read_wave": read_wave,
        "read_demod": read_demod,
        "A0": average,
        "A1": average,
        "A2": average,
        "A3": average,
        "A4": average,
        "A5": average,
        "A6": average,
        "A7": average,
        "S0": single_shot,
        "S1": single_shot,
        "S2": single_shot,
        "S3": single_shot,
        "S4": single_shot,
        "S5": single_shot,
        "S6": single_shot,
        "S7": single_shot,
    }
