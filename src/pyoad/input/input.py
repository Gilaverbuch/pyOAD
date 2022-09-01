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
from .help_functions_in import header_info_, read_waveforms_, trace_template_

def read_header_24bit(file_name):
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


    return header_df




def read_waveforms_24bit(file_name, header_df, records_range):
    '''
    This function reads the waveforms of a SHRU 24bit .DXX acoustic binary file. 
    One SHRU file nominally contains 128 records, specify a record number 
    So far the functions reads only the first record of the first channel. 
    
    
    parameters
    ----------
    file_name: path to file
    header_df: header info in a data frame object
    records_range: range of record sections to extract

    Returns
    -------
    numpy array with the data
    '''

    
    tr_template = trace_template_(header_df)
    num_points = int(header_df.loc['npts'].values)
    dt = float(header_df.loc['delta'].values)

    chan_num = int(header_df.loc['channels'].values)

    stream = Stream()

    for rec_num in records_range:

        channels = read_waveforms_(file_name, header_df, rec_num)
        stream_ = Stream()

        for c in range(0,chan_num):

            tr = tr_template.copy()
            tr.stats.starttime = tr.stats.starttime + num_points*dt*rec_num
            tr.stats.station = 'CHN0'+str(c+1)
            tr.data = channels[c]

            stream = stream + tr
            stream_ = stream_ + tr


        # save2mseed(stream_)




    return stream
