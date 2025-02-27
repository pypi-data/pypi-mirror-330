import os
import json
from datetime import datetime,timedelta
import dateutil.parser
import dateutil.rrule
import numpy as np
import pandas as pd
import xarray as xr
from . import Utils
import io
import math
import types
import matplotlib as mpl
from joblib import Parallel,delayed
import xml.etree.ElementTree as ET
from . import base,Utils
originData=base.originData
parse_element=Utils.parse_element

#region 绘图参数
velocity_colors=[
    '#951262',
    '#ED2226',
    '#EB3E22',
    '#EF6A26',
    '#F58324',
    '#F3A122',
    '#FDB52A',
    '#FDD31E',
    '#F9EF1A',
    '#F7FD1C',
    '#D9E9F1',
    '#C7D7F1',
    '#B1C7EB',
    '#99B5E7',
    '#83A5DD',
    '#6E93D3',
    '#6089CB',
    '#4C7CC3',
    '#4870BB',
    '#406AB9',
    '#2A42AB',
    '#242681',
    '#242074',
    '#22206A',
    '#1C622C',
    '#067E42',
    '#0C8B42',
    '#30BD4C',
    '#4EC14A',
    '#58C546',
    '#87742E'
]
velocity_levels=[-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.1,0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,2,2.5,3,4,5,6,7,8,9,10]
velocity_cmap = (mpl.colors.ListedColormap(velocity_colors).with_extremes(over=velocity_colors[-1], under=velocity_colors[0]))
velocity_norm = mpl.colors.BoundaryNorm(velocity_levels, velocity_cmap.N)
#endregion

