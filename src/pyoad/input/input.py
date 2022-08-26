# -*- coding: utf-8 -*-
"""
Python module to read the .D binary data files

.. module:: input functions

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

from scipy import signal
from obspy import read_inventory, read, signal, UTCDateTime, Stream, Trace
from .help_functions import header_info_, read_waveforms_, trace_template_

def read_header(file_name):
    '''
    this function reads the header of a SHRU 24bit .DXX acoustic binary file. 
    
    parameters
    ----------
    file_name: path to file

    Returns
    -------
    Header structure containing the parameters names and values
    '''



    #this is the structure of the shru header
    shru_header = np.dtype([
                            ('rhkey', ('b',4)),
                            ('date', ('>u2', 2)), 
                            ('time', ('>u2', 2)),
                            
                            ('microsec', '>u2'), 
                            ('rec', '>u2'), 
                            ('chan', '>u2'), 
                            
                            ('npts', '>i4'), 
                            ('rhfs', '>f4'), 
                            ('unused1', ('b',2)), 
                            ('rectime', '>i4'),
                            
                            ('rhlat', ('b',16)),
                            ('rhlng', ('b',16)),
                            
                            ('nav120', ('>u4', 28)),
                            ('nav115', ('>u4', 28)),
                            ('nav110', ('>u4', 28)),
                            
                            ('pos', ('b',128)), 
                            
                            ('unused2',('b',208)),
                            
                            ('nav_day',  '>i2'),
                            ('nav_hour', '>i2'),
                            ('nav_min',  '>i2'),
                            ('nav_sec',  '>i2'),
                            ('lblnav_flag', '>i2'), 
                            
                            ('unused3', ('b', 2)),
                            
                            ('reclen',     '>u4'),
                            ('acq_day',    '>i2'),
                            ('acq_hour',   '>i2'),
                            ('acq_min',    '>i2'),
                            ('acq_sec',    '>i2'),
                            ('acq_recnum', '>i2'),
                            
                            ('ADC_tagbyte', '>i2'),
                            ('glitchcode', '>i2'),
                            ('bootflag', '>i2'),
                            
                            ('internal_temp', ('b', 16)), 
                            
                            ('bat_voltage', ('b', 16)),
                            ('bat_current', ('b', 16)), 
                            
                            ('status', ('b', 16)), 
                            ('project', ('b', 16)),
                            
                            ('shru_num', ('b', 16)),
                            
                            ('vla', ('b', 16)),
                            ('hla', ('b', 16)),
                            
                            ('file_name', ('b', 32) ),   #MMddhhmm.Dss
                            
                            ('record', ('b', 16)),
                            ('adate', ('b', 16)),
                            ('atime', ('b', 16)),
                            
                            ('file_length', '>u4'),
                            ('total_recoreds', '>u4'),
                            
                            ('unused4', ('b', 2)),
                            
                            ('adc_mode', '>i2'),
                            ('adc_clk_code', '>i2'),
                            
                            ('unused5', ('b', 2)),
                            
                            ('time_base', '>i4'),
                            
                            ('unused6', ('b', 12)),
                            ('unused7', ('b', 12)),
                            
                            ('rhkeyl', ('b', 4)) 
                                                     ])

    # reading the header
    header_raw = np.fromfile(file_name, dtype=shru_header)

    header_df = header_info_(header_raw)


    # print header 
    # data_type_1 = ['>u2', '>u4', 'uint16', 'uint32', 'int16', 'int32', 'float32']
    # skip_data = ['unused1', 'unused2', 'unused3', 'unused4', 'unused5', 'unused6', 'unused7', 
    #             'nav110', 'nav115', 'nav120', 'rhlat', 'rhlng', 'pos' ]

    # for name in shru_header.names:
    #     if name not in skip_data:

    #         if header_raw[name][0].dtype in data_type_1:

    #             print(name, header_raw[name][0])

    #         else:
    #             string = 0
    #             for c in header_raw[name][0]:
    #                 try:
    #                     string += chr(c)
    #                 except:
    #                     string = chr(c)

    #             print(name, string)


    

    return header_df




def read_waveforms(file_name, header_df):
    '''
    This function reads the waveforms of a SHRU 24bit .DXX acoustic binary file. 
    So far the functions reads only the first record of the first channel. 
    
    
    parameters
    ----------
    file_name: path to file

    Returns
    -------
    numpy array with the data
    '''

    # channel1, channel2, channel3, channel4 = read_waveforms_(file_name, header_df)
    channels = read_waveforms_(file_name, header_df)
    tr_template = trace_template_(header_df)

    chan_num = int(header_df.loc['channels'].values)

    stream = Stream()
    for c in range(0,chan_num):

        tr = tr_template.copy()
        tr.stats.station = 'CHN0'+str(c+1)
        tr.data = channels[c]

        stream = stream + tr



    return stream
