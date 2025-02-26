import numpy as np
import time
import os
import sys
import grpc
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,dir_path)
import ZW_QCS220_pb2
import ZW_QCS220_pb2_grpc

from google.protobuf.empty_pb2 import Empty
import pickle

class ZW_QCS220_DRIVER:

    support_models = ['ZW_QCS220']

    max_value = 2**31 - 1
    min_value = -2**31
    sample_rate = [3]*6    #RFAWG默认采样率6Gsps
    adc_sample_rate = 2.5

    CHs_num = 22

    _nyquist = [None]*CHs_num
    _replay_cnt = [1]*CHs_num
    _relpay_continuou = [0]*CHs_num
    _triger_delay = [0]*CHs_num

    _feedback_data = [None]*CHs_num
    _feedback_message = [None]*CHs_num

    _dac_offset = [0]*CHs_num

    _trigger_us = 2
    _trigger_source = 0 #默认内触发
    _trigger_num = 1
    _trigger_continue = 0

    ADC_CHs_num = 2
    _adc_trigger_delay = [0]*ADC_CHs_num
    _adc_trigger_times = [1]*ADC_CHs_num
    _adc_savelen = [2**17]*ADC_CHs_num

    _mul_trigger_delay = [0]*CHs_num
    _mul_trigger_times = [1]*CHs_num
    _mul_f_len = [2**17]*CHs_num
    _mul_f_data = [None]*CHs_num
    _mul_qbit_phase = [1]*CHs_num

    _mul_decision_ctrl_modle_n = [0]*CHs_num

    def __init__(self, server_ip, server_port=8501):
        self.serverip = server_ip
        self.serverport = server_port

    def performOpen(self,):
        channel_options = [
            ("grpc.keepalive_time_ms", 80000),
            ("grpc.keepalive_timeout_ms", 120000),
            ("grpc.http2.max_pings_without_data", 5),
            ("grpc.keepalive_permit_without_calls", 1),
        ]

        self.channel = grpc.insecure_channel(str(self.serverip + ':' + str(self.serverport)), options=channel_options)
        print(str(self.serverip + ':' + str(self.serverport)))
        self.handle = ZW_QCS220_pb2_grpc.GRPC_QCS220Stub(self.channel)

        self.triggerClose()

    def performClose(self,):
        self.channel.close()

    # def setValue(self, name: str, value: Any, slotID: int, chn: int):
    def setValue(self, name: str, value, **kw):
        if name.startswith('Trigger'):
            self.set_TRIG(name, value)
        
        if name in ['DAC_Sampling']:
            ch = kw.get('chn', 1)
            if ch < 7:
                self.sample_rate[0] = value
                samplerate = value
            elif ch < 15:
                self.sample_rate[1] = value
            elif ch <= 22:
                self.sample_rate[2] = value
            else:
                print('ch must be 1~22')
                return
            self.handle.rfdac_sampling(ZW_QCS220_pb2.ParDacSampling(sampling = value,
                                                                    ch = ch))

        if name in ['Output',  'Nyquist', 'DAC_Replay_count', 'DAC_Relpay_continue', 'DAC_TriggerDelay', 'DAC_Data', 'DAC_Feedback_Set_Data', 'DAC_Feedback_Set_Message', 'DAC_Feedback_En', 'DAC_Offset']:
            ch = kw.get('chn', 1)
            # print(ch)
            if ch > 0 or ch < 25:  # DA
                self.set_DA(name, value, ch)   
            else:
                raise ValueError('DA channel number error!!!')
        
        if name in ['ADC_TriggerDelay', 'ADC_TriggerTimes', 'ADC_SaveLen']:
            ch = kw.get('chn', 1)
            if ch > 0 or ch < 9:  # AD
                if name in ['ADC_TriggerDelay']:
                    self._adc_trigger_delay[ch - 1] = round(value*self.adc_sample_rate*1e9)

                if name in ['ADC_TriggerTimes']:
                    self._adc_trigger_times[ch - 1] = value

                if name in ['ADC_SaveLen']:
                    self._adc_savelen[ch -1] = value

                self.handle.rd_adc_data_ctrl(ZW_QCS220_pb2.ParRdAdcDataCtrl(adc_channel_num = ch-1,
                                                                                 trigger_delay = self._adc_trigger_delay[ch - 1],
                                                                                 times = self._adc_trigger_times[ch - 1],
                                                                                 save_len = self._adc_savelen[ch - 1]))
            else:
                raise ValueError('DA channel number error!!!')
            
        if name.startswith('MUL'):
            ch = kw.get('chn', 1)
            # print(name,ch)
            # print
            if ch > 0 or ch < 9 :
                self.set_mul(name, value, ch)
            else:
                raise ValueError('MUL channel number error!!!')

    def getValue(self, name: str, **kw):

        if name.startswith('Trigger'):
            return self.get_Trig(name)
        
        if name in ['Nyquist']:
            ret = self.handle.rfdac_GetNyquistZone(Empty())
            return ret.NyquistZone
        
        if name in ['DAC_Replay_count', 'DAC_Relpay_continue', 'DAC_TriggerDelay']:
            ch = kw.get('chn', 1)
            ret = self.handle.GetSequencePar(ZW_QCS220_pb2.ParGetSequencePar(chn = ch))

            if name in ['DAC_Replay_count']:
                return ret.replay_times
            elif name in ['DAC_TriggerDelay']:
                return ret.trigger_delay/self.sample_rate/1e9
            elif name in ['DAC_Relpay_continue']:
                return ret.replay_continue
    
    def setSequence(self, slotID, chn, waveID, seq):
        # print(slotID)
        # print(chn)
        # print(waveID)
        # print(self._triger_delay[chn-1])
        # print(self._replay_cnt[chn-1])
        # print(self._relpay_continuou[chn-1])
        # seq_str = ''.join(seq_b)
        # print(type(seq_str))
        # print(seq_str)
        # seqb = seq.__dict__
        # print(seqb)
        bytes_seqb = pickle.dumps(seq)
        self.handle.setSequence(ZW_QCS220_pb2.ParSetSequence(slotID = slotID,
                                                                   chn = chn - 1,
                                                                   waveID = waveID,
                                                                   trigger_delay = self._triger_delay[chn-1],
                                                                   replay_times = self._replay_cnt[chn-1],
                                                                   replay_continue = self._relpay_continuou[chn-1],
                                                                   seq_b = bytes_seqb)
        )

    def getResult(self, ch, option = 'IQ'):

        if ch:  # list有数据，读取指定通道
            chn = ch[1]
            # print("chn:%d"%chn)
            if option in ['raw']:   # 读取原始AD数据
                while 1:
                    ret = self.handle.rd_adc_data(ZW_QCS220_pb2.ParAdcData(adc_channel_num = chn - 1,
                                                                                        times = self._adc_trigger_times[chn -1],
                                                                                        save_len = self._adc_savelen[chn - 1]))
                    save_len_i = ret.save_len
                    # print("save_len_i:%d" %save_len_i)
                    if save_len_i > 0:
                        # print("save_len_i:%d" %save_len_i)
                        adc_data = np.frombuffer(ret.adc_data, dtype=np.int32)
                        return adc_data
                    else:
                        time.sleep(0.01)

            if option in ['IQ']:    # 读取解模数据
                tot_num = self._mul_qbit_phase[chn - 1]
                # print("tot_num:%d" %tot_num)
                # print(self._mul_f_data[chn - 1])
                muldata = []
                for modle_num in range(tot_num):
                    # print("modle_num:%d" %modle_num)
                    while 1:
                        ret = self.handle.rd_adc_mul_data(ZW_QCS220_pb2.ParAdcMulData(adc_channel = chn - 1,
                                                                                        modle_num = modle_num,
                                                                                        times = self._mul_trigger_times[chn -1]))
                        read_data_len = ret.read_data_len
                        if read_data_len != -1:
                            # print("read_data_len" ,read_data_len)
                            mul_data_bufe = np.frombuffer(ret.recv_data, dtype = np.complex128)
                            # sample_times = len(self._mul_f_data[chn - 1][modle_num][2])
                            # mul_data_bufe = np.reshape(mul_data_bufe,(sample_times,-1),order = 'f')
                            # muldata.extend(mul_data_bufe)
                            muldata.append(mul_data_bufe)
                            break
                muldata = np.array(muldata).T
                return muldata
            
        else:   # list为空，读取全部通道解模数据

            
            # print("tot_num%d" %tot_num)
            muldata = []
            for channel in range(self.CHs_num):
                tot_num = self._mul_qbit_phase[channel]
                # print("channel:%d" %channel)
                for modle_num in range(tot_num):
                    # print("modle_num:%d" %modle_num)
                    while 1:
                        ret = self.handle.rd_adc_mul_data(ZW_QCS220_pb2.ParAdcMulData(adc_channel = channel,
                                                                                        modle_num = modle_num))
                        read_data_len = ret.read_data_len
                        if read_data_len != -1:
                            mul_data_bufe = np.frombuffer(ret.recv_data, dtype = np.complex128)
                            sample_times = len(self._mul_f_data[channel][modle_num][2])
                            mul_data_bufe = np.reshape(mul_data_bufe,(sample_times,-1),order = 'f')
                            muldata.extend(mul_data_bufe)
                            break

            muldata = np.array(muldata).T
            return muldata
    
    def run(self,):
        for i in range(1, self.CHs_num+1, 1):
            self.on(i)
        self.handle.trigger_ctrl(ZW_QCS220_pb2.ParTrigger(trigger_source = self._trigger_source,
                                 trigger_us = self._trigger_us,
                                 trigger_num = self._trigger_num,
                                 trigger_continue = self._trigger_continue)
        )    
        
    def stop(self,):
        for i in range(1, self.CHs_num+1, 1):
            self.off(i)
        self.triggerClose()

    def set_TRIG(self, name, value):
        if name in ['TriggerPeriod']:
             self._trigger_us = round(value*1e6)
        elif name in ['TriggerSource']:
            assert value in ['Internal',
                             'External'], 'Trigger source is not supported.'
            self._trigger_source = int(value == 'External')
        elif name in ['TriggerNumber']:
            self._trigger_num = value
        elif name in ['TriggerContinue']:
            self._trigger_continue = int(value)
        elif name in ['TriggerOff']:
            self.triggerClose()
        elif name in ['Trigger']:
            self.Trig()
        
    def get_Trig(self, name):
        ret = self.handle.get_trigger_par(Empty())

        if name in ['TriggerPeriod']:
             return ret.trigger_us/1e6
        elif name in ['TriggerSource']:
            return ret.trigger_source
        elif name in ['TriggerNumber']:
            return ret.trigger_num
        elif name in ['TriggerContinue']:
            return ret.trigger_continue


    def Trig(self):
        '''  
           trigger_source 0 为内部触发，1为外部触发
           trigger_us 触发周期单位us; 8Gsps 6.25MHz, 对应160ns,必须为对应时长的整倍数
           trigger_num 触发次数，当trigger_continue为1时无效
           trigger_continue 1 为连续触发模式，此时触发次数无效；0 为按触发次数触发。
        '''
        ret = self.handle.trigger_ctrl(
            ZW_QCS220_pb2.ParTrigger(trigger_source=self._trigger_source,
                                           trigger_us=self._trigger_us,
                                           trigger_num=self._trigger_num,
                                           trigger_continue=self._trigger_continue)
        )
        assert ret.str == 'ok', 'Error in `Trig()`'

    def triggerClose(self):
        '''
        该函数用于关闭触发器
        '''
        ret = self.handle.trigger_close(Empty())
        assert ret.str == 'ok', 'Error in `triggerClose()`'

    def set_DA(self, name, value, ch):
        """ch starts from 1
        """

        if name in ['Output']:
            if value:
                self.on(ch=ch)
            else:
                self.off(ch=ch)
        elif name in ['Nyquist']:
            if value == 'normal':
                if self._nyquist[ch-1] in ['mix', None]:
                    self.handle.rfdac_SetNyquistZone(ZW_QCS220_pb2.ParDacSetNyquistZone(NyquistZone = 0, ch = ch))
                    self._nyquist[ch-1] = 'normal'
                    time.sleep(0.1)
            elif value == 'mix':
                if self._nyquist[ch-1] in ['normal', None]:
                    self.handle.rfdac_SetNyquistZone(ZW_QCS220_pb2.ParDacSetNyquistZone(NyquistZone = 1, ch = ch))
                    self._nyquist[ch-1] = 'mix'
                    time.sleep(0.1)
            else:
                pass
        elif name in ['DAC_Replay_count']:
            self._replay_cnt[ch-1] = int(value)
            if self._replay_cnt[ch - 1] > self.max_value:
                self._replay_cnt[ch - 1] = self.max_value
            self.handle.dac_ch_ctrl(ZW_QCS220_pb2.ParDacChCtrl(channel_num = ch - 1,
                                                                trigger_delay = self._triger_delay[ch-1],
                                                                replay_times = self._replay_cnt[ch-1],
                                                                replay_continue = self._relpay_continuou[ch-1]))
        elif name in ['DAC_TriggerDelay']:
            if ch < 7:
                samplerate = self.sample_rate[0]
            elif ch < 15:
                samplerate = self.sample_rate[1]
            elif ch <= 22:
                samplerate = self.sample_rate[2]
            else:
                print('ch must be 1~22')
                return
            samplerate 
            self._triger_delay[ch-1] = round(value*samplerate*1e9)
            self.handle.dac_ch_ctrl(ZW_QCS220_pb2.ParDacChCtrl(channel_num = ch - 1,
                                                                trigger_delay = self._triger_delay[ch-1],
                                                                replay_times = self._replay_cnt[ch-1],
                                                                replay_continue = self._relpay_continuou[ch-1]))
        elif name in ['DAC_Relpay_continue']:
            self._relpay_continuou[ch-1] = int(value)
            self.handle.dac_ch_ctrl(ZW_QCS220_pb2.ParDacChCtrl(channel_num = ch - 1,
                                                                trigger_delay = self._triger_delay[ch-1],
                                                                replay_times = self._replay_cnt[ch-1],
                                                                replay_continue = self._relpay_continuou[ch-1]))
        elif name in ['DAC_Offset']:
            if ch > 22 or ch < 15:
                print("只有15~22通道可设置偏置")
                return
            self._dac_offset[ch -1] = value
            self.handle.set_ch_offset(ZW_QCS220_pb2.ParSetChOffset(channel_num = ch -1,
                                                                   offset = value))
        elif name in ['DAC_Feedback_Set_Data']:
            self._feedback_data[ch - 1] = value
        elif name in ['DAC_Feedback_Set_Message']:
            self._feedback_message[ch - 1] = value
        elif name in ['DAC_Feedback_En']:
            enbale = value
            feedback_data = self._feedback_data[ch - 1]
            fblenmax = len(feedback_data)
            fblen = []
            for i in range(8):
                # print(i)
                if i >= fblenmax:
                    fblen.append(0)
                else:
                    fblen.append(len(feedback_data[i]))

            fbdata = np.array(feedback_data)

            for i in range(8):
                fbdata = np.insert(fbdata,i,fblen[i])

            fbdata = fbdata.tobytes()

            fbmessage = np.array(self._feedback_message[ch - 1])
            fbmessage = fbmessage.tobytes()

            self.handle.dac_feedback_set(ZW_QCS220_pb2.ParDacFeedBackSet(channel_num = ch -1,
                                                                          feedback_en = enbale,
                                                                          dac_data = fbdata,
                                                                          fb_message = fbmessage))
        elif name in ['DAC_Data']:
            # print(self._triger_delay[ch - 1], self._replay_cnt[ch - 1], self._relpay_continuou[ch-1])
            self.handle.dac_updata(ZW_QCS220_pb2.ParDacUpdata(channel_num = ch - 1,
                                                                 trigger_delay = self._triger_delay[ch - 1],
                                                                 replay_times = self._replay_cnt[ch - 1],
                                                                 replay_continue = self._relpay_continuou[ch-1],
                                                                 dac_data = value.tobytes()))

    def set_mul(self, name, value, ch):
        # print('set_mul')
        # print(value)
        # if name in ['MUL_TriggerDelay', 'MUL_Times', 'MUL_F_Len', 'MUL_F_Data', 'MUL_SetPars']:

        if name in ['MUL_TriggerDelay']:
            self._mul_trigger_delay[ch - 1] = round(value*self.adc_sample_rate*1e9)
        
        if name in ['MUL_Times']:
            self._mul_trigger_times[ch - 1] = value

        if name in ['MUL_F_Len']:
            self._mul_f_len[ch - 1] = value

        if name in ['MUL_F_Data']:
            
            # for i in range(len(value)):
            #     print(np.round(value[i][2]*self.adc_sample_rate*1e9))
            #     value[i][2] = np.round(value[i][2]*self.adc_sample_rate*1e9)

            self._mul_f_data[ch - 1] = value
            self._mul_qbit_phase[ch - 1] = len(value)
        if name in ['MUL_SetPars']:
            # print(self._mul_f_data[ch -1])
            # mul_f = self._mul_f_data[ch -1]
            # mul_f_ii = []
            # mul_f_iii = []
            # for i in range(len(mul_f)):
            #     mul_f_ii.extend(np.reshape(mul_f[i][:2],(-1)))
            #     mul_f_ii.extend([len(mul_f[i][2])])
            #     mul_f_ii.extend(np.reshape(mul_f[i][2],(-1)))

            # mul_f = np.asarray(mul_f_ii)
            # mul_f = mul_f.tobytes()
            mul_f = pickle.dumps(self._mul_f_data[ch -1])

            self.handle.rd_adc_mul_data_ctrl(ZW_QCS220_pb2.ParAdcMulDataCtrl(adc_channel_num = (ch-1),
                                                                                  trigger_delay = self._mul_trigger_delay[ch-1],
                                                                                  times = self._mul_trigger_times[ch-1],
                                                                                  mul_f_len = self._mul_f_len[ch-1],
                                                                                  mul_f = mul_f))

    def on(self, ch):  # 打开通道
        ret = self.handle.dac_open(ZW_QCS220_pb2.ParDacOpen(channel_num = (ch-1)))

        # assert ret.str == 'ok', 'Error in `on()`'

    def off(self, ch):  # 关闭通道
        ret = self.handle.dac_close(ZW_QCS220_pb2.ParDacOpen(channel_num = (ch-1)))
        # assert ret.str == 'ok', 'Error in `off()`'