#region 风廓线雷达数据文件元数据
# 定义变量名字典
line0_variables = {
    'WNDRAD':'风廓线雷达数据文件标识',
    'File_version':'文件版本号'
}
line1_variables = {
    'Station_Id':'站号',
    'Longitude':'经度',
    'Latitude':'纬度',
    'Altitude':'海拔高度',
    'Machine_Type':'风廓线仪型号',
}
line2_variables = {
    'Antenna_Gain': '天线增益',
    'Feeder_Loss': '馈线损耗',
    'East_Beam_Angle': '东波束与铅垂线的夹角',
    'West_Beam_Angle': '西波束与铅垂线的夹角',
    'South_Beam_Angle': '南波束与铅垂线的夹角',
    'North_Beam_Angle': '北波束与铅垂线的夹角',
    'Center_Row_Beam_Angle': '中（行）波束与铅垂线的夹角（度）',
    'Center_Column_Beam_Angle': '中（列）波束与铅垂线的夹角（度）',
    'Number_Of_Beams': '波束数',
    'Sampling_Frequency': '采样频率',
    'Transmit_Wavelength': '发射波长',
    'Pulse_Repetition_Frequency': '脉冲重复频率',
    'Pulse_Width': '脉冲宽度',
    'Horizontal_Beam_Width': '水平波束宽度',
    'Vertical_Beam_Width': '垂直波束宽度',
    'Peak_Transmit_Power': '发射峰值功率',
    'Average_Transmit_Power': '发射平均功率',
    'Start_Sampling_Height': '起始采样高度',
    'End_Sampling_Height': '终止采样高度'
}
line3_variables = {
    'Time_Source': '时间来源',
    'Observation_Start_Time': '观测开始时间',
    'Observation_End_Time': '观测结束时间',
    'Calibration_Status': '标校状态',
    'Incoherent_Accumulation': '非相干积累',
    'Coherent_Accumulation': '相干积累',
    'FFT_Points': 'Fft点数',
    'Spectral_Averages': '谱平均数',
    'Beam_Order_Flag': '波束顺序标志',
    'East_Beam_Azimuth_Correction': '东波束方位角修正值',
    'West_Beam_Azimuth_Correction': '西波束方位角修正值',
    'South_Beam_Azimuth_Correction': '南波束方位角修正值',
    'North_Beam_Azimuth_Correction': '北波束方位角修正值'
}
L2data_variables={
    'Sampling_Height': '采样高度',
    'Velocity_Spectrum_Width': '速度谱宽',
    'Signal_To_Noise_Ratio': '信噪比',
    'Radial_Velocity': '径向速度'
}
L3meta_variables={
    "Station_Id": "区站号",
    "Longitude": "经度",
    "Latitude": "纬度",
    "Altitude": "观测场拔海高度",
    "Machine_Type": "风廓线仪型号",
    "Observation_Time": "观测时间"
}
L3data_variables = {
    "Sampling_Height": "采样高度",
    "Wind_Direction": "水平风向",
    "Wind_Speed": "水平风速",
    "Vertical_Wind_Speed": "垂直风速",
    "Horizontal_Confidence": "水平方向可信度",
    "Vertical_Confidence": "垂直方向可信度",
    "Cn2": "Cn2"
} 
L1Struct_FileTag = np.dtype([
    ('FileID', 'S8'),   # 字符类型数组，用于存储文件标识，字节数为8，这里固定值为WNDFFT
    ('VersionNo', 'f4'),  # 单精度浮点数类型，用于表示数据格式版本号，字节数为4，格式为两位整数两位小数，示例值如01.20
    ('FileHeaderLength', 'i4') # 32位整数类型，用于表示文件头的长度，字节数为4，是4位整数
])
L1Struct_SiteInfo = np.dtype([
    ('Country', 'S16'),
    ('Province', 'S16'),
    ('StationNumber', 'S16'),
    ('Station', 'S16'),
    ('RadarType', 'S16'),
    ('Longitude', 'S16'),
    ('Latitude', 'S16'),
    ('Altitude', 'S16'),
    ('Temp', 'S40')
])
L1Struct_PerformanceInfo = np.dtype([
    ('Ae', 'i4'),
    ('AgcWast', 'f4'),
    ('AngleE', 'f4'),
    ('AngleW', 'f4'),
    ('AngleS', 'f4'),
    ('AngleN', 'f4'),
    ('AngleR', 'f4'),
    ('AngleL', 'f4'),
    ('ScanBeamN', 'u4'),
    ('SampleP', 'u4'),
    ('WaveLength', 'u4'),
    ('Prp', 'f4'),
    ('PusleW', 'f4'),
    ('HBeamW', 'u2'),
    ('VBeamW', 'u2'),
    ('TranPp', 'f4'),
    ('TranAp', 'f4'),
    ('StartSamplBin', 'u4'),
    ('EndSamplBin', 'u4'),
    ('BinLength', 'i2'),
    ('BinNum', 'i2'),
    ('Temp', 'S40')
])
L1Struct_ObservationInfo = np.dtype([
    ('SYear', 'u2'),
    ('SMonth', 'u1'),
    ('SDay', 'u1'),
    ('SHour', 'u1'),
    ('SMinute', 'u1'),
    ('SSecond', 'u1'),
    ('TimeP', 'u1'),
    ('SMillisecond', 'u4'),
    ('Calibration', 'u2'),
    ('BeamfxChange', 'i2'),
    ('EYear', 'u2'),
    ('EMonth', 'u1'),
    ('EDay', 'u1'),
    ('EHour', 'u1'),
    ('EMinute', 'u1'),
    ('ESecond', 'u1'),
    ('NNtr', 'i1'),
    ('Ntr', 'i2'),
    ('SpAver', 'u2'),
    ('Fft', 'u2'),
    ('unknow', 'u2'),
    ('BeamDir', 'S12'),
    ('AzimuthE', 'f4'),
    ('AzimuthW', 'f4'),
    ('AzimuthS', 'f4'),
    ('AzimuthN', 'f4'),
    ('Temp', 'S40')
])
#endregion


L1Data=types.new_class('L1Data',(originData,))
L1ObData=types.new_class('L1ObData',(originData,))
L2Data=types.new_class('L2Data',(originData,))
L2LevelData=types.new_class('L2LevelData',(originData,))
L3Data=types.new_class('L3Data',(originData,))
L3Datas=types.new_class('L3Datas',(originData,))
CalibrationData=types.new_class('CalibrationDatas',(originData,))
StatusData=types.new_class('StatusData',(originData,))


