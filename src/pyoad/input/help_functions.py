# -*- coding: utf-8 -*-
"""
Python module to read the .D binary data files

.. module:: help functions for input module functions

:author:
    Gil Averbuch (gil.averbuch@whoi.edu)

:copyright:
    Gil Averbuch

:license:
    This code is distributed under the terms of the
    GNU General Public License, Version 3
    (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

import numpy as np
import pandas as pd
from obspy import  UTCDateTime, Trace


def header_info_(raw_header):
    '''
    this function reads the header of a SHRU 24bit .DXX acoustic binary file. 
    
    parameters
    ----------
    file_name: numpy fromfile array

    Returns
    -------
    Header structure containing the parameters names and values
    '''



    header_list = []
    header_values = []


    # shru_num
    s_num = 0
    for c in raw_header['shru_num'][0]:
        try:
            s_num += chr(c)
        except:
            s_num = chr(c)


    header_list.append('shru_num')
    header_values.append(int(s_num[:3]))

    # channels
    n_chan = raw_header['chan'][0]
    header_list.append('channels')
    header_values.append(int(n_chan))

    # npts
    num_points = raw_header['npts'][0]
    header_list.append('npts')
    header_values.append(num_points)

    # sampling rate
    header_list.append('sampling_rate')
    header_values.append(raw_header['rhfs'][0])

    # delta
    dt = 1/raw_header['rhfs'][0]
    header_list.append('delta')
    header_values.append(dt)

    # starttime
    string = 0
    for c in raw_header['atime'][0]:
        try:
            string += chr(c)
        except:
            string = chr(c)

    start_time = UTCDateTime(str(raw_header['date'][0][0]) + str(raw_header['date'][0][1]) + 'T' + string[:15])

    header_list.append('starttime')
    header_values.append(start_time)
        
        
    # endtime
    end_time = start_time + num_points*dt
    header_list.append('endtime')
    header_values.append(end_time)



    # internal_temp
    in_temp = 0
    for c in raw_header['internal_temp'][0]:
        try:
            in_temp += chr(c)
        except:
            in_temp = chr(c)
            
    header_list.append('internal_temp')
    header_values.append(float(in_temp[:4]))


    # bat_voltage
    bat_volt = 0
    for c in raw_header['bat_voltage'][0]:
        try:
            bat_volt += chr(c)
        except:
            bat_volt = chr(c)
            
    header_list.append('bat_voltage')
    header_values.append(float(bat_volt[:4]))


    # bat_current
    bat_cur = 0
    for c in raw_header['bat_current'][0]:
        try:
            bat_cur += chr(c)
        except:
            bat_cur = chr(c)
            
    header_list.append('bat_current')
    header_values.append(float(bat_cur[:3]))

    # vla
    vla = 0
    for c in raw_header['vla'][0]:
        try:
            vla += chr(c)
        except:
            vla = chr(c)
            
    header_list.append('vla')
    header_values.append(vla)

    # hla
    hla = 0
    for c in raw_header['hla'][0]:
        try:
            hla += chr(c)
        except:
            hla = chr(c)
            
    header_list.append('hla')
    header_values.append(hla)

    header_list = pd.DataFrame(header_values, index=header_list)
    # print(header_list)

    # # print header 
    # data_type_1 = ['>u2', '>u4', 'uint16', 'uint32', 'int16', 'int32', 'float32']
    # skip_data = ['unused1', 'unused2', 'unused3', 'unused4', 'unused5', 'unused6', 'unused7', 
    #             'nav110', 'nav115', 'nav120', 'rhlat', 'rhlng', 'pos' ]

    # for name in shru_header.names:
    #     if name not in skip_data:

    #         if raw_header[name][0].dtype in data_type_1:

    #             print(name, raw_header[name][0])

    #         else:
    #             string = 0
    #             for c in raw_header[name][0]:
    #                 try:
    #                     string += chr(c)
    #                 except:
    #                     string = chr(c)

    #             print(name, string)

    # put header in an xarray object that will later contain also the data. 
    # it will have a structure of Data['header'] and Data['data']...

    return header_list



def read_waveforms_(file_name, header_df):
    '''
    Help function that reads the waveforms of a SHRU 24bit .DXX acoustic binary file.
    
    parameters
    ----------
    file_name: numpy fromfile array

    Returns
    -------
    Header structure containing the parameters names and values
    '''

    f_data = open(file_name, "rb")  # reopen the file
    data_binary = f_data.read()

    pos = 1024
    l = (len(data_binary[pos:])//128) #divide by the number of records
    npts = 1048576

    channel1 = []   # Initially save data as python list and not numpy array because .append to list is much much faster.  
    channel2 = []
    channel3 = []
    channel4 = []

    scaling = (2.5/(2**23)/20)

    chan_num = int(header_df.loc['channels'].values)

    pos_step = chan_num*3 # every 3 summed into a single data point
    
    for loc in range(pos,l, pos_step):
        
        d1 = bytearray(data_binary[loc:loc+3])
        d1.append(0)
        dpoint1 = int.from_bytes(d1, byteorder='big', signed=True) * scaling
        channel1.append(dpoint1)

        loc = loc+3
        d2 = bytearray(data_binary[loc:loc+3])
        d2.append(0)
        dpoint2 = int.from_bytes(d2, byteorder='big', signed=True) * scaling
        channel2.append(dpoint2)

        loc = loc+6
        d3 = bytearray(data_binary[loc:loc+3])
        d3.append(0)
        dpoint3 = int.from_bytes(d3, byteorder='big', signed=True) * scaling
        channel3.append(dpoint3)

        loc = loc+9
        d4 = bytearray(data_binary[loc:loc+3])
        d4.append(0)
        dpoint4 = int.from_bytes(d4, byteorder='big', signed=True) * scaling
        channel4.append(dpoint4)

    channel1 = np.asarray(channel1, dtype=np.float32)
    channel2 = np.asarray(channel2, dtype=np.float32)
    channel3 = np.asarray(channel3, dtype=np.float32)
    channel4 = np.asarray(channel4, dtype=np.float32)

    return channel1, channel2, channel3, channel4




def trace_template_(header_df):
    '''
    Help function that creates an obspy trace template for the channels
    
    parameters
    ----------
    file_name: header data frame

    Returns
    -------
    Trace template
    '''

    tr = Trace()
    tr.stats.network = 'SR' + str(header_df.loc['shru_num'].values[0])
    # tr.stats.station = 
    tr.stats.channel = 'EDH' #same as IMS for now. check IRIS for more accurate code
    tr.stats.starttime = header_df.loc['starttime'].values[0]
    tr.stats.sampling_rate = header_df.loc['sampling_rate'].values[0]
    tr.stats.delta = header_df.loc['delta'].values[0]
    tr.stats.npts = header_df.loc['npts'].values[0]
    tr.stats.calib = 1

    return tr


