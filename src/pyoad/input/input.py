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
    D = np.fromfile(file_name, dtype=shru_header)


    # print header 
    data_type_1 = ['>u2', '>u4', 'uint16', 'uint32', 'int16', 'int32', 'float32']
    skip_data = ['unused1', 'unused2', 'unused3', 'unused4', 'unused5', 'unused6', 'unused7', 
                'nav110', 'nav115', 'nav120', 'rhlat', 'rhlng', 'pos' ]

    for name in shru_header.names:
        if name not in skip_data:

            if D[name][0].dtype in data_type_1:

                print(name, D[name][0])

            else:
                string = 0
                for c in D[name][0]:
                    try:
                        string += chr(c)
                    except:
                        string = chr(c)

                print(name, string)

    # put header in an xarray object that will later contain also the data. 
    # it will have a structure of Data['header'] and Data['data']...

    return D[:][0]     




def read_waveforms(file_name):
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

    f_data = open(file_name, "rb")  # reopen the file
    data_binary = f_data.read()

    pos = 1024
    l = (len(data_binary[pos:])//128)
    npts = 1048576

    channel1 = []

    for loc in range(pos,l, 12):
        
        d = bytearray(data_binary[loc:loc+3])
        d.append(0)
        dpoint = int.from_bytes(d, byteorder='big', signed=True) * (2.5/(2**23)/20)
        channel1.append(dpoint)

    channel1 = np.asarray(channel1, dtype=np.float32)
    
    return channel1