def readSingleL1file(fp:str)->L1Data:
    '''
    读取风廓线雷达单个L1功率谱文件，文件命名格式为：Z_RADA_I_IIiii_yyyyMMddhhmmss_O_WPRD_雷达型号_FFT.BIN
    args:
        fp:L1功率谱文件路径
    return:
        L1Data对象
    '''
    try:
        with open(fp, 'rb') as f:
            bs=f.read()
        fkxL1obj=L1Data()
        bsoffset = 0
        data = np.frombuffer(bs[bsoffset:bsoffset + L1Struct_FileTag.itemsize], L1Struct_FileTag)
        bsoffset = bsoffset + L1Struct_FileTag.itemsize
        fkxL1obj['FileTag'] = originData.from_dict({name: data[name][0] for name in data.dtype.names})
        fkxL1obj.FileTag['FileID'] = fkxL1obj.FileTag['FileID'].split(b'\x00')[0].decode('gbk')
        data = np.frombuffer(bs[bsoffset:bsoffset + L1Struct_SiteInfo.itemsize], L1Struct_SiteInfo)
        bsoffset = bsoffset + L1Struct_SiteInfo.itemsize
        fkxL1obj['SiteInfo'] = originData.from_dict(
            {name: data[name][0].split(b'\x00')[0].decode('gbk') for name in data.dtype.names}
        )
        fkxL1obj['Datas'] = []
        while (bsoffset < len(bs)):
            L1ObDatai = L1ObData()
            data = np.frombuffer(bs[bsoffset:bsoffset + L1Struct_PerformanceInfo.itemsize], L1Struct_PerformanceInfo)
            bsoffset = bsoffset + L1Struct_PerformanceInfo.itemsize
            L1ObDatai['PerformanceInfo'] = originData.from_dict({name: data[name][0] for name in data.dtype.names})
            L1ObDatai.PerformanceInfo['Temp'] = L1ObDatai.PerformanceInfo['Temp'].split(b'\x00')[0].decode('gbk')
            data = np.frombuffer(bs[bsoffset:bsoffset + L1Struct_ObservationInfo.itemsize], L1Struct_ObservationInfo)
            bsoffset = bsoffset + L1Struct_ObservationInfo.itemsize
            L1ObDatai['ObservationInfo'] = originData.from_dict({name: data[name][0] for name in data.dtype.names})
            L1ObDatai.ObservationInfo.BeamDir = L1ObDatai.ObservationInfo['BeamDir'].decode('gbk')
            L1ObDatai.ObservationInfo.Temp = L1ObDatai.ObservationInfo['Temp'].decode('gbk')
            L1ObDatai.Speed_per_FFT_point = L1ObDatai.PerformanceInfo.Prp / 2 / L1ObDatai.ObservationInfo.Fft * L1ObDatai.PerformanceInfo.WaveLength * 1e-5
            data_len = L1ObDatai.ObservationInfo.Fft * L1ObDatai.PerformanceInfo.BinNum * L1ObDatai.PerformanceInfo.ScanBeamN
            data = np.frombuffer(
                bs[bsoffset:bsoffset + 4 * data_len],
                'f4',
                count=data_len
            ).reshape(L1ObDatai.PerformanceInfo.ScanBeamN, L1ObDatai.PerformanceInfo.BinNum,
                      L1ObDatai.ObservationInfo.Fft)
            bsoffset = bsoffset + 4 * data_len
            da = xr.DataArray(
                data,
                dims=['Beam', 'height', 'Fft'],
                coords={
                    'Beam': list(L1ObDatai.ObservationInfo.BeamDir),
                    'height': np.arange(
                        L1ObDatai.PerformanceInfo.BinNum) * L1ObDatai.PerformanceInfo.BinLength + L1ObDatai.PerformanceInfo.StartSamplBin,
                    'Fft': np.arange(L1ObDatai.ObservationInfo.Fft)
                },
                attrs={
                    'WaveLength': L1ObDatai.PerformanceInfo.WaveLength,
                    'Prp': L1ObDatai.PerformanceInfo.Prp,
                    'ObStarTime': datetime(
                        L1ObDatai.ObservationInfo.SYear,
                        L1ObDatai.ObservationInfo.SMonth,
                        L1ObDatai.ObservationInfo.SDay,
                        L1ObDatai.ObservationInfo.SHour,
                        L1ObDatai.ObservationInfo.SMinute,
                        L1ObDatai.ObservationInfo.SSecond,
                    ),
                    'ObEndTime': datetime(
                        L1ObDatai.ObservationInfo.EYear,
                        L1ObDatai.ObservationInfo.EMonth,
                        L1ObDatai.ObservationInfo.EDay,
                        L1ObDatai.ObservationInfo.EHour,
                        L1ObDatai.ObservationInfo.EMinute,
                        L1ObDatai.ObservationInfo.ESecond,
                    ),
                    'Speed_per_FFT_point': L1ObDatai.Speed_per_FFT_point,
                    'WaveLength_unit': '1e-5 meter',
                    'Prp_unit': 'Hz',
                    'Speed_per_FFT_point_unit': 'm/s',
                    'height_unit': 'meter',
                }
            )
            L1ObDatai['DspToDpDat'] = da
            fkxL1obj['Datas'].append(L1ObDatai)
        return fkxL1obj
    except Exception as ex:
        print(ex)
        return None

