# -*- coding: utf-8 -*-
"""
Python module to read the .D binary data files

.. module:: output functions

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
import os
from tqdm import tqdm
from obspy import read_inventory, read, signal, UTCDateTime, Stream, Trace
# from .help_functions_out import 


def save2mseed_(waveforms, dir_name):


    print('Writing to MSEED...')
    for tr in tqdm(waveforms):

        r = dir_name
        y = str(tr.stats.starttime.year)+'/'
        n = tr.stats.network+'/'
        s = tr.stats.station+'/'
        name = tr.id + '.'+str(tr.stats.starttime.year) + '.'+ str(tr.stats.starttime.julday) + \
        '.'+ str(tr.stats.starttime.hour) + '.'+ str(tr.stats.starttime.minute) + '.'+ str(tr.stats.starttime.second) 
        fname = r+y+n+s+name
        


        try:
            tr.write(fname, format="MSEED")  
            
        except:
            
            if os.path.exists(r+y+n+s)==True:
                tr.write(fname, format="MSEED") 
                print('saving file')
            
            elif os.path.exists(r+y+n)==True:
                os.mkdir(r+y+n+s)
                tr.write(fname, format="MSEED")  
                print('creating station directory')

            elif os.path.exists(r+y)==True:
                os.mkdir(r+y+n)
                os.mkdir(r+y+n+s)
                tr.write(fname, format="MSEED")  
                print('creating network + station directories')

            elif os.path.exists(r)==True:
                os.mkdir(r+y)
                os.mkdir(r+y+n)
                os.mkdir(r+y+n+s)
                tr.write(fname, format="MSEED")  
                print('creating year + network + station directories')

            else:
                os.mkdir(r)
                os.mkdir(r+y)
                os.mkdir(r+y+n)
                os.mkdir(r+y+n+s)
                tr.write(fname, format="MSEED")  
                print('creating Results + year + network + station directories')

