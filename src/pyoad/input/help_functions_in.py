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
import matplotlib.pyplot as plt
plt.rcParams['font.size'] = '16'
plt.rcParams['figure.dpi'] = 125
plt.rcParams['figure.facecolor'] = 'white'


import numpy as np
import pandas as pd
from obspy import  UTCDateTime, Trace


# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------

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

    # reclen
    reclen = raw_header['reclen'][0]
    header_list.append('reclen')
    header_values.append(reclen)

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


    return header_list

# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------



# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------

def read_waveforms_24bit_(file_name, header_df, record_num, sensitivity_, gain_):
    '''
    Help function that reads the waveforms of a SHRU 24bit .DXX acoustic binary file.
    
    parameters
    ----------
    file_name: numpy fromfile array
    header_df: header info in a data frame object
    record_num: record number (out of 128)
    sensitivity: default is 170. optional to set to different value or specify it per channel

    Returns
    -------
    Header structure containing the parameters names and values
    '''

    f_data = open(file_name, "rb")  # reopen the file
    data_binary = f_data.read()

    pos = 1024  #skip the length of the header
    l = int(header_df.loc['reclen'].values) #record length
    npts = int(header_df.loc['npts'].values)

    chan_num = int(header_df.loc['channels'].values)
    byte_step = 3
    pos_step = chan_num*byte_step # every 3 summed into a single data point

    scaling = (2.5/(2**23)/gain_)
    sensitivity = np.zeros(chan_num, dtype=np.float32)
    sensitivity[:] = 10**(sensitivity_/20)
    mPa_2_Pa = 1e-3

    channel = [[] for _ in range(chan_num)] # Initially save data as python list and not numpy array because .append to list is much much faster. 

    skip = l-pos
    if record_num==0:
        pos1 = pos
        pos2 = pos1 + l - pos
    else:
        
        pos1 = pos + l*record_num 
        pos2 = pos1 + l - pos

    for loc in range(pos1,pos2, pos_step):

        for c in range(0,chan_num):

            d = bytearray(data_binary[loc:loc+byte_step])
            dpoint = int.from_bytes(d, byteorder='big', signed=True) * scaling * sensitivity[c] * mPa_2_Pa
            channel[c].append(dpoint)
            loc+=byte_step

    channels = np.zeros([chan_num, len(channel[0])], dtype=np.float32)

    for c in range(0,chan_num):
        
        channels[c] = np.asarray(channel[c], dtype=np.float32)

    return channels

# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------



# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------

def read_waveforms_16bit_(file_name, header_df, record_num, sensitivity_, gain_):
    '''
    Help function that reads the waveforms of a SHRU 16bit .DXX acoustic binary file.
    
    parameters
    ----------
    file_name: numpy fromfile array
    header_df: header info in a data frame object
    record_num: record number (out of 128)
    sensitivity: default is 170. optional to set to different vakue or specify it per channel
    gain: default sensor gain is 20

    Returns
    -------
    Header structure containing the parameters names and values
    '''

    f_data = open(file_name, "rb")  # reopen the file
    data_binary = f_data.read()

    pos = 1024  #skip the length of the header
    l = int(header_df.loc['reclen'].values) #record length
    npts = int(header_df.loc['npts'].values)

    chan_num = int(header_df.loc['channels'].values)
    byte_step = 2
    pos_step = chan_num*byte_step # every 3 summed into a single data point

    
    scaling = (2.5/8192/gain_)
    sensitivity = np.zeros(chan_num, dtype=np.float32)
    sensitivity[:] = 10**(sensitivity_/20)
    mPa_2_Pa = 1e-3
    
    channel = [[] for _ in range(chan_num)] # Initially save data as python list and not numpy array because .append to list is much much faster. 

    skip = l-pos
    if record_num==0:
        pos1 = pos
        pos2 = pos1 + l - pos
    else:
        
        pos1 = pos + l*record_num 
        pos2 = pos1 + l - pos

    for loc in range(pos1,pos2, pos_step):

        for c in range(0,chan_num):

            d = bytearray(data_binary[loc:loc+byte_step])
            dpoint = int.from_bytes(d, byteorder='big', signed=True) 
            

            channel[c].append(dpoint)
            loc+=byte_step


    channels = np.zeros([chan_num, len(channel[0])], dtype=np.float32)


    for c in range(0,chan_num):
        
        channels[c] = np.asarray(channel[c], dtype=np.float32)

        ## following Keith's code faster version
        channels[c] = channels[c]/4
        mantissa = np.floor(channels[c])
        gain = 4*(channels[c] - mantissa)
        gain = 2**(3*gain)
        channels[c] = (channels[c]/gain) * scaling * sensitivity[c] * mPa_2_Pa

    return channels

# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------




# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------

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
    tr.stats.channel = 'FDH' # 
    tr.stats.starttime = header_df.loc['starttime'].values[0]
    tr.stats.sampling_rate = header_df.loc['sampling_rate'].values[0]
    tr.stats.delta = header_df.loc['delta'].values[0]
    tr.stats.npts = header_df.loc['npts'].values[0]
    tr.stats.calib = 1
    tr.stats.units = 'Pa'

    return tr

# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------