def readSingleL2file(fp:str)->L2Data:
    '''
    读取风廓线雷达单个L2径向数据文件，文件命名格式为：Z_RADA_I_IIiii_yyyyMMddhhmmss_O_WPRD_雷达型号_RAD.TXT
    args:
        fp:L2产品径向数据文件路径
    return:
        L2Data对象
    '''
    try:
        with open(fp, 'r') as f:
            lines = [line.strip() for line in f]        
        fkxL2obj=L2Data()

        lineds=lines[0].split(' ')    
        keys=list(line0_variables.keys())    
        for i, key in enumerate(keys):
            fkxL2obj[key] = lineds[i]

        lineds=lines[1].split(' ')
        keys=list(line1_variables.keys())
        for i, key in enumerate(keys):
            fkxL2obj[key] = lineds[i] if i == 0 or i == 4 else Utils.dtryfloat(lineds[i])

        fkxL2obj['levels']=[]

        tsplitlineis = [1] + [i for i in range(5, len(lines)) if lines[i] == 'NNNN']

        columnnames=list(L2data_variables.keys())
        leveli=None
        beamj=0
        Beam_Count=1
        dfleveli=[]
        for i in range(len(tsplitlineis)-1):
            lineStart=tsplitlineis[i]
            lineEnd=tsplitlineis[i+1]  
            if(i%Beam_Count==0):
                leveli=L2LevelData()
                dfleveli=[]
                beamj=0
                lineStart=lineStart+1
                lineds=lines[lineStart].split(' ')
                keys=list(line2_variables.keys())
                for j in range(len(keys)):
                    key=keys[j]
                    leveli[key]=Utils.dtryfloat(lineds[j])

                lineStart=lineStart+1
                lineds=lines[lineStart].split(' ')
                keys=list(line3_variables.keys())
                for j, key in enumerate(keys):
                    if(key=='Beam_Order_Flag'):
                        leveli[key]=lineds[j].replace('/','')
                        leveli['Beam_Order_Flags']=list(map(lambda bi:leveli['Beam_Order_Flag'][bi],range(len(leveli['Beam_Order_Flag']))))
                        leveli['Beam_Count']=len(leveli['Beam_Order_Flag'])
                    else:
                        if(key=='Observation_Start_Time' or key=='Observation_End_Time'):
                            leveli[key]=dateutil.parser.parse(lineds[j])
                        else:           
                            leveli[key]=Utils.dtryfloat(lineds[j])
                Beam_Count=leveli['Beam_Count']

            dfleveli.append(lines[lineStart+2:lineEnd])
            beamj=beamj+1
            
            if(beamj==Beam_Count):            
                # 顺序逐层添加（不包含末尾层）
                dlevelcolumnnames = [
                    f"{beam_order_flag}_{key}" for beam_order_flag in leveli['Beam_Order_Flags'] for key in columnnames  
                ] 
                sscolumnnames=[dlevelcolumnnames[i] for i in range(0,len(dlevelcolumnnames),len(columnnames))]
                dfleveli=np.array(dfleveli).T
                dfleveli=pd.read_csv(io.StringIO('\n'.join([' '.join(x) for x in list(dfleveli)])),sep=' ',header=None,names=dlevelcolumnnames)
                dfleveli=dfleveli.rename(columns={sscolumnnames[0]:sscolumnnames[0][2:]}).drop(sscolumnnames[1:],axis=1)
                dfleveli=dfleveli.apply(lambda x:pd.to_numeric(x,errors='coerce'))   
                leveli['Data']=dfleveli
                fkxL2obj['levels'].append(leveli)

        
        fkxL2obj['Beam_Order_Flags']=fkxL2obj['levels'][0]['Beam_Order_Flags']
        fkxL2obj['Beam_Count']=fkxL2obj['levels'][0]['Beam_Count']
        levels_count=len(fkxL2obj['levels'])
        fkxL2obj['levels_count']=levels_count
        if(levels_count==1):
            dlevels=['low']
        else:
            if(levels_count==2):
                dlevels=['low','high']
            else:
                dlevels=['low','middle','high']
        fkxL2obj['dlevels']=dlevels

        return fkxL2obj
    except Exception as ex:
        print(ex)
        # raise ex
        return None

def CalcL2toL3(fkxL2obj,qcw=3,interp=False,rollmean=True,rollmeancout=5):
    '''
    基于L2数据数学计算L3数据
    args:
        fkxL2obj:L2Data对象
        qcw:质控阈值
        interp:是否插值
        rollmean:是否滚动平均
        rollmeancout:滚动平均窗口大小
    return:
        L3Data对象
    '''

    Calc_L2_data=[]
    for j,levelj in enumerate(fkxL2obj.levels):
        dlevelj=levelj.Data
        qcindexs=dlevelj[dlevelj['E_Radial_Velocity']+dlevelj['W_Radial_Velocity']>qcw].index
        dlevelj.loc[qcindexs,'E_Radial_Velocity']=np.nan
        dlevelj.loc[qcindexs,'W_Radial_Velocity']=np.nan
        qcindexs=dlevelj[dlevelj['N_Radial_Velocity']+dlevelj['S_Radial_Velocity']>qcw].index
        dlevelj.loc[qcindexs,'N_Radial_Velocity']=np.nan
        dlevelj.loc[qcindexs,'S_Radial_Velocity']=np.nan

        h=dlevelj['Sampling_Height'].values
        Vre=dlevelj['E_Radial_Velocity'].values
        # Wre=dlevelj['E_Signal_To_Noise_Ratio'].values/np.exp(dlevelj['E_Velocity_Spectrum_Width'].values*20)
        Wre=1/np.exp(dlevelj['E_Velocity_Spectrum_Width'].values)
        Vrn=dlevelj['N_Radial_Velocity'].values
        # Wrn=dlevelj['N_Signal_To_Noise_Ratio'].values/np.exp(dlevelj['N_Velocity_Spectrum_Width'].values*20)
        Wrn=1/np.exp(dlevelj['N_Velocity_Spectrum_Width'].values)
        Vw=dlevelj['R_Radial_Velocity'].values
        # Ww=dlevelj['R_Signal_To_Noise_Ratio'].values/np.exp(dlevelj['R_Velocity_Spectrum_Width'].values*20)
        Ww=1/np.exp(dlevelj['R_Velocity_Spectrum_Width'].values)
        Vrw=dlevelj['W_Radial_Velocity'].values
        # Wrw=dlevelj['W_Signal_To_Noise_Ratio'].values/np.exp(dlevelj['W_Velocity_Spectrum_Width'].values*20)
        Wrw=1/np.exp(dlevelj['W_Velocity_Spectrum_Width'].values)
        Vrs=dlevelj['S_Radial_Velocity'].values
        # Wrs=dlevelj['S_Signal_To_Noise_Ratio'].values/np.exp(dlevelj['S_Velocity_Spectrum_Width'].values*20)
        Wrs=1/np.exp(dlevelj['S_Velocity_Spectrum_Width'].values)
        Vs=np.array([Vre,Vrw,Vrs,Vrn,Vw])
        Ws=np.array([Wre,Wrw,Wrs,Wrn,Ww])

        Vsw=np.array([
            np.where(np.isnan(Vrw),np.nan,Vre),np.where(np.isnan(Vre),np.nan,Vrw),
            np.where(np.isnan(Vrn),np.nan,Vrs),np.where(np.isnan(Vrs),np.nan,Vrn),
            Vw
        ])
        w=np.sum(((Vsw*Ws)/np.nansum(Ws,axis=0)),axis=0)
        # w=np.nanmean(Vsw,axis=0)

        a_e=levelj['East_Beam_Angle']+levelj['East_Beam_Azimuth_Correction']
        o_e=90-a_e
        po_e=math.radians(o_e)
        u_e=(w*math.sin(po_e)-Vre)/math.cos(po_e)
        a_w=levelj['West_Beam_Angle']+levelj['West_Beam_Azimuth_Correction']
        o_w=90-a_w
        po_w=math.radians(o_w)
        u_w=(Vrw-w*math.sin(po_w))/math.cos(po_w)    
        u=np.sum((np.array([u_e,u_w])*Ws[:2])/np.nansum(Ws[:2],axis=0),axis=0) 

        a_s=levelj['South_Beam_Angle']+levelj['South_Beam_Azimuth_Correction']
        o_s=90-a_s
        po_s=math.radians(o_s)
        v_s=(Vrs-w*math.sin(po_s))/math.cos(po_s)
        a_n=levelj['North_Beam_Angle']+levelj['North_Beam_Azimuth_Correction']
        o_n=90-a_n
        po_n=math.radians(o_n)
        v_n=(w*math.sin(po_n)-Vrn)/math.cos(po_n)   
        v=np.sum((np.array([v_s,v_n])*Ws[2:4])/np.nansum(Ws[2:4],axis=0),axis=0)    

        calcdfi=pd.DataFrame({
            'Sampling_Height':h,
            'Vertical_Wind_Speed':w,
            'U_Wind_Speed':u,
            # 'U_Wind_Speede':u_e,
            # 'U_Wind_Speedw':u_w,
            'V_Wind_Speed':v,
            # 'V_Wind_Speedn':v_n,
            # 'V_Wind_Speeds':v_s
        })
        Calc_L2_data.append(calcdfi)  
    Calc_L3Data=pd.concat(Calc_L2_data).reset_index(drop=True).groupby('Sampling_Height').mean().reset_index()
    if(interp):
        Calc_L3Data=Calc_L3Data.set_index('Sampling_Height').interpolate(method='linear').reset_index()
    if(rollmean):        
        Calc_L3Data=Calc_L3Data.set_index('Sampling_Height').sort_index().rolling(window=rollmeancout, min_periods=1).mean().reset_index()
    wdir,wspd=Utils.vuv2w(Calc_L3Data['U_Wind_Speed'].values,Calc_L3Data['V_Wind_Speed'].values)
    Calc_L3Data['Wind_Direction']=wdir
    Calc_L3Data['Wind_Speed']=wspd
    Calc_L3Data=Calc_L3Data[['Sampling_Height', 'Wind_Direction', 'Wind_Speed', 'Vertical_Wind_Speed', 'U_Wind_Speed','V_Wind_Speed']]
    Calc_L3Data.dropna(inplace=True)   
    
    fkxL3obj=L3Data()
    keys=list(line0_variables.keys())    
    for key in keys:
        fkxL3obj[key]=fkxL2obj[key]
    keys=list(L3meta_variables.keys())    
    for key in keys:
        if(key=='Observation_Time'):
            fkxL3obj[key]=fkxL2obj.levels[0]['Observation_End_Time']     
        else:
            fkxL3obj[key]=fkxL2obj[key]      
    fkxL3obj['Data']=Calc_L3Data
    
    return fkxL3obj

def readSingleL3file(fp:str)->L3Data:
    '''
    读取风廓线雷达单个L3产品数据文件；
    支持
    ROBS：Z_RADA_I_IIiii_yyyyMMddhhmmss_P_WPRD_雷达型号_ROBS.TXT
    HOBS：Z_RADA_I_IIiii_yyyyMMddhhmmss_P_WPRD_雷达型号_HOBS.TXT
    OOBS：Z_RADA_I_IIiii_yyyyMMddhhmmss_P_WPRD_雷达型号_OOBS.TXT
    args:
        fp:L3产品文件路径
    return:
        L3Data对象
    '''
    try:
        with open(fp, 'r') as f:
            lines = [line.strip() for line in f]      

        fkxL3obj=L3Data()    
        lineds=lines[0].split(' ')    
        keys=list(line0_variables.keys())    
        for i, key in enumerate(keys):
            fkxL3obj[key] = lineds[i]

        lineds=lines[1].split(' ')
        keys=list(L3meta_variables.keys())
        for i, key in enumerate(keys):
            if(key=='Station_Id' or key=='Machine_Type'):            
                fkxL3obj[key]=lineds[i]
            else:
                if(key=='Observation_Time'):
                    fkxL3obj[key]=dateutil.parser.parse(lineds[i])
                else:
                    fkxL3obj[key]=float(lineds[i])

        da=pd.read_fwf(
            io.StringIO('\n'.join(lines[3:-1])), 
            widths=[5, 6, 6, 7, 4, 4, 9],
            encoding='gbk',
            names=list(L3data_variables.keys()),
            dtype=str
        )
        # 之前定义各列使用 str 类型存储，后续需要把 //// 表示的缺失值用 numpy.nan 进行替换
        da=da.apply(lambda x:pd.to_numeric(x,errors='coerce'))  
        uvs = Utils.vw2uv(da['Wind_Direction'].values, da['Wind_Speed'].values)
        da['U_Wind_Speed']=uvs[0]
        da['V_Wind_Speed']=uvs[1]
        fkxL3obj['Data']=da
        return fkxL3obj
    except Exception as ex:
        print(ex)
        # raise ex
        return None

def readL3files(fps:list,use_multiprocess=False,multiproces_corenum=-1)->L3Datas:
    """
    读取多个L3产品文件，并返回L3Datas对象。

    参数:
        fps (list): L3产品文件路径列表。
        use_multiprocess (bool): 是否使用多进程读取文件，默认为False。
        multiproces_corenum (int): 多进程核心数量，默认为-1表示使用所有可用核心。

    返回:
        L3Datas: 包含所有读取的L3Data对象的L3Datas实例。
    """
    rbds=L3Datas()
    if(use_multiprocess):
        rbds['L3Datas']=Parallel(n_jobs=multiproces_corenum)(delayed(readSingleL3file)(fp) for fp in fps)
    else:
        rbds['L3Datas']=[readSingleL3file(fp) for fp in fps]
    for i,ld in enumerate(rbds['L3Datas']):
        rbds.append(ld)    
    return rbds

def readSingleCalibrationXMLfile(fp:str)->CalibrationData:
    '''
    读取风廓线雷达单个标校数据xml格式文件；
    支持 Z_RADA_I _IIiii_yyyyMMddhhmmss_C_WPRD_雷达型号_CAL.XML
    args:
        fp:单个标校数据xml格式文件
    return:
        CalibrationData对象
    '''
    try:
        with open(fp, 'r', encoding='utf8') as f:
            xml_data = f.read()
        xmld = ET.fromstring(xml_data)
        return CalibrationData.from_dict(parse_element(xmld))
    except Exception as ex:
        print(ex)
        return None

def readSingleStatuXMLfile(fp:str)->StatusData:
    '''
    读取风廓线雷达单个状态数据xml格式文件；
    支持 Z_RADA_I_IIiii_yyyyMMddhhmmss_R_WPRD_雷达型号_STA.XML
    args:
        fp:单个状态数据xml格式文件
    return:
        StatusData对象
    '''
    try:
        with open(fp, 'r', encoding='utf8') as f:
            xml_data = f.read()
        xmld = ET.fromstring(xml_data)
        return StatusData.from_dict(parse_element(xmld))
    except Exception as ex:
        print(ex)
        return None
